---
name: sql-guide
description: |
  SQL language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with SQL files (.sql), database migrations, or when the user mentions SQL/databases.
  Provides query optimization patterns, indexing guidelines, transaction management,
  and migration standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: sql
  extensions: ".sql"
---

# SQL Guide

> Applies to: PostgreSQL 15+, MySQL 8+, Database Migrations, Query Optimization

## Core Principles

1. **Parameterized Queries Always**: Never concatenate user input into SQL strings -- use bind parameters (`$1`, `?`, `:name`) without exception
2. **Explicit Over Implicit**: Name all constraints, specify column lists in INSERT, avoid `SELECT *` in production code
3. **Migrations Are Immutable**: Once applied to a shared environment, never modify a migration -- create a new one
4. **Indexes Are Not Free**: Every index speeds reads but slows writes; justify each index with a query plan
5. **Transactions Are Boundaries**: Keep transactions short, choose the correct isolation level, and always handle rollback

## Guardrails

### Naming Conventions

- Tables: `snake_case`, **plural** (`users`, `order_items`, `audit_logs`)
- Columns: `snake_case`, **singular** (`email`, `created_at`, `is_active`)
- Primary keys: `id` (integer or UUID depending on project convention)
- Foreign keys: `<singular_table>_id` (`user_id`, `order_id`)
- Indexes: `idx_<table>_<columns>` (`idx_users_email`, `idx_orders_user_id_created_at`)
- Unique constraints: `uq_<table>_<columns>` (`uq_users_email`)
- Check constraints: `ck_<table>_<description>` (`ck_orders_positive_total`)
- Boolean columns: `is_` or `has_` prefix (`is_active`, `has_verified_email`)
- Timestamps: `created_at`, `updated_at`, `deleted_at` (always `TIMESTAMPTZ`)

### Query Safety

- ALWAYS use parameterized queries -- no string interpolation of user input
- ALWAYS specify column lists in `INSERT` statements
- NEVER use `SELECT *` in application code (acceptable in ad-hoc queries only)
- ALWAYS add `LIMIT` to queries that return lists (prevent unbounded result sets)
- NEVER use `TRUNCATE` or `DROP` in application code without explicit safeguards
- ALWAYS use `EXISTS` instead of `COUNT(*) > 0` for existence checks
- ALWAYS qualify column names with table aliases in JOINs

```sql
-- GOOD: parameterized, explicit columns, bounded
SELECT u.id, u.email, u.created_at
FROM users u
WHERE u.email = $1
  AND u.is_active = true
LIMIT 1;

-- BAD: string concatenation, SELECT *, no LIMIT
SELECT * FROM users WHERE email = '" + userInput + "';
```

### Indexing

- Create indexes to support `WHERE`, `JOIN`, and `ORDER BY` clauses
- Composite index column order: equality columns first, then range, then sort
- Use `UNIQUE` indexes to enforce business rules at the database level
- Prefer partial indexes when filtering on a known subset (`WHERE is_active = true`)
- Use `CONCURRENTLY` for index creation on live tables (PostgreSQL)
- Review index usage periodically -- drop unused indexes

```sql
-- Composite index: equality (status) first, then range (created_at)
CREATE INDEX CONCURRENTLY idx_orders_status_created
ON orders (status, created_at DESC);

-- Partial index: only index active users
CREATE INDEX idx_users_email_active
ON users (email) WHERE is_active = true;
```

### Transactions

- Keep transactions as short as possible (no I/O or external calls inside)
- Use `READ COMMITTED` for most operations (PostgreSQL default)
- Use `REPEATABLE READ` when a transaction reads the same data multiple times
- Use `SERIALIZABLE` for financial or inventory operations requiring strict consistency
- Always explicitly `COMMIT` or `ROLLBACK` -- never leave transactions hanging
- Use `SAVEPOINT` for partial rollback within complex transactions

```sql
BEGIN;
  SAVEPOINT before_update;

  UPDATE accounts SET balance = balance - 100.00 WHERE id = $1;
  UPDATE accounts SET balance = balance + 100.00 WHERE id = $2;

  -- If second update fails, roll back to savepoint
  -- ROLLBACK TO SAVEPOINT before_update;
COMMIT;
```

### Migrations

- Every migration MUST have both `up` and `down` functions
- Migrations MUST be idempotent (`IF NOT EXISTS`, `IF EXISTS` guards)
- Never rename or drop columns in a single step -- use a multi-step process
- Add columns as `NULL` first, backfill, then add `NOT NULL` constraint
- Never modify a migration that has been applied to a shared environment
- Migration filenames: `YYYYMMDDHHMMSS_description.sql` or sequential numbering
- Test both `up` and `down` in development before committing

