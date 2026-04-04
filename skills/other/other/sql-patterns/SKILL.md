---
name: sql-patterns
description: Provides SQL best practices for query optimization, schema design, migrations, transactions, and indexing. Use when writing database queries, designing schemas, creating migrations, or when user mentions 'SQL', 'database', 'query', 'schema', 'migration', 'index', 'transaction'.
---

# SQL Patterns

Best practices for writing safe, performant, and maintainable SQL. All examples use parameterized queries to prevent SQL injection.

## Security-First Principles

Every query MUST use parameterized inputs. Never concatenate user input into SQL strings.

```sql
-- DANGEROUS: SQL injection vulnerability
SELECT * FROM users WHERE email = '" + email + "';

-- SAFE: Parameterized query
SELECT id, name, email FROM users WHERE email = $1;
```

### Destructive Operation Safety

Never run destructive operations without a WHERE clause and explicit confirmation.

| Operation | Risk Level | Required Safeguards |
|-----------|------------|---------------------|
| `DROP TABLE` | CRITICAL | Backup first, use `IF EXISTS`, require approval |
| `TRUNCATE TABLE` | CRITICAL | Backup first, confirm table name, check foreign keys |
| `DELETE` without `WHERE` | CRITICAL | Always add WHERE clause, run SELECT first to preview |
| `UPDATE` without `WHERE` | CRITICAL | Always add WHERE clause, run SELECT first to preview |
| `ALTER TABLE DROP COLUMN` | HIGH | Backup first, check dependencies, use migration |
| `DROP INDEX` | MEDIUM | Verify query plans won't degrade |

Always preview before modifying:

```sql
-- Step 1: Preview what will be affected
SELECT id, email, status FROM users WHERE status = 'inactive';

-- Step 2: Verify the count
SELECT COUNT(*) FROM users WHERE status = 'inactive';

-- Step 3: Only then modify (parameterized)
DELETE FROM users WHERE status = $1;  -- $1 = 'inactive'
```

## Query Optimization

### Using EXPLAIN

Always analyze query plans before deploying queries that touch large tables.

```sql
-- Basic explain
EXPLAIN SELECT id, name FROM users WHERE email = $1;

-- With execution stats (PostgreSQL)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.name, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > $1;
```

### Reading EXPLAIN Output

| Term | Meaning | Action |
|------|---------|--------|
| Seq Scan | Full table scan | Add an index on filter columns |
| Index Scan | Using an index | Good -- verify it's the right index |
| Index Only Scan | Answered from index alone | Best case for read queries |
| Nested Loop | Row-by-row join | Fine for small result sets, bad for large |
| Hash Join | Hash-based join | Good for medium-large joins |
| Sort | In-memory or disk sort | Add index if used with ORDER BY/DISTINCT |
| Bitmap Heap Scan | Index + table lookup | Normal for multi-condition queries |

### Selective Column Queries

```sql
-- BAD: SELECT * fetches unnecessary data, breaks if schema changes
SELECT * FROM users WHERE status = $1;

-- GOOD: Explicit columns, only what you need
SELECT id, name, email, status FROM users WHERE status = $1;
```

### Pagination

```sql
-- BAD: OFFSET-based pagination degrades with large offsets
SELECT id, name FROM products ORDER BY id LIMIT 20 OFFSET 10000;

-- GOOD: Cursor-based pagination using the last seen ID
SELECT id, name FROM products
WHERE id > $1
ORDER BY id
LIMIT 20;
```

## Indexing Guide

### Index Types

| Type | Use Case | Example |
|------|----------|---------|
| B-tree (default) | Equality, range, sorting, LIKE 'prefix%' | `CREATE INDEX idx_email ON users (email)` |
| Hash | Equality only (rare, B-tree usually better) | `CREATE INDEX idx_code ON codes USING hash (code)` |
| GIN | Full-text search, JSONB, arrays | `CREATE INDEX idx_tags ON posts USING gin (tags)` |
| GiST | Geometric, range types, full-text | `CREATE INDEX idx_location ON places USING gist (coords)` |
| Partial | Subset of rows matching a condition | `CREATE INDEX idx_active ON users (email) WHERE active = true` |

### Composite Indexes

Column order matters. Place equality columns first, then range columns.

