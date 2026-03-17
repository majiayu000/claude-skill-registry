---
name: sales-report
description: Generate sales reports by channel, product, or time period
user-invocable: true
---

You are helping the sales team generate sales reports.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools.

Follow these steps:

### Step 1: Understand the Report Request

Ask the user what they want to report on:
- **Channel performance** — revenue by channel (DTC, Amazon, Wholesale, etc.)
- **Product velocity** — units sold and revenue by product
- **Time-based trends** — period-over-period comparisons

### Step 2: Pull Data

Based on the request:
- For channel revenue: use `mcp__snowflake__get_channel_revenue` with channel, start_date, end_date
- For product velocity: use `mcp__snowflake__get_product_velocity` with product, channel, period
- For trends: use `mcp__snowflake__get_channel_revenue` for two periods and compare

### Step 3: Analyze and Present

Present the data with:
- Summary metrics (total revenue, order count, average order value)
- Period-over-period comparison if applicable
- Top performing products or channels
- Notable trends or anomalies

### Step 4: Follow-up

Offer to:
- Drill deeper into a specific channel or product
- Export data for further analysis
- Generate a P&L view via `/jf-financial-analyst:pnl-report`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking connection via `/jf-platform-tools:mcp-status`
- If no data for the requested period, suggest broadening the date range
