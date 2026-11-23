# Member 1 verification - 23 November 2026

Repository snapshot is based on `origin/tharun` commit `3278a0f` with Kunal's new workflow services, tests and requirements handoff on the local team branch `kiunal`. Atul's UI branch is `a8ccd2d`. The local changes have not been pushed at this evidence snapshot because GitHub publishing authentication is pending.

## Executed checks

Environment used Python 3.14, repository-pinned Django 5.2.19, psycopg 3.3.9 and a disposable PostgreSQL 17.12 database on 127.0.0.1:55439. The PostgreSQL instance was shut down after the run. No feature data was written to a shared database.

| Command | Actual result |
| --- | --- |
| `python manage.py check` | Passed, zero issues |
| `python manage.py makemigrations --check --dry-run` | Passed, no changes detected |
| `python manage.py test --verbosity 2` | Passed, 29 tests |
| `git diff --check` | Passed |

The 29 tests comprise seven existing foundation tests and 22 new opportunity workflow tests. The latter execute the actual Django service functions against test-only UA-2 fixture tables, including transaction rollback after a failed audit-event write, ownership/role restrictions, incomplete drafts, returned correction/resubmission, stale snapshots, publication, manual closure, idempotent expiry, and exact-deadline/timezone checks.

Earlier local SQLite execution of the 22 workflow tests also passed. PostgreSQL is the full-suite evidence reported above. CI on the new workflow code remains pending publication and a real Actions run. Tharun's seven-test push-CI result is teammate-reported in KAN-44 comment 10026.

## Integration still required

DT-3 accounts, the production Opportunity/OpportunityEvent models and their migrations, and the KAN-46 views have not yet been implemented in the inspected repository. The integration contract specifies their field names and service entry points. The student list/detail/application views must call the shared open-record checks. Real-account permissions, UI end-to-end acceptance and concurrent application/closure behavior still require those modules.

## Requirements handoff

The assignment's synthetic-persona fallback was used to complete RA-3's process notes. Real interviews and participants both remain zero. RA-4 explicitly marks all eight department assumptions Unknown, with validation questions and consequences. Team state/baseline sign-off remains open in KAN-18/KAN-19. Atul's six design findings remain open because no revised attachments were supplied after the review. The current requirements-owner decisions retain the three roles, one organization per representative, and coordinator decline without a required recommendation from Under Review/Shortlisted.
