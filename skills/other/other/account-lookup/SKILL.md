---
name: account-lookup
description: Look up customer details across promo and wholesale stores
user-invocable: true
---

You are helping the sales team look up customer account information.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__search_accounts`).

Follow these steps:

### Step 1: Get Search Criteria

Ask the user for any of:
- Customer name (partial match supported)
- Email address
- Company name
- Shopify customer ID

### Step 2: Search Across Stores

Use `mcp__promo-order__search_accounts` to search the promo store. The MCP promo-order server has read access to both:
- **Promo store** — promotional and sample order history
- **Wholesale store** — wholesale order history (read-only)

### Step 3: Present Results

For each matching customer, display:
- Name, email, company
- Shipping address
- Tags and notes
- Order count and total spend (if available)
- Which store(s) they appear in

If the customer exists in both stores, present a unified view noting the source of each data point.

### Step 4: Follow-Up Actions

After showing the account, offer:
- View recent order history (`/jf-sales-command:order-history`)
- Create a new promo order (`/jf-sales-command:create-promo-order`)
- Search for a different customer

### Error Handling

- If no results found, suggest alternative search terms or check for typos
- If MCP tools are unavailable, inform the user the promo-order server may need reconnection
