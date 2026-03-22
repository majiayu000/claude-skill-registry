---
name: sql-expert
description: Expert system for generating, validating, and optimizing ClickHouse SQL. Use this when the user needs data, queries, or analysis.
metadata:
  author: System
  disable-slash-command: true
---

> ## 🚨 CRITICAL RULE: MANDATORY VALIDATION
> You **MUST** call `validate_sql(sql)` for **every** new query you generate.
> **Context Note**: Historical validation steps are pruned to save tokens, but this does NOT excuse you from validating new queries in the current turn. Always validate before executing.

# 1. Schema Discovery & Context
- **Missing Schema**: If you do not have the table schema, you MUST use `get_tables` and `explore_schema` first.
  - *Optimization*: If the user already mentioned exact field names, pass them in the `columns` argument of `explore_schema` instead of loading the full table schema.
- **Exact Identifier Rule**: Treat exact identifier-like tokens from the user question as candidate columns on the first schema lookup. This especially applies to ClickHouse metric names such as `ProfileEvent_*`, `CurrentMetric_*`, and flattened event columns on `system.*` tables.
- **Missing Columns**: If you don't see the expected column, retry `explore_schema` with a narrower `columns` list based on the user-mentioned identifier or the closest confirmed column names.
- **Schema Fidelity**: Only use columns that are confirmed to exist in the table schema from `explore_schema`. Do not assume standard columns exist if they are not in the tool output.
- **User Context**: If the user asks about "my data", use `WHERE user = '<clickHouseUser>'`.
- **System Tables**: For queries on `system.*` tables (e.g., `system.query_log`, `system.parts`, `system.merges`), defer to the `clickhouse-system-queries` skill - it contains table-specific patterns, predicates, and resource metrics that this skill does not cover. For `system.query_log`, do not generate SQL until `references/system-query-log.md` has been loaded via `skill_resource`, and do not call `search_query_log` for chart/time-series requests.

# 2. Syntax Rules (The Grammar)
- **Tables**: ALWAYS use fully qualified names (e.g., `database.table`).
- **Semicolons**: NEVER include a trailing semicolon (`;`).
- **Enums**: Use exact string literals for Enum columns.
- **Safety**: ALWAYS use `LIMIT` for data exploration queries.

# 3. Optimization Rules (Best Practices)
- **Time filters**: Always filter by the partition key (usually `event_date` or `timestamp`) first. Use **bounded time windows** (e.g., last 24h, 7 days) unless the user asks for all history.
- **Primary Keys (CRITICAL)**: ClickHouse indexes are sparse. You **MUST** filter on the **leading column** of the Primary Key if you filter on any secondary column.
  - *Bad*: `WHERE event_time > now() - 1h` (If PK is `event_date, event_time`, this scans everything).
  - *Good*: `WHERE event_date >= toDate(now() - 1h) AND event_time > now() - 1h` (Uses index, handles midnight crossover).
- **Approximation**: Use `uniq()` instead of `uniqExact()` unless precision is explicitly requested.
- **Joins**: Put the **smaller table on the RIGHT**. Use `GLOBAL IN` only for distributed queries.

# 4. Execution Workflow
1. **Generate**: Create the SQL following the rules above.
2. **Validate (MANDATORY)**: Call `validate_sql(sql)`.
   - *If invalid*: Read the error, fix the SQL, and retry (max 3 attempts).
3. **Decide Action**:
   - *Visualization*: IF the user wants a chart, DO NOT execute. Pass the SQL to the visualization skill logic.
   - *Data*: IF the user wants answers (lists, counts), call `execute_sql(sql)`.
   - *Code Only*: IF the user asks to "write SQL", just output the code block.
