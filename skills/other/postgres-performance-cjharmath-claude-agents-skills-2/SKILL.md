---
name: postgres-performance
description: High-performance PostgreSQL patterns. Use when optimizing queries, designing for scale, or debugging performance issues.
---

# PostgreSQL Performance Engineering

## Problem Statement

Performance problems compound. A query that takes 50ms at 1K rows takes 5s at 100K rows. This skill covers patterns for building performant database interactions from the start and fixing performance issues.

---

## Pattern: Query Optimization Workflow

### Step 1: Identify Slow Queries

```sql
-- Enable pg_stat_statements (if not already)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries
SELECT 
    query,
    calls,
    round(mean_exec_time::numeric, 2) as avg_ms,
    round(total_exec_time::numeric, 2) as total_ms,
    rows
FROM pg_stat_statements
WHERE calls > 10
ORDER BY mean_exec_time DESC
LIMIT 20;
```

### Step 2: Analyze Query Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM assessments 
WHERE user_id = 'abc-123' 
ORDER BY created_at DESC 
LIMIT 10;
```

**What to look for:**

| Warning Sign | Problem | Solution |
|--------------|---------|----------|
| Seq Scan on large table | Missing index | Add index |
| High `loops` count | N+1 in join | Rewrite query, add index |
| Sort with high cost | No index for ORDER BY | Covering index |
| Hash/Merge Join with high rows | Large intermediate result | Filter earlier, better indexes |
| Buffers: shared read high | Data not cached | More RAM, or query less data |

### Step 3: Fix and Verify

```sql
-- Add index
CREATE INDEX CONCURRENTLY ix_assessments_user_created 
ON assessments (user_id, created_at DESC);

-- Verify improvement
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM assessments 
WHERE user_id = 'abc-123' 
ORDER BY created_at DESC 
LIMIT 10;
-- Should now show "Index Scan" instead of "Seq Scan"
```

---

## Pattern: Covering Indexes (Index-Only Scans)

**Problem:** Query reads index, then fetches rows from table (heap fetch).

```sql
-- Query
SELECT id, title, status FROM assessments WHERE user_id = ?;

-- Regular index: requires heap fetch
CREATE INDEX ix_assessments_user ON assessments (user_id);
-- Plan: Index Scan + Heap Fetches

-- ✅ Covering index: all columns in index
CREATE INDEX ix_assessments_user_covering 
ON assessments (user_id) 
INCLUDE (id, title, status);
-- Plan: Index Only Scan (no heap fetch, much faster)
```

**When to use:**
- Frequently run queries
- Queries selecting few columns
- Tables with many columns (heap fetch is expensive)

---

## Pattern: Pagination at Scale

```sql
-- ❌ SLOW: OFFSET-based pagination
SELECT * FROM events ORDER BY created_at DESC LIMIT 20 OFFSET 10000;
-- Must scan and discard 10,000 rows!

-- ✅ FAST: Cursor-based (keyset) pagination
SELECT * FROM events 
WHERE created_at < '2024-01-15T10:30:00Z'  -- Last seen timestamp
ORDER BY created_at DESC 
LIMIT 20;
-- Jumps directly to the right place via index

-- For compound cursor (when duplicates possible):
SELECT * FROM events 
WHERE (created_at, id) < ('2024-01-15T10:30:00Z', 'last-id')
ORDER BY created_at DESC, id DESC 
LIMIT 20;
```

**In SQLAlchemy:**
```python
# Cursor-based pagination
async def get_events_page(
    session: AsyncSession,
    cursor_time: datetime | None,
    cursor_id: UUID | None,
    limit: int = 20,
) -> list[Event]:
    query = select(Event).order_by(Event.created_at.desc(), Event.id.desc())
    
    if cursor_time and cursor_id:
        query = query.where(
            tuple_(Event.created_at, Event.id) < (cursor_time, cursor_id)
        )
    
    result = await session.execute(query.limit(limit))
    return result.scalars().all()
```

---

## Pattern: Batch Processing

```sql
-- ❌ SLOW: One huge query/update
UPDATE events SET processed = true WHERE processed = false;
-- Locks millions of rows, times out

-- ✅ FAST: Batch processing
DO $$
DECLARE
    batch_size INT := 10000;
    rows_affected INT;
BEGIN
    LOOP
        UPDATE events 
        SET processed = true 
        WHERE id IN (
            SELECT id FROM events 
            WHERE processed = false 
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        );
        
        GET DIAGNOSTICS rows_affected = ROW_COUNT;
        
        IF rows_affected = 0 THEN
            EXIT;
        END IF;
        
        COMMIT;
        PERFORM pg_sleep(0.1);  -- Brief pause to let other queries through
    END LOOP;
END $$;
```

**In Python:**
```python
async def process_in_batches(session: AsyncSession, batch_size: int = 10000):
    while True:
        result = await session.execute(
            text("""
                UPDATE events SET processed = true
                WHERE id IN (
                    SELECT id FROM events 
                    WHERE processed = false 
                    LIMIT :batch_size
                    FOR UPDATE SKIP LOCKED
                )
                RETURNING id
            """),
            {"batch_size": batch_size}
        )
        
        updated = result.fetchall()
        await session.commit()
        
        if len(updated) == 0:
            break
        
        await asyncio.sleep(0.1)
