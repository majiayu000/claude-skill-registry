---
name: database-performance
description: Analyze and optimize database performance through index analysis and query profiling. Identify missing/unused indexes, interpret EXPLAIN plans, find performance bottlenecks, and recommend optimization strategies. Use when optimizing slow queries, analyzing database workloads, improving query execution speed, or managing database indexes.
---

# Database Performance Optimization

Comprehensive database performance analysis covering index optimization and query profiling to enhance database speed and efficiency.

## Overview

This skill empowers you to:
- **Analyze database indexes**: Identify missing indexes for better performance and unused indexes for removal
- **Profile query performance**: Interpret EXPLAIN plans, find bottlenecks, and optimize query execution
- **Recommend optimizations**: Provide actionable strategies for index creation, query rewriting, and configuration tuning

---

## Part 1: Index Analysis

### How It Works

1. **Workload Analysis**: Analyze database query patterns and existing index configurations
2. **Missing Index Detection**: Identify queries that would benefit from additional indexes
3. **Unused Index Detection**: Find indexes that are never used and can be safely removed
4. **Recommendation Generation**: Provide specific index creation/removal suggestions

### When to Use Index Analysis

- Optimize slow-running queries
- Identify performance bottlenecks related to missing indexes
- Reclaim storage space by removing unused indexes
- Plan index strategy for new tables
- Audit existing index configurations

### Index Analysis Examples

#### Example 1: Optimizing a Slow Query

**User request**: "My orders table query is running slowly. Can you help optimize it?"

**Analysis Process**:
1. Examine the query: `SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending'`
2. Check existing indexes on orders table
3. Identify missing composite index on `(customer_id, status)`
4. **Recommendation**: 
   ```sql
   CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
   ```

#### Example 2: Identifying Unused Indexes

**User request**: "Can you help me identify and remove any unused indexes in my database?"

**Analysis Process**:
1. Query database statistics for index usage
2. Identify indexes with zero reads
3. Verify these indexes aren't required for constraints
4. **Recommendation**:
   ```sql
   -- Indexes with 0 usage in last 30 days
   DROP INDEX idx_old_column ON users;
   DROP INDEX idx_rarely_used ON orders;
   ```

### Index Best Practices

**✅ DO:**
- Create indexes on columns frequently used in WHERE clauses
- Use composite indexes for queries filtering on multiple columns
- Index foreign keys for faster JOIN operations
- Monitor index usage regularly
- Remove unused indexes to improve write performance

**❌ DON'T:**
- Over-index tables (each index slows down writes)
- Create duplicate indexes (e.g., `(a)` and `(a, b)`)
- Index low-cardinality columns (e.g., boolean fields)
- Forget to analyze impact before dropping indexes

---

## Part 2: Query Performance Analysis

### How It Works

1. **Receive Input**: User provides EXPLAIN plan, slow query, or performance problem description
2. **Analyze Metrics**: Examine execution plan, identify full table scans, join inefficiencies, missing indexes
3. **Bottleneck Detection**: Pinpoint specific performance issues (I/O, CPU, memory)
4. **Provide Solutions**: Suggest query rewrites, new indexes, or configuration changes

### When to Use Query Analysis

- Analyze EXPLAIN plans of slow queries
- Identify performance bottlenecks in complex queries
- Optimize JOIN operations
- Reduce query execution time
- Understand database resource utilization

### Query Analysis Examples

#### Example 1: Analyzing a Slow Query with EXPLAIN

**User request**: "Here's the EXPLAIN plan for my slow query. Can you help me optimize it?"

```sql
EXPLAIN SELECT o.*, u.name 
FROM orders o 
JOIN users u ON o.user_id = u.id 
WHERE o.status = 'pending' AND o.created_at > '2025-01-01';
```

**EXPLAIN Output**:
```
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | o     | ALL  | NULL          | NULL | NULL    | NULL | 5000 | Using where |
|  1 | SIMPLE      | u     | ref  | PRIMARY       | PRIMARY | 4   | o.user_id | 1    |             |
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
```

**Analysis**:
- ⚠️ **Issue 1**: Full table scan on `orders` (type: ALL, rows: 5000)
- ⚠️ **Issue 2**: No index on `status` or `created_at` columns
- ✅ **Good**: Efficient JOIN on `users` using PRIMARY key

**Recommendations**:
```sql
-- Create composite index for WHERE clause
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- After creating index, EXPLAIN shows:
-- type: range (instead of ALL)
-- rows: 150 (instead of 5000)
-- 97% reduction in rows scanned!
```

#### Example 2: Optimizing Complex JOIN

**User request**: "My query with multiple JOINs is very slow. What could be the problem?"

**Original Query**:
```sql
SELECT p.*, c.name as category, u.name as author
FROM posts p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN users u ON p.user_id = u.id
WHERE p.published = 1
ORDER BY p.created_at DESC
LIMIT 20;
```

**Analysis**:
1. Check if foreign keys (`category_id`, `user_id`) are indexed
2. Verify `published` column has index
3. Check if `created_at` is indexed for ORDER BY

**Recommendations**:
```sql
-- Add indexes for JOIN and WHERE
CREATE INDEX idx_posts_published ON posts(published);
CREATE INDEX idx_posts_category ON posts(category_id);
CREATE INDEX idx_posts_user ON posts(user_id);

-- Add compound index for WHERE + ORDER BY
CREATE INDEX idx_posts_pub_created ON posts(published, created_at DESC);
```

