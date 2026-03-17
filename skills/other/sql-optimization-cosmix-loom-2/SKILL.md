---
name: sql-optimization
description: Analyzes and optimizes SQL queries for better performance, including index design, query rewriting, execution plan analysis, and database tuning. Covers PostgreSQL-specific optimizations, N+1 prevention, CTE/window function optimization, join strategies, and common anti-patterns. Trigger keywords: SQL, query optimization, EXPLAIN, EXPLAIN ANALYZE, index, slow query, execution plan, query plan, join optimization, subquery, CTE, common table expression, window function, partition, N+1, query cache, database performance, sequential scan, index scan, bitmap scan, nested loop, hash join, merge join, PostgreSQL, query tuning, table scan, cardinality, statistics, vacuum, analyze.
allowed-tools: Read, Grep, Glob, Bash
---

# SQL Optimization

## Overview

This skill focuses on analyzing and optimizing SQL queries for improved performance. It covers query analysis, index optimization, execution plan interpretation, query rewriting strategies, PostgreSQL-specific optimizations, and common anti-patterns. Use this skill for slow queries, N+1 problems, join optimization, index design, and database performance tuning.

## Instructions

### 1. Analyze Query Performance

- Identify slow queries from logs
- Run EXPLAIN/EXPLAIN ANALYZE
- Measure query execution time
- Check resource utilization

### 2. Understand Execution Plans

- Identify scan types (Sequential Scan, Index Scan, Bitmap Scan)
- Check join algorithms (Nested Loop, Hash Join, Merge Join)
- Analyze index usage and selectivity
- Find bottleneck operations (sorts, filters, aggregations)
- Understand cost estimates vs actual rows
- Check buffer usage and I/O patterns

### 3. Apply Optimizations

- Design appropriate indexes (B-tree, Hash, GiST, GIN)
- Rewrite inefficient queries (subqueries to JOINs, CTEs)
- Optimize join order and algorithms
- Use window functions for complex aggregations
- Leverage partial indexes and covering indexes
- Consider denormalization for read-heavy workloads
- Update table statistics (ANALYZE)
- Tune PostgreSQL configuration parameters

### 4. Validate Improvements

- Compare before/after metrics
- Test with production-like data
- Verify correctness
- Monitor after deployment

## Best Practices

1. **Index Strategically**: Index columns in WHERE, JOIN, ORDER BY
2. **Avoid SELECT \***: Select only needed columns
3. **Use EXPLAIN ANALYZE**: Always analyze execution plans with actual timing
4. **Limit Results**: Use pagination for large datasets
5. **Avoid N+1**: Use JOINs or batch queries
6. **Prefer EXISTS over IN**: For subqueries with large result sets
7. **Update Statistics**: Run ANALYZE after bulk operations
8. **Use CTEs for Readability**: But watch for optimization fences
9. **Avoid Functions on Indexed Columns**: Prevents index usage
10. **Monitor Continuously**: Track query performance over time

## PostgreSQL-Specific Optimizations

### Execution Plan Operators

**Scan Types:**

- **Sequential Scan**: Full table scan (slow for large tables)
- **Index Scan**: Uses index + table lookups (good for low selectivity)
- **Index Only Scan**: Uses covering index (fastest)
- **Bitmap Index Scan**: Multiple index scans combined (good for OR conditions)

**Join Algorithms:**

- **Nested Loop**: Best for small tables or index lookups
- **Hash Join**: Best for medium-sized tables with equality joins
- **Merge Join**: Best for large pre-sorted tables

### Statistics and Maintenance

```sql
-- Update table statistics for better query plans
ANALYZE table_name;

-- Check statistics freshness
SELECT schemaname, tablename, last_analyze, last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY last_analyze NULLS FIRST;

-- Find bloated tables
SELECT schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_dead_tup, n_live_tup,
    round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Vacuum bloated tables
VACUUM ANALYZE table_name;
```

### Configuration Tuning

```sql
-- Key parameters to check
SHOW shared_buffers;        -- Should be 25% of RAM
SHOW effective_cache_size;  -- Should be 50-75% of RAM
SHOW work_mem;              -- Per-operation memory
SHOW random_page_cost;      -- Lower for SSDs (1.1-2.0)
```

## Common Anti-Patterns

### 1. SELECT \* in Application Code

```sql
-- BAD: Fetches unnecessary columns
SELECT * FROM users WHERE id = 1;

-- GOOD: Fetch only needed columns
SELECT id, email, name FROM users WHERE id = 1;
```

### 2. Implicit Type Conversion

```sql
-- BAD: Can't use index if id is integer
SELECT * FROM users WHERE id = '123';

-- GOOD: Match column type
SELECT * FROM users WHERE id = 123;
```

### 3. OR Conditions Without Indexes

```sql
-- BAD: May not use indexes efficiently
SELECT * FROM orders WHERE status = 'pending' OR status = 'processing';

-- GOOD: Use IN or create partial index
SELECT * FROM orders WHERE status IN ('pending', 'processing');
```

### 4. Correlated Subqueries

```sql
-- BAD: Executes subquery for each row
SELECT p.name,
    (SELECT COUNT(*) FROM order_items WHERE product_id = p.id) AS order_count
FROM products p;

-- GOOD: Use JOIN with aggregation
SELECT p.name, COUNT(oi.id) AS order_count
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
GROUP BY p.id, p.name;
```

### 5. Missing WHERE Clauses

