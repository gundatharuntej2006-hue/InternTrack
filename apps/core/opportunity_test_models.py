"""Test-only UA-2 fixtures while DT-3/DT models are being implemented.

These unmanaged models are imported only by the workflow tests. Tests create
and remove their tables explicitly, without altering production migrations.
"""

from django.db import models


class ReviewOrganization(models.Model):
    status = models.CharField(max_length=20, default="ACTIVE")

    class Meta:
        app_label = "core"
        managed = False


class ReviewAccount(models.Model):
    role = models.CharField(max_length=20)
    organization = models.ForeignKey(ReviewOrganization, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        app_label = "core"
        managed = False


class ReviewOpportunity(models.Model):
    organization = models.ForeignKey(ReviewOrganization, on_delete=models.PROTECT)
    created_by = models.ForeignKey(ReviewAccount, on_delete=models.PROTECT, related_name="drafts")
    mentor = models.ForeignKey(ReviewAccount, null=True, on_delete=models.PROTECT, related_name="mentored")
    approved_by = models.ForeignKey(ReviewAccount, null=True, on_delete=models.PROTECT, related_name="approved")
    approved_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=150, blank=True, default="")
    description = models.TextField(blank=True, default="")
    eligibility = models.TextField(blank=True, default="")
    mode = models.CharField(max_length=20, blank=True, default="")
    location = models.CharField(max_length=150, blank=True, default="")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    deadline = models.DateTimeField(null=True)
    state = models.CharField(max_length=20, default="DRAFT")
    return_reason = models.TextField(default="")
    closed_reason = models.TextField(default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "core"
        managed = False


class ReviewOpportunityEvent(models.Model):
    opportunity = models.ForeignKey(ReviewOpportunity, related_name="review_events", on_delete=models.CASCADE)
    from_state = models.CharField(max_length=20)
    to_state = models.CharField(max_length=20)
    actor = models.ForeignKey(ReviewAccount, null=True, on_delete=models.PROTECT)
    reason = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "core"
        managed = False
