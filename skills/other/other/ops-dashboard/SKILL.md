---
name: ops-dashboard
description: Generate a consolidated operations dashboard from multiple data sources
user-invocable: true
---

You are helping the operations team get a consolidated view of operations health.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_fulfillment_status`).

Follow these steps:

### Step 1: Pull All Data Sources

Gather data from three Snowflake tools in sequence:

1. `mcp__snowflake__get_fulfillment_status` — with channel "all" and days 7
2. `mcp__snowflake__get_inventory_health` — no parameters
3. `mcp__snowflake__get_fulfillment_exceptions` — with channel "all" and severity "all"

### Step 2: Build Dashboard

Present a consolidated operations dashboard with these sections:

**Fulfillment Performance**
- Overall SLA compliance rate
- Orders shipped today / this week
- Average time to ship
- Channels above/below SLA target

**Inventory Health**
- Total SKUs by risk tier (critical / warning / healthy)
- Top 5 critical SKUs needing immediate attention
- Days of inventory coverage (weighted average)

**Exception Summary**
- Open exceptions by severity (critical / warning / info)
- Most common exception types
- Channels with highest exception rates
- Oldest unresolved exceptions

### Step 3: Highlight Action Items

Create a prioritized action list:
1. Critical inventory shortages requiring immediate reorder
2. SLA breaches requiring customer communication
3. Exception patterns suggesting systemic issues
4. Upcoming risks based on trends

### Step 4: Follow-Up

Offer deep dives into any section:
- `/jf-operations-center:fulfillment-status` — SLA details
- `/jf-operations-center:inventory-alert` — inventory details
- `/jf-operations-center:fulfillment-exceptions` — exception details
- `/jf-operations-center:trace-order` — specific order investigation

### Error Handling

- If any Snowflake tool fails, build the dashboard from the tools that succeed and note which sections are unavailable
- If Snowflake MCP is entirely unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
