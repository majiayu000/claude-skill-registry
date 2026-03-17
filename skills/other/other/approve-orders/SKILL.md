---
name: approve-orders
description: Approve promo orders for 3PL fulfillment
user-invocable: true
---

You are helping the sales team approve draft promo orders for fulfillment.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__get_pending_orders`).

Follow these steps:

### Step 1: Show Pending Orders

Ask the user which orders to show:
- **All pending** — use `mcp__promo-order__get_pending_orders` (all draft orders)
- **MCP-created only** — use `mcp__promo-order__get_mcp_pending_orders` (filters to orders created via MCP, tagged 'mcp-created')

Use `include_details=true` to get line items and shipping addresses.

Display them in a table with Order ID, Customer, Items, and Value.

If the user specified particular order IDs, filter to just those.

### Step 2: Review and Confirm

For each order to approve, show the full details:
- Customer name and shipping address
- Line items with quantities
- Order type and total retail value
- Any notes or tags

Ask the user to confirm which orders to approve. Accept:
- "All" to approve everything shown
- Specific order IDs (comma-separated)
- "All except [IDs]"

### Step 3: Execute Approvals

Use `mcp__promo-order__approve_orders` with:
- `draft_order_ids`: comma-separated list of IDs, or `"all"` to approve all MCP-created drafts
- `confirm`: `true` (required safety check)

**This is an irreversible action.** Confirm with the user before executing.

### Step 4: Report Results

Show results:
- Order ID | Customer | Status | Notes
- Summary: N approved, N skipped, N failed

Approved orders are marked as paid and queued for 3PL fulfillment.

### Error Handling

- If an order fails to approve, show the error — the batch continues with remaining orders
- If the order was already approved or cancelled, the result will note the current status
- Never auto-approve without explicit user confirmation