```

---

## Pattern: Efficient Aggregations

```sql
-- ❌ SLOW: Count with complex WHERE
SELECT COUNT(*) FROM events WHERE user_id = ? AND status = 'active';
-- Scans all matching rows

-- ✅ FAST: Approximate count (for large tables)
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'events';

-- ✅ FAST: Maintain counter cache
-- Add column: assessments.answer_count
-- Update on INSERT/DELETE to answers

-- ✅ FAST: Materialized view for complex aggregations
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    user_id,
    COUNT(*) as total_assessments,
    AVG(rating) as avg_rating
FROM assessments
GROUP BY user_id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

---

## Pattern: Connection Pool Tuning

```python
# Async SQLAlchemy with proper pool settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool

# For serverless/Lambda (no persistent connections)
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # New connection per request
)

# For long-running servers
engine = create_async_engine(
    DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=10,           # Base connections
    max_overflow=20,        # Extra connections under load
    pool_timeout=30,        # Wait for connection
    pool_recycle=1800,      # Recycle connections every 30 min
    pool_pre_ping=True,     # Test connection before use
)
```

**PostgreSQL side:**
```sql
-- Check max connections
SHOW max_connections;  -- Default 100

-- See current connections
SELECT count(*) FROM pg_stat_activity;

-- Connection per application
SELECT application_name, count(*) 
FROM pg_stat_activity 
GROUP BY application_name;
```

---

## Pattern: Read Replicas

```python
# Route reads to replica, writes to primary
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

primary_engine = create_async_engine(PRIMARY_URL)
replica_engine = create_async_engine(REPLICA_URL)

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if self._flushing or self.is_modified():
            return primary_engine.sync_engine
        return replica_engine.sync_engine
```

---

## Pattern: Denormalization for Read Performance

```sql
-- ❌ SLOW: Joining 4 tables for common query
SELECT 
    a.id, a.title, u.name as user_name, 
    COUNT(q.id) as question_count,
    AVG(ans.value) as avg_score
FROM assessments a
JOIN users u ON a.user_id = u.id
JOIN questions q ON q.assessment_id = a.id
LEFT JOIN answers ans ON ans.question_id = q.id
GROUP BY a.id, a.title, u.name;

-- ✅ FAST: Denormalized columns
ALTER TABLE assessments ADD COLUMN user_name VARCHAR(100);
ALTER TABLE assessments ADD COLUMN question_count INT DEFAULT 0;
ALTER TABLE assessments ADD COLUMN avg_score NUMERIC(3,2);

-- Update via triggers or application code
-- Query becomes simple:
SELECT id, title, user_name, question_count, avg_score FROM assessments;
```

**Tradeoffs:**
- ✅ Much faster reads
- ❌ More complex writes (must update denormalized data)
- ❌ Potential for stale data

---

## Pattern: Partitioning Large Tables

```sql
-- Partition events by month
CREATE TABLE events (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    event_type VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Query specific partition (fast)
SELECT * FROM events WHERE created_at >= '2024-01-15' AND created_at < '2024-02-01';

-- Drop old data instantly
DROP TABLE events_2023_01;  -- Much faster than DELETE
```

---

## Pattern: Caching Strategy

```python
# Cache frequently-read, rarely-changed data
import redis.asyncio as redis
import json

cache = redis.from_url(REDIS_URL)

async def get_user_stats(user_id: UUID) -> UserStats:
    cache_key = f"user_stats:{user_id}"
    
    # Try cache first
    cached = await cache.get(cache_key)
    if cached:
        return UserStats.model_validate_json(cached)
    
    # Query database
    async with get_session() as session:
        stats = await calculate_user_stats(session, user_id)
    
    # Cache for 5 minutes
    await cache.setex(cache_key, 300, stats.model_dump_json())
    
    return stats

# Invalidate on write
async def update_user_assessment(user_id: UUID, ...):
    # ... update database ...
    await cache.delete(f"user_stats:{user_id}")
```

---

## Performance Monitoring Queries

```sql
-- Table bloat (needs VACUUM)
SELECT 
    schemaname, relname,
    n_dead_tup as dead_tuples,
    n_live_tup as live_tuples,
    round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Index bloat
SELECT
    indexrelname as index,
    pg_size_pretty(pg_relation_size(indexrelid)) as size,
    idx_scan as scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Unused indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Cache hit ratio (should be > 99%)
SELECT 
    sum(blks_hit) * 100.0 / sum(blks_hit + blks_read) as cache_hit_ratio
FROM pg_stat_database;

-- Long-running queries
SELECT 
    pid,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE state = 'active' 
    AND query NOT LIKE '%pg_stat%'
    AND now() - query_start > interval '30 seconds';
```

---

## Performance Checklist

Before deploying:

- [ ] Slow queries identified and optimized
- [ ] Indexes match query patterns
- [ ] Covering indexes for frequent queries
- [ ] Pagination uses cursor-based (not OFFSET)
- [ ] Large tables partitioned if > 10M rows
- [ ] Connection pool sized appropriately
- [ ] Cache layer for hot data
- [ ] Monitoring in place for slow queries
- [ ] VACUUM and ANALYZE scheduled
