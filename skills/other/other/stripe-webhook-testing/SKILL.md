---
name: stripe-webhook-testing
description: Set up Stripe CLI to forward webhooks to local development server for testing Stripe integrations
---

# Stripe Webhook Testing Skill

This skill should be used when the user wants to test Stripe webhooks locally during development.

## Prerequisites

- Stripe CLI installed (`brew install stripe/stripe-cli/stripe` on macOS)
- Backend server running on port 3000
- Stripe test mode API keys configured in `.env`

## Setup Process

### Step 1: Ensure Webhook Endpoint Exists

The backend must have a webhook endpoint at `/api/stripe/webhook`. Verify this in:
- `backend/src/main.rs` - route definition
- `backend/src/handlers/stripe_handlers.rs` - handler implementation

### Step 2: Start Backend Server

Ensure the backend is running:
```bash
cd backend && cargo run
```

The server must be running before starting Stripe CLI forwarding.

### Step 3: Start Stripe CLI Forwarding

Run the following command to forward webhooks to localhost:
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

The CLI will output a webhook secret starting with `whsec_...`.

### Step 4: Configure Webhook Secret

1. Copy the webhook secret from the CLI output
2. Add or update `STRIPE_WEBHOOK_SECRET` in `backend/.env`:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxx
   ```
3. Restart the backend server to pick up the new secret

### Step 5: Trigger Test Events

Use Stripe CLI to trigger test webhook events:

```bash
# Subscription events
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted

# Checkout events
stripe trigger checkout.session.completed

# Invoice events
stripe trigger invoice.paid
stripe trigger invoice.payment_failed
```

### Step 6: Verify in Logs

Check backend console output for:
- "Stripe webhook received"
- "Stripe signature header found"
- "Stripe event verified successfully"
- Processing messages for specific event types

## Supported Webhook Events

The backend currently handles:
- `customer.subscription.created` - New subscription activated
- `customer.subscription.updated` - Subscription modified
- `customer.subscription.deleted` - Subscription cancelled
- `checkout.session.completed` - Checkout completed

## Troubleshooting

- **Signature verification failed**: Ensure `STRIPE_WEBHOOK_SECRET` matches the secret from `stripe listen`
- **Endpoint not found**: Verify backend is running on port 3000
- **Events not triggering**: Run `stripe listen` first, then trigger events in a new terminal
