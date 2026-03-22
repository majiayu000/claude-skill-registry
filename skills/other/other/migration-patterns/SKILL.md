---
name: migration-patterns
description: >
  Guide for database schema migrations with zero-downtime patterns, rollback strategies,
  data migrations, and migration testing. Use when the user writes database migrations,
  asks about schema changes in production, needs zero-downtime migration patterns, or
  plans rollback strategies. Trigger whenever database migration, schema change, or
  ALTER TABLE in production is discussed.
---

# Migration Patterns

Write safe database migrations that can be applied to production with zero downtime,
tested rollback paths, and separated schema and data changes.

## When to Use
- User writes a database migration
- User needs to change schema without downtime
- User asks about safe column additions or removals
- User needs to migrate data between schemas
- User plans rollback strategies for migrations

## Core Patterns

### Zero-Downtime Column Addition

Add columns as nullable or with defaults. Never add a NOT NULL column without a default
to an existing table with data.

```sql
-- Migration: Add new column
-- Step 1: Add nullable column (instant, no lock)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill data (can be done in batches)
UPDATE users SET phone = '' WHERE phone IS NULL;

-- Step 3: Add constraint (in a later migration, after backfill completes)
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
ALTER TABLE users ALTER COLUMN phone SET DEFAULT '';
```

```sql
-- BAD: This locks the table and rewrites all rows on older PostgreSQL versions
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '';

-- GOOD on PostgreSQL 11+: Default is stored in catalog, no rewrite
-- But still verify on your version and table size
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '';
```

### Zero-Downtime Column Removal

Remove columns in three phases across separate deployments to avoid breaking running code.

```
Phase 1 (code change): Stop reading/writing the column in application code
Phase 2 (migration):   DROP the column from the database
```

```sql
-- Migration file: 003_drop_legacy_status.sql

-- Phase 2: Safe to drop after Phase 1 is deployed
ALTER TABLE orders DROP COLUMN IF EXISTS legacy_status;
```

Never drop a column that application code still references. Deploy the code change first,
then drop the column in the next release.

### Zero-Downtime Column Rename

Renaming a column requires a multi-step migration to avoid breaking running code.

```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Step 2: Backfill
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Step 3: Deploy code that writes to BOTH columns
-- Step 4: Deploy code that reads from new column
-- Step 5: Drop old column (next release)
ALTER TABLE users DROP COLUMN name;
```

### Safe Index Creation

Create indexes concurrently to avoid locking the table during builds.

```sql
-- BAD: Locks table for writes during index creation
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- GOOD: Non-blocking index creation
CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);

-- Note: CONCURRENTLY cannot run inside a transaction block
-- Most migration tools support this with a special flag
```

### Data Migration Pattern

Separate schema migrations from data migrations. Schema migrations change structure;
data migrations transform content.

```sql
-- Schema migration: 004_add_user_roles.sql
CREATE TABLE roles (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE user_roles (
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);

-- Data migration: 004a_seed_roles.sql (separate file)
INSERT INTO roles (name) VALUES ('admin'), ('editor'), ('viewer');

-- Backfill from old column (run in batches for large tables)
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.name = u.role_name
ON CONFLICT DO NOTHING;
```

Batch processing for large data migrations:

```sql
-- Batch update to avoid long-running transactions
DO $$
DECLARE
  batch_size INT := 5000;
  rows_updated INT;
BEGIN
  LOOP
    WITH batch AS (
      SELECT id FROM users
      WHERE migrated = false
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    )
    UPDATE users SET
      full_name = first_name || ' ' || last_name,
      migrated = true
    FROM batch
    WHERE users.id = batch.id;

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    COMMIT;
    RAISE NOTICE 'Updated % rows', rows_updated;
  END LOOP;
END $$;
```

### Rollback Strategy

Every migration must have a tested reverse migration.

```python
# Alembic example (Python)
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.create_index('idx_users_phone', 'users', ['phone'])

def downgrade():
    op.drop_index('idx_users_phone', 'users')
    op.drop_column('users', 'phone')
```

```javascript
// Knex example (JavaScript)
exports.up = function(knex) {
  return knex.schema.alterTable('users', (table) => {
    table.string('phone', 20).nullable()
    table.index('phone', 'idx_users_phone')
  })
}

exports.down = function(knex) {
  return knex.schema.alterTable('users', (table) => {
    table.dropIndex('phone', 'idx_users_phone')
    table.dropColumn('phone')
  })
}
```

### Migration Testing Checklist

```bash
# 1. Apply migration to a copy of production data
pg_dump production_db | psql test_db
migrate up

# 2. Verify schema matches expectations
psql test_db -c "\d+ users"

# 3. Run rollback
migrate down

# 4. Verify clean rollback
psql test_db -c "\d+ users"

# 5. Re-apply migration
migrate up

# 6. Run application test suite against migrated schema
npm test
```

## Anti-Patterns

- **No rollback migration**: Every `up` needs a `down`. If you cannot reverse a migration, document the manual recovery procedure.
- **Mixing schema and data migrations**: Schema changes should be in one migration, data backfills in another. This makes rollbacks predictable.
- **Long-running transactions**: A migration that takes 30 minutes locks the table for 30 minutes. Use batched updates and concurrent index creation.
- **Renaming columns directly**: `ALTER TABLE RENAME COLUMN` breaks all running application code instantly. Use the add-copy-drop pattern instead.
- **Not testing migrations on production-sized data**: A migration that runs in 1 second on 1000 rows may take 30 minutes on 10 million rows. Always test with production-scale data.
- **Deploying code and migration simultaneously**: Deploy the migration first, verify it succeeded, then deploy the code that depends on it. Or deploy code that handles both old and new schemas.

## Quick Reference

| Operation | Safe Approach | Avoid |
|---|---|---|
| Add column | Add as nullable or with default | NOT NULL without default |
| Drop column | Remove from code first, then drop | Drop while code references it |
| Rename column | Add new, backfill, drop old | ALTER TABLE RENAME |
| Add index | CREATE INDEX CONCURRENTLY | CREATE INDEX (locks table) |
| Change type | Add new column, backfill, swap | ALTER COLUMN TYPE on large tables |
| Add NOT NULL | Add CHECK constraint first | ALTER SET NOT NULL on large tables |
| Drop table | Remove all references first | DROP TABLE while code uses it |
