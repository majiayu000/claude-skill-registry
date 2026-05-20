---
name: optimization
description: Optimize slow queries, analyze SQL performance, find expensive queries. Use when the user mentions slow queries, optimize, performance, cpu, memory, duration.
---

# SQL Optimization Skill

Use this skill when the user asks to optimize slow queries, analyze performance, or find expensive queries by metric (cpu, memory, disk, duration). Workflow is evidence-driven: collect evidence with tools, then recommend based on evidence only.

## Pre-flight Check

1. **HAS SQL**: Conversation contains a SQL query → Go to WORKFLOW step 2 (Collect Evidence).
2. **HAS QUERY_ID**: Conversation contains query_id → Go to WORKFLOW step 2 (Call `collect_sql_optimization_evidence` immediately).
3. **DISCOVERY REQUEST**: User asks to find/optimize expensive queries by metric → Go to WORKFLOW step 1 (Discovery).
4. **NEITHER**: Output ONLY a concise 1-sentence request for the SQL query or query_id (e.g. "Please provide the SQL query or query_id you'd like to optimize."). Do NOT ask for any other details (like version, table sizes, etc.). Then include the following UI trigger block in the response (must be present and unchanged; place it at the end of the reply):

```user_actions
{ "type": "optimization_skill_input" }
```

## Discovery

- Trigger: "find top N queries by cpu/memory/duration", "optimize the slowest queries", "what queries consume most memory".
- Metric mapping: cpu/CPU time/processor → "cpu"; memory/RAM/mem → "memory"; slow/duration/time/latency → "duration"; disk/I/O/read bytes → "disk".
- **Limitation**: `find_expensive_queries` ONLY supports cpu, memory, disk, duration. It cannot filter by user, database, table name, or query pattern. If user needs other filters, ask for query_id or use supported metrics.

## Time Filtering

- `time_window`: Relative minutes from now (e.g., 60 = last hour).
- `time_range`: Absolute range `{ from: "ISO date", to: "ISO date" }`.
- When calling `collect_sql_optimization_evidence` after `find_expensive_queries`, you MUST pass the same time_window or time_range used in discovery.

## Workflow

1. **Discovery (if needed)**: Call `find_expensive_queries` with metric, limit, and time_window/time_range. Then proceed with top result(s).
2. **Collect Evidence**: Call `collect_sql_optimization_evidence` with sql or query_id (and same time params if coming from discovery). DO NOT write SQL to query system tables manually.
3. **Analyze**: Review evidence for optimization opportunities.
4. **Recommendations**: Rank by Impact/Risk/Effort. Prefer low-risk query rewrites first.
5. **Validate**: Use `validate_sql` for any proposed SQL changes. Add inline comments (-- comment) to highlight key changes.

## Table Schema Evidence

- Use table_schema fields: columns, engine, partition_key, primary_key, sorting_key, secondary_indexes.
- Suggest secondary indexes only when evidence shows frequent WHERE filters on selective columns and the index type fits the predicate.
  - Use `minmax` for range predicates on sorted columns.
  - Use `set` for low-cardinality equality filters.
  - Use `bloom_filter` for high-cardinality equality filters (e.g., trace_id, user_id).
  - Use `tokenbf_v1` for frequent token-based text search.

## Rules

- Do NOT recommend based on assumptions. If evidence is missing, collect it with tools.
- If tools return NO meaningful evidence, output only a brief 3-5 sentence message explaining what's missing.
- Always validate proposed SQL with `validate_sql` before recommending.
- `find_expensive_queries` may return truncated SQL. Never send truncated SQL to `collect_sql_optimization_evidence`.
- If the SQL appears incomplete (truncated/ellipsized/ends mid-clause), use `query_id` instead of sql.
- When both `query_id` and SQL are available, prefer `query_id` to reduce tokens and avoid truncation issues.
