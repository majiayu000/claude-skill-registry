---
name: integrating-payment-gateways
description: Patterns for connecting payment providers (Stripe, etc.) with Appwrite. Use for handling secure transactions and updating booking status.
---

# Payment Gateway Integration

## When to use this skill
- When implementating actual "checkout" flows.
- When an order status needs to change from "pending" to "paid".

## Architecture
1.  **Client**: Redirect user to payment provider (Stripe Checkout).
2.  **Provider**: Sends a **Webhook** back to your Appwrite Function or Route Handler upon success.
3.  **Server**: Verifies the webhook signature.
4.  **Database**: Updates the booking document in Appwrite.

## Rules
- **Never Store CC Info**: Use tokens/checkouts provided by the gateway.
- **Idempotency**: Ensure that receiving the same webhook twice doesn't result in double bookings.

## Instructions
- **Test Mode**: Always use "Sandbox" or "Test" keys during development.
- **Logs**: Keep detailed logs of webhook transactions for debugging.
