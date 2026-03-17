---
name: database-schema-sync
description: Database schema management using idempotent sync script instead of Alembic migrations. Use when (1) Adding new database tables, (2) Adding new columns to existing tables, (3) Modifying database schema, (4) Deploying to production, (5) Syncing schema across environments. REQUIRED APPROACH - ALWAYS use scripts/sync-production-schema.py with --dry-run first, NEVER run Alembic migrations directly in production.
---

# Database Schema Management

## USE SCHEMA SYNC SCRIPT, NOT ALEMBIC MIGRATIONS

**PREFERRED APPROACH:** Smart schema sync script that detects and applies only missing changes.

## STRICT RULES

* ✅ **ALWAYS USE:** `scripts/sync-production-schema.py` for production deployments
* ✅ **IDEMPOTENT:** Can run multiple times safely without errors
* ✅ **TRANSPARENT:** Shows exactly what will change before applying
* ❌ **AVOID:** Running Alembic migrations directly in production
* ❌ **AVOID:** Manual SQL scripts that aren't version controlled
* ⚠️ **KEEP:** Alembic migration files for documentation purposes only

## Why Schema Sync Script?

**✅ Advantages:**
* **Simpler:** One script vs managing many migration files
* **Safer:** Checks what exists before applying changes
* **Idempotent:** Run multiple times without errors
* **Transparent:** Shows diff before applying
* **Flexible:** Works with any database state (dev, staging, prod)
* **No tracking:** No need to manage "which migrations have run"

**❌ Alembic Migration Problems:**
* Fails if run twice (not idempotent)
* Requires tracking which migrations applied
* All-or-nothing (can't skip one migration)
* Complex rollback scenarios
* Team coordination overhead

## Workflow

### 1. DRY RUN FIRST (Always!)

```bash
# Show what would change WITHOUT applying
python scripts/sync-production-schema.py --dry-run
```

### 2. REVIEW OUTPUT

```bash
# Output shows:
# ✓ Tables/columns that already exist (skipped)
# ℹ New tables/columns that would be created
# ⚠ Any potential issues
```

### 3. APPLY TO PRODUCTION

```bash
# Apply changes to production database
export DATABASE_URL="postgresql://..."
python scripts/sync-production-schema.py --apply
```

### 4. VERIFY

```bash
# Connect and verify schema
psql "$DATABASE_URL" -c "\dt"  # List tables
psql "$DATABASE_URL" -c "\d table_name"  # Describe table
```

## Required Locations

* **Schema Sync Script:** `/Users/aideveloper/core/scripts/sync-production-schema.py`
* **Documentation:** `/Users/aideveloper/core/docs/deployment/SCHEMA_SYNC_GUIDE.md`
* **Alembic Migrations (for documentation):** `/Users/aideveloper/core/src/backend/alembic/versions/`

## When to Update Schema

### Adding New Tables

1. Define models in `src/backend/app/models/`
2. Add table creation logic to `scripts/sync-production-schema.py`
3. Update `docs/deployment/SCHEMA_SYNC_GUIDE.md` with new table info
4. Test with `--dry-run` first
5. Apply to dev, staging, then production

### Adding New Columns

1. Update model in `src/backend/app/models/`
2. Add column check and ADD COLUMN logic to sync script
3. Use IF NOT EXISTS patterns for safety
4. Test with `--dry-run` first
5. Apply to environments

## Safety Checks Built-In

* ✅ Checks table exists before creating
* ✅ Checks column exists before adding
* ✅ Transaction safety (rollback on error)
* ✅ Dry-run mode to preview changes
* ✅ Color-coded output for easy reading
* ✅ Summary of all changes applied

## Integration with CI/CD

**Railway Deployment:**
```yaml
# In Procfile or deploy script
release: python scripts/sync-production-schema.py --apply
```

**GitHub Actions:**
```yaml
- name: Sync Production Schema
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: python scripts/sync-production-schema.py --apply
```

## ENFORCEMENT

* ❌ **NEVER** run `alembic upgrade head` in production
* ❌ **NEVER** manually execute SQL in production without sync script
* ❌ **NEVER** skip dry-run step for production changes
* ✅ **ALWAYS** use `scripts/sync-production-schema.py` for schema changes
* ✅ **ALWAYS** run `--dry-run` before `--apply`
* ✅ **ALWAYS** verify changes in dev/staging before production
* ✅ **ALWAYS** update documentation when adding new tables/columns

## VIOLATION CONSEQUENCES

* Database schema drift between environments
* Failed deployments from migration conflicts
* Data loss from incorrect migrations
* Production downtime from schema errors
* Team confusion about database state

**THIS IS A REQUIRED STANDARD. USE SCHEMA SYNC SCRIPT FOR ALL DATABASE CHANGES.**

## Reference Files

See `references/sync-vs-alembic.md` for detailed comparison of sync script vs Alembic migrations.

See `references/workflow-examples.md` for code examples of adding tables, columns, indexes, and handling complex migrations.

Run `scripts/verify-sync-script.sh` to validate that sync script exists and is properly configured.
