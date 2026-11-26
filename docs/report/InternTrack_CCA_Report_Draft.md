# Online Internship and Training Management System

Software Engineering CCA team report

Working draft prepared 23 November 2026. Submission target 27 November 2026. Team review and instructor details remain pending.

| Member | Responsibility |
|---|---|
| Kunal | Requirements and analysis |
| Atul Dhull | UI/UX and system design |
| Tharun | Development and testing |
| Ritika Girish Kulkarni | Project management and documentation |

## 1 Introduction

InternTrack proposes a single-department workflow for internship opportunity approval, student applications, coordinator decisions, placement goals and weekly progress. The problem hypothesis is that disconnected announcements, forms, email and spreadsheets can obscure decision status and supervision. This has not been validated with the department. Analysis uses three explicitly synthetic role walkthroughs with zero real interview participants.

The proposed scope covers one cohort, invited accounts, student/coordinator/organization roles and text check-ins. The objectives are to make vetted opportunities available, prevent duplicate or late applications, maintain a dated decision trail, and support supervised progress. Department assumptions remain explicitly unvalidated.

## 2 Requirements

The current draft baseline is SRS v0.2 in KAN-19. It covers authentication and authorization, opportunity drafting and publication, browsing and applications, organization recommendations, coordinator-confirmed status, placements and goals, weekly notes and mentor response, and a basic pending queue. Rich notices and aggregate export remain lower-priority scope subject to team decisions. Whole-team sign-off is pending.

Source requirements and detailed acceptance criteria follow in Appendix A. They are specifications, and do not establish integrated acceptance results.

## 3 Selected Process Model

[TEAM INPUT REQUIRED: selected process model, its diagram, phases and rationale. No agreed model was established in the reviewed evidence.]

## 4 Project Plan

Ritika maintains the WBS, schedule, dependencies, risk register and action log. The recorded submission target is 27 November. Internal targets are tentative: report compilation and proposed integration testing on 24 November, team review and rehearsal on 25 November, and final file/access checks on 26 November. Technical owners must confirm feasibility. Appendix B contains the detailed planning record, including historical targets and later dated updates.

## 5 Software Design

Atul’s design workstreams cover navigation/wireframes (KAN-44), schema and permissions (KAN-45), and architecture/contracts (KAN-46). Kunal reported reviewing these and recording six findings. Final design approval is pending.

[INSERT REVIEWED FIGURES: DFD Levels 0, 1 and 2; data dictionary; sequence diagram with normal and alternative flows; architecture and deployment diagrams. Add titles, figure numbers, technology rationale and scalability explanation.]

## 6 Tools and Collaboration

Jira tracks tasks, owners, milestones, status and handovers. Repository: https://github.com/gundatharuntej2006-hue/InternTrack . Board: https://gundatharuntej2006.atlassian.net/jira/software/projects/KAN/boards/2 .

Ritika prepared the planning tracker, WBS, risk register, action log, report structure and submission review procedure. Kunal’s contribution includes requirements, synthetic walkthroughs, workflow services and tests in PR #1. Tharun reported DT-1 repository/setup delivery. Atul’s design review material is referenced above. Final commit and contribution evidence for each member must be checked before submission.

## 7 Ethical and Professional Considerations

Use synthetic demonstration data and minimize personal information. Validate role and record access with technical owners. Review accessibility and clear status wording, attribute external material, and disclose assumptions and validation limits. These are proposed mitigations requiring team validation. The detailed draft ethics table is retained in the Jira report working material in Appendix C.

## 8 Conclusion and References

The team has produced planning records and reviewable requirements/design contributions. Integrated application readiness and final acceptance remain open. The final conclusion must be updated from verified demonstration evidence.

Sources: CCA_Team_Project_Guidelines_UG_Students.docx; Jira KAN-8, KAN-9, KAN-19, KAN-44/45/46; Kunal’s 23 November updates on KAN-9; repository PR #1. Add references for any reused technical assets and diagrams supplied by the team.

## Appendix A Requirements source record

RA-7. Planned effort 2h. Revised review handoff delivered 20 November 2026. Whole-team baseline sign-off remains pending.

