---
name: clickhouse-grafana-monitoring
description: ClickHouse analytics and Grafana dashboard configuration for Vigil Guard v2.0.0 monitoring. Use when querying logs, analyzing 3-branch detection metrics, creating dashboards, investigating events, working with n8n_logs database, managing retention policies, or monitoring branch performance (branch_a_score, branch_b_score, branch_c_score).
version: 2.0.0
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# ClickHouse & Grafana Monitoring (v2.0.0)

## Overview

Analytics and monitoring stack for Vigil Guard v2.0.0 using ClickHouse database and Grafana dashboards for real-time 3-branch parallel detection analysis.

## When to Use This Skill

- Querying event logs from ClickHouse
- Analyzing 3-branch detection metrics (Heuristics, Semantic, LLM Guard)
- Creating/modifying Grafana dashboards
- Investigating specific threats or prompts
- Monitoring branch performance and timing
- Comparing arbiter decision accuracy
- Managing data retention policies (TTL)
- Troubleshooting logging issues

## ClickHouse Schema (v2.0.0)

### Database: n8n_logs

```sql
-- events_raw: Raw webhook inputs (90 days TTL)
CREATE TABLE n8n_logs.events_raw (
  timestamp DateTime64(3, 'UTC'),
  original_input String,
  session_id String
) ENGINE = MergeTree()
PARTITION BY partition_date
ORDER BY (timestamp, event_id)
TTL toDateTime(timestamp) + INTERVAL 90 DAY DELETE;

-- events_processed: Processed with 3-branch detection results (365 days TTL)
CREATE TABLE n8n_logs.events_processed (
  timestamp DateTime64(3, 'UTC'),
  original_input String,
  sanitized_output String,
  final_status String,  -- ALLOWED, SANITIZED, BLOCKED
  threat_score Float64,
  threat_labels Array(String),
  score_breakdown Map(String, Float64),

  -- v2.0.0: 3-Branch Detection Scores
  branch_a_score Float32,      -- Heuristics
  branch_b_score Float32,      -- Semantic
  branch_c_score Float32,      -- LLM Guard

  -- v2.0.0: Arbiter Decision
  arbiter_decision String,     -- ALLOW/SANITIZE/BLOCK
  arbiter_confidence Float32,

  -- v2.0.0: Branch Timing
  branch_a_timing_ms UInt32,
  branch_b_timing_ms UInt32,
  branch_c_timing_ms UInt32,
  total_timing_ms UInt32,

  -- v2.0.0: Degraded Branch Tracking
  branch_a_degraded UInt8,     -- 1 if timeout/error
  branch_b_degraded UInt8,
  branch_c_degraded UInt8

) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, sessionId, id)
TTL toDateTime(timestamp) + INTERVAL 365 DAY DELETE;

-- retention_config: Data retention policy configuration
CREATE TABLE n8n_logs.retention_config (
  id UInt8 DEFAULT 1,
  events_raw_ttl_days UInt16 DEFAULT 90,
  events_processed_ttl_days UInt16 DEFAULT 365,
  warn_disk_usage_percent UInt8 DEFAULT 80,
  critical_disk_usage_percent UInt8 DEFAULT 90,
  last_modified_at DateTime DEFAULT now(),
  last_modified_by String DEFAULT 'system'
) ENGINE = MergeTree()
ORDER BY id;
```

## 3-Branch Detection Queries (v2.0.0)

### Branch Performance Analysis

```sql
-- Average branch scores by decision
SELECT
  arbiter_decision,
  round(avg(branch_a_score), 2) as avg_heuristics,
  round(avg(branch_b_score), 2) as avg_semantic,
  round(avg(branch_c_score), 2) as avg_llm_guard,
  count() as total
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 DAY
GROUP BY arbiter_decision;
```

### Branch Timing Analysis

```sql
-- Branch response times
SELECT
  round(avg(branch_a_timing_ms), 0) as avg_heuristics_ms,
  round(avg(branch_b_timing_ms), 0) as avg_semantic_ms,
  round(avg(branch_c_timing_ms), 0) as avg_llm_guard_ms,
  round(avg(total_timing_ms), 0) as avg_total_ms,
  round(percentile(branch_a_timing_ms, 0.95), 0) as p95_heuristics,
  round(percentile(branch_b_timing_ms, 0.95), 0) as p95_semantic,
  round(percentile(branch_c_timing_ms, 0.95), 0) as p95_llm_guard
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 HOUR;
```

### Degraded Branch Detection

```sql
-- Count degraded branches (timeouts/errors)
SELECT
  sum(branch_a_degraded) as heuristics_degraded,
  sum(branch_b_degraded) as semantic_degraded,
  sum(branch_c_degraded) as llm_guard_degraded,
  count() as total,
  round(sum(branch_a_degraded) / count() * 100, 2) as heuristics_pct,
  round(sum(branch_b_degraded) / count() * 100, 2) as semantic_pct,
  round(sum(branch_c_degraded) / count() * 100, 2) as llm_guard_pct
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 HOUR;
```

