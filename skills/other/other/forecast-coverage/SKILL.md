---
name: forecast-coverage
description: Check inventory coverage against demand forecast for a product
user-invocable: true
---

You are helping the finance or operations team check inventory coverage against demand forecasts.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_inventory_coverage`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user for:
- **Product**: Which product or SKU to check?

### Step 2: Pull Coverage Data

Use `mcp__snowflake__get_inventory_coverage` with the product parameter.

### Step 3: Present Coverage

Show:
- **Current inventory** — units on hand
- **Weeks of coverage** — how many weeks current inventory will last at forecasted demand
- **Reorder point** — when a reorder should be triggered
- **Projected stockout date** — if no reorder occurs

### Step 4: Risk Assessment

Classify the coverage status:
- **Healthy** — 8+ weeks of coverage
- **Watch** — 4-8 weeks of coverage
- **At Risk** — 2-4 weeks of coverage
- **Critical** — less than 2 weeks of coverage

### Step 5: Follow-Up

Offer:
- **Demand forecast** — `/jf-financial-analyst:forecast-demand` for detailed weekly projections
- **Inventory health** (all SKUs) — available via jf-operations-center plugin
- **Check another product**

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If the product is not found, suggest checking the product name/SKU
