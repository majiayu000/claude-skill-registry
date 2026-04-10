---
name: sql-query-optimization
description: SQL query optimization for PostgreSQL/MySQL with indexing, EXPLAIN analysis. Use for slow queries, N+1 problems, missing indexes, or encountering sequential scans, OFFSET pagination, temp table spills, inefficient JOINs.

  Keywords: sql optimization, query performance, database indexes, explain analyze, slow queries, n+1 problem,
  query plan, index strategy, composite index, covering index, postgresql performance, mysql optimization,
  query rewriting, prepared statements, connection pooling, sequential scan, missing index, SELECT *,
  LIMIT optimization, subquery performance, pagination, cursor based pagination, batch operations,
  pg_stat_statements, full-text search, bitmap scan, index only scan, query tuning, database performance,
  cache hit ratio, work_mem, shared_buffers, database monitoring
license: MIT
---

# SQL Query Optimization

**Status**: Production Ready ✅
**Last Updated**: 2025-12-15
**Latest Versions**: PostgreSQL 17, MySQL 8.4
**Dependencies**: None

---

## Quick Start (10 Minutes)

### 1. Identify Slow Query

```sql
-- PostgreSQL: Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 2. Analyze with EXPLAIN

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM orders WHERE user_id = 123;

-- Look for:
-- - Seq Scan on large tables → needs index
-- - High "Rows Removed by Filter" → poor selectivity
-- - Temp read/written → increase work_mem
```

### 3. Create Index

```sql
-- Add missing index
CREATE INDEX CONCURRENTLY idx_orders_user
ON orders(user_id);

-- Verify improvement
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE user_id = 123;
-- Execution time should drop 10-100x
```

---

## Critical Rules

### Always Do ✓

| Rule | Why | Example |
|------|-----|---------|
| Index foreign keys | JOINs need indexed columns | `CREATE INDEX idx_orders_user ON orders(user_id)` |
| Use EXPLAIN ANALYZE before production | Verify query plan is optimal | `EXPLAIN (ANALYZE, BUFFERS) <query>` |
| Select specific columns | Reduces data transfer 90% | `SELECT id, name FROM users` not `SELECT *` |
| Add LIMIT to unbounded queries | Prevents memory exhaustion | `SELECT * FROM logs ORDER BY id LIMIT 100` |
| Use prepared statements | Prevents SQL injection + faster | `db.query('SELECT * FROM users WHERE id = $1', [id])` |
| Run ANALYZE after bulk operations | Updates query planner statistics | `ANALYZE table_name` |
| Monitor pg_stat_statements | Track query performance over time | Review daily for regressions |
| Use connection pooling | Reduces connection overhead 10x | `new Pool({ max: 20 })` |

### Never Do ✗

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| SELECT * in production | Fetches unnecessary columns | Select specific columns only |
| Leading wildcard LIKE '%term%' | Cannot use index | Use full-text search instead |
| String concatenation for SQL | SQL injection vulnerability | Use parameterized queries |
| No LIMIT on large results | Memory exhaustion | Always add LIMIT + pagination |
| N+1 queries in loops | Network latency × N | Use JOIN or batch loading |
| Ignoring EXPLAIN output | Deploy slow queries to production | Always EXPLAIN before deploy |
| Multiple INSERTs in loop | Slow bulk operations | Use batch INSERT with multiple VALUES |
| OFFSET for pagination | O(n) time, scans skipped rows | Use cursor-based pagination |

---

## Top 7 Critical Errors

### 1. Sequential Scan on Large Table
**Symptom**: `Seq Scan on orders (cost=0.00..150000.00)` on 1M+ rows
**Cause**: No index on filter column
**Fix**: `CREATE INDEX idx_orders_column ON orders(column)`
**Impact**: 10-100x faster

### 2. Missing Index on Foreign Key
**Symptom**: Slow JOINs (5+ seconds)
**Cause**: Foreign key columns not indexed
**Fix**: `CREATE INDEX idx_orders_user_id ON orders(user_id)`
**Impact**: 50-500x faster JOINs

### 3. N+1 Query Problem
**Symptom**: 1 + N queries for N records
**Cause**: ORM lazy loading in loop
**Fix**: Use JOIN or eager loading: `SELECT u.*, o.* FROM users u LEFT JOIN orders o ON u.id = o.user_id`
**Impact**: N queries → 1 query

