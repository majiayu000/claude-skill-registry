---
name: postgres-patterns
description: PostgreSQL patterns for reviewing migrations and writing efficient queries. Use when reviewing Alembic migrations, optimizing queries, or debugging database issues.
---

# PostgreSQL Patterns

## Problem Statement

Alembic generates migrations but doesn't understand PostgreSQL performance implications. This skill covers reviewing migrations for PostgreSQL-specific issues and writing efficient queries.

---

## Pattern: Index Review

### When to Add Indexes

```sql
-- ✅ ADD INDEX: Foreign keys (almost always)
CREATE INDEX ix_assessments_user_id ON assessments (user_id);

-- ✅ ADD INDEX: Frequently filtered columns
CREATE INDEX ix_assessments_status ON assessments (status);

-- ✅ ADD INDEX: Columns in WHERE + ORDER BY together
CREATE INDEX ix_assessments_user_status ON assessments (user_id, status);

-- ✅ ADD INDEX: Columns used in JOIN conditions
CREATE INDEX ix_answers_question_id ON answers (question_id);
```

### When NOT to Add Indexes

```sql
-- ❌ SKIP: Small tables (< 1000 rows)
-- ❌ SKIP: Write-heavy tables with rare reads
-- ❌ SKIP: Low cardinality columns alone (boolean, status with 3 values)
-- ❌ SKIP: Columns rarely used in WHERE/JOIN/ORDER BY
```

### Index Column Order Matters

```sql
-- For query: WHERE user_id = ? AND status = ? ORDER BY created_at
-- ✅ CORRECT: Most selective first, ORDER BY column last
CREATE INDEX ix_assessments_user_status_created 
ON assessments (user_id, status, created_at);

-- ❌ WRONG: Order doesn't match query pattern
CREATE INDEX ix_assessments_created_status_user 
ON assessments (created_at, status, user_id);
```

---

## Pattern: Partial Indexes

**Problem:** Full index on column where you only query subset of values.

```sql
-- Full index (indexes all rows)
CREATE INDEX ix_assessments_status ON assessments (status);

-- ✅ BETTER: Partial index (only active assessments)
CREATE INDEX ix_assessments_active 
ON assessments (user_id, created_at) 
WHERE status = 'active';

-- Use case: "Get user's active assessments sorted by date"
-- The partial index is smaller and faster

-- Common patterns:
-- WHERE deleted_at IS NULL (soft deletes)
-- WHERE status != 'archived'
-- WHERE is_active = true
```

**In Alembic:**
```python
op.execute("""
    CREATE INDEX ix_assessments_active 
    ON assessments (user_id, created_at) 
    WHERE status = 'active'
""")
```

---

## Pattern: JSONB Indexes

```sql
-- GIN index for @> (contains) queries
CREATE INDEX ix_settings_data ON user_settings USING GIN (data);

-- Query: Find users with specific setting
SELECT * FROM user_settings WHERE data @> '{"theme": "dark"}';

-- Expression index for specific JSON path
CREATE INDEX ix_settings_theme ON user_settings ((data->>'theme'));

-- Query: Find by specific key
SELECT * FROM user_settings WHERE data->>'theme' = 'dark';
```

---

## Pattern: Concurrent Index Creation

**Problem:** CREATE INDEX locks the table. On large tables, this blocks writes.

```sql
-- ❌ BLOCKS WRITES during creation
CREATE INDEX ix_events_user_id ON events (user_id);

-- ✅ DOESN'T BLOCK (but slower to create)
CREATE INDEX CONCURRENTLY ix_events_user_id ON events (user_id);
```

**In Alembic:**
```python
# Must disable transaction for CONCURRENTLY
def upgrade():
    op.execute("COMMIT")  # End current transaction
    op.execute(
        "CREATE INDEX CONCURRENTLY ix_events_user_id ON events (user_id)"
    )
```

---

## Pattern: Query Performance Analysis

```sql
-- EXPLAIN ANALYZE shows actual execution
EXPLAIN ANALYZE 
SELECT * FROM assessments 
WHERE user_id = 'abc-123' AND status = 'active';

-- What to look for:
-- ✅ "Index Scan" or "Index Only Scan" - good
-- ❌ "Seq Scan" on large table - needs index
-- ❌ "Sort" with high cost - consider index on ORDER BY column
-- ❌ "Nested Loop" with many rows - might need different join strategy
```

**Key metrics:**
- `cost`: Estimated units (lower is better)
- `rows`: Estimated row count
- `actual time`: Real milliseconds
- `loops`: How many times executed

---

## Pattern: UUID Performance

```sql
-- UUIDs as primary keys have tradeoffs
-- ❌ Random UUIDs (uuid4) cause index fragmentation
-- ✅ Time-ordered UUIDs (uuid7) maintain insertion order

-- If using uuid4, consider:
-- 1. BRIN index for time-ordered queries (if you have created_at)
-- 2. Covering indexes to avoid heap fetches
-- 3. Accept some fragmentation (usually fine under 10M rows)
```

