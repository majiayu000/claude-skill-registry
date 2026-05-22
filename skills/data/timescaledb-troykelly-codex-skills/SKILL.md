---
name: timescaledb
description: MANDATORY when working with time-series data, hypertables, continuous aggregates, or compression - enforces TimescaleDB 2.24.0 best practices including lightning-fast recompression, UUIDv7 continuous aggregates, and Direct Compress
---

# TimescaleDB 2.24.0 Time-Series Database

## Overview

TimescaleDB 2.24.0 introduces transformational features: lightning-fast recompression (100x faster updates), Direct Compress integration with continuous aggregates, UUIDv7 support in aggregates, and bloom filter sparse index changes. This skill ensures you leverage these capabilities correctly.

**Core principle:** Time-series data has unique access patterns. Design for append-heavy, time-range queries from the start.

**Announce at start:** "I'm applying timescaledb to ensure TimescaleDB 2.24.0 best practices."

## When This Skill Applies

This skill is MANDATORY when ANY of these patterns are touched:

| Pattern | Examples |
|---------|----------|
| `**/*hypertable*` | migrations/create_hypertable.sql |
| `**/*timeseries*` | models/timeseries.ts |
| `**/*metrics*` | services/metricsService.ts |
| `**/*events*` | db/events.sql |
| `**/*logs*` | tables/logs.sql |
| `**/*sensor*` | iot/sensor_data.sql |
| `**/*continuous_agg*` | views/hourly_stats.sql |
| `**/*compression*` | policies/compression.sql |

Or when files contain:

```sql
-- These patterns trigger this skill
create_hypertable
continuous aggregate
compress_chunk
add_compression_policy
```

## TimescaleDB 2.24.0 Features

### 1. Lightning-Fast Recompression

TimescaleDB 2.24.0 introduces `recompress := true` for dramatically faster updates to compressed data:

```sql
-- OLD (2.23 and earlier): Decompress entire chunk, update, recompress
-- Could take minutes for large chunks

-- NEW (2.24.0): Update compressed data directly
UPDATE sensor_data
SET value = corrected_value
WHERE time BETWEEN '2026-01-01' AND '2026-01-02';
-- 100x faster for compressed chunks

-- Enable recompression mode (automatic in 2.24.0)
-- Updates to compressed chunks now:
-- 1. Identify affected segments
-- 2. Decompress only those segments
-- 3. Apply updates
-- 4. Recompress immediately

-- Verify recompression is happening
SELECT * FROM timescaledb_information.job_stats
WHERE job_id IN (
  SELECT job_id FROM timescaledb_information.jobs
  WHERE proc_name = 'policy_recompression'
);
```

**When this matters:**
- Late-arriving data corrections
- Backfill operations
- Data quality fixes
- Retroactive updates

### 2. Direct Compress with Continuous Aggregates

Continuous aggregates can now compress directly without materialized hypertable overhead:

```sql
-- Create continuous aggregate with direct compression
CREATE MATERIALIZED VIEW hourly_metrics
WITH (timescaledb.continuous, timescaledb.compress = true) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  device_id,
  avg(temperature) AS avg_temp,
  min(temperature) AS min_temp,
  max(temperature) AS max_temp,
  count(*) AS sample_count
FROM sensor_readings
GROUP BY bucket, device_id
WITH NO DATA;

-- Add compression policy directly to continuous aggregate
SELECT add_compression_policy('hourly_metrics', INTERVAL '7 days');

-- Refresh policy
SELECT add_continuous_aggregate_policy('hourly_metrics',
  start_offset => INTERVAL '1 month',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);
```

**Benefits:**
- No intermediate materialized hypertable
- Automatic compression of aggregate data
- Reduced storage for historical aggregates
- Simpler management

### 3. UUIDv7 in Continuous Aggregates

TimescaleDB 2.24.0 supports PostgreSQL 18's native UUIDv7 in continuous aggregates:

```sql
-- Hypertable with UUIDv7 primary key (PostgreSQL 18)
CREATE TABLE events (
  id uuid DEFAULT uuidv7(),
  time timestamptz NOT NULL,
  event_type text NOT NULL,
  payload jsonb,
  PRIMARY KEY (id, time)
);

SELECT create_hypertable('events', 'time');

-- Continuous aggregate can now reference UUIDv7 columns
CREATE MATERIALIZED VIEW event_counts
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  event_type,
  count(*) AS event_count,
  count(DISTINCT id) AS unique_events  -- UUIDv7 works here now
FROM events
GROUP BY bucket, event_type
WITH NO DATA;
```

### 4. Bloom Filter Sparse Index Changes

TimescaleDB 2.24.0 modifies bloom filter behavior for sparse indexes:

