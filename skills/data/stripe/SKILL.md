---
name: stripe-expert
description: Comprehensive Stripe API expert with access to 3,253 official documentation files covering all payment processing, billing, subscriptions, webhooks, Connect, Terminal, Radar, Identity, Tax, Climate, and integrations. Invoke when user mentions Stripe, payments, subscriptions, billing, payment processing, checkout, invoices, or any payment-related features.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
---

# Stripe Integration Expert

## Purpose

Provide comprehensive, accurate guidance for integrating Stripe payment infrastructure based on 3,253+ official Stripe documentation files. Cover all aspects of payment processing, billing, subscriptions, webhooks, fraud prevention, and advanced features.

## Documentation Coverage

**Full access to official Stripe documentation (when available):**
- **Location:** `docs/stripe/`
- **Files:** 3,253 markdown files
- **Coverage:** Complete API reference, guides, integrations, and best practices

**Note:** Documentation must be pulled separately:
```bash
pipx install docpull
docpull https://docs.stripe.com -o .claude/skills/stripe/docs
```

**Major Areas:**
- Payment processing (Payment Intents, Checkout, Elements)
- Subscription billing (Subscriptions, Invoices, Metering)
- Customer management
- Payment methods (cards, wallets, bank transfers, buy now pay later)
- Webhooks and events
- Connect (marketplace and platform payments)
- Terminal (in-person payments)
- Radar (fraud detection)
- Identity verification
- Tax calculation
- Climate carbon removal
- Issuing (card creation)
- Treasury (banking-as-a-service)
- Financial Connections
- Agentic Commerce (AI agent payments)

## When to Use

Invoke when user mentions:
- **Payment Processing:** Stripe, payments, checkout, payment intent, one-time payment
- **Subscriptions:** billing, recurring payments, subscription, metered billing, usage-based
- **Customer Management:** customers, payment methods, invoices
- **Webhooks:** webhooks, events, payment confirmation, notifications
- **Advanced Features:** Connect, marketplace, platform, split payments, ACH, SEPA
- **Fraud & Security:** Radar, 3D Secure, SCA, PCI compliance, fraud detection
- **Tax:** tax calculation, VAT, GST, sales tax
- **In-Person:** Terminal, card readers, point of sale
- **Identity:** verification, KYC, identity checks
- **Banking:** Treasury, financial accounts, payouts, bank accounts

## How to Use Documentation

When answering questions:

1. **Search for specific topics:**
   ```bash
   # Use Grep to find relevant docs
   grep -r "payment intent" docs/stripe/ --include="*.md"
   ```

2. **Read specific API references:**
   ```bash
   # API docs are in docs/stripe/api/
   cat docs/stripe/api/payment_intents/api-payment_intents-create.md
   ```

3. **Find integration guides:**
   ```bash
   # Guides and tutorials
   ls docs/stripe/*.md
   ```

## Core Authentication

### API Keys

```javascript
// Server-side (Node.js)
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Client-side (safe for browsers)
const stripe = Stripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);
```

**Key Types:**
- **Test:** `pk_test_...` (publishable), `sk_test_...` (secret)
- **Live:** `pk_live_...` (publishable), `sk_live_...` (secret)
- **Restricted:** Custom permissions for limited access

**Security:**
- NEVER commit secret keys
- Use environment variables
- Rotate immediately if exposed
- Use restricted keys when possible

## Payment Integration Patterns

### Pattern 1: Stripe Checkout (Fastest)

**Best for:** Quick setup, standard checkout flow, subscriptions

```typescript
// Server-side API route
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price: 'price_xxx', // Pre-created price ID
      quantity: 1,
    }],
    mode: 'payment', // or 'subscription' or 'setup'
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/cancel`,
  });

  return Response.json({ url: session.url });
}

// Client-side redirect
window.location.href = checkoutUrl;
```

### Pattern 2: Payment Element (Custom UI)

**Best for:** Custom checkout experience, embedded in your site

```typescript
// Server: Create Payment Intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000, // $20.00 in cents
  currency: 'usd',
  automatic_payment_methods: { enabled: true },
});

// Client: Mount Payment Element
import { Elements, PaymentElement } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

function CheckoutForm() {
  return (
    <Elements stripe={stripePromise} options={{ clientSecret }}>
      <PaymentElement />
      <button onClick={handleSubmit}>Pay</button>
    </Elements>
  );
}
```

### Pattern 3: Subscriptions

**Create subscription:**
```typescript
const subscription = await stripe.subscriptions.create({
  customer: 'cus_xxx',
  items: [{ price: 'price_xxx' }],
  payment_behavior: 'default_incomplete',
  payment_settings: { save_default_payment_method: 'on_subscription' },
  expand: ['latest_invoice.payment_intent'],
});

// Return client secret for 3DS
const clientSecret = subscription.latest_invoice.payment_intent.client_secret;
```

**Subscription lifecycle:**
- `incomplete` → `active` → `past_due` → `canceled` / `unpaid`

**Metered billing:**
```typescript
// Report usage
await stripe.subscriptionItems.createUsageRecord('si_xxx', {
  quantity: 100,
  timestamp: Math.floor(Date.now() / 1000),
});
```

## Webhook Implementation

### Setup Webhook Endpoint

```typescript
import { headers } from 'next/headers';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    // Verify signature (CRITICAL for security)
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }

  // Handle event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      // Fulfill order, send confirmation email
      await fulfillOrder(paymentIntent);
      break;

    case 'payment_intent.payment_failed':
      // Notify customer of failure
      await notifyPaymentFailure(event.data.object);
      break;

    case 'customer.subscription.created':
    case 'customer.subscription.updated':
      // Update subscription status in database
      await updateSubscription(event.data.object);
      break;

    case 'customer.subscription.deleted':
      // Cancel user access
      await cancelAccess(event.data.object);
      break;

    case 'invoice.payment_succeeded':
      // Subscription payment succeeded
      await confirmSubscriptionPayment(event.data.object);
      break;

    case 'invoice.payment_failed':
      // Notify customer to update payment method
      await notifyPaymentMethodUpdate(event.data.object);
      break;

    case 'charge.dispute.created':
      // Handle dispute
      await handleDispute(event.data.object);
      break;

    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  return new Response(JSON.stringify({ received: true }));
}
```

**Critical webhook events:**
- `payment_intent.succeeded` - Payment completed
- `payment_intent.payment_failed` - Payment failed
- `customer.subscription.*` - Subscription lifecycle
- `invoice.payment_succeeded` - Recurring payment succeeded
- `invoice.payment_failed` - Recurring payment failed
- `charge.dispute.created` - Customer disputed charge
- `checkout.session.completed` - Checkout session completed

**Testing webhooks locally:**
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks

# Trigger test events
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created
```

