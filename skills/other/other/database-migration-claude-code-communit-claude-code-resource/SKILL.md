---
name: database-migration
description: Database migration best practices — schema changes, zero-downtime migrations, rollback strategies, and data migration patterns. Reference when modifying database schemas.
---

# Database Migration

## Migration File Conventions

Every schema change must be captured in a versioned migration file. Follow these conventions:

- **Timestamped naming**: Use `YYYYMMDDHHMMSS_descriptive_name` (e.g., `20240315143022_add_status_to_orders.sql`).
- **Sequential ordering**: Migrations run in order. Never insert a migration before one that has already been applied.
- **One concern per file**: Each migration handles a single logical change. Do not combine unrelated schema changes.
- **Descriptive names**: The filename should describe the change, not the ticket number. Use verbs like `add`, `remove`, `create`, `drop`, `rename`, `alter`.
- **Idempotent when possible**: Use `IF NOT EXISTS` / `IF EXISTS` guards to make re-runs safe.

```
migrations/
  20240301100000_create_users_table.sql
  20240305120000_add_email_index_to_users.sql
  20240310090000_create_orders_table.sql
  20240315143022_add_status_to_orders.sql
```

## Forward and Rollback Pairs

Every migration must have a corresponding rollback. If you cannot write a safe rollback, document why and flag it for review.

```sql
-- Migration: 20240315143022_add_status_to_orders.sql

-- UP
ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'pending';
CREATE INDEX idx_orders_status ON orders (status);

-- DOWN
DROP INDEX IF EXISTS idx_orders_status;
ALTER TABLE orders DROP COLUMN IF EXISTS status;
```

### Rollback Rules

| Scenario | Rollback Strategy |
|----------|-------------------|
| Add column | Drop column |
| Add index | Drop index |
| Create table | Drop table |
| Add constraint | Drop constraint |
| Rename column | Rename back |
| Drop column | Cannot auto-rollback — must restore from backup or use prior migration to re-add |
| Data backfill | Reverse backfill or accept data state |

## Zero-Downtime Schema Changes

When your application cannot tolerate downtime during deploys, follow the expand-and-contract pattern. Never make breaking schema changes in a single step.

### Step-by-Step: Renaming a Column

Renaming a column directly (`ALTER TABLE ... RENAME COLUMN`) breaks running application instances that reference the old name. Instead:

1. **Deploy 1 — Expand**: Add the new column alongside the old one.
   ```sql
   ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
   ```

2. **Deploy 2 — Dual Write**: Update application code to write to both columns.
   ```javascript
   // Write to both columns
   await db.query(
     'UPDATE users SET name = $1, full_name = $1 WHERE id = $2',
     [name, userId]
   );
   ```

3. **Deploy 3 — Backfill**: Copy existing data from old column to new column.
   ```sql
   UPDATE users SET full_name = name WHERE full_name IS NULL;
   ```

4. **Deploy 4 — Cut Over**: Update application to read from and write to new column only.
   ```javascript
   // Read from new column
   const user = await db.query('SELECT full_name FROM users WHERE id = $1', [userId]);
   ```

5. **Deploy 5 — Contract**: Drop the old column after a safe observation period.
   ```sql
   ALTER TABLE users DROP COLUMN name;
   ```

### Step-by-Step: Adding a NOT NULL Constraint

Adding a `NOT NULL` constraint on an existing column with null values will fail or lock the table. Safe approach:

1. Add a check constraint as `NOT VALID` (PostgreSQL) to avoid scanning existing rows:
   ```sql
   ALTER TABLE orders ADD CONSTRAINT orders_status_not_null
     CHECK (status IS NOT NULL) NOT VALID;
   ```

2. Backfill any null values:
   ```sql
   UPDATE orders SET status = 'unknown' WHERE status IS NULL;
   ```

3. Validate the constraint (acquires lighter lock):
   ```sql
   ALTER TABLE orders VALIDATE CONSTRAINT orders_status_not_null;
   ```

4. Optionally convert to a proper `NOT NULL` column constraint:
   ```sql
   ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
   ALTER TABLE orders DROP CONSTRAINT orders_status_not_null;
   ```

## Dangerous Operations

