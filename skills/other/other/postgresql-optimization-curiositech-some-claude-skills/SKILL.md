---
name: postgresql-optimization
description: Expert in PostgreSQL performance tuning, query optimization, and database administration. Specializes in EXPLAIN analysis, indexing strategies, connection pooling, partitioning, and production-grade PostgreSQL operations.
version: 1.0.0
category: database
tags: [postgresql, sql, performance, indexing, query-optimization, database]
---

# PostgreSQL Optimization

## Overview

Expert in PostgreSQL performance tuning, query optimization, and database administration. Specializes in EXPLAIN analysis, indexing strategies, connection pooling, partitioning, and production-grade PostgreSQL operations.

## When to Use

- Diagnosing slow queries with EXPLAIN ANALYZE
- Creating optimal indexes for query patterns
- Designing database schemas for performance
- Configuring PostgreSQL for production workloads
- Implementing connection pooling (PgBouncer, Supavisor)
- Setting up partitioning for large tables
- Analyzing and reducing lock contention
- Migrating or upgrading PostgreSQL versions

## Capabilities

### Query Optimization
- EXPLAIN / EXPLAIN ANALYZE interpretation
- Query plan analysis and optimization
- Identifying sequential scans vs index scans
- Join optimization and query rewriting
- CTE vs subquery performance trade-offs
- Window function optimization

### Indexing Strategies
- B-tree, GIN, GiST, BRIN index selection
- Partial indexes for filtered queries
- Expression indexes for computed values
- Covering indexes (INCLUDE clause)
- Index-only scans optimization
- Concurrent index creation

### Schema Design
- Normalization vs denormalization trade-offs
- JSONB column design and indexing
- Array columns and operations
- Enum types vs lookup tables
- Foreign key cascade strategies
- Table inheritance and partitioning

### Configuration Tuning
- Memory settings (shared_buffers, work_mem, effective_cache_size)
- Connection limits and pooling
- WAL and checkpoint tuning
- Autovacuum configuration
- Statistics collection settings

### Advanced Features
- Partitioning (range, list, hash)
- Materialized views with refresh strategies
- Full-text search with tsvector/tsquery
- PostGIS geospatial queries
- Logical replication setup
- pg_stat_statements analysis

## Dependencies

Works well with:
- `database-modeler` - Schema design and ERD creation
- `data-pipeline-engineer` - ETL and data processing
- `site-reliability-engineer` - Database monitoring and alerting
- `nextjs-app-router-expert` - Full-stack data fetching

## Examples

### Reading EXPLAIN ANALYZE Output
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id;

-- Key metrics to look for:
-- - "Seq Scan" on large tables → needs index
-- - "Rows Removed by Filter" high → filter before join
-- - "Sort Method: external merge" → increase work_mem
-- - "Buffers: shared hit" vs "shared read" → cache efficiency
```

### Creating Effective Indexes
```sql
-- Basic B-tree for equality and range queries
CREATE INDEX CONCURRENTLY idx_orders_user_created
ON orders (user_id, created_at DESC);

-- Partial index for common filter
CREATE INDEX CONCURRENTLY idx_orders_pending
ON orders (created_at)
WHERE status = 'pending';

-- GIN index for JSONB containment queries
CREATE INDEX CONCURRENTLY idx_products_metadata
ON products USING GIN (metadata jsonb_path_ops);

-- Covering index to enable index-only scans
CREATE INDEX CONCURRENTLY idx_users_email_covering
ON users (email) INCLUDE (name, created_at);

-- Expression index for case-insensitive search
CREATE INDEX CONCURRENTLY idx_users_email_lower
ON users (LOWER(email));
```

### Optimizing N+1 Queries
```sql
-- BAD: N+1 pattern (1 + N queries)
SELECT * FROM posts WHERE user_id = $1;
-- Then for each post: SELECT * FROM comments WHERE post_id = $1;

