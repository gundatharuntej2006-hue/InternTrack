"""Render every InternTrack template with fake data into tools/ui_preview_out/*.html.

Run from the repo root:   python tools/ui_preview.py
Then open tools/ui_preview_out/index.html in a browser.
No database needed. This only checks that templates render and look right.
"""
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace as NS

import django
import django.forms
from django.conf import settings
from django.urls import include, path

HERE = Path(__file__).resolve().parent.parent  # repo root
sys.path.insert(0, str(HERE / "apps" / "core"))
OUT = HERE / "tools" / "ui_preview_out"


def _v(request, *a, **k):  # dummy view, only needed so {% url %} can reverse
    return None


def ns(name, patterns):
    return path("", include((patterns, name)))


urlpatterns = [
    ns("accounts", [path("login/", _v, name="login"), path("logout/", _v, name="logout")]),
    ns("dashboard", [path("coordinator/", _v, name="queue"), path("notices/", _v, name="notices"),
                     path("coordinator/export.csv", _v, name="export")]),
    ns("opportunities", [
        path("opportunities/", _v, name="list"), path("opportunities/<int:pk>/", _v, name="detail"),
        path("coordinator/opportunities/", _v, name="review_list"),
        path("coordinator/opportunities/<int:pk>/approve/", _v, name="approve"),
        path("coordinator/opportunities/<int:pk>/return/", _v, name="return"),
        path("coordinator/opportunities/<int:pk>/close/", _v, name="close"),
        path("org/opportunities/", _v, name="org_list"), path("org/opportunities/new/", _v, name="create"),
        path("org/opportunities/<int:pk>/edit/", _v, name="edit"),
        path("org/opportunities/<int:pk>/submit/", _v, name="submit")]),
    ns("applications", [
        path("opportunities/<int:pk>/apply/", _v, name="apply"), path("my/applications/", _v, name="my_list"),
        path("coordinator/applications/", _v, name="review_list"),
        path("coordinator/applications/<int:pk>/decide/", _v, name="decide"),
        path("org/opportunities/<int:pk>/applicants/", _v, name="applicants"),
        path("org/applications/<int:pk>/recommend/", _v, name="recommend")]),
    ns("placements", [
        path("my/placement/", _v, name="my_placement"), path("my/placement/checkin/", _v, name="checkin"),
        path("mentor/checkins/", _v, name="mentor_checkins"),
        path("mentor/checkins/<int:pk>/feedback/", _v, name="feedback"),
        path("coordinator/placements/", _v, name="list"),
        path("coordinator/placements/<int:pk>/complete/", _v, name="complete")]),
]

settings.configure(
    DEBUG=True, ROOT_URLCONF=__name__, USE_TZ=False, TIME_ZONE="Asia/Kolkata", SECRET_KEY="preview-only",
    INSTALLED_APPS=["django.contrib.staticfiles"], STATIC_URL="../../static/",
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [str(HERE / "templates")],
                "OPTIONS": {"string_if_invalid": "[[MISSING %s]]"}}],
)
django.setup()

from django.core.paginator import Paginator  # noqa: E402
from django.template.loader import render_to_string  # noqa: E402

import forms as F  # noqa: E402

now = datetime(2026, 11, 25, 10, 30)
LABEL = {"SUBMITTED": "Submitted", "UNDER_REVIEW": "Under Review", "SHORTLISTED": "Shortlisted",
         "SELECTED": "Selected", "DECLINED": "Declined", "DRAFT": "Draft", "PENDING_REVIEW": "Pending Review",
         "PUBLISHED": "Published", "RETURNED": "Returned", "CLOSED": "Closed", "ACTIVE": "Active",
         "COMPLETED": "Completed", "SHORTLIST": "Shortlist", "SELECT": "Select", "DECLINE": "Decline"}

# ---- fake people and objects -------------------------------------------------
org_a, org_b = NS(name="Org A Analytics"), NS(name="Org B Software")
student = NS(name="Asha Rao", role="STUDENT", get_role_display="Student", is_authenticated=True, year_of_study=3)
student2 = NS(name="Ravi Kumar", role="STUDENT", get_role_display="Student", is_authenticated=True, year_of_study=4)
coord = NS(name="Dr. Coordinator", role="COORDINATOR", get_role_display="Coordinator", is_authenticated=True)
rep = NS(name="Meera (Org A)", role="ORG_REP", get_role_display="Organization rep", is_authenticated=True)


def opp(pk, title, org, state="PUBLISHED", mode="REMOTE", loc="", days=5, **kw):
    return NS(pk=pk, title=title, organization=org, state=state, get_state_display=LABEL[state], mode=mode,
              get_mode_display={"REMOTE": "Remote", "ONSITE": "On-site", "HYBRID": "Hybrid"}[mode], location=loc,
              deadline=now + timedelta(days=days), start_date=date(2027, 1, 4), end_date=date(2027, 3, 26),
              eligibility="3rd year or above. Basic Python and SQL.", mentor=rep,
              description="Clean and analyse a real dataset.\nBuild one dashboard and present findings.",
              return_reason=kw.get("return_reason", ""), applicant_count=kw.get("applicants", 0))


