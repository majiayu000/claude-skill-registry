---
name: treido-backend
description: Build and modify Treido server-side logic including Server Actions, API routes, Stripe integration, and caching. Use when working on app/actions/, app/api/, lib/ directories, webhooks, payment flows, or any server-side data fetching. Triggers include creating actions, API endpoints, Stripe checkout/webhooks, or fixing caching issues.
deprecated: true
---

# Treido Backend

> Deprecated (2026-01-29). Use `treido-orchestrator` + `treido-impl-backend` (and `treido-audit-*` + `treido-verify`).

## Quick Start

1. Identify the entrypoint (action, route handler, or webhook)
2. Define the contract (input/output types, auth requirements, error cases)
3. Implement (1-3 files max per batch)
4. Run verification: `pnpm -s typecheck && pnpm -s lint`

## Decision Tree

```
What are you building?
├─ Server Action → app/actions/ (shared) or app/[locale]/(group)/**/_actions/ (route-private)
├─ API Route → app/api/**/route.ts
├─ Stripe webhook → app/api/webhooks/stripe/route.ts
├─ Utility function → lib/
└─ UI component → Wrong skill. Use treido-frontend
```

## File Boundaries

| Type | Location | Rule |
|------|----------|------|
| Shared actions | `app/actions/` | Used across multiple routes |
| Route-private actions | `app/[locale]/(group)/**/_actions/` | Single route only |
| API routes | `app/api/` | REST endpoints, webhooks |
| Utilities | `lib/` | Pure functions, no React |

## Server Actions

### Basic Pattern
```tsx
// app/actions/cart.ts
'use server';

import { revalidateTag } from 'next/cache';
import { createClient } from '@/lib/supabase/server';

export async function addToCart(productId: string, quantity: number) {
  // 1. Validate input
  if (!productId || quantity < 1) {
    throw new Error('Invalid input');
  }
  
  // 2. Get authenticated client
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    throw new Error('Unauthorized');
  }
  
  // 3. Perform operation
  const { error } = await supabase
    .from('cart_items')
    .insert({ user_id: user.id, product_id: productId, quantity });
  
  if (error) throw error;
  
  // 4. Invalidate cache
  revalidateTag('cart');
}
```

## API Routes

### Basic Pattern
```tsx
// app/api/products/route.ts
import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET(request: Request) {
  const supabase = await createClient();
  
  const { data, error } = await supabase
    .from('products')
    .select('id, title, price, images')
    .eq('status', 'active')
    .limit(20);
  
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  
  return NextResponse.json(data);
}
```

## Security Rules (Non-Negotiable)

### No Secrets in Logs
```tsx
// ❌ FORBIDDEN - leaks sensitive data
console.log('User data:', user);
console.log('Headers:', request.headers);
console.log('Token:', session.access_token);

// ✅ CORRECT - safe logging
console.log('Processing request for user:', user.id);
console.log('Action completed');
```

### Supabase Query Projections
```tsx
// ❌ FORBIDDEN in hot paths
const { data } = await supabase.from('products').select('*');

// ✅ CORRECT - explicit field projection
const { data } = await supabase
  .from('products')
  .select('id, title, price, images');
```

## Stripe Integration

### Checkout Session
```tsx
// app/actions/checkout.ts
'use server';

import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function createCheckoutSession(items: CartItem[]) {
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: items.map(item => ({
      price_data: {
        currency: 'bgn',
        product_data: { name: item.title },
        unit_amount: item.price * 100, // cents
      },
      quantity: item.quantity,
    })),
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/checkout/success`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/checkout/cancel`,
  });
  
  return session.url;
}
```

### Webhook Handler
```tsx
// app/api/webhooks/stripe/route.ts
import Stripe from 'stripe';
import { headers } from 'next/headers';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(request: Request) {
  const body = await request.text();
  const headersList = await headers();
  const signature = headersList.get('stripe-signature')!;
  
  // 1. Verify signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Invalid signature', { status: 400 });
  }
  
  // 2. Handle event (idempotently)
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object);
      break;
    // Add other event types
  }
  
  return new Response('OK');
}
```

## Caching Rules

### With 'use cache'
```tsx
'use cache';

import { cacheLife, cacheTag } from 'next/cache';

export async function getProducts() {
  cacheLife('hours');
  cacheTag('products');
  
  const supabase = await createClient();
  const { data } = await supabase
    .from('products')
    .select('id, title, price');
  
  return data;
}
```

### ⚠️ FORBIDDEN in Cached Functions
```tsx
'use cache';

// ❌ NEVER call these inside cached functions
import { cookies, headers } from 'next/headers';
await cookies();  // FORBIDDEN
await headers();  // FORBIDDEN
```

## Verification

After every change:

```bash
pnpm -s typecheck && pnpm -s lint
```

For payment/auth flows:

```bash
REUSE_EXISTING_SERVER=true pnpm -s test:e2e:smoke
```

## References

**For caching patterns:** See [references/caching.md](references/caching.md)
**For Stripe patterns:** See [references/stripe.md](references/stripe.md)
