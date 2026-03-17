---
name: unit-economics
description: Analyze per-unit economics by channel
user-invocable: true
---

You are helping the finance team analyze unit economics across sales channels.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_unit_economics`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user:
- **Channel**: Which channel to analyze? (e.g., DTC, Amazon, Wholesale, or "all" for comparison)

### Step 2: Pull Unit Economics

Use `mcp__snowflake__get_unit_economics` with the user's channel parameter.

### Step 3: Present Results

For each channel, show the per-unit waterfall:
- **Average selling price (ASP)**
- **COGS per unit**
- **Fulfillment cost per unit** (pick, pack, ship)
- **Payment processing per unit**
- **Marketing cost per unit** (if available, e.g., CAC / units)
- **Contribution margin per unit**
- **Contribution margin %**

### Step 4: Cross-Channel Comparison

If multiple channels:
- Rank channels by contribution margin %
- Identify which cost components drive the differences
- Highlight the most and least profitable channels

### Step 5: Follow-Up

Offer:
- **Cost breakdown** — `/jf-financial-analyst:cost-analysis`
- **P&L report** — `/jf-financial-analyst:pnl-report`
- **Scenario modeling** — `/jf-financial-analyst:scenario-model` to test price or cost changes

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If unit economics data is incomplete, note which cost components are available
