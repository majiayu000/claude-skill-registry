---
name: context-database-schema
description: |
  Supabase PostgreSQL schema management, 86+ migrations, RLS policies, and type generation.
  Handles table creation, schema changes, migrations, foreign key constraints, and migration workflows.
  Use when working with database schema, migrations, data modeling, or type definitions,
  or when user mentions database changes, table modifications, schema updates, migration failures,
  "relation does not exist" errors, foreign key issues, Supabase schema operations, users table, accounts table, or holdings table.
tags: [database, schema, migrations, supabase]
---

# Database Schema

Navigate Supabase database schema, 86+ migrations, and type definitions.

## Overview

PostgreSQL schema via Supabase with RLS policies. See `docs/database/SCHEMA.md`.

## Database Access

**⚠️ CRITICAL: Must be in Railway shell for all database operations**

```bash
# Verify environment first
echo $RAILWAY_ENVIRONMENT  # Must be non-empty

# If empty, enter Railway shell:
railway shell
```

**Common Queries:**

```bash
# Quick introspection
psql "$DATABASE_URL" -c "\dt"  # List all tables
psql "$DATABASE_URL" -c "\d users"  # Describe users table
psql "$DATABASE_URL" -c "\d+ accounts"  # Detailed table info with indexes

# Core tables
psql "$DATABASE_URL" -c "SELECT * FROM users LIMIT 5;"
psql "$DATABASE_URL" -c "SELECT * FROM accounts WHERE user_id = 'user_xxx';"
psql "$DATABASE_URL" -c "SELECT * FROM holdings WHERE account_id = 'acc_xxx';"
```

**Migrations:**

```bash
# Inside railway shell + supabase directory
cd supabase
supabase db push  # Apply local migrations (see health check below)
supabase db diff -f new_migration_name  # Generate migration from changes
```

**See AGENTS.md "Database Access" section for complete guide.**

## Migrations

- `supabase/migrations/` - All 86+ migrations (sequential)
- Format: `YYYYMMDD_description.sql`
- Key prefixes: `*clerk*`, `*plaid*`, `*eodhd*`

### End-to-end Checklist (schema changes)

Any time you change schema (tables, columns, indexes, RLS) or add Supabase migrations:

1. **Work in Railway dev shell**
   - Confirm: `echo $RAILWAY_ENVIRONMENT` is non-empty.
   - Use the dev `DATABASE_URL` and `SUPABASE_PROJECT_ID`.

2. **Apply migrations to dev**
   ```bash
   cd supabase
   supabase db push
   ```
   - If this fails on **old** migrations, follow the health check flow below (registry repair or idempotent DDL) before proceeding.

3. **Regenerate types and manifest**
   ```bash
   # From repo root, still in Railway shell
   export SUPABASE_PROJECT_ID=klrrntdswlvjdqusahdk  # or injected value
   make schema:generate
   ```
   - This must update:
     - `supabase/types/database.types.ts`
     - `supabase/generated/schema_manifest.json`
     - `backend/schemas/generated/**`

4. **Verify schema parity**
   ```bash
   cd backend
   PYTHONPATH=. poetry run python ../scripts/verify_generated_schemas.py
   ```
   - This is the same check Tier 2 Auth Stub uses in CI.
   - Fix any reported mismatches (missing columns, wrong nullability) before committing.

5. **Commit everything together**
   - In a feature branch:
     - `supabase/migrations/**` changes
     - `supabase/schemas/**` changes
     - Regenerated types and manifests
     - Updated `backend/schemas/generated/**`
   - Do **not** split schema SQL and generated artifacts into separate feature branches; they must land atomically.

### Migration Health Check (bd-k1c learnings)

Before adding or merging new migrations:

1. **Verify registry vs schema**
   - Run in Railway shell:
     ```bash
     cd supabase
     supabase db push
     ```
   - If it fails on **old** migrations (tables/triggers already exist), it means the schema was initialized by `golden_schema.sql` / `all_migrations.sql` / manual SQL and the migration registry is behind.

2. **If db push fails on old migrations**
   - Do **not** hack the schema via ad‑hoc SQL.
   - Instead, repair the registry or make old migrations idempotent:
     - Option A (registry repair): mark older versions as applied in `supabase_migrations.schema_migrations` (see `supabase/scripts/fix_migration_registry_bd_k1c.sql` for the bd‑k1c repair).
     - Option B (idempotent migrations): wrap non‑idempotent DDL (e.g. `CREATE TRIGGER`) in `IF NOT EXISTS` blocks so replaying them is safe.
   - Re‑run `supabase db push` after repair; only then add/merge new migrations.

