---
name: schema-drift
description: Detect schema changes in Snowflake tables
user-invocable: true
---

You are helping the user detect schema drift in Snowflake tables.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools.

Follow these steps:

### Step 1: Define Scope

Ask the user what to check:
- **Specific database and schema** — e.g., SIGMA_ANALYTICS.PRODUCTION
- **Specific tables** — check named tables only
- **Full scan** — check all accessible databases and schemas

If no preference, default to scanning `SIGMA_ANALYTICS` schemas: PRODUCTION, PRODUCTION_OPERATIONS, PRODUCTION_FORECAST, PRODUCTION_MASTERITEM, DEVELOPMENT.

### Step 2: Inventory Current Schema

Use `mcp__snowflake__list_tables` to get tables in each schema. For each table, use `mcp__snowflake__describe_table` to get column names, types, and nullability.

### Step 3: Compare Against Expected

Compare the discovered schema against known expectations:
- Tables that exist but are not documented
- Missing tables that should exist
- Column type changes (e.g., VARCHAR became NUMBER)
- Nullable columns that were previously NOT NULL
- Columns added or removed since last check

### Step 4: Report Findings

Present a drift report:

| Table | Change Type | Details |
|-------|-------------|---------|
| SCHEMA.TABLE | Column Added | `new_col` (VARCHAR) |
| SCHEMA.TABLE | Column Removed | `old_col` no longer present |
| SCHEMA.TABLE | Type Changed | `col` was NUMBER, now VARCHAR |

### Step 5: Recommendations

For each drift finding, suggest:
- Whether the change looks intentional or accidental
- Downstream impacts (dashboards, scripts, other tables that reference it)
- Whether dependent SQL needs updating

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking connection via `/jf-platform-tools:mcp-status`
- If a schema is not accessible, note the permission issue and continue with accessible schemas
- If the table list is very large, process in batches and report progress
