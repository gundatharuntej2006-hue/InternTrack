# InternTrack - Software Requirements Specification

RA-5 / RA-7. Version 0.2, 20 November 2026. Owner: Kunal. Updated after reviewing Atul's KAN-44/45/46 handoff and KAN-47 template archive. Team/sponsor baseline sign-off pending. Review findings are recorded in RA-09-wireframe-review.md under review/2026-11-20 and the actual screen mapping is in RA-10-traceability-v0.2.md.

## 1. Purpose, problem and objectives

InternTrack supports one department's internship journey from vetted opportunity publication to human decisions and weekly supervised progress. The local problem hypothesis is that disconnected announcements, forms, email and spreadsheets may obscure approval, decision state and supervision. This has not been verified for the department.

Objectives: publish vetted opportunities; prevent duplicate/late applications; separate organization recommendations from coordinator decisions; show dated public status and next action; create one selected placement with 2-3 goals; collect brief weekly notes and assigned-mentor feedback; expose pending work. Evaluate usefulness through actual task success, comprehension and coordinator effort once a prototype and consenting users exist.

## 2. Scope and environment

One department, one cohort, web only, invited/seeded accounts, three roles (student/coordinator/organization), text-only check-ins, local synthetic demo or approved hosting. Leadership receives an optional aggregate export, not an account. Framework proposal: Django templates/services and PostgreSQL; final pinned versions, schema and repository are integration decisions for M3/M4.

Excluded: employer marketplace/self-registration, AI matching/ranking, resume parsing, interviews/offers/contracts, payments, GPS, certificates, grading, university SSO, email/SMS, chat, verification of real organizations, legal eligibility determination, multi-campus policy and large uploads. Eligibility is department-defined information/answers; automated ranking is excluded.

Working app submission is required by 27 November per user. Proposal effort is 240 person-hours across ten weeks; it is not evidence that this capacity fits the remaining days. Team must confirm a compressed schedule. Defer FR11 and FR10 before weakening authorization, transactions or public decision integrity.

## 3. Functional stories and acceptance conditions

Each AC below is a test specification, not a recorded pass. State contract is in RA-06. Screen identifiers are proposed contracts in RA-10.

### FR1 / US-01 - Invited authentication and authorization (Must)
As an invited user, I want access appropriate to my role and records so private data stays limited to authorized participants.

- AC1.1 Given an invited valid account, signing in establishes its server-derived identity and role; invalid credentials produce an appropriate error without a session.
- AC1.2 A student requesting another student's application, placement, check-in or feedback receives access denial with no private content.
- AC1.3 A representative requesting another organization's opportunities/applicants is denied; an unassigned mentor cannot read or respond to an unrelated placement.
- AC1.4 Direct URL/POST/API attempts receive the same checks as page navigation; changing client-supplied user/organization IDs cannot grant access. Coordinator access is department-wide within this single-department MVP.

### FR2 / US-02 - Draft opportunity (Must)
As a representative, I want to draft my organization's opportunity so the coordinator can vet complete information before students see it.

- AC2.1 Authorized representative can save a draft containing title, description, eligibility, mode/location, start/end dates, deadline and mentor reference; missing/invalid fields receive field errors on submission for review.
- AC2.2 Draft and Returned records are absent from student lists, search results and direct detail endpoints.
- AC2.3 Representative cannot set publication/approver fields or alter another organization's record; submitting a complete Draft or corrected Returned record requests review.

### FR3 / US-03 - Approval and publication (Must)
As a coordinator, I want to publish or return proposals so students see vetted open opportunities.

- AC3.1 Only a coordinator can approve Pending Review to Published; approval records actor/time. Invalid or expired proposals cannot become student-visible.
- AC3.2 Coordinator can return Pending Review with a useful reason; representative sees the explanation and may correct/resubmit.
- AC3.3 Student list and detail expose only Published records strictly before deadline, even when a closure job has not run; manual closure removes visibility immediately.
- AC3.4 Invalid transitions, stale concurrent updates and unauthorized actions leave state unchanged. Audit and transition save together.

### FR4 / US-04 - Browse and apply once (Must)
As a student, I want to inspect eligibility/deadline, filter opportunities and submit one timely application.