| Operation | Risk | Safe Alternative |
|-----------|------|-----------------|
| `RENAME COLUMN` | Breaks queries referencing old name | Expand-and-contract pattern (add new, migrate, drop old) |
| `CHANGE COLUMN TYPE` | May require full table rewrite, long lock | Add new column with new type, backfill, swap |
| `DROP COLUMN` | Irreversible data loss | Verify no code references, back up data, then drop |
| `DROP TABLE` | Irreversible data and schema loss | Rename to `_deprecated_` first, drop after observation period |
| `ADD NOT NULL` (to existing column) | Fails if nulls exist; full table scan | Add as nullable, backfill, then add constraint |
| `ADD COLUMN WITH DEFAULT` (pre-PG11) | Full table rewrite on older PostgreSQL | Add nullable column, set default, backfill |
| `CREATE INDEX` | Blocks writes on table (non-concurrent) | Use `CREATE INDEX CONCURRENTLY` (PostgreSQL) |
| `ADD FOREIGN KEY` | Validates all existing rows, long lock | Add as `NOT VALID`, then `VALIDATE` separately |
| `ALTER TABLE ... LOCK` | Exclusive lock blocks all access | Minimize lock duration, run during low traffic |

## Data Migration Strategies

### Backfill Scripts

For populating new columns with computed or default data:

```javascript
// Batch backfill to avoid locking and memory issues
async function backfillStatus(db, batchSize = 1000) {
  let totalUpdated = 0;
  let updated;

  do {
    const result = await db.query(`
      UPDATE orders
      SET status = 'pending'
      WHERE id IN (
        SELECT id FROM orders
        WHERE status IS NULL
        LIMIT $1
        FOR UPDATE SKIP LOCKED
      )
      RETURNING id
    `, [batchSize]);

    updated = result.rowCount;
    totalUpdated += updated;
    console.log(`Backfilled ${totalUpdated} rows...`);

    // Pause between batches to reduce load
    await new Promise(resolve => setTimeout(resolve, 100));
  } while (updated === batchSize);

  console.log(`Backfill complete. Total rows updated: ${totalUpdated}`);
}
```

### Dual-Write Pattern

When migrating data to a new structure or new system:

1. Start writing to both old and new locations.
2. Backfill historical data from old to new.
3. Verify consistency between old and new.
4. Switch reads to new location.
5. Stop writing to old location.
6. Decommission old structure after observation period.

### Shadow Tables

For large structural changes where you cannot modify the original table in place:

```sql
-- 1. Create the new table with desired schema
CREATE TABLE users_v2 (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Copy data in batches
INSERT INTO users_v2 (full_name, email, created_at)
SELECT
  COALESCE(first_name || ' ' || last_name, first_name, 'Unknown'),
  email,
  created_at
FROM users
WHERE id BETWEEN 1 AND 10000;
-- Repeat for remaining batches

-- 3. Set up triggers or dual-write for new data during migration

-- 4. Swap tables atomically
ALTER TABLE users RENAME TO users_deprecated;
ALTER TABLE users_v2 RENAME TO users;

-- 5. Drop old table after observation period
-- DROP TABLE users_deprecated;
```

## Migration Testing

### Pre-Deployment Testing Checklist

- [ ] Migration runs successfully on a fresh database.
- [ ] Migration runs successfully on a copy of production data.
- [ ] Rollback runs successfully and leaves database in prior state.
- [ ] Migration completes within acceptable time on production-sized data.
- [ ] No exclusive locks held for more than a few seconds.
- [ ] Application code is compatible with both before and after schema states (for zero-downtime deploys).
- [ ] Data integrity is preserved (row counts, checksums on critical columns).

### Testing Against Production-Like Data

Always test migrations against a database with realistic data volume:

```bash
# Restore a production backup to a test environment
pg_restore --dbname=test_db production_backup.dump

# Run the migration
psql -d test_db -f migrations/20240315143022_add_status_to_orders.sql

# Verify results
psql -d test_db -c "SELECT COUNT(*) FROM orders WHERE status IS NULL;"

# Time the migration
time psql -d test_db -f migrations/20240315143022_add_status_to_orders.sql
```

## Database Seeding for Development

Maintain seed files that populate development databases with realistic test data:

