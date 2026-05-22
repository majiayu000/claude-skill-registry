---
name: stripe-billing
description: Stripe payment and billing operations with progressive disclosure
allowed-tools: [Bash, Read]
---

# Stripe Billing Skill

## Overview

Provides 90%+ context savings compared to raw Stripe MCP server by loading only relevant operations on-demand.

## Requirements

- STRIPE_SECRET_KEY environment variable (required)
- STRIPE_WEBHOOK_SECRET environment variable (optional, for webhooks)
- stripe Python package or Stripe CLI

## Tools (Progressive Disclosure)

### Customer Operations

| Tool            | Description                 | Confirmation |
| --------------- | --------------------------- | ------------ |
| list-customers  | List customers with filters | No           |
| get-customer    | Get customer details        | No           |
| create-customer | Create new customer         | Yes          |
| update-customer | Update customer info        | Yes          |

### Subscription Operations

| Tool                | Description              | Confirmation |
| ------------------- | ------------------------ | ------------ |
| list-subscriptions  | List subscriptions       | No           |
| get-subscription    | Get subscription details | No           |
| create-subscription | Create subscription      | Yes          |
| cancel-subscription | Cancel subscription      | Yes          |
| update-subscription | Modify subscription      | Yes          |

### Invoice Operations

| Tool             | Description          | Confirmation |
| ---------------- | -------------------- | ------------ |
| list-invoices    | List invoices        | No           |
| get-invoice      | Get invoice details  | No           |
| create-invoice   | Create draft invoice | Yes          |
| finalize-invoice | Finalize invoice     | Yes          |
| pay-invoice      | Pay invoice          | Yes          |

### Payment Operations

| Tool            | Description           | Confirmation |
| --------------- | --------------------- | ------------ |
| list-payments   | List payment intents  | No           |
| get-payment     | Get payment details   | No           |
| create-payment  | Create payment intent | Yes          |
| confirm-payment | Confirm payment       | Yes          |
| refund-payment  | Issue refund          | Yes          |

### Product/Price Operations

| Tool           | Description    | Confirmation |
| -------------- | -------------- | ------------ |
| list-products  | List products  | No           |
| list-prices    | List prices    | No           |
| create-product | Create product | Yes          |
| create-price   | Create price   | Yes          |

## Quick Reference

```bash
# List customers
stripe customers list --limit 10

# Get subscription
stripe subscriptions retrieve sub_xxx

# Create payment intent
stripe payment_intents create --amount 2000 --currency usd
```

## Configuration

- **STRIPE_SECRET_KEY**: API key (sk_test_xxx or sk_live_xxx)
- **STRIPE_WEBHOOK_SECRET**: Webhook signing secret (whsec_xxx)

## Security

⚠️ **NEVER expose API keys in logs or output**
⚠️ **Test mode keys (sk*test*) for development only**
⚠️ **All write operations require confirmation**

## Agent Integration

- **developer** (primary): Payment integrations
- **analyst** (secondary): Billing analytics

## Troubleshooting

| Issue           | Solution                       |
| --------------- | ------------------------------ |
| Invalid API key | Check STRIPE_SECRET_KEY format |
| Rate limited    | Implement exponential backoff  |
| Webhook failed  | Verify STRIPE_WEBHOOK_SECRET   |
