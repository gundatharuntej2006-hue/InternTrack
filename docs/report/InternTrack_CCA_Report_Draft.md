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

Ritika maintains the WBS, schedule, dependencies, risk register and action log. The recorded submission target is 27 November. Internal targets are tentative: report compilation and proposed integration testing on 24 November, team review and rehearsal on 25 November, and final file/access checks on 26 November. Technical owners must confirm feasibility. The detailed planning record remains in KAN-8, with actions in KAN-9.

## 5 Software Design

Atul’s design workstreams cover navigation/wireframes (KAN-44), schema and permissions (KAN-45), and architecture/contracts (KAN-46). Kunal reported reviewing these and recording six findings. Final design approval is pending.

[INSERT REVIEWED FIGURES: DFD Levels 0, 1 and 2; data dictionary; sequence diagram with normal and alternative flows; architecture and deployment diagrams. Add titles, figure numbers, technology rationale and scalability explanation.]

## 6 Tools and Collaboration

Jira tracks tasks, owners, milestones, status and handovers. Repository: https://github.com/gundatharuntej2006-hue/InternTrack . Board: https://gundatharuntej2006.atlassian.net/jira/software/projects/KAN/boards/2 .

Ritika prepared the planning tracker, WBS, risk register, action log, report structure and submission review procedure. Kunal’s contribution includes requirements, synthetic walkthroughs, workflow services and tests in PR #1. Tharun reported DT-1 repository/setup delivery. Atul’s design review material is referenced above. Final commit and contribution evidence for each member must be checked before submission.

## 7 Ethical and Professional Considerations

Use synthetic demonstration data and minimize personal information. Validate role and record access with technical owners. Review accessibility and clear status wording, attribute external material, and disclose assumptions and validation limits. These are proposed mitigations requiring team validation. The draft ethics table is maintained in KAN-10 for team validation.

## 8 Conclusion and References

The team has produced planning records and reviewable requirements/design contributions. Integrated application readiness and final acceptance remain open. The final conclusion must be updated from verified demonstration evidence.

Sources: CCA_Team_Project_Guidelines_UG_Students.docx; Jira KAN-8, KAN-9, KAN-19, KAN-44/45/46; Kunal’s 23 November updates on KAN-9; repository PR #1. Add references for any reused technical assets and diagrams supplied by the team.


## Design and verification evidence

Atul’s PR #3 delivered 20 templates, shared CSS, forms and design contracts. Its source documents are under docs/design on the atul branch. At the last check PR #3 remained open. The 25 November accessibility report records 20/20 automated template checks, 11/11 contrast pairs and 19/19 mobile previews passing. These results are reported by Atul. Running-app retesting, NVDA and 200% zoom remain pending. Clarify the report’s WCAG 2.1 AA target against KAN-49’s 2.2 AA target before final submission.

Kunal’s 24 November update reports PR #1 merged into main and 30 local tests with passing push/PR CI for follow-up commit 02050cfd6441305098f77d63ed283a3c0d00d3d0. PR #2 was open at that check. Integrated acceptance remains unverified in the reviewed evidence.

## Final editorial gate

Before export, insert the agreed process-model justification and final design figures, confirm technical evidence and citations, update the conclusion, and remove all unresolved editorial placeholders. Keep assumptions and known limitations visible. Submission cutoff, channel, required file naming and presentation time require instructor confirmation.
