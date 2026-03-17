---
name: supabase-migration-writer
description: Expert assistant for Supabase database operations in the KR92 Bible Voice project. Use when (1) creating database migrations, (2) adding/modifying tables or RLS policies, (3) creating RPC functions, (4) querying Supabase configuration (secrets, Edge Functions, schemas), (5) writing rollback scripts, or (6) answering questions about database schema and configuration.
---

# Supabase Migration Writer

## Context Files (Read First)

For schema and Supabase layout, read from `Docs/context/`:
- `Docs/context/db-schema-short.md` - Database schema overview
- `Docs/context/supabase-map.md` - Edge Functions, migrations, access matrix

**Cross-cutting learnings:** See `.claude/LEARNINGS.md` → "Supabase/Database" section for RLS+GRANT patterns, RPC gotchas, and CHECK constraints.

## Quick Reference

- **Project ID**: `iryqgmjauybluwnqhxbg`
- **Migrations**: `supabase/migrations/`
- **Edge Functions**: `supabase/functions/`

## Migration File Convention

```
supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

Example: `20250124120000_add_user_notes_table.sql`

## Essential Patterns

### Create Table with RLS
```sql
CREATE TABLE IF NOT EXISTS public.table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_table_user_id ON public.table_name(user_id);

ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data"
ON public.table_name FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can insert own data"
ON public.table_name FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.table_name
FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();
```

### Add Column
```sql
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS new_column TEXT DEFAULT 'value';

COMMENT ON COLUMN public.table_name.new_column IS 'Description';
```

### Create RPC Function
```sql
CREATE OR REPLACE FUNCTION public.function_name(
  p_user_id UUID DEFAULT auth.uid(),
  p_limit INT DEFAULT 20
)
RETURNS TABLE (col1 UUID, col2 TEXT)
LANGUAGE sql STABLE SECURITY DEFINER
SET search_path TO 'public', 'bible_schema'
AS $$
  SELECT col1, col2
  FROM table_name
  WHERE user_id = p_user_id
  LIMIT p_limit;
$$;

GRANT EXECUTE ON FUNCTION public.function_name TO authenticated;
```

## Data Types Quick Reference

| Use Case | Type |
|----------|------|
| ID | `UUID DEFAULT gen_random_uuid()` |
| User ref | `UUID REFERENCES auth.users(id)` |
| Text | `TEXT` |
| Boolean | `BOOLEAN DEFAULT true` |
| Timestamp | `TIMESTAMPTZ DEFAULT now()` |
| Number | `INTEGER` |
| Decimal | `NUMERIC(10,2)` |
| JSON | `JSONB DEFAULT '{}'` |
| Array | `TEXT[] DEFAULT '{}'` |
| Enum | `TEXT CHECK (col IN ('a', 'b'))` |

## MCP Tools Available

Use Supabase MCP tools directly:

```
mcp__supabase__list_tables        # List all tables
mcp__supabase__execute_sql        # Run queries
mcp__supabase__apply_migration    # Apply DDL
mcp__supabase__list_edge_functions
mcp__supabase__get_logs           # Debug issues
mcp__supabase__get_advisors       # Security/perf checks
```

## References

- **Context docs**: `Docs/context/db-schema-short.md`, `Docs/context/supabase-map.md` (authoritative)
- **Secrets & env vars**: See [references/secrets.md](references/secrets.md)

## Testing Migrations

```bash
# Apply locally
supabase db push

# Reset and reapply all
supabase db reset
```

## Best Practices Checklist

- [ ] Use `IF NOT EXISTS` / `IF EXISTS`
- [ ] Add `created_at` and `updated_at` timestamps
- [ ] Enable RLS on all tables
- [ ] Add indexes for foreign keys and filtered columns
- [ ] Use `SECURITY DEFINER` for RPC functions
- [ ] Set `search_path` in functions
- [ ] Add `COMMENT ON` for documentation
- [ ] Create rollback script for complex changes
- [ ] **Update TypeScript types after migration** (see learnings)

## CRITICAL: Type Synchronization

**After ANY migration that adds tables, columns, or RPC functions:**

```bash
npx supabase gen types typescript --project-id iryqgmjauybluwnqhxbg > apps/raamattu-nyt/src/integrations/supabase/types.ts
```

If types can't be regenerated, manually add to `types.ts`. See [references/learnings.md](references/learnings.md) for patterns and workarounds.

**Why this matters:** Lovable Cloud uses the committed `types.ts` file. If types are out of sync, builds fail.
