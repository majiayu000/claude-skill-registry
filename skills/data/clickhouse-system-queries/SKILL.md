---
name: clickhouse-system-queries
description: >
  Query ClickHouse system tables to inspect query logs, monitor cluster health,
  check replication status, and analyze slow queries. Use when the user mentions
  "system tables", "query_log", "ClickHouse monitoring", "cluster status",
  "slow queries", or asks to diagnose ClickHouse operational issues.
metadata:
  author: DataStoria
  disable-slash-command: true
---

# ClickHouse System Queries Skill

Use this skill when the user asks for operational inspection on ClickHouse `system.*` tables.

Current table coverage:

- `system.query_log` via `references/system-query-log.md`

Relationship to `sql-expert`:

- `sql-expert` handles general SQL generation and user/business tables.
- This skill handles system-table operational patterns and routing to table-specific references.

## System Metrics and ProfileEvents

- Confirm column shape from schema/reference before writing predicates.
- If the user named an exact metric, pass it in the `columns` list via `explore_schema` instead of loading the full table schema.
- If `ProfileEvents` is a `Map`, access entries as `ProfileEvents['Name']`. If flattened, use `ProfileEvent_Name`.

Example — map vs flattened access:

```sql
-- Map access
SELECT ProfileEvents['DistributedConnectionFailTry'] AS fails
FROM system.query_log WHERE event_date = today();

-- Flattened column access
SELECT ProfileEvent_DistributedConnectionFailTry AS fails
FROM system.query_log WHERE event_date = today();
```

## Workflow

1. **Resolve target** — identify system table and intent. Inherit the most recent time window from conversation, or default to last 60 minutes.

2. **Load reference** — for `system.query_log`, call `skill_resource` to load `references/system-query-log.md` before writing any SQL. For unsupported tables, fall back to `sql-expert`.

3. **Execute** — choose the right tool:
   - `search_query_log` for standard ranked searches and filtered lookups
   - `execute_sql` for visualization, time-bucketed aggregation, trends, or histograms

   ```sql
   -- search_query_log: standard lookup
   -- finds top 10 slowest queries in the last hour

   -- execute_sql: time-bucketed visualization
   SELECT toStartOfFiveMinutes(event_time) AS bucket,
          count() AS queries,
          avg(query_duration_ms) AS avg_ms
   FROM system.query_log
   WHERE event_date = today() AND event_time > now() - INTERVAL 1 HOUR
   GROUP BY bucket ORDER BY bucket
   ```

   Default to `LIMIT 50` unless the user specifies otherwise.

4. **Summarize** with concise findings and next actions.

## Guardrails

- Always apply time bounds for log-like system tables
- Always use the table-specific reference when available
- Never generate `system.query_log` SQL until `references/system-query-log.md` is loaded in the current turn
- Never use `search_query_log` for chart-oriented requests
- Never omit `LIMIT` in exploratory queries