-- GOOD: Single query with lateral join
SELECT p.*, c.comments
FROM posts p
LEFT JOIN LATERAL (
  SELECT json_agg(c.*) as comments
  FROM comments c
  WHERE c.post_id = p.id
) c ON true
WHERE p.user_id = $1;

-- GOOD: Window function for aggregates
SELECT
  p.*,
  COUNT(*) OVER (PARTITION BY p.user_id) as user_post_count
FROM posts p
WHERE p.user_id = $1;
```

### Table Partitioning
```sql
-- Create partitioned table by date range
CREATE TABLE events (
  id BIGSERIAL,
  event_type TEXT NOT NULL,
  payload JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE events_2024_01 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Automate partition creation with pg_partman
CREATE EXTENSION pg_partman;
SELECT partman.create_parent('public.events', 'created_at', 'native', 'monthly');
```

### Connection Pooling Config (PgBouncer)
```ini
; pgbouncer.ini

[databases]
myapp = host=localhost dbname=myapp

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; Pool settings
pool_mode = transaction        ; Recommended for most apps
max_client_conn = 1000
default_pool_size = 20
reserve_pool_size = 5

; Timeouts
server_idle_timeout = 600
client_idle_timeout = 0
```

### Performance Configuration
```sql
-- Check current settings
SHOW shared_buffers;        -- ~25% of RAM
SHOW effective_cache_size;  -- ~75% of RAM
SHOW work_mem;              -- Per-operation, start small (64MB)
SHOW maintenance_work_mem;  -- For VACUUM, CREATE INDEX (512MB-1GB)

-- Recommended production settings (for 32GB RAM server)
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;  -- For SSD storage
ALTER SYSTEM SET effective_io_concurrency = 200;  -- For SSD

-- Reload configuration
SELECT pg_reload_conf();
```

### Finding Slow Queries
```sql
-- Enable pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Top 10 slowest queries by total time
SELECT
  round(total_exec_time::numeric, 2) as total_ms,
  calls,
  round(mean_exec_time::numeric, 2) as avg_ms,
  round((100 * total_exec_time / sum(total_exec_time) OVER())::numeric, 2) as pct,
  query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries with most I/O
SELECT
  round(shared_blks_read::numeric, 2) as disk_reads,
  round(shared_blks_hit::numeric, 2) as cache_hits,
  round(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2) as cache_hit_ratio,
  query
FROM pg_stat_statements
ORDER BY shared_blks_read DESC
LIMIT 10;
```

### Analyzing Table Bloat
```sql
-- Check table bloat
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size,
  pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as table_size,
  n_dead_tup,
  n_live_tup,
  round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;

-- Manual VACUUM for critical tables
VACUUM (VERBOSE, ANALYZE) orders;

-- Reclaim space (requires exclusive lock)
VACUUM FULL orders;  -- Use during maintenance window
```

## Best Practices

1. **Always use EXPLAIN ANALYZE** - Don't guess, measure actual query performance
2. **Create indexes CONCURRENTLY** - Avoid blocking writes during index creation
3. **Partial indexes for hot paths** - Index only the rows you query frequently
4. **Use connection pooling** - PgBouncer or Supavisor for production
5. **Monitor pg_stat_statements** - Track query performance over time
6. **Regular ANALYZE** - Keep statistics current for query planner
7. **Avoid SELECT *** - Only fetch columns you need
8. **Batch large updates** - Process in chunks to avoid lock contention
9. **Use prepared statements** - Reduce parsing overhead for repeated queries

## Common Pitfalls

- **Missing indexes** - Check for sequential scans on large tables
- **Over-indexing** - Too many indexes slow down writes
- **work_mem too low** - Causes disk-based sorts and hash joins
- **Connection exhaustion** - Not using connection pooling
- **Stale statistics** - Autovacuum not running frequently enough
- **Bloated tables** - Not vacuuming after large deletes/updates
- **N+1 queries** - Fetching related data in loops instead of joins
- **SELECT * everywhere** - Fetching unnecessary columns