## Customer Management

```typescript
// Create customer
const customer = await stripe.customers.create({
  email: 'customer@example.com',
  name: 'John Doe',
  metadata: { user_id: '12345' },
  payment_method: 'pm_xxx',
  invoice_settings: {
    default_payment_method: 'pm_xxx',
  },
});

// Attach payment method
await stripe.paymentMethods.attach('pm_xxx', {
  customer: 'cus_xxx',
});

// List customer's payment methods
const paymentMethods = await stripe.paymentMethods.list({
  customer: 'cus_xxx',
  type: 'card',
});

// Update customer
await stripe.customers.update('cus_xxx', {
  metadata: { plan: 'premium' },
});
```

## Advanced Features

### Connect (Marketplaces & Platforms)

**Create connected account:**
```typescript
const account = await stripe.accounts.create({
  type: 'express',
  country: 'US',
  email: 'vendor@example.com',
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true },
  },
});

// Create account link for onboarding
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: 'https://example.com/reauth',
  return_url: 'https://example.com/return',
  type: 'account_onboarding',
});
```

**Split payments:**
```typescript
// Application fee
await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'usd',
  application_fee_amount: 1000, // 10% platform fee
  transfer_data: {
    destination: 'acct_xxx', // Connected account
  },
});

// Or use separate transfers
await stripe.transfers.create({
  amount: 9000,
  currency: 'usd',
  destination: 'acct_xxx',
});
```

### Radar (Fraud Prevention)

```typescript
// Rules are configured in Dashboard
// But you can review risk scores:
const paymentIntent = await stripe.paymentIntents.retrieve('pi_xxx', {
  expand: ['latest_charge.payment_method_details.card'],
});

const riskScore = paymentIntent.latest_charge?.outcome?.risk_score;
const riskLevel = paymentIntent.latest_charge?.outcome?.risk_level; // 'normal', 'elevated', 'highest'

// Block high-risk payments
if (riskLevel === 'highest') {
  await stripe.paymentIntents.cancel('pi_xxx');
}
```

### Tax Calculation

```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{
    price: 'price_xxx',
    quantity: 1,
  }],
  automatic_tax: { enabled: true }, // Stripe calculates tax automatically
  customer_update: {
    address: 'auto', // Collect address for tax
  },
  success_url: 'https://example.com/success',
  cancel_url: 'https://example.com/cancel',
});
```

## Testing

### Test Card Numbers

**Success:**
- `4242 4242 4242 4242` - Visa
- `5555 5555 5555 4444` - Mastercard
- `3782 822463 10005` - American Express

**Requires 3D Secure:**
- `4000 0025 0000 3155` - Visa (3DS required)
- `4000 0027 6000 3184` - Visa (3DS required, decline)

**Declined:**
- `4000 0000 0000 9995` - Generic decline
- `4000 0000 0000 9987` - Insufficient funds
- `4000 0000 0000 9979` - Stolen card

**Other:**
- Any future expiry date (e.g., `12/34`)
- Any 3-digit CVC (4 digits for Amex)
- Any 5-digit ZIP

## Security Best Practices

1. **API Keys:**
   - Never expose secret keys client-side
   - Use restricted keys when possible
   - Rotate keys periodically
   - Monitor key usage in Dashboard

2. **Webhooks:**
   - ALWAYS verify webhook signatures
   - Use HTTPS endpoints only
   - Return 200 immediately, process async
   - Handle retries (Stripe retries failed webhooks)

3. **Amounts:**
   - Validate amounts server-side
   - Never trust client-sent amounts
   - Use Price objects when possible

4. **PCI Compliance:**
   - Never store card numbers
   - Use Stripe Elements/Checkout
   - Let Stripe handle sensitive data

5. **Idempotency:**
   - Use idempotency keys for critical operations
   - Prevents duplicate charges on retry

## Common Errors

**Authentication:**
- `Invalid API Key` - Check key format and environment
- `No such customer` - Customer deleted or wrong ID

**Payment failures:**
- `card_declined` - Generic decline (ask customer to try different card)
- `insufficient_funds` - Not enough money
- `incorrect_cvc` - Wrong security code
- `expired_card` - Card expired

**Subscription errors:**
- `resource_missing` - Price or product doesn't exist
- `payment_intent_authentication_failure` - 3DS failed

## Framework-Specific Guides

### Next.js App Router

```typescript
// app/api/create-payment-intent/route.ts
import { NextRequest } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: NextRequest) {
  const { amount } = await req.json();

  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    automatic_payment_methods: { enabled: true },
  });

  return Response.json({ clientSecret: paymentIntent.client_secret });
}
```

### React Hook

```typescript
import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

export function useStripeCheckout() {
  const [loading, setLoading] = useState(false);

  const checkout = async (priceId: string) => {
    setLoading(true);

    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priceId }),
    });

    const { sessionId } = await res.json();

    const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);
    await stripe?.redirectToCheckout({ sessionId });

    setLoading(false);
  };

  return { checkout, loading };
}
```

## TypeScript Types & Configuration

### Database Schema Types

