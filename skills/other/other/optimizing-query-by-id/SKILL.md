---
name: optimizing-query-by-id
description: |
  Optimizes Snowflake query performance using query ID from history. Use when optimizing Snowflake queries for:
  (1) User provides a Snowflake query_id (UUID format) to analyze or optimize
  (2) Task mentions "slow query", "optimize", "query history", or "query profile" with a query ID
  (3) Analyzing query performance metrics - bytes scanned, spillage, partition pruning
  (4) User references a previously run query that needs optimization
  Fetches query profile, identifies bottlenecks, returns optimized SQL with expected improvements.
---

# Optimize Query from Query ID

**Fetch query → Get profile → Apply best practices → Verify improvement → Return optimized query**

## Workflow

### 1. Fetch Query Details from Query ID

```sql
SELECT
    query_id,
    query_text,
    total_elapsed_time/1000 as seconds,
    bytes_scanned/1e9 as gb_scanned,
    bytes_spilled_to_local_storage/1e9 as gb_spilled_local,
    bytes_spilled_to_remote_storage/1e9 as gb_spilled_remote,
    partitions_scanned,
    partitions_total,
    rows_produced
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_id = '<query_id>';
```

Note the key metrics:
- `seconds`: Total execution time
- `gb_scanned`: Data read (lower is better)
- `gb_spilled`: Spillage indicates memory pressure
- `partitions_scanned/total`: Partition pruning effectiveness

### 2. Get Query Profile Details

```sql
-- Get operator-level statistics
SELECT *
FROM TABLE(GET_QUERY_OPERATOR_STATS('<query_id>'));
```

Look for:
- Operators with high `output_rows` vs `input_rows` (explosions)
- TableScan operators with high bytes
- Sort/Aggregate operators with spillage

### 3. Identify Optimization Opportunities

Based on profile, look for:

| Metric | Issue | Fix |
|--------|-------|-----|
| partitions_scanned = partitions_total | No pruning | Add filter on cluster key |
| gb_spilled > 0 | Memory pressure | Simplify query, increase warehouse |
| High bytes_scanned | Full scan | Add selective filters, reduce columns |
| Join explosion | Cartesian or bad key | Fix join condition, filter before join |

### 4. Apply Optimizations

Rewrite the query:
- Select only needed columns
- Filter early (before joins)
- Use CTEs to avoid repeated scans
- Ensure filters align with clustering keys
- Add LIMIT if full result not needed

### 5. Get Explain Plan for Optimized Query

```sql
EXPLAIN USING JSON
<optimized_query>;
```

### 6. Compare Plans

Compare original vs optimized:
- Fewer partitions scanned?
- Fewer intermediate rows?
- Better join order?

### 7. Return Results

Provide:
1. Original query metrics (time, data scanned, spillage)
2. Identified issues
3. The optimized query
4. Summary of changes made
5. Expected improvement

## Example Output

**Original Query Metrics:**
- Execution time: 45 seconds
- Data scanned: 12.3 GB
- Partitions: 500/500 (no pruning)
- Spillage: 2.1 GB

**Issues Found:**
1. No partition pruning - filtering on non-cluster column
2. SELECT * scanning unnecessary columns
3. Large table joined without pre-filtering

**Optimized Query:**
```sql
WITH filtered_events AS (
    SELECT event_id, user_id, event_type, created_at
    FROM events
    WHERE created_at >= '2024-01-01'
      AND created_at < '2024-02-01'
      AND event_type = 'purchase'
)
SELECT fe.event_id, fe.created_at, u.name
FROM filtered_events fe
JOIN users u ON fe.user_id = u.id;
```

**Changes:**
- Added date range filter matching cluster key
- Replaced SELECT * with specific columns
- Pre-filtered in CTE before join

**Expected Improvement:**
- Partitions: 500 → ~15 (97% reduction)
- Data scanned: 12.3 GB → ~0.4 GB
- Estimated time: 45s → ~3s
