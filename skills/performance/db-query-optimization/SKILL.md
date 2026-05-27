---
name: Database Query Optimization
description: Comprehensive guide to optimizing database queries, understanding EXPLAIN plans, indexing strategies, and eliminating N+1 queries
---

# Database Query Optimization

## Why Query Optimization Matters

The database is often the bottleneck in modern applications. A single slow query can bring down your entire system.

### Key Impacts
- **Slow Queries = Slow Application**: Database latency directly affects user experience
- **Database is Often the Bottleneck**: CPU and memory are cheap; database I/O is expensive
- **Exponential Cost**: Unoptimized queries get exponentially slower as data grows
- **Resource Exhaustion**: Slow queries consume connections, lock tables, and block other queries
- **Cascading Failures**: One slow query can cause timeouts across your entire system

### The Golden Rule
> "Optimize for reads, not writes" (unless you're write-heavy)

Most applications are read-heavy (90% reads, 10% writes). Optimize accordingly.

---

## Query Analysis Tools

### PostgreSQL

#### 1. EXPLAIN
Shows the query execution plan without running the query.

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**Output:**
```
Seq Scan on users  (cost=0.00..35.50 rows=1 width=100)
  Filter: (email = 'test@example.com'::text)
```

#### 2. EXPLAIN ANALYZE
Runs the query and shows actual execution times.

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

**Output:**
```
Index Scan using users_email_idx on users  (cost=0.29..8.30 rows=1 width=100) (actual time=0.015..0.016 rows=1 loops=1)
  Index Cond: (email = 'test@example.com'::text)
Planning Time: 0.123 ms
Execution Time: 0.045 ms
```

#### 3. pg_stat_statements
Tracks execution statistics for all SQL statements.

**Enable:**
```sql
-- In postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

-- Create extension
CREATE EXTENSION pg_stat_statements;
```

**Query slow queries:**
```sql
SELECT 
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### MySQL

#### 1. EXPLAIN
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**Output:**
```
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | users | ALL  | NULL          | NULL | NULL    | NULL | 1000 | Using where |
+----+-------------+-------+------+---------------+------+---------+------+------+-------------+
```

#### 2. Slow Query Log
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- Log queries > 1 second
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
```

**Analyze with mysqldumpslow:**
```bash
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log
```

### MongoDB

#### 1. explain()
```javascript
db.users.find({ email: 'test@example.com' }).explain('executionStats');
```

**Output:**
```json
{
  "executionStats": {
    "executionTimeMillis": 150,
    "totalDocsExamined": 10000,
    "totalKeysExamined": 0,
    "executionStages": {
      "stage": "COLLSCAN"  // ❌ Bad: Collection scan
    }
  }
}
```

#### 2. Profiler
```javascript
// Enable profiler (level 2 = all operations)
db.setProfilingLevel(2);

// Query slow operations
db.system.profile.find({ millis: { $gt: 100 } }).sort({ ts: -1 }).limit(10);
```

### Redis

#### SLOWLOG
```bash
# Get slow commands
SLOWLOG GET 10

# Configure threshold (microseconds)
CONFIG SET slowlog-log-slower-than 10000  # 10ms
```

---

## Understanding EXPLAIN

### PostgreSQL EXPLAIN Output

#### Scan Types (Best to Worst)

1. **Index Scan** ✅ (Best)
   ```
   Index Scan using users_email_idx on users
   ```
   - Uses index to find rows
   - Fast for small result sets

2. **Index Only Scan** ✅ (Best)
   ```
   Index Only Scan using users_email_name_idx on users
   ```
   - All data in index (no table lookup needed)
   - Fastest possible

3. **Bitmap Index Scan** ⚠️ (OK)
   ```
   Bitmap Index Scan on users_created_at_idx
   ```
   - Combines multiple indexes
   - Good for medium result sets

4. **Seq Scan** ❌ (Bad for large tables)
   ```
   Seq Scan on users
   ```
   - Scans entire table
   - OK for small tables (<1000 rows)
   - Bad for large tables

#### Join Types

1. **Nested Loop** (Small datasets)
   ```
   Nested Loop
   ```
   - Good for small result sets
   - O(n × m) complexity

2. **Hash Join** (Medium datasets)
   ```
   Hash Join
   ```
   - Builds hash table in memory
   - Good for medium result sets

3. **Merge Join** (Large sorted datasets)
   ```
   Merge Join
   ```
   - Requires sorted inputs
   - Good for large result sets

#### Cost Estimates

```
Seq Scan on users  (cost=0.00..35.50 rows=1 width=100)
                          ↑      ↑      ↑       ↑
                       startup  total  estimated  row
                       cost     cost   rows       width
```

- **Startup Cost**: Cost to get first row
- **Total Cost**: Cost to get all rows
- **Rows**: Estimated number of rows
- **Width**: Average row size in bytes

**Lower cost = better**

---

## Index Fundamentals

### Index Types

#### 1. B-tree Indexes (Default, Most Common)

**Use Cases:**
- Equality (`=`)
- Range (`<`, `>`, `BETWEEN`)
- Sorting (`ORDER BY`)
- Pattern matching (`LIKE 'prefix%'`)

**Create:**
```sql
CREATE INDEX users_email_idx ON users(email);
```

#### 2. Hash Indexes (Equality Only)

**Use Cases:**
- Equality (`=`) only
- Faster than B-tree for equality

**Create:**
```sql
CREATE INDEX users_email_hash_idx ON users USING HASH (email);
```

**Limitations:**
- No range queries
- No sorting
- PostgreSQL only (MySQL doesn't support)

#### 3. GiST/GIN (Full-Text, Arrays, JSON)

**Use Cases:**
- Full-text search
- Array contains (`@>`)
- JSON queries (`@>`, `?`)

**Create:**
```sql
-- Full-text search
CREATE INDEX posts_content_gin_idx ON posts USING GIN (to_tsvector('english', content));

-- Array contains
CREATE INDEX tags_gin_idx ON posts USING GIN (tags);

-- JSON
CREATE INDEX metadata_gin_idx ON products USING GIN (metadata);
```

#### 4. Partial Indexes (Filtered)

**Use Cases:**
- Index only a subset of rows
- Smaller index size
- Faster queries on filtered data

**Create:**
```sql
-- Only index active users
CREATE INDEX users_active_email_idx ON users(email) WHERE status = 'active';
```

#### 5. Covering Indexes (Include Columns)

**Use Cases:**
- Avoid table lookups
- Index-only scans

**Create:**
```sql
-- PostgreSQL
CREATE INDEX users_email_name_idx ON users(email) INCLUDE (name);

-- MySQL (composite index)
CREATE INDEX users_email_name_idx ON users(email, name);
```

---

## When to Add Indexes

### ✅ Add Indexes For:

1. **Frequent WHERE Conditions**
   ```sql
   -- Query
   SELECT * FROM users WHERE email = 'test@example.com';
   
   -- Index
   CREATE INDEX users_email_idx ON users(email);
   ```

2. **JOIN Columns**
   ```sql
   -- Query
   SELECT * FROM orders o JOIN users u ON o.user_id = u.id;
   
   -- Index
   CREATE INDEX orders_user_id_idx ON orders(user_id);
   ```

3. **ORDER BY Columns**
   ```sql
   -- Query
   SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;
   
   -- Index
   CREATE INDEX posts_created_at_idx ON posts(created_at DESC);
   ```

4. **Foreign Keys**
   ```sql
   -- Always index foreign keys!
   CREATE INDEX orders_user_id_idx ON orders(user_id);
   ```

### ❌ Don't Add Indexes For:

1. **Write-Heavy Tables**
   - Indexes slow down INSERT, UPDATE, DELETE
   - Trade-off: Read speed vs write speed

2. **Low-Cardinality Columns**
   ```sql
   -- BAD: Only 2 unique values
   CREATE INDEX users_is_active_idx ON users(is_active);
   ```
   - Exception: Partial indexes on rare values
   ```sql
   -- GOOD: Only index inactive users (rare)
   CREATE INDEX users_inactive_idx ON users(id) WHERE is_active = false;
   ```

3. **Small Tables (<1000 rows)**
   - Seq scan is faster than index scan
   - Index overhead not worth it

4. **Columns with Functions**
   ```sql
   -- BAD: Index not used
   SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
   
   -- GOOD: Functional index
   CREATE INDEX users_email_lower_idx ON users(LOWER(email));
   ```

---

## Index Maintenance

### 1. Find Unused Indexes

**PostgreSQL:**
```sql
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE 'pg_toast%'
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Action:** Drop unused indexes
```sql
DROP INDEX users_unused_idx;
```

### 2. Find Duplicate Indexes

**PostgreSQL:**
```sql
SELECT 
  pg_size_pretty(SUM(pg_relation_size(idx))::BIGINT) AS size,
  (array_agg(idx))[1] AS idx1,
  (array_agg(idx))[2] AS idx2,
  (array_agg(idx))[3] AS idx3,
  (array_agg(idx))[4] AS idx4
FROM (
  SELECT 
    indexrelid::regclass AS idx,
    (indrelid::text ||E'\n'|| indclass::text ||E'\n'|| indkey::text ||E'\n'||
     COALESCE(indexprs::text,'')||E'\n' || COALESCE(indpred::text,'')) AS key
  FROM pg_index
) sub
GROUP BY key
HAVING COUNT(*) > 1
ORDER BY SUM(pg_relation_size(idx)) DESC;
```

### 3. Index Bloat (REINDEX)

**Check bloat:**
```sql
SELECT 
  schemaname,
  tablename,
  indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Rebuild bloated indexes:**
```sql
REINDEX INDEX CONCURRENTLY users_email_idx;
```

---

## Query Optimization Techniques

### 1. SELECT Only Needed Columns (Not SELECT *)

**Bad:**
```sql
SELECT * FROM users WHERE id = 1;
```

**Good:**
```sql
SELECT id, name, email FROM users WHERE id = 1;
```

**Why:**
- Less data transferred
- Smaller result set
- Can use covering indexes

### 2. Proper WHERE Filtering

**Bad:**
```sql
-- Fetches all rows, filters in application
SELECT * FROM users;
-- app.filter(user => user.status === 'active')
```

**Good:**
```sql
-- Filters in database
SELECT * FROM users WHERE status = 'active';
```

### 3. Avoid Functions on Indexed Columns

**Bad:**
```sql
-- Index not used
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
```

**Good:**
```sql
-- Use functional index
CREATE INDEX users_email_lower_idx ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- Or store lowercase email
SELECT * FROM users WHERE email = 'test@example.com';
```

### 4. Use EXISTS Instead of COUNT

**Bad:**
```sql
-- Counts all rows
SELECT COUNT(*) FROM orders WHERE user_id = 1;
-- if (count > 0) { ... }
```

**Good:**
```sql
-- Stops at first match
SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = 1);
```

### 5. Batch Queries (Avoid N+1)

**Bad:**
```javascript
// N+1 queries
const users = await db.users.findMany();
for (const user of users) {
  user.posts = await db.posts.findMany({ where: { userId: user.id } });
}
```

**Good:**
```javascript
// Single query with join
const users = await db.users.findMany({
  include: { posts: true }
});
```

### 6. Connection Pooling

**Bad:**
```javascript
// New connection per query
const client = new Client();
await client.connect();
await client.query('SELECT * FROM users');
await client.end();
```

**Good:**
```javascript
// Connection pool
const pool = new Pool({ max: 20 });
await pool.query('SELECT * FROM users');
```

---

## N+1 Query Problem

### The Problem

**Example:**
```javascript
// 1 query to get users
const users = await db.query('SELECT * FROM users LIMIT 10');

// N queries to get posts for each user
for (const user of users) {
  const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
  user.posts = posts;
}
// Total: 1 + 10 = 11 queries
```

**Impact:**
- 10 users = 11 queries
- 100 users = 101 queries
- 1000 users = 1001 queries

### Solutions

#### 1. JOIN

**SQL:**
```sql
SELECT 
  u.*,
  p.id AS post_id,
  p.title AS post_title,
  p.content AS post_content
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
WHERE u.id IN (1, 2, 3, 4, 5);
```

**Prisma:**
```javascript
const users = await prisma.user.findMany({
  include: { posts: true }
});
```

**SQLAlchemy:**
```python
users = db.query(User).options(joinedload(User.posts)).all()
```

#### 2. IN Clause

**SQL:**
```sql
-- 1. Get users
SELECT * FROM users LIMIT 10;

-- 2. Get all posts in one query
SELECT * FROM posts WHERE user_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
```

**JavaScript:**
```javascript
const users = await db.query('SELECT * FROM users LIMIT 10');
const userIds = users.map(u => u.id);
const posts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIds]);

// Group posts by user_id
const postsByUserId = posts.reduce((acc, post) => {
  if (!acc[post.user_id]) acc[post.user_id] = [];
  acc[post.user_id].push(post);
  return acc;
}, {});

// Attach posts to users
users.forEach(user => {
  user.posts = postsByUserId[user.id] || [];
});
```

#### 3. DataLoader (GraphQL)

**Usage:**
```javascript
const DataLoader = require('dataloader');

const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIds]);
  
  // Group by user_id
  const postsByUserId = userIds.map(id => 
    posts.filter(post => post.user_id === id)
  );
  
  return postsByUserId;
});

// Usage
const posts = await postLoader.load(userId);
```

---

## Pagination Optimization

### 1. LIMIT/OFFSET (Simple but Slow)

**Query:**
```sql
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 1000;
```

**Problem:**
- Database still scans first 1000 rows
- Slow for large offsets
- Inconsistent results if data changes

**When to Use:**
- Small datasets
- Low page numbers (< 100)

### 2. Keyset Pagination (Cursor-Based, Faster)

**Query:**
```sql
-- First page
SELECT * FROM posts ORDER BY created_at DESC, id DESC LIMIT 20;

-- Next page (using last item's created_at and id)
SELECT * FROM posts 
WHERE (created_at, id) < ('2024-01-15 10:00:00', 12345)
ORDER BY created_at DESC, id DESC 
LIMIT 20;
```

**Pros:**
- Constant time (doesn't scan skipped rows)
- Consistent results
- Scales to millions of rows

**Cons:**
- Can't jump to arbitrary page
- Requires unique, sortable column

**Implementation:**
```javascript
async function getPosts(cursor = null, limit = 20) {
  let query = 'SELECT * FROM posts';
  let params = [];
  
  if (cursor) {
    const [created_at, id] = cursor.split('_');
    query += ' WHERE (created_at, id) < (?, ?)';
    params = [created_at, id];
  }
  
  query += ' ORDER BY created_at DESC, id DESC LIMIT ?';
  params.push(limit);
  
  const posts = await db.query(query, params);
  
  const nextCursor = posts.length === limit
    ? `${posts[posts.length - 1].created_at}_${posts[posts.length - 1].id}`
    : null;
  
  return { posts, nextCursor };
}
```

### 3. Avoid COUNT(*) on Every Page

**Bad:**
```sql
-- Runs on every page load
SELECT COUNT(*) FROM posts;  -- Slow!
SELECT * FROM posts LIMIT 20 OFFSET 0;
```

**Good:**
```sql
-- Cache the count or estimate it
SELECT reltuples::bigint AS estimate FROM pg_class WHERE relname = 'posts';

-- Or don't show total count
SELECT * FROM posts LIMIT 20 OFFSET 0;
```

---

## Aggregate Optimization

### 1. Materialized Views

**Problem:**
```sql
-- Slow: Calculates on every request
SELECT 
  user_id,
  COUNT(*) AS post_count,
  AVG(views) AS avg_views
FROM posts
GROUP BY user_id;
```

**Solution:**
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_post_stats AS
SELECT 
  user_id,
  COUNT(*) AS post_count,
  AVG(views) AS avg_views
FROM posts
GROUP BY user_id;

-- Create index on materialized view
CREATE INDEX user_post_stats_user_id_idx ON user_post_stats(user_id);

-- Query materialized view (fast!)
SELECT * FROM user_post_stats WHERE user_id = 1;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY user_post_stats;
```

### 2. Summary Tables

**Problem:**
```sql
-- Slow: Aggregates millions of rows
SELECT 
  DATE(created_at) AS date,
  COUNT(*) AS orders,
  SUM(total) AS revenue
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at);
```

**Solution:**
```sql
-- Create summary table
CREATE TABLE daily_order_stats (
  date DATE PRIMARY KEY,
  orders INTEGER,
  revenue DECIMAL(10, 2)
);

-- Populate with trigger or cron job
INSERT INTO daily_order_stats (date, orders, revenue)
SELECT 
  DATE(created_at),
  COUNT(*),
  SUM(total)
FROM orders
WHERE DATE(created_at) = CURRENT_DATE
GROUP BY DATE(created_at)
ON CONFLICT (date) DO UPDATE SET
  orders = EXCLUDED.orders,
  revenue = EXCLUDED.revenue;

-- Query summary table (fast!)
SELECT * FROM daily_order_stats WHERE date >= '2024-01-01';
```

### 3. Pre-Computed Aggregates

**Problem:**
```sql
-- Slow: Counts on every request
SELECT COUNT(*) FROM posts WHERE user_id = 1;
```

**Solution:**
```sql
-- Add post_count column to users table
ALTER TABLE users ADD COLUMN post_count INTEGER DEFAULT 0;

-- Update with trigger
CREATE OR REPLACE FUNCTION update_user_post_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE users SET post_count = post_count + 1 WHERE id = NEW.user_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE users SET post_count = post_count - 1 WHERE id = OLD.user_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_post_count_trigger
AFTER INSERT OR DELETE ON posts
FOR EACH ROW EXECUTE FUNCTION update_user_post_count();

-- Query (instant!)
SELECT post_count FROM users WHERE id = 1;
```

---

## PostgreSQL Specific

### 1. Parallel Queries

**Enable:**
```sql
SET max_parallel_workers_per_gather = 4;
```

**Check if query uses parallelism:**
```sql
EXPLAIN SELECT COUNT(*) FROM large_table;
-- Look for "Parallel Seq Scan"
```

### 2. Partitioning

**Range Partitioning:**
```sql
-- Create partitioned table
CREATE TABLE orders (
  id SERIAL,
  user_id INTEGER,
  created_at TIMESTAMP,
  total DECIMAL(10, 2)
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Queries automatically use correct partition
SELECT * FROM orders WHERE created_at >= '2024-01-15';
```

**Benefits:**
- Faster queries (scans only relevant partitions)
- Easier maintenance (drop old partitions)
- Better vacuum performance

### 3. Extensions

**pg_trgm (Fuzzy Search):**
```sql
CREATE EXTENSION pg_trgm;

-- Create GIN index for fuzzy search
CREATE INDEX users_name_trgm_idx ON users USING GIN (name gin_trgm_ops);

-- Fuzzy search
SELECT * FROM users WHERE name % 'jhon';  -- Finds "John"
```

---

## MongoDB Specific

### 1. Compound Indexes

**Query:**
```javascript
db.users.find({ status: 'active', created_at: { $gte: ISODate('2024-01-01') } });
```

**Index:**
```javascript
db.users.createIndex({ status: 1, created_at: -1 });
```

**Index Prefix Rule:**
- Index on `{a: 1, b: 1, c: 1}` supports queries on:
  - `{a: 1}`
  - `{a: 1, b: 1}`
  - `{a: 1, b: 1, c: 1}`
- But NOT `{b: 1}` or `{c: 1}`

### 2. Covered Queries

**Query:**
```javascript
db.users.find(
  { email: 'test@example.com' },
  { _id: 0, name: 1, email: 1 }  // Projection
);
```

**Index:**
```javascript
db.users.createIndex({ email: 1, name: 1 });
```

**Check if covered:**
```javascript
db.users.find(
  { email: 'test@example.com' },
  { _id: 0, name: 1, email: 1 }
).explain('executionStats');

// Look for "totalDocsExamined": 0 (covered query!)
```

### 3. Aggregation Pipeline Optimization

**Bad:**
```javascript
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $sort: { created_at: -1 } },
  { $limit: 10 }
]);
```

**Good:**
```javascript
// Add index
db.orders.createIndex({ status: 1, created_at: -1 });