```typescript
// types/stripe.ts
import Stripe from 'stripe';

export interface StripeCustomerData {
  stripeCustomerId: string;
  stripeSubscriptionId?: string;
  stripePriceId?: string;
  stripeCurrentPeriodEnd?: Date;
  userId: string;
}

export interface CreateCheckoutSessionParams {
  userId: string;
  priceId: string;
  successUrl: string;
  cancelUrl: string;
  metadata?: Record<string, string>;
}

export interface WebhookEventData {
  event: Stripe.Event;
  customerId?: string;
  subscriptionId?: string;
  invoiceId?: string;
}

export type StripeSubscriptionStatus =
  | 'incomplete'
  | 'incomplete_expired'
  | 'trialing'
  | 'active'
  | 'past_due'
  | 'canceled'
  | 'unpaid';

export interface SubscriptionUpdate {
  subscriptionId: string;
  status: StripeSubscriptionStatus;
  currentPeriodEnd: Date;
  cancelAtPeriodEnd: boolean;
  priceId: string;
}
```

### Stripe Client Configuration

```typescript
// lib/stripe/config.ts
import Stripe from 'stripe';

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is not set');
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-11-20.acacia',
  typescript: true,
  appInfo: {
    name: 'Your App Name',
    version: '1.0.0',
  },
  // Retry logic for network failures
  maxNetworkRetries: 2,
  timeout: 30000, // 30 seconds
});

// Client-side configuration
export const getStripe = () => {
  if (!process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY) {
    throw new Error('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY is not set');
  }
  return loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);
};
```

### Environment Variables

```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Production
STRIPE_SECRET_KEY=sk_live_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Next.js App Router Integration

### Server Actions for Payments

```typescript
// app/actions/stripe.ts
'use server';

import { stripe } from '@/lib/stripe/config';
import { auth } from '@/lib/auth';
import { revalidatePath } from 'next/cache';

export async function createCheckoutSession(priceId: string) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    customer_email: session.user.email,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{
      price: priceId,
      quantity: 1,
    }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing?canceled=true`,
    metadata: {
      userId: session.user.id,
    },
  });

  return { url: checkoutSession.url };
}

export async function createPortalSession() {
  const session = await auth();
  if (!session?.user?.stripeCustomerId) {
    throw new Error('No Stripe customer found');
  }

  const portalSession = await stripe.billingPortal.sessions.create({
    customer: session.user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_URL}/dashboard`,
  });

  return { url: portalSession.url };
}

export async function cancelSubscription(subscriptionId: string) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });

  revalidatePath('/dashboard');
  return { success: true };
}
```

### Client Component with Server Actions

```typescript
// app/components/PricingCard.tsx
'use client';

import { useState } from 'react';
import { createCheckoutSession } from '@/app/actions/stripe';

export function PricingCard({ priceId, name, price, features }) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    try {
      setLoading(true);
      const { url } = await createCheckoutSession(priceId);
      if (url) window.location.href = url;
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Failed to start checkout');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pricing-card">
      <h3>{name}</h3>
      <p>${price}/mo</p>
      <ul>
        {features.map(f => <li key={f}>{f}</li>)}
      </ul>
      <button onClick={handleCheckout} disabled={loading}>
        {loading ? 'Loading...' : 'Subscribe'}
      </button>
    </div>
  );
}
```

### Route Handlers

```typescript
// app/api/create-payment-intent/route.ts
import { NextRequest } from 'next/server';
import { stripe } from '@/lib/stripe/config';
import { auth } from '@/lib/auth';

export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { amount, currency = 'usd' } = await req.json();

    // Validate amount server-side (CRITICAL)
    if (!amount || amount < 50) { // $0.50 minimum
      return Response.json({ error: 'Invalid amount' }, { status: 400 });
    }

    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency,
      automatic_payment_methods: { enabled: true },
      metadata: {
        userId: session.user.id,
      },
    });

    return Response.json({
      clientSecret: paymentIntent.client_secret
    });
  } catch (error) {
    console.error('Payment intent error:', error);
    return Response.json(
      { error: 'Failed to create payment intent' },
      { status: 500 }
    );
  }
}
```

## Production Patterns

### Error Handling

```typescript
// lib/stripe/errors.ts
import Stripe from 'stripe';

export function handleStripeError(error: unknown): {
  message: string;
  userMessage: string;
  code?: string;
} {
  if (error instanceof Stripe.errors.StripeError) {
    // Card errors
    if (error.type === 'StripeCardError') {
      return {
        message: error.message,
        userMessage: 'Your card was declined. Please try a different payment method.',
        code: error.code,
      };
    }

    // Rate limit errors
    if (error.type === 'StripeRateLimitError') {
      return {
        message: 'Too many requests',
        userMessage: 'Too many requests. Please try again in a moment.',
      };
    }

    // Invalid request errors
    if (error.type === 'StripeInvalidRequestError') {
      return {
        message: error.message,
        userMessage: 'Invalid request. Please contact support.',
        code: error.code,
      };
    }

    // API errors
    if (error.type === 'StripeAPIError') {
      return {
        message: 'Stripe API error',
        userMessage: 'Payment service temporarily unavailable. Please try again.',
      };
    }

    // Connection errors
    if (error.type === 'StripeConnectionError') {
      return {
        message: 'Network error',
        userMessage: 'Network error. Please check your connection and try again.',
      };
    }

    // Authentication errors
    if (error.type === 'StripeAuthenticationError') {
      return {
        message: 'Authentication failed',
        userMessage: 'Authentication error. Please contact support.',
      };
    }
  }

  // Generic error
  return {
    message: error instanceof Error ? error.message : 'Unknown error',
    userMessage: 'An unexpected error occurred. Please try again.',
  };
}