```sql
-- Bloom filters for sparse data patterns
-- Useful for columns with many NULLs or low cardinality

CREATE TABLE logs (
  time timestamptz NOT NULL,
  level text,
  message text,
  error_code text,  -- Often NULL, sparse
  trace_id uuid     -- Often NULL, sparse
);

SELECT create_hypertable('logs', 'time');

-- Configure compression with bloom filter for sparse columns
ALTER TABLE logs SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'level',
  timescaledb.compress_orderby = 'time DESC',
  -- Bloom filter helps find rare non-NULL values
  timescaledb.compress_bloomfilter = 'error_code, trace_id'
);

-- Query efficiency: Bloom filter skips segments without matches
SELECT * FROM logs
WHERE error_code = 'E500'
  AND time > now() - INTERVAL '1 day';
-- Scans only segments where bloom filter indicates possible match
```

**When to use bloom filters:**
- Sparse columns (many NULLs)
- Rare value queries (finding errors in logs)
- High-cardinality exact match queries
- NOT useful for range queries

## Hypertable Design

### Creating Hypertables

```sql
-- Standard time-series table
CREATE TABLE metrics (
  time timestamptz NOT NULL,
  device_id uuid NOT NULL,
  metric_name text NOT NULL,
  value double precision,
  metadata jsonb DEFAULT '{}'
);

-- Convert to hypertable
SELECT create_hypertable('metrics', 'time',
  chunk_time_interval => INTERVAL '1 day',  -- Chunk size
  create_default_indexes => true
);

-- With space partitioning (for high-cardinality dimensions)
SELECT create_hypertable('metrics', 'time',
  partitioning_column => 'device_id',
  number_partitions => 4,
  chunk_time_interval => INTERVAL '1 day'
);
```

### Chunk Interval Selection

| Data Volume | Suggested Interval | Rationale |
|-------------|-------------------|-----------|
| < 1GB/day | 1 week | Fewer chunks, simpler management |
| 1-10 GB/day | 1 day | Balance between size and granularity |
| 10-100 GB/day | 6 hours | Faster compression, better parallelism |
| > 100 GB/day | 1 hour | Maximum parallelism, fast drops |

```sql
-- Adjust chunk interval
SELECT set_chunk_time_interval('metrics', INTERVAL '6 hours');

-- View current chunks
SELECT show_chunks('metrics', older_than => INTERVAL '1 day');
```

### Primary Key Design

```sql
-- CORRECT: Time column in primary key for efficient chunk pruning
CREATE TABLE events (
  id uuid DEFAULT uuidv7(),
  time timestamptz NOT NULL,
  event_type text NOT NULL,
  PRIMARY KEY (id, time)  -- time included
);

-- WRONG: Time not in primary key (inefficient queries)
CREATE TABLE events_bad (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  time timestamptz NOT NULL  -- Not in PK
);
```

## Compression Strategy

### Enabling Compression

```sql
-- Configure compression
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',      -- Group by this
  timescaledb.compress_orderby = 'time DESC',         -- Sort order
  timescaledb.compress_chunk_time_interval = '1 day'  -- Recompress interval
);

-- Manual compression
SELECT compress_chunk(c)
FROM show_chunks('metrics', older_than => INTERVAL '7 days') c;

-- Automatic compression policy
SELECT add_compression_policy('metrics', INTERVAL '7 days');
```

### Segment By Selection

```sql
-- GOOD: Segment by commonly filtered dimension
-- Queries filter on device_id get excellent performance
ALTER TABLE metrics SET (
  timescaledb.compress_segmentby = 'device_id'
);

-- GOOD: Multiple segment columns for flexible queries
ALTER TABLE metrics SET (
  timescaledb.compress_segmentby = 'device_id, metric_name'
);

-- BAD: High cardinality segment (too many segments)
-- Don't segment by user_id if you have millions of users
ALTER TABLE events SET (
  timescaledb.compress_segmentby = 'user_id'  -- Too many segments!
);

-- BETTER for high cardinality: Include in orderby instead
ALTER TABLE events SET (
  timescaledb.compress_segmentby = 'event_type',
  timescaledb.compress_orderby = 'user_id, time DESC'
);
```

### Order By Selection

```sql
-- Time descending for "most recent" queries
ALTER TABLE metrics SET (
  timescaledb.compress_orderby = 'time DESC'
);

-- Composite order for specific query patterns
ALTER TABLE logs SET (
  timescaledb.compress_orderby = 'level, time DESC'
);
-- Benefits: WHERE level = 'error' ORDER BY time DESC

-- Include frequently filtered columns
ALTER TABLE events SET (
  timescaledb.compress_orderby = 'device_id, time DESC'
);
```

## Continuous Aggregates

### Creating Aggregates