3. **New migrations (forward-only rule)**
   - Prefer `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`, and `CREATE INDEX IF NOT EXISTS` when possible to make replays safe.
   - For **new migrations you add from now on**, use a **unique timestamp prefix** per file (e.g. `20251206152000_...`).
   - **RPC Functions**: ALWAYS provide default values for arguments (e.g. `filter jsonb DEFAULT '{}'`) to avoid signature mismatches with standard backends.
   - **Standard Scrape/Doc Schema**:
     - `raw_scrapes`: MUST have `storage_uri` (text).
     - `documents`: MUST have `source` (text).

4. **Dev/test-data migrations hygiene**
   - **Dev/test-data migrations** must live under `supabase/dev_migrations/`, NOT `supabase/migrations/`
   - Schema migrations (DDL, RLS, indexes, FKs) go in `supabase/migrations/`
   - Test-data seeding goes in `scripts/db-commands/` or `supabase/dev_migrations/`
   - Do not use `supabase db push --include-all` on historical migrations; treat it as debugging tool only
   - See `supabase/dev_migrations/README.md` for usage

### Migration Registry Repair (When CLI Fails)

If `supabase db push` fails with "Remote migration versions not found" (Drift), do **NOT** run manual SQL in Dashboard. This creates a vicious cycle.

**Fix:**
1. Ensure `DATABASE_URL` is set in Railway (required for CLI).
2. Run repair to sync registry with local files:
   ```bash
   # In Railway shell
   supabase migration repair --status applied <version_id>
   # Or for batch:
   supabase migration repair --status applied 20251129... 20251204...
   ```
3. Then run `supabase db push` for new migrations.

## Schema Definitions

- `supabase/schemas/public/` - Table definitions
- `supabase/schemas/public/tables/` - Individual table files

## Type Generation

- `supabase/types/database.types.ts` - Generated TypeScript types
- Generate via: `supabase gen types typescript`

## Backend Types

- `backend/schemas/generated/` - Generated Python types (if any)

## Scripts

- `scripts/db-commands/` - Database utilities
- `backend/migrations/versions/` - Alembic migrations (if used)

## Key Tables and Recent Changes

### Holdings Table (`public.holdings`)

**Core columns:**
- `id`, `account_id`, `security_id`, `quantity`, `cost_basis`
- `created_at`, `updated_at`, `closed_at`

**Active vs Closed Holdings (bd-k1c.4):**
- **Active holdings**: `closed_at IS NULL` - current portfolio positions
- **Closed positions**: `closed_at IS NOT NULL`, `quantity` conventionally `0`
- Plaid pipeline **soft-closes** positions that disappear from broker snapshots (doesn't delete)
- Manual holdings are NOT auto-closed by provider sync

**Index:**
- Partial index `idx_holdings_closed_at ON holdings(closed_at) WHERE closed_at IS NULL` for efficient active holdings queries

**Current portfolio views**: Filter with `WHERE closed_at IS NULL`

### Holdings Snapshots Table (`public.holdings_snapshots`)

**Purpose**: Append-only time-series snapshots for historical portfolio analytics (bd-k1c.6)

**Core columns:**
- `snapshot_at` (TIMESTAMPTZ) - snapshot time, typically daily at market close
- `user_id`, `account_id`, `security_id`
- `quantity`, `cost_basis`, `market_value`, `price_source`

**Key constraints:**
- `UNIQUE (snapshot_at, account_id, security_id)` for idempotency
- Indexes on `(user_id, snapshot_at DESC)`, `(account_id, snapshot_at DESC)`, `(security_id, snapshot_at DESC)`

**Relationship to holdings:**
- Snapshots derived from active holdings + price data
- Snapshot job: `backend/scripts/create_holdings_snapshot.py`

### Provider Security Mappings (`public.provider_security_mappings`)

**Purpose**: Map provider security IDs to canonical securities

**Natural key (bd-k1c.3):**
- `UNIQUE (brokerage_connection_id, provider_security_id)`
- `provider_security_id VARCHAR(255)` - stable provider-side identifier (e.g., Plaid `security_id`)
- `provider_payload JSONB` - retained for audit, NOT in uniqueness constraint

**Index:**
- `idx_provider_security_mappings_provider_security_id` for fast lookups

**Used by:**
- `RawDataService.get_existing_security_mapping`
- `SecurityResolver._link_provider_mapping` (upserts on natural key)

## Recent bd-k1c Changes

The **bd-k1c epic** (Plaid portfolio pipeline hardening) introduced several schema enhancements:

- **Holdings soft-close semantics** (`closed_at` column) - distinguishes active vs closed positions
- **Time-series snapshots** (`holdings_snapshots` table) - enables historical analytics
- **Provider mapping refinement** (`provider_security_id` natural key) - more robust brokerage integrations

See `docs/bd-k1c/EPIC_OVERVIEW.md` for full context and child features.

## Documentation

- **Internal**: `docs/database/SCHEMA.md`

## Related Areas

- See `context-clerk-integration` for RLS patterns
- See `context-plaid-integration` for plaid_prices table and provider mappings
- See `context-symbol-resolution` for securities table
- See `context-portfolio` for holdings views and analytics