#### Example 3: Fixing N+1 Query Problem

**User request**: "My application is making too many queries. How do I fix this?"

**Problem**:
```python
# N+1 Problem: 1 query + N queries (if 100 posts = 101 queries!)
posts = Post.all()  # 1 query
for post in posts:
    print(post.author.name)  # N queries (1 per post)
```

**Solution**:
```python
# Use eager loading: Only 2 queries total
posts = Post.select_related('author').all()  # 1 query with JOIN
for post in posts:
    print(post.author.name)  # No additional queries!
```

### Query Optimization Techniques

**1. Use Proper Indexes**
```sql
-- Before: Full table scan
SELECT * FROM orders WHERE customer_id = 123;

-- After: Index seek
CREATE INDEX idx_customer ON orders(customer_id);
```

**2. Avoid SELECT ***
```sql
-- ❌ Bad: Retrieves all columns (slower)
SELECT * FROM users WHERE id = 1;

-- ✅ Good: Only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

**3. Use LIMIT for Large Results**
```sql
-- ❌ Bad: Returns millions of rows
SELECT * FROM logs WHERE created_at > '2025-01-01';

-- ✅ Good: Paginate results
SELECT * FROM logs WHERE created_at > '2025-01-01' LIMIT 1000 OFFSET 0;
```

**4. Optimize Subqueries**
```sql
-- ❌ Bad: Correlated subquery (runs N times)
SELECT * FROM users WHERE id IN (
    SELECT DISTINCT user_id FROM orders WHERE total > 1000
);

-- ✅ Good: JOIN (runs once)
SELECT DISTINCT u.* 
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE o.total > 1000;
```

**5. Use EXPLAIN to Verify**
```sql
-- Always verify your optimization
EXPLAIN SELECT ...;

-- Look for:
-- - type: Should be 'ref' or 'range', not 'ALL'
-- - rows: Lower is better
-- - Extra: Avoid 'Using filesort' or 'Using temporary'
```

---

## Common Performance Bottlenecks

### 1. Missing Indexes
**Symptom**: Full table scans (EXPLAIN shows type: ALL)  
**Solution**: Create indexes on WHERE, JOIN, and ORDER BY columns

### 2. Inefficient JOINs
**Symptom**: Large number of rows examined  
**Solution**: Ensure foreign keys are indexed, use proper JOIN types

### 3. N+1 Queries
**Symptom**: Multiple queries in loops  
**Solution**: Use eager loading (JOIN, select_related, includes)

### 4. Large Result Sets
**Symptom**: Slow queries returning thousands of rows  
**Solution**: Implement pagination with LIMIT/OFFSET or cursors

### 5. Complex Subqueries
**Symptom**: Nested queries causing multiple table scans  
**Solution**: Rewrite as JOINs or CTEs (Common Table Expressions)

### 6. Unused Indexes
**Symptom**: Slow writes, wasted storage  
**Solution**: Identify and remove indexes with zero usage

### 7. Missing Query Cache
**Symptom**: Repeated identical queries  
**Solution**: Implement application-level caching (Redis, Memcached)

---

## Performance Analysis Tools

### PostgreSQL
```sql
-- Enable query timing
\timing on

-- Analyze query plan
EXPLAIN ANALYZE SELECT ...;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### MySQL
```sql
-- Enable profiling
SET profiling = 1;

-- Run query
SELECT ...;

-- Show profile
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- Check unused indexes
SELECT * FROM sys.schema_unused_indexes;
```

### SQL Server
```sql
-- Show execution plan
SET SHOWPLAN_ALL ON;
GO
SELECT ...;
GO

-- Find missing indexes
SELECT * FROM sys.dm_db_missing_index_details;

-- Find unused indexes
SELECT * FROM sys.dm_db_index_usage_stats
WHERE user_seeks = 0 AND user_scans = 0;
```

---

## Best Practices Summary

### Index Management
- ✅ Index WHERE, JOIN, ORDER BY columns
- ✅ Use composite indexes for multi-column queries
- ✅ Monitor index usage regularly
- ✅ Remove unused indexes
- ❌ Don't over-index (slows writes)
- ❌ Don't index low-cardinality columns

### Query Optimization
- ✅ Use EXPLAIN to analyze queries
- ✅ Avoid SELECT * (fetch only needed columns)
- ✅ Use LIMIT for pagination
- ✅ Optimize JOINs with proper indexes
- ✅ Implement eager loading to avoid N+1
- ❌ Don't use correlated subqueries
- ❌ Don't forget to test optimizations

### Performance Monitoring
- ✅ Track slow query logs
- ✅ Monitor database metrics (CPU, I/O, memory)
- ✅ Set up alerts for slow queries
- ✅ Review query performance regularly
- ✅ Benchmark before and after changes

---

## Integration with Other Tools

- **Database Monitoring**: Integrate with New Relic, Datadog, or AppDynamics
- **Query Logging**: Use slow query logs to identify problematic queries
- **Schema Design**: Combine with schema design tools for optimal table structure
- **ORM Integration**: Work with ORMs to understand generated queries
- **Load Testing**: Use with load testing tools to find performance limits

---

**Remember**: Database performance is iterative. Measure, optimize, and verify improvements with EXPLAIN and real-world metrics.
