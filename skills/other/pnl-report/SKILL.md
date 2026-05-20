---
name: pnl-report
description: Generate a P&L summary report by channel and period
user-invocable: true
---

You are helping the finance team generate a profit and loss summary.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_pnl_summary`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user for:
- **Channel**: Which sales channel? (e.g., DTC, Amazon, Wholesale, or "all")
- **Period**: What time period? (month, quarter, or year)

### Step 2: Pull P&L Data

Use `mcp__snowflake__get_pnl_summary` with the user's channel and period parameters.

### Step 3: Present the P&L

Format as a standard income statement:
- **Gross Revenue** — total sales by channel
- **Discounts & Returns** — deductions from gross
- **Net Revenue** — gross minus deductions
- **COGS** — cost of goods sold
- **Gross Profit** — net revenue minus COGS
- **Gross Margin %** — gross profit as percentage of net revenue
- **Operating Expenses** — fulfillment, marketing, overhead (if available)
- **Net Income** — bottom line (if available)

### Step 4: Highlight Key Metrics

Call out:
- Gross margin % vs target
- Largest cost drivers
- Channel-level comparison if multiple channels
- Period-over-period change if data supports it

### Step 5: Follow-Up

Offer:
- **Unit economics** — `/jf-financial-analyst:unit-economics`
- **Cost breakdown** — `/jf-financial-analyst:cost-analysis`
- **Variance analysis** — `/jf-financial-analyst:variance-analysis`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If data is incomplete for the requested period, note which line items are available
