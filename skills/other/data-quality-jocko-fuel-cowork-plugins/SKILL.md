---
name: data-quality
description: Run data quality checks on Snowflake tables
user-invocable: true
---

You are helping the user check data quality in Snowflake tables.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools.

Follow these steps:

### Step 1: Define Scope

Ask the user what to check:
- **Specific table** — run checks on a named table
- **Schema-wide** — check all tables in a schema
- **Critical tables** — check tables used by Sigma dashboards

If no preference, default to scanning `SIGMA_ANALYTICS.PRODUCTION` and `SIGMA_ANALYTICS.PRODUCTION_OPERATIONS`.

### Step 2: Run Quality Checks

For each table, use `mcp__snowflake__get_table_stats` to get column-level statistics:
- Distinct count per column
- Null count and null percentage per column
- Row count

### Step 3: Flag Issues

Apply these quality thresholds:

| Check | Threshold | Severity |
|-------|-----------|----------|
| Null percentage | > 50% | Warning |
| Null percentage | > 90% | Critical |
| Zero rows | 0 rows | Critical |
| Low distinct count | < 2 on non-boolean | Warning |
| All nulls | 100% null | Critical |

### Step 4: Report Findings

Present a quality report:

**Summary**
- Tables checked: N
- Tables passing: N
- Tables with warnings: N
- Tables with critical issues: N

**Details**

| Table | Column | Issue | Null % | Severity |
|-------|--------|-------|--------|----------|
| SCHEMA.TABLE | col_name | High null rate | 92% | Critical |

### Step 5: Recommendations

For each issue:
- Suggest root cause investigation (data pipeline issue, schema change, missing data source)
- Flag if the table is used by downstream dashboards or reports
- Recommend whether to alert the data team

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking connection via `/jf-platform-tools:mcp-status`
- If a table has too many columns, report the top issues rather than every column
- If access is denied on a table, note it and continue with accessible tables
