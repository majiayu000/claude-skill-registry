---
name: apply-migration
description: Apply SQL migration files to JusticeHub Supabase database with verification and error handling.
---

# Apply Database Migration

**Invocation**: `/apply-migration <migration-file>`

## Usage

```bash
/apply-migration 20260102_alma_unification_links.sql
```

## How It Works

1. Reads migration from `supabase/migrations/`
2. Connects to Supabase using `.env.local` credentials
3. Executes SQL via direct PostgreSQL connection
4. Verifies created tables/columns
5. Logs success/failure

## Prerequisites

- `.env.local` with `NEXT_PUBLIC_SUPABASE_URL`, `SUPABASE_DB_PASSWORD`
- Migration file in `supabase/migrations/`
- `pg` library installed

## Connection

```
postgresql://postgres:PASSWORD@HOST:6543/postgres
```

Fallback to session pooler if direct fails.

## Success Output

```
✅ Migration executed successfully!
🔍 Verifying tables...
   ✅ article_related_interventions
   ✅ alma_intervention_profiles
🎉 Migration Complete!
```

## Failure Output

```
❌ Error: syntax error at or near "CRATE"

📋 Manual alternative:
   1. Open Supabase Dashboard → SQL Editor
   2. Copy from: supabase/migrations/bad_migration.sql
   3. Fix syntax and run
```

## Safety Features

- Transaction safety
- Idempotent checks (`IF NOT EXISTS`)
- Proper connection cleanup
- Backup reminder

## Files

- Script: `scripts/apply-migration-skill.mjs`
- Migrations: `supabase/migrations/*.sql`

## Related

- `/create-migration` - Generate new migration
- `/verify-schema` - Check database schema
