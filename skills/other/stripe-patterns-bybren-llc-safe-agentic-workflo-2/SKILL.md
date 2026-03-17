---
name: stripe-patterns
description: Stripe payment integration patterns. Use when implementing payment flows, handling webhooks, or working with subscriptions. Routes to existing patterns and provides evidence templates for payment testing.
---

# Stripe Patterns Skill

## Purpose

Guide safe and consistent Stripe integration. Routes to existing payment patterns and provides evidence templates for testing.

## When This Skill Applies

Invoke this skill when:

- Creating or modifying checkout flows
- Implementing Stripe webhooks
- Working with subscriptions or invoices
- Testing payment functionality
- Handling refunds or disputes

## Canonical Code References

### Configuration

- **Stripe Client Factory**: `lib/stripe-config.ts`
  - Use `createStripeClient()` for consistent API version
  - Never hardcode API keys

### API Routes

- **Checkout Session**: `app/api/payments/create-checkout-session/route.ts`
- **Webhook Handler**: `app/api/payments/webhook/route.ts`

### Helpers

- **Payment Helpers**: `utils/data/payments/` (use RLS context)
- **Subscription Helpers**: `utils/data/subscriptions/`
- **Invoice Helpers**: `utils/data/invoices/`

## Critical Rules

### Test Mode Safety Checklist

Before ANY payment work:

- [ ] Verify `STRIPE_SECRET_KEY` starts with `sk_test_`
- [ ] Confirm test webhook secret (`whsec_...` from Stripe CLI)
- [ ] Use test card numbers only (4242...)
- [ ] Never use production keys in development

### Idempotency Checklist

For webhook handlers:

- [ ] Store event ID before processing
- [ ] Check for duplicate events
- [ ] Use database transactions
- [ ] Return 200 OK even on idempotency skip

```typescript
// Idempotent webhook pattern
await withSystemContext(prisma, "webhook", async (client) => {
  // Check if already processed
  const existing = await client.webhook_events.findUnique({
    where: { stripe_event_id: event.id },
  });
  if (existing) {
    console.log(`Skipping duplicate event: ${event.id}`);
    return;
  }

  // Process and record
  await client.webhook_events.create({
    data: {
      stripe_event_id: event.id,
      event_type: event.type,
      processed_at: new Date(),
    },
  });
});
```

### Webhook Signature Verification

**ALWAYS** verify webhook signatures:

```typescript
import { stripe } from "@/lib/stripe-config";

const signature = request.headers.get("stripe-signature");
const event = stripe.webhooks.constructEvent(
  body,
  signature,
  process.env.STRIPE_WEBHOOK_SECRET,
);
```

## Common Patterns

### Create Checkout Session

```typescript
import { createStripeClient } from "@/lib/stripe-config";
import { withUserContext } from "@/lib/rls-context";

export async function createCheckout(userId: string, priceId: string) {
  const stripe = createStripeClient();

  // Store user context for success handling
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId },
  });

  return session;
}
```

### Handle Subscription Events

```typescript
// Webhook event types to handle
const SUBSCRIPTION_EVENTS = [
  "customer.subscription.created",
  "customer.subscription.updated",
  "customer.subscription.deleted",
  "invoice.payment_succeeded",
  "invoice.payment_failed",
];
```

## Evidence Template for Linear

When completing payment work, attach this evidence block:

```markdown
**Payment Testing Evidence**

- [ ] Test mode verified (`sk_test_` key)
- [ ] Webhook signature verification tested
- [ ] Idempotency tested (duplicate event handling)
- [ ] Success flow tested (card 4242...)
- [ ] Failure flow tested (card 4000000000000002)
- [ ] Subscription lifecycle tested (create/update/cancel)

**Test Results:**

- Checkout session: [session_id]
- Webhook events processed: [count]
- Subscription status: [active/cancelled]
```

## Authoritative References

- **Stripe Config**: `lib/stripe-config.ts`
- **Webhook Route**: `app/api/payments/webhook/route.ts`
- **Payment Tests**: `__tests__/payments/`
- **Stripe Docs**: https://stripe.com/docs
