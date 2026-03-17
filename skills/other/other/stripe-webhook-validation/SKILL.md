---
name: stripe-webhook-validation
description: |
  Fix for Stripe webhook signature validation failures in the payments app.
  Use when: "Stripe webhook signature verification failed", "Invalid signature",
  "No signatures found matching the expected signature", webhook 400 errors.
  Only loads when working in apps/payments/.
author: Memory Forge
version: 1.0.0
date: 2025-01-28
---

# Stripe Webhook Signature Validation Fix

## Problem

Stripe webhook signature validation fails with "No signatures found matching the expected signature" even when the webhook secret is correct.

## Trigger Conditions

- Error: `Stripe webhook signature verification failed`
- Error: `No signatures found matching the expected signature`
- HTTP 400 on `/webhooks/stripe` endpoint
- Working in `apps/payments/` directory

## Solution

### Step 1: Check Raw Body Parsing

The most common cause is body parsing middleware modifying the request body before signature verification.

```typescript
// WRONG: Body already parsed
app.use(express.json());
app.post('/webhooks/stripe', stripeWebhook); // ❌ Body is already parsed

// CORRECT: Use raw body for webhook endpoint
app.post('/webhooks/stripe',
  express.raw({ type: 'application/json' }), // ✅ Raw body
  stripeWebhook
);
app.use(express.json()); // Parse JSON for other routes
```

### Step 2: Verify Signature with Raw Body

```typescript
const stripeWebhook = (req: Request, res: Response) => {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  try {
    // req.body must be the raw buffer, not parsed JSON
    const event = stripe.webhooks.constructEvent(
      req.body, // Raw buffer
      sig,
      webhookSecret
    );
    // Handle event...
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
};
```

### Step 3: NestJS Specific Fix

For NestJS, use `rawBody` option:

```typescript
// main.ts
const app = await NestFactory.create(AppModule, {
  rawBody: true, // Enable raw body access
});

// webhook.controller.ts
@Post('stripe')
async handleStripeWebhook(
  @Headers('stripe-signature') signature: string,
  @Req() req: RawBodyRequest<Request>,
) {
  const event = this.stripe.webhooks.constructEvent(
    req.rawBody, // Use rawBody, not body
    signature,
    this.webhookSecret,
  );
}
```

## Verification

1. Send a test webhook from Stripe Dashboard
2. Check logs for successful signature verification
3. Verify event is processed correctly

## Notes

- This skill only loads when working in `apps/payments/`
- The webhook secret must match the endpoint (test vs live)
- Clock skew tolerance is 300 seconds by default
- For local testing, use Stripe CLI: `stripe listen --forward-to localhost:3000/webhooks/stripe`
