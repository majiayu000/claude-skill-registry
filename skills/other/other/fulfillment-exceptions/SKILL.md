---
name: fulfillment-exceptions
description: View fulfillment exceptions filtered by channel and severity
user-invocable: true
---

You are helping the operations team review fulfillment exceptions that need attention.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_fulfillment_exceptions`).

Follow these steps:

### Step 1: Gather Filters

Ask the user for:
- **Channel**: Which sales channel? (e.g., DTC, Amazon, Wholesale, or "all")
- **Severity**: Filter by severity? (e.g., critical, warning, or "all")

### Step 2: Pull Exceptions

Use `mcp__snowflake__get_fulfillment_exceptions` with the user's channel and severity parameters.

### Step 3: Present Results

Organize exceptions by severity:
- **Critical** — orders that have missed SLA or require immediate intervention
- **Warning** — orders at risk of missing SLA
- **Info** — minor issues or anomalies

For each exception, show:
- Order number and channel
- Exception type (delay, damage, address issue, inventory shortage, etc.)
- Age of the exception (how long since it was flagged)
- Current status and any resolution steps taken

### Step 4: Summarize

Provide:
- Total exception count by severity
- Most common exception types
- Channels with highest exception rates
- Recommended priority actions

### Step 5: Follow-Up

Offer:
- **Trace a specific order** — `/jf-operations-center:trace-order`
- **View SLA status** — `/jf-operations-center:fulfillment-status`
- **Full ops dashboard** — `/jf-operations-center:ops-dashboard`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If no exceptions are found, confirm that this is good news and suggest reviewing SLA status for context
