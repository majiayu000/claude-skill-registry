---
name: backorder-status
description: Check partial fulfillment and backorder status for open orders
user-invocable: true
---

You are helping the operations team check on partially fulfilled and backordered orders.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__query`).

Follow these steps:

### Step 1: Determine Scope

Ask the user:
- **Specific order?** — provide an order number to check
- **All backorders?** — see all orders with partial fulfillment or backorder status
- **Channel filter?** — limit to a specific sales channel

### Step 2: Query Backorder Data

Use `mcp__snowflake__query` to find orders with partial fulfillment. Start by discovering available tables:

Use `mcp__snowflake__search_tables` with query "fulfillment" or "order" to find the right tables.

Then query for orders where fulfillment is incomplete:
- Orders with multiple fulfillments where some items are still pending
- Orders flagged as backordered
- Orders where line item quantity exceeds fulfilled quantity

### Step 3: Present Results

For each backordered/partial order:
- Order number and date
- Customer name and channel
- Items fulfilled vs items pending
- Reason for backorder (if available)
- Estimated resolution date (if available)

### Step 4: Summarize

Provide:
- Total orders with backorder/partial status
- Total units pending fulfillment
- Average age of backorders
- Most common products on backorder

### Step 5: Follow-Up

Offer:
- **Trace a specific order** — `/jf-operations-center:trace-order`
- **Inventory health check** — `/jf-operations-center:inventory-alert`
- **Demand forecast** for backordered products — via `mcp__snowflake__get_demand_forecast`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If no backorders are found, confirm the positive status and suggest checking inventory alerts for proactive monitoring
- If table structure is unfamiliar, use `mcp__snowflake__describe_table` to understand available columns
