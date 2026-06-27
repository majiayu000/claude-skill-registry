---
name: data-contract-migrations
description: Design and verify data contracts, schema changes, migrations, rollbacks, backfills, compatibility windows, tenant isolation, and API-to-database field mapping. Use when changing database schema, event payloads, persisted documents, analytics tables, multi-tenant data boundaries, or any user-visible data contract where silent fallback or undeclared fields would be dangerous.
---

# Data Contract Migrations

## Purpose

Use this skill when data shape changes can break reads, writes, reports, tenants, or integrations. The goal is an explicit compatibility and migration plan, not just a SQL diff.

## Preflight

Gather these facts before proposing changes:

1. Current schema, models, serializers, API contracts, and persisted samples.
2. Writers and readers of each field.
3. Migration tool and rollback support.
4. Data volume, tenant boundaries, and backfill cost.
5. Required zero-downtime or maintenance-window constraints.
6. Existing tests or fixtures that prove compatibility.

If the current data does not contain a field, treat it as absent. Do not invent fallback fields.

## Migration Design

Use expand-migrate-contract for production systems:

1. Expand: add nullable columns, new tables, new enum values, or versioned payloads without breaking old readers.
2. Dual-write or adapter: write both old and new forms when needed.
3. Backfill: migrate historical data with batching, checkpoints, and retry behavior.
4. Read switch: move readers to the new contract after verification.
5. Contract: remove old fields only after the compatibility window and rollback risk pass.

For small systems, a direct migration is acceptable only when downtime, rollback, and data loss risks are explicitly low.

## Required Checks

Every plan must include:

- Forward migration command.
- Rollback or roll-forward recovery command.
- Backfill idempotency and resume behavior.
- Data validation query before and after.
- Tenant isolation check when tenants exist.
- API/serializer compatibility test.
- Observability for migration progress and failure.

## Output Shape

```text
contract_change:
affected_readers_writers:
migration_strategy:
backfill_plan:
rollback_or_recovery:
tenant_and_security_checks:
verification_queries:
test_commands:
release_gate:
```

Raise errors for missing critical data rather than warning and falling back to incomplete output.
