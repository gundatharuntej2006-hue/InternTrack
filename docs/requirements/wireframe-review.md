# RA-9 review of Atul's UI and architecture handoff

Reviewed by Kunal's Requirement and Analysis workstream on 20 November 2026.
Sources are Jira attachment 10002 and screenshot 10001 on KAN-44, schema attachment 10004 on KAN-45, contracts attachment 10006 on KAN-46 and template archive 10007 on KAN-47. Requirements reference KAN-17 and state rules KAN-18.

## Review result

The design covers the core invited-login, opportunity publication, application, recommendation, decision, placement and check-in journey. The role navigation, public versus private decision text, learning goals, duplicate/late messages and pending/overdue queue align with the user stories at design level. Review findings below need owner follow-up. Integrated behavior and actual accessibility checks remain to be run against the application.

The screenshot and HTML source were inspected. The prototype uses same-page anchors. Static inspection verifies anchor targets, while backend interactions and keyboard/screen-reader behavior require the working application. The archive contains Django templates plus preview variants and forms.py.

## Findings

| ID | Requirement | Evidence | Requested change | Verification |
| --- | --- | --- | --- | --- |
| UI-01 | FR2 AC2.1 and AC2.3 | O2 offers Save draft and Submit for review. `opportunities/form.html` says Save as a draft any time. `OpportunityForm` requires description, eligibility, mode, dates, deadline and mentor for both actions. | Distinguish save versus submission validation in the form/service contract. Permit incomplete draft fields according to the agreed draft-save minimum, while enforcing complete valid data before Pending Review. Confirm draft nullable/default model fields match that behavior. | Save a partial draft, reopen it, then attempt incomplete submission and see field errors with no state change. |
| UI-02 | FR4 AC4.1 and RA-6 deadline contract | S1/S2/O2 show date-only deadlines. New templates show time but omit a visible timezone, and datetime-local help omits the interpretation timezone. | Show full date, time and IST/Asia-Kolkata timezone, including the organization deadline input. Explain that applications close at the stated instant. Align listing, details, review and form contracts. | Same instant displayed consistently. Server accepts just before and rejects at/after deadline. |
| UI-03 | FR8 AC8.3 | S5 wireframe only shows Mentor replied, with no feedback text/detail link. `placements/my_placement.html` already renders the comment. | Align S5 with the newer template by showing mentor feedback or an accessible detail link. Include the mentor and response time so the student can understand the reply. | Student owner can read actual permitted feedback. Assigned mentor and coordinator access verified in app. |
| UI-04 | FR3 manual close, FR7 AC7.1-7.2 | C2 wireframe omits closing a Published opportunity. New `review_list.html` has the Close form. C4 decision screen does not show which mentor will be used. | Align C2 wireframe with the existing Published/Close section. Show the opportunity's assigned mentor on C4 and clearly surface missing/invalid mentor and active-placement conflicts. Mentor can be derived from the approved opportunity without adding another role or editable ownership field. | Authorized early closure hides the listing immediately. Selection either creates one placement with displayed mentor/goals or rolls back fully. |
| UI-05 | FR2/FR3 returned cycle | O1 shows Returned with see comment, but the wireframe has no Edit/resubmit target and O2 Save draft anchor has no href. The templates already contain an Edit link and action-specific submit buttons. | Link Returned/Draft to edit and show the retained return explanation. Make the draft-save and correction/resubmission journey explicit in the prototype. | Return with reason, owner corrects, resubmits, coordinator reviews again. |
| UI-06 | FR10 AC10.1 | KAN-46 section 7 lists only the owning org representative as publication recipient. | If FR10 is retained, add eligible invited students to publication-notice recipients and preserve per-recipient access. The Notification enum also needs event types or an explicit mapping for the contract's Opportunity submitted and Application submitted events. | Student sees publication notice on next page load. Unauthorized recipients receive no notice content or object access. |

## Schema decisions owned by Requirement and Analysis

1. Use exactly the three roles STUDENT, COORDINATOR and ORG_REP. An ORG_REP can act as an assigned mentor. Placement/check-in/feedback permission must check assignment even when that person belongs to the same organization.
2. Each ORG_REP belongs to one organization in MVP. A single organization may have multiple representatives. Derive organization from the authenticated user for all writes.
3. A recorded organization recommendation is required before coordinator selection. The recommendation remains advice and the coordinator records the final decision and reason. A prior recommendation is not required for coordinator decline from Under Review or Shortlisted. Submitted first moves to Under Review. Unconfirmed recommendations do not alter student status.

These are Member 1's requirements decisions for the prototype. Department-policy validation and whole-team baseline sign-off remain open. Recommendation gating for decline is an explicit clarification of the previous draft.

The one-feedback-per-check-in design is a reasonable MVP proposal for the team to confirm. Tharun owns acceptance of the OpportunityEvent implementation and migration. Retaining opportunity review history supports the requirements. KAN-45's description should reflect the attachment's twelve tables, including OpportunityEvent.

## Status contract

No display-label changes are requested. Opportunity uses Draft, Pending Review, Published, Returned, Closed. Application uses Submitted, Under Review, Shortlisted, Selected, Declined. Placement uses Active, Completed. Recommendation actions use Shortlist, Select, Decline and remain separate from application statuses. Overdue is a calculated follow-up flag, separate from placement lifecycle state.

RA-9 can close when this review and its actual gaps are posted on KAN-44. KAN-18 and KAN-19 require whole-team agreement/sign-off. Architecture/database feasibility and integrated UI acceptance belong to their respective owners and working-build reviews.