### 4. Leading Wildcard LIKE
**Symptom**: `WHERE name LIKE '%search%'` sequential scan
**Cause**: Index cannot match middle of string
**Fix**: Use full-text search (GIN index) or trigrams
**Impact**: 100-1000x faster

### 5. SELECT * in Production
**Symptom**: High network traffic, slow responses
**Cause**: Fetches all 50 columns instead of needed 3
**Fix**: `SELECT id, name, email` (explicit column list)
**Impact**: 90% less data transfer

### 6. Missing LIMIT on Large Results
**Symptom**: Server out of memory, query timeout
**Cause**: Attempting to return 5M rows
**Fix**: `SELECT * FROM logs WHERE ... LIMIT 100` + pagination
**Impact**: Constant memory usage

### 7. Stale Statistics After Bulk Load
**Symptom**: Wrong query plan chosen despite index
**Cause**: PostgreSQL statistics outdated
**Fix**: `ANALYZE table_name` after bulk operations
**Impact**: Correct query plan selection

**See `references/error-catalog.md` for all 12 errors with detailed solutions.**

---

## Common Patterns Summary

| Pattern | Use Case | Example | Performance |
|---------|----------|---------|-------------|
| **B-Tree Index** | Equality, range, sort queries | `CREATE INDEX idx ON t(col)` | Default, best general purpose |
| **Composite Index** | Multi-column WHERE clauses | `CREATE INDEX idx ON t(c1, c2)` | 5-50x faster than single index |
| **Covering Index** | Include all query columns | `CREATE INDEX idx ON t(c1) INCLUDE (c2)` | 2-10x faster (no heap fetch) |
| **Partial Index** | Filter subset of rows | `CREATE INDEX idx ON t(c) WHERE status='active'` | 50-90% smaller index |
| **JOIN Rewrite** | Replace IN subquery | `INNER JOIN users u ON o.user_id = u.id` | 5-20x faster than subquery |
| **Batch INSERT** | Bulk data loading | `INSERT INTO t VALUES (..),(..)` | 10-100x faster than individual |
| **Cursor Pagination** | Large offset performance | `WHERE id > last_id LIMIT 100` | Constant time vs O(n) |

---

## Configuration Summary

### PostgreSQL Config

```sql
-- Increase work_mem for complex queries (reloadable - no restart needed)
SET work_mem = '256MB';

-- Increase shared_buffers for better caching (25% of RAM)
ALTER SYSTEM SET shared_buffers = '8GB';

-- IMPORTANT: shared_buffers requires a full PostgreSQL server restart!
-- This setting is NOT reloadable via pg_reload_conf()
--
-- To apply shared_buffers change:
-- 1. Stop PostgreSQL:   sudo systemctl stop postgresql
-- 2. Start PostgreSQL:  sudo systemctl start postgresql
-- OR use:              sudo systemctl restart postgresql
--
-- Verify the change took effect:
-- SHOW shared_buffers;

-- Enable auto-vacuum (reloadable - can use pg_reload_conf)
ALTER SYSTEM SET autovacuum = on;

-- Reload config (ONLY works for parameters that don't require restart)
-- This will NOT reload shared_buffers - restart required for that!
SELECT pg_reload_conf();
```

### MySQL Config

```ini
# my.cnf
[mysqld]
innodb_buffer_pool_size = 8G  # 70% of RAM
max_connections = 500
slow_query_log = 1
long_query_time = 1
```

---

## When to Load References

**Performance Analysis**:
- Load `references/explain-analysis.md` when: Reading EXPLAIN output, understanding query plans, analyzing buffer statistics, comparing PostgreSQL vs MySQL EXPLAIN
- Load `references/performance-monitoring.md` when: Setting up monitoring, tracking slow queries over time, monitoring cache hit ratios, identifying bloated tables

**Index Optimization**:
- Load `references/index-strategies.md` when: Choosing index type (B-Tree, GIN, GiST, Hash), creating composite indexes, determining column order, using covering indexes, implementing partial indexes, monitoring index usage

**Query Optimization**:
- Load `references/query-rewrites.md` when: Rewriting slow queries, converting subqueries to JOINs, eliminating N+1 queries, implementing pagination, optimizing LIKE queries, batching operations

