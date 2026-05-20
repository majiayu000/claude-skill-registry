---
name: database-monitoring
description: Monitor database performance and health. Use when setting up monitoring, analyzing metrics, or troubleshooting database issues.
---

# Database Monitoring

## Overview

Implement comprehensive database monitoring for performance analysis, health checks, and proactive alerting. Covers metrics collection, analysis, and troubleshooting strategies.

## When to Use

- Performance baseline establishment
- Real-time health monitoring
- Capacity planning
- Query performance analysis
- Resource utilization tracking
- Alerting rule configuration
- Incident response and troubleshooting

## PostgreSQL Monitoring

### Connection Monitoring

**PostgreSQL - Active Connections:**

```sql
-- View current connections
SELECT
  pid,
  usename,
  application_name,
  client_addr,
  state,
  query_start,
  state_change
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start DESC;

-- Count connections per database
SELECT
  datname,
  COUNT(*) as connection_count,
  MAX(EXTRACT(EPOCH FROM (NOW() - query_start))) as max_query_duration_sec
FROM pg_stat_activity
GROUP BY datname;

-- Find idle transactions
SELECT
  pid,
  usename,
  state,
  query_start,
  xact_start,
  EXTRACT(EPOCH FROM (NOW() - xact_start)) as transaction_age_sec
FROM pg_stat_activity
WHERE state = 'idle in transaction'
ORDER BY xact_start;
```

**PostgreSQL - Max Connections Configuration:**

```sql
-- Check current max_connections
SHOW max_connections;

-- Set max_connections (requires restart)
-- In postgresql.conf:
-- max_connections = 200

-- Monitor connection pool usage
SELECT
  sum(numbackends) as total_backends,
  (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_connections,
  ROUND(100.0 * sum(numbackends) /
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections'), 2) as usage_percent
FROM pg_stat_database;
```

### Query Performance Monitoring

**PostgreSQL - Query Statistics:**

```sql
-- Enable query statistics (pg_stat_statements extension)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slowest queries
SELECT
  query,
  calls,
  mean_exec_time,
  max_exec_time,
  total_exec_time
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Top queries by total execution time
SELECT
  SUBSTRING(query, 1, 50) as query_snippet,
  calls,
  ROUND(total_exec_time::NUMERIC, 2) as total_time_ms,
  ROUND(mean_exec_time::NUMERIC, 2) as avg_time_ms,
  ROUND(stddev_exec_time::NUMERIC, 2) as stddev_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

**PostgreSQL - Long Running Queries:**

```sql
-- Find queries running longer than 1 minute
SELECT
  pid,
  usename,
  application_name,
  state,
  query,
  EXTRACT(EPOCH FROM (NOW() - query_start)) as duration_seconds
FROM pg_stat_activity
WHERE (NOW() - query_start) > INTERVAL '1 minute'
ORDER BY query_start;

-- Cancel long-running query
SELECT pg_cancel_backend(pid);

-- Terminate stuck query
SELECT pg_terminate_backend(pid);
```

### Table & Index Monitoring

**PostgreSQL - Table Statistics:**

```sql
-- Table size analysis
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
  ROUND(100.0 * pg_total_relation_size(schemaname||'.'||tablename) /
    (SELECT pg_database_size(current_database()))::NUMERIC, 2) as percent_of_db
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Table row counts and dead tuples
SELECT
  schemaname,
  tablename,
  n_live_tup,
  n_dead_tup,
  ROUND(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2) as dead_percent
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Trigger VACUUM when dead tuples exceed threshold
-- Tables with > 20% dead tuples need VACUUM
SELECT
  schemaname,
  tablename,
  ROUND(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2) as dead_percent
FROM pg_stat_user_tables
WHERE n_dead_tup > n_live_tup * 0.2;
```

**PostgreSQL - Index Monitoring:**

```sql
-- Unused indexes (never scanned)
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index fragmentation
SELECT
  schemaname,
  tablename,
  indexname,
  ROUND(100.0 * (pg_relation_size(indexrelid) -
    pg_relation_size(indexrelid, 'main')) /
    pg_relation_size(indexrelid), 2) as fragmentation_percent
FROM pg_stat_user_indexes
WHERE pg_relation_size(indexrelid) > 1000000
ORDER BY fragmentation_percent DESC;