// Usage in API routes
export async function POST(req: NextRequest) {
  try {
    const paymentIntent = await stripe.paymentIntents.create({...});
    return Response.json({ clientSecret: paymentIntent.client_secret });
  } catch (error) {
    const { userMessage, message } = handleStripeError(error);
    console.error('Stripe error:', message);
    return Response.json({ error: userMessage }, { status: 400 });
  }
}
```

### Idempotency Keys

```typescript
// lib/stripe/idempotency.ts
import { v4 as uuidv4 } from 'uuid';

export async function createPaymentWithIdempotency(
  amount: number,
  userId: string
) {
  const idempotencyKey = `payment_${userId}_${Date.now()}_${uuidv4()}`;

  try {
    const paymentIntent = await stripe.paymentIntents.create(
      {
        amount,
        currency: 'usd',
        metadata: { userId },
      },
      {
        idempotencyKey, // Prevents duplicate charges on retry
      }
    );

    return paymentIntent;
  } catch (error) {
    // If request fails, retry with same idempotency key
    // Stripe will return the original result instead of creating duplicate
    throw error;
  }
}

// For subscriptions
export async function createSubscriptionIdempotent(
  customerId: string,
  priceId: string
) {
  const idempotencyKey = `sub_${customerId}_${priceId}`;

  return stripe.subscriptions.create(
    {
      customer: customerId,
      items: [{ price: priceId }],
    },
    { idempotencyKey }
  );
}
```

### Retry Logic with Exponential Backoff

```typescript
// lib/stripe/retry.ts
export async function retryStripeOperation<T>(
  operation: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      // Don't retry certain errors
      if (error instanceof Stripe.errors.StripeCardError) {
        throw error; // Card declined - don't retry
      }
      if (error instanceof Stripe.errors.StripeInvalidRequestError) {
        throw error; // Invalid params - don't retry
      }

      // Retry with exponential backoff
      const delay = Math.min(1000 * Math.pow(2, i), 10000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Usage
const paymentIntent = await retryStripeOperation(() =>
  stripe.paymentIntents.create({
    amount: 1000,
    currency: 'usd',
  })
);
```

### Rate Limiting

```typescript
// lib/stripe/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests per 10 seconds
});

export async function POST(req: NextRequest) {
  const ip = req.ip ?? '127.0.0.1';
  const { success, limit, reset, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return Response.json(
      { error: 'Too many requests' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString(),
        },
      }
    );
  }

  // Process Stripe request
  const paymentIntent = await stripe.paymentIntents.create({...});
  return Response.json({ clientSecret: paymentIntent.client_secret });
}
```

## Stripe Connect Deep Dive

### Account Creation & Onboarding

```typescript
// lib/stripe/connect.ts
export async function createConnectedAccount(email: string, country: string) {
  const account = await stripe.accounts.create({
    type: 'express', // or 'standard' or 'custom'
    country,
    email,
    capabilities: {
      card_payments: { requested: true },
      transfers: { requested: true },
    },
    business_type: 'individual', // or 'company'
  });

  return account;
}

export async function createAccountOnboardingLink(accountId: string) {
  const accountLink = await stripe.accountLinks.create({
    account: accountId,
    refresh_url: `${process.env.NEXT_PUBLIC_URL}/connect/reauth`,
    return_url: `${process.env.NEXT_PUBLIC_URL}/connect/return`,
    type: 'account_onboarding',
  });

  return accountLink.url;
}

// Check if account is fully onboarded
export async function isAccountOnboarded(accountId: string): Promise<boolean> {
  const account = await stripe.accounts.retrieve(accountId);

  return (
    account.details_submitted &&
    account.charges_enabled &&
    account.payouts_enabled
  );
}
```

### Marketplace Payment Flows

```typescript
// Pattern 1: Direct Charge (platform receives, then transfers)
export async function createDirectCharge(
  amount: number,
  connectedAccountId: string
) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    application_fee_amount: Math.floor(amount * 0.1), // 10% platform fee
    transfer_data: {
      destination: connectedAccountId,
    },
  });

  return paymentIntent;
}

// Pattern 2: Destination Charge (connected account receives, platform takes fee)
export async function createDestinationCharge(
  amount: number,
  connectedAccountId: string
) {
  const paymentIntent = await stripe.paymentIntents.create(
    {
      amount,
      currency: 'usd',
      application_fee_amount: Math.floor(amount * 0.1),
    },
    {
      stripeAccount: connectedAccountId, // Charge appears on connected account
    }
  );

  return paymentIntent;
}

// Pattern 3: Separate Transfers
export async function createSeparateTransfer(
  amount: number,
  connectedAccountId: string,
  chargeId: string
) {
  const platformFee = Math.floor(amount * 0.1);
  const transferAmount = amount - platformFee;

  const transfer = await stripe.transfers.create({
    amount: transferAmount,
    currency: 'usd',
    destination: connectedAccountId,
    source_transaction: chargeId,
  });

  return transfer;
}
```

### Multi-Party Payments (Split Payments)

```typescript
// Split payment between multiple sellers
export async function createMultiPartyPayment(
  totalAmount: number,
  sellers: Array<{ accountId: string; amount: number }>
) {
  // Create charge on platform account
  const paymentIntent = await stripe.paymentIntents.create({
    amount: totalAmount,
    currency: 'usd',
  });

  // After charge succeeds, create transfers to each seller
  const transfers = await Promise.all(
    sellers.map(seller =>
      stripe.transfers.create({
        amount: seller.amount,
        currency: 'usd',
        destination: seller.accountId,
      })
    )
  );

  return { paymentIntent, transfers };
}
```

### Connect Webhooks

```typescript
// Listen for Connect account events
export async function POST(req: Request) {
  const event = await verifyWebhook(req);

  switch (event.type) {
    case 'account.updated':
      const account = event.data.object as Stripe.Account;
      // Check if account completed onboarding
      if (account.details_submitted && account.charges_enabled) {
        await updateDatabase({ accountId: account.id, status: 'active' });
      }
      break;

    case 'account.application.deauthorized':
      // User disconnected their account
      const deauthAccount = event.data.object as Stripe.Account;
      await handleAccountDisconnection(deauthAccount.id);
      break;

    case 'capability.updated':
      // Track capability status (card_payments, transfers, etc.)
      const capability = event.data.object;
      await trackCapabilityStatus(capability);
      break;

    case 'payout.paid':
      // Payout to connected account succeeded
      const payout = event.data.object as Stripe.Payout;
      await notifyVendorPayoutSuccess(payout);
      break;

    case 'payout.failed':
      // Payout failed - notify vendor
      const failedPayout = event.data.object as Stripe.Payout;
      await notifyVendorPayoutFailure(failedPayout);
      break;
  }

  return Response.json({ received: true });
}
```

## Stripe Terminal (In-Person Payments)

### Reader Setup

```typescript
// lib/stripe/terminal.ts
export async function registerReader(
  registrationCode: string,
  label: string,
  locationId: string
) {
  const reader = await stripe.terminal.readers.create({
    registration_code: registrationCode,
    label,
    location: locationId,
  });

  return reader;
}