// Same query, now uses index
db.orders.aggregate([
  { $match: { status: 'completed' } },
  { $sort: { created_at: -1 } },
  { $limit: 10 }
]);
```

**Tips:**
- Put `$match` first (filter early)
- Put `$limit` early (reduce data)
- Use indexes for `$match` and `$sort`

---

## Query Caching

### 1. Application-Level Cache (Redis)

**Pattern:**
```javascript
async function getUser(id) {
  // Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  // Query database
  const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  
  // Cache result
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  return user;
}
```

### 2. Database Query Cache (MySQL, Deprecated in 8.0)

**MySQL 5.7:**
```sql
SET GLOBAL query_cache_type = 1;
SET GLOBAL query_cache_size = 268435456;  -- 256MB
```

**Note:** Removed in MySQL 8.0 (use application-level caching instead)

### 3. Materialized Views (PostgreSQL)

**See "Aggregate Optimization" section above**

---

## Monitoring Query Performance

### 1. Slow Query Log

**PostgreSQL:**
```sql
-- In postgresql.conf
log_min_duration_statement = 1000  -- Log queries > 1s

-- Or set at runtime
ALTER DATABASE mydb SET log_min_duration_statement = 1000;
```

**MySQL:**
```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

### 2. pg_stat_statements

**Enable:**
```sql
CREATE EXTENSION pg_stat_statements;
```

