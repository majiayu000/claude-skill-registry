---
name: mcp-stripe
description: "Stripe MCP transaction operations skill. Execute transaction operations via Stripe MCP server (https://mcp.stripe.com): customer management, products/prices, invoices, payment links, subscriptions, refunds, dispute handling, balance queries. Triggers: user requests Stripe operations including create customer, create product, create invoice, generate payment link, query transactions, process refunds, manage subscriptions, view disputes, check balance, etc."
disable-model-invocation: true
---

# Stripe MCP Transaction Skill

Execute transaction operations via Stripe MCP server.

## File-based Pipeline (Pass Paths Only)

When integrating billing operations into multi-step workflows, persist all context and artifacts to disk, passing only paths between agents/sub-agents.

Recommended directory structure (within project): `runs/<workflow>/active/<run_id>/`

- Input: `01-input/goal.md` (requirements), `01-input/context.json` (known customer/invoice/subscription/payment_intent IDs, etc.)
- Plan: `03-plans/stripe-actions.md` (list of operations to execute; money/contracts must be written here and await confirmation first)
- Output: `05-final/receipt.md` + `05-final/receipt.json` (object type + ID + key fields + next steps)
- Logs: `logs/events.jsonl` (summary of each tool call; do not log sensitive information verbatim)

## Connection Configuration

MCP Server: `https://mcp.stripe.com`

**Claude Code Connection**:
```bash
claude mcp add --transport http stripe https://mcp.stripe.com/
claude /mcp  # authenticate
```

**Authentication**: OAuth preferred; if API key needed, use restricted key as Bearer token.

**Mode**: Test mode by default. Switching to live requires user to explicitly say "live" and double confirmation.

## Three Hard Rules

1. **Read before write** - Before creating customer/product/price, first use `list_*` or `search_stripe_resources` to check if it already exists, avoid duplicate objects
2. **Money and contracts require confirmation** - `create_refund`, `cancel_subscription`, `update_subscription`, `update_dispute` must display content and get explicit user confirmation before execution
3. **When in doubt, search** - If unsure about object ID, fields, or approach, first call `search_stripe_documentation` or `search_stripe_resources`, don't guess parameters

## Available Tools

| Category | Tool | Description |
|----------|------|-------------|
| Account | `get_stripe_account_info` | Get account info |
| Balance | `retrieve_balance` | Query available/pending balance |
| Customer | `create_customer`, `list_customers` | Create/list customers |
| Product | `create_product`, `list_products` | Create/list products |
| Price | `create_price`, `list_prices` | Create/list prices |
| Invoice | `create_invoice`, `create_invoice_item`, `finalize_invoice`, `list_invoices` | Full invoice workflow |
| Payment Link | `create_payment_link` | Create shareable payment link |
| Payment Intent | `list_payment_intents` | List payment intents (query only) |
| Refund | `create_refund` | ⚠️ Dangerous - requires confirmation |
| Dispute | `list_disputes`, `update_dispute` | ⚠️ update requires confirmation |
| Subscription | `list_subscriptions`, `update_subscription`, `cancel_subscription` | ⚠️ update/cancel require confirmation |
| Coupon | `create_coupon`, `list_coupons` | Create/list coupons |
| Search | `search_stripe_resources`, `fetch_stripe_resources`, `search_stripe_documentation` | Search objects/documentation |

**Cannot do** (not in tool list):
- ❌ Create PaymentIntent / charge directly
- ❌ Create subscription (create_subscription)
- ❌ Create Promotion Code (only coupon)
- ❌ Delete objects

## Dangerous Action Handling Flow

Before executing `create_refund`, `cancel_subscription`, `update_subscription`, `update_dispute`:

1. **Display first** - List the object ID and key fields to be operated on
2. **Explain impact** - Refund amount/cancellation time/change content
3. **Request confirmation** - Wait for user to explicitly reply "confirm"/"yes"/"proceed"
4. **Execute and receipt** - Return operation result + object ID + status

Example confirmation prompt:
```
About to execute refund:
- PaymentIntent: pi_xxx
- Amount: £50.00 (full amount)
- Reason: requested_by_customer

Reply "confirm" to proceed, or "cancel" to abort.
```

## Default Configuration

- **Currency**: Prioritize user-specified currency; if not specified, use existing object currency (Price/Invoice/PaymentIntent); if still unclear, ask
- **Amount**: Accept decimal input, auto-convert to smallest unit integer (e.g., £19.99 → 1999)
- **Output receipt**: Object type + ID + key fields + next steps

## Common Workflows

### Create Customer
```
1. search_stripe_resources or list_customers to check if already exists
2. If not exists, create_customer(name, email, metadata)
3. Return cus_xxx + key info
```

### Create Product and Price
```
1. list_products to check if product already exists
2. create_product(name, description)
3. create_price(product=prod_xxx, unit_amount=amount in smallest unit, currency="gbp", recurring if needed)
4. Return prod_xxx + price_xxx
```

### Create and Send Invoice
```
1. Confirm customer ID (if unknown, query with list_customers)
2. create_invoice(customer=cus_xxx, collection_method, days_until_due)
3. create_invoice_item(invoice=inv_xxx, price=price_xxx, quantity)
4. finalize_invoice(invoice=inv_xxx)
5. Return inv_xxx + hosted_invoice_url
```

### Create Payment Link
```
1. Confirm price ID (if unknown, query with list_prices)
2. create_payment_link(line_items=[{price, quantity}], after_completion if needed)
3. Return payment link URL
```

### Refund (Dangerous)
```
1. list_payment_intents to find target payment
2. Display pi_xxx + amount + customer info
3. Request user confirmation
4. After confirmation, create_refund(payment_intent=pi_xxx, amount for partial refund, reason)
5. Return re_xxx + status
```

### Cancel Subscription (Dangerous)
```
1. list_subscriptions(customer=cus_xxx) to find target
2. Display sub_xxx + current status + next billing date
3. Ask: cancel immediately or at period end (cancel_at_period_end)
4. After confirmation, cancel_subscription(subscription=sub_xxx)
5. Return cancellation result
```

## Tool Parameter Details

See [tools.md](tools.md)

## Error Handling

- **Object doesn't exist**: Use search_stripe_resources or fetch_stripe_resources to find correct ID
- **Parameter error**: Use search_stripe_documentation to query correct parameter format
- **Insufficient permissions**: Prompt user to check API key permission scope
- **Network error**: Suggest retry or check MCP connection status
