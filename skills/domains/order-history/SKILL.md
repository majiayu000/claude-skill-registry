---
name: order-history
description: View order history for a customer with recency analysis
user-invocable: true
---

You are helping the sales team review a customer's order history.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__search_accounts`).

Follow these steps:

### Step 1: Identify the Customer

Ask the user for the customer name, email, or Shopify customer ID. Use `mcp__promo-order__search_accounts` to resolve.

### Step 2: Retrieve Order History

Use `mcp__promo-order__get_order_history` to fetch the customer's order history. Include both promo and wholesale orders if available.

### Step 3: Present Order History

Display orders in reverse chronological order:
- Order ID, date, status
- Line items and quantities
- Order type (promo/sample/wholesale)
- Fulfillment status

### Step 4: Recency Analysis

Calculate and highlight:
- **Last order date** and days since
- **90-day recency flag**: If last order > 90 days ago, flag as "lapsed" and suggest re-engagement
- **Order frequency**: Average days between orders
- **Top products**: Most frequently ordered items

### Step 5: Recommendations

Based on the history:
- If lapsed (>90 days): Suggest a re-engagement promo order
- If active: Note the typical reorder window
- If first-time: Note as new account, suggest a sample order

### Error Handling

- If customer not found, offer to search by different criteria
- If no orders exist, note the customer has no order history yet
