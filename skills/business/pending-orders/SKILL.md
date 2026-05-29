---
name: pending-orders
description: List all draft orders awaiting approval
user-invocable: true
---

You are helping the sales team review pending draft orders.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__get_pending_orders`).

Follow these steps:

### Step 1: Retrieve Pending Orders

Ask the user which view they prefer:
- **All pending orders** — `mcp__promo-order__get_pending_orders` (all draft orders in the store)
- **MCP-created only** — `mcp__promo-order__get_mcp_pending_orders` (filters to orders created via this tool, tagged 'mcp-created')

Default to all pending unless the user asks for MCP-only.

Use `include_details=true` to get line items and shipping addresses.

### Step 2: Present the Queue

Display pending orders in a table:
- Order ID | Customer | Created Date | Type | Items | Value | Created By

Sort by creation date (oldest first — these need attention).

### Step 3: Summary Stats

Show:
- Total pending orders
- Total retail value of pending orders
- Oldest pending order (days waiting)
- Breakdown by order type (promo vs sample)

### Step 4: Actions

Offer the user:
- **Approve specific orders** — `/jf-sales-command:approve-orders`
- **View details** on a specific order
- **Filter** by date range, customer, or order type

### Error Handling

- If no pending orders exist, confirm the queue is clear
- If MCP tools are unavailable, inform the user the promo-order server may need reconnection
