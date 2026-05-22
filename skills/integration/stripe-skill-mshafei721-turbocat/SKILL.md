---
name: stripe
slug: stripe-integration
version: 1.0.0
category: integration
description: Complete Stripe payment integration with checkout, pricing, and subscription management
triggers:
  - pattern: "stripe|payment|checkout|subscription|pricing"
    confidence: 0.8
    examples:
      - "add Stripe payments"
      - "create checkout flow"
      - "setup subscription billing"
      - "integrate payment processing"
      - "add pricing page with Stripe"
mcp_dependencies:
  - server: stripe
    required: false
    capabilities:
      - "payments"
      - "subscriptions"
---

# Stripe Integration Skill

Complete Stripe payment integration template with React components, hooks, and server-side setup. This template provides a production-ready payment flow with checkout, pricing cards, and subscription management.

## Overview

This template includes:
- **Stripe Client Setup** - Server-side Stripe SDK configuration
- **React Hooks** - useStripeCheckout for payment flows
- **UI Components** - CheckoutButton and PricingCard components
- **Type Safety** - Full TypeScript support
- **Error Handling** - Comprehensive error management
- **Webhook Support** - Handle Stripe events

## When to Use This Template

Use this template when you need:
- Payment processing integration
- Subscription billing setup
- One-time checkout flows
- Pricing page implementation
- Customer portal integration
- Webhook event handling

## What's Included

### Code Files

- `code/client.ts` - Stripe SDK setup and server-side utilities
- `code/hooks.ts` - React hooks for checkout and payments
- `code/components/checkout-button.tsx` - Checkout button component
- `code/components/pricing-card.tsx` - Pricing display component

### Configuration

- `mcp/config.json` - MCP server configuration for Stripe
- `env/.env.template` - Required environment variables

### Documentation

- `docs/README.md` - Complete setup and usage guide

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install stripe @stripe/stripe-js
   ```

2. **Configure Environment Variables**
   ```bash
   cp templates/stripe/env/.env.template .env.local
   # Add your Stripe keys
   ```

3. **Copy Template Files**
   ```bash
   # Use the template loader utility
   npx tsx scripts/load-template.ts stripe
   ```

4. **Create Stripe Products**
   - Go to Stripe Dashboard
   - Create products and prices
   - Copy price IDs to your code

## Key Features

### 1. Checkout Flow

Create seamless checkout experiences:

```typescript
import { useStripeCheckout } from '@/lib/stripe/hooks'

function PayButton() {
  const { createCheckout, isLoading } = useStripeCheckout()

  const handleCheckout = async () => {
    await createCheckout({
      priceId: 'price_1234',
      successUrl: '/success',
      cancelUrl: '/pricing',
    })
  }

  return (
    <button onClick={handleCheckout} disabled={isLoading}>
      {isLoading ? 'Loading...' : 'Buy Now'}
    </button>
  )
}
```

### 2. Subscription Management

Handle recurring billing:

```typescript
import { createSubscription } from '@/lib/stripe/client'

const subscription = await createSubscription({
  customerId: 'cus_1234',
  priceId: 'price_recurring',
  metadata: {
    userId: user.id,
  },
})
```

### 3. Customer Portal

Let customers manage subscriptions:

```typescript
import { createCustomerPortalSession } from '@/lib/stripe/client'

const portalUrl = await createCustomerPortalSession({
  customerId: 'cus_1234',
  returnUrl: '/dashboard',
})
```

### 4. Webhook Handling

Process Stripe events:

```typescript
import { handleStripeWebhook } from '@/lib/stripe/webhooks'

// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const signature = request.headers.get('stripe-signature')!
  const body = await request.text()

  const event = await handleStripeWebhook(body, signature)

  switch (event.type) {
    case 'checkout.session.completed':
      // Handle successful checkout
      break
    case 'customer.subscription.updated':
      // Handle subscription changes
      break
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
  })
}
```

## Component Usage

### Checkout Button

```tsx
import { CheckoutButton } from '@/components/stripe/checkout-button'

<CheckoutButton
  priceId="price_1234"
  variant="primary"
  size="lg"
>
  Subscribe Now
</CheckoutButton>
```

### Pricing Card

```tsx
import { PricingCard } from '@/components/stripe/pricing-card'

<PricingCard
  name="Pro Plan"
  price={29}
  interval="month"
  features={[
    'Unlimited projects',
    'Advanced analytics',
    'Priority support',
  ]}
  priceId="price_1234"
  highlighted={true}
/>
```

## Security Best Practices

### Never Expose Secret Keys

- Always use environment variables
- Keep `STRIPE_SECRET_KEY` server-side only
- Use `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` for client

### Validate Webhooks

- Always verify webhook signatures
- Use Stripe's webhook secret
- Handle duplicate events

### Idempotency

- Use idempotency keys for critical operations
- Prevent duplicate charges
- Handle retry scenarios

## Testing

### Test Mode

All operations work in test mode:

```bash
# Use test keys
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Test Cards

- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`

### Webhook Testing

```bash
# Install Stripe CLI
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
```

## Common Patterns

### One-Time Payment

```typescript
const checkout = await createCheckoutSession({
  mode: 'payment',
  lineItems: [
    {
      price: 'price_1234',
      quantity: 1,
    },
  ],
})
```

### Subscription with Trial

```typescript
const checkout = await createCheckoutSession({
  mode: 'subscription',
  lineItems: [
    {
      price: 'price_recurring',
      quantity: 1,
    },
  ],
  subscriptionData: {
    trialPeriodDays: 14,
  },
})
```

### Usage-Based Billing

```typescript
await stripe.subscriptionItems.createUsageRecord(
  'si_1234',
  {
    quantity: 100,
    timestamp: Math.floor(Date.now() / 1000),
  }
)
```

## Troubleshooting

### Common Errors

**"No such price"**
- Verify price ID is correct
- Check you're using the right API mode (test/live)

**"Invalid API Key"**
- Ensure environment variables are set
- Restart dev server after changing .env

**"Webhook signature verification failed"**
- Check webhook secret is correct
- Ensure raw body is passed to verification

## Environment Variables

Required variables (see `env/.env.template`):

- `STRIPE_SECRET_KEY` - Server-side API key
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Client-side publishable key
- `STRIPE_WEBHOOK_SECRET` - Webhook signing secret

## Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Dashboard](https://dashboard.stripe.com)
- [Webhook Events Reference](https://stripe.com/docs/api/events/types)
- [Test Cards](https://stripe.com/docs/testing)

---

**Template Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