```sql
-- Query pattern: WHERE status = $1 AND created_at > $2
-- Index matches the query pattern: equality first, range second
CREATE INDEX idx_status_created ON orders (status, created_at);

-- This index will NOT help the query above efficiently:
CREATE INDEX idx_created_status ON orders (created_at, status);
```

### When to Add Indexes

| Signal | Action |
|--------|--------|
| Seq Scan on large table in EXPLAIN | Add index on filter/join columns |
| Slow ORDER BY | Add index on sort columns |
| Slow JOIN | Add index on foreign key columns |
| Frequent WHERE on same columns | Add composite index |
| Low selectivity column (e.g., boolean) | Partial index instead of full |

### When NOT to Index

- Tables with fewer than ~1,000 rows (seq scan is faster)
- Columns that are rarely queried
- Columns with very low cardinality on large tables (unless partial index)
- Write-heavy tables where index maintenance cost exceeds read benefit

## Schema Design

### Normalization Quick Reference

| Normal Form | Rule | Example Violation |
|-------------|------|-------------------|
| 1NF | Atomic values, no repeating groups | `tags: "a,b,c"` in one column |
| 2NF | No partial dependencies on composite key | Non-key column depends on part of key |
| 3NF | No transitive dependencies | `zip_code` determines `city` in `users` |

### When to Denormalize

Denormalize only when you have measured performance problems and understand the tradeoff.

| Scenario | Denormalization Strategy | Tradeoff |
|----------|------------------------|----------|
| Frequent join of 3+ tables | Materialized view | Stale data, refresh cost |
| Read-heavy reporting | Summary table | Write complexity, eventual consistency |
| Display name with foreign key | Cache column + trigger | Must keep in sync |
| Nested JSON responses | JSONB column | Harder to query, larger rows |

### Foreign Key Design

```sql
-- Always define foreign keys with explicit actions
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index foreign keys (PostgreSQL does NOT auto-index them)
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_orders_product_id ON orders (product_id);
```

| ON DELETE | Behavior | Use When |
|-----------|----------|----------|
| RESTRICT | Block delete if referenced | Parent record must exist (orders -> users) |
| CASCADE | Delete children too | Children are meaningless without parent (comments -> post) |
| SET NULL | Set FK to NULL | Relationship is optional (assigned_to -> users) |
| NO ACTION | Like RESTRICT but deferred | Checking at transaction commit |

## Migration Best Practices

### Reversible Migrations

Every migration should have a rollback strategy.

```sql
-- Migration: up
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Migration: down (rollback)
ALTER TABLE users DROP COLUMN phone;
```

### Zero-Downtime Migration Patterns

Adding a column (safe):

```sql
-- Step 1: Add nullable column (no lock, no rewrite)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill in batches (avoid locking entire table)
UPDATE users SET phone = $1 WHERE id BETWEEN $2 AND $3;

-- Step 3: Add NOT NULL constraint after backfill (if needed)
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

Renaming a column (requires coordination):

```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Step 2: Backfill (batched)
UPDATE users SET full_name = name WHERE id BETWEEN $1 AND $2;