### Primary Detector Analysis

```sql
-- Which branch triggered the most detections?
SELECT
  CASE
    WHEN branch_a_score > branch_b_score AND branch_a_score > branch_c_score THEN 'Heuristics'
    WHEN branch_b_score > branch_c_score THEN 'Semantic'
    ELSE 'LLM Guard'
  END as primary_detector,
  count() as detections,
  round(avg(threat_score), 2) as avg_final_score
FROM n8n_logs.events_processed
WHERE arbiter_decision != 'ALLOW'
  AND timestamp > now() - INTERVAL 7 DAY
GROUP BY primary_detector
ORDER BY detections DESC;
```

### Branch Agreement Analysis

```sql
-- Cases where branches disagree
SELECT
  original_input,
  branch_a_score,
  branch_b_score,
  branch_c_score,
  arbiter_decision,
  abs(branch_a_score - branch_b_score) as ab_diff,
  abs(branch_b_score - branch_c_score) as bc_diff
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 DAY
  AND (
    abs(branch_a_score - branch_b_score) > 30 OR
    abs(branch_b_score - branch_c_score) > 30
  )
ORDER BY (ab_diff + bc_diff) DESC
LIMIT 20;
```

## Common Queries

### Recent Events

```sql
SELECT
  timestamp,
  original_input,
  arbiter_decision,
  branch_a_score,
  branch_b_score,
  branch_c_score,
  total_timing_ms
FROM n8n_logs.events_processed
ORDER BY timestamp DESC
LIMIT 20;
```

### Status Distribution (Last 24h)

```sql
SELECT
  arbiter_decision,
  count() as count,
  round(count() * 100.0 / sum(count()) OVER (), 2) as percentage
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 DAY
GROUP BY arbiter_decision;
```

### Score Breakdown Analysis

```sql
-- Top contributing categories (from heuristics)
SELECT
  arrayJoin(mapKeys(score_breakdown)) as category,
  count() as occurrences,
  round(avg(score_breakdown[category]), 2) as avg_score
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 7 DAY
  AND mapContains(score_breakdown, category)
GROUP BY category
ORDER BY occurrences DESC
LIMIT 15;
```

### Search Prompts

```sql
SELECT
  timestamp,
  original_input,
  arbiter_decision,
  branch_a_score,
  branch_b_score,
  branch_c_score
FROM n8n_logs.events_processed
WHERE original_input LIKE '%SQL%'
  AND timestamp > now() - INTERVAL 7 DAY
ORDER BY timestamp DESC
LIMIT 50;
```

### Blocked Events Analysis

```sql
SELECT
  original_input,
  branch_a_score as heuristics,
  branch_b_score as semantic,
  branch_c_score as llm_guard,
  threat_score as final_score,
  mapKeys(score_breakdown) as categories
FROM n8n_logs.events_processed
WHERE arbiter_decision = 'BLOCK'
  AND timestamp > now() - INTERVAL 7 DAY
ORDER BY threat_score DESC
LIMIT 20;
```

## Map Type Usage

### score_breakdown Field

```sql
-- Get score for specific category
SELECT
  original_input,
  score_breakdown['SQL_XSS_ATTACKS'] AS sql_score,
  score_breakdown['JAILBREAK_ATTEMPT'] AS jailbreak_score
FROM n8n_logs.events_processed
WHERE mapContains(score_breakdown, 'SQL_XSS_ATTACKS')
  AND timestamp > now() - INTERVAL 1 DAY;

-- Find events with specific category
SELECT * FROM n8n_logs.events_processed
WHERE mapContains(score_breakdown, 'SQL_XSS_ATTACKS')
  AND timestamp > now() - INTERVAL 1 DAY
LIMIT 10;
```

## ClickHouse CLI

### Access Container

```bash
# Interactive client
docker exec -it vigil-clickhouse clickhouse-client

# Single query
docker exec vigil-clickhouse clickhouse-client -q "SELECT count() FROM n8n_logs.events_processed"

# Pretty format
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT
    arbiter_decision,
    branch_a_score,
    branch_b_score,
    branch_c_score
  FROM n8n_logs.events_processed
  LIMIT 5
  FORMAT Pretty
"
```

### Connection Details

- Host: `vigil-clickhouse` (internal) or `localhost:8123` (HTTP)
- Port: 8123 (HTTP), 9000 (native)
- Database: `n8n_logs`
- User: `admin`
- Password: (from `.env` file)

## Grafana Dashboards (v2.0.0)

### 3-Branch Detection Dashboard

**Panels:**
1. **Branch Score Comparison** (time series) - 3 lines showing branch scores over time
2. **Arbiter Decision Distribution** (pie chart) - ALLOW/SANITIZE/BLOCK
3. **Branch Timing Heatmap** - Response times per branch
4. **Degraded Branch Alerts** - Count of branch failures
5. **Primary Detector Stats** - Which branch triggers most

### Dashboard JSON Example