```sql
-- UP: 20250115120000_add_users_phone.sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_phone
ON users (phone) WHERE phone IS NOT NULL;

-- DOWN: 20250115120000_add_users_phone.sql
DROP INDEX CONCURRENTLY IF EXISTS idx_users_phone;
ALTER TABLE users DROP COLUMN IF EXISTS phone;
```

## Schema Design

### Standard Table Template

```sql
CREATE TABLE IF NOT EXISTS orders (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id       BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status        VARCHAR(20) NOT NULL DEFAULT 'pending'
                    CONSTRAINT ck_orders_valid_status
                    CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    total_cents   INTEGER NOT NULL
                    CONSTRAINT ck_orders_positive_total CHECK (total_cents >= 0),
    notes         TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Auto-update updated_at (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Design Rules

- Use `BIGINT GENERATED ALWAYS AS IDENTITY` for auto-increment PKs (PostgreSQL 10+)
- Use `UUID` PKs when IDs are exposed externally or distributed systems require it
- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all time columns -- always store UTC
- Add `NOT NULL` constraints by default; allow `NULL` only when semantically meaningful
- Use `CHECK` constraints to enforce domain rules at the database level
- Use `ENUM` types sparingly -- prefer `VARCHAR` with `CHECK` for easier migration
- Add `ON DELETE CASCADE` or `ON DELETE SET NULL` explicitly to every foreign key
- Use soft deletes (`deleted_at TIMESTAMPTZ`) when audit trail is required

## Key Patterns

### Common Table Expressions (CTEs)

Prefer CTEs over subqueries for readability and maintainability.

```sql
-- Readable: each step has a name
WITH active_orders AS (
    SELECT user_id, COUNT(*) AS order_count, SUM(total_cents) AS total_spent
    FROM orders
    WHERE status != 'cancelled'
      AND created_at >= now() - INTERVAL '30 days'
    GROUP BY user_id
),
high_value_users AS (
    SELECT user_id
    FROM active_orders
    WHERE total_spent > 50000  -- over $500
)
SELECT u.id, u.email, ao.order_count, ao.total_spent
FROM users u
JOIN active_orders ao ON ao.user_id = u.id
WHERE u.id IN (SELECT user_id FROM high_value_users)
ORDER BY ao.total_spent DESC;
```

### Window Functions

Use window functions for ranking, running totals, and row comparisons without self-joins.

```sql
-- Rank users by spending within each region
SELECT
    u.id,
    u.region,
    SUM(o.total_cents) AS total_spent,
    RANK() OVER (PARTITION BY u.region ORDER BY SUM(o.total_cents) DESC) AS rank
FROM users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.region;

-- Running total of daily revenue
SELECT
    date_trunc('day', created_at) AS day,
    SUM(total_cents) AS daily_revenue,
    SUM(SUM(total_cents)) OVER (ORDER BY date_trunc('day', created_at)) AS running_total
FROM orders
WHERE status = 'delivered'
GROUP BY date_trunc('day', created_at)
ORDER BY day;
```

### UPSERT (INSERT ... ON CONFLICT)

```sql
-- PostgreSQL: insert or update on conflict
INSERT INTO user_preferences (user_id, theme, language)
VALUES ($1, $2, $3)
ON CONFLICT (user_id)
DO UPDATE SET
    theme = EXCLUDED.theme,
    language = EXCLUDED.language,
    updated_at = now();
```

### Batch Operations

```sql
-- Batch insert with unnest (PostgreSQL)
INSERT INTO tags (name, category)
SELECT unnest($1::text[]), unnest($2::text[])
ON CONFLICT (name) DO NOTHING;

-- Batch update with VALUES list
UPDATE products AS p
SET price_cents = v.new_price
FROM (VALUES
    (1, 2999),
    (2, 4999),
    (3, 1499)
) AS v(id, new_price)
WHERE p.id = v.id;
```

### Parameterized Queries (Application Code)

```python
# Python (psycopg2/asyncpg) -- ALWAYS use parameterized queries
cursor.execute(
    "SELECT id, email FROM users WHERE email = %s AND is_active = %s",
    (email, True),
)

# Node.js (pg)
const result = await pool.query(
    'SELECT id, email FROM users WHERE email = $1 AND is_active = $2',
    [email, true]
);

