# RA-11 / RA-12 opportunity handoff

Kunal's Django services are in `apps/opportunities/services.py`, using the KAN-45 schema and KAN-18 display-state contract. They implement partial draft saving, owner-only submission, coordinator approval/return/manual close, idempotent deadline expiry, listing/detail filtering and the application-time open check. State and OpportunityEvent persist atomically. Updates lock the row and reject stale `updated_at` snapshots.

DT-3 accounts and the KAN-50 feature migrations are still pending in the repository at this handoff. The services accept the shared ORM instances so those model implementations can call them directly. Test-only unmanaged UA-2 fixture models exercise the service's real database transactions. They are created and removed by the tests and do not change production migrations.

## Model and view wiring

- Opportunity uses the field names from KAN-45, including `organization`, `created_by`, `mentor`, `approved_by`, `approved_at`, `updated_at`, `return_reason`, `closed_reason` and uppercase `state` values.
- OpportunityEvent should expose `Opportunity.review_events` with `related_name="review_events"`. It stores `from_state`, `to_state`, nullable `actor`, `reason` and automatic `created_at`. Restrict edit/delete product operations to keep history append-only.
- An authenticated active account supplies `role` and `organization_id`. Views derive actor from `request.user`. View permissions must filter object access before service calls and convert forbidden cross-owner access to the agreed 404 response.
- Draft columns must allow incomplete content until submission. Views clean submitted field types and lengths, but require complete fields only for the submit action. The service rejects posted ownership/state/approval fields.
- List and direct detail views use `student_visible(queryset)`. Student application creation locks the same opportunity inside its transaction and calls `require_open_for_application()` immediately before creating the application. This coordinates deadline/manual-close checks with opportunity actions.
- POST routes are those in KAN-46. Keep CSRF protection and return form validation errors on the owning role's page. Route trusted expiry maintenance to `expire()` without exposing a student/representative expiry action.
- Send in-app notifications after the transaction commits. FR10 still needs the publication-recipient correction logged on KAN-44/46.

Tests run with `python manage.py test apps.core.test_opportunities -v 2`. The existing CI workflow also discovers this module through the full Django suite against PostgreSQL. Record actual CI run URLs/results in KAN-24. DB-backed unit passes alone leave end-to-end UI, real-account permission and application concurrency integration to be validated once their modules exist.

The production approval timestamp uses server time, while caller-supplied aware `now` supports deterministic deadline checks and trusted scheduler evaluation. Persist UTC-aware values and display full date/time in Asia/Kolkata. At the exact deadline, student visibility and application eligibility end even if expiry maintenance has not run.