- AC4.1 Listing/filtering returns only visible open records; empty results have a clear message; details include eligibility, mode/location and deadline/timezone.
- AC4.2 Before the deadline, a valid submission creates one Submitted application with one initial event and a receipt; identity derives from the session.
- AC4.3 A repeated or concurrent submission for the same student/opportunity creates no duplicate; the explanation identifies the existing application.
- AC4.4 At or after the deadline, or after manual closure/unpublication, server rejects submission and creates no application/event.

### FR5 / US-05 - Organization recommendation (Must)
As a representative, I want to inspect permitted applicants and recommend Shortlist, Decline or Select for coordinator review.

- AC5.1 Only the opportunity's organization can read its applicant list and submit recommendations.
- AC5.2 Recommendation records suggested outcome, rationale, actor and time; request is visible to the coordinator.
- AC5.3 Recording a recommendation alone does not change the student-visible status, append a final decision or create a placement. Cross-organization attempts change nothing.

### FR6 / US-06 - Confirmed status trail (Must)
As an applicant, I want a dated coordinator-confirmed status with public reason and next step so I know what to do.

- AC6.1 Only coordinator can confirm valid post-submission transitions; every confirmed update requires nonblank public reason/next step and records previous/new state, actor and server time.
- AC6.2 Status update and append-only event commit together or neither commits; historical events cannot be silently edited/deleted through product actions.
- AC6.3 Student sees their own ordered confirmed trail, actor role, date and public explanation; internal notes and unconfirmed recommendations are excluded from every student response.
- AC6.4 Invalid transitions and unauthorized changes are rejected without events or changed status. Selected is terminal in MVP.
- AC6.5 Coordinator may decline from Under Review or Shortlisted without a prior organization recommendation. Submitted first moves to Under Review. A public reason and next step are required for decline.

### FR7 / US-07 - Selected placement and goals (Must)
As a coordinator, I want confirmed selection to create a linked mentor placement with 2-3 learning goals.

- AC7.1 A valid Selected transition atomically creates one placement for that application, assigned mentor and exactly 2 or 3 nonempty goals; student and assigned mentor can read them.
- AC7.2 Missing mentor, invalid goal count, duplicate selection, concurrency conflict or an existing active placement causes a clear rejection and full rollback.
- AC7.3 Declined application has no placement. A unique selected-application relation and transaction/concurrency controls prevent duplicate placements and multiple active placements per student.
- AC7.4 Coordinator selection requires a recorded organization recommendation. The recommendation remains advisory and the coordinator records the final confirmed outcome.

### FR8 / US-08 - Weekly note and mentor response (Must)
As an intern, I want a brief weekly note tied to a learning goal and an assigned mentor response.

- AC8.1 Student with an Active placement submits accomplishment, blocker and next step for a week and one goal belonging to that placement; one note per placement/week is enforced server-side.
- AC8.2 Invalid goal ownership, inactive placement, cross-student or duplicate submission is rejected without a new note.
- AC8.3 Assigned mentor can respond to that note; unassigned users cannot. Student owner, assigned mentor and coordinator can read the permitted note/response.
- AC8.4 Coordinator alone can complete Active placement after final check-in; Completed cannot accept new weekly submissions under the proposed MVP contract.

### FR9 / US-09 - Needs-action queue (Should; basic pending list required)
As a coordinator, I want pending proposals, pending decisions and overdue check-ins in one place.

- AC9.1 Queue contains pending review opportunities, recommendations/decisions awaiting coordinator action and overdue check-in items, linking only to authorized records.
- AC9.2 Counts equal underlying eligible records for the same time/filter; completed/closed resolved items are excluded as appropriate.
- AC9.3 Overdue appears only after seven days following week end under the configured demo rule; exact boundary, timezone and zero-item cases are tested. Rich queue/overdue flags are Should; the basic pending list remains Must under proposal section 13.

### FR10 / US-10 - In-app notices (Should)
As a user, I want relevant in-app event notices when publication, confirmed status or mentor response occurs.