**Systematic Process**:
- Load `references/optimization-workflow.md` when: Following step-by-step optimization process, creating optimization hypothesis, measuring improvements, monitoring long-term performance

**Error Resolution**:
- Load `references/error-catalog.md` when: Debugging specific errors (sequential scans, missing indexes, N+1 queries, etc.), understanding root causes, implementing verified solutions

---

## Using Bundled Resources

### Templates (Copy-Paste SQL)

```bash
# EXPLAIN query templates
templates/explain-query.sql

# Index creation patterns
templates/index-examples.sql

# Query rewrite examples
templates/query-rewrites.sql

# Monitoring queries
templates/monitoring-queries.sql
```

### References (Deep Dives)

```bash
# Comprehensive guides
references/error-catalog.md              # All 12 errors + solutions
references/explain-analysis.md           # Reading query plans
references/index-strategies.md           # Index types & selection
references/query-rewrites.md             # Before/after optimizations
references/performance-monitoring.md     # Long-term monitoring
references/optimization-workflow.md      # Systematic process
```

---

## Dependencies

**PostgreSQL Extensions**:
- `pg_stat_statements` - Query performance tracking (built-in)
- `pg_trgm` - Trigram similarity search (optional, for fuzzy matching)

**MySQL**:
- `performance_schema` - Performance monitoring (enabled by default in 8.0+)

**No additional dependencies required.**

---

## Known Issues Prevention

| Issue | Symptom | Prevention |
|-------|---------|------------|
| Sequential scans | Seq Scan on 1M+ rows | Index filter columns before production |
| Missing FK indexes | Slow JOINs | Always index foreign keys |
| N+1 queries | 1+N database calls | Use JOIN or eager loading |
| Leading wildcards | LIKE '%x%' slow | Use full-text search (GIN) |
| SELECT * bloat | High network traffic | Select specific columns |
| No LIMIT | Memory exhaustion | Always LIMIT unbounded queries |
| Stale statistics | Wrong query plans | ANALYZE after bulk operations |
| Wrong index order | Index exists but not used | Match query pattern |
| Missing composite | Multiple WHERE slow | Create composite index |
| No connection pool | High latency | Implement pooling (20-50 connections) |
| SQL injection | Security vulnerability | Use prepared statements only |
| Temp spills | Disk I/O on sorts | Increase work_mem |

---

## Complete Setup Checklist

Production Deployment:
- [ ] Enable pg_stat_statements or performance_schema
- [ ] Index all foreign key columns
- [ ] Index columns in WHERE, JOIN, ORDER BY clauses
- [ ] Replace SELECT * with specific columns
- [ ] Add LIMIT to all unbounded queries
- [ ] Use prepared statements (parameterized queries)
- [ ] Implement connection pooling (20-50 connections)
- [ ] Configure work_mem (256MB-1GB per connection)
- [ ] Configure shared_buffers (25% of RAM for PostgreSQL)
- [ ] Enable slow query logging (threshold: 100-1000ms)
- [ ] Run EXPLAIN ANALYZE on all critical queries
- [ ] Set up daily monitoring of pg_stat_statements
- [ ] Schedule ANALYZE after nightly bulk operations
- [ ] Monitor cache hit ratio (target: >99%)
- [ ] Review and drop unused indexes monthly

---

## Production Example

**Before Optimization**:
```sql
-- Query: Fetch user orders
SELECT * FROM orders WHERE user_id = 123;

-- Performance:
-- Execution time: 2500ms
-- Seq Scan on orders (1M rows scanned)
-- Network: 50MB transferred
-- No index on user_id
```

**After Optimization**:
```sql
-- Add index
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);

-- Optimize query
SELECT id, total, status, created_at
FROM orders
WHERE user_id = 123
LIMIT 100;

-- Performance:
-- Execution time: 12ms (208x faster!)
-- Index Scan using idx_orders_user_id (100 rows)
-- Network: 50KB transferred (1000x less!)
-- Covering index with INCLUDE
```

**Result**: 208x faster execution, 1000x less data transfer

---

**For comprehensive optimization guidance, error resolution, and production patterns, load the appropriate reference files listed in "When to Load References" above.**
