---
name: "supabase-sql"
description: "Clean and format SQL migrations for Supabase - idempotency, RLS policies, formatting, schema fixes. Use when: fix this SQL, clean migration, RLS policy, Supabase schema, format postgres, prepare for SQL Editor, idempotent migration."
---

<objective>
Clean and format SQL migrations for direct paste into Supabase SQL Editor. Ensures idempotency, proper RLS policies (especially service role patterns), standardized formatting, and dependency documentation.
</objective>

<quick_start>
**Clean any SQL migration:**

1. Fix typos (`- ` → `-- ` for comments)
2. Add idempotency (`IF NOT EXISTS`, `DROP ... IF EXISTS`)
3. Fix RLS policies (service role uses `TO service_role`, not JWT checks)
4. Remove dead code (unused enums)
5. Standardize casing (`NOW()`, `TIMESTAMPTZ`)
6. Add dependencies comment at end

```sql
DROP POLICY IF EXISTS "Policy name" ON table_name;
CREATE POLICY "Policy name" ON table_name ...
```
</quick_start>

<success_criteria>
SQL cleanup is successful when:
- All policies and triggers use `DROP ... IF EXISTS` before `CREATE`
- Service role policies use `TO service_role` (not JWT checks)
- Indexes use `IF NOT EXISTS`
- No unused enums remain
- Dependencies listed at end of migration
- SQL runs without errors in Supabase SQL Editor
</success_criteria>

<core_patterns>
Clean SQL migrations for direct paste into Supabase SQL Editor.

## Cleanup Checklist

Run through each item:

1. **Fix typos** - Common: `- ` instead of `-- ` on comment lines
2. **Add idempotency** - `IF NOT EXISTS` on indexes, `DROP ... IF EXISTS` before policies/triggers
3. **Remove dead code** - Enums created but never used (TEXT + CHECK often preferred)
4. **Fix RLS policies** - Service role must use `TO service_role`, not JWT checks
5. **Standardize casing** - `NOW()` not `now()`, `TIMESTAMPTZ` not `timestamptz`
6. **Remove clutter** - Verbose RAISE NOTICE blocks, redundant comments, file path headers
7. **Validate dependencies** - List required tables at end

## Output Format

```sql
-- ============================================
-- Migration Name
-- Created: YYYY-MM-DD
-- Purpose: One-line description
-- ============================================

-- ============================================
-- Table Name
-- ============================================

CREATE TABLE IF NOT EXISTS ...

-- ============================================
-- Indexes
-- ============================================

CREATE INDEX IF NOT EXISTS ...

-- ============================================
-- Row Level Security
-- ============================================

ALTER TABLE ... ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "..." ON ...;
CREATE POLICY "..." ON ...

-- ============================================
-- Functions
-- ============================================

CREATE OR REPLACE FUNCTION ...

-- ============================================
-- Triggers
-- ============================================

DROP TRIGGER IF EXISTS ... ON ...;
CREATE TRIGGER ...
```

## Common Fixes

### RLS Policy for Service Role

```sql
-- WRONG (doesn't work reliably)
CREATE POLICY "Service role access" ON my_table
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role');

-- CORRECT
CREATE POLICY "Service role access" ON my_table
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
```

### Idempotent Policies

```sql
-- Always drop before create
DROP POLICY IF EXISTS "Policy name" ON table_name;
CREATE POLICY "Policy name" ON table_name ...
```

### Idempotent Triggers

```sql
DROP TRIGGER IF EXISTS trigger_name ON table_name;
CREATE TRIGGER trigger_name ...
```

### Unused Enums

If you see enum created but table uses `TEXT CHECK (...)` instead, remove the enum:

```sql
-- DELETE THIS - never used
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'my_enum') THEN
        CREATE TYPE my_enum AS ENUM ('a', 'b', 'c');
    END IF;
END$$;

-- Table actually uses TEXT with CHECK (keep this)
status TEXT NOT NULL CHECK (status IN ('a', 'b', 'c'))
```

## Dependencies Section

Always end with dependencies note if tables are referenced:

```sql
-- Dependencies: businesses, call_logs, subscription_plans
-- Requires function: update_updated_at_column()
```

## Reference Files

- `reference/rls-patterns.md` - Common RLS policy patterns for Supabase
- `reference/function-patterns.md` - Trigger functions, atomic operations
