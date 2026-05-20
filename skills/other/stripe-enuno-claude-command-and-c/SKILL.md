---
name: stripe
description: "Billing and payment operations for Stripe: customers, products, prices, invoices, payment links, subscriptions, refunds, disputes, balance. Triggers: create customer, create product, create invoice, generate payment link, query transactions, process refunds, manage subscriptions, view disputes, check balance. Money operations require confirmation. MCP is optional — works with Dashboard/CLI too."
allowed-tools:
  - Read
  - Bash
  - WebFetch
  - stripe_*
---

# Stripe Billing Operations

Execute billing and payment operations on Stripe: customers, products, invoices, payment links, subscriptions, refunds, and disputes.

> **MCP is optional.** This skill works with MCP (auto), Stripe CLI, or Dashboard. See [BACKENDS.md](BACKENDS.md) for execution options.

## Three Hard Rules

1. **Read before write** — Before creating customer/product/price, check if it already exists to avoid duplicates
2. **Money operations require confirmation** — Refunds, subscription changes, dispute updates must be confirmed before execution
3. **When in doubt, search** — If unsure about object ID or parameters, search first, don't guess

## Security Rules

| Operation Type | Rule |
|----------------|------|
| Read (list, get, search) | Execute directly |
| Create (customer, product, price, invoice) | Check for duplicates first |
| Money (refund, subscription cancel/update, dispute) | Display details → Await confirmation → Execute |
| Mode | Test mode by default. Live requires explicit "live mode" + double confirmation |

## Dangerous Actions (Require Confirmation)

Before executing these operations:

1. **Display** — Show object ID and key fields
2. **Explain impact** — Amount, timing, consequences
3. **Await confirmation** — Wait for explicit "confirm"/"yes"/"proceed"
4. **Execute and receipt** — Return result + object ID + status

| Action | Risk |
|--------|------|
| `create_refund` | Money leaves account |
| `cancel_subscription` | Revenue loss |
| `update_subscription` | Contract change |
| `update_dispute` | Legal implications |

Example confirmation prompt:
```
About to execute refund:
- PaymentIntent: pi_xxx
- Amount: $50.00 (full amount)
- Reason: requested_by_customer

Reply "confirm" to proceed, or "cancel" to abort.
```

## Common Workflows

### Create Customer
```
1. Search/list to check if customer exists (by email)
2. If not exists, create_customer(name, email, metadata)
3. Return cus_xxx + key info
```

### Create Product and Price
```
1. List products to check if already exists
2. create_product(name, description)
3. create_price(product=prod_xxx, unit_amount=cents, currency)
4. Return prod_xxx + price_xxx
```

### Create and Send Invoice
```
1. Confirm customer ID (list_customers if unknown)
2. create_invoice(customer=cus_xxx, collection_method, days_until_due)
3. create_invoice_item(invoice=inv_xxx, price=price_xxx, quantity)
4. finalize_invoice(invoice=inv_xxx)
5. Return inv_xxx + hosted_invoice_url
```

### Create Payment Link
```
1. Confirm price ID (list_prices if unknown)
2. create_payment_link(line_items=[{price, quantity}])
3. Return payment link URL
```

### Refund (Dangerous)
```
1. list_payment_intents to find target payment
2. Display pi_xxx + amount + customer info
3. Request user confirmation
4. create_refund(payment_intent=pi_xxx, amount?, reason)
5. Return re_xxx + status
```

### Cancel Subscription (Dangerous)
```
1. list_subscriptions(customer=cus_xxx) to find target
2. Display sub_xxx + status + next billing date
3. Ask: cancel immediately or at period end?
4. After confirmation, cancel_subscription(subscription=sub_xxx)
5. Return cancellation result
```

## Default Configuration

- **Currency**: Use user-specified; else use existing object's currency; else ask
- **Amount**: Accept decimals, auto-convert to smallest unit (e.g., $19.99 → 1999)
- **Output**: Object type + ID + key fields + next steps

## Limitations

These operations are NOT available via standard tools:
- ❌ Create PaymentIntent / charge directly
- ❌ Create subscription (only list/update/cancel)
- ❌ Create Promotion Code (only coupon)
- ❌ Delete objects

For these, use Dashboard or API directly.

## File-based Pipeline

When integrating into multi-step workflows:

```
runs/<workflow>/active/<run_id>/
├── proposal.md                # Requirements / objective
├── context.json               # Known IDs (customer, invoice, etc.)
├── tasks.md                   # Checklist + approval gate
├── evidence/stripe-actions.md # Operations to execute (money ops written here first)
├── evidence/receipt.md        # Results + object IDs
└── logs/events.jsonl          # Optional tool call summary (no sensitive data)
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Object doesn't exist | Search to find correct ID |
| Parameter error | Check documentation for correct format |
| Insufficient permissions | Check API key scope |
| Network error | Retry or check connection |

## Related Files

- [BACKENDS.md](BACKENDS.md) — Execution options (MCP/CLI/Dashboard)
- [SETUP.md](SETUP.md) — MCP configuration (optional)
- [tools.md](tools.md) — Detailed tool parameters
