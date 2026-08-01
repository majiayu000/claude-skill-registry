---
name: supabase-skill
description: ALWAYS consolidate all database changes in project/supabase/migrations/00000000000000schema.sql
---

# Supabase Skill for Agritech Project

## Core Principle

**ALWAYS consolidate all database changes in `project/supabase/migrations/00000000000000_schema.sql`**

This is a single-file migration approach where all schema changes (tables, functions, triggers, RLS policies, etc.) are maintained in one comprehensive migration file.

## Project Structure

```
project/
├── supabase/
│   └── migrations/
│       └── 00000000000000_schema.sql  # Single consolidated schema file
└── src/
    └── ... (React frontend)
```

## Migration Strategy

### Single File Approach
- All database schema changes go into `00000000000000_schema.sql`
- This file contains the complete, idempotent database schema
- All CREATE statements use `IF NOT EXISTS`, `OR REPLACE`, or `DO $$ BEGIN ... EXCEPTION ... END $$` patterns
- The file is self-contained and can be run multiple times safely

### Idempotency Requirements
- **Tables**: Use `CREATE TABLE IF NOT EXISTS`
- **Functions**: Use `CREATE OR REPLACE FUNCTION`
- **Types/ENUMs**: Use `DO $$ BEGIN ... EXCEPTION WHEN duplicate_object THEN null; END $$`
- **Indexes**: Use `CREATE INDEX IF NOT EXISTS`
- **Triggers**: Use `DROP TRIGGER IF EXISTS` before `CREATE TRIGGER`
- **Policies**: Use `DROP POLICY IF EXISTS` before `CREATE POLICY`

## Schema Organization

The schema file is organized into sections:

1. **Extensions** - PostGIS, UUID generation
2. **Helper Functions** - Utility functions like `update_updated_at_column()`
3. **ENUM Types** - All custom types (quote_status, invoice_status, etc.)
4. **Core Tables** - Organizations, users, profiles
5. **Farm Management** - Farms, parcels
6. **Billing Cycle** - Quotes, sales orders, purchase orders
7. **Accounting** - Accounts, journal entries, invoices, payments
8. **Workers & Tasks** - Workers, tasks, work units
9. **Harvest & Delivery** - Harvest records, deliveries
10. **Inventory & Stock** - Items, warehouses, stock entries
11. **Satellite Data** - Satellite indices, processing jobs
12. **Analyses & Reports** - Soil analyses, reports
13. **RLS Policies** - Row Level Security policies
14. **Triggers** - Database triggers
15. **Data Seeding** - Initial data setup

## RLS (Row Level Security) Patterns

### Helper Function
All RLS policies use the `is_organization_member()` helper function:

```sql
CREATE OR REPLACE FUNCTION is_organization_member(p_organization_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
STABLE
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.organization_users
    WHERE user_id = auth.uid()
      AND organization_id = p_organization_id
      AND is_active = true
  );
$$;
```

### Policy Naming Convention
- Read: `org_read_{table_name}`
- Write/Insert: `org_write_{table_name}`
- Update: `org_update_{table_name}`
- Delete: `org_delete_{table_name}`
- All operations: `org_access_{table_name}` (for child tables)

### Policy Pattern
```sql
DROP POLICY IF EXISTS "org_read_{table}" ON {table};
CREATE POLICY "org_read_{table}" ON {table}
  FOR SELECT USING (
    is_organization_member(organization_id)
  );
```

## Common Patterns

### Organization-Scoped Tables
All main tables include `organization_id` and RLS policies:
```sql
CREATE TABLE IF NOT EXISTS {table_name} (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  -- other columns
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Updated_at Triggers
For tables with `updated_at` columns:
```sql
DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};
CREATE TRIGGER trg_{table}_updated_at
  BEFORE UPDATE ON {table}
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Number Generation Functions
Use helper functions for generating sequential numbers:
- `generate_quote_number(p_organization_id UUID)`
- `generate_sales_order_number(p_organization_id UUID)`
- `generate_invoice_number(p_organization_id UUID, p_invoice_type invoice_type)`

## When Making Changes

### Adding a New Table
1. Add table definition in appropriate section
2. Add indexes
3. Enable RLS: `ALTER TABLE IF EXISTS {table} ENABLE ROW LEVEL SECURITY;`
4. Add RLS policies (read, write, update, delete)
5. Add `updated_at` trigger if needed
6. Add to appropriate section comment

### Modifying Existing Table
1. Use `ALTER TABLE IF EXISTS` for schema changes
2. Ensure idempotency (check if column/index exists first)
3. Update related RLS policies if needed
4. Update triggers if needed

### Adding Functions
1. Use `CREATE OR REPLACE FUNCTION`
2. Add `SECURITY DEFINER` if it needs to bypass RLS
3. Set `SET search_path = public` for security
4. Add `GRANT EXECUTE` statements
5. Add comments with `COMMENT ON FUNCTION`

### Adding RLS Policies
1. Always `DROP POLICY IF EXISTS` first
2. Use consistent naming: `org_{operation}_{table}`
3. Use `is_organization_member()` for organization-scoped tables
4. For child tables, check parent table membership

## Data Seeding

Initial data setup is done in the same file:
- Default currencies
- Default roles
- User profile synchronization
- Organization setup
- Subscription setup

Use `DO $$ ... END $$` blocks for conditional seeding.

## Testing Changes

Before committing:
1. Verify idempotency - run migration twice, should succeed both times
2. Check RLS policies - ensure users can only access their organization's data
3. Verify foreign keys - ensure all references are valid
4. Test triggers - ensure they fire correctly

## Important Notes

- **Never create separate migration files** - always update `00000000000000_schema.sql`
- **Always use idempotent statements** - migrations should be safe to run multiple times
- **RLS is enabled on all tables** - ensure policies are created for every table
- **Use SECURITY DEFINER carefully** - only for functions that need to bypass RLS
- **Maintain section organization** - keep related items together
- **Add comments** - document complex logic and important decisions

## Common Commands

### Apply Migration
```bash
cd project
npm run db:migrate
```

### Generate TypeScript Types
```bash
npm run db:generate-types
```

### Reset Database (Local)
```bash
npm run db:reset
```

## File Location

All schema changes must be made in:
```
project/supabase/migrations/00000000000000_schema.sql
```

**Remember: This is the single source of truth for the database schema.**