-- Step 3: Application reads from both, writes to both
-- Step 4: Switch application to new column only
-- Step 5: Drop old column in later migration
ALTER TABLE users DROP COLUMN name;
```

### Migration Checklist

- [ ] Migration has a rollback script
- [ ] Large table changes use batched updates
- [ ] No `ALTER TABLE ... ADD COLUMN ... DEFAULT` on large tables (pre-PG 11)
- [ ] Index creation uses `CONCURRENTLY` on production tables
- [ ] Foreign key columns are indexed
- [ ] Migration tested on a copy of production data
- [ ] No data loss on rollback

```sql
-- SAFE: Concurrent index creation (doesn't lock writes)
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- UNSAFE: Locks the table during creation
CREATE INDEX idx_users_email ON users (email);
```

## Transaction Patterns

### Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Use Case |
|-------|-----------|---------------------|--------------|----------|
| READ UNCOMMITTED | Possible | Possible | Possible | Almost never (analytics only) |
| READ COMMITTED | No | Possible | Possible | Default for most apps |
| REPEATABLE READ | No | No | Possible (not in PG) | Financial calculations |
| SERIALIZABLE | No | No | No | Critical consistency (transfers) |

```sql
-- Set isolation level for a transaction
BEGIN ISOLATION LEVEL SERIALIZABLE;

UPDATE accounts SET balance = balance - $1 WHERE id = $2;
UPDATE accounts SET balance = balance + $1 WHERE id = $3;

COMMIT;
```

### Avoiding Deadlocks

Deadlocks occur when two transactions wait for each other's locks.

```sql
-- BAD: Transaction A locks row 1 then 2; Transaction B locks row 2 then 1
-- Transaction A:
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Transaction B (concurrent):
UPDATE accounts SET balance = balance - 50 WHERE id = 2;
UPDATE accounts SET balance = balance + 50 WHERE id = 1;
-- DEADLOCK!

-- GOOD: Always lock rows in consistent order (by ID)
-- Both transactions lock id=1 first, then id=2
BEGIN;
SELECT id FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
UPDATE accounts SET balance = balance - $1 WHERE id = 1;
UPDATE accounts SET balance = balance + $1 WHERE id = 2;
COMMIT;
```

### Advisory Locks

Use for application-level mutual exclusion without table locks.

```sql
-- Acquire an advisory lock (blocks until available)
SELECT pg_advisory_lock($1);

-- Do exclusive work...

-- Release the lock
SELECT pg_advisory_unlock($1);

-- Non-blocking variant (returns true/false)
SELECT pg_try_advisory_lock($1);
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `SELECT *` | Fetches unneeded data, breaks on schema change | List explicit columns |
| N+1 queries | Loop fires one query per row | Use JOIN or batch IN query |
| String concatenation in SQL | SQL injection vulnerability | Use parameterized queries ($1, ?) |
| Missing indexes on foreign keys | Slow JOINs and cascading deletes | Add index on every FK column |
| `DELETE FROM table` (no WHERE) | Deletes ALL rows | Always include WHERE clause |
| `LIKE '%term%'` | Cannot use B-tree index, full scan | Use full-text search (GIN index) |
| Storing CSV in one column | Violates 1NF, impossible to query | Use a junction/join table |
| `ORDER BY RANDOM()` | Scans and sorts entire table | Use `TABLESAMPLE` or app-level random |
| UUID v4 as primary key | Fragmented B-tree inserts | Use UUID v7 (time-ordered) or SERIAL |
| N+1 in application code | `for user in users: query(user.id)` | `WHERE id IN ($1, $2, ...)` |
| `COUNT(*)` for existence check | Counts all rows | `SELECT EXISTS (SELECT 1 FROM ... LIMIT 1)` |

## Parameterized Query Examples

### Node.js (pg)

```javascript
// SAFE: Parameterized query
const result = await pool.query(
  'SELECT id, name, email FROM users WHERE email = $1 AND active = $2',
  [email, true]
);

// SAFE: INSERT with RETURNING
const { rows } = await pool.query(
  'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id',
  [name, email]
);
```

### Python (psycopg2)

```python
# SAFE: Parameterized query
cursor.execute(
    "SELECT id, name, email FROM users WHERE email = %s AND active = %s",
    (email, True)
)

# SAFE: Batch insert
from psycopg2.extras import execute_values
execute_values(
    cursor,
    "INSERT INTO users (name, email) VALUES %s",
    [(name, email) for name, email in user_data]
)
```

### Go (database/sql)

```go
// SAFE: Parameterized query
row := db.QueryRowContext(ctx,
    "SELECT id, name, email FROM users WHERE email = $1",
    email,
)
```

## Quick Reference: Safe Defaults

| Concern | Default Choice |
|---------|---------------|
| Primary key | `SERIAL` or `BIGSERIAL` (UUID v7 if distributed) |
| Timestamps | `TIMESTAMPTZ` (always with timezone) |
| Money/currency | `NUMERIC(19,4)` (never FLOAT) |
| String storage | `VARCHAR(n)` with reasonable limit or `TEXT` |
| Boolean | `BOOLEAN` (not integer flags) |
| Foreign keys | Always define with `ON DELETE` behavior |
| Indexes | B-tree default, GIN for JSONB/arrays/full-text |
| Transactions | READ COMMITTED default, SERIALIZABLE for money |
| Migrations | Always reversible, always batched for large tables |
