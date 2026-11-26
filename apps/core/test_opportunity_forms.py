from datetime import timedelta

from django.test import SimpleTestCase
from django.utils import timezone

from .forms import OpportunityForm


class OpportunityDraftFormTests(SimpleTestCase):
    """Draft saving must stay possible while submission enforces completeness."""

    def full_data(self):
        deadline = timezone.localtime(timezone.now() + timedelta(days=5))
        return {
            "title": "Synthetic opportunity", "description": "Demo work",
            "eligibility": "Demo cohort", "mode": "REMOTE", "location": "",
            "deadline": deadline.strftime("%Y-%m-%dT%H:%M"),
            "start_date": (deadline + timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (deadline + timedelta(days=30)).strftime("%Y-%m-%d"),
            "mentor": "1",
        }

    def form(self, data, *, submitting=False):
        return OpportunityForm(data=data, submitting=submitting, mentor_choices=[("1", "Demo mentor")])

    def test_title_only_draft_is_valid(self):
        form = self.form({"title": "Work in progress"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_onsite_draft_can_defer_location(self):
        form = self.form({"title": "Work in progress", "mode": "ONSITE"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_hybrid_draft_can_defer_location(self):
        form = self.form({"title": "Work in progress", "mode": "HYBRID"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_submission_requires_mode(self):
        form = self.form({**self.full_data(), "mode": ""}, submitting=True)
        self.assertFalse(form.is_valid())
        self.assertIn("mode", form.errors)

    def test_onsite_submission_requires_location(self):
        form = self.form({**self.full_data(), "mode": "ONSITE"}, submitting=True)
        self.assertFalse(form.is_valid())
        self.assertIn("location", form.errors)

    def test_complete_remote_submission_is_valid(self):
        form = self.form(self.full_data(), submitting=True)
        self.assertTrue(form.is_valid(), form.errors)
