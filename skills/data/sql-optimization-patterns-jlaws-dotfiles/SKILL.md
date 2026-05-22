---
name: sql-optimization-patterns
description: Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use when debugging slow queries, designing database schemas, or optimizing application performance.
---

# SQL Optimization Patterns

## EXPLAIN Analysis

```sql
-- With actual execution stats (PostgreSQL)
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

**Key Metrics:**
- **Seq Scan**: Full table scan (usually slow for large tables)
- **Index Scan / Index Only Scan**: Using index (good / best)
- **Nested Loop**: Join for small datasets
- **Hash Join**: Join for larger datasets
- **Merge Join**: Join for sorted data

## Index Strategies

| Type | Use Case |
|------|----------|
| **B-Tree** | Default: equality/range (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`) |
| **Hash** | Only equality (`=`) |
| **GIN** | Full-text, arrays, JSONB (`@>`, `?`, `@@`) |
| **GiST** | Geometric data, ranges |
| **BRIN** | Very large naturally ordered tables (time-series) |

```sql
-- Standard B-Tree
CREATE INDEX idx_users_email ON users(email);

-- Composite (order matters - leftmost prefix used)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (index subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering (index-only scans)
CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (name, created_at);

-- Full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

## Pattern 1: Eliminate N+1 Queries

```python
# BAD: N+1 queries
users = db.query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)
```

```sql
-- FIX: JOIN
SELECT u.id, u.name, o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3, 4, 5);

-- FIX: Batch query
SELECT * FROM orders WHERE user_id IN (1, 2, 3, 4, 5);
```

## Pattern 2: Cursor-Based Pagination

```sql
-- BAD: OFFSET on large tables
SELECT * FROM users ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- GOOD: Cursor-based
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Requires index
CREATE INDEX idx_users_cursor ON users(created_at DESC, id DESC);
```

## Pattern 3: Aggregate Efficiently

```sql
-- Approximate count (fast)
SELECT reltuples::bigint AS estimate FROM pg_class WHERE relname = 'orders';

-- Filter before counting
SELECT COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL '7 days';

-- Filter first, then group
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id
HAVING COUNT(*) > 10;
```

## Pattern 4: Subquery Optimization

```sql
-- BAD: Correlated subquery
SELECT u.name, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- GOOD: JOIN with aggregation
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;

-- CTEs for clarity
WITH recent_users AS (
    SELECT id, name, email FROM users
    WHERE created_at > NOW() - INTERVAL '30 days'
),
user_order_counts AS (
    SELECT user_id, COUNT(*) as order_count FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT ru.name, COALESCE(uoc.order_count, 0) as orders
FROM recent_users ru
LEFT JOIN user_order_counts uoc ON ru.id = uoc.user_id;
```

## Pattern 5: Batch Operations

```sql
-- Batch insert
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com');

-- Bulk insert (PostgreSQL)
COPY users (name, email) FROM '/tmp/users.csv' CSV HEADER;

-- Batch update with temp table
CREATE TEMP TABLE temp_user_updates (id INT, new_status VARCHAR);
INSERT INTO temp_user_updates VALUES (1, 'active'), (2, 'active');
UPDATE users u SET status = t.new_status FROM temp_user_updates t WHERE u.id = t.id;
```

## Materialized Views

```sql
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT u.id, u.name, COUNT(o.id) as total_orders,
    SUM(o.total) as total_spent, MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

CREATE INDEX idx_user_summary_spent ON user_order_summary(total_spent DESC);

-- Concurrent refresh (no lock)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;
```

## Partitioning

```sql
CREATE TABLE orders (
    id SERIAL, user_id INT, total DECIMAL, created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Queries auto-prune partitions
SELECT * FROM orders WHERE created_at BETWEEN '2024-02-01' AND '2024-02-28';
```

## Monitoring Queries

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Find missing indexes
SELECT schemaname, tablename, seq_scan, seq_tup_read,
    seq_tup_read / seq_scan AS avg_seq_tup_read
FROM pg_stat_user_tables WHERE seq_scan > 0
ORDER BY seq_tup_read DESC LIMIT 10;

-- Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Maintenance

```sql
ANALYZE users;              -- Update statistics
VACUUM ANALYZE users;       -- Reclaim dead tuples + stats
VACUUM FULL users;          -- Reclaim space (locks table)
REINDEX TABLE users;        -- Rebuild indexes
```
