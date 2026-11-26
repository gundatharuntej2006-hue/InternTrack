# RA-13 acceptance review - 24 November 2026

Reviewer is Kunal's Requirement and Analysis workstream. The accepted repository snapshot is main merge 75fa89a49dde50296126e1a070db15d3a2ef5a37, merged on 23 November at 22:21 IST. Main CI passed at https://github.com/gundatharuntej2006-hue/InternTrack/actions/runs/45221251506 . PR #1 was merged by account Rengoku9000. There are no recorded GitHub reviews or review comments. Requirements/state sign-off remains tracked separately in KAN-18/KAN-19.

## Acceptance evidence

The 24 November candidate adds a PostgreSQL concurrency regression to the unchanged workflow services. Local PostgreSQL execution passed all 30 tests, comprising 23 opportunity tests and seven foundation tests. Django check and migration check passed. The new test starts separate database transactions from the same Pending Review snapshot. One coordinator approval/return succeeds and the stale competing decision is rejected. The final state has exactly one matching audit event.

| Acceptance area | Expected | Observed evidence | Current outcome |
| --- | --- | --- | --- |
| FR2 partial draft and submit | Save incomplete draft, reject incomplete review submission | test_partial_new_draft_can_save_but_not_submit | Service test passed; UI/form/model alignment open |
| FR2 ownership | Own organization only; exclude posted ownership/approval fields | test_only_owner_can_submit, test_draft_cannot_change_owner_or_publication_fields | Service tests passed; actual-login/object-route tests pending |
| FR2/FR3 correction | Return with reason, edit, resubmit and retain events | test_return_requires_reason_and_supports_edit_resubmit | Service test passed; prototype edit/resubmit finding UI-05 open |
| FR3 approval | Coordinator publishes only a valid pending opportunity | test_publication_records_approval_and_history, test_only_coordinator_can_publish_return_and_close | Service tests passed; production endpoint acceptance pending |
| FR3 student visibility | Only Published and before deadline | test_all_nonpublished_states_hidden, test_exact_deadline_and_timezone | Query tests passed; student list/detail integration pending |
| FR3 audit reliability | State/event commit together or roll back | test_atomic_event_failure_rolls_back_state_and_approval | PostgreSQL transaction test passed |
| FR3 competing review actions | One transition wins, stale competing action is rejected | test_concurrent_approve_and_return_allow_only_one_transition | Separate-connection PostgreSQL test passed in 24 November candidate |
| FR3 closure | Manual close hides record; due expiry is idempotent | test_manual_close_hides_record_and_requires_reason, test_expiry_is_due_only_and_idempotent | Service tests passed; close view/scheduler wiring pending |
| FR4 application guard | Recheck state/deadline within application transaction | test_application_guard_rechecks_state_and_deadline | Guard test passed; application insertion and concurrent closure integration pending |
| FR1 invited sign-in/object protection | Three roles and server-side object checks via real requests | No production accounts module or feature views in inspected main | Not run |
| FR4 application creation | One timely application, duplicate rejection and receipt | No Application model/view in inspected main | Not run |
| FR5/FR6 decisions | Own-org recommendation, coordinator confirmation and private-note exclusion | UI/contracts reviewed; runtime module absent | Not run |
| FR7 selection | Atomic unique placement/mentor/2-3 goals and one-active rule | Schema/acceptance criteria supplied; runtime module absent | Not run |
| FR8 supervision | Weekly uniqueness, assigned feedback and coordinator completion | UI/contracts reviewed; runtime module absent | Not run |
| FR9/FR10/FR11 | Queue counts, recipient-safe notices, aggregate export if retained | Proposed screen/contracts only | Not run |

## Milestone disposition

| Milestone | Required journey | Disposition and remaining evidence |
| --- | --- | --- |
| M2 publication demo | Representative draft -> coordinator publication -> student listing | Service-layer criteria have evidence. Full demo acceptance is pending production accounts/models/migrations/views and a reproducible seeded path. |
| M3 application/decision demo | Application -> recommendation -> confirmed trail/placement | Pending application/decision/placement modules and runtime test evidence. |
| M4 full journey | Goal-linked note -> mentor response -> coordinator queue | Pending progress/feedback/queue integration. |
| M5 tested demo/report | Reproducible demo, permissions, accessibility, load and restore evidence | Pending full build and actual exit-check evidence. |

The review has started and records actual service-layer results. KAN-25 remains In Progress until the demo milestone conditions are evaluated against working integrated builds. These outcomes do not supply usability measurements. Participants and sessions remain zero.

## Next integration handoff

Tharun can call the merged services from the KAN-46 routes once KAN-30 accounts and KAN-50 models are implemented. Atul's UI-01 through UI-06 findings remain open. Use the same opportunity lock in application creation before checking eligibility and inserting the application. Record production test paths and CI/build evidence in KAN-22 when each module is available.
