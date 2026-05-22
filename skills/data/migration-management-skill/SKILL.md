---
document_name: "migration-management.skill.md"
location: ".claude/skills/migration-management.skill.md"
codebook_id: "CB-SKILL-MIGRATE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for database migration management"
skill_metadata:
  category: "development"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Database schema knowledge"
    - "Migration tool familiarity"
category: "skills"
status: "active"
tags:
  - "skill"
  - "database"
  - "migration"
  - "schema"
ai_parser_instructions: |
  This skill defines procedures for migration management.
  Used by Database Engineer agent.
---

# Migration Management Skill

=== PURPOSE ===

Procedures for creating, testing, and deploying database migrations.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(database-engineer) @ref(CB-AGENT-DATABASE-001) | Primary skill for migrations |

=== PROCEDURE: Migration Naming ===

**Format:**
```
{timestamp}_{description}.{extension}

Examples:
20260104120000_create_users_table.sql
20260104120100_add_email_to_users.sql
20260104120200_create_posts_table.sql
```

**Description Guidelines:**
- Start with action: `create_`, `add_`, `remove_`, `rename_`, `alter_`
- Include target: table name or description
- Be specific but concise

**Good Names:**
```
create_users_table
add_email_index_to_users
remove_deprecated_status_column
rename_name_to_full_name_in_users
add_foreign_key_posts_to_users
```

=== PROCEDURE: Migration Structure ===

**Up and Down:**
```sql
-- migrate:up
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- migrate:down
DROP TABLE users;
```

**Prisma Format:**
```prisma
// schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique @db.VarChar(255)
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}
```

=== PROCEDURE: Safe Migration Practices ===

**Safe Operations (Always OK):**
```sql
-- Adding tables
CREATE TABLE new_table (...);

-- Adding nullable columns
ALTER TABLE users ADD COLUMN bio TEXT;

-- Adding columns with defaults
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- Adding indexes (with CONCURRENTLY in Postgres)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

**Dangerous Operations (Require Extra Care):**

| Operation | Risk | Mitigation |
|-----------|------|------------|
| DROP TABLE | Data loss | Backup first, soft-delete period |
| DROP COLUMN | Data loss | Backup first, deprecation period |
| RENAME | App breaks | Deploy app changes first |
| ALTER TYPE | Locks table | Use migration strategy |
| ADD NOT NULL | Fails if NULLs exist | Add default or backfill first |

=== PROCEDURE: Adding NOT NULL Column ===

**Wrong (Fails if table has data):**
```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL;
```

**Correct (Multi-step):**
```sql
-- Step 1: Add nullable column with default
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';

-- Step 2: Backfill existing rows
UPDATE users SET role = 'user' WHERE role IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN role SET NOT NULL;

-- Step 4: Optionally remove default
ALTER TABLE users ALTER COLUMN role DROP DEFAULT;
```

=== PROCEDURE: Renaming Column ===

**Strategy: Expand-Contract Pattern**

```sql
-- Migration 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(100);
UPDATE users SET full_name = name;

-- Deploy: Update app to write to both columns
-- Migration 2: (after app deployed)
-- Make new column NOT NULL if needed

-- Migration 3: (after verification)
ALTER TABLE users DROP COLUMN name;
```

=== PROCEDURE: Large Table Migrations ===

**For tables with millions of rows:**

1. **Add columns without defaults:**
```sql
-- Fast: doesn't rewrite table
ALTER TABLE large_table ADD COLUMN new_col TEXT;
```

2. **Backfill in batches:**
```sql
-- Application code or script
UPDATE large_table
SET new_col = computed_value
WHERE id IN (SELECT id FROM large_table WHERE new_col IS NULL LIMIT 10000);
```

3. **Create indexes concurrently:**
```sql
-- Doesn't lock table
CREATE INDEX CONCURRENTLY idx_large_table_new_col ON large_table(new_col);
```

=== PROCEDURE: Migration Checklist ===

**Before Creating:**
- [ ] Understand current schema state
- [ ] Check if migration is reversible
- [ ] Consider table size and lock implications
- [ ] Review for breaking changes

**Before Applying to Production:**
- [ ] Tested in development environment
- [ ] Tested in staging environment
- [ ] Down migration tested
- [ ] Backup strategy confirmed
- [ ] Rollback plan documented
- [ ] @agent(devops-engineer) notified

**After Applying:**
- [ ] Verify schema state
- [ ] Monitor application logs
- [ ] Check performance metrics
- [ ] Update schema documentation

=== PROCEDURE: Rollback Strategy ===

**Immediate Rollback:**
```bash
# If migration tool supports it
npm run migrate:rollback

# Or manually run down migration
psql -f migrations/20260104_down.sql
```

**Point-in-Time Recovery:**
1. Stop application
2. Restore from backup
3. Apply migrations up to desired point
4. Restart application

**Forward Fix:**
Sometimes faster to fix forward than rollback:
```sql
-- If column rename broke things, add alias view
CREATE VIEW users_compat AS
  SELECT *, full_name AS name FROM users;
```

=== PROCEDURE: Migration Testing ===

**Local Testing:**
```bash
# Reset database
npm run db:reset

# Run all migrations
npm run migrate

# Verify schema
npm run db:schema

# Run down migrations
npm run migrate:rollback -- --all

# Run up again
npm run migrate
```

**CI Pipeline Test:**
```yaml
test-migrations:
  script:
    - docker-compose up -d db
    - npm run migrate
    - npm run db:seed
    - npm run test:integration
    - npm run migrate:rollback -- --all
```

=== PROCEDURE: Coordination ===

**Before breaking changes:**
1. Notify @agent(backend-engineer) of schema changes
2. Coordinate deployment timing with @agent(devops-engineer)
3. Get review from @agent(security-lead) for sensitive data columns
4. Update documentation with @agent(doc-chef)

**Deployment sequence:**
```
1. Deploy backward-compatible migration
2. Deploy application code
3. Deploy cleanup migration (if needed)
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(schema-design) | Schema design context |
| @skill(deployment) | Deployment coordination |
