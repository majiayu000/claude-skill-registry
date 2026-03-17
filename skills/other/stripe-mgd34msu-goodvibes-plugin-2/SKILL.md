---
name: stripe
description: Integrates Stripe payments including checkout, subscriptions, webhooks, and customer management. Use when accepting payments, setting up subscriptions, handling webhooks, or managing billing.
---

# Stripe

Payment processing platform for online businesses with powerful APIs.

## Quick Start

**Install:**
```bash
npm install stripe @stripe/stripe-js
```

**Environment variables:**
```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Server Setup

```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true,
});
```

## Checkout Session

### Create Checkout

```typescript
// app/api/checkout/route.ts
import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';

export async function POST(req: Request) {
  const { priceId, quantity = 1 } = await req.json();

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment', // or 'subscription'
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity,
        },
      ],
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/canceled`,
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create checkout session' },
      { status: 500 }
    );
  }
}
```

### Client Redirect

```tsx
'use client';

import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);

export function CheckoutButton({ priceId }: { priceId: string }) {
  const handleCheckout = async () => {
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priceId }),
    });

    const { url } = await response.json();

    if (url) {
      window.location.href = url;
    }
  };

  return (
    <button onClick={handleCheckout}>
      Buy Now
    </button>
  );
}
```

### Dynamic Products

```typescript
// Create checkout with custom product
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [
    {
      price_data: {
        currency: 'usd',
        product_data: {
          name: 'Custom Product',
          description: 'A great product',
          images: ['https://example.com/image.png'],
        },
        unit_amount: 2000, // $20.00 in cents
      },
      quantity: 1,
    },
  ],
  success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success`,
  cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/canceled`,
});
```

## Subscriptions

### Create Subscription Checkout

```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId, // Optional: existing customer
  line_items: [
    {
      price: 'price_monthly_plan',
      quantity: 1,
    },
  ],
  success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
  subscription_data: {
    trial_period_days: 14,
    metadata: {
      userId: 'user_123',
    },
  },
});
```

### Manage Subscription

```typescript
// Cancel subscription
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
});

// Cancel immediately
await stripe.subscriptions.cancel(subscriptionId);

// Update subscription
await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscriptionItemId,
      price: 'price_new_plan',
    },
  ],
  proration_behavior: 'create_prorations',
});
```

### Customer Portal

```typescript
// app/api/portal/route.ts
import { stripe } from '@/lib/stripe';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { customerId } = await req.json();

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
  });

  return NextResponse.json({ url: session.url });
}
```

## Payment Intents

### Server-Side

```typescript
// app/api/payment-intent/route.ts
import { stripe } from '@/lib/stripe';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { amount, currency = 'usd' } = await req.json();

  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount, // In cents
      currency,
      automatic_payment_methods: {
        enabled: true,
      },
    });

    return NextResponse.json({
      clientSecret: paymentIntent.client_secret,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create payment intent' },
      { status: 500 }
    );
  }
}
```

### Client-Side Payment Form

```tsx
'use client';

import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  PaymentElement,
  useStripe,
  useElements,
} from '@stripe/react-stripe-js';

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);

function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) return;

    setProcessing(true);
    setError(null);

    const { error: submitError } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/success`,
      },
    });

    if (submitError) {
      setError(submitError.message ?? 'Payment failed');
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      {error && <p className="text-red-500">{error}</p>}
      <button
        type="submit"
        disabled={!stripe || processing}
        className="mt-4 w-full bg-blue-600 text-white py-2 rounded"
      >
        {processing ? 'Processing...' : 'Pay'}
      </button>
    </form>
  );
}

