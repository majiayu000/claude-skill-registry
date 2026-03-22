---
name: stripe
description: >
  Interact with Stripe via REST API. List customers, payments, payouts, connected accounts,
  check balances, view webhook events, and manage Stripe Connect. Use for any Stripe
  administration, debugging, or data inspection task.
allowed-tools: Bash, Read, Grep, Glob
---

# Stripe REST API

Manage FuzzyCat's Stripe account via curl. The test-mode secret key is in `.env.local`.

## Authentication

```bash
STRIPE_SK=$(grep STRIPE_SECRET_KEY .env.local | cut -d'"' -f2)
# All curl commands use: -u "$STRIPE_SK:"
```

## Common Commands

### Account & Balance

```bash
# Account info
curl -s https://api.stripe.com/v1/account -u "$STRIPE_SK:" | python3 -m json.tool

# Balance
curl -s https://api.stripe.com/v1/balance -u "$STRIPE_SK:" | python3 -m json.tool
```

### Customers

```bash
# List customers (most recent 10)
curl -s "https://api.stripe.com/v1/customers?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# Get specific customer
curl -s "https://api.stripe.com/v1/customers/cus_xxx" -u "$STRIPE_SK:" | python3 -m json.tool

# Search customers by email
curl -s "https://api.stripe.com/v1/customers/search" -u "$STRIPE_SK:" \
  -d "query=email:'owner@example.com'" | python3 -m json.tool
```

### Payments & Payment Intents

```bash
# List recent payments
curl -s "https://api.stripe.com/v1/payment_intents?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# Get specific payment intent
curl -s "https://api.stripe.com/v1/payment_intents/pi_xxx" -u "$STRIPE_SK:" | python3 -m json.tool

# List charges
curl -s "https://api.stripe.com/v1/charges?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool
```

### Stripe Connect (Connected Accounts)

```bash
# List connected accounts
curl -s "https://api.stripe.com/v1/accounts?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# Get specific connected account
curl -s "https://api.stripe.com/v1/accounts/acct_xxx" -u "$STRIPE_SK:" | python3 -m json.tool

# List transfers to connected accounts
curl -s "https://api.stripe.com/v1/transfers?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool
```

### Checkout Sessions

```bash
# List checkout sessions
curl -s "https://api.stripe.com/v1/checkout/sessions?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# Get specific session
curl -s "https://api.stripe.com/v1/checkout/sessions/cs_xxx" -u "$STRIPE_SK:" | python3 -m json.tool
```

### Webhooks

```bash
# List webhook endpoints
curl -s "https://api.stripe.com/v1/webhook_endpoints?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# List recent events
curl -s "https://api.stripe.com/v1/events?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# Filter events by type
curl -s "https://api.stripe.com/v1/events?limit=10&type=payment_intent.succeeded" -u "$STRIPE_SK:" | python3 -m json.tool
```

### Subscriptions & Prices (if used)

```bash
# List products
curl -s "https://api.stripe.com/v1/products?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool

# List prices
curl -s "https://api.stripe.com/v1/prices?limit=10" -u "$STRIPE_SK:" | python3 -m json.tool
```

## FuzzyCat-Specific

- **Payment model**: Destination charges with `application_fee_amount` (not separate transfers)
- **Connect type**: Standard accounts for clinics
- **Deposit**: Stripe Checkout session with debit card
- **Installments**: ACH Direct Debit via Payment Intents
- **Key files**: `server/services/stripe/` (index, connect, checkout, ach, customer), `server/services/payout.ts`

## Tips

- Always use `-u "$STRIPE_SK:"` (note the trailing colon — prevents password prompt)
- Test mode keys start with `sk_test_`; live keys start with `sk_live_`
- Use `| python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0])"` to extract specific items
- Add `?expand[]=data.customer` to expand nested objects inline