o1 = opp(1, "Data Analyst Intern", org_a, applicants=2)
o2 = opp(2, "Web Developer Intern", org_b, mode="ONSITE", loc="Bengaluru", days=10)
o3 = opp(3, "ML Research Intern", org_a, state="PENDING_REVIEW", mode="HYBRID", loc="Bengaluru")
o4 = opp(4, "QA Intern", org_a, state="RETURNED", return_reason="Add the eligibility details and a deadline.")
o5 = opp(5, "Cloud Intern", org_a, state="DRAFT")


def ev(days_ago, to, actor_role, reason="", actor=coord, note=""):
    return NS(created_at=now - timedelta(days=days_ago), to_status=to, get_to_status_display=LABEL[to],
              actor_role=actor_role, actor=actor, public_reason=reason, internal_note=note)


rec = NS(suggestion="SELECT", get_suggestion_display="Select", representative=rep, created_at=now - timedelta(days=2),
         rationale="Strong Python sample project and good availability.")
app1 = NS(pk=11, student=student, opportunity=o1, status="SELECTED", get_status_display="Selected",
          submitted_at=now - timedelta(days=6),
          public_next_step="Selection confirmed. Open your placement and review your learning goals.",
          statement="I enjoy working with data and built a small dashboard for a college club.",
          eligibility_answers={"year of study": "3", "skills": "Python, SQL, Excel"},
          public_events=[ev(6, "SUBMITTED", "Student", actor=student), ev(4, "UNDER_REVIEW", "Coordinator",
                         "Your application is being reviewed."), ev(1, "SELECTED", "Coordinator",
                         "Strong match for the Python requirement.")],
          latest_recommendation=rec, my_recommendation=rec)
app2 = NS(pk=12, student=student, opportunity=o2, status="SUBMITTED", get_status_display="Submitted",
          submitted_at=now - timedelta(days=1), public_next_step="Application received. Wait for coordinator review.",
          statement="I have built two Django projects.", eligibility_answers={"year of study": "3"},
          public_events=[ev(1, "SUBMITTED", "Student", actor=student)], latest_recommendation=None,
          my_recommendation=None)
app3 = NS(pk=13, student=student2, opportunity=o1, status="UNDER_REVIEW", get_status_display="Under Review",
          submitted_at=now - timedelta(days=3), public_next_step="", statement="I like statistics.",
          eligibility_answers={"year of study": "4", "skills": "R, Python"}, public_events=[],
          latest_recommendation=None, my_recommendation=None)

goals = [NS(pk=1, text="Clean and explore a real dataset"), NS(pk=2, text="Build one dashboard"),
         NS(pk=3, text="Present findings to the team")]
placement = NS(pk=21, opportunity=o1, student=student, mentor=rep, start_date=o1.start_date, end_date=o1.end_date,
               state="ACTIVE", get_state_display="Active", last_checkin_week=date(2027, 1, 11), is_overdue=False)
placement2 = NS(pk=22, opportunity=o2, student=student2, mentor=rep, start_date=o2.start_date, end_date=o2.end_date,
                state="ACTIVE", get_state_display="Active", last_checkin_week=None, is_overdue=True)
fb = NS(comment="Good progress. Try grouping by month next.", mentor=rep, responded_at=now)
c1 = NS(pk=31, placement=placement, goal=goals[0], week_start=date(2027, 1, 4),
        accomplishment="Cleaned the sales dataset and removed duplicates.", blocker="",
        next_step="Start the dashboard.", feedback=fb)
c2 = NS(pk=32, placement=placement, goal=goals[1], week_start=date(2027, 1, 11),
        accomplishment="Built first two charts.", blocker="Not sure which chart suits monthly trends.",
        next_step="Finish filters.", feedback=None)

class LoginForm(django.forms.Form):
    """Same field names as Django's AuthenticationForm (username, password); no database needed."""
    username = django.forms.EmailField(label="University email", widget=django.forms.EmailInput(attrs={"autocomplete": "username"}))
    password = django.forms.CharField(label="Password", widget=django.forms.PasswordInput(attrs={"autocomplete": "current-password"}))


goal_choices = [(g.pk, g.text) for g in goals]
bad_apply = F.ApplicationForm(data={"statement": "", "year_of_study": ""})
bad_apply.is_valid()
bad_apply.add_error(None, "You have already applied to this opportunity.")

