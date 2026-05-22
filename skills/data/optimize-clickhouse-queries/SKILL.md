---
name: optimize-clickhouse-queries
description: Optimize slow queries, analyze SQL performance, and collect evidence for expensive workloads.
metadata:
  author: System
---

# SQL Optimization Skill

Workflow is evidence-driven: collect evidence with tools, then recommend based on evidence only.

## Pre-flight Check

1. **HAS SQL**: Conversation contains a SQL query -> Go to WORKFLOW step 2 (Collect Evidence).
2. **HAS QUERY_ID**: Conversation contains query_id -> Go to WORKFLOW step 2 (Call `collect_sql_optimization_evidence` immediately).
3. **DISCOVERY REQUEST**: User asks to optimize the slowest/heaviest queries but does not provide SQL/query_id -> Go to WORKFLOW step 1 (Discovery).
4. **NEITHER**: Output ONLY a concise 1-sentence request for the SQL query or query_id (e.g. "Please provide the SQL query or query_id you'd like to optimize."). Do NOT ask for any other details (like version, table sizes, etc.). Then include the following UI trigger block in the response (must be present and unchanged; place it at the end of the reply):

```user_actions
{ "type": "optimization_skill_input" }
```

## Discovery

- Prefer `search_query_log` for discovery from `system.query_log` (slowest, most expensive, user-scoped, database-scoped, text-scoped, etc.).
- If `search_query_log` cannot express the request, then load the `clickhouse-system-queries` skill, immediately call `skill_resource` for `references/system-query-log.md`, and follow that reference strictly.
- Do NOT write ad-hoc SQL against `system.query_log` from this skill when `search_query_log` can satisfy the request.
- Extract `query_id` from the discovery results for the next step (evidence collection).

## Time Filtering

- `time_window`: Relative minutes from now (e.g., 60 = last hour).
- `time_range`: Absolute range `{ from: "ISO date", to: "ISO date" }`.
- When calling `collect_sql_optimization_evidence` after discovery, you MUST pass the same time_window or time_range used in discovery.

## Mode Selection

- Default `collect_sql_optimization_evidence` to light mode for the first pass.
- Prefer omitting the `mode` argument entirely unless full detail is required.
- Use `mode: "full"` only when the user explicitly asks for detailed/raw evidence or the light pass is insufficient.
- Do not choose `full` just because the request says "optimize", "analyze", or "investigate".

## Workflow

1. **Discovery (if needed)**: Prefer `search_query_log` to find candidates. If the request exceeds the tool's schema, then load `clickhouse-system-queries`, load `references/system-query-log.md` via `skill_resource`, and use that reference. Extract `query_id` from the results.
2. **Collect Evidence**: Call `collect_sql_optimization_evidence` with query_id (preferred) or sql (and same time params if coming from discovery).
3. **Analyze**: Review evidence for optimization opportunities.
4. **Recommendations**: Rank by Impact/Risk/Effort. Prefer low-risk query rewrites first.
5. **Validate**: Use `validate_sql` for any proposed SQL changes. Add inline comments (`-- comment`) to highlight key changes.

## Table Schema Evidence

- Use table_schema fields: columns, engine, partition_key, primary_key, sorting_key, secondary_indexes.
- When `optimization_target` is present, treat it as the real local-table schema behind a `Distributed` table and base key/index recommendations on it.
- Suggest secondary indexes only when evidence shows frequent WHERE filters on selective columns and the index type fits the predicate.
  - Use `minmax` for range predicates on sorted columns.
  - Use `set` for low-cardinality equality filters.
  - Use `bloom_filter` for high-cardinality equality filters (e.g., trace_id, user_id).
  - Use `tokenbf_v1` for frequent token-based text search.

## Rules

- Do NOT recommend based on assumptions. If evidence is missing, collect it with tools.
- If tools return NO meaningful evidence, output only a brief 3-5 sentence message explaining what's missing.
- Always validate proposed SQL with `validate_sql` before recommending.
- If discovery results include both query text and query_id, prefer query_id to avoid truncation issues.
- If the SQL appears incomplete (truncated/ellipsized/ends mid-clause), use `query_id` instead of sql.
- When both `query_id` and SQL are available, prefer `query_id` to reduce tokens and avoid truncation issues.