-- Rebuild fragmented indexes
REINDEX INDEX CONCURRENTLY idx_name;
```

## MySQL Monitoring

### Performance Schema

**MySQL - Query Statistics:**

```sql
-- Enable performance schema
-- In my.cnf: performance_schema = ON

-- Slowest queries
SELECT
  object_schema,
  object_name,
  COUNT_STAR,
  SUM_TIMER_WAIT / 1000000000000 as total_time_sec,
  AVG_TIMER_WAIT / 1000000000 as avg_time_ms
FROM performance_schema.table_io_waits_summary_by_table_io_type
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;

-- Query response time plugin
SELECT
  TIME,
  COUNT,
  TOTAL,
  ERRORS
FROM mysql.query_response_time
ORDER BY TIME DESC;
```

**MySQL - Connection Monitoring:**

```sql
-- Current connections
SHOW PROCESSLIST;

-- Enhanced processlist
SELECT
  ID,
  USER,
  HOST,
  DB,
  COMMAND,
  TIME,
  STATE,
  INFO
FROM INFORMATION_SCHEMA.PROCESSLIST
WHERE STATE != 'Sleep'
ORDER BY TIME DESC;

-- Kill long-running query
KILL QUERY process_id;
KILL CONNECTION process_id;

-- Max connections usage
SHOW STATUS LIKE 'Threads%';
SHOW STATUS LIKE 'Max_used_connections';
```

### InnoDB Monitoring

**MySQL - InnoDB Buffer Pool:**

```sql
-- Buffer pool statistics
SHOW STATUS LIKE 'Innodb_buffer_pool%';

-- Calculate hit ratio
-- (Innodb_buffer_pool_read_requests - Innodb_buffer_pool_reads) /
-- Innodb_buffer_pool_read_requests

-- View InnoDB transactions
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX
ORDER BY trx_started DESC;

-- View InnoDB locks
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;

-- Monitor InnoDB pages
SHOW STATUS LIKE 'Innodb_pages%';
```

**MySQL - Table and Index Statistics:**

```sql
-- Table statistics
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) as Size_MB,
  TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA != 'information_schema'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- Index cardinality
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  SEQ_IN_INDEX,
  CARDINALITY
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'your_database'
ORDER BY TABLE_NAME, SEQ_IN_INDEX;
```

## Real-Time Monitoring Tools

### PostgreSQL Monitoring Setup

**PostgreSQL with Prometheus:**

```yaml
# prometheus.yml configuration
scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']

# Using postgres_exporter
# Download and run:
# ./postgres_exporter --web.listen-address=:9187
```

**Custom Monitoring Query:**

```sql
-- Create monitoring function
CREATE OR REPLACE FUNCTION get_database_metrics()
RETURNS TABLE (
  metric_name VARCHAR,
  metric_value NUMERIC,
  collected_at TIMESTAMP
) AS $$
BEGIN
  -- Return various metrics
  RETURN QUERY
  SELECT 'connections'::VARCHAR,
    (SELECT count(*) FROM pg_stat_activity)::NUMERIC,
    NOW();

  RETURN QUERY
  SELECT 'transactions_per_second',
    (SELECT sum(xact_commit + xact_rollback) / 60 FROM pg_stat_database)::NUMERIC,
    NOW();

  RETURN QUERY
  SELECT 'cache_hit_ratio',
    ROUND(100.0 * (1 - (
      (SELECT sum(heap_blks_read) FROM pg_statio_user_tables)::FLOAT /
      ((SELECT sum(heap_blks_read + heap_blks_hit) FROM pg_statio_user_tables)::FLOAT)
    )), 2)::NUMERIC,
    NOW();
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_database_metrics();
```

### Automated Monitoring Dashboard

```sql
-- Create monitoring table
CREATE TABLE database_metrics_history (
  collected_at TIMESTAMP,
  metric_name VARCHAR(100),
  metric_value NUMERIC,
  PRIMARY KEY (collected_at, metric_name)
);

-- Function to collect metrics
CREATE OR REPLACE FUNCTION collect_metrics()
RETURNS void AS $$
BEGIN
  INSERT INTO database_metrics_history (collected_at, metric_name, metric_value)
  SELECT
    NOW(),
    'active_connections',
    (SELECT count(*) FROM pg_stat_activity WHERE state != 'idle')::NUMERIC
  UNION ALL
  SELECT
    NOW(),
    'cache_hit_ratio',
    ROUND(100.0 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)), 2)
  FROM pg_statio_user_tables
  UNION ALL
  SELECT
    NOW(),
    'database_size_mb',
    pg_database_size(current_database())::NUMERIC / 1024 / 1024
  UNION ALL
  SELECT
    NOW(),
    'table_bloat_percent',
    ROUND(100.0 * sum(n_dead_tup) / sum(n_live_tup + n_dead_tup), 2)
  FROM pg_stat_user_tables;
