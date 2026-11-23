# RA-6 - Proposed shared state contract

Version 0.2, 20 November 2026. Member 1 requirements clarification after review of KAN-44/45/46 and the KAN-47 template archive. Whole-team agreement remains pending. Labels below must match UI, model enums, DFDs and tests. Stored constants can use underscores but display labels must remain exact. All actions require authentication and server-side object permission; unlisted transitions are rejected without mutation.

## Opportunity

| From | Action / actor | To | Preconditions / effect |
| --- | --- | --- | --- |
| New | Save / own organization representative | Draft | Organization derived from actor; never student-visible |
| Draft | Submit / owning representative | Pending Review | All required fields valid; deadline future; mentor belongs to organization |
| Returned | Correct and resubmit / owning representative | Pending Review | Same validation; retain review history |
| Pending Review | Approve / coordinator | Published | Future deadline and complete fields; approval actor/time; atomic event |
| Pending Review | Return / coordinator | Returned | Nonblank return reason visible to owner; atomic event |
| Published | Close / coordinator | Closed | Closure explanation; remove student visibility immediately |
| Published | Deadline closure / system | Closed | At or after deadline; idempotent event |

Proposed policy: editable fields in Draft/Returned only; Pending Review is frozen until returned/approved; published content changes require a future reviewed correction feature, not silent edits. Returned may be saved without resubmission. Closed is terminal in MVP. These details are proposed clarifications, not stakeholder-confirmed rules.

Student visibility and application eligibility require BOTH state == Published AND server_now < deadline. Enforce on lists, filters, detail and application POST; do not rely on a scheduled closure job. At exact deadline the record is expired. Proposed displayed timezone Asia/Kolkata with offset; persist aware UTC instants and compare aware times. Start date <= end date; deadline before or at start is proposed validation requiring team agreement. Manual close and expired-state checks must work during concurrent application submissions using the shared transaction contract.

## Application

| From | Actor/action | To | Guard |
| --- | --- | --- | --- |
| New | Student applies | Submitted | Published/open opportunity; unique student/opportunity; initial event |
| Submitted | Coordinator begins review | Under Review | Public reason/next step |
| Under Review | Coordinator confirms | Shortlisted | Public reason/next step |
| Under Review | Coordinator confirms | Selected | Recommendation review; mentor; 2-3 goals; one-active-placement guard |
| Under Review | Coordinator confirms | Declined | Public reason/next step; no placement |
| Shortlisted | Coordinator confirms | Selected | Same selection guards |
| Shortlisted | Coordinator confirms | Declined | Public reason/next step; no placement |

Selected and Declined are terminal in this MVP contract. Submitted first moves to Under Review. Organization recommendation Shortlist/Select/Decline is stored separately and leaves visible application state unchanged. Member 1 decision on 20 November: a recorded organization recommendation is required before coordinator selection. Coordinator may decline from Under Review or Shortlisted without a prior recommendation, with a required public reason and next step. Recommendation remains advice and the coordinator confirms the outcome. Team sign-off on the baseline is tracked in KAN-19.

Every coordinator-confirmed transition records immutable previous/new state, actor/time and public reason/next step in the same transaction as current state. Selection also locks/checks student active placement and creates placement/goals transactionally. A repeated/concurrent selection must not leave a duplicate placement or partial event. Private notes never appear in student response payloads.

## Placement

| From | Actor/action | To | Guard |
| --- | --- | --- | --- |
| New | Successful coordinator selection | Active | One per selected application; mentor and 2-3 goals; at most one Active per student |
| Active | Coordinator completes | Completed | Final check-in exists; completion actor/time recorded |

Completed is terminal; decline never creates placement. The definition of final check-in and whether mentor acknowledgment is required for completion needs sponsor review; do not claim it is resolved. Proposed check-in week begins Monday in project timezone; one note per placement/week. A goal must belong to the same placement. Only assigned mentor writes feedback.

## Public wording examples

| Label | Safe example / next action |
| --- | --- |
| Submitted | Application received. Wait for coordinator review. |
| Under Review | Your application is being reviewed. No action is required now. |
| Shortlisted | You have been shortlisted. Follow the coordinator's next-step instructions. |
| Selected | Selection confirmed. Open your placement and review your learning goals. |
| Declined | You were not selected for this opportunity. You may review other open opportunities. |
| Returned (organization only) | Add the missing deadline and eligibility details, then resubmit. |

Actual reasons must be specific and approved by coordinator; templates are examples, not decisions about real students. Avoid confidential comparative notes, protected characteristics, invented promises and color-only labels. Show actor role, update date/time/timezone and next step separately from private notes.

## Role and schema clarification for Atul

Three roles are STUDENT, COORDINATOR and ORG_REP. Mentor access is granted by assignment to an ORG_REP account. Each representative belongs to one organization, and each organization may have multiple representatives. Same-organization membership alone does not grant access to every placement or permit feedback for an unassigned student.

Atul's v0.1 schema and forms use the same Opportunity, Application and Placement display labels and transition graph. No label changes are requested. Overdue is a calculated follow-up flag. One feedback per check-in remains a team decision. OpportunityEvent supports retained opportunity history, with migration feasibility to be confirmed by Tharun.

Changes from v0.1 clarify the decline recommendation gate and mentor/organization policy. These are requirements-owner prototype decisions derived from the proposal and schema review. Department validation and whole-team sign-off are still pending. Actual Jira references are KAN-44 wireframes, KAN-45 schema, KAN-46 contracts, KAN-47/48 templates, KAN-28 repository and KAN-29 CI.