```sql
-- BAD: Updates entire table
UPDATE products SET updated_at = NOW();

-- GOOD: Update only what changed
UPDATE products SET updated_at = NOW()
WHERE id IN (SELECT product_id FROM price_changes);
```

## Advanced Patterns

### CTEs (Common Table Expressions)

```sql
-- CTEs for readability and reusability
WITH recent_orders AS (
    SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS total_spent
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY customer_id
),
high_value_customers AS (
    SELECT customer_id
    FROM recent_orders
    WHERE total_spent > 1000
)
SELECT c.name, c.email, ro.order_count, ro.total_spent
FROM customers c
INNER JOIN high_value_customers hvc ON c.id = hvc.customer_id
INNER JOIN recent_orders ro ON c.id = ro.customer_id;

-- Recursive CTEs for hierarchical data
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 AS level
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

### Window Functions

```sql
-- Ranking and row numbers
SELECT
    product_id,
    category_id,
    price,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank,
    RANK() OVER (ORDER BY price DESC) AS overall_rank,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS dense_rank
FROM products;

-- Running totals and moving averages
SELECT
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7day
FROM daily_sales
ORDER BY date;

-- Lead/Lag for time-series analysis
SELECT
    customer_id,
    order_date,
    total,
    LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date,
    LEAD(total) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order_total,
    total - LAG(total) OVER (PARTITION BY customer_id ORDER BY order_date) AS total_diff
FROM orders;
```

## Examples

### Example 1: Query Optimization with EXPLAIN

```sql
-- Original slow query
SELECT o.*, c.name, c.email
FROM orders o, customers c
WHERE o.customer_id = c.id
AND o.status = 'pending'
AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC;

-- Step 1: Analyze with EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name, c.email
FROM orders o, customers c
WHERE o.customer_id = c.id
AND o.status = 'pending'
AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC;

-- Output analysis:
-- Seq Scan on orders  (cost=0.00..15420.00 rows=50000)
--   Filter: (status = 'pending' AND created_at > '2024-01-01')
--   Rows Removed by Filter: 450000
-- Problem: Sequential scan on large table!

-- Step 2: Create composite index
CREATE INDEX idx_orders_status_created
ON orders(status, created_at DESC)
WHERE status IN ('pending', 'processing');

-- Step 3: Rewrite with explicit JOIN
SELECT o.id, o.total, o.created_at, c.name, c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending'
AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC
LIMIT 100;

-- After optimization:
-- Index Scan using idx_orders_status_created (cost=0.42..125.50 rows=100)
-- 99% reduction in query time!
```

### Example 2: N+1 Query Problem

```sql
-- Problem: N+1 queries
-- Application code:
-- orders = SELECT * FROM orders WHERE user_id = 1
-- for order in orders:
--     items = SELECT * FROM order_items WHERE order_id = order.id

-- Solution: Single query with JOIN
SELECT
    o.id AS order_id,
    o.total,
    o.created_at,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    p.name AS product_name
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.user_id = 1
ORDER BY o.created_at DESC, oi.id;

-- Alternative: Batch query
SELECT * FROM orders WHERE user_id = 1;
-- Get order IDs: [1, 2, 3, 4, 5]
SELECT * FROM order_items WHERE order_id IN (1, 2, 3, 4, 5);
```

### Example 3: Index Design Strategies

```sql
-- Single column index for equality checks
CREATE INDEX idx_users_email ON users(email);

-- Composite index for multiple conditions
-- Order columns: equality first, then range, then sort
CREATE INDEX idx_orders_user_status_date
ON orders(user_id, status, created_at DESC);

-- Partial index for filtered queries
CREATE INDEX idx_orders_pending
ON orders(created_at DESC)
WHERE status = 'pending';

-- Covering index to avoid table lookups
CREATE INDEX idx_orders_summary
ON orders(user_id, status)
INCLUDE (total, created_at);

-- Expression index for computed conditions
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Check existing indexes
SELECT
    indexname,
    indexdef,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes
WHERE tablename = 'orders';

-- Find unused indexes
SELECT
    schemaname, tablename, indexname,
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Example 4: Query Rewriting Patterns

```sql
-- Pattern 1: Replace subquery with JOIN
-- Before
SELECT * FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE region = 'US');

-- After
SELECT o.* FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE c.region = 'US';

-- Pattern 2: Use EXISTS instead of IN for large subqueries
-- Before
SELECT * FROM products
WHERE id IN (SELECT product_id FROM order_items);

-- After
SELECT * FROM products p
WHERE EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id
);

-- Pattern 3: Avoid functions on indexed columns
-- Before (can't use index)
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- After (uses index)
SELECT * FROM users
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- Pattern 4: Optimize pagination
-- Before (slow for large offsets)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 10000;

-- After (keyset pagination)
SELECT * FROM products
WHERE id > 10000
ORDER BY id
LIMIT 20;

-- Pattern 5: Batch operations
-- Before (row-by-row)
UPDATE products SET price = price * 1.1 WHERE id = 1;
UPDATE products SET price = price * 1.1 WHERE id = 2;
-- ... repeated 1000 times

-- After (single batch)
UPDATE products SET price = price * 1.1
WHERE id = ANY(ARRAY[1, 2, 3, ..., 1000]);

-- Or use CTE for complex batches
WITH price_updates AS (
    SELECT id, new_price FROM temp_price_updates
)
UPDATE products p
SET price = pu.new_price
FROM price_updates pu
WHERE p.id = pu.id;
```
