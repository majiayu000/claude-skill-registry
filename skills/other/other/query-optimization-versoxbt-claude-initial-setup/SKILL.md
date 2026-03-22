---
name: query-optimization
description: >
  Guide for optimizing SQL queries with EXPLAIN ANALYZE, index tuning, N+1 detection,
  covering indexes, and query plan analysis. Use when the user has slow database queries,
  asks about query performance, needs to interpret EXPLAIN output, or wants to eliminate
  N+1 queries. Trigger whenever query performance, slow queries, or database optimization
  is discussed.
---

# Query Optimization

Diagnose and fix slow SQL queries using EXPLAIN ANALYZE, proper indexing, query
rewriting, and N+1 detection.

## When to Use
- User reports slow database queries
- User asks about EXPLAIN ANALYZE output
- User needs to optimize query performance
- User has N+1 query problems in an ORM
- User asks about index tuning or covering indexes

## Core Patterns

### EXPLAIN ANALYZE

Always start with EXPLAIN ANALYZE to understand what the database is actually doing.

```sql
-- Basic usage
EXPLAIN ANALYZE
SELECT o.id, o.status, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending'
ORDER BY o.ordered_at DESC
LIMIT 20;
```

Key things to look for in the output:

```
-- BAD: Sequential scan on large table
Seq Scan on orders  (cost=0.00..15234.00 rows=500000 width=48)
  Filter: (status = 'pending'::text)
  Rows Removed by Filter: 450000

-- GOOD: Index scan
Index Scan using idx_orders_status_ordered_at on orders
  (cost=0.42..85.20 rows=50000 width=48)
  Index Cond: (status = 'pending'::text)
```

```sql
-- Check actual vs estimated rows (large discrepancies mean stale statistics)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 12345;

-- If estimates are wrong, update statistics
ANALYZE orders;
```

### Index Tuning

Create indexes that match your query patterns. Column order in composite indexes matters.

```sql
-- Query: WHERE status = ? AND ordered_at > ? ORDER BY ordered_at
-- Index must match: equality columns first, then range/sort columns
CREATE INDEX idx_orders_status_ordered_at ON orders(status, ordered_at DESC);

-- Query: WHERE customer_id = ? AND status = ? ORDER BY ordered_at DESC
CREATE INDEX idx_orders_customer_status_date
  ON orders(customer_id, status, ordered_at DESC);

-- Verify the index is being used
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 100 AND status = 'pending'
ORDER BY ordered_at DESC
LIMIT 10;
```

### Covering Indexes (Index-Only Scans)

Include all columns the query needs in the index to avoid hitting the table at all.

```sql
-- Query only needs id, status, ordered_at
-- INCLUDE adds columns to the index leaf without affecting sort order
CREATE INDEX idx_orders_status_covering
  ON orders(status, ordered_at DESC)
  INCLUDE (id, customer_id);

-- This enables an index-only scan (no table lookup)
EXPLAIN ANALYZE
SELECT id, customer_id, ordered_at
FROM orders
WHERE status = 'pending'
ORDER BY ordered_at DESC
LIMIT 20;

-- Look for "Index Only Scan" in the output
```

### N+1 Query Detection and Fix

N+1 queries execute 1 query for the parent, then N queries for each child. Fix with
JOINs or batch loading.

```sql
-- BAD: N+1 pattern (executed in application code)
-- Query 1: SELECT * FROM orders WHERE status = 'pending'
-- Query 2..N+1: SELECT * FROM customers WHERE id = ?  (once per order)

-- GOOD: Single query with JOIN
SELECT o.id, o.status, o.ordered_at, c.name, c.email
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending'
ORDER BY o.ordered_at DESC;

-- GOOD: Batch loading (when JOIN produces too many rows)
SELECT * FROM orders WHERE status = 'pending' ORDER BY ordered_at DESC;
SELECT * FROM customers WHERE id IN (1, 2, 3, 4, 5);  -- collected IDs from first query
```

ORM-level fixes:

```python
# SQLAlchemy: Use joinedload or selectinload
from sqlalchemy.orm import joinedload, selectinload

# JOIN strategy (one query)
orders = session.query(Order).options(
    joinedload(Order.customer)
).filter(Order.status == "pending").all()

# Subquery strategy (two queries, better for large result sets)
orders = session.query(Order).options(
    selectinload(Order.items)
).filter(Order.status == "pending").all()
```

### Query Rewriting

Restructure queries to help the optimizer choose better plans.

```sql
-- BAD: Correlated subquery (executes per row)
SELECT c.name,
  (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) AS order_count
FROM customers c;

-- GOOD: JOIN with aggregation (single pass)
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;

-- BAD: OR conditions prevent index use
SELECT * FROM orders WHERE customer_id = 100 OR status = 'pending';

-- GOOD: UNION ALL uses indexes on both conditions
SELECT * FROM orders WHERE customer_id = 100
UNION ALL
SELECT * FROM orders WHERE status = 'pending' AND customer_id != 100;

-- BAD: Function on indexed column prevents index use
SELECT * FROM customers WHERE LOWER(email) = 'user@example.com';

-- GOOD: Expression index
CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));
SELECT * FROM customers WHERE LOWER(email) = 'user@example.com';
```

## Anti-Patterns

- **Not using EXPLAIN ANALYZE**: Guessing at performance problems wastes time. Always measure first with EXPLAIN ANALYZE.
- **Indexing every column**: Indexes cost write performance and storage. Index only columns used in WHERE, JOIN, and ORDER BY of frequent queries.
- **SELECT ***: Fetching all columns prevents covering index optimizations and wastes network bandwidth. Select only the columns you need.
- **Ignoring stale statistics**: PostgreSQL's planner uses table statistics to choose plans. Run `ANALYZE` after bulk data changes.
- **Using OFFSET for pagination**: `OFFSET 10000` still scans 10000 rows. Use keyset pagination: `WHERE id > last_seen_id ORDER BY id LIMIT 20`.
- **Premature optimization**: Optimize queries that are actually slow in production, not queries that might be slow someday.

## Quick Reference

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Find unused indexes
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find missing indexes (sequential scans on large tables)
SELECT relname, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND pg_relation_size(relid) > 10000000
ORDER BY seq_tup_read DESC;

-- Table and index sizes
SELECT
  relname AS table_name,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  pg_size_pretty(pg_indexes_size(relid)) AS index_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Keyset pagination (fast, stable)
SELECT * FROM orders
WHERE (ordered_at, id) < ('2024-01-15 10:30:00', 5000)
ORDER BY ordered_at DESC, id DESC
LIMIT 20;
```
