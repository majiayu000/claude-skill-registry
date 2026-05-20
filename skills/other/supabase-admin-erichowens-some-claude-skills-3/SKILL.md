---
name: supabase-admin
description: Supabase administration, RLS policies, migrations, and schema design. Use for database architecture, Row Level Security, performance tuning, auth integration. Activate on "Supabase", "RLS", "migration", "policy", "schema", "auth.uid()". NOT for Supabase Auth UI configuration (use dashboard), edge functions (use cloudflare-worker-dev), or general SQL without Supabase context.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - mcp__supabase__*
category: DevOps & Site Reliability
tags:
  - supabase
  - rls
  - database
  - postgres
  - migration
  - schema
  - security
---

# Supabase Administration Expert

Master Supabase schema design, Row Level Security policies, migrations, and performance optimization for production applications.

## When to Use

✅ **USE this skill for:**
- Row Level Security (RLS) policy design and debugging
- Database migrations and schema changes
- Auth integration (triggers, profile creation)
- Query performance optimization
- Supabase-specific SQL patterns (`auth.uid()`, `auth.jwt()`)

❌ **DO NOT use for:**
- Supabase Auth UI configuration → use Supabase dashboard docs
- Edge Functions → use `cloudflare-worker-dev` skill
- General PostgreSQL without Supabase context → use standard SQL resources
- Client-side Supabase SDK usage → use Supabase JS docs

## Core Competencies

### 1. Row Level Security (RLS)

**Always Enable RLS on User Tables:**
```sql
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;
```

**Policy Patterns:**

```sql
-- Public read, authenticated write
CREATE POLICY "Public read" ON posts FOR SELECT USING (true);
CREATE POLICY "Owners can write" ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Owner-only access
CREATE POLICY "Users own their data" ON profiles
  FOR ALL USING (auth.uid() = id);

-- Role-based access
CREATE POLICY "Admins can do anything" ON content
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );
```

**Performance-Critical: Index auth.uid() Columns:**
```sql
-- 100x performance improvement for RLS policies
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_profiles_id ON profiles(id);
```

**Subquery Optimization for JWT Functions:**
```sql
-- BAD: JWT parsed for every row
CREATE POLICY "slow" ON posts FOR SELECT
  USING (user_id = auth.uid());

-- GOOD: JWT parsed once via subquery
CREATE POLICY "fast" ON posts FOR SELECT
  USING (user_id = (SELECT auth.uid()));
```

### 2. Migration Best Practices

**File Naming Convention:**
```
supabase/migrations/
├── 001_initial_schema.sql
├── 002_add_profiles_trigger.sql
├── 003_forum_tables.sql
└── 004_add_rls_policies.sql
```

**Migration Template:**
```sql
-- Migration: 005_feature_name
-- Description: What this migration does
-- Author: name
-- Date: YYYY-MM-DD

-- Up migration
BEGIN;

-- Your DDL here
CREATE TABLE ...;
ALTER TABLE ...;
CREATE POLICY ...;

COMMIT;

-- Down migration (as comment for reference)
-- DROP TABLE ...;
-- DROP POLICY ...;
```

**Safe Migration Patterns:**
```sql
-- Add column with default (no table lock)
ALTER TABLE users ADD COLUMN status text DEFAULT 'active';

-- Add NOT NULL constraint safely
ALTER TABLE users ADD COLUMN email text;
UPDATE users SET email = 'unknown@example.com' WHERE email IS NULL;
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- Create index concurrently (no lock)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### 3. Auth Integration

**Auto-create Profile on Signup:**
```sql
-- Function to create profile
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, display_name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'display_name', split_part(NEW.email, '@', 1))
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

**Check Auth Status in Policies:**
```sql
-- Authenticated users only
CREATE POLICY "Authenticated access" ON data
  FOR SELECT USING (auth.role() = 'authenticated');

-- Get current user's ID
SELECT auth.uid();

-- Get current user's JWT claims
SELECT auth.jwt();
```

### 4. Common Schema Patterns

**Timestamps with Defaults:**
```sql
CREATE TABLE posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  content text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_posts_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

**Soft Delete Pattern:**
```sql
ALTER TABLE posts ADD COLUMN deleted_at timestamptz;

CREATE POLICY "Hide deleted" ON posts
  FOR SELECT USING (deleted_at IS NULL);
```

**Full-Text Search:**
```sql
-- Add search vector column
ALTER TABLE posts ADD COLUMN search_vector tsvector;

-- Create GIN index
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Update function
CREATE OR REPLACE FUNCTION posts_search_update()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Search query
SELECT * FROM posts
WHERE search_vector @@ plainto_tsquery('english', 'search terms');
```

### 5. Debugging RLS Issues

**Common Problem: Empty Results, No Error**
```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- List all policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Test as specific role
SET ROLE anon;
SELECT * FROM your_table LIMIT 1;
RESET ROLE;

-- Test with specific user
SET request.jwt.claims TO '{"sub": "user-uuid-here"}';
SELECT * FROM your_table;
```

**Diagnostic Query:**
```sql
-- Check what the current user can see
SELECT
  auth.uid() as current_user,
  auth.role() as current_role,
  (SELECT count(*) FROM your_table) as visible_rows;
```

## Quick Reference

| Task | Command |
|------|---------|
| Enable RLS | `ALTER TABLE t ENABLE ROW LEVEL SECURITY;` |
| Create policy | `CREATE POLICY "name" ON t FOR action USING (condition);` |
| Drop policy | `DROP POLICY "name" ON t;` |
| Check policies | `SELECT * FROM pg_policies WHERE tablename = 't';` |
| Current user | `SELECT auth.uid();` |
| Force RLS for owner | `ALTER TABLE t FORCE ROW LEVEL SECURITY;` |

## References

See `/references/` for detailed guides:
- `rls-patterns.md` - Advanced RLS policy patterns
- `migration-checklist.md` - Pre-deployment checklist
- `performance-tuning.md` - Query and index optimization
- `social-schema.md` - Schema patterns for social features
