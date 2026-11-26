from datetime import timedelta, timezone as datetime_timezone
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import close_old_connections, connection, connections
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from apps.opportunities import services
from .opportunity_test_models import (
    ReviewAccount, ReviewOpportunity, ReviewOpportunityEvent, ReviewOrganization,
)


class OpportunityWorkflowTests(TestCase):
    """Run the real ORM services and transactions against isolated UA-2 tables."""

    @classmethod
    def setUpClass(cls):
        cls.fixture_models = [ReviewOrganization, ReviewAccount, ReviewOpportunity, ReviewOpportunityEvent]
        with connection.schema_editor() as editor:
            for model in cls.fixture_models:
                editor.create_model(model)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as editor:
            for model in reversed(cls.fixture_models):
                editor.delete_model(model)

    def setUp(self):
        self.now = timezone.now()
        self.org = ReviewOrganization.objects.create()
        self.other_org = ReviewOrganization.objects.create()
        self.rep = ReviewAccount.objects.create(role="ORG_REP", organization=self.org)
        self.other_rep = ReviewAccount.objects.create(role="ORG_REP", organization=self.other_org)
        self.coordinator = ReviewAccount.objects.create(role="COORDINATOR")
        self.student = ReviewAccount.objects.create(role="STUDENT")
        self.draft = ReviewOpportunity.objects.create(
            organization=self.org, created_by=self.rep, mentor=self.rep,
            title="Synthetic internship", description="Build a demo", eligibility="Demo cohort",
            mode="REMOTE", start_date=(self.now + timedelta(days=3)).date(),
            end_date=(self.now + timedelta(days=30)).date(), deadline=self.now + timedelta(days=2),
        )

    def pending(self):
        return services.submit_for_review(self.draft, self.rep, now=self.now)

    def published(self):
        return services.approve(self.pending(), self.coordinator, now=self.now)

    def test_publication_records_approval_and_history(self):
        opportunity = self.published()
        self.assertEqual(opportunity.state, services.PUBLISHED)
        self.assertEqual(opportunity.approved_by_id, self.coordinator.pk)
        self.assertIsNotNone(opportunity.approved_at)
        self.assertEqual(list(opportunity.review_events.order_by("id").values_list("to_state", flat=True)),
                         [services.PENDING_REVIEW, services.PUBLISHED])

    def test_all_nonpublished_states_hidden(self):
        for state in (services.DRAFT, services.PENDING_REVIEW, services.RETURNED, services.CLOSED):
            with self.subTest(state=state):
                ReviewOpportunity.objects.filter(pk=self.draft.pk).update(state=state)
                self.assertFalse(services.student_visible(ReviewOpportunity.objects.all(), now=self.now).exists())

    def test_exact_deadline_and_timezone(self):
        opportunity = self.published()
        records = ReviewOpportunity.objects.all()
        self.assertTrue(services.student_visible(records, now=opportunity.deadline-timedelta(microseconds=1)).exists())
        self.assertFalse(services.student_visible(records, now=opportunity.deadline).exists())
        local = opportunity.deadline.astimezone(datetime_timezone(timedelta(hours=5, minutes=30)))
        self.assertFalse(services.student_visible(records, now=local).exists())
        self.assertFalse(services.student_visible(records, now=opportunity.deadline+timedelta(seconds=1)).exists())

    def test_only_owner_can_submit(self):
        for actor in (self.other_rep, self.student, self.coordinator, AnonymousUser()):
            with self.subTest(actor=actor), self.assertRaises(PermissionDenied):
                services.submit_for_review(self.draft, actor)
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.state, services.DRAFT)
        self.assertEqual(self.draft.review_events.count(), 0)

    def test_inactive_actor_denied(self):
        self.rep.is_active = False
        with self.assertRaises(PermissionDenied):
            services.submit_for_review(self.draft, self.rep)

    def test_only_coordinator_can_publish_return_and_close(self):
        pending = self.pending()
        for action, args in ((services.approve, ()), (services.return_for_changes, ("Fix",)),
                             (services.close, ("Closed",))):
            with self.subTest(action=action), self.assertRaises(PermissionDenied):
                action(pending, self.rep, *args)

    def test_required_submission_fields(self):
        self.draft.description = " "
        self.draft.deadline = self.now
        self.draft.save()
        with self.assertRaises(ValidationError) as error:
            services.submit_for_review(self.draft, self.rep, now=self.now)
        self.assertIn("description", error.exception.message_dict)
        self.assertIn("deadline", error.exception.message_dict)

    def test_foreign_mentor_rejected(self):
        self.draft.mentor = self.other_rep
        self.draft.save()
        with self.assertRaises(ValidationError):
            services.submit_for_review(self.draft, self.rep)

    def test_onsite_requires_location_and_dates_valid(self):
        self.draft.mode = "ONSITE"
        self.draft.end_date = self.draft.start_date - timedelta(days=1)
        self.draft.save()
        with self.assertRaises(ValidationError) as error:
            services.submit_for_review(self.draft, self.rep)
        self.assertIn("location", error.exception.message_dict)
        self.assertIn("end_date", error.exception.message_dict)

    def test_inactive_organization_cannot_submit(self):
        self.org.status = "INACTIVE"
        self.org.save()
        with self.assertRaises(ValidationError):
            services.submit_for_review(self.draft, self.rep)

    def test_expired_pending_cannot_be_approved(self):
        pending = self.pending()
        with self.assertRaises(ValidationError):
            services.approve(pending, self.coordinator, now=pending.deadline)
        pending.refresh_from_db()
        self.assertEqual(pending.state, services.PENDING_REVIEW)
        self.assertEqual(pending.review_events.count(), 1)

    def test_return_requires_reason_and_supports_edit_resubmit(self):
        pending = self.pending()
        with self.assertRaises(ValidationError):
            services.return_for_changes(pending, self.coordinator, " ")
        returned = services.return_for_changes(pending, self.coordinator, " Clarify eligibility ")
        self.assertEqual(returned.return_reason, "Clarify eligibility")
        edited = services.save_draft(returned, self.rep, {"eligibility": "Updated cohort"})
        submitted = services.submit_for_review(edited, self.rep)
        self.assertEqual(submitted.state, services.PENDING_REVIEW)
        self.assertEqual(submitted.review_events.count(), 3)

    def test_partial_new_draft_can_save_but_not_submit(self):
        opportunity = ReviewOpportunity(organization=self.org)
        saved = services.save_draft(opportunity, self.rep, {"title": "Work in progress"})
        self.assertEqual(saved.created_by_id, self.rep.pk)
        self.assertEqual(saved.review_events.get().to_state, services.DRAFT)
        with self.assertRaises(ValidationError):
            services.submit_for_review(saved, self.rep)

    def test_draft_cannot_change_owner_or_publication_fields(self):
        for fields in ({"organization_id": self.other_org.pk}, {"state": services.PUBLISHED},
                       {"approved_by_id": self.rep.pk}):
            with self.subTest(fields=fields), self.assertRaises(ValidationError):
                services.save_draft(self.draft, self.rep, fields)

    def test_published_and_pending_cannot_be_edited(self):
        pending = self.pending()
        with self.assertRaises(ValidationError):
            services.save_draft(pending, self.rep, {"title": "Changed"})
        published = services.approve(pending, self.coordinator)
        with self.assertRaises(ValidationError):
            services.save_draft(published, self.rep, {"title": "Changed"})

    def test_stale_record_rejected_without_new_event(self):
        old = ReviewOpportunity.objects.get(pk=self.draft.pk)
        self.pending()
        with self.assertRaises(ValidationError):
            services.submit_for_review(old, self.rep)
        self.assertEqual(old.review_events.count(), 1)

    def test_atomic_event_failure_rolls_back_state_and_approval(self):
        pending = self.pending()
        with patch.object(ReviewOpportunityEvent, "save", side_effect=RuntimeError("write failed")):
            with self.assertRaises(RuntimeError):
                services.approve(pending, self.coordinator)
        pending.refresh_from_db()
        self.assertEqual(pending.state, services.PENDING_REVIEW)
        self.assertIsNone(pending.approved_at)
        self.assertIsNone(pending.approved_by_id)
        self.assertEqual(pending.review_events.count(), 1)

    def test_manual_close_hides_record_and_requires_reason(self):
        published = self.published()
        with self.assertRaises(ValidationError):
            services.close(published, self.coordinator, "")
        closed = services.close(published, self.coordinator, "Cohort filled")
        self.assertEqual(closed.state, services.CLOSED)
        self.assertFalse(services.student_visible(ReviewOpportunity.objects.all()).exists())

    def test_expiry_is_due_only_and_idempotent(self):
        published = self.published()
        with self.assertRaises(ValidationError):
            services.expire(published, now=self.now)
        closed = services.expire(published, now=published.deadline)
        self.assertEqual(closed.review_events.count(), 3)
        again = services.expire(published, now=published.deadline)
        self.assertEqual(again.review_events.count(), 3)
        self.assertIsNone(again.review_events.latest("id").actor_id)

    def test_application_guard_rechecks_state_and_deadline(self):
        with self.assertRaises(ValidationError):
            services.require_open_for_application(self.draft)
        published = self.published()
        services.require_open_for_application(published, now=self.now)
        with self.assertRaises(ValidationError):
            services.require_open_for_application(published, now=published.deadline)
        closed = services.close(published, self.coordinator, "Closed early")
        with self.assertRaises(ValidationError):
            services.require_open_for_application(closed, now=self.now)

    def test_naive_timestamp_is_rejected(self):
        with self.assertRaises(ValidationError):
            services.student_visible(ReviewOpportunity.objects.all(), now=self.now.replace(tzinfo=None))

    def test_unlisted_moves_rejected(self):
        with self.assertRaises(ValidationError):
            services.approve(self.draft, self.coordinator)
        published = self.published()
        with self.assertRaises(ValidationError):
            services.return_for_changes(published, self.coordinator, "Change")
        with self.assertRaises(ValidationError):
            services.submit_for_review(published, self.rep)


