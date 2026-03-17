---
name: Database Operations
description: Manage database operations, migrations, RLS policies, and performance optimization
triggers:
  - "database"
  - "supabase"
  - "query database"
  - "run migration"
  - "sql"
---

# Database Operations Skill

Perform database operations using Supabase MCP integration or raw SQL.

## Capabilities

- Execute SQL queries
- Run migrations
- Manage RLS policies
- Schema inspection
- Data seeding
- Performance optimization
- Backup operations

## MCP Integration

Uses: `@supabase/mcp` (if available)

## Critical Patterns

### Always Enable RLS
```sql
-- MANDATORY for all tables
ALTER TABLE <table_name> ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own data"
  ON <table_name> FOR SELECT
  USING (auth.uid() = user_id);
```

### Migration Template
```sql
-- Migration: {sequence}_{description}
-- Date: {timestamp}

BEGIN;

-- Changes
CREATE TABLE IF NOT EXISTS new_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS immediately
ALTER TABLE new_table ENABLE ROW LEVEL SECURITY;

-- Add policies
CREATE POLICY "Users access own rows"
  ON new_table FOR ALL
  USING (auth.uid() = user_id);

COMMIT;
```

## Common Operations

### Schema Inspection
```bash
"Using Supabase MCP, show:
 - All tables in database
 - Schema for {table_name}
 - All RLS policies
 Save: temp/database/schema.md"
```

### Run Migration
```bash
"Using Supabase MCP:
 Read: database/migrations/003_add_analytics.sql
 Execute on database
 Verify: Migration successful
 Update: Migration log"
```

### Performance Check
```bash
"Analyze database performance:
 - Check table sizes
 - Identify slow queries (>100ms)
 - Find missing indexes
 - Suggest optimizations
 Output: temp/database/performance-report.md"
```

## Security Checklist

- [ ] RLS enabled on ALL tables
- [ ] Policies prevent unauthorized access
- [ ] Service role key never exposed to client
- [ ] Input validation on all queries
- [ ] Parameterized queries (no SQL injection)

---

**Remember**: Security first! Always enable RLS and use parameterized queries.