export async function createTerminalLocation(address: {
  line1: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
}) {
  const location = await stripe.terminal.locations.create({
    display_name: 'Retail Store',
    address,
  });

  return location;
}
```

### Payment Collection

```typescript
// Create payment intent for Terminal
export async function createTerminalPaymentIntent(amount: number) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    payment_method_types: ['card_present'],
    capture_method: 'manual', // Authorize first, capture later
  });

  return paymentIntent;
}

// Server-side: Process Terminal connection token
export async function POST(req: NextRequest) {
  const connectionToken = await stripe.terminal.connectionTokens.create();
  return Response.json({ secret: connectionToken.secret });
}
```

### Client-Side Terminal Integration

```typescript
// Client component for Terminal SDK
'use client';

import { loadStripeTerminal } from '@stripe/terminal-js';

export function TerminalReader() {
  useEffect(() => {
    const initTerminal = async () => {
      const terminal = await loadStripeTerminal();

      const term = terminal.create({
        onFetchConnectionToken: async () => {
          const res = await fetch('/api/terminal/connection-token');
          const { secret } = await res.json();
          return secret;
        },
        onUnexpectedReaderDisconnect: () => {
          console.log('Reader disconnected');
        },
      });

      // Discover readers
      const discoverResult = await term.discoverReaders();
      if (discoverResult.discoveredReaders.length > 0) {
        // Connect to first reader
        await term.connectReader(discoverResult.discoveredReaders[0]);
      }
    };

    initTerminal();
  }, []);

  return <div>Terminal Reader Component</div>;
}
```

## Stripe Radar (Fraud Prevention)

### Custom Fraud Rules

```typescript
// Review high-risk charges before processing
export async function reviewHighRiskCharge(paymentIntentId: string) {
  const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId, {
    expand: ['latest_charge'],
  });

  const charge = paymentIntent.latest_charge as Stripe.Charge;
  const outcome = charge?.outcome;

  if (outcome?.risk_level === 'highest') {
    // Block the payment
    await stripe.paymentIntents.cancel(paymentIntentId);
    return { action: 'blocked', reason: outcome.reason };
  }

  if (outcome?.risk_level === 'elevated' && outcome?.risk_score > 65) {
    // Require manual review
    return { action: 'review', riskScore: outcome.risk_score };
  }

  return { action: 'approve' };
}

// Add custom fraud metadata
export async function createPaymentWithFraudCheck(
  amount: number,
  email: string,
  ipAddress: string
) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    metadata: {
      customer_email: email,
      customer_ip: ipAddress,
      order_id: generateOrderId(),
    },
    // Radar uses this data for fraud detection
  });

  return paymentIntent;
}
```

### 3D Secure Authentication

```typescript
// Force 3D Secure for high-value transactions
export async function createSecurePayment(amount: number) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    payment_method_options: {
      card: {
        request_three_d_secure: amount > 10000 ? 'any' : 'automatic',
      },
    },
  });

  return paymentIntent;
}

// Handle 3DS authentication in client
async function handleCardAction(clientSecret: string) {
  const stripe = await getStripe();
  const { error, paymentIntent } = await stripe.handleCardAction(clientSecret);

  if (error) {
    console.error('3DS failed:', error);
    return { success: false };
  }

  if (paymentIntent.status === 'requires_confirmation') {
    // Confirm on server
    await fetch('/api/confirm-payment', {
      method: 'POST',
      body: JSON.stringify({ paymentIntentId: paymentIntent.id }),
    });
  }

  return { success: true };
}
```

### Reviewing Disputes

```typescript
// Handle dispute webhooks
case 'charge.dispute.created':
  const dispute = event.data.object as Stripe.Dispute;

  // Automatically submit evidence for low-amount disputes
  if (dispute.amount < 5000) { // $50
    await stripe.disputes.update(dispute.id, {
      evidence: {
        customer_email_address: dispute.metadata.customer_email,
        customer_name: dispute.metadata.customer_name,
        shipping_tracking_number: dispute.metadata.tracking_number,
      },
    });
  } else {
    // Flag for manual review
    await notifyDisputeTeam(dispute);
  }
  break;

case 'charge.dispute.closed':
  const closedDispute = event.data.object as Stripe.Dispute;
  if (closedDispute.status === 'won') {
    await notifyDisputeWon(closedDispute);
  } else {
    await processDisputeLoss(closedDispute);
  }
  break;
```

## Stripe Identity

### Identity Verification

```typescript
// Create verification session
export async function createIdentityVerification(email: string) {
  const verificationSession = await stripe.identity.verificationSessions.create({
    type: 'document',
    metadata: {
      user_email: email,
    },
    options: {
      document: {
        require_live_capture: true,
        require_matching_selfie: true,
        allowed_types: ['driving_license', 'passport', 'id_card'],
      },
    },
  });

  return {
    clientSecret: verificationSession.client_secret,
    url: verificationSession.url,
  };
}