```javascript
// seeds/001_users.js
exports.seed = async function(knex) {
  await knex('users').del();
  await knex('users').insert([
    { id: 1, name: 'Alice Developer', email: 'alice@example.com', role: 'admin' },
    { id: 2, name: 'Bob Tester', email: 'bob@example.com', role: 'user' },
    { id: 3, name: 'Carol Manager', email: 'carol@example.com', role: 'manager' },
  ]);
};

// seeds/002_orders.js
exports.seed = async function(knex) {
  await knex('orders').del();
  await knex('orders').insert([
    { id: 1, user_id: 1, status: 'completed', total: 99.99 },
    { id: 2, user_id: 2, status: 'pending', total: 49.50 },
    { id: 3, user_id: 1, status: 'shipped', total: 150.00 },
  ]);
};
```

### Seed Data Principles

- Seeds are idempotent: running them twice produces the same state.
- Seeds use fixed IDs for referential integrity.
- Seeds cover all enum values and edge cases.
- Seeds never contain real user data or secrets.

## ORM Migration Tools Comparison

| Tool | Language | Migration Format | Rollback | Auto-Generate | Key Feature |
|------|----------|-----------------|----------|---------------|-------------|
| Prisma Migrate | JS/TS | SQL files from schema diff | Limited (reset-based) | Yes, from `schema.prisma` | Declarative schema, drift detection |
| Knex.js | JS/TS | JavaScript files | Manual `down()` function | No (manual) | Flexible, raw SQL support |
| Alembic | Python | Python files | Manual `downgrade()` | Yes, from SQLAlchemy models | Branching support, auto-detect |
| ActiveRecord | Ruby | Ruby DSL files | Automatic `change` reversible | No (manual) | Reversible DSL methods |
| Diesel | Rust | SQL files | Manual `down.sql` | Yes, from schema diff | Compile-time schema verification |
| Flyway | Java/JVM | SQL or Java files | Paid feature (undo) | No (manual) | Convention-based, polyglot |
| golang-migrate | Go | SQL files | Manual `down.sql` | No (manual) | CLI-first, driver-agnostic |

## Locking Considerations

Database schema changes acquire locks that can block application queries. Understand the lock implications:

### PostgreSQL Lock Levels

| DDL Operation | Lock Acquired | Blocks Reads | Blocks Writes | Duration |
|---------------|--------------|-------------|---------------|----------|
| `CREATE INDEX` | `ShareLock` | No | Yes | Duration of index build |
| `CREATE INDEX CONCURRENTLY` | `ShareUpdateExclusiveLock` | No | No | Longer build, but non-blocking |
| `ADD COLUMN` (nullable, no default) | `AccessExclusiveLock` | Yes | Yes | Near-instant (metadata only) |
| `ADD COLUMN` (with default, PG11+) | `AccessExclusiveLock` | Yes | Yes | Near-instant (virtual default) |
| `DROP COLUMN` | `AccessExclusiveLock` | Yes | Yes | Near-instant (marks as dropped) |
| `ALTER COLUMN TYPE` | `AccessExclusiveLock` | Yes | Yes | Full table rewrite |
| `ADD CONSTRAINT` | `AccessExclusiveLock` | Yes | Yes | Full table scan to validate |
| `ADD CONSTRAINT ... NOT VALID` | `ShareRowExclusiveLock` | No | Partially | Near-instant |
| `VALIDATE CONSTRAINT` | `ShareUpdateExclusiveLock` | No | No | Scans table, non-blocking |

### Mitigating Lock Contention

```sql
-- Set a lock timeout to fail fast instead of waiting indefinitely
SET lock_timeout = '5s';

-- Retry the operation if it times out
-- Application code should handle this and retry with backoff

-- Kill long-running queries that block migrations
SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < NOW() - INTERVAL '5 minutes'
  AND query NOT LIKE '%pg_stat_activity%';
```

## Migration Deployment Checklist

Run through this checklist before applying any migration to production:

### Planning

- [ ] Migration has been reviewed by another engineer.
- [ ] Forward migration and rollback have been written and tested.
- [ ] Migration has been tested against a production-sized dataset.
- [ ] Estimated execution time is known and acceptable.
- [ ] Lock impact has been analyzed (see locking table above).
- [ ] Application code is compatible with schema before and after migration.

### Execution

- [ ] Database backup taken immediately before migration.
- [ ] Migration applied during low-traffic period (if it requires locks).
- [ ] Migration output monitored for errors.
- [ ] Application health verified after migration completes.
- [ ] Row counts and data integrity spot-checked.

### Post-Migration

- [ ] Old schema artifacts cleaned up (after observation period).
- [ ] Rollback script archived but accessible.
- [ ] Monitoring confirms no query performance regressions.
- [ ] Migration documented in changelog or release notes.
