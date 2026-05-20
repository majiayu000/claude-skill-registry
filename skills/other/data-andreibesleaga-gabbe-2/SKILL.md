---
name: db-migration
description: Database schema changes and migration workflow — safe, reversible, tested
triggers: [migration, schema, database, alter table, add column, rename column, DB change]
context_cost: medium
---

# DB Migration Skill

## Goal
Implement database schema changes safely using migration-first development. All migrations must be reversible and tested before applying to production.

## Steps

1. **Inspect current schema**
   - Read current migration files to understand existing schema
   - Check: any foreign key constraints that would be affected?
   - Check: any indexes on columns being modified?
   - Check: any application code relying on the current schema shape?

2. **Design the schema change**
   - Minimal change to achieve the goal
   - Consider backward compatibility:
     - Adding nullable column: backward compatible ✓
     - Adding NOT NULL column without default: breaking ✗
     - Renaming column: breaking ✗ (use add → populate → rename → drop strategy)
     - Changing column type: potentially breaking — check data conversion

3. **Write the migration** (forward + rollback)

   **Prisma (Node.js):**
   ```bash
   npx prisma migrate dev --name add_email_verified_to_users
   # Edit: prisma/migrations/[timestamp]_add_email_verified_to_users/migration.sql
   ```

   **Laravel:**
   ```bash
   php artisan make:migration add_email_verified_to_users_table
   # Edit: database/migrations/[timestamp]_add_email_verified_to_users_table.php
   ```

   **Alembic (Python):**
   ```bash
   uv run alembic revision --autogenerate -m "Add email_verified_to_users"
   # Edit: migrations/versions/[hash]_add_email_verified_to_users.py
   ```

   **Raw SQL migration file:**
   ```sql
   -- UP migration
   ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMP NULL;
   CREATE INDEX idx_users_email_verified ON users(email_verified_at);

   -- DOWN migration (rollback)
   DROP INDEX IF EXISTS idx_users_email_verified;
   ALTER TABLE users DROP COLUMN IF EXISTS email_verified_at;
   ```

4. **Safe rename/drop strategy** (never rename or drop directly)
   ```
   Phase 1: Add new column (backward compatible)
   Phase 2: Populate new column in application code (dual-write)
   Phase 3: Deploy application using new column
   Phase 4: Remove old column (now safe — no code uses it)

   This allows zero-downtime deployments.
   ```

5. **Test the migration**
   ```bash
   # Apply migration to test database
   [migration command] --environment test

   # Verify schema is correct
   # Check that all application tests pass with new schema
   [test command]

   # Test rollback
   [rollback migration command]

   # Re-apply migration
   [migration command] --environment test
   ```

6. **Check for performance implications**
   - Is the new column indexed if it will be used in WHERE clauses?
   - Does the migration lock the table? (ALTER TABLE on large tables can block)
   - For large tables: consider pt-online-schema-change or gh-ost for zero-lock migrations

7. **Update application code**
   - Update ORM models/entities to reflect new schema
   - Update TypeScript types / PHP DTOs
   - Update any seed data or fixture files
   - Update API response schemas if schema change is exposed via API

8. **Document the migration**
   - Update `docs/database-schema.md` (if it exists)
   - If the migration has unusual behavior: add comment in migration file explaining why

## Safety Checklist

```
Before applying to staging/production:
[ ] Migration tested on copy of production data (or realistic dataset)
[ ] Rollback tested and verified working
[ ] All application tests passing with new schema
[ ] Lock duration estimated for large tables
[ ] Backup confirmed before migration
[ ] Monitoring in place to detect errors after migration
```

## Constraints
- NEVER drop a column or table without first verifying no application code uses it
- NEVER make a NOT NULL column without a DEFAULT or populating existing rows first
- ALWAYS write a rollback (DOWN) migration
- Production migrations require human approval

## Output Format
Migration file + updated model/entity + test confirmation. Report: "Migration [name] created. Forward + rollback tested. All [N] tests passing."
