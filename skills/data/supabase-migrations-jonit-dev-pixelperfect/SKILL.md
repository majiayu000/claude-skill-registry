---
name: supabase-migrations
description: Create and manage Supabase database migrations using MCP tools. Use when creating tables, modifying schemas, adding RLS policies, or working with database structure.
---

# Supabase Migrations

## MCP Tools Available

- `mcp__supabase__apply_migration` - Apply DDL changes
- `mcp__supabase__execute_sql` - Run queries (not for DDL)
- `mcp__supabase__list_tables` - View existing tables
- `mcp__supabase__list_migrations` - View migration history
- `mcp__supabase__get_advisors` - Check for security/performance issues

## Project ID

Use `mcp__supabase__list_projects` to find the project ID first.

## Migration Naming

Use snake_case: `create_users_table`, `add_credits_column`, `enable_rls_on_images`

## Standard Patterns

### Create Table with RLS

```sql
CREATE TABLE public.images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.images ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own images"
  ON public.images FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own images"
  ON public.images FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

### Add Column

```sql
ALTER TABLE public.users
ADD COLUMN credits INTEGER DEFAULT 0 NOT NULL;
```

### Create Index

```sql
CREATE INDEX idx_images_user_id ON public.images(user_id);
```

## Post-Migration

Always run `mcp__supabase__get_advisors` with type "security" after DDL changes to catch missing RLS policies.

## TypeScript Types

After schema changes, use `mcp__supabase__generate_typescript_types` to update types.