// Check verification status
export async function checkVerificationStatus(sessionId: string) {
  const session = await stripe.identity.verificationSessions.retrieve(sessionId);

  return {
    status: session.status, // 'requires_input', 'verified', 'canceled'
    verified: session.status === 'verified',
    lastError: session.last_error,
  };
}

// Webhook handler
case 'identity.verification_session.verified':
  const verifiedSession = event.data.object;
  await updateUserVerificationStatus(
    verifiedSession.metadata.user_email,
    'verified'
  );
  break;

case 'identity.verification_session.requires_input':
  const requiresInputSession = event.data.object;
  await notifyUserVerificationIssue(requiresInputSession);
  break;
```

## Stripe Issuing (Card Creation)

### Create Virtual/Physical Cards

```typescript
// Create cardholder
export async function createCardholder(
  name: string,
  email: string,
  phone: string
) {
  const cardholder = await stripe.issuing.cardholders.create({
    name,
    email,
    phone_number: phone,
    billing: {
      address: {
        line1: '123 Main St',
        city: 'San Francisco',
        state: 'CA',
        postal_code: '94111',
        country: 'US',
      },
    },
    type: 'individual',
  });

  return cardholder;
}

// Create virtual card
export async function createVirtualCard(cardholderId: string) {
  const card = await stripe.issuing.cards.create({
    cardholder: cardholderId,
    currency: 'usd',
    type: 'virtual',
    status: 'active',
    spending_controls: {
      spending_limits: [{
        amount: 100000, // $1,000 limit
        interval: 'monthly',
      }],
      allowed_categories: ['food_restaurants', 'gas_stations'],
    },
  });

  return card;
}

// Retrieve card details (PAN, CVV, etc.) - SENSITIVE
export async function getCardDetails(cardId: string) {
  const card = await stripe.issuing.cards.retrieve(cardId, {
    expand: ['number', 'cvc'],
  });

  return {
    number: card.number,
    cvc: card.cvc,
    expMonth: card.exp_month,
    expYear: card.exp_year,
  };
}
```

### Authorization Controls

```typescript
// Webhook: Real-time authorization approval
case 'issuing_authorization.request':
  const authorization = event.data.object as Stripe.Issuing.Authorization;

  // Check spending limits
  const userLimits = await getUserSpendingLimits(authorization.cardholder);

  if (authorization.amount > userLimits.perTransaction) {
    // Decline authorization
    await stripe.issuing.authorizations.decline(authorization.id, {
      metadata: { reason: 'exceeds_limit' },
    });
  } else {
    // Approve authorization
    await stripe.issuing.authorizations.approve(authorization.id);
  }
  break;

case 'issuing_authorization.created':
  // Log transaction for user
  await logCardTransaction(event.data.object);
  break;
```

## Stripe Tax

### Automatic Tax Calculation

```typescript
// Enable tax on Checkout
export async function createCheckoutWithTax(priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [{ price: priceId, quantity: 1 }],
    automatic_tax: { enabled: true },
    customer_update: {
      address: 'auto', // Collect address for tax calculation
      shipping: 'auto',
    },
    success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/cancel`,
  });

  return session;
}

// Calculate tax for custom amount
export async function calculateTax(
  amount: number,
  customerAddress: {
    line1: string;
    city: string;
    state: string;
    postal_code: string;
    country: string;
  }
) {
  const calculation = await stripe.tax.calculations.create({
    currency: 'usd',
    line_items: [{
      amount,
      reference: 'product_001',
    }],
    customer_details: {
      address: customerAddress,
      address_source: 'shipping',
    },
  });

  return {
    amountTotal: calculation.amount_total,
    taxAmount: calculation.tax_amount_exclusive,
    taxBreakdown: calculation.tax_breakdown,
  };
}

// Tax-inclusive pricing
export async function createTaxInclusivePrice() {
  const price = await stripe.prices.create({
    unit_amount: 1000,
    currency: 'usd',
    product: 'prod_xxx',
    tax_behavior: 'inclusive', // Tax is included in price
  });

  return price;
}
```

## Stripe Treasury (Banking-as-a-Service)

### Financial Accounts

```typescript
// Create financial account for user
export async function createFinancialAccount(userId: string) {
  const financialAccount = await stripe.treasury.financialAccounts.create({
    supported_currencies: ['usd'],
    features: {
      card_issuing: { requested: true },
      deposit_insurance: { requested: true },
      financial_addresses: { aba: { requested: true } },
      inbound_transfers: { ach: { requested: true } },
      outbound_payments: {
        ach: { requested: true },
        us_domestic_wire: { requested: true },
      },
    },
    metadata: { user_id: userId },
  });

  return financialAccount;
}

// Get account balance
export async function getAccountBalance(accountId: string) {
  const account = await stripe.treasury.financialAccounts.retrieve(accountId);

  return {
    available: account.balance.cash.usd,
    pending: account.balance.inbound_pending.usd,
  };
}

// Create outbound payment
export async function sendPayment(
  financialAccountId: string,
  amount: number,
  destinationRoutingNumber: string,
  destinationAccountNumber: string
) {
  const outboundPayment = await stripe.treasury.outboundPayments.create({
    financial_account: financialAccountId,
    amount,
    currency: 'usd',
    destination_payment_method_data: {
      type: 'us_bank_account',
      us_bank_account: {
        routing_number: destinationRoutingNumber,
        account_number: destinationAccountNumber,
        account_holder_type: 'individual',
      },
    },
  });

  return outboundPayment;
}
```

## Stripe Climate

### Carbon Removal Contributions

```typescript
// Add carbon removal to checkout
export async function createCheckoutWithClimate(priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [{ price: priceId, quantity: 1 }],
    // Let customer choose carbon removal contribution
    custom_fields: [{
      key: 'climate_contribution',
      label: { type: 'custom', custom: 'Contribute to carbon removal?' },
      type: 'dropdown',
      dropdown: {
        options: [
          { label: 'No contribution', value: '0' },
          { label: '$1 - Remove 1kg CO2', value: '100' },
          { label: '$5 - Remove 5kg CO2', value: '500' },
          { label: '$10 - Remove 10kg CO2', value: '1000' },
        ],
      },
    }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/cancel`,
  });

  return session;
}

