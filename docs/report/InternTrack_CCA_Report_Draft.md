# Online Internship and Training Management System

Software Engineering CCA team report

Working draft consolidated 26 November 2026. Submission target 27 November 2026. Team review and instructor details remain pending.

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

Detailed source requirements are maintained in KAN-19 and the repository requirements documents. They are specifications, and do not establish integrated acceptance results.

## 3 Selected Process Model

[TEAM INPUT REQUIRED: selected process model, its diagram, phases and rationale. No agreed model was established in the reviewed evidence.]

## 4 Project Plan

Ritika maintains the WBS, schedule, dependencies, risk register and action log. The recorded submission target is 27 November. The earlier 24 November compilation/integration and 25 November review/rehearsal targets have elapsed; their completion is unverified. Final file/access checks are planned for 26 November. Technical owners must confirm feasibility. The detailed planning record remains in KAN-8, with actions in KAN-9.

| Work package | Responsible member | Handover dependency |
|---|---|---|
| Scope and requirements | Kunal | Reviewed requirements and assumptions |
| Process selection | Team decision, Ritika documents | Agreed rationale and phase diagram |
| WBS, schedule and risk tracking | Ritika | Owner estimates and delivery updates |
| Design models and contracts | Atul | Requirements/state baseline |
| Build, integration and testing | Tharun with feature contributors | Schema, permissions and feature handovers |
| Report compilation | Ritika | Reviewed technical evidence |
| Review, rehearsal and submission | Ritika coordinates, all members participate | Final files, verified links and instructor instructions |

The main risks are late handovers, requirements/design inconsistencies, incomplete integrated validation, missing contribution evidence and inaccessible submission links. Ritika tracks these in Jira, requests revised dates for slipped handovers, and records known limitations in the report.

## 5 Software Design

Atul’s design workstreams cover navigation/wireframes (KAN-44), schema and permissions (KAN-45), and architecture/contracts (KAN-46). Kunal reported reviewing these and recording six findings. Final design approval is pending.

[INSERT REVIEWED FIGURES: DFD Levels 0, 1 and 2; data dictionary; sequence diagram with normal and alternative flows; architecture and deployment diagrams. Add titles, figure numbers, technology rationale and scalability explanation.]

## 6 Tools and Collaboration

Jira tracks tasks, owners, milestones, status and handovers. Repository: https://github.com/gundatharuntej2006-hue/InternTrack . Board: https://gundatharuntej2006.atlassian.net/jira/software/projects/KAN/boards/2 .

Ritika prepared the planning tracker, WBS, risk register, action log, report structure and submission review procedure. Kunal’s contribution includes requirements, synthetic walkthroughs, workflow services and tests in PR #1. Tharun reported DT-1 repository/setup delivery. Atul’s design review material is referenced above. Final commit and contribution evidence for each member must be checked before submission.

## 7 Ethical and Professional Considerations

Use synthetic demonstration data and minimize personal information. Validate role and record access with technical owners. Review accessibility and clear status wording, attribute external material, and disclose assumptions and validation limits. These are proposed mitigations requiring team validation. The following mitigations require team validation.

| Risk | Potential impact | Proposed mitigation and evidence |
|---|---|---|
| Personal information exposure | Disclosure of student or organization records | Use synthetic demo data, minimize fields and inspect screenshots before publication. |
| Excessive permissions | Unauthorized record access or decisions | Technical owners verify role and ownership checks and retain negative-test evidence. |
| Accessibility barriers | Users cannot navigate or understand forms | Retain preview checks and complete runtime keyboard, screen-reader and zoom reviews. |
| Uncredited reuse | Misrepresentation or licence conflict | Cite external sources and verify licences for reused assets and code. |
| Unsupported findings | Readers mistake synthetic analysis for field research | State zero real participants and preserve Unknown department assumptions. |
| Unclear accountability | Decisions and defects lack owners | Maintain dated Jira actions, reviewer decisions and contribution evidence. |

## 8 Conclusion and References

The team has produced planning records and reviewable requirements/design contributions. Integrated application readiness and final acceptance remain open. The final conclusion must be updated from verified demonstration evidence.

### Source register

| Source | Use in this report |
|---|---|
| CCA Team Project Guidelines for UG Students, supplied course document | Required structure, models, submission evidence and participation |
| [KAN-8](https://gundatharuntej2006.atlassian.net/browse/KAN-8) | Planning baseline, WBS and risks |
| [KAN-9](https://gundatharuntej2006.atlassian.net/browse/KAN-9) | Dated teammate handovers and verification updates |
| [KAN-19](https://gundatharuntej2006.atlassian.net/browse/KAN-19) | SRS v0.2 and pending baseline decisions |
| [PR #1](https://github.com/gundatharuntej2006-hue/InternTrack/pull/1) | Requirements and workflow contribution |
| [PR #3](https://github.com/gundatharuntej2006-hue/InternTrack/pull/3) | Design and template delivery |
| [Accessibility source at inspected commit](https://github.com/gundatharuntej2006-hue/InternTrack/blob/cec841975d6e12b2c2cf84e9cca088f65843fe8a/docs/design/UA6_accessibility.html) | Author-reported preview results and pending runtime checks |

Add asset, library and diagram references when final technical material is inserted.


## Design and verification evidence

Atul’s PR #3 delivered 20 templates, shared CSS, forms and design contracts. Its source documents are under docs/design on the atul branch. At the last check PR #3 remained open. The 25 November accessibility report records 20/20 automated template checks, 11/11 contrast pairs and 19/19 mobile previews passing. These results are reported by Atul. Running-app retesting, NVDA and 200% zoom remain pending. Clarify the report’s WCAG 2.1 AA target against KAN-49’s 2.2 AA target before final submission.

Kunal’s 24 November update reports PR #1 merged into main and 30 local tests with passing push/PR CI for follow-up commit 02050cfd6441305098f77d63ed283a3c0d00d3d0. PR #2 was open at that check. Integrated acceptance remains unverified in the reviewed evidence.

## Final editorial gate

Before export, insert the agreed process-model justification and final design figures, confirm technical evidence and citations, update the conclusion, and remove all unresolved editorial placeholders. Keep assumptions and known limitations visible. Submission cutoff, channel, required file naming and presentation time require instructor confirmation.
