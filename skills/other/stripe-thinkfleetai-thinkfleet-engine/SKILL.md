---
name: stripe
description: "Manage Stripe payments — customers, charges, subscriptions, invoices, and refunds."
metadata: {"thinkfleetbot":{"emoji":"💳","requires":{"bins":["curl","jq"],"env":["STRIPE_SECRET_KEY"]}}}
---

# Stripe

Manage customers, payments, subscriptions, and invoices via the Stripe API.

## Environment Variables

- `STRIPE_SECRET_KEY` - Stripe secret key (starts with `sk_`)

## List customers

```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/customers?limit=10" | jq '.data[] | {id, email, name}'
```

## Create payment intent

```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/payment_intents" \
  -d "amount=2000" -d "currency=usd" | jq '{id, amount, currency, status}'
```

## List charges

```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/charges?limit=10" | jq '.data[] | {id, amount, currency, status}'
```

## List subscriptions

```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/subscriptions?limit=10" | jq '.data[] | {id, customer, status, current_period_end}'
```

## List invoices

```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/invoices?limit=10" | jq '.data[] | {id, customer, total, status}'
```

## Issue refund

```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/refunds" \
  -d "charge=ch_xxx" | jq '{id, amount, status}'
```

## Notes

- Amounts are in cents (2000 = $20.00).
- Always confirm before creating charges or refunds.
- Use test keys (`sk_test_`) for development.