END;
$$ LANGUAGE plpgsql;

-- Schedule via cron
-- SELECT cron.schedule('collect_metrics', '* * * * *', 'SELECT collect_metrics()');
```

## Health Checks

**PostgreSQL - Health Check Function:**

```sql
CREATE OR REPLACE FUNCTION database_health_check()
RETURNS TABLE (
  check_name VARCHAR,
  status VARCHAR,
  details VARCHAR
) AS $$
BEGIN
  -- Check connections
  RETURN QUERY
  SELECT
    'connections'::VARCHAR,
    CASE WHEN (SELECT count(*) FROM pg_stat_activity)::INT /
      (SELECT setting::INT FROM pg_settings WHERE name = 'max_connections')::FLOAT > 0.8
      THEN 'WARNING' ELSE 'OK' END,
    'Active connections: ' || (SELECT count(*) FROM pg_stat_activity)::TEXT;

  -- Check cache hit ratio
  RETURN QUERY
  SELECT
    'cache_hit_ratio',
    CASE WHEN 100.0 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) < 90
      THEN 'WARNING' ELSE 'OK' END,
    'Cache hit ratio: ' ||
      ROUND(100.0 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)), 2)::TEXT
  FROM pg_statio_user_tables;

  -- Check transaction wraparound
  RETURN QUERY
  SELECT
    'transaction_wraparound'::VARCHAR,
    CASE WHEN min(age(datfrozenxid)) > 10000000
      THEN 'CRITICAL' ELSE 'OK' END,
    'Oldest transaction age: ' || min(age(datfrozenxid))::TEXT
  FROM pg_database;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM database_health_check();
```

## Alerting Rules

**Common Alert Conditions:**

```
1. High Connection Usage (>80% of max_connections)
2. Query execution time exceeds threshold (>5 seconds)
3. Cache hit ratio below 90%
4. Table bloat percentage > 20%
5. Replication lag > 1 minute
6. Disk space usage > 80%
7. Long-running transactions (>30 minutes)
8. Index bloat percentage > 30%
```

## Performance Tuning Metrics

**PostgreSQL - Key Metrics to Monitor:**

```sql
-- Cache hit ratio (should be > 99%)
SELECT
  sum(heap_blks_hit)::FLOAT / (sum(heap_blks_hit) + sum(heap_blks_read)) as cache_hit_ratio
FROM pg_statio_user_tables;

-- Transactions per second
SELECT
  sum(xact_commit + xact_rollback) / 60 as txns_per_sec
FROM pg_stat_database;

-- Index usage ratio
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## Troubleshooting Guide

**PostgreSQL - Slow Query Diagnosis:**

```sql
-- 1. Check query plan
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- 2. Check indexes
SELECT * FROM pg_stat_user_indexes WHERE tablename = 'orders';

-- 3. Update statistics
ANALYZE orders;

-- 4. Check table bloat
SELECT n_dead_tup, n_live_tup FROM pg_stat_user_tables WHERE relname = 'orders';

-- 5. Run VACUUM if needed
VACUUM ANALYZE orders;
```

## Best Practices

✅ DO monitor key performance indicators (KPIs)
✅ DO set up alerts for critical metrics
✅ DO baseline performance regularly
✅ DO investigate anomalies promptly
✅ DO maintain monitoring history
✅ DO test alerting rules
✅ DO document alerting procedures

❌ DON'T ignore warnings
❌ DON'T skip baseline measurements
❌ DON'T set overly sensitive alert thresholds
❌ DON'T monitor without taking action
❌ DON'T forget about disk space

## Resources

- [PostgreSQL Monitoring Documentation](https://www.postgresql.org/docs/current/monitoring.html)
- [MySQL Monitoring](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html)
- [pg_stat_statements Extension](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [Prometheus PostgreSQL Exporter](https://github.com/prometheus-community/postgres_exporter)
- [Grafana Database Dashboards](https://grafana.com/grafana/dashboards)
