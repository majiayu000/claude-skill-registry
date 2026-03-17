---
name: migration
description: Create reversible database migrations with rollback scripts.
  Use when modifying database schemas.
---

# Migration Skill

## Purpose
Create safe, reversible database migrations.

## Migration Template
Use: [templates/migration-template.sql](templates/migration-template.sql)

```sql
-- Migration: [description]
-- Created: [date]
-- Author: [name]

-- ==================== UP ====================
BEGIN;

-- Your migration here
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

COMMIT;

-- ==================== DOWN ====================
BEGIN;

DROP TABLE IF EXISTS users;

COMMIT;
```

## Pre-Migration Checklist
Use: [checklists/pre-migration.md](checklists/pre-migration.md)

- [ ] Down migration works
- [ ] Tested on production-like data
- [ ] Performance impact assessed
- [ ] Backup plan documented
- [ ] Deployment timing considered

## Migration Types

### Safe Migrations
- Add table
- Add nullable column
- Add index (CONCURRENTLY)
- Add foreign key (without validation)

### Risky Migrations
- Drop table (verify no references)
- Drop column (verify no usage)
- Rename column (may break app)
- Change column type (may lose data)

### Dangerous Migrations
- Truncate table
- Drop database
- Remove constraints

## Large Table Migrations
For tables with >1M rows:
1. Create new structure
2. Backfill in batches
3. Add constraints
4. Switch over
5. Clean up old structure

## Rollback Strategy
- Test down migration before running up
- Document manual rollback steps
- Have production backup
- Consider feature flags for code changes
