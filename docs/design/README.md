# UI design and templates (Member 3: UI Design and Architecture)

Jira epic: KAN-5.

## Design documents (open in a browser)

| File | Jira | Contents |
|---|---|---|
| `UA1_navigation_wireframes.html` | KAN-44 | Navigation map, 16 wireframes, clickable demo path |
| `UA2_schema_permissions.html` | KAN-45 | ER diagram, 12 tables, status values, constraints, permission matrix |
| `UA3_architecture_contracts.html` | KAN-46 | Architecture, deployment, URL contract, form contract, labels, notifications |

## Templates and static files

- `templates/`: 20 page templates plus shared parts in `templates/includes/`.
- `static/css/app.css`: one stylesheet for every page (found through `STATICFILES_DIRS`).
- `apps/core/forms.py`: every form from the UA-3 form contract. Field names match the templates.

Preview every page with fake data, without a database:

```bash
python tools/ui_preview.py
# then open tools/ui_preview_out/index.html
```

## What each view must provide

Templates use URL names such as `{% url 'opportunities:list' %}`, so each app needs
`app_name` set to the namespace below. Every page also expects `user` (with `role`,
`name`, `get_role_display`) and, optionally, `notice_count` and `nav` (highlights the menu item).

| Template | URL name | Context |
|---|---|---|
| `accounts/login.html` | `accounts:login`, `accounts:logout` | `form` (AuthenticationForm), `next` |
| `opportunities/list.html` | `opportunities:list` | `filter_form` (OpportunityFilterForm), `page_obj`, `query_string` |
| `opportunities/detail.html` | `opportunities:detail` | `opportunity`, `existing_application` (or None), `is_open` |
| `applications/apply.html` | `applications:apply` | `opportunity`, `form` (ApplicationForm) |
| `applications/my_list.html` | `applications:my_list` | `applications`, each with `public_events` (events without internal notes; each event has `actor_role`) |
| `placements/my_placement.html` | `placements:my_placement` | `placement` (Active, else latest Completed, else None), `goals`, `checkins` (each with `feedback` or None; feedback has `mentor`, `comment`, `responded_at`), `can_submit_this_week`, `this_week` |
| `placements/checkin_form.html` | `placements:checkin` | `placement`, `week_start`, `form` (CheckInForm) |
| `dashboard/queue.html` | `dashboard:queue`, `dashboard:export` | `counts` (`pending_opportunities`, `pending_decisions`, `overdue_checkins`), `items` (`label`, `kind`, `url`, `since`) |
| `opportunities/review_list.html` | `opportunities:review_list`, `:approve`, `:return`, `:close` | `opportunities` (pending), `published` |
| `applications/review_list.html` | `applications:review_list` | `filter_form` (ApplicationFilterForm), `page_obj` (each with `latest_recommendation`), `query_string` |
| `applications/decide.html` | `applications:decide` | `application` (shows `application.opportunity.mentor`), `recommendation`, `form` (DecisionForm with `current_status`), `events` |
| `placements/list.html` | `placements:list`, `placements:complete` | `placements` (each with `last_checkin_week`, `is_overdue`), `overdue_only` |
| `dashboard/notices.html` | `dashboard:notices` | `notices` (`message`, `url`, `created_at`, `read_at`) |
| `opportunities/org_list.html` | `opportunities:org_list`, `:create`, `:edit` | `opportunities` (each with `applicant_count`) |
| `opportunities/form.html` | `opportunities:create`, `:edit` | `opportunity` (None when new), `form` (OpportunityForm, `submitting=True` when the POST has `action=submit`) |
| `applications/applicants.html` | `applications:applicants`, `applications:recommend` | `opportunity`, `applications` (each with `my_recommendation`) |
| `placements/mentor_checkins.html` | `placements:mentor_checkins`, `placements:feedback` | `checkins` |

The menu in `base.html` only shows a link once its URL name exists, so placeholder
pages can extend `base.html` before every feature app is built.

`placement.opportunity` is a model property returning `placement.application.opportunity`.
Status and choice fields use the `get_<field>_display` labels from UA-2.

Times: `TIME_ZONE` defaults to `Asia/Kolkata`; templates print deadlines as `5 Dec 2026, 17:00 IST`.