// Process climate contribution
export async function createClimateOrder(amount: number, metadata: any) {
  const order = await stripe.climate.orders.create({
    amount, // Amount in cents to spend on carbon removal
    metric_tons: amount / 1000, // ~$1 per kg
    beneficiary: 'your_business',
    metadata,
  });

  return order;
}

// List carbon removal suppliers
export async function listClimateSuppliers() {
  const suppliers = await stripe.climate.suppliers.list({ limit: 10 });
  return suppliers.data;
}
```

## Metered Billing & Usage-Based Pricing

### Setup Usage-Based Subscription

```typescript
// Create metered price
export async function createMeteredPrice(productId: string) {
  const price = await stripe.prices.create({
    product: productId,
    currency: 'usd',
    recurring: {
      interval: 'month',
      usage_type: 'metered', // Charge based on usage
    },
    billing_scheme: 'tiered', // or 'per_unit'
    tiers_mode: 'graduated',
    tiers: [
      { up_to: 1000, unit_amount: 10 }, // $0.10 per unit for first 1000
      { up_to: 5000, unit_amount: 8 },  // $0.08 per unit for 1001-5000
      { up_to: 'inf', unit_amount: 5 }, // $0.05 per unit for 5001+
    ],
  });

  return price;
}

// Report usage
export async function reportUsage(
  subscriptionItemId: string,
  quantity: number,
  action: 'increment' | 'set' = 'increment'
) {
  const usageRecord = await stripe.subscriptionItems.createUsageRecord(
    subscriptionItemId,
    {
      quantity,
      timestamp: Math.floor(Date.now() / 1000),
      action, // 'increment' adds to total, 'set' overwrites
    },
    { idempotencyKey: `usage_${subscriptionItemId}_${Date.now()}` }
  );

  return usageRecord;
}

// Get usage summary
export async function getUsageSummary(subscriptionItemId: string) {
  const summary = await stripe.subscriptionItems.listUsageRecordSummaries(
    subscriptionItemId,
    { limit: 1 }
  );

  return {
    totalUsage: summary.data[0]?.total_usage || 0,
    period: {
      start: summary.data[0]?.period?.start,
      end: summary.data[0]?.period?.end,
    },
  };
}
```

### Real-World Usage Tracking

```typescript
// Track API calls
export async function trackApiCall(userId: string, endpoint: string) {
  const user = await getUser(userId);

  if (!user.subscriptionItemId) {
    throw new Error('No active subscription');
  }

  // Report usage to Stripe
  await reportUsage(user.subscriptionItemId, 1, 'increment');

  // Log locally for analytics
  await logApiCall({ userId, endpoint, timestamp: new Date() });
}

// Middleware to track usage
export async function middleware(req: NextRequest) {
  const session = await auth();

  if (session?.user?.id) {
    // Track this request as usage
    await trackApiCall(session.user.id, req.nextUrl.pathname);
  }

  return NextResponse.next();
}
```

## Billing Portal Customization

### Create Custom Billing Portal

```typescript
// Configure portal
export async function configurePortal() {
  const configuration = await stripe.billingPortal.configurations.create({
    business_profile: {
      headline: 'Manage your subscription',
    },
    features: {
      customer_update: {
        enabled: true,
        allowed_updates: ['email', 'address', 'shipping', 'phone', 'tax_id'],
      },
      invoice_history: { enabled: true },
      payment_method_update: { enabled: true },
      subscription_cancel: {
        enabled: true,
        mode: 'at_period_end',
        cancellation_reason: {
          enabled: true,
          options: [
            'too_expensive',
            'missing_features',
            'switched_service',
            'unused',
            'customer_service',
            'too_complex',
            'low_quality',
            'other',
          ],
        },
      },
      subscription_pause: {
        enabled: true,
      },
      subscription_update: {
        enabled: true,
        default_allowed_updates: ['price', 'quantity', 'promotion_code'],
        products: [
          {
            product: 'prod_basic',
            prices: ['price_basic_monthly', 'price_basic_yearly'],
          },
          {
            product: 'prod_pro',
            prices: ['price_pro_monthly', 'price_pro_yearly'],
          },
        ],
      },
    },
  });

  return configuration.id;
}

// Create portal session with config
export async function createCustomPortalSession(
  customerId: string,
  configId: string
) {
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_URL}/dashboard`,
    configuration: configId,
  });

  return session.url;
}
```

## Testing & Development

### Test Mode Helpers

```typescript
// lib/stripe/test-helpers.ts
export async function createTestCustomer(email: string) {
  if (!process.env.STRIPE_SECRET_KEY?.startsWith('sk_test_')) {
    throw new Error('Test helpers only work in test mode');
  }

  const customer = await stripe.customers.create({
    email,
    metadata: { test: 'true' },
  });

  return customer;
}

export async function createTestSubscription(
  customerId: string,
  priceId: string
) {
  // Use test card that won't require payment
  const paymentMethod = await stripe.paymentMethods.create({
    type: 'card',
    card: { token: 'tok_visa' }, // Test token
  });

  await stripe.paymentMethods.attach(paymentMethod.id, { customer: customerId });

  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    default_payment_method: paymentMethod.id,
  });

  return subscription;
}

// Trigger test webhook locally
export async function triggerTestWebhook(eventType: string) {
  // Uses Stripe CLI: stripe trigger <event>
  const { exec } = require('child_process');
  exec(`stripe trigger ${eventType}`);
}
```

### Test Scenarios

