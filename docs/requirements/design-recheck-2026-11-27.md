# Member 1 design recheck - 27 November 2026

Atul's PR #3 was merged to main at f179c7dd9390760a4564e7ce7ae982497dbdede8 during this review. The inspected UI revision is 8077000. PR #2 contains Kunal's follow-up test/acceptance work and the corrections below. The production account, application and placement models/views are still pending in the inspected main snapshot.

## Review findings disposition

| Finding | Current evidence | Disposition |
| --- | --- | --- |
| UI-01 draft versus submission | Partial remote drafts pass and incomplete submissions fail. On-site drafts without location were still rejected by the merged form. UI copy promised title-only saving while the contract required title plus mode. | Corrected in Kunal's follow-up: mode is optional on a draft and required on submission, and location is required for on-site/hybrid submission. UI and contract now agree on title-only drafts. Six regression tests cover this split. |
| UI-02 deadline/timezone | Full date/time/zone is shown on student list/detail, org list and coordinator review. Input help names IST and project default is Asia/Kolkata. | Resolved at design/template level for the configured project timezone. Runtime exact-deadline enforcement still needs integrated view validation. |
| UI-03 feedback readability | Student placement renders mentor comment, mentor name and response date. Completed placement retains goals/check-ins/feedback and hides check-in submission. | Resolved at template level using synthetic preview data. |
| UI-04 closure and mentor | Published close controls appear on C2. Decision view shows the inherited mentor and an explicit missing-mentor message. | Resolved at design/template level. Production actor/transaction checks remain part of the integrated workflow acceptance. |
| UI-05 returned correction | Draft/Returned titles and edit actions link to the editor, which displays the retained return reason and resubmission instruction. Wireframe save now has a destination. | Resolved at design/template level. |
| UI-06 publication notices | Notification recipients include active student accounts, and eight event values match between schema and contract. Free-text eligibility remains a student/coordinator judgment. | Resolved at contract level. Delivery, recipient authorization and transaction/rollback checks await the notification module. |

The added application sequence used ApplicationEvent where the agreed data dictionary names StatusEvent. Kunal corrected the diagram to preserve the canonical model name. No display-status renames are requested.

## Independent verification

- All 20 template previews render without missing-variable markers.
- Atul's automated checker passed HTML checks for all 20 pages, all 11 contrast pairs and its CSS positioning check.
- Targeted form/template/contract checks verify partial-save versus submit, past-deadline rejection, Completed-record readability, inherited/missing mentor messages, returned editing, visible timezone output, notification event values and valid wireframe anchor targets.
- Local PostgreSQL execution passed 36 tests, including the six new form regressions, the concurrent workflow test and existing tests. Django system/migration checks passed.

The static preview emits Django's expected missing-CSRF-context warning because it renders templates outside a real request. Real CSRF enforcement requires the application routes. Browser zoom/reflow/target-size and NVDA results are outside this independent source/form recheck. Atul's accessibility report v2 explicitly keeps running-app and NVDA work open.

## Report handoff

Ritika can cite merged PR #1, the current main UI merge, and PR #2's final CI evidence. Team requirements/consent sign-off, production integration, full acceptance and the five-user usability study remain open. Real interview and usability participant counts remain zero. The design fixes should be recorded as source/template/contract verification when compiling the final report.
