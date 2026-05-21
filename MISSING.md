# Missing Pieces

This file tracks missing or incomplete rewrite surfaces that were patched with lightweight compatibility behavior so the app can build and run.

## Compatibility placeholders

- `apps.console.api.v1` namespace: added as a compatibility package that points at `apps/api/v1` and `apps/_tasks` so legacy imports keep resolving.
- `apps.console.billing`: recreated as a placeholder self-hosted billing domain with minimal models for plan, billing, and PayPal credit references.
- `rest_framework.serializers.NullBooleanField`: shimmed in `apps/api/v1/__init__.py` because DRF 3.15 removed it while many serializers still use it.
- `apps/api/v1/utils/api_filters.py`: recreated with a minimal `DateRangeFilter` backend because the module was missing from the rewrite.
- `apps/api/v1/utils/api_permissions.py`: added a minimal authenticated-only `MemberPermissions` class. This is a placeholder, not a full rewrite of the original permission logic.
- `apps/utils/api_exceptions.py`: added as a compatibility alias for the current `apps/api/v1/utils/api_exceptions.py` module.
- `billing_sync_all`: added as a placeholder Celery task because the rewrite currently imports it but does not implement it.

## Optional legacy surfaces currently skipped

- Billing-backed API routes are conditionally skipped when their imports fail because the `apps.console.billing` domain is not present in the current rewrite.
- Celery autodiscovery is skipped when async workers are disabled so lite mode does not import unfinished billing-dependent integration tasks during startup.

## Dependency gaps fixed during boot work

- Added `djangorestframework-datatables`
- Added `twilio`
- Added `firebase-admin`
- Added `stripe`
- Added `boto`

## Remaining work

- Restore or intentionally replace the missing `apps.console.billing` domain.
- Replace placeholder compatibility utilities with proper rewrite implementations.
- Revisit permission behavior once core boot and SQLite lite mode are stable.