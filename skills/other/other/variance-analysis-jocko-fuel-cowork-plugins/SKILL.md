---
name: variance-analysis
description: Analyze period-over-period financial variance across channels
user-invocable: true
---

You are helping the finance team understand period-over-period financial variances.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_pnl_summary`).

Follow these steps:

### Step 1: Define Comparison

Ask the user:
- **Metric focus**: Revenue, COGS, margin, or full P&L?
- **Current period**: Which period to analyze? (e.g., "this month", "Q1 2026")
- **Comparison period**: What to compare against? (e.g., "last month", "same month last year")
- **Channel**: Specific channel or all?

### Step 2: Pull Data for Both Periods

Use `mcp__snowflake__get_pnl_summary` for each period. Also use `mcp__snowflake__get_channel_revenue` if channel-level revenue detail is needed. Use `mcp__snowflake__get_unit_economics` for per-unit variance.

### Step 3: Calculate Variances

For each metric, calculate:
- **Absolute variance** — current period minus comparison period
- **Percentage variance** — (current - comparison) / comparison * 100
- **Direction** — favorable or unfavorable

### Step 4: Root Cause Analysis

For the largest variances, investigate:
- Is the variance driven by volume changes or price/cost changes?
- Which channels or products are the biggest contributors?
- Are there one-time items distorting the comparison?
- Delegate to the `forecast-root-cause-analyzer` agent for deeper analysis if needed

### Step 5: Present Results

Format as a variance report:
- Summary table with current, prior, and variance columns
- Top 3-5 drivers of the variance
- Favorable vs unfavorable breakdown
- Recommendations or areas requiring attention

### Step 6: Follow-Up

Offer:
- **P&L report** — `/jf-financial-analyst:pnl-report`
- **Scenario modeling** — `/jf-financial-analyst:scenario-model`
- **Demand forecast** — `/jf-financial-analyst:forecast-demand`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If comparison period data is incomplete, note which metrics can and cannot be compared
