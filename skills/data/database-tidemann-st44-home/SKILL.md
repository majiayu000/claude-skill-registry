---
name: agent-database
description: PostgreSQL expert for .sql migration files, CREATE TABLE, ALTER TABLE, indexes, constraints, foreign keys, schema changes, docker/postgres/migrations/, init.sql, idempotent SQL, transactions, BEGIN/COMMIT, psql, database testing, schema_migrations
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Database Migration Skill

Expert in PostgreSQL schema management and migrations following project conventions.

## When to Use This Skill

Use this skill when:

- Creating new tables
- Adding or modifying columns
- Creating indexes or constraints
- Any database schema change
- Migration-related tasks

## CRITICAL: Migration-First Workflow (MANDATORY)

**ALL database changes MUST have a migration file.**

**Without a migration, changes will NOT deploy to production.**

### Migration Workflow

1. **Create Migration File**

   ```bash
   # In docker/postgres/migrations/
   # Name: NNN_description.sql (e.g., 003_add_user_roles.sql)
   ```

2. **Write Idempotent Migration**

   ```sql
   BEGIN;

   -- Create table only if it doesn't exist
   CREATE TABLE IF NOT EXISTS users (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     "firstName" TEXT NOT NULL,
     "lastName" TEXT NOT NULL,
     email TEXT UNIQUE NOT NULL,
     "createdAt" TIMESTAMP DEFAULT NOW()
   );

   -- Add column only if it doesn't exist
   DO $$
   BEGIN
     IF NOT EXISTS (
       SELECT 1 FROM information_schema.columns
       WHERE table_name = 'users' AND column_name = 'role'
     ) THEN
       ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user';
     END IF;
   END $$;

   -- Record migration
   INSERT INTO schema_migrations (version, description)
   VALUES ('003', 'Add user roles')
   ON CONFLICT (version) DO NOTHING;

   COMMIT;
   ```

3. **Update init.sql**

   ```bash
   # Add the same schema to docker/postgres/init.sql
   # For fresh database installations
   ```

4. **Test Migration Locally**

   ```bash
   # Apply migration to test database
   docker exec -i st44-db-test psql -U postgres -d st44_test < docker/postgres/migrations/003_add_user_roles.sql

   # Verify it worked
   docker exec -it st44-db-test psql -U postgres -d st44_test -c "\d users"
   ```

5. **Test Idempotency**
   ```bash
   # Run migration again - should not error
   docker exec -i st44-db-test psql -U postgres -d st44_test < docker/postgres/migrations/003_add_user_roles.sql
   ```

## CRITICAL: camelCase Column Names

**ALL columns MUST use camelCase with double quotes.**

### ✅ CORRECT

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  "firstName" TEXT NOT NULL,
  "lastName" TEXT NOT NULL,
  "createdAt" TIMESTAMP DEFAULT NOW()
);
```

### ❌ FORBIDDEN

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  first_name TEXT NOT NULL,  -- NO snake_case!
  last_name TEXT NOT NULL,   -- NO snake_case!
);
```

**Why:** Consistency across entire stack (TypeScript, API, database).

## Migration File Requirements

### File Naming

```
docker/postgres/migrations/
├── 001_initial_schema.sql
├── 002_add_households.sql
├── 003_add_user_roles.sql
└── 004_add_tasks_table.sql
```

- **Format:** `NNN_description.sql`
- **Number:** Sequential (001, 002, 003...)
- **Description:** Lowercase with underscores

### File Structure

```sql
BEGIN;

-- Your schema changes here
-- Use IF NOT EXISTS for idempotency

-- Always record the migration
INSERT INTO schema_migrations (version, description)
VALUES ('NNN', 'Description of changes')
ON CONFLICT (version) DO NOTHING;

COMMIT;
```

## Idempotency Patterns

### Creating Tables

```sql
CREATE TABLE IF NOT EXISTS table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "columnName" TEXT NOT NULL
);
```

### Adding Columns

```sql
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'users' AND column_name = 'role'
  ) THEN
    ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user';
  END IF;
END $$;
```

### Creating Indexes

```sql
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

### Adding Constraints

```sql
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'users_email_unique'
  ) THEN
    ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);
  END IF;
END $$;
```

## Testing Checklist

Before marking migration complete:

- [ ] Migration file created in `docker/postgres/migrations/NNN_description.sql`
- [ ] init.sql updated with same schema
- [ ] Migration uses BEGIN/COMMIT transaction
- [ ] All operations are idempotent (IF NOT EXISTS)
- [ ] camelCase column names with double quotes
- [ ] schema_migrations table updated
- [ ] Tested on local database
- [ ] Tested idempotency (ran twice without errors)
- [ ] Verified with `\d table_name` in psql

## Common Database Operations

### UUID Primary Keys

```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);
```

### Timestamps

```sql
"createdAt" TIMESTAMP DEFAULT NOW(),
"updatedAt" TIMESTAMP DEFAULT NOW()
```

### Foreign Keys

```sql
"userId" UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
```

### Enums (Use TEXT with CHECK)

```sql
role TEXT CHECK (role IN ('admin', 'parent', 'child'))
```

## Testing Migrations

### Start Test Database

```bash
npm run db:test:up
```

### Apply Migration

```bash
docker exec -i st44-db-test psql -U postgres -d st44_test < docker/postgres/migrations/003_add_user_roles.sql
```

### Verify Schema

```bash
docker exec -it st44-db-test psql -U postgres -d st44_test -c "\d users"
```

### Test Idempotency

```bash
# Run same migration again - should not error
docker exec -i st44-db-test psql -U postgres -d st44_test < docker/postgres/migrations/003_add_user_roles.sql
```

### Stop Test Database

```bash
npm run db:test:down
```

## Workflow

1. **Read** the optimized agent spec: `.claude/agents/agent-database.md`
2. **Understand** what schema changes are needed
3. **Create** migration file with next sequential number
4. **Write** idempotent SQL with camelCase columns
5. **Update** init.sql with same schema
6. **Test** locally on test database
7. **Verify** idempotency (run twice)
8. **Only then** commit and push

## Reference Files

For detailed patterns and examples:

- `.claude/agents/agent-database.md` - Complete agent specification
- `docker/postgres/init.sql` - Current database schema
- `docker/postgres/migrations/` - Existing migration examples
- `CLAUDE.md` - Project-wide conventions

## Deployment Guarantee

**If you create a migration file and it passes testing:**
✅ It WILL deploy to production
✅ It WILL run automatically
✅ Schema changes are guaranteed

**If you DON'T create a migration file:**
❌ Changes will NOT deploy
❌ Production will be out of sync
❌ Backend will fail with schema errors

**This is why migration-first is mandatory.**

## Success Criteria

Before marking work complete:

- [ ] Migration file exists and is numbered correctly
- [ ] init.sql updated
- [ ] All columns use camelCase
- [ ] Migration is idempotent
- [ ] Tested locally and verified
- [ ] Idempotency tested (ran twice)
- [ ] No errors when applying migration