class OpportunityConcurrencyTests(TransactionTestCase):
    """Verify row locking with separate committed transactions/connections."""

    @classmethod
    def setUpClass(cls):
        cls.fixture_models = [ReviewOrganization, ReviewAccount, ReviewOpportunity, ReviewOpportunityEvent]
        with connection.schema_editor() as editor:
            for model in cls.fixture_models:
                editor.create_model(model)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as editor:
            for model in reversed(cls.fixture_models):
                editor.delete_model(model)

    @skipUnlessDBFeature("has_select_for_update")
    def test_concurrent_approve_and_return_allow_only_one_transition(self):
        organization = ReviewOrganization.objects.create()
        representative = ReviewAccount.objects.create(role="ORG_REP", organization=organization)
        coordinator = ReviewAccount.objects.create(role="COORDINATOR")
        now = timezone.now()
        opportunity = ReviewOpportunity.objects.create(
            organization=organization, created_by=representative, mentor=representative,
            title="Concurrent review", description="Synthetic work", eligibility="Demo cohort",
            mode="REMOTE", start_date=(now + timedelta(days=3)).date(),
            end_date=(now + timedelta(days=30)).date(), deadline=now + timedelta(days=2),
            state=services.PENDING_REVIEW,
        )
        both_loaded = Barrier(2)

        def decide(action):
            close_old_connections()
            try:
                snapshot = ReviewOpportunity.objects.get(pk=opportunity.pk)
                actor = ReviewAccount.objects.get(pk=coordinator.pk)
                both_loaded.wait(timeout=10)
                try:
                    if action == "approve":
                        updated = services.approve(snapshot, actor)
                    else:
                        updated = services.return_for_changes(snapshot, actor, "Clarify eligibility")
                    return "accepted", updated.state
                except ValidationError:
                    return "rejected", None
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as workers:
            approve_result = workers.submit(decide, "approve")
            return_result = workers.submit(decide, "return")
            results = [approve_result.result(timeout=20), return_result.result(timeout=20)]

        self.assertCountEqual([result[0] for result in results], ["accepted", "rejected"])
        opportunity.refresh_from_db()
        event = opportunity.review_events.get()
        self.assertEqual(event.from_state, services.PENDING_REVIEW)
        self.assertEqual(event.to_state, opportunity.state)
        accepted_state = next(state for result, state in results if result == "accepted")
        self.assertEqual(opportunity.state, accepted_state)
