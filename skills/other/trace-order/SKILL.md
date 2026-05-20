---
name: trace-order
description: Trace an order through the fulfillment pipeline by order number
user-invocable: true
---

You are helping the operations team trace a specific order through the fulfillment pipeline.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__query`).

Follow these steps:

### Step 1: Get Order Identifier

Ask the user for the order number (e.g., Shopify order number, fulfillment ID, or tracking number).

### Step 2: Look Up Order

Use `mcp__snowflake__query` to search for the order across relevant tables. Start with:

```sql
SELECT * FROM SIGMA_ANALYTICS.PRODUCTION_OPERATIONS.ORDER_FULFILLMENT
WHERE ORDER_NUMBER = '{order_number}'
   OR FULFILLMENT_ID = '{order_number}'
   OR TRACKING_NUMBER = '{order_number}'
LIMIT 10
```

If no results, try broader searches using `mcp__snowflake__search_tables` to find the right table, then query it.

### Step 3: Build Timeline

Present the order's journey through the pipeline:
1. **Order placed** — date, channel, customer
2. **Payment captured** — date, amount, method
3. **Sent to fulfillment** — date, warehouse
4. **Picked/packed** — date, picker, box dimensions
5. **Shipped** — date, carrier, tracking number
6. **Delivered** — date, proof of delivery

Mark any stages that are missing or delayed.

### Step 4: Identify Issues

If the order is delayed or stuck:
- Identify which stage is the bottleneck
- Calculate how long it has been at that stage
- Compare against SLA targets
- Suggest next steps (escalation, carrier contact, etc.)

### Step 5: Follow-Up

Offer:
- **Check fulfillment exceptions** — `/jf-operations-center:fulfillment-exceptions`
- **Trace another order**
- **View channel SLA status** — `/jf-operations-center:fulfillment-status`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If the order is not found, ask the user to verify the order number and suggest alternative identifiers
- If tables are not found, use `mcp__snowflake__list_tables` to discover available operations tables
