---
name: optimizing-sql
description: Optimize SQL query performance through EXPLAIN analysis, indexing strategies, and query rewriting for PostgreSQL, MySQL, and SQL Server. Use when debugging slow queries, analyzing execution plans, or improving database performance.
---

# SQL Optimization

Provide tactical guidance for optimizing SQL query performance across PostgreSQL, MySQL, and SQL Server through execution plan analysis, strategic indexing, and query rewriting.

## When to Use This Skill

Trigger this skill when encountering:
- Slow query performance or database timeouts
- Analyzing EXPLAIN plans or execution plans
- Determining index requirements
- Rewriting inefficient queries
- Identifying query anti-patterns (N+1, SELECT *, correlated subqueries)
- Database-specific optimization needs (PostgreSQL, MySQL, SQL Server)

## Core Optimization Workflow

### Step 1: Analyze Query Performance

Run execution plan analysis to identify bottlenecks:

**PostgreSQL:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

**MySQL:**
```sql
EXPLAIN FORMAT=JSON SELECT * FROM products WHERE category_id = 5;
```

**SQL Server:**
Use SQL Server Management Studio: Display Estimated Execution Plan (Ctrl+L)

**Key Metrics to Monitor:**
- **Cost**: Estimated resource consumption
- **Rows**: Number of rows processed (estimated vs actual)
- **Scan Type**: Sequential scan vs index scan
- **Execution Time**: Actual time spent on operation

For detailed execution plan interpretation, see `references/explain-guide.md`.

### Step 2: Identify Optimization Opportunities

**Common Red Flags:**

| Indicator | Problem | Solution |
|-----------|---------|----------|
| Seq Scan / Table Scan | Full table scan on large table | Add index on filter columns |
| High row count | Processing excessive rows | Add WHERE filter or index |
| Nested Loop with large outer table | Inefficient join algorithm | Index join columns |
| Correlated subquery | Subquery executes per row | Rewrite as JOIN or EXISTS |
| Sort operation on large result set | Expensive sorting | Add index matching ORDER BY |

For scan type interpretation, see `references/scan-types.md`.

### Step 3: Apply Indexing Strategies

**Index Decision Framework:**

```
Is column used in WHERE, JOIN, ORDER BY, or GROUP BY?
├─ YES → Is column selective (many unique values)?
│  ├─ YES → Is table frequently queried?
│  │  ├─ YES → ADD INDEX
│  │  └─ NO → Consider based on query frequency
│  └─ NO (low selectivity) → Skip index
└─ NO → Skip index
```

**Index Types by Use Case:**

**PostgreSQL:**
- **B-tree** (default): General-purpose, supports <, ≤, =, ≥, >, BETWEEN, IN
- **Hash**: Equality comparisons only (=)
- **GIN**: Full-text search, JSONB, arrays
- **GiST**: Spatial data, geometric types
- **BRIN**: Very large tables with naturally ordered data

**MySQL:**
- **B-tree** (default): General-purpose index
- **Full-text**: Text search on VARCHAR/TEXT columns
- **Spatial**: Spatial data types

**SQL Server:**
- **Clustered**: Table data sorted by index (one per table)
- **Non-clustered**: Separate index structure (multiple allowed)

For comprehensive indexing guidance, see `references/indexing-decisions.md` and `references/index-types.md`.

### Step 4: Design Composite Indexes

For queries filtering on multiple columns, use composite indexes:

**Column Order Matters:**
1. **Equality filters first** (most selective)
2. **Additional equality filters** (by selectivity)
3. **Range filters or ORDER BY** (last)

**Example:**
```sql
-- Query pattern
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'shipped'
ORDER BY created_at DESC
LIMIT 10;

-- Optimal composite index
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);
```

For composite index design patterns, see `references/composite-indexes.md`.

### Step 5: Rewrite Inefficient Queries

**Common Anti-Patterns to Avoid:**

**1. SELECT * (Over-fetching)**
```sql
-- ❌ Bad: Fetches all columns
SELECT * FROM users WHERE id = 1;

-- ✅ Good: Fetch only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

**2. N+1 Queries**
```sql
-- ❌ Bad: 1 + N queries
SELECT * FROM users LIMIT 100;
-- Then in loop: SELECT * FROM posts WHERE user_id = ?;

-- ✅ Good: Single JOIN
SELECT users.*, posts.id AS post_id, posts.title
FROM users
LEFT JOIN posts ON users.id = posts.user_id;
```

**3. Non-Sargable Queries** (functions on indexed columns)
```sql
-- ❌ Bad: Function prevents index usage
SELECT * FROM orders WHERE YEAR(created_at) = 2025;

-- ✅ Good: Sargable range condition
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

**4. Correlated Subqueries**
```sql
-- ❌ Bad: Subquery executes per row
SELECT name,
  (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id)
FROM users;

-- ✅ Good: JOIN with GROUP BY
SELECT users.name, COUNT(orders.id) AS order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
```

For complete anti-pattern reference, see `references/anti-patterns.md`.
For efficient query patterns, see `references/efficient-patterns.md`.

## Quick Reference Tables