Review evidence: [KAN-44 findings](https://gundatharuntej2006.atlassian.net/browse/KAN-44?focusedCommentId=10019), [KAN-45 schema answers](https://gundatharuntej2006.atlassian.net/browse/KAN-45?focusedCommentId=10020), [KAN-18 state contract](https://gundatharuntej2006.atlassian.net/browse/KAN-18), [KAN-22 screen/test mapping](https://gundatharuntej2006.atlassian.net/browse/KAN-22).

The earlier tentative 17/18 November dates have elapsed. This delivery is dated 20 November. Reviewer decisions and actual approval evidence must be recorded here. Due working application: 27 November 2026.

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

* AC1.1 Given an invited valid account, signing in establishes its server-derived identity and role; invalid credentials produce an appropriate error without a session.
* AC1.2 A student requesting another student's application, placement, check-in or feedback receives access denial with no private content.
* AC1.3 A representative requesting another organization's opportunities/applicants is denied; an unassigned mentor cannot read or respond to an unrelated placement.
* AC1.4 Direct URL/POST/API attempts receive the same checks as page navigation; changing client-supplied user/organization IDs cannot grant access. Coordinator access is department-wide within this single-department MVP.

### FR2 / US-02 - Draft opportunity (Must)

As a representative, I want to draft my organization's opportunity so the coordinator can vet complete information before students see it.

* AC2.1 Authorized representative can save a draft containing title, description, eligibility, mode/location, start/end dates, deadline and mentor reference; missing/invalid fields receive field errors on submission for review.
* AC2.2 Draft and Returned records are absent from student lists, search results and direct detail endpoints.
* AC2.3 Representative cannot set publication/approver fields or alter another organization's record; submitting a complete Draft or corrected Returned record requests review.

### FR3 / US-03 - Approval and publication (Must)

As a coordinator, I want to publish or return proposals so students see vetted open opportunities.

* AC3.1 Only a coordinator can approve Pending Review to Published; approval records actor/time. Invalid or expired proposals cannot become student-visible.
* AC3.2 Coordinator can return Pending Review with a useful reason; representative sees the explanation and may correct/resubmit.
* AC3.3 Student list and detail expose only Published records strictly before deadline, even when a closure job has not run; manual closure removes visibility immediately.
* AC3.4 Invalid transitions, stale concurrent updates and unauthorized actions leave state unchanged. Audit and transition save together.

### FR4 / US-04 - Browse and apply once (Must)

As a student, I want to inspect eligibility/deadline, filter opportunities and submit one timely application.

* AC4.1 Listing/filtering returns only visible open records; empty results have a clear message; details include eligibility, mode/location and deadline/timezone.
* AC4.2 Before the deadline, a valid submission creates one Submitted application with one initial event and a receipt; identity derives from the session.
* AC4.3 A repeated or concurrent submission for the same student/opportunity creates no duplicate; the explanation identifies the existing application.
* AC4.4 At or after the deadline, or after manual closure/unpublication, server rejects submission and creates no application/event.

### FR5 / US-05 - Organization recommendation (Must)

As a representative, I want to inspect permitted applicants and recommend Shortlist, Decline or Select for coordinator review.

* AC5.1 Only the opportunity's organization can read its applicant list and submit recommendations.
* AC5.2 Recommendation records suggested outcome, rationale, actor and time; request is visible to the coordinator.
* AC5.3 Recording a recommendation alone does not change the student-visible status, append a final decision or create a placement. Cross-organization attempts change nothing.

### FR6 / US-06 - Confirmed status trail (Must)

As an applicant, I want a dated coordinator-confirmed status with public reason and next step so I know what to do.

* AC6.1 Only coordinator can confirm valid post-submission transitions; every confirmed update requires nonblank public reason/next step and records previous/new state, actor and server time.
* AC6.2 Status update and append-only event commit together or neither commits; historical events cannot be silently edited/deleted through product actions.
* AC6.3 Student sees their own ordered confirmed trail, actor role, date and public explanation; internal notes and unconfirmed recommendations are excluded from every student response.
* AC6.4 Invalid transitions and unauthorized changes are rejected without events or changed status. Selected is terminal in MVP.
* AC6.5 Coordinator may decline from Under Review or Shortlisted without a prior organization recommendation. Submitted first moves to Under Review. A public reason and next step are required for decline.

### FR7 / US-07 - Selected placement and goals (Must)

As a coordinator, I want confirmed selection to create a linked mentor placement with 2-3 learning goals.

* AC7.1 A valid Selected transition atomically creates one placement for that application, assigned mentor and exactly 2 or 3 nonempty goals; student and assigned mentor can read them.
* AC7.2 Missing mentor, invalid goal count, duplicate selection, concurrency conflict or an existing active placement causes a clear rejection and full rollback.
* AC7.3 Declined application has no placement. A unique selected-application relation and transaction/concurrency controls prevent duplicate placements and multiple active placements per student.
* AC7.4 Coordinator selection requires a recorded organization recommendation. The recommendation remains advisory and the coordinator records the final confirmed outcome.

### FR8 / US-08 - Weekly note and mentor response (Must)

As an intern, I want a brief weekly note tied to a learning goal and an assigned mentor response.

* AC8.1 Student with an Active placement submits accomplishment, blocker and next step for a week and one goal belonging to that placement; one note per placement/week is enforced server-side.
* AC8.2 Invalid goal ownership, inactive placement, cross-student or duplicate submission is rejected without a new note.
* AC8.3 Assigned mentor can respond to that note; unassigned users cannot. Student owner, assigned mentor and coordinator can read the permitted note/response.
* AC8.4 Coordinator alone can complete Active placement after final check-in; Completed cannot accept new weekly submissions under the proposed MVP contract.

### FR9 / US-09 - Needs-action queue (Should; basic pending list required)

As a coordinator, I want pending proposals, pending decisions and overdue check-ins in one place.

* AC9.1 Queue contains pending review opportunities, recommendations/decisions awaiting coordinator action and overdue check-in items, linking only to authorized records.
* AC9.2 Counts equal underlying eligible records for the same time/filter; completed/closed resolved items are excluded as appropriate.
* AC9.3 Overdue appears only after seven days following week end under the configured demo rule; exact boundary, timezone and zero-item cases are tested. Rich queue/overdue flags are Should; the basic pending list remains Must under proposal section 13.

### FR10 / US-10 - In-app notices (Should)

As a user, I want relevant in-app event notices when publication, confirmed status or mentor response occurs.

* AC10.1 Eligible recipient sees a notice after next page load following committed publication, own status change or assigned/own mentor response.
* AC10.2 Rolled-back actions produce no notice; cross-user access is denied and notice text contains no private content beyond the recipient's permission.
* AC10.3 Notification delivery is in-app only; no email/SMS service is implied. Event-to-recipient publication policy needs team agreement.

### FR11 / US-11 - Anonymous aggregate export (Could)

As a coordinator, I want aggregate counts for leadership without directly identifying students.

* AC11.1 Coordinator can export department counts by approved non-identifying category; totals reconcile with seeded records.
* AC11.2 Output has no names, emails, account/application identifiers or free text; non-coordinators cannot export.
* AC11.3 Small-cohort re-identification risk and grouping/suppression policy must be reviewed before any real-data use; no anonymity guarantee follows from simply removing names.

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

## Appendix B Planning source record

Historical dates and tentative proposals are retained below. Use the most recent dated updates when interpreting status.

Record milestones, owners, dependencies and target dates for requirements, design, implementation and testing. Done when the team can review the schedule and track milestone status.

Role reference: KAN-7.

## Milestone tracker

The final deadline and interim reviews are TBD pending the assignment brief. Status for individual milestones awaits owner confirmation. KAN-4 is In Progress at the workstream level.

| Milestone | Deliverable | Owner | Start | Target | Dependency | Status | Confirmation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initiation | Scope and ownership record | Ritika Girish Kulkarni AIML-1 (KAN-7) | TBD | TBD | Assignment brief | Planning started | Pending confirmation |
| Literature survey | Source matrix | Kunal AIML-1 (KAN-4) | TBD | TBD | Initial scope | Pending update | Pending confirmation |
| Existing system analysis | Current workflow and limitations | Kunal AIML-1 (KAN-4) | TBD | TBD | Literature survey | Pending update | Pending confirmation |
| Research gap identification | Evidence-backed gaps | Kunal AIML-1 (KAN-4) | TBD | TBD | Survey and existing system analysis | Pending update | Pending confirmation |
| Requirement gathering | Reviewed requirements | Kunal AIML-1 (KAN-4) | TBD | TBD | Scope and gap analysis | Pending update | Pending confirmation |
| SRS preparation | Reviewed SRS | Kunal AIML-1 (KAN-4) | TBD | TBD | Reviewed requirements | Pending update | Pending confirmation |
| System architecture and design | Architecture and UML drafts | Atul Dhull (KAN-5) | TBD | TBD | SRS | Pending update | Pending confirmation |
| UI/UX design | Screen flows and prototypes | Atul Dhull (KAN-5) | TBD | TBD | SRS and architecture interfaces | Pending update | Pending confirmation |
| Development | Implemented modules | GUNDA Tharun tej (KAN-6) | TBD | TBD | SRS and design | Pending update | Pending confirmation |
| Integration | Integrated build | GUNDA Tharun tej (KAN-6) | TBD | TBD | Implemented modules | Pending update | Pending confirmation |
| Testing | Test cases and results | GUNDA Tharun tej (KAN-6) | TBD | TBD | Integrated build and SRS | Pending update | Pending confirmation |
| Bug fixing | Fix log and retest results | GUNDA Tharun tej (KAN-6) | TBD | TBD | Test results | Pending update | Pending confirmation |
| Final documentation | Reviewed report and evidence pack | Ritika Girish Kulkarni AIML-1 (KAN-7) | TBD | TBD | SRS, design, implementation and testing inputs | Pending update | Pending confirmation |
| Final review and submission | Verified submission and receipt | Ritika Girish Kulkarni AIML-1 (KAN-7) | TBD | TBD | Final documentation and confirmed submission instructions | Pending update | Pending confirmation |

## CCA scope and planning baseline

Ritika owns the WBS, effort estimates, responsibility allocation, schedule/Gantt, milestones, dependencies, risk list and Jira tracking. Use the seven CCA stages as the schedule baseline: scope → process model → planning → design → repository and tool evidence → ethics → integrated review and presentation. Track Kunal’s requirements, Atul’s models and Tharun’s repository or demo inputs as handovers. Treat development/testing in the earlier tracker as conditional on instructor or team scope. Submission and presentation dates and any interim reviews remain TBD pending the instructor announcement.

## November deadline update

Submission target: 27 November 2026. Presentation: TENTATIVE 27 November 2026, pending instructor confirmation.

Proposed working dates (TENTATIVE, pending owner confirmation): 17 Nov — Kunal hands over scope and requirements. 18 Nov — team confirms process model and Ritika drafts WBS and risk list. 20 Nov — Atul hands over design models. 23 Nov — Tharun shares repository and demo evidence. 24 Nov — Ritika compiles the report and team reviews ethics and contribution evidence. 25 Nov — team reviews the report and rehearses. 26 Nov — Ritika verifies files, links and access.

## CCA work breakdown structure

Submission deadline: 27 November 2026. Presentation on 27 November is tentative. Working targets and effort estimates below are tentative and await owner confirmation. Effort is estimated hands-on time.

| ID | Work package and completion evidence | Owner | Dependency | Target | Effort |
| --- | --- | --- | --- | --- | --- |
| 1 | Obtain reviewed problem statement, scope, stakeholders, assumptions and requirements | Kunal provides, Ritika tracks | Agreed project topic | 17 Nov | 30 min coordination |
| 2 | Record the team’s process-model choice, phases, diagram and rationale | Ritika documents, team validates | 1 | 18 Nov | 1 h |
| 3 | Maintain WBS, Jira owners/status, schedule, milestones and risk register | Ritika | 1, 2 | 18 Nov baseline, then ongoing | 2 h setup |
| 4 | Collect DFD 0/1/2, data dictionary, sequence with alternative flow, and architecture explanation | Atul provides, Ritika tracks | 1 | 20 Nov | 30 min coordination |
| 5 | Collect repository URL, README, commit history, demo scenario and individual contribution evidence | Tharun and team provide, Ritika compiles | 1, 4 | 23 Nov | 1 h |
| 6 | Compile the report and ethics issue/impact/mitigation table for team validation | Ritika | 2, 3, 4, 5 | 24 Nov | 3 h |
| 7 | Coordinate consistency review and rehearsal. Prepare Jira and planning walkthrough | Ritika coordinates, team reviews | 6 | 25 Nov | 1.5 h |
| 8 | Export the team PDF and verify cover, figures, citations, links and access | Ritika | 7 | 26 Nov | 1 h |
| 9 | Coordinate submission, capture receipt and present the planning section at the confirmed slot | Ritika coordinates, team participates | 8 and instructor instructions | 27 Nov submission | 30 min submission coordination |

## Project risk register

Risks are open for review. Ratings are preliminary. Ritika tracks each risk and coordinates the response.

| ID | Risk | Likelihood / impact | Trigger and response |
| --- | --- | --- | --- |
| R1 | Late or unconfirmed handovers compress report review | Medium / High | If an owner misses a proposed target, request a revised date and usable partial material. Keep affected report sections open in KAN-10. |
| R2 | Design and requirements conflict or a required model is missing | Medium / High | At handover, check the CCA design inventory and ask Kunal and Atul to resolve inconsistencies before rehearsal. |
| R3 | Presentation slot, cutoff or submission method is unclear | Medium / High | Check the instructor announcement and record confirmed details in KAN-9 and KAN-11. |
| R4 | Instructor cannot access the board or repository | Medium / High | Check access and prepare board evidence on 26 Nov. Ask the resource owner to resolve any access issue. |
| R5 | Contribution evidence or citations are incomplete | Medium / Medium | Before team review, collect one traceable contribution record per member and flag missing citations to the relevant contributor. |
| R6 | Demo fails or speaking roles are unclear | Medium / Medium | Rehearse on 25 Nov, confirm each member’s speaking role and prepare a walkthrough using approved diagrams and screenshots. |

## Requirements review and release dependencies

* 16 Nov (TENTATIVE): Coordinate draft feedback and confirm reviewer availability.
* 17 Nov (TENTATIVE): Kunal hands over reviewed requirements, subject to feedback.
* 18 Nov (TENTATIVE): Kunal hands over the reviewed SRS baseline, subject to state-rule and assumption review. Track sign-off in KAN-19.
* Kunal reports a working-application deadline of 27 Nov. Obtain Atul’s design handoff and Tharun’s integration, testing and release evidence dates before committing to a compressed schedule. Track any scope trade-offs with the team.

## Development and testing handover — 23 November 2026

Source: Tharun’s message supplied by Ritika. Repository: https://github.com/gundatharuntej2006-hue/InternTrack      
Tharun reports repository/DT-1 handover completed on 23 Nov, a public repository, setup/README committed, and 7/7 DT-1 tests passed. Fresh-clone verification is pending. These implementation and test claims are teammate-reported.

| Milestone | Target | Confirmation |
| --- | --- | --- |
| Integrated build and initial integration testing | 24 Nov | TENTATIVE |
| Report evidence handover | 24 Nov | Planned by Tharun |
| Bug fixes and retesting | 25 Nov | TENTATIVE |
| Demo-ready build | 25 Nov | TENTATIVE |
| Rehearsal support | 25 Nov | Available subject to build readiness |
| Final checks | 26 Nov | TENTATIVE internal plan |
| Submission | 27 Nov | Recorded submission target |

Dependencies: DT-2 CI and DT-3 authentication are pending. Integration needs schema, permission rules and feature modules. Collaborator invitations await acceptance according to Tharun. Final testing requires integrated modules. The build and rehearsal dates require continued tracking in KAN-9.

## Planning baseline readiness — 23 November 2026

Completed planning outputs: WBS and responsibility allocation, indicative effort estimates, dependency map, dated milestone plan and risk register. Review/sign-off remains open. Preserve historical targets as tentative elapsed targets rather than delivery commitments.    
Remaining timeline: 24 Nov report compilation and proposed integrated validation; 25 Nov proposed team review, fixes and rehearsal; 26 Nov final document and access checks; 27 Nov submission. Internal dates are TENTATIVE. Presentation slot and submission cutoff await confirmation.    
Ritika can maintain these records and compile available evidence now. Technical milestone acceptance remains with the respective owners.

## Schedule evidence update from Kunal — 23 November 2026

Recorded actual delivery on 23 Nov: workflow service contribution in commit 3bdbee3, PR #1, local database tests and CI evidence. Kunal accepted his repository invitation. His synthetic process/assumption deliverables are reported Done. Remaining milestones depend on team sign-off, six design findings, and production accounts/models/views. Keep integrated build and rehearsal targets tentative until those gates have evidence.

## Appendix C Report working material

The following is the working record, including placeholders and dated corrections, for editorial consolidation before final export.

Collect team inputs for requirements, design, implementation and testing. Assemble and review the report for completeness, consistency and source references.

Role reference: KAN-7.

## SEPM report skeleton

**Online Internship and Training Management System**

Draft outline pending assignment brief and team inputs.

### 1. Title Page

\[Add official institution, course, team and submission details.\]

### 2. Abstract

\[Summarize the reviewed report when complete.\]

### 3. Introduction

\[Describe the verified project context.\]

### 4. Problem Statement

\[Insert the agreed problem.\]

### 5. Objectives

\[Insert approved objectives.\]

### 6. Scope

\[Insert agreed boundaries.\]

### 7. Literature Survey

\[Insert sources and synthesis.\]

### 8. Existing System Analysis

\[Insert evidence and workflow findings.\]

### 9. Research Gaps

\[Insert evidence-backed gaps.\]

### 10. Proposed System

\[Insert approved system overview.\]

### 11. Software Requirements Specification

\[Insert reviewed functional and nonfunctional requirements.\]

### 12. System Architecture

\[Insert reviewed architecture and design rationale.\]

### 13. UML Diagrams

\[Insert diagrams from Atul with captions.\]

### 14. Project Planning and Methodology

\[Insert agreed methodology, milestones and responsibilities.\]

### 15. Implementation

\[Insert Tharun’s implementation and repository details.\]

### 16. Testing and Results

\[Insert actual test cases, outcomes and retests.\]

### 17. Conclusion

\[Summarize evidenced outcomes.\]

### 18. Future Enhancements

\[Record agreed future work.\]

### 19. References

\[Add cited sources in required style.\]

## CCA report structure to use

Cover page: project title, course, team members and roles, date.

1. Introduction — problem, objectives, scope and stakeholders.
2. Requirements — functional and nonfunctional requirements and assumptions from Kunal.
3. Selected Process Model — team-approved diagram, phases and justification.
4. Project Plan — Ritika’s WBS, allocation, schedule/Gantt, milestones and risks.
5. Software Design — Atul’s DFD 0/1/2, data dictionary, sequence/transaction diagram with normal and alternative flows, and architecture with deployment and scalability notes.
6. Tools and Collaboration — Jira and repository links, README, commit history and individual contribution evidence.
7. Ethical and Professional Considerations — compile team-validated issues, impacts, mitigations and responsibilities.
8. Conclusion and References — summary, limitations and citations.          
  Ritika owns compilation, consistency review and formatting. Technical sections await owner inputs.

## Report compilation review

Target first compiled draft: **24 Nov (TENTATIVE)**. Team review: **25 Nov (TENTATIVE)**.

* Ritika can draft the cover, project plan and collaboration sections from Jira. Verify team names, course and date before export.
* Insert Kunal’s reviewed scope and requirements, the team-approved process model, and Atul’s design models. Check that the demo scenario matches the requirements and the sequence diagram includes an alternative flow.
* Add Tharun’s repository and demo evidence, a traceable contribution from each member, and team-validated ethics issues and mitigations.
* Review figure captions, citations, assumptions and limitations. Record missing material in KAN-9 before the team review.

## Draft cover and project management sections

**Online Internship and Training Management System**
Software Engineering · Continuous Comprehensive Assessment (CCA)      
Team submission deadline: 27 November 2026

* Kunal — Requirements and analysis
* Atul Dhull — UI/UX and system design
* Tharun — Development and testing
* Ritika Girish Kulkarni — Project management and documentation

### Project Plan

The team tracks deliverables and handovers in Jira. The WBS and risk register in KAN-8 cover requirements, process model, design, repository evidence, report compilation, rehearsal and submission. Kunal has shared draft requirements and proposed reviewed handovers for 17 and 18 November. The design, integration and release dates remain open. The current plan targets a compiled report on 24 November, team review and rehearsal on 25 November, and final file and access checks on 26 November. These internal dates remain tentative. The main planning risk is late technical evidence reducing the time available for consistency review.

### Tools and Collaboration

Jira tracks ownership, status, dependencies and risks. KAN-9 records handover dates and blockers. KAN-4 and KAN-17 provide traceable evidence of Kunal’s draft requirements work. \[Insert verified repository URL, README, commit history and contribution evidence for each member.\]

Project board: https://gundatharuntej2006.atlassian.net/jira/software/projects/KAN/boards/2

## Report text ready for assembly

### Project planning and scheduling

The project uses a work breakdown structure covering requirements, process selection, planning, design, repository evidence, documentation, review and submission. Kunal supplies requirements and analysis; Atul supplies UI/UX and system design; Tharun supplies development and testing; Ritika coordinates milestones and compiles the report. Jira records responsibility, progress, dependencies and risks. The team’s recorded submission deadline is 27 November 2026.

The revised requirements handoff was reported on 20 November. Tharun reported repository and initial setup handover on 23 November. The working plan reserves 24 November for report compilation and proposed integration testing, 25 November for review and rehearsal, and 26 November for final checks. These internal targets remain tentative. Schedule risks and owner confirmations are tracked in KAN-8 and KAN-9.

### Collaboration and contribution evidence

Jira provides the project board and dated handover discussions. The reported repository is https://github.com/gundatharuntej2006-hue/InternTrack . Kunal’s requirements evidence is referenced in KAN-19; design review findings are tracked in KAN-44. Ritika’s contribution comprises the WBS, milestone tracker, risk register, action log, report structure and submission checklist. Final evidence should link each member to their deliverables and relevant commits or review records.

### Proposed ethical and professional considerations

The following mitigations are proposals for team validation.

| Issue | Potential impact | Proposed mitigation |
| --- | --- | --- |
| Personal information in internship records | Unnecessary disclosure | Minimize collected fields, document purpose and consent, and exclude personal records from public evidence. |
| Account permissions | Unauthorized access or changes | Have technical owners validate access rules and retain evidence of relevant checks. |
| Accessibility and fairness | Users may struggle to access opportunities | Review labels, keyboard operation and eligibility wording with the design and requirements owners. |
| Intellectual property | Missing attribution or incompatible reuse | Cite sources and verify asset and library licences before submission. |
| Unvalidated assumptions and incomplete tests | Misleading conclusions | Label assumptions and distinguish reported setup test results from integrated validation. |
| Professional accountability | Unclear ownership and unsupported completion claims | Keep dated decisions, responsibilities, review records and evidence links in Jira. |

### Limitations to disclose

Department assumptions remain unvalidated. Tharun’s reported 7/7 test results cover DT-1 setup; integrated validation and fresh-clone verification remain pending. Presentation timing is unconfirmed. Update these statements when evidence changes.

## Updated requirements and evidence material for report — 23 November 2026

Requirements source: https://github.com/gundatharuntej2006-hue/InternTrack/tree/kiunal/docs/requirements . Review PR: https://github.com/gundatharuntej2006-hue/InternTrack/pull/1 .

### Requirements and study context

The reviewed draft proposes InternTrack for a single department’s internship workflow, covering opportunity approval, timely applications, coordinator-confirmed decisions, placements and weekly progress. These requirements remain subject to whole-team baseline sign-off in KAN-19. The local problem remains a hypothesis. The analysis uses three explicitly synthetic role walkthroughs; no real interviews or participants were involved. Eight department assumptions remain Unknown.

### Contribution and verification evidence

Kunal reports commit 3bdbee3 added transactional workflow services and 22 database-backed tests. His reported local suite totals 29 passing tests including seven foundation tests. He supplied passing push and PR CI links on KAN-9 comment 10041. This supersedes the earlier statement that only seven setup tests were available. Production accounts/models/views and end-to-end acceptance remain pending. Treat the results as teammate-provided evidence until reviewed for the final report.

### Planning review of the baseline

The stated 240-person-hour ten-week proposal does not establish feasible capacity before 27 Nov. Remaining work must follow the compressed milestone tracker. Track proposed deferral of FR10/FR11 through team change control and preserve essential authorization and transaction/history integrity checks. Schedule review is recorded; whole-team technical or sponsor approval is pending.