```sql
-- Basic continuous aggregate
CREATE MATERIALIZED VIEW hourly_stats
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  device_id,
  avg(value) AS avg_value,
  min(value) AS min_value,
  max(value) AS max_value,
  count(*) AS sample_count
FROM metrics
GROUP BY bucket, device_id
WITH NO DATA;

-- Hierarchical aggregates (aggregate of aggregate)
CREATE MATERIALIZED VIEW daily_stats
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', bucket) AS bucket,
  device_id,
  avg(avg_value) AS avg_value,
  min(min_value) AS min_value,
  max(max_value) AS max_value,
  sum(sample_count) AS sample_count
FROM hourly_stats
GROUP BY 1, device_id
WITH NO DATA;
```

### Refresh Policies

```sql
-- Add refresh policy
SELECT add_continuous_aggregate_policy('hourly_stats',
  start_offset => INTERVAL '3 days',   -- Refresh this far back
  end_offset => INTERVAL '1 hour',      -- Don't refresh latest (incomplete)
  schedule_interval => INTERVAL '1 hour'
);

-- Real-time aggregates (include unrefreshed data)
ALTER MATERIALIZED VIEW hourly_stats SET (
  timescaledb.materialized_only = false  -- Include real-time data
);

-- Force refresh
CALL refresh_continuous_aggregate('hourly_stats',
  '2026-01-01'::timestamptz,
  '2026-01-02'::timestamptz
);
```

### With Compression (2.24.0)

```sql
-- Continuous aggregate with built-in compression
CREATE MATERIALIZED VIEW hourly_metrics
WITH (
  timescaledb.continuous,
  timescaledb.compress = true  -- New in 2.24.0
) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  device_id,
  avg(temperature) AS avg_temp,
  percentile_agg(temperature) AS temp_pct  -- For percentiles later
FROM sensor_readings
GROUP BY bucket, device_id
WITH NO DATA;

-- Add compression policy for the aggregate
SELECT add_compression_policy('hourly_metrics', INTERVAL '30 days');

-- Combined with refresh policy
SELECT add_continuous_aggregate_policy('hourly_metrics',
  start_offset => INTERVAL '7 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);
```

## Retention Policies

### Data Lifecycle

```sql
-- Drop old raw data (keep aggregates)
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- View retention policies
SELECT * FROM timescaledb_information.jobs
WHERE proc_name = 'policy_retention';

-- Remove retention policy
SELECT remove_retention_policy('metrics');
```

### Tiered Storage Pattern

```sql
-- Pattern: Raw → Hourly → Daily → Archive

-- 1. Raw data: Keep 7 days uncompressed
-- 2. Raw data: Keep 30 days compressed
-- 3. Raw data: Drop after 90 days

-- 4. Hourly aggregates: Keep 1 year
-- 5. Daily aggregates: Keep forever

-- Implementation:
-- Raw data policies
SELECT add_compression_policy('metrics', INTERVAL '7 days');
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- Hourly aggregate policies
SELECT add_compression_policy('hourly_stats', INTERVAL '30 days');
SELECT add_retention_policy('hourly_stats', INTERVAL '1 year');

-- Daily stats: No retention (keep forever)
SELECT add_compression_policy('daily_stats', INTERVAL '90 days');
```

## Query Patterns

### Time Range Queries

```sql
-- Recent data (uses index)
SELECT * FROM metrics
WHERE time > now() - INTERVAL '1 hour'
  AND device_id = $1
ORDER BY time DESC
LIMIT 100;

-- Time range with aggregation
SELECT
  time_bucket('5 minutes', time) AS bucket,
  avg(value) AS avg_value
FROM metrics
WHERE time BETWEEN $1 AND $2
  AND device_id = $3
GROUP BY bucket
ORDER BY bucket;

-- Last value per device
SELECT DISTINCT ON (device_id)
  device_id,
  time,
  value
FROM metrics
WHERE time > now() - INTERVAL '1 day'
ORDER BY device_id, time DESC;
```

### Using Continuous Aggregates

```sql
-- Query aggregate instead of raw data
SELECT * FROM hourly_stats
WHERE bucket > now() - INTERVAL '7 days'
  AND device_id = $1
ORDER BY bucket DESC;

-- Real-time aggregate (includes unrefreshed data)
SELECT * FROM hourly_stats
WHERE bucket > now() - INTERVAL '1 hour';
-- Automatically combines materialized + real-time data
```

### Percentiles and Statistics

```sql
-- Use percentile_agg for continuous aggregates
CREATE MATERIALIZED VIEW metrics_percentiles
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  device_id,
  percentile_agg(value) AS value_pct,  -- Aggregate percentile state
  stats_agg(value) AS value_stats       -- Statistical aggregates
FROM metrics
GROUP BY bucket, device_id;

-- Query percentiles from aggregate
SELECT
  bucket,
  device_id,
  approx_percentile(0.50, value_pct) AS median,
  approx_percentile(0.95, value_pct) AS p95,
  approx_percentile(0.99, value_pct) AS p99,
  average(value_stats) AS avg,
  stddev(value_stats) AS stddev
FROM metrics_percentiles
WHERE bucket > now() - INTERVAL '24 hours';
```