```json
{
  "title": "Vigil Guard v2.0.0 - 3-Branch Detection",
  "panels": [
    {
      "title": "Branch Scores Over Time",
      "type": "timeseries",
      "targets": [{
        "rawSql": "SELECT timestamp, branch_a_score, branch_b_score, branch_c_score FROM n8n_logs.events_processed WHERE $__timeFilter(timestamp)"
      }]
    },
    {
      "title": "Branch Timing (ms)",
      "type": "gauge",
      "targets": [{
        "rawSql": "SELECT avg(branch_a_timing_ms) as heuristics, avg(branch_b_timing_ms) as semantic, avg(branch_c_timing_ms) as llm_guard FROM n8n_logs.events_processed WHERE $__timeFilter(timestamp)"
      }]
    }
  ]
}
```

## Data Retention Policy

### TTL Configuration

**Default Retention Periods:**
- `events_raw`: 90 days (~1-2 GB)
- `events_processed`: 365 days (~9-18 GB)
- **Total estimated**: 10-20 GB/year @ 5,000 prompts/day

### Retention Management UI

**Location**: Configuration → System → Data Retention
**URL**: `http://localhost/ui/config/retention`

**Features:**
- View disk usage with color-coded thresholds
- Edit TTL days (1-3650 range)
- Force cleanup button (OPTIMIZE TABLE FINAL)
- Audit trail

### Force Cleanup

```bash
# Via ClickHouse CLI
docker exec vigil-clickhouse clickhouse-client -q "OPTIMIZE TABLE n8n_logs.events_raw FINAL"
docker exec vigil-clickhouse clickhouse-client -q "OPTIMIZE TABLE n8n_logs.events_processed FINAL"

# Via API
curl -X POST http://localhost:8787/api/retention/cleanup \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"table": "all"}'
```

## Performance Monitoring

### Branch Health Dashboard Query

```sql
-- Real-time branch health (last 5 minutes)
SELECT
  toStartOfMinute(timestamp) as minute,
  count() as requests,
  round(avg(branch_a_timing_ms), 0) as heuristics_ms,
  round(avg(branch_b_timing_ms), 0) as semantic_ms,
  round(avg(branch_c_timing_ms), 0) as llm_guard_ms,
  sum(branch_a_degraded) as heuristics_errors,
  sum(branch_b_degraded) as semantic_errors,
  sum(branch_c_degraded) as llm_guard_errors
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 5 MINUTE
GROUP BY minute
ORDER BY minute DESC;
```

### SLA Monitoring

```sql
-- Branch SLA compliance (timeouts)
SELECT
  toStartOfHour(timestamp) as hour,
  countIf(branch_a_timing_ms <= 1000) / count() * 100 as heuristics_sla,
  countIf(branch_b_timing_ms <= 2000) / count() * 100 as semantic_sla,
  countIf(branch_c_timing_ms <= 3000) / count() * 100 as llm_guard_sla
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 24 HOUR
GROUP BY hour
ORDER BY hour DESC;
```

## Troubleshooting

### No Branch Data

```bash
# Verify 3-branch services are running
curl http://localhost:5005/health  # Heuristics
curl http://localhost:5006/health  # Semantic
curl http://localhost:8000/health  # LLM Guard

# Check if branch columns exist
docker exec vigil-clickhouse clickhouse-client -q "
  DESCRIBE TABLE n8n_logs.events_processed
" | grep branch
```

### High Branch Degradation

```bash
# Check which branch is failing
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT
    CASE
      WHEN branch_a_degraded = 1 THEN 'Heuristics'
      WHEN branch_b_degraded = 1 THEN 'Semantic'
      WHEN branch_c_degraded = 1 THEN 'LLM Guard'
      ELSE 'None'
    END as degraded_branch,
    count() as count
  FROM n8n_logs.events_processed
  WHERE timestamp > now() - INTERVAL 1 HOUR
    AND (branch_a_degraded = 1 OR branch_b_degraded = 1 OR branch_c_degraded = 1)
  GROUP BY degraded_branch
"

# Check service logs
docker logs vigil-heuristics-service --tail 50
docker logs vigil-semantic-service --tail 50
docker logs vigil-prompt-guard-api --tail 50
```

### Connection Failed

```bash
# Test ClickHouse connection
docker exec vigil-clickhouse clickhouse-client -q "SELECT 1"

# Check credentials
grep CLICKHOUSE_ .env
```

## Related Skills

- `n8n-vigil-workflow` - Understanding 24-node pipeline and logging
- `docker-vigil-orchestration` - 11 services management
- `pattern-library-manager` - Understanding branch detection

## References

- Schema: `services/monitoring/sql/01-create-tables.sql`
- Dashboards: `services/monitoring/grafana/provisioning/dashboards/`
- Retention docs: `docs/CLICKHOUSE_RETENTION.md`
- ClickHouse docs: https://clickhouse.com/docs

## Version History

- **v2.0.0** (Current): 3-branch columns, arbiter decision, timing metrics
- **v1.6.11**: Single-pipeline scoring, score_breakdown Map
- **v1.6.0**: Added retention_config table
