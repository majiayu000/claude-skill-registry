---
name: create-migration
description: Create Supabase database migrations and deploy edge functions for the LiTHePlan project. Use this skill whenever the user wants to add/modify tables, columns, indexes, RLS policies, functions, triggers, or deploy edge functions. Triggers on phrases like "add a column", "create a table", "write a migration", "update the schema", "deploy an edge function", "add RLS", "create an index", or any request that requires a database schema change.
---

# Supabase Migration & Edge Function Workflow

## Principle

**Read with MCP. Write with CLI.**

- Use the Supabase MCP tools (`list_tables`, `describe_table_schema`, `execute_sql`) to understand the current schema before writing anything.
- Use `bunx supabase` CLI to create migration files and deploy edge functions — never use the MCP to mutate production data directly.

---

## Migration Workflow

### 1. Understand the current schema

Before writing SQL, use MCP to read what's already there:

```
mcp: list_tables → see all tables and schemas
mcp: describe_table_schema → inspect specific table columns, types, constraints
mcp: execute_sql (SELECT only) → check existing RLS policies, indexes, sequences
```

Specifically check:
- Does the table/column already exist?
- Are there existing RLS policies that the migration might conflict with?
- Are there foreign key relationships to account for?

### 2. Draft the SQL

Write the migration SQL following these conventions:

**Naming**
- Tables: `snake_case`, plural (`user_profiles`, `course_terms`)
- Columns: `snake_case`
- Indexes: `idx_<table>_<column(s)>` (e.g., `idx_courses_user_id`)
- Functions: `snake_case` verbs (`get_user_courses`, `update_profile`)

**Structure every migration with explicit transaction handling when needed:**
```sql
-- 1. DDL changes (CREATE TABLE, ALTER TABLE, etc.)
-- 2. Indexes (CREATE INDEX CONCURRENTLY where safe)
-- 3. RLS (ALTER TABLE ... ENABLE ROW LEVEL SECURITY)
-- 4. Policies (CREATE POLICY ...)
-- 5. Grants (GRANT SELECT ON ... TO authenticated)
```

**RLS is required for any new public-schema table** — never leave a table without policies after enabling RLS. Use this pattern:

```sql
alter table public.your_table enable row level security;

create policy "Users can view their own rows"
  on public.your_table for select
  using (auth.uid() = user_id);

create policy "Users can insert their own rows"
  on public.your_table for insert
  with check (auth.uid() = user_id);
```

**Reference the `supabase-postgres-best-practices` skill** for:
- Index strategy (avoid over-indexing, use partial indexes where appropriate)
- Query performance patterns
- Connection and locking considerations

### 3. Create the migration file

Generate the timestamp and create the file:

```bash
timestamp=$(date -u +%Y%m%d%H%M%S)
# File name: supabase/migrations/${timestamp}_<short_description>.sql
# Example: supabase/migrations/20260315143022_add_term_tags_table.sql
```

Write clear SQL — include a comment at the top explaining what this migration does and why.

### 4. Validate locally (if local Supabase is running)

```bash
# Check if local is running
bunx supabase status

# If running, apply to local to validate
bunx supabase db reset --local   # full reset + replay all migrations
# OR for quick check:
bunx supabase db diff --local    # see what the diff looks like
```

If local isn't running, skip validation and flag it to the user: the migration file is ready but should be reviewed before pushing to the remote.

### 5. Push to remote (only when user confirms)

```bash
bunx supabase db push
```

Confirm with the user before running this — it's irreversible without a manual rollback migration.

---

## Edge Function Workflow

### 1. Check existing functions

```bash
ls supabase/functions/
```

Or use MCP if it supports listing edge functions.

### 2. Create or modify the function

Edge functions live in `supabase/functions/<function-name>/index.ts`. They use Deno + the `@supabase/supabase-js` client with the service role key (available as `Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')`).

**Always use the anon/service key from env, never hardcode.**

### 3. Deploy (only when user confirms)

```bash
bunx supabase functions deploy <function-name>
# For all functions:
bunx supabase functions deploy
```

---

## What NOT to do

- Don't use `execute_sql` MCP to run DDL mutations on the remote — use CLI migrations so changes are versioned.
- Don't skip RLS on public-schema tables.
- Don't use `CASCADE` deletes without discussing the implications with the user.
- Don't push to remote without the user's explicit confirmation.
