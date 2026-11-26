# RA-14 status and public wording audit - 24 November 2026

The audit uses KAN-18 v0.2, the KAN-45 schema attachment 10004, KAN-46 contracts attachment 10006, the KAN-47 template archive 10007, and the merged workflow code in main 75fa89a. The design attachments are unchanged since the 20 November review. This is the current source/design audit. Runtime database/display/permission verification needs the production modules.

## Canonical mapping

| Object | Stored values | Display labels | Evidence and result |
| --- | --- | --- | --- |
| Opportunity | DRAFT, PENDING_REVIEW, PUBLISHED, RETURNED, CLOSED | Draft, Pending Review, Published, Returned, Closed | KAN-18/45/46 agree. Merged services use all five stored values. Opportunity tests use the same constants. Source mapping matches. |
| Application | SUBMITTED, UNDER_REVIEW, SHORTLISTED, SELECTED, DECLINED | Submitted, Under Review, Shortlisted, Selected, Declined | KAN-18/45/46 agree. Atul's forms.py NEXT_STATUSES matches the graph. Production Application/StatusEvent model and integration tests remain pending. |
| Placement | ACTIVE, COMPLETED | Active, Completed | KAN-18/45/46 and template conditions agree. Production model/tests remain pending. |
| Recommendation | SHORTLIST, SELECT, DECLINE | Shortlist, Select, Decline | Schema/form contracts distinguish these suggestions from coordinator-confirmed status. Runtime separation tests remain pending. |
| Follow-up flag | Calculated overdue value | Overdue | Template presents a text flag alongside placement state. No new lifecycle status is requested. |

No status-label renames are required by this audit. The display helper templates/includes/status.html renders its supplied label as text, so the production get_state_display/get_status_display values must use the mapping above. Wireframe badge capitalization should preserve these names. Final DFD/data-dictionary copies should use the same mapping at the handoff review.

## Public wording and information boundaries

| Check | Existing evidence | Outcome / follow-up |
| --- | --- | --- |
| Each confirmed decision has a public reason and next step | DecisionForm requires both; S4 renders public_reason and current public_next_step | Design/source matches. Verify direct POST enforcement and persisted values when the service is integrated. |
| Student trail shows date and actor role | applications/my_list.html renders event timestamp and actor_role | Design/source matches. UI-02 still requires a visible timezone and consistent full deadline/time input help. |
| Internal notes stay private | Student template uses public_events; coordinator template renders internal_note separately | Verify the student queryset/response excludes private data, including JSON/notices. Rendering different templates alone does not verify data isolation. |
| Recommendation remains advisory | O3/C3 explanatory text and separate Recommendation schema | Runtime recommendation must leave visible Application status unchanged. |
| Selected next action | Open placement and review learning goals | KAN-18/46 wording matches; verify real mentor/goals link in the integrated flow. |
| Returned next action | Read reason, correct fields and resubmit | New templates support this; UI-05 asks the wireframe to expose that route. |
| Mentor response | Student template renders the comment | UI-03 asks the wireframe to match the feedback view and identify responder/time. |
| Completion | Completed display label and retained history | KAN-46's active-only placement URL contract still needs a defined Completed-record read path. |
| Publication notices | FR10 requires the event to reach eligible students if retained | UI-06 remains open for recipients and event-type alignment. |

## Closure condition

KAN-26 has source-audit evidence and remains In Progress. Final closure requires comparing actual UI labels, production choices/data dictionary and executable integrated tests, plus an authorized student response proving private notes/unconfirmed recommendations stay outside public output. Team feedback should record any required label or policy changes in KAN-18/KAN-19.
