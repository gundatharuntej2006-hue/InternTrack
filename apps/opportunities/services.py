"""RA-11: transactional opportunity rules using the UA-2 field contract.

Views supply the authenticated account and an ORM Opportunity instance. The
model supplies `review_events`, the reverse OpportunityEvent relationship.
See docs/requirements/opportunity-integration.md for the pending model wiring.
"""

from datetime import datetime

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone


DRAFT = "DRAFT"
PENDING_REVIEW = "PENDING_REVIEW"
PUBLISHED = "PUBLISHED"
RETURNED = "RETURNED"
CLOSED = "CLOSED"

EDITABLE_FIELDS = {
    "title", "description", "eligibility", "mode", "location",
    "start_date", "end_date", "deadline", "mentor_id",
}


def _time(now):
    now = timezone.now() if now is None else now
    if not isinstance(now, datetime) or timezone.is_naive(now):
        raise ValidationError("Use a timezone-aware server timestamp.")
    return now


def _actor(actor, role):
    if not (getattr(actor, "is_authenticated", False)
            and getattr(actor, "is_active", False)
            and getattr(actor, "role", None) == role):
        raise PermissionDenied("This action is not permitted for this account.")


def _owner(actor, opportunity):
    _actor(actor, "ORG_REP")
    if not actor.organization_id or actor.organization_id != opportunity.organization_id:
        raise PermissionDenied("This opportunity belongs to another organization.")


def _locked(opportunity):
    current = type(opportunity).objects.select_for_update().get(pk=opportunity.pk)
    if current.updated_at != opportunity.updated_at:
        raise ValidationError("This opportunity changed. Reload and try again.")
    return current


def _submission_errors(opportunity, now):
    errors = {}
    for field in ("title", "description", "eligibility"):
        if not getattr(opportunity, field, "").strip():
            errors[field] = "Complete this field before submitting for review."
    if opportunity.mode not in ("REMOTE", "ONSITE", "HYBRID"):
        errors["mode"] = "Choose a valid internship mode."
    if opportunity.mode in ("ONSITE", "HYBRID") and not opportunity.location.strip():
        errors["location"] = "Enter a location for on-site or hybrid opportunities."
    if not opportunity.start_date:
        errors["start_date"] = "Enter the start date."
    if not opportunity.end_date:
        errors["end_date"] = "Enter the end date."
    if (opportunity.start_date and opportunity.end_date
            and opportunity.start_date > opportunity.end_date):
        errors["end_date"] = "End date must be on or after start date."
    deadline = opportunity.deadline
    if not isinstance(deadline, datetime) or timezone.is_naive(deadline):
        errors["deadline"] = "Enter a timezone-aware application deadline."
    elif deadline <= now:
        errors["deadline"] = "The application deadline must be in the future."
    if not opportunity.mentor_id:
        errors["mentor"] = "Choose a mentor from this organization."
    else:
        mentor = opportunity.mentor
        if (mentor.role != "ORG_REP" or not mentor.is_active
                or mentor.organization_id != opportunity.organization_id):
            errors["mentor"] = "Choose an active representative of this organization."
    if opportunity.organization.status != "ACTIVE":
        errors["organization"] = "The organization must be active before publication."
    return errors


def _validate_submission(opportunity, now):
    errors = _submission_errors(opportunity, now)
    if errors:
        raise ValidationError(errors)


def _record(opportunity, state, actor, reason=""):
    previous = opportunity.state
    opportunity.state = state
    fields = ["state", "updated_at"]
    if state == PUBLISHED:
        opportunity.approved_by = actor
        opportunity.approved_at = timezone.now()
        fields += ["approved_by", "approved_at"]
    if state == RETURNED:
        opportunity.return_reason = reason
        fields.append("return_reason")
    if state == CLOSED:
        opportunity.closed_reason = reason
        fields.append("closed_reason")
    opportunity.save(update_fields=fields)
    opportunity.review_events.create(
        from_state=previous, to_state=state, actor=actor, reason=reason,
    )
    return opportunity


def student_visible(queryset, *, now=None):
    """Filter listing and detail queries even when expiry maintenance is delayed."""
    return queryset.filter(state=PUBLISHED, deadline__gt=_time(now))


def require_open_for_application(opportunity, *, now=None):
    """Call on the locked row inside the application-creation transaction."""
    now = _time(now)
    if (opportunity.state != PUBLISHED or opportunity.deadline is None
            or opportunity.deadline <= now):
        raise ValidationError("This opportunity is closed to applications.")


@transaction.atomic
def save_draft(opportunity, actor, changes):
    """Save cleaned editable values. Complete fields are required on submit."""
    _owner(actor, opportunity)
    if set(changes) - EDITABLE_FIELDS:
        raise ValidationError("Only draft content fields may be edited.")
    current = _locked(opportunity) if opportunity.pk else opportunity
    _owner(actor, current)
    if current.state not in (DRAFT, RETURNED):
        raise ValidationError("Only Draft or Returned opportunities may be edited.")
    creating = current.pk is None
    for field, value in changes.items():
        setattr(current, field, value)
    if creating:
        current.created_by = actor
    current.save()
    if creating:
        current.review_events.create(from_state="", to_state=DRAFT, actor=actor, reason="")
    return current


@transaction.atomic
def submit_for_review(opportunity, actor, *, now=None):
    _owner(actor, opportunity)
    current = _locked(opportunity)
    _owner(actor, current)
    if current.state not in (DRAFT, RETURNED):
        raise ValidationError("Only Draft or Returned opportunities may be submitted.")
    _validate_submission(current, _time(now))
    return _record(current, PENDING_REVIEW, actor)


@transaction.atomic
def approve(opportunity, actor, *, now=None):
    _actor(actor, "COORDINATOR")
    current = _locked(opportunity)
    if current.state != PENDING_REVIEW:
        raise ValidationError("Only Pending Review opportunities may be published.")
    _validate_submission(current, _time(now))
    return _record(current, PUBLISHED, actor)


@transaction.atomic
def return_for_changes(opportunity, actor, reason):
    _actor(actor, "COORDINATOR")
    if not isinstance(reason, str) or not reason.strip():
        raise ValidationError("Explain what the organization should change.")
    current = _locked(opportunity)
    if current.state != PENDING_REVIEW:
        raise ValidationError("Only Pending Review opportunities may be returned.")
    return _record(current, RETURNED, actor, reason.strip())


@transaction.atomic
def close(opportunity, actor, reason):
    _actor(actor, "COORDINATOR")
    if not isinstance(reason, str) or not reason.strip():
        raise ValidationError("Enter a reason for closing the opportunity.")
    current = _locked(opportunity)
    if current.state != PUBLISHED:
        raise ValidationError("Only Published opportunities may be closed.")
    return _record(current, CLOSED, actor, reason.strip())


@transaction.atomic
def expire(opportunity, *, now=None):
    """Trusted scheduled-service entry point. Repeated expiry adds no event."""
    now = _time(now)
    current = type(opportunity).objects.select_for_update().get(pk=opportunity.pk)
    if current.state == CLOSED:
        return current
    if (current.state != PUBLISHED or current.deadline is None
            or current.deadline > now):
        raise ValidationError("This opportunity has not reached its publication deadline.")
    return _record(current, CLOSED, None, "Application deadline reached.")
