# RA-10 traceability update

Version 0.2, 20 November 2026. Screen evidence now comes from KAN-44, template archive 10007 on KAN-47 and URL contracts on KAN-46. US/AC definitions remain in KAN-17. These screen IDs follow Atul's actual naming. Test IDs are specifications until integrated executable test links are provided.

| Requirement | Story / AC | Actual design and template evidence | Test specification | Evidence status |
| --- | --- | --- | --- | --- |
| FR1 Must | US-01 AC1.1-1.4 | KAN-44 L1; accounts/login.html; base.html role navigation; KAN-45 permission matrix | AT01 valid/invalid login, AT02 cross-user/org/mentor direct access | Design mapped. Server authorization tests pending. |
| FR2 Must | US-02 AC2.1-2.3 | KAN-44 O1/O2; opportunities/org_list.html and form.html; KAN-45 Opportunity | AT03 draft/save/submit and hidden records, AT04 unauthorized edit | UI-01 and UI-05 logged. |
| FR3 Must | US-03 AC3.1-3.4 | KAN-44 C2/S1; opportunities/review_list.html and list.html; KAN-46 approve/return/close URLs | AT05 transitions, AT06 expiry/permissions/stale updates | UI-02/UI-04. Local pure opportunity tests exist in tests/test_opportunity_rules.py. DB/app/CI results pending. |
| FR4 Must | US-04 AC4.1-4.4 | KAN-44 S1/S2/S3; opportunities/list.html, detail.html; applications/apply.html | AT07 open/filter/apply, AT08 duplicate/concurrent/late/exact deadline (T1/T2) | Design mapped. UI-02. Integrated tests pending. |
| FR5 Must | US-05 AC5.1-5.3 | KAN-44 O3/C3; applications/applicants.html and review_list.html; KAN-45 Recommendation | AT09 ownership, AT10 advice leaves public status unchanged (T3/T4) | Design mapped. Permission tests pending. |
| FR6 Must | US-06 AC6.1-6.4 | KAN-44 C4/S4; applications/decide.html and my_list.html; forms.py NEXT_STATUSES; KAN-45 StatusEvent | AT11 transition/reason, AT12 event atomicity/private text | Names and NEXT_STATUSES match. Runtime and data isolation pending. |
| FR7 Must | US-07 AC7.1-7.3 | KAN-44 C4/S5; applications/decide.html, placements/my_placement.html; KAN-45 Placement/LearningGoal constraints | AT13 goals, AT14 rollback/mentor validation, AT15 concurrent selection/one-active (T5/T6) | UI-04. PostgreSQL transaction tests pending. |
| FR8 Must | US-08 AC8.1-8.4 | KAN-44 S5/S6/O4/C5; placements/my_placement.html, checkin_form.html, mentor_checkins.html and list.html | AT16 weekly/goal uniqueness, AT17 assigned mentor, AT18 final-check-in completion (T7/T8) | UI-03. Final-check-in condition and one-feedback policy require team confirmation. |
| FR9 Should with minimum pending list Must | US-09 AC9.1-9.3 | KAN-44 C1/C3/C5; dashboard/queue.html; placements/list.html | AT19 seeded count reconciliation, AT20 overdue/week/timezone (T10) | Design mapped. Actual queue counts/boundaries pending. |
| FR10 Should | US-10 AC10.1-10.3 | dashboard/notices.html; KAN-46 /notices/ and notification recipient table; KAN-45 Notification | AT21 committed notices, AT22 recipient isolation/no rollback notices | UI-06 logged. Publication recipients need contract correction if retained. |
| FR11 Could | US-11 AC11.1-11.3 | KAN-46 /coordinator/export.csv; KAN-45 coordinator-only aggregate export | AT23 aggregate reconciliation/no identifiers | Endpoint contract only. Export implementation/retention in scope pending. |

Cross-cutting checks remain AT24 keyboard/screen-reader/reflow, AT25 load/p95, AT26 backup/restore, AT27 security/CSRF/rate limit, AT28 clean setup/migrations. KAN-49 tracks Atul's accessibility work. No integrated pass is recorded without an actual build, command/steps and result.

## Executable opportunity evidence - 24 November 2026

PR #1 is merged to main at 75fa89a49dde50296126e1a070db15d3a2ef5a37. Main CI passed at https://github.com/gundatharuntej2006-hue/InternTrack/actions/runs/45221251506 . FR2/FR3 now have actual Django services in apps/opportunities/services.py and PostgreSQL-backed tests in apps/core/test_opportunities.py. Test fixture tables are in apps/core/opportunity_test_models.py. These supplement the original proposed AT03-AT06 mappings above.

- FR2 AC2.1/2.3 maps to partial-draft/submission validation, ownership, protected-field and returned-edit/resubmit tests.
- FR2 AC2.2 / FR3 AC3.3 maps to test_all_nonpublished_states_hidden and test_exact_deadline_and_timezone.
- FR3 AC3.1/3.2 maps to publication approval/history and coordinator/return-reason validation tests.
- FR3 AC3.4 maps to test_stale_record_rejected_without_new_event, test_atomic_event_failure_rolls_back_state_and_approval, and the 24 November concurrency candidate test_concurrent_approve_and_return_allow_only_one_transition.
- FR4 AC4.4 has application guard evidence in test_application_guard_rechecks_state_and_deadline. Actual Application insertion/uniqueness tests are still pending.

The 24 November local PostgreSQL run passed 30 tests, including 23 opportunity tests and seven foundation tests. Review outcomes are recorded in acceptance-review-2026-11-24.md and status-wording-audit-2026-11-24.md. Other Must-FR runtime mappings remain pending their modules. KAN-22 remains In Progress.

Naming correction to the initial assignment references follows actual Jira tasks. UA-1 wireframes are KAN-44, UA-2 schema is KAN-45, UA-3 contracts are KAN-46, UA-4/5 templates are KAN-47/48. Repository/setup is KAN-28 and CI is KAN-29. Exact links supersede the earlier placeholder UA-2/UA-5 references.