# Go (database/sql)
row := db.QueryRowContext(ctx,
    "SELECT id, email FROM users WHERE email = $1 AND is_active = $2",
    email, true,
)
```

## Performance

### EXPLAIN ANALYZE

Always use `EXPLAIN ANALYZE` to validate query plans before deploying.

```sql
-- Check execution plan and actual timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2025-01-01'
GROUP BY u.id, u.email
ORDER BY order_count DESC
LIMIT 20;
```

**What to look for:**
- `Seq Scan` on large tables -- usually needs an index
- `Nested Loop` with large outer sets -- consider `Hash Join` via index or rewrite
- `Sort` operations with high cost -- add index matching `ORDER BY`
- `Rows Removed by Filter` much larger than `Actual Rows` -- index the filter column
- `Buffers: shared hit` vs `shared read` -- high reads indicate cold cache

### Index Strategy

| Access Pattern | Index Type | Example |
|---|---|---|
| Equality lookup | B-tree (default) | `WHERE email = $1` |
| Range scan | B-tree | `WHERE created_at > $1` |
| Full-text search | GIN + tsvector | `WHERE search_vector @@ to_tsquery($1)` |
| JSONB field access | GIN | `WHERE metadata @> '{"key": "val"}'` |
| Array containment | GIN | `WHERE tags @> ARRAY['sql']` |
| Geometric/spatial | GiST | `WHERE location <-> point($1,$2) < $3` |
| Pattern matching (`LIKE 'abc%'`) | B-tree with `text_pattern_ops` | `WHERE name LIKE 'abc%'` |

### N+1 Prevention

```sql
-- BAD: N+1 (one query per user to fetch orders)
-- Application loops: for each user, SELECT orders WHERE user_id = ?

-- GOOD: single query with JOIN
SELECT u.id, u.email, o.id AS order_id, o.total_cents
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.is_active = true
ORDER BY u.id, o.created_at DESC;

-- GOOD: batch with ANY (when you have a list of IDs)
SELECT id, email, created_at
FROM users
WHERE id = ANY($1::bigint[]);
```

### Pagination

```sql
-- Cursor-based pagination (preferred for large datasets)
SELECT id, email, created_at
FROM users
WHERE created_at < $1  -- cursor: last seen created_at
  AND is_active = true
ORDER BY created_at DESC
LIMIT 25;

-- Offset-based pagination (simpler but slower for deep pages)
SELECT id, email, created_at
FROM users
WHERE is_active = true
ORDER BY created_at DESC
LIMIT 25 OFFSET $1;
```

## Tooling

### Essential Commands

```bash
# PostgreSQL CLI
psql -h localhost -U myuser -d mydb       # Connect
psql -f migration.sql mydb                # Run migration file
pg_dump -Fc mydb > backup.dump            # Backup (custom format)
pg_restore -d mydb backup.dump            # Restore

# pgcli (enhanced CLI with autocomplete)
pgcli -h localhost -U myuser -d mydb

# Schema inspection
\dt                   # List tables
\d+ table_name        # Describe table with details
\di                   # List indexes
\df                   # List functions
```

### Migration Tools

```bash
# golang-migrate
migrate create -ext sql -dir db/migrations -seq add_users_phone
migrate -path db/migrations -database "$DATABASE_URL" up
migrate -path db/migrations -database "$DATABASE_URL" down 1

# Alembic (Python/SQLAlchemy)
alembic revision -m "add users phone"
alembic upgrade head
alembic downgrade -1

# Prisma (Node.js)
npx prisma migrate dev --name add_users_phone
npx prisma migrate deploy

# dbmate
dbmate new add_users_phone
dbmate up
dbmate rollback
```

### Useful Diagnostic Queries (PostgreSQL)

```sql
-- Find slow queries (requires pg_stat_statements extension)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%pkey%'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Active connections and queries
SELECT pid, state, query, query_start, now() - query_start AS duration
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Window functions, CTE patterns, indexing strategies, advanced query techniques

## External References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [Use The Index, Luke](https://use-the-index-luke.com/) -- SQL indexing and tuning
- [Modern SQL](https://modern-sql.com/) -- Modern SQL features across databases
- [pgMustard EXPLAIN Guide](https://www.pgmustard.com/docs/explain) -- Reading query plans
- [SQL Style Guide (Holywell)](https://www.sqlstyle.guide/) -- Formatting conventions
- [Postgres Wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This) -- Common PostgreSQL anti-patterns
