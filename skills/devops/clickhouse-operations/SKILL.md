---
name: clickhouse-operations
description: |
  Complete ClickHouse operations guide for DevOps and SRE teams managing production deployments.
  Provides practical guidance on monitoring essential metrics (query latency, throughput, memory, disk),
  introspecting system tables, performance analysis, scaling strategies (vertical and horizontal),
  backup/disaster recovery, tuning at query/server/table levels, and troubleshooting common issues.
  Use when diagnosing ClickHouse problems, optimizing performance, planning capacity, setting up
  monitoring, implementing backups, or managing production clusters. Includes resource management
  strategies for disk space, connections, and background operations plus production checklists.
allowed-tools: Read, Bash, Grep
---

# ClickHouse Operations & Production Management

## Table of Contents

- [Purpose](#purpose)
- [Quick Start](#quick-start)
- [Key Operations](#key-operations)
  - [Step 1: Set Up Essential Monitoring](#step-1-set-up-essential-monitoring)
  - [Step 2: Diagnose Issues Using System Tables](#step-2-diagnose-issues-using-system-tables)
  - [Step 3: Implement Vertical Scaling (Single Server)](#step-3-implement-vertical-scaling-single-server)
  - [Step 4: Implement Horizontal Scaling (Cluster)](#step-4-implement-horizontal-scaling-cluster)
  - [Step 5: Set Up Backup & Disaster Recovery](#step-5-set-up-backup--disaster-recovery)
  - [Step 6: Tune Performance at Multiple Levels](#step-6-tune-performance-at-multiple-levels)
  - [Step 7: Troubleshoot Common Issues](#step-7-troubleshoot-common-issues)
  - [Step 8: Manage Resources Effectively](#step-8-manage-resources-effectively)
  - [Step 9: Production Deployment Checklist](#step-9-production-deployment-checklist)
- [Examples](#examples)
  - [Emergency Query Memory Pressure](#example-1-emergency-query-thats-using-too-much-memory)
  - [Disk Space Crisis](#example-2-disk-space-running-out-critical)
  - [Monitoring Setup](#example-3-setting-up-monitoring-for-new-cluster)
  - [Backup Implementation](#example-4-implementing-backup-with-30-day-retention)
- [References & Resources](#references--resources)
  - [Complete Query Reference](./references/queries.md) - Diagnostic and monitoring queries
  - [Extended Troubleshooting Guide](./references/troubleshooting.md) - Root cause analysis and solutions
  - [Scaling Case Studies](./examples/scaling-case-studies.md) - Real-world scaling decisions
  - [Monitoring Setup Examples](./examples/monitoring-setup.md) - Production-ready Prometheus/Grafana configs
- [Requirements](#requirements)

## Purpose

This skill provides comprehensive operational guidance for managing ClickHouse in production environments. It covers monitoring strategies, system diagnostics, scaling approaches, backup procedures, performance tuning, troubleshooting, and resource management to help DevOps and SRE teams maintain reliable, performant ClickHouse deployments.

## Quick Start

**Monitor current cluster health in 30 seconds:**

```bash
# SSH to ClickHouse server
clickhouse-client --query "
SELECT
    formatReadableSize(total_space) as total_disk,
    formatReadableSize(free_space) as free_disk,
    round(free_space / total_space * 100, 2) as free_percent
FROM system.disks;

-- Check running queries
SELECT query_id, user, elapsed, memory_usage / 1024 / 1024 as memory_mb
FROM system.processes
LIMIT 5;

-- Check recent errors
SELECT name, value as count, last_error_time
FROM system.errors
WHERE value > 0
ORDER BY last_error_time DESC
LIMIT 5;
"
```

## Key Operations

This section walks through the 9 essential steps for managing ClickHouse in production.

### Step 1: Set Up Essential Monitoring

ClickHouse requires monitoring of 9 critical metrics. Use these queries with your monitoring system (Prometheus, Grafana, Datadog, etc.):

**Query Latency & Throughput:**
```sql
-- p95 latency (replace 0.95 for p99 = 0.99)
SELECT quantile(0.95)(query_duration_ms) as p95_latency_ms
FROM system.query_log
WHERE event_date >= today()
  AND type = 'QueryFinish'
  AND query NOT LIKE '%system.%';

-- Queries per second (current)
SELECT COUNT() / max(CAST(elapsed as Float64)) as qps
FROM system.processes
WHERE query NOT LIKE '%system.%';
```

**Insert Rate & Memory Usage:**
```sql
-- Insert throughput (rows/second)
SELECT
    table,
    SUM(rows) / SUM(CAST(query_duration_ms as Float64)) * 1000 as rows_per_second
FROM system.query_log
WHERE query LIKE 'INSERT%'
  AND type = 'QueryFinish'
  AND event_date >= today()
GROUP BY table;

-- Memory usage
SELECT
    formatReadableSize(value) as current_memory,
    formatReadableSize(80000000000) as target_limit  -- Adjust to 80% of your RAM
FROM system.metrics
WHERE metric = 'MemoryTracking';
```

**Disk Usage & Background Operations:**
```sql
-- Disk utilization
SELECT
    formatReadableSize(free_space) as free,
    formatReadableSize(total_space) as total,
    round(free_space / total_space * 100, 2) as free_percent
FROM system.disks;

-- Merge pressure (high pending merges = slow inserts)
SELECT database, table, COUNT() as parts_count
FROM system.parts
WHERE active = 1
GROUP BY database, table
HAVING parts_count > 1000
ORDER BY parts_count DESC;
```

**Alert Thresholds:**
- Query latency p95 > 5 seconds
- Insert rate drops > 20% without load change
- Free disk < 20% of total
- Active parts > 1000 per table
- Memory usage > 80% of limit
- Replication lag > 60 seconds
- Failed query rate > 1%

### Step 2: Diagnose Issues Using System Tables

When problems occur, use these targeted queries to pinpoint root causes:

**Find Slow Queries:**
```sql
-- Slowest queries (last 24 hours)
SELECT
    event_time,
    query_duration_ms,
    read_rows,
    formatReadableSize(read_bytes) as bytes_read,
    formatReadableSize(memory_usage) as peak_memory,
    query
FROM system.query_log
WHERE type = 'QueryFinish'
  AND event_date >= today() - 1
  AND query NOT LIKE '%system.%'
ORDER BY query_duration_ms DESC
LIMIT 20;
```

**Identify Problematic Queries:**
```sql
-- Most resource-intensive queries
SELECT
    query,
    COUNT() as exec_count,
    AVG(query_duration_ms) as avg_duration_ms,
    MAX(memory_usage) / 1024 / 1024 as peak_memory_mb,
    SUM(read_bytes) / 1024 / 1024 / 1024 as total_gb_read
FROM system.query_log
WHERE event_date >= today() - 7
  AND type = 'QueryFinish'
GROUP BY query
ORDER BY total_gb_read DESC
LIMIT 20;
```

**Track Failed Queries:**
```sql
-- Error breakdown
SELECT
    exception,
    COUNT() as count,
    MAX(event_time) as last_error
FROM system.query_log
WHERE type = 'ExceptionWhileProcessing'
  AND event_date >= today() - 1
GROUP BY exception
ORDER BY count DESC;
```

**Monitor Table Growth:**
```sql
-- Largest tables and growth rate
SELECT
    database,
    name as table,
    SUM(rows) as total_rows,
    formatReadableSize(SUM(bytes_on_disk)) as disk_size,
    formatReadableSize(SUM(data_compressed_bytes)) as compressed,
    round(SUM(data_uncompressed_bytes) / SUM(data_compressed_bytes), 1) as compression_ratio
FROM system.parts
WHERE active = 1
  AND database NOT IN ('system', 'information_schema')
GROUP BY database, name
ORDER BY bytes_on_disk DESC;
```

### Step 3: Implement Vertical Scaling (Single Server)

Scale up individual ClickHouse servers by increasing CPU, memory, or disk resources:

**CPU Optimization:**
```sql
-- Check current thread setting
SELECT value FROM system.settings WHERE name = 'max_threads';

-- Optimize for your hardware
SET max_threads = 16;  -- Set to CPU core count (or slightly less)

-- Permanent setting in /etc/clickhouse-server/config.xml
-- <max_threads>16</max_threads>
```

**Memory Management:**
```sql
-- Current server memory limit
SELECT value FROM system.settings WHERE name = 'max_server_memory_usage';

-- Set per-query limit (10 GB example)
SET max_memory_usage = 10000000000;

-- Production config (/etc/clickhouse-server/config.xml):
-- <max_server_memory_usage>64000000000</max_server_memory_usage>  <!-- 64 GB = 80% of 80GB RAM -->
-- <max_concurrent_queries>100</max_concurrent_queries>

-- Monitor current usage
SELECT formatReadableSize(value) as memory_usage
FROM system.metrics
WHERE metric = 'MemoryTracking';
```

**Disk I/O Tuning:**
```xml
<!-- In /etc/clickhouse-server/config.xml -->
<merge_tree>
    <!-- Enable direct I/O for large table scans -->
    <min_bytes_to_use_direct_io>10485760</min_bytes_to_use_direct_io>  <!-- 10 MB -->
</merge_tree>

<!-- Filesystem recommendations: Use NVMe SSD for best performance -->
<!-- Separate data and logs to different disks if possible -->
```

### Step 4: Implement Horizontal Scaling (Cluster)

For massive scale, distribute data across multiple nodes:

**Define Cluster Configuration:**
```xml
<!-- Add to /etc/clickhouse-server/config.xml on all nodes -->
<remote_servers>
    <production_cluster>
        <shard>
            <replica>
                <host>node1.example.com</host>
                <port>9000</port>
            </replica>
            <replica>
                <host>node2.example.com</host>
                <port>9000</port>
            </replica>
        </shard>
        <shard>
            <replica>
                <host>node3.example.com</host>
                <port>9000</port>
            </replica>
            <replica>
                <host>node4.example.com</host>
                <port>9000</port>
            </replica>
        </shard>
    </production_cluster>
</remote_servers>
```

**Create Distributed Tables:**
```sql
-- Step 1: Create local table on each shard
CREATE TABLE events_local ON CLUSTER 'production_cluster' (
    user_id UInt32,
    event_type String,
    timestamp DateTime,
    properties String
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events', '{replica}')
ORDER BY (user_id, timestamp)
PARTITION BY toDate(timestamp);

-- Step 2: Create distributed table (insert point)
CREATE TABLE events ON CLUSTER 'production_cluster' AS events_local
ENGINE = Distributed('production_cluster', default, events_local, rand());

-- Step 3: Use distributed table for inserts
INSERT INTO events VALUES (123, 'purchase', now(), '{"amount": 99.99}');

-- Step 4: Query across all shards
SELECT COUNT() as total_events FROM events;
SELECT topK(10)(event_type) FROM events;  -- Top 10 event types
```

**Monitor Cluster Health:**
```sql
-- Check replication status
SELECT
    database,
    table,
    total_replicas,
    active_replicas,
    absolute_delay
FROM system.replicas
ORDER BY absolute_delay DESC;

-- Verify all nodes responding
SELECT hostname(), version(), uptime() as uptime_seconds
FROM clusterAllReplicas('production_cluster', system.one);
```

### Step 5: Set Up Backup & Disaster Recovery

Implement automated, tested backup procedures:

**Filesystem Snapshot Strategy (Recommended for production):**
```bash
#!/bin/bash
# backup_clickhouse.sh - Daily automated backup

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/clickhouse/$BACKUP_DATE"
CH_DATA_DIR="/var/lib/clickhouse"

mkdir -p "$BACKUP_DIR"

# Optional: Stop ClickHouse for consistent backup
# sudo systemctl stop clickhouse-server

# Create backup with rsync (preserve hard links)
rsync -av --hard-links "$CH_DATA_DIR/" "$BACKUP_DIR/"

# Optional: Restart ClickHouse
# sudo systemctl start clickhouse-server

# Keep only last 30 days of backups
find /backups/clickhouse -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;

echo "Backup completed to $BACKUP_DIR"
```

**Native BACKUP Command (ClickHouse 22.8+):**
```sql
-- Backup single table
BACKUP TABLE events TO Disk('backups', 'events_' || toString(today()) || '.zip');

-- Backup entire database
BACKUP DATABASE default TO Disk('backups', 'db_' || toString(today()) || '.zip');

-- Restore table
RESTORE TABLE events FROM Disk('backups', 'events_20240115.zip');

-- Restore database
RESTORE DATABASE default FROM Disk('backups', 'db_20240115.zip');
```

**Disaster Recovery Procedure:**
```bash
#!/bin/bash
# Restore complete ClickHouse instance

set -e

NEW_SERVER="new.example.com"
BACKUP_DATE="20240115"

echo "Starting disaster recovery..."

# 1. Install ClickHouse on new server
ssh "root@$NEW_SERVER" 'apt-get update && apt-get install -y clickhouse-server clickhouse-client'

# 2. Stop ClickHouse
ssh "clickhouse@$NEW_SERVER" 'sudo systemctl stop clickhouse-server'

# 3. Restore data directory
ssh "root@$NEW_SERVER" "rsync -av /remote/backup/$BACKUP_DATE/ /var/lib/clickhouse/"

# 4. Fix permissions
ssh "root@$NEW_SERVER" 'chown -R clickhouse:clickhouse /var/lib/clickhouse'

# 5. Start ClickHouse
ssh "root@$NEW_SERVER" 'systemctl start clickhouse-server'

# 6. Verify data integrity
ssh "clickhouse@$NEW_SERVER" 'clickhouse-client --query "SELECT COUNT() FROM events"'

echo "Disaster recovery complete!"
```

**Test Backups Monthly:**
```bash
# Schedule this as a monthly cron job
0 2 1 * * /opt/scripts/test_backup_restore.sh

# Test script should:
# - Restore latest backup to test instance
# - Run sanity checks (table counts, data integrity)
# - Report success/failure to ops team
```

### Step 6: Tune Performance at Multiple Levels

**Query-Level Tuning:**
```sql
-- For analytical queries on large datasets
SET max_threads = 16;           -- Use all cores
SET max_memory_usage = 50000000000;  -- 50 GB for large aggregations
SET max_execution_time = 300;   -- 5 minutes timeout

-- For batch operations
SET async_insert = 1;           -- Queue inserts asynchronously
SET wait_for_async_insert = 0;  -- Don't wait for async confirmation

-- For complex GROUP BY operations
SET group_by_overflow_mode = 'any';  -- Switch to approximate aggregation if limit exceeded

-- Enable query results cache
SET use_query_cache = 1;
```

**Server-Level Configuration** (/etc/clickhouse-server/config.xml):
```xml
<clickhouse>
    <!-- Memory: Set to ~80% of available RAM -->
    <max_server_memory_usage>64000000000</max_server_memory_usage>

    <!-- Concurrency -->
    <max_concurrent_queries>100</max_concurrent_queries>
    <max_connections>4096</max_connections>

    <!-- Background operations (merges, mutations) -->
    <background_pool_size>16</background_pool_size>
    <background_schedule_pool_size>8</background_schedule_pool_size>

    <!-- Compression: LZ4 is fast (default), ZSTD is smaller -->
    <compression>
        <case>
            <method>lz4</method>
        </case>
    </compression>

    <!-- Network: Keep connections alive efficiently -->
    <keep_alive_timeout>3</keep_alive_timeout>
    <socket_receive_timeout_sec>300</socket_receive_timeout_sec>
    <socket_send_timeout_sec>300</socket_send_timeout_sec>

    <!-- Logging: Use warning level in production to reduce I/O -->
    <logger>
        <level>warning</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>100M</size>
        <count>10</count>
    </logger>
</clickhouse>
```

**Table-Level Optimization:**
```sql
-- Use appropriate codecs for different column types
CREATE TABLE events (
    user_id UInt32,
    timestamp DateTime CODEC(DoubleDelta, LZ4),  -- Delta encoding for timestamps
    event_type LowCardinality(String),           -- Dictionary encoding for low-cardinality
    price Decimal(10, 2) CODEC(T64, ZSTD(3)),   -- Better compression for decimals
    json_data String CODEC(ZSTD(3))              -- ZSTD for larger strings
)
ENGINE = MergeTree()
ORDER BY (user_id, timestamp)
PARTITION BY toDate(timestamp)
SETTINGS
    index_granularity = 8192,
    min_bytes_for_wide_part = 10485760,     -- 10 MB
    min_rows_for_wide_part = 100000;

-- Enable TTL for automatic data lifecycle management
ALTER TABLE events MODIFY TTL timestamp + INTERVAL 90 DAY;

-- Force optimization (merges all parts, applies TTL)
OPTIMIZE TABLE events FINAL;
```

### Step 7: Troubleshoot Common Issues

**Issue: Query Timeout (Queries killed after max_execution_time)**

Diagnosis:
```sql
SELECT query, query_duration_ms, read_rows, read_bytes / 1024 / 1024 as read_mb
FROM system.query_log
WHERE query_duration_ms > 30000  -- > 30 seconds
ORDER BY query_duration_ms DESC
LIMIT 10;
```

Solutions:
```sql
-- Option 1: Increase timeout for specific query
SET max_execution_time = 300;  -- 5 minutes
SELECT * FROM events WHERE timestamp > '2024-01-01';

-- Option 2: Add index for faster filtering
ALTER TABLE events ADD INDEX idx_timestamp timestamp TYPE minmax GRANULARITY 4;

-- Option 3: Use SAMPLE to estimate results faster
SELECT COUNT() FROM events SAMPLE 0.1;  -- Estimate from 10% of data

-- Option 4: Reduce scanned data with appropriate WHERE clauses
SELECT COUNT() FROM events WHERE timestamp >= today() - 7;  -- Last 7 days only
```

---

**Issue: Out of Memory (Memory limit exceeded errors)**

Diagnosis:
```sql
SELECT
    query_id,
    user,
    memory_usage / 1024 / 1024 as memory_mb,
    query
FROM system.processes
ORDER BY memory_usage DESC;

-- Check recent OOM errors
SELECT exception FROM system.query_log
WHERE exception LIKE '%Memory%'
  AND event_date >= today() - 1;
```

Solutions:
```sql
-- Option 1: Increase memory limit per query
SET max_memory_usage = 30000000000;  -- 30 GB (if server has capacity)

-- Option 2: Use approximate aggregations instead of exact
SELECT uniq(user_id) FROM events;       -- Faster approximate distinct count
SELECT topK(1000)(category) FROM events;  -- Top 1000 without full GROUP BY

-- Option 3: Process in smaller batches
SELECT * FROM events WHERE date = toDate(now()) LIMIT 1000000;

-- Option 4: Increase server memory limit if within hardware capacity
-- Edit config.xml: <max_server_memory_usage>128000000000</max_server_memory_usage>
```

---

**Issue: Slow Inserts (Low insert throughput)**

Diagnosis:
```sql
SELECT
    table,
    COUNT() as insert_count,
    SUM(rows) as total_rows,
    SUM(rows) / SUM(CAST(query_duration_ms as Float64)) * 1000 as rows_per_second
FROM system.query_log
WHERE query LIKE 'INSERT%'
  AND type = 'QueryFinish'
  AND event_date >= today()
GROUP BY table;

-- Check number of parts (high = slow inserts)
SELECT database, table, COUNT() as parts_count
FROM system.parts
WHERE active = 1
GROUP BY database, table
ORDER BY parts_count DESC;
```

Solutions:
```sql
-- Option 1: Increase batch size (1000 -> 100000 rows per insert)
INSERT INTO events
SELECT * FROM source_table
LIMIT 100000;  -- Larger batches = better throughput

-- Option 2: Enable async inserts for non-critical data
SET async_insert = 1;
SET wait_for_async_insert = 0;  -- Fire and forget
INSERT INTO events VALUES (row1), (row2), ...;

-- Option 3: Reduce merge pressure
ALTER TABLE events MODIFY SETTING max_parts_in_total = 10000;
SYSTEM STOP MERGES events;  -- Temporarily disable merges during bulk load
-- ... run inserts ...
SYSTEM START MERGES events;

-- Option 4: Force merge after bulk load to consolidate
OPTIMIZE TABLE events;
```

---

**Issue: High Replication Lag (Replicas behind leader)**

Diagnosis:
```sql
SELECT
    database,
    table,
    total_replicas,
    active_replicas,
    absolute_delay
FROM system.replicas
ORDER BY absolute_delay DESC;

-- On problematic replica, check queue
SELECT * FROM system.replication_queue;
```

Solutions:
```bash
# Option 1: Check network between replicas
ping replica-host
mtr replica-host  # For detailed network path analysis

# Option 2: Check ZooKeeper cluster health
echo stat | nc zookeeper-host 2181
echo mntr | nc zookeeper-host 2181

# Option 3: Force sync replica with leader
clickhouse-client --query "SYSTEM SYNC REPLICA database.table;"

# Option 4: Restart replica if stuck in queue
sudo systemctl restart clickhouse-server

# Option 5: If far behind, resync from scratch
# clickhouse-client --query "SYSTEM DROP REPLICA 'replica2' FROM ZOOKEEPER;"
```

---

**Issue: Kafka Table Not Consuming (No new data from Kafka)**

Diagnosis:
```sql
-- Check Kafka consumer status
SELECT * FROM system.kafka_consumers;

-- Check for Kafka-related errors
SELECT exception, COUNT() as count
FROM system.query_log
WHERE query LIKE '%Kafka%'
  AND exception != ''
  AND event_date >= today() - 1
GROUP BY exception;
```

Solutions:
```bash
# Option 1: Check connectivity to Kafka broker
telnet kafka-broker 9092

# Option 2: Verify consumer group exists and offsets
kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
    --group clickhouse_consumer --describe

# Option 3: Reset offsets to consume from beginning (if stuck)
kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
    --group clickhouse_consumer --reset-offsets --to-earliest \
    --topic events --execute

# Option 4: Recreate Kafka table
# clickhouse-client --query "DROP TABLE kafka_events;"
# clickhouse-client -d default < create_kafka_table.sql
```

### Step 8: Manage Resources Effectively

**Disk Space Management:**
```sql
-- Monitor disk usage
SELECT
    formatReadableSize(free_space) as free,
    formatReadableSize(total_space) as total,
    round(free_space / total_space * 100, 2) as free_percent
FROM system.disks;

-- Drop old partitions (instant, no merge)
ALTER TABLE events DROP PARTITION '202301';
ALTER TABLE events DROP PARTITION '202302';

-- Set TTL for automatic cleanup
ALTER TABLE events MODIFY TTL timestamp + INTERVAL 90 DAY;

-- Manual optimization (applies TTL, merges parts)
OPTIMIZE TABLE events FINAL;

-- Check size reduction from optimization
SELECT
    formatReadableSize(SUM(bytes_on_disk)) as disk_size,
    COUNT() as parts_count
FROM system.parts
WHERE table = 'events' AND active = 1;
```

**Connection Management:**
```sql
-- View all current connections
SELECT
    query_id,
    user,
    client_hostname,
    elapsed as elapsed_seconds,
    query
FROM system.processes
ORDER BY elapsed DESC;

-- Kill specific long-running query
KILL QUERY WHERE query_id = 'abc123';

-- Kill all queries from a user (e.g., runaway job)
KILL QUERY WHERE user = 'batch_user';

-- Persistent limit in config.xml
-- <max_connections>4096</max_connections>
```

**Background Operation Control:**
```sql
-- Check merge queue
SELECT
    database,
    table,
    elapsed,
    progress,
    num_parts,
    formatReadableSize(total_size_bytes_compressed) as size
FROM system.merges
ORDER BY elapsed DESC;

-- Pause merges temporarily (e.g., for urgent queries)
SYSTEM STOP MERGES events;

-- Resume merges
SYSTEM START MERGES events;

-- Force immediate merge
OPTIMIZE TABLE events;

-- Prevent excessive merges for new tables
CREATE TABLE events_bulk (...)
ENGINE = MergeTree()
SETTINGS
    max_parts_in_total = 10000,  -- Allow more parts before forcing merge
    parts_to_throw_insert = 20000;  -- Fail inserts at this threshold
```

### Step 9: Production Deployment Checklist

Use this before deploying ClickHouse to production:

**Pre-Deployment (Hardware & Infrastructure)**
- [ ] CPU: Minimum 8 cores, 16+ cores recommended
- [ ] Memory: 64 GB minimum, 128+ GB for production workloads
- [ ] Disk: NVMe SSD, 3x estimated data size minimum free space
- [ ] Network: < 1 ms latency between cluster nodes
- [ ] Redundancy: 3+ nodes if replication required
- [ ] ZooKeeper: 3-5 dedicated nodes for cluster coordination
- [ ] Monitoring: Prometheus/Grafana/Datadog setup ready
- [ ] Backup storage: Tested, sufficient capacity, separate location

**Configuration**
- [ ] Memory limits: `max_server_memory_usage = 80% of RAM`
- [ ] Connections: `max_connections` tuned for expected workload
- [ ] Logging: Level set to `warning` (not `trace` or `debug`)
- [ ] Compression: LZ4 configured for most tables
- [ ] TTL policies: Data lifecycle management enabled
- [ ] Authentication: users.xml configured with strong passwords
- [ ] Replication: ZooKeeper paths and cluster config validated
- [ ] Kafka: Consumer groups and topic offsets confirmed

**Operational**
- [ ] Monitoring alerts: Configured for all critical metrics
  - [ ] Query latency p95 > 5s
  - [ ] Disk free < 20%
  - [ ] Memory > 80%
  - [ ] Replication lag > 60s
  - [ ] Error rate > 1%
- [ ] Log rotation: Logrotate or equivalent configured
- [ ] Graceful shutdown: systemctl stop (not kill -9)
- [ ] Upgrades: Tested in staging, rollback plan documented
- [ ] Capacity planning: Growth projections and scaling triggers
- [ ] Disaster recovery: Documented, tested within past 90 days
- [ ] Backups: Automated, tested restore procedure verified
- [ ] Documentation: Runbooks for common operations updated

**Post-Deployment (First Week)**
- [ ] Load testing: Realistic query and insert patterns
- [ ] Monitoring validation: All alerts working correctly
- [ ] Performance baseline: Record metrics for future comparison
- [ ] Team training: Ops team familiar with alerting & runbooks
- [ ] Incident response: On-call rotation established

## Examples

### Example 1: Emergency Query That's Using Too Much Memory

You're alerted that query p95 latency has spiked. A long-running job is causing memory pressure.

```sql
-- 1. Identify the problem query
SELECT
    query_id,
    user,
    elapsed,
    memory_usage / 1024 / 1024 / 1024 as memory_gb,
    query
FROM system.processes
WHERE memory_usage > 10000000000  -- > 10 GB
ORDER BY memory_usage DESC;

-- 2. Kill it immediately if necessary
KILL QUERY WHERE query_id = 'user_batch_12345';

-- 3. Investigate what went wrong in query log
SELECT
    query_duration_ms,
    memory_usage / 1024 / 1024 / 1024 as memory_gb,
    query
FROM system.query_log
WHERE user = 'batch_user'
  AND event_date >= today()
ORDER BY event_time DESC
LIMIT 10;

-- 4. Optimize the problematic query
-- Instead of: SELECT * FROM events GROUP BY user_id, event_type, device, os, browser, location
-- Use approximate: SELECT topK(1000)(user_id) FROM events
```

### Example 2: Disk Space Running Out (Critical)

Alert: Free disk space dropped below 15%. You have 4 hours before system fails.

```sql
-- 1. Check disk space immediately
SELECT
    formatReadableSize(free_space) as free,
    formatReadableSize(total_space) as total,
    round(free_space / total_space * 100, 2) as free_percent
FROM system.disks;

-- 2. Identify largest tables
SELECT
    database,
    name as table,
    formatReadableSize(SUM(bytes_on_disk)) as size,
    COUNT() as parts_count
FROM system.parts
WHERE active = 1
  AND database NOT IN ('system', 'information_schema')
GROUP BY database, name
ORDER BY bytes_on_disk DESC
LIMIT 10;

-- 3. Drop old partitions from largest table
ALTER TABLE events DROP PARTITION '202301';
ALTER TABLE events DROP PARTITION '202302';
ALTER TABLE events DROP PARTITION '202303';

-- 4. Trigger optimization to merge parts and reduce size
OPTIMIZE TABLE events FINAL;

-- 5. Monitor recovery
SELECT formatReadableSize(free_space) as free
FROM system.disks;

-- 6. For permanent fix: add more disk capacity and adjust TTL
ALTER TABLE events MODIFY TTL timestamp + INTERVAL 90 DAY;
```

### Example 3: Setting Up Monitoring for New Cluster

You've deployed a new 3-node ClickHouse cluster and need Prometheus monitoring.

Create `clickhouse_queries.yaml` for Prometheus scraper:

```yaml
global:
  scrape_interval: 30s

scrape_configs:
  - job_name: 'clickhouse-metrics'
    static_configs:
      - targets: ['clickhouse1:9090', 'clickhouse2:9090', 'clickhouse3:9090']
      - labels: {job: 'clickhouse-cluster'}
    metrics_path: '/metrics'
```

Create monitoring queries for Grafana:
```sql
-- Dashboard: Query Latency
SELECT
    avg(query_duration_ms) as avg_latency_ms,
    quantile(0.95)(query_duration_ms) as p95_latency_ms,
    quantile(0.99)(query_duration_ms) as p99_latency_ms
FROM system.query_log
WHERE event_date >= today()
  AND type = 'QueryFinish'
  AND query NOT LIKE '%system.%';

-- Dashboard: Insert Rate
SELECT
    toStartOfMinute(event_time) as minute,
    SUM(rows) as total_rows
FROM system.query_log
WHERE query LIKE 'INSERT%'
  AND event_date >= today()
GROUP BY minute
ORDER BY minute DESC;

-- Dashboard: Replication Health
SELECT
    database,
    table,
    absolute_delay as lag_seconds,
    active_replicas,
    total_replicas
FROM system.replicas;
```

### Example 4: Implementing Backup with 30-Day Retention

Create automated daily backups that keep 30 days of history:

```bash
#!/bin/bash
# /usr/local/bin/backup_clickhouse.sh

set -e

BACKUP_DIR="/backups/clickhouse"
RETENTION_DAYS=30
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_DATE"

mkdir -p "$FULL_BACKUP_PATH"

echo "Starting ClickHouse backup at $BACKUP_DATE"

# Method 1: Using ClickHouse native backup (if ClickHouse 22.8+)
clickhouse-client << EOF
    BACKUP DATABASE default TO Disk('backups', 'db_$BACKUP_DATE.zip');
    BACKUP TABLE events TO Disk('backups', 'events_$BACKUP_DATE.zip');
EOF

# Method 2: Filesystem snapshot (alternative)
# rsync -av /var/lib/clickhouse/ "$FULL_BACKUP_PATH/"

# Cleanup old backups
find "$BACKUP_DIR" -maxdepth 1 -type d -mtime +"$RETENTION_DAYS" -exec rm -rf {} \;

# Verify backup integrity (sample check)
if [ -f "$FULL_BACKUP_PATH/.metadata" ]; then
    echo "Backup verified at $FULL_BACKUP_PATH"
else
    echo "Warning: Backup verification failed"
    exit 1
fi

echo "Backup completed successfully"
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/backup_clickhouse.sh >> /var/log/clickhouse_backup.log 2>&1

# Monthly restore test (1st of month at 3 AM)
0 3 1 * * /usr/local/bin/test_backup_restore.sh >> /var/log/clickhouse_restore_test.log 2>&1
```

## References & Resources

This skill provides comprehensive reference materials and real-world examples organized in supporting files:

### Query Reference Library
**File:** [references/queries.md](./references/queries.md)

Complete library of diagnostic, monitoring, and operational queries organized by category:
- Monitoring & diagnostics queries (real-time cluster status, query performance, error tracking)
- Performance analysis queries (insert performance, merge operations, memory usage, index effectiveness)
- Resource management queries (disk space, connections, background operations)
- Cluster operations queries (replication health, cluster-wide metrics, data consistency)
- Data lifecycle queries (TTL and retention management, partition management)
- System introspection queries (configuration, table engine information, system events)

### Troubleshooting Guide
**File:** [references/troubleshooting.md](./references/troubleshooting.md)

Extended troubleshooting guide with root cause analysis and resolution procedures for:
- Query performance issues (slow queries, wrong results)
- Resource issues (OOM killer, high CPU, disk space)
- Replication & clustering (replication lag, coordination failures)
- Data ingestion issues (slow inserts, Kafka consumer problems)
- Operational issues (unresponsive server, backup/restore failures)

### Scaling Decision Framework
**File:** [examples/scaling-case-studies.md](./examples/scaling-case-studies.md)

Real-world scaling case studies and decision trees:
- Case Study 1: Scaling for growing data volume (capacity planning)
- Case Study 2: Scaling for query performance (optimization)
- Case Study 3: Scaling for insert throughput (ingestion bottlenecks)
- Scaling decision matrix (choosing between vertical and horizontal scaling)
- 6-month scaling roadmap template

### Monitoring Setup Examples
**File:** [examples/monitoring-setup.md](./examples/monitoring-setup.md)

Production-ready monitoring implementations:
- Prometheus configuration for ClickHouse
- Grafana dashboard setup
- Alert rule examples
- Real-world monitoring patterns

## Requirements

- ClickHouse server installed and running (version 21.0+, 22.8+ for native BACKUP)
- SSH access to ClickHouse servers
- `clickhouse-client` command-line tool available
- For cluster operations: ZooKeeper 3.4+ configured
- For Kafka integration: Kafka/Redpanda brokers accessible
- Backup storage: Sufficient disk space (3x data size minimum)
- Monitoring system: Prometheus, Grafana, or Datadog for dashboards
