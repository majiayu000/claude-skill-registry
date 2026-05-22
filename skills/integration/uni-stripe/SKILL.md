---
name: uni-stripe
description: |
  Stripe payments via uni CLI. Use when user wants to check balance, create payment links, manage customers, invoices, refunds, or subscriptions.
  Requires STRIPE_SECRET_KEY or run 'uni stripe auth'.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Stripe (uni)

Manage Stripe payments from the terminal. Requires API key setup.

## Authentication

```bash
uni stripe auth sk_test_xxx       # Set API key directly
uni stripe auth --status          # Check configuration
uni stripe auth --logout          # Remove credentials

# Or use environment variable
export STRIPE_SECRET_KEY="sk_test_xxx"
```

Get keys from: https://dashboard.stripe.com/apikeys

## Balance

```bash
uni stripe balance                # Check account balance
uni stripe bal                    # Alias
```

## Payments

```bash
uni stripe payments               # List recent payments
uni stripe payments -n 20         # More payments
uni stripe payments pi_xxx        # View specific payment
```

## Payment Links

```bash
uni stripe link 50                # Create $50 payment link
uni stripe link 99.99 -d "Consulting"  # With description
uni stripe link 100 -c eur        # Different currency
uni stripe link --list            # List existing links
```

## Customers

```bash
uni stripe customers              # List customers
uni stripe customers john@example.com -n "John Doe"  # Create
uni stripe customers cus_xxx      # View specific customer
```

## Invoices

```bash
uni stripe invoices                              # List invoices
uni stripe invoices create --customer cus_xxx -a 100 -d "Service"
uni stripe invoices send in_xxx                  # Send invoice
```

## Refunds

```bash
uni stripe refunds                # List refunds
uni stripe refunds pi_xxx         # Refund a payment
uni stripe refunds pi_xxx -a 25   # Partial refund ($25)
uni stripe refunds pi_xxx -r requested_by_customer
```

## Subscriptions

```bash
uni stripe subs                   # List subscriptions
uni stripe subs sub_xxx           # View subscription
uni stripe subs cancel sub_xxx    # Cancel subscription
```

## Products

```bash
uni stripe products               # List products
uni stripe products --prices      # With pricing info
uni stripe products "Pro Plan" -d "Full access"  # Create product
```

## Notes

- Use `sk_test_...` for testing, `sk_live_...` for production
- All amounts are in the smallest currency unit (cents for USD)
- IDs shown in output `[xxx]` can be used in subsequent commands
- Test mode is clearly indicated in output