```typescript
// Test card numbers for different scenarios
export const TEST_CARDS = {
  // Successful payments
  visa: '4242424242424242',
  mastercard: '5555555555554444',
  amex: '378282246310005',
  discover: '6011111111111117',

  // 3D Secure required
  visa3DS: '4000002500003155',
  visa3DSDecline: '4000008400001629',

  // Declined
  genericDecline: '4000000000009995',
  insufficientFunds: '4000000000009987',
  lostCard: '4000000000009987',
  stolenCard: '4000000000009979',
  expiredCard: '4000000000000069',
  incorrectCVC: '4000000000000127',
  processingError: '4000000000000119',

  // Other scenarios
  disputeWarning: '4000000000002685', // Triggers early fraud warning
  alwaysDispute: '4000000000000259', // Will be disputed immediately
};

// Test with specific card
export async function testPaymentFlow(scenario: keyof typeof TEST_CARDS) {
  const paymentMethod = await stripe.paymentMethods.create({
    type: 'card',
    card: { number: TEST_CARDS[scenario], exp_month: 12, exp_year: 2034, cvc: '123' },
  });

  const paymentIntent = await stripe.paymentIntents.create({
    amount: 1000,
    currency: 'usd',
    payment_method: paymentMethod.id,
    confirm: true,
  });

  return paymentIntent;
}
```

## Performance Optimization

### Expand Related Objects

```typescript
// Bad: Multiple API calls
const invoice = await stripe.invoices.retrieve('in_xxx');
const subscription = await stripe.subscriptions.retrieve(invoice.subscription);
const customer = await stripe.customers.retrieve(invoice.customer);

// Good: Single API call with expand
const invoice = await stripe.invoices.retrieve('in_xxx', {
  expand: ['subscription', 'customer', 'payment_intent'],
});

// Now access directly
console.log(invoice.subscription.status);
console.log(invoice.customer.email);
console.log(invoice.payment_intent.client_secret);
```

### Batch Operations

```typescript
// Retrieve multiple customers efficiently
export async function batchRetrieveCustomers(customerIds: string[]) {
  const customers = await Promise.all(
    customerIds.map(id =>
      stripe.customers.retrieve(id).catch(() => null) // Handle missing customers
    )
  );

  return customers.filter(Boolean);
}

// Use list endpoints with pagination
export async function getAllActiveSubscriptions() {
  const subscriptions: Stripe.Subscription[] = [];
  let hasMore = true;
  let startingAfter: string | undefined;

  while (hasMore) {
    const page = await stripe.subscriptions.list({
      status: 'active',
      limit: 100,
      starting_after: startingAfter,
    });

    subscriptions.push(...page.data);
    hasMore = page.has_more;
    startingAfter = page.data[page.data.length - 1]?.id;
  }

  return subscriptions;
}
```

### Caching Strategies

```typescript
// Cache prices (they rarely change)
import { unstable_cache } from 'next/cache';

export const getPrices = unstable_cache(
  async () => {
    const prices = await stripe.prices.list({
      active: true,
      expand: ['data.product'],
    });
    return prices.data;
  },
  ['stripe-prices'],
  {
    revalidate: 3600, // 1 hour
    tags: ['prices'],
  }
);

// Invalidate cache when price changes
export async function POST(req: Request) {
  const event = await verifyWebhook(req);

  if (event.type === 'price.updated' || event.type === 'price.created') {
    revalidateTag('prices');
  }

  return Response.json({ received: true });
}
```

## Documentation Quick Reference

**Need to find something specific?**

Use Grep to search the 3,253 documentation files:

```bash
# Search all docs
grep -r "search term" .claude/skills/api/stripe/docs/

# Search API references only
grep -r "search term" .claude/skills/api/stripe/docs/api/

# Find specific endpoint
ls .claude/skills/api/stripe/docs/api/payment_intents/
```

**Common doc locations:**
- API Reference: `docs/api/`
- Payment Intents: `docs/api/payment_intents/`
- Subscriptions: `docs/api/subscriptions/`
- Webhooks: `docs/api/webhook_endpoints/`
- Connect: `docs/api/accounts/`

## Resources

- **Dashboard:** https://dashboard.stripe.com
- **API Docs:** https://docs.stripe.com/api
- **Testing:** https://docs.stripe.com/testing
- **Stripe CLI:** https://docs.stripe.com/stripe-cli
- **Status:** https://status.stripe.com
- **Changelog:** https://docs.stripe.com/changelog

## Implementation Checklist

**Setup:**
- [ ] Install SDK: `npm install stripe @stripe/stripe-js @stripe/react-stripe-js`
- [ ] Get API keys from Dashboard (test + live)
- [ ] Set environment variables
- [ ] Configure TypeScript types

**Payment Flow:**
- [ ] Choose integration (Checkout vs Payment Element vs Payment Links)
- [ ] Implement payment creation (server-side)
- [ ] Add client-side payment UI
- [ ] Handle payment confirmation
- [ ] Add error handling with proper user messages
- [ ] Add loading states
- [ ] Test 3D Secure flow

**Webhooks:**
- [ ] Create webhook endpoint (`/api/webhooks`)
- [ ] Verify webhook signatures (CRITICAL)
- [ ] Handle key events (payment_intent.succeeded, customer.subscription.*)
- [ ] Test with Stripe CLI
- [ ] Deploy and configure webhook in Dashboard
- [ ] Monitor webhook delivery

**Production:**
- [ ] Implement retry logic with exponential backoff
- [ ] Add idempotency keys for critical operations
- [ ] Set up rate limiting
- [ ] Security audit (no exposed keys, webhook verification)
- [ ] Test in production mode before launch
- [ ] Set up monitoring and alerts
- [ ] Document runbook for common issues

**Advanced (if needed):**
- [ ] Configure Connect for marketplaces
- [ ] Set up Radar rules for fraud prevention
- [ ] Enable automatic tax calculation
- [ ] Configure billing portal
- [ ] Set up usage-based billing
- [ ] Implement dispute handling
