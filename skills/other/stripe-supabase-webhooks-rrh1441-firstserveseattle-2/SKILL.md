---
name: stripe-supabase-webhooks
description: This skill should be used when implementing Stripe webhook handlers in Next.js App Router with Supabase database integration. It applies when handling subscription lifecycle events, syncing payment status to a database, implementing upsert logic with fallback strategies, or sending transactional emails on payment events. Triggers on requests involving Stripe webhooks, subscription management, payment event handling, or Supabase subscriber tables.
---

# Stripe Supabase Webhooks

## Overview

This skill provides patterns for implementing robust Stripe webhook handlers in Next.js App Router applications that sync subscription state to Supabase. It covers signature verification, event dispatching, intelligent upsert strategies, and transactional email integration.

## Core Patterns

### 1. Route Handler Setup

```typescript
// app/api/stripe-webhook/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

export const dynamic = 'force-dynamic'; // Disable edge caching

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-27.acacia' as Stripe.LatestApiVersion,
});

const supa = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // Use service role for webhooks
);
```

### 2. Webhook Signature Verification

Always verify signatures before processing:

```typescript
export async function POST(req: NextRequest) {
  const rawBody = Buffer.from(await req.arrayBuffer());
  const sig = req.headers.get('stripe-signature') ?? '';

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      rawBody,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!,
    );
  } catch (err) {
    console.warn('Signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // Process event...
  return NextResponse.json({ received: true });
}
```

### 3. Cascading Upsert Strategy

When syncing Stripe data to Supabase, use a cascading lookup strategy to handle various user identification scenarios:

```typescript
async function upsertSubscriber(fields: {
  stripeCustomerId: string;
  stripeSubscriptionId?: string;
  userId?: string;        // From auth
  email?: string;         // From Stripe customer
  plan?: string;
  status?: Stripe.Subscription.Status | 'expired';
  hasCard?: boolean;
  trialEnd?: number | null;
}) {
  const updateData = {
    stripe_customer_id: fields.stripeCustomerId,
    stripe_subscription_id: fields.stripeSubscriptionId,
    email: fields.email,
    plan: fields.plan,
    status: fields.status,
    has_card: fields.hasCard,
    trial_end: fields.trialEnd,
    updated_at: new Date().toISOString(),
  };

  // Priority 1: Update by user_id (most reliable for authenticated users)
  if (fields.userId) {
    const { data: existing } = await supa
      .from('subscribers')
      .select('id')
      .eq('user_id', fields.userId)
      .maybeSingle();

    if (existing) {
      await supa.from('subscribers').update(updateData).eq('user_id', fields.userId);
      return;
    }
  }

  // Priority 2: Update by email (handles pre-signup records)
  if (fields.email) {
    const { data: existing } = await supa
      .from('subscribers')
      .select('id')
      .eq('email', fields.email)
      .maybeSingle();

    if (existing) {
      await supa.from('subscribers').update(updateData).eq('email', fields.email);
      return;
    }
  }

  // Priority 3: Upsert by stripe_customer_id (fallback)
  await supa
    .from('subscribers')
    .upsert(updateData, { onConflict: 'stripe_customer_id' });
}
```

### 4. Event Type Handling

Handle subscription lifecycle events with proper customer data retrieval:

```typescript
switch (event.type) {
  case 'checkout.session.completed': {
    const session = event.data.object as Stripe.Checkout.Session;
    const custId = session.customer as string;
    const subId = session.subscription as string;

    const customer = await stripe.customers.retrieve(custId) as Stripe.Customer;
    const subscription = await stripe.subscriptions.retrieve(subId);

    await upsertSubscriber({
      stripeCustomerId: custId,
      stripeSubscriptionId: subId,
      userId: session.metadata?.userId || session.client_reference_id,
      email: customer.email ?? session.customer_details?.email ?? '',
      plan: planFromPrice(subscription.items.data[0]?.price.id ?? ''),
      status: subscription.status,
      hasCard: true,
      trialEnd: subscription.trial_end,
    });

    // Send welcome email
    if (customer.email) {
      await EmailService.sendWelcomeEmail(customer.email, plan);
    }
    break;
  }

  case 'customer.subscription.updated': {
    const sub = event.data.object as Stripe.Subscription;
    const customer = await stripe.customers.retrieve(sub.customer as string) as Stripe.Customer;

    await upsertSubscriber({
      stripeCustomerId: sub.customer as string,
      stripeSubscriptionId: sub.id,
      email: customer.email ?? '',
      plan: planFromPrice(sub.items.data[0]?.price.id ?? ''),
      status: sub.status,
      hasCard: cardOnFile(customer),
      trialEnd: sub.trial_end,
    });
    break;
  }

  case 'customer.subscription.deleted': {
    const sub = event.data.object as Stripe.Subscription;
    await upsertSubscriber({
      stripeCustomerId: sub.customer as string,
      stripeSubscriptionId: sub.id,
      status: 'canceled',
      hasCard: false,
    });
    break;
  }

  case 'invoice.payment_succeeded':
  case 'invoice.payment_failed': {
    const inv = event.data.object as Stripe.Invoice;
    const customer = await stripe.customers.retrieve(inv.customer as string) as Stripe.Customer;

    await upsertSubscriber({
      stripeCustomerId: inv.customer as string,
      stripeSubscriptionId: inv.subscription as string | undefined,
      email: customer.email ?? '',
      status: inv.status as Stripe.Subscription.Status,
    });
    break;
  }
}
```

### 5. Helper Functions

```typescript
/** Check if customer has payment method on file */
function cardOnFile(cust: Stripe.Customer): boolean {
  return Boolean(
    cust.invoice_settings?.default_payment_method || cust.default_source
  );
}

/** Map Stripe price ID to internal plan name */
function planFromPrice(priceId: string): string {
  const PRICE_MAP: Record<string, string> = {
    [process.env.STRIPE_MONTHLY_PRICE_ID!]: 'monthly',
    [process.env.STRIPE_ANNUAL_PRICE_ID!]: 'annual',
  };
  return PRICE_MAP[priceId] ?? 'unknown';
}
```

## Key Events to Handle

| Event | When It Fires | Action |
|-------|--------------|--------|
| `checkout.session.completed` | Customer completes checkout | Create/update subscriber, send welcome email |
| `customer.subscription.updated` | Any subscription change | Sync status, plan, trial_end |
| `customer.subscription.deleted` | Subscription canceled/expired | Mark as canceled |
| `payment_method.attached` | Card added | Update has_card flag |
| `customer.updated` | Customer email/payment changes | Sync email and card status |
| `invoice.payment_succeeded` | Successful renewal | Update status |
| `invoice.payment_failed` | Failed payment | Update status, send failure email |

## Database Schema Requirements

```sql
CREATE TABLE subscribers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE REFERENCES auth.users(id),
  email TEXT,
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT,
  plan TEXT CHECK (plan IN ('monthly', 'annual', 'unknown')),
  status TEXT,
  has_card BOOLEAN DEFAULT false,
  trial_end BIGINT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_stripe_customer ON subscribers(stripe_customer_id);
```

## Environment Variables

```env
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_MONTHLY_PRICE_ID=price_...
STRIPE_ANNUAL_PRICE_ID=price_...
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

## Testing Webhooks Locally

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Forward webhooks to local dev server
stripe listen --forward-to localhost:3000/api/stripe-webhook

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```

## References

See `references/event-handling.md` for detailed event payload examples and edge cases.