**Find slow queries:**
```sql
SELECT 
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time,
  stddev_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 3. APM Tools

**Datadog:**
- Automatic query tracking
- Slow query detection
- EXPLAIN plan analysis

**New Relic:**
- Database monitoring
- Slow transaction traces
- Query analysis

---

## Real Optimization Examples

### Example 1: Slow JOIN Query

**Problem:**
```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id, u.name;

-- Execution Time: 5000 ms
```

**EXPLAIN Output:**
```
Hash Join  (cost=1000.00..5000.00 rows=10000 width=100) (actual time=100.000..5000.000 rows=10000 loops=1)
  Hash Cond: (p.user_id = u.id)
  ->  Seq Scan on posts p  (cost=0.00..3000.00 rows=100000 width=4)
  ->  Hash  (cost=500.00..500.00 rows=10000 width=100)
        ->  Seq Scan on users u  (cost=0.00..500.00 rows=10000 width=100)
```

**Fix:**
```sql
-- Add index on foreign key
CREATE INDEX posts_user_id_idx ON posts(user_id);

-- Re-run query
EXPLAIN ANALYZE
SELECT u.name, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id, u.name;

-- Execution Time: 50 ms (100x faster!)
```

### Example 2: Missing Index Detection

**Problem:**
```sql
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Slow: 500ms
```

**EXPLAIN:**
```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';
```

**Output:**
```
Seq Scan on orders  (cost=0.00..10000.00 rows=100 width=100) (actual time=0.100..500.000 rows=10 loops=1)
  Filter: ((user_id = 123) AND (status = 'pending'::text))
  Rows Removed by Filter: 99990
