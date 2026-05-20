---
name: inventory-alert
description: Check inventory health and highlight critical SKU risk tiers
user-invocable: true
---

You are helping the operations team monitor inventory health across all products.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_inventory_health`).

Follow these steps:

### Step 1: Pull Inventory Health

Use `mcp__snowflake__get_inventory_health` (no parameters required) to get the current inventory dashboard.

### Step 2: Present Risk Tiers

Organize results by risk level:
- **Critical** — SKUs at or below safety stock, immediate action needed
- **Warning** — SKUs projected to stock out within 2 weeks
- **Healthy** — SKUs with adequate coverage

For critical SKUs, highlight:
- Product name and SKU
- Current inventory level
- Days of coverage remaining
- Reorder status (if available)

### Step 3: Summarize

Provide a concise summary:
- Total SKUs by risk tier
- Top 5 most urgent SKUs requiring attention
- Any patterns (e.g., entire product line at risk)

### Step 4: Follow-Up

Offer:
- **Forecast coverage** for a specific product — use `mcp__snowflake__get_inventory_coverage`
- **Demand forecast** — use `mcp__snowflake__get_demand_forecast`
- **Full ops dashboard** — `/jf-operations-center:ops-dashboard`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If inventory data appears stale, warn the user about potential data freshness issues
