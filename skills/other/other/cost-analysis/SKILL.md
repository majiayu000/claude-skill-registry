---
name: cost-analysis
description: Break down costs by category (fulfillment, payment, marketplace)
user-invocable: true
---

You are helping the finance team analyze cost breakdowns.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_cost_breakdown`).

Follow these steps:

### Step 1: Choose Category

Ask the user which cost category to analyze:
- **Fulfillment** — pick, pack, ship, warehouse costs
- **Payment** — payment processing fees by method and provider
- **Marketplace** — marketplace fees, commissions, advertising costs

### Step 2: Pull Cost Data

Use `mcp__snowflake__get_cost_breakdown` with the selected category.

### Step 3: Present Breakdown

Format the cost breakdown:
- **Total cost** for the category
- **Sub-category breakdown** — each component's share
- **Cost as % of revenue** — context for cost magnitude
- **Trend** — increasing, decreasing, or stable vs prior period

### Step 4: Benchmarking

Where possible, provide context:
- Cost per order / per unit
- Cost as % of revenue compared across channels
- Largest cost drivers within the category
- Areas where costs appear above expected ranges

### Step 5: Follow-Up

Offer:
- **Another cost category** — run again with a different category
- **Unit economics** — `/jf-financial-analyst:unit-economics`
- **P&L report** — `/jf-financial-analyst:pnl-report`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If a cost category has no data, inform the user and suggest trying a different category