```

**Fix:**
```sql
-- Add compound index
CREATE INDEX orders_user_id_status_idx ON orders(user_id, status);

-- Re-run
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Execution Time: 2ms (250x faster!)
```

**Output:**
```
Index Scan using orders_user_id_status_idx on orders  (cost=0.29..8.30 rows=10 width=100) (actual time=0.015..2.000 rows=10 loops=1)
  Index Cond: ((user_id = 123) AND (status = 'pending'::text))
```

### Example 3: N+1 Query Elimination

**Problem:**
```javascript
// 1 + N queries
const users = await db.query('SELECT * FROM users LIMIT 10');
for (const user of users) {
  user.posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
}
// Time: 1000ms
```

**Fix:**
```javascript
// 1 query
const users = await db.query(`
  SELECT 
    u.*,
    json_agg(json_build_object('id', p.id, 'title', p.title)) AS posts
  FROM users u
  LEFT JOIN posts p ON p.user_id = u.id
  GROUP BY u.id
  LIMIT 10
`);
// Time: 50ms (20x faster!)
```

### Example 4: Pagination Improvement

**Problem:**
```sql
-- Page 1000 (offset 20000)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 20000;

-- Execution Time: 2000ms
```

**Fix:**
```sql
-- Keyset pagination
SELECT * FROM posts 
WHERE (created_at, id) < ('2024-01-15 10:00:00', 12345)
ORDER BY created_at DESC, id DESC 
LIMIT 20;

