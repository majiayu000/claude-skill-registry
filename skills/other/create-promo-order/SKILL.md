---
name: create-promo-order
description: Create a promotional or sample order for a customer
user-invocable: true
---

You are helping the sales team create a promotional or sample order.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__search_accounts`).

Follow these steps:

### Step 1: Identify the Customer

Ask the user for the customer name or email. Use `mcp__promo-order__search_accounts` to find the customer record.

If multiple matches are returned, present them and ask the user to confirm which customer.

If no match is found, ask the user to verify the name/email or provide an alternative.

### Step 2: Choose Order Type

Ask the user:
- **Promo order** — 100% discounted draft order for promotional purposes
- **Sample order** — 100% discounted draft order for product sampling

### Step 3: Select Products

Use `mcp__promo-order__check_products` to show available products with current inventory levels.

Let the user select products and quantities. Validate that:
- Requested quantities are available in inventory
- Products are eligible for promo/sample orders

### Step 4: Collect Required Tracking Fields

Call `mcp__promo-order__list_metafield_options` to get valid values for:
- **internal_requestor** — who is requesting this order (e.g., "Gordon Divine", "Brian Littlefield")
- **promo_order_type** — the purpose (e.g., "Wholesale/DSD Account Sampling", "Trade Shows and Events")

Present the options and ask the user to select one of each. These are required on every order.

### Step 5: Confirm and Create

Display a summary:
- Customer name and shipping address
- Order type (promo/sample)
- Line items with quantities
- Total retail value (pre-discount)
- Internal requestor and order type

After user confirmation, use `mcp__promo-order__create_promo_order` with:
- `customer_id`: from Step 1
- `variant_ids`: comma-separated variant IDs from Step 3
- `quantities`: comma-separated quantities matching variants
- `note`: any notes from the user
- `internal_requestor`: from Step 4
- `promo_order_type`: from Step 4

### Step 6: Report Result

Show the created draft order ID and link. Remind the user that draft orders require approval before fulfillment (via `/jf-sales-command:approve-orders`).

### Error Handling

- If MCP tools are unavailable, inform the user that the promo-order server may need reconnection
- If inventory is insufficient, suggest alternative products or reduced quantities
- If customer creation is needed, direct the user to the Shopify admin