export function PaymentForm({ clientSecret }: { clientSecret: string }) {
  return (
    <Elements
      stripe={stripePromise}
      options={{
        clientSecret,
        appearance: {
          theme: 'stripe',
          variables: {
            colorPrimary: '#3b82f6',
          },
        },
      }}
    >
      <CheckoutForm />
    </Elements>
  );
}
```

## Webhooks

### Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe';
import { headers } from 'next/headers';
import { NextResponse } from 'next/server';
import Stripe from 'stripe';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed');
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    );
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        await handleCheckoutComplete(session);
        break;
      }

      case 'customer.subscription.created': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionCreated(subscription);
        break;
      }

      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionUpdated(subscription);
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionDeleted(subscription);
        break;
      }

      case 'invoice.paid': {
        const invoice = event.data.object as Stripe.Invoice;
        await handleInvoicePaid(invoice);
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;
        await handlePaymentFailed(invoice);
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook handler error:', error);
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 500 }
    );
  }
}

// Handler functions
async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const customerId = session.customer as string;
  const customerEmail = session.customer_email;

  // Create or update user in database
  await db.user.upsert({
    where: { email: customerEmail! },
    update: { stripeCustomerId: customerId },
    create: {
      email: customerEmail!,
      stripeCustomerId: customerId,
    },
  });
}

async function handleSubscriptionCreated(subscription: Stripe.Subscription) {
  await db.subscription.create({
    data: {
      stripeSubscriptionId: subscription.id,
      stripeCustomerId: subscription.customer as string,
      status: subscription.status,
      priceId: subscription.items.data[0].price.id,
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  await db.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      status: subscription.status,
      priceId: subscription.items.data[0].price.id,
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await db.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: { status: 'canceled' },
  });
}
```

### Local Webhook Testing

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

## Customers

### Create Customer

```typescript
const customer = await stripe.customers.create({
  email: 'user@example.com',
  name: 'John Doe',
  metadata: {
    userId: 'user_123',
  },
});
```

### Get Customer

```typescript
const customer = await stripe.customers.retrieve(customerId);

// With subscriptions
const customer = await stripe.customers.retrieve(customerId, {
  expand: ['subscriptions'],
});
```

### Update Customer

```typescript
await stripe.customers.update(customerId, {
  email: 'newemail@example.com',
  metadata: {
    plan: 'pro',
  },
});
```

## Products and Prices

### Create Product

```typescript
const product = await stripe.products.create({
  name: 'Pro Plan',
  description: 'Full access to all features',
  images: ['https://example.com/pro.png'],
  metadata: {
    features: 'unlimited,priority_support,api_access',
  },
});
```

### Create Price

```typescript
// One-time price
const price = await stripe.prices.create({
  product: product.id,
  unit_amount: 2000, // $20.00
  currency: 'usd',
});

// Recurring price
const monthlyPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 1000, // $10.00
  currency: 'usd',
  recurring: {
    interval: 'month',
  },
});

// Usage-based price
const usagePrice = await stripe.prices.create({
  product: product.id,
  currency: 'usd',
  recurring: {
    interval: 'month',
    usage_type: 'metered',
  },
  billing_scheme: 'per_unit',
  unit_amount: 10, // $0.10 per unit
});
```

### List Products with Prices

```typescript
const products = await stripe.products.list({
  active: true,
  expand: ['data.default_price'],
});
```

## Utility Functions

```typescript
// lib/stripe-helpers.ts

export function formatPrice(amount: number, currency: string = 'usd') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency.toUpperCase(),
  }).format(amount / 100);
}

export function getSubscriptionStatus(status: string) {
  const statusMap: Record<string, { label: string; color: string }> = {
    active: { label: 'Active', color: 'green' },
    trialing: { label: 'Trial', color: 'blue' },
    past_due: { label: 'Past Due', color: 'yellow' },
    canceled: { label: 'Canceled', color: 'red' },
    unpaid: { label: 'Unpaid', color: 'red' },
  };

  return statusMap[status] || { label: status, color: 'gray' };
}

export async function getOrCreateCustomer(userId: string, email: string) {
  // Check if customer exists in database
  const user = await db.user.findUnique({ where: { id: userId } });

  if (user?.stripeCustomerId) {
    return user.stripeCustomerId;
  }

  // Create new Stripe customer
  const customer = await stripe.customers.create({
    email,
    metadata: { userId },
  });

  // Save to database
  await db.user.update({
    where: { id: userId },
    data: { stripeCustomerId: customer.id },
  });

  return customer.id;
}
```

## Best Practices

1. **Always use webhooks** - Don't rely on redirect URLs
2. **Verify webhook signatures** - Prevent spoofed events
3. **Store customer IDs** - Link Stripe to your users
4. **Handle idempotency** - Check for duplicate events
5. **Test with CLI** - Use `stripe listen` locally

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing webhook verification | Use constructEvent() |
| Trusting client amounts | Calculate on server |
| No error handling | Wrap in try/catch |
| Hardcoded prices | Use price IDs from Stripe |
| Missing idempotency | Check webhook event IDs |

## Reference Files

- [references/webhooks.md](references/webhooks.md) - All webhook events
- [references/subscriptions.md](references/subscriptions.md) - Subscription patterns
- [references/testing.md](references/testing.md) - Test mode setup