-- Execution Time: 5ms (400x faster!)
```

---

## Tools

### PostgreSQL

- **pgAdmin**: GUI for database management
- **pgBadger**: Log analyzer
- **pg_stat_statements**: Query statistics
- **EXPLAIN Visualizer**: https://explain.dalibo.com/

### MySQL

- **MySQL Workbench**: GUI for database management
- **mysqldumpslow**: Slow query log analyzer
- **Percona Toolkit**: Advanced MySQL tools

### General

- **DataGrip**: Multi-database IDE
- **DBeaver**: Open-source database tool
- **Datadog**: APM with database monitoring
- **New Relic**: APM with database monitoring

---

## Optimization Checklist

### Before Optimizing

- [ ] Identify slow queries (slow query log, APM)
- [ ] Run EXPLAIN ANALYZE
- [ ] Measure baseline performance

### Optimization Steps

- [ ] Add indexes for WHERE, JOIN, ORDER BY columns
- [ ] Eliminate N+1 queries
- [ ] Use SELECT only needed columns
- [ ] Optimize pagination (keyset vs offset)
- [ ] Add connection pooling
- [ ] Cache frequent queries
- [ ] Use materialized views for aggregates

### After Optimizing

- [ ] Run EXPLAIN ANALYZE again
- [ ] Measure new performance
- [ ] Document improvement
- [ ] Monitor for regressions

---

## Summary

### Quick Reference

**Query Analysis:**
- PostgreSQL: `EXPLAIN ANALYZE`, `pg_stat_statements`
- MySQL: `EXPLAIN`, slow query log
- MongoDB: `explain()`, profiler

**Index Types:**
- B-tree: Default, most common
- Hash: Equality only
- GIN/GiST: Full-text, arrays, JSON
- Partial: Filtered indexes
- Covering: Include columns

**Common Optimizations:**
1. Add indexes for WHERE, JOIN, ORDER BY
2. Eliminate N+1 queries (use JOINs or IN)
3. Use keyset pagination (not LIMIT/OFFSET)
4. Avoid SELECT *
5. Use connection pooling
6. Cache frequent queries
7. Use materialized views for aggregates

**Red Flags:**
- Seq Scan on large tables
- N+1 queries
- LIMIT with large OFFSET
- Functions on indexed columns
- Missing indexes on foreign keys

**Tools:**
- pgAdmin, DataGrip, DBeaver
- pg_stat_statements, slow query log
- Datadog, New Relic