### Index Selection Guide

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE column = value` | Single-column B-tree | `CREATE INDEX ON table (column)` |
| `WHERE col1 = ? AND col2 = ?` | Composite B-tree | `CREATE INDEX ON table (col1, col2)` |
| `WHERE text_col LIKE '%word%'` | Full-text (GIN/Full-text) | `CREATE INDEX ON table USING GIN (to_tsvector('english', text_col))` |
| `WHERE geom && box` | Spatial (GiST) | `CREATE INDEX ON table USING GIST (geom)` |
| `WHERE json_col @> '{"key":"value"}'` | JSONB (GIN) | `CREATE INDEX ON table USING GIN (json_col)` |

### Join Optimization Checklist

- [ ] Index foreign key columns on both sides of JOIN
- [ ] Order joins starting with table returning fewest rows
- [ ] Use INNER JOIN when possible (more efficient than OUTER JOIN)
- [ ] Avoid joining more than 5 tables (break into CTEs or subqueries)
- [ ] Consider denormalization for frequently joined tables in read-heavy systems

### Execution Plan Performance Targets

| Scan Type | Performance | When Acceptable |
|-----------|-------------|-----------------|
| Index-Only Scan | Best | Always preferred |
| Index Scan | Excellent | Small-medium result sets |
| Bitmap Heap Scan | Good | Medium result sets (PostgreSQL) |
| Sequential Scan | Poor | Only for small tables (<1000 rows) or full table queries |
| Table Scan | Poor | Only for small tables or unavoidable full scans |

## Database-Specific Optimizations

### PostgreSQL-Specific Features

**Partial Indexes** (index subset of rows):
```sql
CREATE INDEX idx_active_users_login
ON users (last_login)
WHERE status = 'active';
```

**Expression Indexes** (index computed values):
```sql
CREATE INDEX idx_users_email_lower
ON users (LOWER(email));
```

**Covering Indexes** (avoid heap access):
```sql
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name);
```

For comprehensive PostgreSQL optimization, see `references/postgresql.md`.

### MySQL-Specific Features

**Index Hints** (override optimizer):
```sql
SELECT * FROM orders USE INDEX (idx_orders_customer)
WHERE customer_id = 123;
```

**Storage Engine Selection:**
- **InnoDB** (default): Transactional, row-level locks, clustered primary key
- **MyISAM**: Faster reads, no transactions, table-level locks

For comprehensive MySQL optimization, see `references/mysql.md`.

### SQL Server-Specific Features

**Query Store** (track query performance over time):
```sql
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
```

**Execution Plan Warnings:**
- Look for yellow exclamation marks in graphical execution plans
- Thick arrows indicate high row counts

For comprehensive SQL Server optimization, see `references/sqlserver.md`.

## Advanced Optimization Techniques

### Common Table Expressions (CTEs)

Break complex queries into readable, maintainable parts:

```sql
WITH active_customers AS (
  SELECT id, name FROM customers WHERE status = 'active'
),
recent_orders AS (
  SELECT customer_id, COUNT(*) as order_count
  FROM orders
  WHERE created_at > NOW() - INTERVAL '30 days'
  GROUP BY customer_id
)
SELECT ac.name, COALESCE(ro.order_count, 0) as orders
FROM active_customers ac
LEFT JOIN recent_orders ro ON ac.id = ro.customer_id;
```

### EXISTS vs IN for Subqueries

Use EXISTS for better performance with large datasets:

```sql
-- ✅ Good: EXISTS stops at first match
SELECT * FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);

-- ❌ Less efficient: IN builds full list
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);
```

### Denormalization Decision Framework

Consider denormalization when:
- Query joins 3+ tables frequently
- Data is relatively static (infrequent updates)
- Read performance is critical
- Write overhead is acceptable

**Denormalization Strategies:**
1. **Duplicate columns**: Copy foreign key data into main table
2. **Summary tables**: Pre-aggregate data
3. **Materialized views**: Database-maintained denormalized views
4. **Application caching**: Redis/Memcached for frequently accessed data

## Optimization Workflow Example

**Scenario:** API endpoint taking 2 seconds to load

**Step 1: Identify Slow Query**
```
Use APM/observability tools to identify database query causing delay
```

**Step 2: Run EXPLAIN ANALYZE**
```sql
EXPLAIN ANALYZE SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

**Step 3: Analyze Output**
```
Seq Scan on orders (cost=0.00..2500.00 rows=10)
  Filter: (customer_id = 123)
  Rows Removed by Filter: 99990
```
**Problem**: Sequential scan filtering 99,990 rows

**Step 4: Add Composite Index**
```sql
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at DESC);
```

**Step 5: Verify Improvement**
```sql
EXPLAIN ANALYZE SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```
```
Index Scan using idx_orders_customer_created (cost=0.42..12.44 rows=10)
  Index Cond: (customer_id = 123)
```
**Result**: 200x faster (2000ms → 10ms)

## Monitoring and Maintenance

**Regular Optimization Tasks:**
- Review slow query logs weekly
- Update database statistics regularly (ANALYZE in PostgreSQL, UPDATE STATISTICS in SQL Server)
- Monitor index usage (drop unused indexes)
- Archive old data to keep tables manageable
- Review execution plans for critical queries quarterly

**PostgreSQL Statistics Update:**
```sql
ANALYZE table_name;
```

**MySQL Statistics Update:**
```sql
ANALYZE TABLE table_name;
```

**SQL Server Statistics Update:**
```sql
UPDATE STATISTICS table_name;
```

## Related Skills

- **databases-relational**: Schema design and database fundamentals
- **observability**: Performance monitoring and slow query detection
- **api-patterns**: API-level optimization (pagination, caching)
- **performance-engineering**: Application performance profiling

## Additional Resources

For comprehensive documentation, reference these files:

- `references/explain-guide.md` - Detailed EXPLAIN plan interpretation
- `references/scan-types.md` - Scan type meanings and performance implications
- `references/indexing-decisions.md` - When and how to add indexes
- `references/index-types.md` - Database-specific index types
- `references/composite-indexes.md` - Multi-column index design
- `references/anti-patterns.md` - Common anti-patterns with solutions
- `references/efficient-patterns.md` - Efficient query patterns
- `references/postgresql.md` - PostgreSQL-specific optimizations
- `references/mysql.md` - MySQL-specific optimizations
- `references/sqlserver.md` - SQL Server-specific optimizations

For working SQL examples, see `examples/` directory.
