---
name: stripe-integration
description: Guide for integrating Stripe payments into an existing project. Covers one-time payments, subscriptions, and advanced patterns with security best practices.
---

# Stripe Integration Guide

This skill helps you integrate Stripe into an existing project. It provides decision trees, code patterns, and security checklists.

## Prerequisites

- Stripe account (test mode is fine)
- Node.js 18+ (or equivalent runtime)
- Existing web application with backend capability

## Step 1: Determine Integration Type

Ask the user these questions to determine the right pattern:

### Q1: What payment model do you need?

| Answer | Go to |
|--------|-------|
| One-time payment (buy a product/service once) | `patterns/one-time-checkout.md` |
| Subscription (recurring billing) | `patterns/subscription.md` |
| Usage-based billing (metered) | `patterns/usage-based.md` |
| Custom payment flow (full control) | `patterns/payment-intent.md` |

### Q2: Do you need multi-party payments?

| Answer | Action |
|--------|--------|
| Yes (marketplace, platform fees) | Also read `patterns/connect.md` |
| No | Skip Connect |

### Q3: What's your tech stack?

| Stack | Additional Guide |
|-------|------------------|
| Next.js (App Router) | `stacks/nextjs.md` |
| Express.js | `stacks/express.md` |
| Serverless (Vercel/Netlify Functions) | `stacks/serverless.md` |
| Other | Use Express guide as reference |

## Step 2: Core Principles (MUST READ)

Before writing any code, understand these non-negotiable rules:

### 2.1 Server-Side PaymentIntent Creation

```javascript
// WRONG - Client-side (attackers can modify amount)
const paymentIntent = await stripe.paymentIntents.create({
  amount: userProvidedAmount, // DANGEROUS!
  currency: 'usd',
});

// CORRECT - Server-side with validated amount
app.post('/create-payment-intent', async (req, res) => {
  const { productId } = req.body;
  const product = await db.products.findById(productId);

  const paymentIntent = await stripe.paymentIntents.create({
    amount: product.priceInCents, // From YOUR database
    currency: 'usd',
  });

  res.json({ clientSecret: paymentIntent.client_secret });
});
```

### 2.2 Webhook Idempotency

Stripe may send the same event multiple times. You MUST handle duplicates:

```javascript
app.post('/webhook', async (req, res) => {
  const event = stripe.webhooks.constructEvent(/*...*/);

  // Check if already processed
  const existing = await db.processedEvents.findById(event.id);
  if (existing) {
    return res.status(200).json({ received: true }); // Already handled
  }

  // Process the event
  await handleEvent(event);

  // Mark as processed
  await db.processedEvents.create({ id: event.id, processedAt: new Date() });

  res.status(200).json({ received: true });
});
```

### 2.3 Async Webhook Processing

Return 2xx immediately, process business logic asynchronously:

```javascript
// WRONG - Synchronous processing (may timeout)
app.post('/webhook', async (req, res) => {
  const event = verifyEvent(req);
  await sendEmail(event);           // Slow!
  await updateDatabase(event);      // Slow!
  await notifyExternalService(event); // May fail!
  res.status(200).send();
});

// CORRECT - Queue for async processing
app.post('/webhook', async (req, res) => {
  const event = verifyEvent(req);
  await queue.add('stripe-event', event); // Fast enqueue
  res.status(200).json({ received: true }); // Return immediately
});
```

### 2.4 Currency in Smallest Units

Always use cents (or smallest unit), never dollars:

```javascript
// WRONG
amount: 19.99  // Floating point errors!

// CORRECT
amount: 1999   // $19.99 in cents
```

### 2.5 Environment Variables

Never hardcode API keys:

```bash
# .env
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

```javascript
// WRONG
const stripe = require('stripe')('sk_test_xxx');

// CORRECT
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
```

## Step 3: Implementation Checklist

After implementing, verify these items:

### Security Checklist

- [ ] API keys are in environment variables, not code
- [ ] Webhook signature is verified
- [ ] PaymentIntent is created server-side only
- [ ] Amounts come from your database, not client requests
- [ ] HTTPS is enforced in production
- [ ] Webhook endpoint is not rate-limited by your own middleware

### Reliability Checklist

- [ ] Webhook events are deduplicated by event.id
- [ ] Webhook handler returns 2xx within 5 seconds
- [ ] Failed webhook processing is retried via queue
- [ ] Database transactions wrap payment state changes

### Testing Checklist

- [ ] Tested with `4242 4242 4242 4242` (success)
- [ ] Tested with `4000 0000 0000 0002` (decline)
- [ ] Tested with `4000 0025 0000 3155` (requires 3D Secure)
- [ ] Tested webhook with Stripe CLI: `stripe listen --forward-to localhost:3000/webhook`
- [ ] Tested duplicate webhook handling

## Step 4: Go-Live Checklist

Before switching to live mode:

- [ ] Replace test keys with live keys
- [ ] Update webhook endpoint in Stripe Dashboard
- [ ] Verify webhook signing secret is updated
- [ ] Test one real transaction with small amount
- [ ] Set up monitoring/alerting for failed payments
- [ ] Document refund process for support team

## Quick Reference: Test Card Numbers

| Card Number | Scenario |
|-------------|----------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Decline |
| `4000 0025 0000 3155` | Requires 3D Secure |
| `4000 0000 0000 9995` | Insufficient funds |
| `4000 0000 0000 0069` | Expired card |

Any future expiry date and any 3-digit CVC will work in test mode.

## Related Documentation

- `essentials/webhook-handling.md` - Deep dive into webhooks
- `essentials/error-handling.md` - Error categorization and recovery
- `essentials/idempotency.md` - Preventing duplicate operations
- `essentials/security-checklist.md` - Full security audit checklist
