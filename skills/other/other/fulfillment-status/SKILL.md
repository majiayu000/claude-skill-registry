---
name: fulfillment-status
description: Check fulfillment SLA status by channel and timeframe
user-invocable: true
---

You are helping the operations team check fulfillment SLA performance.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_fulfillment_status`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user for:
- **Channel**: Which sales channel? (e.g., DTC, Amazon, Wholesale, or "all")
- **Timeframe**: How many days to look back? (default: 7)

### Step 2: Pull Fulfillment Status

Use `mcp__snowflake__get_fulfillment_status` with the user's channel and days parameters.

### Step 3: Present Results

Format the SLA data clearly:
- Overall SLA compliance rate (% of orders meeting target)
- Breakdown by fulfillment stage (pick, pack, ship, deliver)
- Any channels or stages falling below SLA thresholds
- Trend vs previous period if available

Highlight any SLA breaches in bold.

### Step 4: Follow-Up

Offer:
- **Drill into exceptions** — `/jf-operations-center:fulfillment-exceptions`
- **Full ops dashboard** — `/jf-operations-center:ops-dashboard`
- **Trace a specific order** — `/jf-operations-center:trace-order`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If no data is returned for the specified channel, suggest trying "all" or a different channel name
