---
name: forecast-demand
description: View demand forecast for a product over a specified time horizon
user-invocable: true
---

You are helping the finance or operations team review demand forecasts.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_demand_forecast`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user for:
- **Product**: Which product or SKU to forecast?
- **Horizon**: How many weeks out? (default: 12 weeks)

### Step 2: Pull Forecast Data

Use `mcp__snowflake__get_demand_forecast` with the product and horizon_weeks parameters.

### Step 3: Present Forecast

Format the forecast clearly:
- **Weekly demand projections** — units expected per week
- **Trend direction** — increasing, decreasing, or flat
- **Confidence level** — if provided by the model
- **Seasonality notes** — any seasonal patterns detected

### Step 4: Context

Add relevant context:
- Compare forecast to current inventory (use `mcp__snowflake__get_inventory_coverage` for the same product)
- Note if forecast suggests a stockout risk
- Highlight weeks where demand exceeds current supply plan

### Step 5: Follow-Up

Offer:
- **Inventory coverage** — `/jf-financial-analyst:forecast-coverage`
- **Scenario modeling** — `/jf-financial-analyst:scenario-model`
- **Forecast for a different product**

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If the product is not found in forecast data, suggest checking the product name/SKU
