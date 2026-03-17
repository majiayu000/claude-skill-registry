---
name: supabase-migrations
description: Create and manage Supabase database migrations. Use when making schema changes, creating tables, adding columns, or managing database structure. Triggers on "migration", "schema", "database", "table", "Supabase".
---

# Supabase Database Migrations

Create, test, and deploy Supabase database migrations safely.

## When to Use

- User mentions "migration", "schema change", "database"
- User wants to create/modify tables
- User asks about Supabase database structure
- User needs to add columns, indexes, or constraints
- User mentions RLS or Row Level Security

## Migration Workflow

```bash
# Create new migration
npx supabase migration new <name>

# Test locally (resets local DB)
npx supabase db reset

# Push to production
npx supabase db push

# Repair if remote is out of sync
npx supabase migration repair --status applied <version>
```

## Migration File Format

**Location:** `supabase/migrations/`
**Format:** `YYYYMMDDHHMMSS_description.sql`

### Example Migration

```sql
-- supabase/migrations/20250106120000_add_user_preferences.sql

-- Add new column
ALTER TABLE users
ADD COLUMN preferences JSONB DEFAULT '{}';

-- Create index for faster queries
CREATE INDEX idx_users_preferences ON users USING GIN (preferences);

-- Add RLS policy
CREATE POLICY "Users can update own preferences"
ON users
FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);
```

## Key Rules

### DO:
- Test migrations locally first with `npx supabase db reset`
- Use `npx supabase migration repair` if remote is out of sync
- Create new migrations (never modify applied ones)
- Include RLS policies in migrations
- Use descriptive migration names

### DON'T:
- Modify already-applied migrations
- Push untested migrations to production
- Forget RLS policies on new tables
- Use destructive operations without backup

## Common Patterns

### Create Table with RLS

```sql
-- Create table
CREATE TABLE items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Policy: Users see own items
CREATE POLICY "Users can view own items"
ON items FOR SELECT
USING (auth.uid() = user_id);

-- Policy: Users insert own items
CREATE POLICY "Users can insert own items"
ON items FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### Add Column Safely

```sql
-- Add nullable column first
ALTER TABLE users ADD COLUMN phone TEXT;

-- Then add constraint if needed
ALTER TABLE users
ALTER COLUMN phone SET NOT NULL,
ADD CONSTRAINT phone_format CHECK (phone ~ '^\+[0-9]{10,15}$');
```

## Debugging

```bash
# Check migration status
npx supabase migration list

# Query production database
npx supabase db query "SELECT * FROM items LIMIT 10;"

# View table structure
npx supabase db query "\d items"
```

## Environment Setup

Ensure Supabase CLI is linked to your project:

```bash
npx supabase link --project-ref <project-id>
```