## Index Strategy

### Default Indexes

```sql
-- create_hypertable creates this by default:
-- CREATE INDEX ON metrics (time DESC);

-- Add composite indexes for common queries
CREATE INDEX idx_metrics_device_time ON metrics (device_id, time DESC);

-- Partial indexes for specific patterns
CREATE INDEX idx_metrics_errors ON metrics (time DESC)
WHERE value > threshold;
```

### Compressed Chunk Considerations

```sql
-- Indexes are not used on compressed chunks
-- Query planner uses:
-- 1. Chunk exclusion (time range)
-- 2. Segment filtering (compress_segmentby columns)
-- 3. Orderby optimization (compress_orderby columns)

-- Design compression settings for query patterns, not indexes
ALTER TABLE metrics SET (
  timescaledb.compress_segmentby = 'device_id',  -- Filter column
  timescaledb.compress_orderby = 'time DESC'      -- Sort column
);
```

## Migration Patterns

### Converting Regular Table to Hypertable

```sql
-- 1. Ensure time column exists and is NOT NULL
ALTER TABLE legacy_metrics ALTER COLUMN time SET NOT NULL;

-- 2. Convert to hypertable
SELECT create_hypertable('legacy_metrics', 'time',
  migrate_data => true,
  chunk_time_interval => INTERVAL '1 day'
);

-- 3. Add compression
ALTER TABLE legacy_metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',
  timescaledb.compress_orderby = 'time DESC'
);

-- 4. Add policies
SELECT add_compression_policy('legacy_metrics', INTERVAL '7 days');
SELECT add_retention_policy('legacy_metrics', INTERVAL '90 days');
```

### Adding TimescaleDB to Existing Database

```sql
-- 1. Install extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 2. Verify version
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
-- Should show 2.24.0

-- 3. Check PostgreSQL compatibility
SELECT timescaledb_information.version();
```

## TimescaleDB Artifact

When implementing time-series features, post this artifact:

```markdown
<!-- TIMESCALEDB_IMPLEMENTATION:START -->
## TimescaleDB Implementation Summary

### Hypertables

| Table | Chunk Interval | Space Partitions | Compression |
|-------|----------------|------------------|-------------|
| metrics | 1 day | device_id (4) | Yes |
| events | 6 hours | None | Yes |
| logs | 1 hour | level (2) | Yes |

### Compression Settings

| Table | Segment By | Order By | Bloom Filter |
|-------|------------|----------|--------------|
| metrics | device_id | time DESC | None |
| logs | level | time DESC | error_code, trace_id |

### Continuous Aggregates

| Aggregate | Source | Interval | Compression |
|-----------|--------|----------|-------------|
| hourly_metrics | metrics | 1 hour | Yes (30d) |
| daily_metrics | hourly_metrics | 1 day | Yes (90d) |

### Policies

| Table/Aggregate | Compression | Retention | Refresh |
|-----------------|-------------|-----------|---------|
| metrics | 7 days | 90 days | N/A |
| hourly_metrics | 30 days | 1 year | 1 hour |
| daily_metrics | 90 days | Never | 1 day |

### TimescaleDB 2.24.0 Features Used

- [ ] Lightning-fast recompression
- [ ] Direct Compress with continuous aggregates
- [ ] UUIDv7 in continuous aggregates
- [ ] Bloom filter sparse indexes

**TimescaleDB Version:** 2.24.0
**Verified At:** [timestamp]
<!-- TIMESCALEDB_IMPLEMENTATION:END -->
```

## Checklist

Before completing TimescaleDB implementation:

- [ ] Hypertable created with appropriate chunk interval
- [ ] Compression configured with correct segmentby/orderby
- [ ] Compression policy added
- [ ] Retention policy added (if applicable)
- [ ] Continuous aggregates created for common queries
- [ ] Refresh policies configured
- [ ] Indexes appropriate for uncompressed chunks
- [ ] Query patterns tested with EXPLAIN ANALYZE
- [ ] 2.24.0 features leveraged where beneficial
- [ ] Artifact posted to issue

## Integration

This skill integrates with:
- `database-architecture` - Hypertables follow general schema patterns
- `postgres-rls` - RLS works with hypertables (use caution with compression)
- `postgis` - Spatial time-series data

## References

- [TimescaleDB 2.24.0 Release Notes](https://github.com/timescale/timescaledb/releases/tag/2.24.0)
- [TimescaleDB Documentation](https://docs.timescale.com/)
- [Compression Best Practices](https://docs.timescale.com/use-timescale/latest/compression/)
- [Continuous Aggregates Guide](https://docs.timescale.com/use-timescale/latest/continuous-aggregates/)
