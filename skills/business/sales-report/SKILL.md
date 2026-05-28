---
name: sales-report
description: Generate revenue, units, and margin reports by channel
user-invocable: true
---

You are helping the sales team generate sales performance reports.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools.

### Step 1: Define Report Scope

Ask the user:
- **Channels**: DTC (Shopify), Amazon, Wholesale, or All?
- **Time period**: This week, MTD, QTD, YTD, or custom date range?
- **Grouping**: By channel, by product, by region, or combined?
- **Comparison**: vs prior period, vs prior year, vs budget?

### Step 2: Gather Data

Use Snowflake MCP as the primary data source:
- For channel revenue: use `mcp__snowflake__get_channel_revenue` with channel, start_date, end_date
- For product velocity: use `mcp__snowflake__get_product_velocity` with product, channel, period

Supplement with other sources as needed:
- **Shopify DTC** — Order data from Shopify Admin API
- **Amazon** — Seller Central reporting data
- **Wholesale** — Wholesale store order data via MCP promo-order tools (read-only access)
- **Circana retail POS** — Syndicated sell-through data (for retailer performance)

### Step 3: Build the Report

Present a structured report:

**Revenue Summary**
- Total revenue by channel
- Period-over-period change ($ and %)
- Revenue mix by channel

**Units Summary**
- Total units by channel
- Average selling price by channel

**Product Performance**
- Top 10 products by revenue
- Top 10 by units
- Products with significant period-over-period changes

### Step 4: Insights

Highlight:
- Channels with accelerating or decelerating growth
- Products with unusual velocity changes
- Margin anomalies or pricing issues

### Step 5: Follow-Up

Offer:
- Drill into a specific channel or product
- Generate a buyer presentation with the data
- Export for slides or spreadsheets

### Error Handling

- If a channel data source is unavailable, note it and report on available channels
- Clearly label which data sources contributed to the report