PAGES = [
    ("login", "accounts/login.html", NS(is_authenticated=False), "L1 Login", {"form": LoginForm(), "next": ""}),
    ("s1_list", "opportunities/list.html", student, "S1 Opportunity list",
     {"nav": "opportunities", "filter_form": F.OpportunityFilterForm(), "query_string": "",
      "page_obj": Paginator([o1, o2], 20).page(1)}),
    ("s1_empty", "opportunities/list.html", student, "S1 Opportunity list (empty)",
     {"nav": "opportunities", "filter_form": F.OpportunityFilterForm(data={"q": "zzz"}), "query_string": "",
      "page_obj": Paginator([], 20).page(1)}),
    ("s2_detail", "opportunities/detail.html", student, "S2 Detail (can apply)",
     {"nav": "opportunities", "opportunity": o2, "existing_application": None, "is_open": True}),
    ("s2_applied", "opportunities/detail.html", student, "S2 Detail (already applied)",
     {"nav": "opportunities", "opportunity": o1, "existing_application": app1, "is_open": True}),
    ("s3_apply", "applications/apply.html", student, "S3 Apply form", {"opportunity": o2, "form": F.ApplicationForm()}),
    ("s3_errors", "applications/apply.html", student, "S3 Apply form (errors)", {"opportunity": o1, "form": bad_apply}),
    ("s4_my_apps", "applications/my_list.html", student, "S4 My applications",
     {"nav": "applications", "applications": [app1, app2]}),
    ("s5_placement", "placements/my_placement.html", student, "S5 My placement",
     {"nav": "placement", "placement": placement, "goals": goals, "checkins": [c1, c2],
      "can_submit_this_week": True, "this_week": date(2027, 1, 18)}),
    ("s6_checkin", "placements/checkin_form.html", student, "S6 Weekly check-in",
     {"nav": "placement", "placement": placement, "week_start": date(2027, 1, 18),
      "form": F.CheckInForm(goal_choices=goal_choices)}),
    ("c1_queue", "dashboard/queue.html", coord, "C1 Needs-action queue",
     {"nav": "queue", "counts": {"pending_opportunities": 1, "pending_decisions": 2, "overdue_checkins": 1},
      "items": [NS(label="ML Research Intern", kind="Opportunity approval", url="#", since=now - timedelta(days=2)),
                NS(label="Ravi Kumar - Data Analyst Intern", kind="Decision waiting", url="#",
                   since=now - timedelta(days=1)),
                NS(label="Ravi Kumar - check-in week of 4 Jan", kind="Overdue check-in", url="#",
                   since=now - timedelta(days=9))]}),
    ("c2_review", "opportunities/review_list.html", coord, "C2 Opportunities to review",
     {"nav": "opportunities", "opportunities": [o3], "published": [o1, o2]}),
    ("c3_apps", "applications/review_list.html", coord, "C3 Applications",
     {"nav": "applications", "query_string": "", "page_obj": Paginator([app3, app2, app1], 20).page(1),
      "filter_form": F.ApplicationFilterForm(opportunity_choices=[(1, o1.title), (2, o2.title)])}),
    ("c4_decide", "applications/decide.html", coord, "C4 Decision form",
     {"nav": "applications", "application": app3, "recommendation": rec,
      "form": F.DecisionForm(current_status="UNDER_REVIEW"),
      "events": [ev(3, "SUBMITTED", "Student", actor=student2), ev(2, "UNDER_REVIEW", "Coordinator",
                 "Your application is being reviewed.", note="Check availability in January.")]}),
    ("c5_placements", "placements/list.html", coord, "C5 Placements",
     {"nav": "placements", "placements": [placement, placement2], "overdue_only": False}),
    ("notices", "dashboard/notices.html", student, "Notices",
     {"nav": "notices", "notices": [NS(message="Your application status changed.", url="#", created_at=now,
                                       read_at=None),
                                    NS(message="Your mentor replied to your check-in.", url="#",
                                       created_at=now - timedelta(days=2), read_at=now)]}),
    ("o1_org_list", "opportunities/org_list.html", rep, "O1 My opportunities",
     {"nav": "opportunities", "opportunities": [o1, o3, o4, o5]}),
    ("o2_form", "opportunities/form.html", rep, "O2 Opportunity form (returned)",
     {"nav": "opportunities", "opportunity": o4,
      "form": F.OpportunityForm(mentor_choices=[(1, "Meera (Org A)")])}),
    ("o3_applicants", "applications/applicants.html", rep, "O3 Applicants",
     {"nav": "opportunities", "opportunity": o1, "applications": [app1, app3]}),
    ("o4_checkins", "placements/mentor_checkins.html", rep, "O4 Mentor check-ins",
     {"nav": "checkins", "checkins": [c2, c1]}),
]


def main():
    OUT.mkdir(exist_ok=True)
    links, problems = [], []
    for slug, tpl, user, title, ctx in PAGES:
        ctx = {"user": user, "notice_count": 1 if getattr(user, "is_authenticated", False) else 0, **ctx}
        html = render_to_string(tpl, ctx)
        # preview pages live in preview/, so point the stylesheet one folder up
        html = html.replace('href="static/', 'href="../../static/').replace('href="/static/', 'href="../../static/')
        if "[[MISSING" in html:
            problems.append(slug)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        links.append(f'<li><a href="{slug}.html">{title}</a> <small>({tpl})</small></li>')
    (OUT / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>InternTrack preview</title>"
        "<link rel='stylesheet' href='../../static/css/app.css'><main><h1>InternTrack screen preview</h1>"
        "<p class='lead'>Fake data only. Links inside pages point to real app URLs and will not work here.</p>"
        f"<ol>{''.join(links)}</ol></main>", encoding="utf-8")
    print(f"Rendered {len(PAGES)} pages into {OUT}")
    print("Missing variables in: " + (", ".join(problems) if problems else "none"))


if __name__ == "__main__":
    main()
