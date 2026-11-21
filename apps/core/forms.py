"""InternTrack form definitions matching the UA-3 form contract.

Field names here are what the templates in frontend/templates expect.
When the real models exist, the ModelForm versions should keep the same field names.
Ownership fields (student, organization, actor) are never form fields: views set them from request.user.
"""
from django import forms

MODE_CHOICES = [("REMOTE", "Remote"), ("ONSITE", "On-site"), ("HYBRID", "Hybrid")]
APPLICATION_STATUS_CHOICES = [
    ("SUBMITTED", "Submitted"), ("UNDER_REVIEW", "Under Review"), ("SHORTLISTED", "Shortlisted"),
    ("SELECTED", "Selected"), ("DECLINED", "Declined"),
]
# Allowed next statuses (KAN-18 state contract v0.1)
NEXT_STATUSES = {
    "SUBMITTED": ["UNDER_REVIEW"],
    "UNDER_REVIEW": ["SHORTLISTED", "SELECTED", "DECLINED"],
    "SHORTLISTED": ["SELECTED", "DECLINED"],
}
SUGGESTION_CHOICES = [("SHORTLIST", "Shortlist"), ("SELECT", "Select"), ("DECLINE", "Decline")]
YEAR_CHOICES = [("", "Choose...")] + [(str(i), f"Year {i}") for i in range(1, 6)]


class OpportunityFilterForm(forms.Form):
    q = forms.CharField(label="Search", required=False, help_text="Title or organization")
    mode = forms.ChoiceField(label="Mode", required=False, choices=[("", "Any")] + MODE_CHOICES)
    location = forms.CharField(label="Location", required=False)


class OpportunityForm(forms.Form):
    title = forms.CharField(max_length=150)
    description = forms.CharField(widget=forms.Textarea)
    eligibility = forms.CharField(widget=forms.Textarea, help_text="Who can apply, for example year and skills")
    mode = forms.ChoiceField(choices=MODE_CHOICES)
    location = forms.CharField(max_length=150, required=False, help_text="Required unless Remote")
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
                                   help_text="Applications close at this time")
    mentor = forms.ChoiceField(choices=[], help_text="A representative of your organization")

    def __init__(self, *args, mentor_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mentor"].choices = [("", "Choose...")] + list(mentor_choices)

    def clean(self):
        data = super().clean()
        if data.get("start_date") and data.get("end_date") and data["start_date"] > data["end_date"]:
            self.add_error("end_date", "End date must be on or after the start date.")
        if data.get("mode") in ("ONSITE", "HYBRID") and not data.get("location"):
            self.add_error("location", "Location is required for on-site and hybrid internships.")
        return data


class ApplicationForm(forms.Form):
    statement = forms.CharField(label="Why are you interested?", max_length=1000, widget=forms.Textarea,
                                help_text="Up to 1000 characters")
    year_of_study = forms.ChoiceField(label="Year of study", choices=YEAR_CHOICES)
    skills = forms.CharField(label="Relevant skills", max_length=300, required=False)


class ApplicationFilterForm(forms.Form):
    opportunity = forms.ChoiceField(label="Opportunity", required=False, choices=[])
    status = forms.ChoiceField(label="Status", required=False, choices=[("", "Any")] + APPLICATION_STATUS_CHOICES)

    def __init__(self, *args, opportunity_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opportunity"].choices = [("", "Any")] + list(opportunity_choices)


class DecisionForm(forms.Form):
    new_status = forms.ChoiceField(label="New status", choices=[])
    public_reason = forms.CharField(label="Reason (the student will see this)", max_length=500, widget=forms.Textarea)
    public_next_step = forms.CharField(label="Next step for the student", max_length=300)
    internal_note = forms.CharField(label="Internal note (never shown to the student)", required=False,
                                    widget=forms.Textarea)
    goal_1 = forms.CharField(label="Learning goal 1", max_length=200, required=False)
    goal_2 = forms.CharField(label="Learning goal 2", max_length=200, required=False)
    goal_3 = forms.CharField(label="Learning goal 3 (optional)", max_length=200, required=False)

    def __init__(self, *args, current_status="SUBMITTED", **kwargs):
        super().__init__(*args, **kwargs)
        labels = dict(APPLICATION_STATUS_CHOICES)
        self.fields["new_status"].choices = [("", "Choose...")] + [
            (s, labels[s]) for s in NEXT_STATUSES.get(current_status, [])]

    def clean(self):
        data = super().clean()
        if data.get("new_status") == "SELECTED":
            if not data.get("goal_1") or not data.get("goal_2"):
                raise forms.ValidationError("A selection needs at least 2 learning goals.")
        return data


class RecommendationForm(forms.Form):
    suggestion = forms.ChoiceField(label="Recommendation", choices=[("", "Choose...")] + SUGGESTION_CHOICES)
    rationale = forms.CharField(label="Why", max_length=1000, widget=forms.Textarea)


class ReasonForm(forms.Form):
    """Used for Return and Close of an opportunity."""
    reason = forms.CharField(max_length=1000, widget=forms.Textarea)


class CheckInForm(forms.Form):
    goal = forms.ChoiceField(label="Learning goal this week", choices=[])
    accomplishment = forms.CharField(label="What I completed", max_length=1000, widget=forms.Textarea)
    blocker = forms.CharField(label="Blocker (optional)", max_length=1000, required=False, widget=forms.Textarea)
    next_step = forms.CharField(label="Next step", max_length=1000, widget=forms.Textarea)

    def __init__(self, *args, goal_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["goal"].choices = [("", "Choose...")] + list(goal_choices)


class FeedbackForm(forms.Form):
    comment = forms.CharField(label="Your feedback", max_length=1000, widget=forms.Textarea)