- AC10.1 Eligible recipient sees a notice after next page load following committed publication, own status change or assigned/own mentor response.
- AC10.2 Rolled-back actions produce no notice; cross-user access is denied and notice text contains no private content beyond the recipient's permission.
- AC10.3 Notification delivery is in-app only; no email/SMS service is implied. Event-to-recipient publication policy needs team agreement.

### FR11 / US-11 - Anonymous aggregate export (Could)
As a coordinator, I want aggregate counts for leadership without directly identifying students.

- AC11.1 Coordinator can export department counts by approved non-identifying category; totals reconcile with seeded records.
- AC11.2 Output has no names, emails, account/application identifiers or free text; non-coordinators cannot export.
- AC11.3 Small-cohort re-identification risk and grouping/suppression policy must be reviewed before any real-data use; no anonymity guarantee follows from simply removing names.

## 4. Nonfunctional targets and verification

| ID | Target | Evidence required before pass |
| --- | --- | --- |
| NFR1 Security | Deployed HTTPS, server-side object checks, CSRF, secure HTTP-only session cookies, framework password hashing, login rate limit | Role/ownership negative tests, request/configuration checks; rate limit and deploy settings evidence |
| NFR2 Privacy | Minimum necessary fields; synthetic public-demo records; approved retention before real pilot | Data inventory, access review, documented department retention/deletion decision |
| NFR3 Accessibility | WCAG 2.2 AA target where feasible: keyboard, focus, labels/errors, contrast, reflow | Manual keyboard/screen-reader and contrast/reflow records; no full-conformance claim without audit |
| NFR4 Performance | 100 students, 20 opportunities, 300 applications; p95 response under 2 seconds on demo hardware | Named dataset, hardware, route mix, sample size and measured latency results |
| NFR5 Reliability | Atomic status/events and selection; daily demo backup and one restore drill | Transaction rollback/concurrency tests, timestamped backup/restore evidence |
| NFR6 Maintainability | Setup/schema/states/roles/deployment documented; migrations and critical tests | Reproducible clean setup, migration execution and relevant automated test output |

These are proposal targets, all unmeasured in the integrated application at authoring time.

## 5. Data/interface constraints

User has server-trusted role and optional organization; Opportunity belongs to one organization; Application uniquely pairs student/opportunity; append-only StatusEvent has approved public text and optional private note; Recommendation is separate; Placement uniquely references selected application and assigned mentor; 2-3 LearningGoals belong to placement; CheckIn uniquely pairs placement/week and references a goal of that placement; Feedback belongs to check-in/assigned mentor; Notification belongs to recipient. IDs from a request never override session identity/ownership. Text lengths and week/calendar policy require schema agreement.

## 6. Baseline gate and change control

RA-7 requires review of RA-5, RA-6 and Member 2's schedule check. Sign-off entries need reviewer/date/decision/evidence. Current decisions: pending for all members and sponsor. Interview assumptions remain unvalidated. Resolve deadline timezone/boundary, overdue week calendar, publication recipients, returned-edit policy, direct-decline path, mentor assignment, and compressed delivery plan before final approval.

MoSCoW: Must FR1-FR8, minimum pending coordinator list and essential security/integrity; Should full FR9/FR10; Could FR11 and configurable reminders; Won't this delivery: excluded integrations/features in section 2. Release gate: reproducible end-to-end synthetic journey, duplicate/late and unauthorized rejection, transaction/history integrity, reviewed critical defects and explicit known limitations. No signed baseline exists yet.

Change log columns: CR-ID, date, FR/AC, request, evidence/rationale, cost/schedule/schema/test impact, approver, decision and resulting version. Initial version 0.1 is the authored draft; no approvals recorded.

Version 0.2 change record, 20 November 2026. Member 1 confirmed three roles with mentor assignment under ORG_REP, one organization per representative, and added AC6.5/AC7.4 to clarify the recommendation gate. Display status names stay as listed in RA-06. Updated actual design traceability and logged UI-01 through UI-06 for owner follow-up. Full-team approval and integrated acceptance evidence remain pending. The earlier tentative 17/18 November reviewed handover dates have elapsed. This revised review package is delivered on 20 November for sign-off without claiming those earlier targets were met.