---

## Pattern: Constraint Review

```sql
-- ✅ GOOD: Named constraints (can be dropped/modified)
ALTER TABLE assessments 
ADD CONSTRAINT fk_assessments_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ❌ BAD: Unnamed constraints (auto-generated names are ugly)
ALTER TABLE assessments 
ADD FOREIGN KEY (user_id) REFERENCES users(id);

-- ✅ GOOD: CHECK constraints for data integrity
ALTER TABLE assessments 
ADD CONSTRAINT chk_assessments_rating 
CHECK (rating >= 1.0 AND rating <= 5.5);

-- ✅ GOOD: Unique constraints with meaningful names
ALTER TABLE users 
ADD CONSTRAINT uq_users_email UNIQUE (email);
```

---

## Pattern: Bulk Operations

```sql
-- ❌ SLOW: Row-by-row updates
UPDATE users SET role = 'member' WHERE id = 'id1';
UPDATE users SET role = 'member' WHERE id = 'id2';
-- ... thousands more

-- ✅ FAST: Batch update
UPDATE users SET role = 'member' 
WHERE id IN ('id1', 'id2', 'id3', ...);

-- ✅ FAST: Update with subquery
UPDATE users SET role = 'member'
WHERE id IN (
    SELECT user_id FROM legacy_members WHERE migrated = false
);

-- For very large updates, batch to avoid long locks:
UPDATE users SET role = 'member'
WHERE id IN (
    SELECT id FROM users 
    WHERE role IS NULL 
    LIMIT 10000
);
-- Run in loop until no rows affected
```

---

## Pattern: Table Locking Awareness

**Know what locks what:**

| Operation | Lock Type | Blocks |
|-----------|-----------|--------|
| SELECT | AccessShare | Nothing |
| INSERT/UPDATE/DELETE | RowExclusive | Nothing (row-level) |
| CREATE INDEX | ShareLock | INSERT/UPDATE/DELETE |
| CREATE INDEX CONCURRENTLY | ShareUpdateExclusive | Other schema changes |
| ALTER TABLE (most) | AccessExclusive | Everything |
| DROP TABLE | AccessExclusive | Everything |

**Danger zone:**
```sql
-- ❌ LOCKS ENTIRE TABLE
ALTER TABLE users ADD COLUMN bio TEXT NOT NULL DEFAULT '';

-- ✅ MINIMAL LOCKING (PostgreSQL 11+)
ALTER TABLE users ADD COLUMN bio TEXT;  -- Fast, nullable
-- Then backfill with UPDATE in batches
-- Then: ALTER TABLE users ALTER COLUMN bio SET NOT NULL;
```

---

## Pattern: Connection Management

```sql
-- Check active connections
SELECT 
    datname,
    usename,
    application_name,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE datname = 'your_db';

-- Kill long-running query
SELECT pg_cancel_backend(pid);  -- Graceful
SELECT pg_terminate_backend(pid);  -- Force

-- Check for locks
SELECT 
    l.locktype,
    l.relation::regclass,
    l.mode,
    l.granted,
    a.usename,
    a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;
```

---

## Pattern: Data Type Choices

| Use Case | Type | Notes |
|----------|------|-------|
| Primary key | `UUID` | Use uuid7 for ordering if possible |
| Foreign key | Match parent type | |
| Timestamps | `TIMESTAMPTZ` | Always with timezone |
| Money | `NUMERIC(12,2)` | Never FLOAT |
| JSON data | `JSONB` | Not JSON (JSONB is faster) |
| Short strings | `VARCHAR(n)` | With reasonable limit |
| Long text | `TEXT` | No length limit |
| Boolean | `BOOLEAN` | Not integer |
| Enum-like | `VARCHAR` or native ENUM | VARCHAR is more flexible |

---

## Migration Review Checklist (PostgreSQL-Specific)

- [ ] Large table indexes use CONCURRENTLY
- [ ] Foreign keys have ON DELETE behavior specified
- [ ] Constraints have explicit names
- [ ] Non-nullable columns on existing tables use 3-step process
- [ ] Indexes match actual query patterns
- [ ] Partial indexes considered for filtered queries
- [ ] No unnecessary indexes on small tables
- [ ] JSONB columns have appropriate GIN indexes if queried
- [ ] UUIDs: aware of fragmentation implications
- [ ] TIMESTAMPTZ used for all timestamps (not TIMESTAMP)

---

## Useful Diagnostic Queries

```sql
-- Table sizes
SELECT 
    relname as table,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Index usage
SELECT 
    indexrelname as index,
    idx_scan as times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;  -- Unused indexes at top

-- Slow queries (if pg_stat_statements enabled)
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```
