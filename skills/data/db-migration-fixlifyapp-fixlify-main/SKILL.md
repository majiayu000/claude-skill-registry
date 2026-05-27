---
name: db-migration
description: Database migration and schema management skill for Fixlify. Automatically activates when discussing database changes, schema modifications, RLS policies, indexes, or Supabase migrations. Ensures safe, reversible database changes.
version: 1.0.0
author: Fixlify Team
tags: [database, migration, supabase, postgresql, rls, schema]
---

# Database Migration Skill

You are a senior database architect specializing in PostgreSQL and Supabase migrations for Fixlify.

## Supabase Project Info

- **Project ID**: mqppvcrlvsgrsqelglod
- **Database**: PostgreSQL 15
- **Region**: Default Supabase region

## Migration File Structure

```
supabase/
├── migrations/
│   ├── 20260101000000_initial_schema.sql
│   ├── 20260102000000_add_clients_table.sql
│   └── 20260103000000_add_jobs_rls.sql
├── functions/
└── config.toml
```

## Migration Naming Convention

```
YYYYMMDDHHMMSS_descriptive_name.sql

Examples:
20260110000001_add_client_tags.sql
20260110000002_create_inventory_table.sql
20260110000003_add_job_status_index.sql
```

## Creating Migrations

### CLI Method
```bash
# Create empty migration
supabase migration new add_feature_name

# Generate from local changes
supabase db diff -f migration_name

# Squash migrations (dev only)
supabase migration squash
```

### Migration Template

```sql
-- Migration: YYYYMMDDHHMMSS_description
-- Author: [name]
-- Description: [what this migration does]
--
-- Dependencies: [list any required previous migrations]
-- Rollback: [SQL to undo this migration]

-- ============================================
-- UP MIGRATION
-- ============================================

-- 1. Create tables
CREATE TABLE IF NOT EXISTS table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Create indexes
CREATE INDEX IF NOT EXISTS idx_table_name_org
ON table_name(organization_id);

-- 3. Enable RLS
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS policies
CREATE POLICY "org_isolation_select" ON table_name
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );

CREATE POLICY "org_isolation_insert" ON table_name
  FOR INSERT WITH CHECK (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );

CREATE POLICY "org_isolation_update" ON table_name
  FOR UPDATE USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );

CREATE POLICY "org_isolation_delete" ON table_name
  FOR DELETE USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );

-- 5. Create triggers
CREATE TRIGGER update_table_name_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROLLBACK (keep commented, use if needed)
-- ============================================
-- DROP POLICY IF EXISTS "org_isolation_delete" ON table_name;
-- DROP POLICY IF EXISTS "org_isolation_update" ON table_name;
-- DROP POLICY IF EXISTS "org_isolation_insert" ON table_name;
-- DROP POLICY IF EXISTS "org_isolation_select" ON table_name;
-- DROP TABLE IF EXISTS table_name;
```

## RLS Policy Patterns

### Organization Isolation (Most Common)
```sql
CREATE POLICY "org_isolation" ON table_name
  FOR ALL USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );
```

### Owner Only Access
```sql
CREATE POLICY "owner_only" ON table_name
  FOR ALL USING (
    user_id = auth.uid()
  );
```

### Public Read, Owner Write
```sql
CREATE POLICY "public_read" ON table_name
  FOR SELECT USING (true);

CREATE POLICY "owner_write" ON table_name
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "owner_update" ON table_name
  FOR UPDATE USING (user_id = auth.uid());
```

### Role-Based Access
```sql
CREATE POLICY "admin_full_access" ON table_name
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid()
      AND role IN ('admin', 'owner')
    )
  );

CREATE POLICY "member_read" ON table_name
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );
```

## Common Patterns

### Adding Columns (Safe)
```sql
-- Add nullable column (safe, no lock)
ALTER TABLE table_name
ADD COLUMN IF NOT EXISTS new_column TEXT;

-- Add with default (safe in PG 11+)
ALTER TABLE table_name
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active';
```

### Adding Columns (Requires Migration Strategy)
```sql
-- Adding NOT NULL column to existing table
-- Step 1: Add nullable
ALTER TABLE table_name ADD COLUMN new_col TEXT;

-- Step 2: Backfill data
UPDATE table_name SET new_col = 'default_value' WHERE new_col IS NULL;

-- Step 3: Add constraint
ALTER TABLE table_name ALTER COLUMN new_col SET NOT NULL;
```

### Creating Indexes (Safe)
```sql
-- Concurrent index (doesn't lock table)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_name
ON table_name(column_name);
```

### Enum Types
```sql
-- Create enum
CREATE TYPE job_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');

-- Add value to existing enum
ALTER TYPE job_status ADD VALUE IF NOT EXISTS 'on_hold';
```

## Testing Migrations

### Local Testing
```bash
# Reset local database and run all migrations
supabase db reset

# Check migration status
supabase migration list

# Run specific migration
supabase db push
```

### Validation Queries
```sql
-- Check table exists
SELECT EXISTS (
  SELECT FROM information_schema.tables
  WHERE table_name = 'table_name'
);

-- Check column exists
SELECT EXISTS (
  SELECT FROM information_schema.columns
  WHERE table_name = 'table_name'
  AND column_name = 'column_name'
);

-- Check RLS is enabled
SELECT relname, relrowsecurity
FROM pg_class
WHERE relname = 'table_name';

-- List policies
SELECT * FROM pg_policies WHERE tablename = 'table_name';
```

## Dangerous Operations (Require Extra Care)

### Column Removal
```sql
-- DANGER: Data loss! Always backup first
-- Step 1: Remove from code
-- Step 2: Deploy code changes
-- Step 3: Wait for stable deployment
-- Step 4: Then drop column

ALTER TABLE table_name DROP COLUMN IF EXISTS old_column;
```

### Table Removal
```sql
-- DANGER: Irreversible! Create backup first
-- Check for foreign key dependencies

SELECT
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND ccu.table_name = 'table_to_drop';
```

### Type Changes
```sql
-- Changing column type (may require data migration)
ALTER TABLE table_name
ALTER COLUMN column_name TYPE new_type
USING column_name::new_type;
```

## Performance Considerations

### Index Strategy
```sql
-- Single column (most common)
CREATE INDEX idx_jobs_status ON jobs(status);

-- Composite (query pattern specific)
CREATE INDEX idx_jobs_org_status ON jobs(organization_id, status);

-- Partial (for filtered queries)
CREATE INDEX idx_jobs_active ON jobs(organization_id)
WHERE status = 'active';

-- GIN for arrays/JSONB
CREATE INDEX idx_jobs_tags ON jobs USING GIN(tags);
```

### Query Performance Check
```sql
EXPLAIN ANALYZE
SELECT * FROM jobs
WHERE organization_id = 'uuid' AND status = 'active';
```

## Checklist Before Deploying Migration

- [ ] Migration tested locally with `supabase db reset`
- [ ] RLS policies added for new tables
- [ ] Indexes created for foreign keys and common queries
- [ ] No breaking changes to existing data
- [ ] Rollback SQL documented
- [ ] TypeScript types updated (run `supabase gen types typescript`)
- [ ] Code changes deployed before destructive migrations
