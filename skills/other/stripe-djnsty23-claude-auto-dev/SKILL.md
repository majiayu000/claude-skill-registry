---
name: stripe
description: Stripe integration patterns - API keys, webhooks, checkout, subscriptions. Loads when working with payments.
triggers:
  - stripe
  - payment
  - checkout
  - subscription
  - billing
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
model: opus
user-invocable: true
---

# Stripe Integration Best Practices

Based on [stripe/ai](https://github.com/stripe/ai) (MIT). Latest API version: 2026-01-28.

## API Selection

### Checkout Sessions (preferred for on-session payments)
- Supports one-time payments and subscriptions
- Handles taxes, discounts, and payment method selection
- Use Stripe-hosted Checkout or Embedded Checkout

### Payment Intents (for off-session or custom flows)
- Use when you need full control over the checkout UI
- Required for off-session payments (saved cards, recurring)

### Deprecated (never use)
- **Charges API** - migrate to Checkout Sessions or Payment Intents
- **Sources API** - use Payment Methods instead
- **Tokens API** - use Confirmation Tokens for card inspection
- **Legacy Card Element** - use Payment Element instead

## Frontend Integration

**Priority order:**
1. **Stripe-hosted Checkout** - fastest, fully managed
2. **Embedded Checkout** - Stripe UI inside your page
3. **Payment Element** - custom layout, Stripe handles payment methods

Enable dynamic payment methods in the Stripe Dashboard rather than hardcoding `payment_method_types`.

## Environment Variables

```bash
# .env.local (never commit)
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# .env.example (commit this)
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
```

Keep `sk_` keys server-side only. Only `pk_` keys may be exposed to the browser.

## Webhook Verification

Always verify webhook signatures:

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Webhook signature verification failed', { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed':
      // Fulfill the order
      break;
    case 'invoice.payment_succeeded':
      // Update subscription status
      break;
    case 'customer.subscription.deleted':
      // Handle cancellation
      break;
  }

  return new Response('OK', { status: 200 });
}
```

## Subscriptions

- Use Billing APIs combined with Stripe Checkout
- Create products and prices in the Dashboard or via API
- Handle lifecycle events: `customer.subscription.created`, `updated`, `deleted`
- Use `invoice.payment_failed` to handle failed renewals

## Saving Payment Methods

Use the SetupIntent API to save payment methods for future use:

```typescript
const setupIntent = await stripe.setupIntents.create({
  customer: customerId,
  automatic_payment_methods: { enabled: true },
});
```

## Stripe Connect (Platforms)

- Use direct or destination charges with `on_behalf_of`
- Configure connected accounts with `controller` properties
- Handle onboarding with Account Links or embedded components

## Error Handling

```typescript
try {
  const session = await stripe.checkout.sessions.create({ ... });
} catch (err) {
  if (err instanceof Stripe.errors.StripeCardError) {
    // Card declined - show user-friendly message
  } else if (err instanceof Stripe.errors.StripeInvalidRequestError) {
    // Invalid parameters - fix the request
  } else {
    // Unexpected error - log and alert
  }
}
```

## Pre-Launch Checklist

- [ ] Switch from test keys to live keys
- [ ] Webhook endpoints configured for production
- [ ] Error handling covers all Stripe error types
- [ ] Idempotency keys on create/update operations
- [ ] Customer portal configured for self-service
- [ ] Review [Stripe Go Live Checklist](https://docs.stripe.com/go-live-checklist)
