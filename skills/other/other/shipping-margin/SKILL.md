---
name: shipping-margin
description: Analyze shipping cost margins by channel and carrier
user-invocable: true
---

You are helping the operations team analyze shipping cost margins.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_cost_breakdown`).

Follow these steps:

### Step 1: Gather Context

Ask the user what they want to analyze:
- **Channel focus**: Specific channel (DTC, Amazon, Wholesale) or all?
- **Cost category**: Fulfillment costs, shipping costs, or both?
- **Comparison**: vs budget, vs previous period, or absolute numbers?

### Step 2: Pull Cost Data

Use `mcp__snowflake__get_cost_breakdown` with category "fulfillment" to get shipping and fulfillment cost data.

Then use `mcp__snowflake__get_unit_economics` to get per-unit shipping margins by channel.

### Step 3: Analyze Margins

Calculate and present:
- **Shipping cost per order** by channel
- **Shipping as % of revenue** by channel
- **Fulfillment cost per unit** by product type
- **Margin impact** — how shipping costs affect gross margin
- **Channel comparison** — which channels have best/worst shipping economics

### Step 4: Identify Opportunities

Highlight:
- Channels where shipping costs are above target
- Products where shipping cost exceeds margin threshold
- Opportunities to optimize (consolidation, carrier negotiation, packaging)

### Step 5: Follow-Up

Offer:
- **Unit economics deep dive** — `/jf-operations-center:shipping-margin` with different parameters
- **Full cost analysis** — available via `mcp__snowflake__get_cost_breakdown` with other categories
- **Ops dashboard** — `/jf-operations-center:ops-dashboard`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If cost data is incomplete, note which data points are missing and suggest checking data freshness
