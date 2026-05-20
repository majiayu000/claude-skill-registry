---
name: billing-subscriptions
description: |
  Multi-provider billing and subscription system for this Next.js application.
  Covers Gateway Factory pattern, Stripe integration, Polar.sh integration, Better Auth plugin,
  plans configuration, checkout flow, customer portal, webhooks, and usage tracking.
  Use this skill when implementing billing features or working with subscription management.
allowed-tools: Read, Glob, Grep
version: 3.0.0
---

# Billing & Subscriptions Skill

Multi-provider billing system with Gateway Factory pattern. Supports Stripe, Polar.sh, and future providers through a unified interface.

## Architecture Overview

```
BILLING ARCHITECTURE:

Configuration Layer:
contents/themes/{theme}/config/billing.config.ts
├── provider: 'stripe' | 'polar'  # (paddle, lemonsqueezy, mercadopago: type defined, not yet implemented)
├── currency: 'usd' | 'eur' | ...
├── defaultPlan: 'free'
├── features: { featureSlug: FeatureDefinition }
├── limits: { limitSlug: LimitDefinition }
├── plans: PlanDefinition[]
└── actionMappings: ActionMappings

Core Library:
core/lib/billing/
├── config-types.ts      # BillingConfig, PlanDefinition interfaces
├── types.ts             # PlanType, SubscriptionStatus, PaymentProvider
├── schema.ts            # Zod validation schemas
├── gateways/
│   ├── types.ts         # Provider-agnostic result types
│   ├── interface.ts     # BillingGateway interface (contract)
│   ├── factory.ts       # getBillingGateway() factory
│   ├── stripe.ts        # StripeGateway implements BillingGateway
│   └── polar.ts         # PolarGateway implements BillingGateway
├── queries.ts           # Database queries
├── enforcement.ts       # Limit/feature enforcement
├── helpers.ts           # Utility functions
└── jobs.ts              # Background jobs

Services Layer:
core/lib/services/
├── subscription.service.ts  # Subscription CRUD (uses factory)
├── plan.service.ts          # Plan management (getPriceId generic)
└── usage.service.ts         # Usage tracking

API Endpoints:
app/api/v1/billing/
├── checkout/route.ts        # Create checkout session (via factory)
├── portal/route.ts          # Customer portal access (via factory)
├── plans/route.ts           # List available plans
├── cancel/route.ts          # Cancel subscription (via factory)
├── change-plan/route.ts     # Upgrade/downgrade
├── check-action/route.ts    # Permission check
├── webhooks/stripe/route.ts # Stripe webhooks (provider-specific)
└── webhooks/polar/route.ts  # Polar webhooks (provider-specific)
```

## When to Use This Skill

- Implementing billing features
- Working with subscription management
- Configuring plans and features
- Adding a new payment provider
- Setting up webhooks (Stripe or Polar)
- Implementing usage limits
- Testing billing flows

## Gateway Factory Pattern

**Key Principle:** Consumers never import from a specific provider. They use `getBillingGateway()` which returns the correct implementation based on `billing.config.ts`.

### BillingGateway Interface

```typescript
// core/lib/billing/gateways/interface.ts
export interface BillingGateway {
  // Checkout
  createCheckoutSession(params: CreateCheckoutParams): Promise<CheckoutSessionResult>
  createPortalSession(params: CreatePortalParams): Promise<PortalSessionResult>

  // Customers
  getCustomer(customerId: string): Promise<CustomerResult>
  createCustomer(params: CreateCustomerParams): Promise<CustomerResult>

  // Subscription Management
  updateSubscriptionPlan(params: UpdateSubscriptionParams): Promise<SubscriptionResult>
  cancelSubscriptionAtPeriodEnd(subscriptionId: string): Promise<SubscriptionResult>
  cancelSubscriptionImmediately(subscriptionId: string): Promise<SubscriptionResult>
  reactivateSubscription(subscriptionId: string): Promise<SubscriptionResult>

  // Webhooks (Stripe passes string signature, Polar passes headers Record)
  verifyWebhookSignature(payload: string | Buffer, signatureOrHeaders: string | Record<string, string>): WebhookEventResult

  // Dashboard & Metadata
  getProviderName(): string
  getSubscriptionDashboardUrl(externalSubscriptionId: string | null | undefined): string | null
  getResourceHintDomains(): { preconnect: string[]; dnsPrefetch: string[] }
}
```

### Provider-Agnostic Types

```typescript
// core/lib/billing/gateways/types.ts
// Return types - NO Stripe.* or Polar.* imports

export interface CheckoutSessionResult {
  id: string
  url: string | null
}

export interface PortalSessionResult {
  url: string
}

export interface SubscriptionResult {
  id: string
  status: string
  cancelAtPeriodEnd: boolean
}

export interface CustomerResult {
  id: string
  email: string | null
  name: string | null
}

export interface WebhookEventResult {
  id: string
  type: string
  data: Record<string, unknown>
}
```

### Factory Usage

```typescript
// CORRECT: Use factory everywhere
import { getBillingGateway } from '@nextsparkjs/core/lib/billing/gateways/factory'

const session = await getBillingGateway().createCheckoutSession(params)
const portal = await getBillingGateway().createPortalSession(params)
await getBillingGateway().cancelSubscriptionAtPeriodEnd(subId)

// Provider metadata
const name = getBillingGateway().getProviderName()             // "Stripe" or "Polar"
const url = getBillingGateway().getSubscriptionDashboardUrl(id) // Dashboard URL or null

// Resource hints (used in layout.tsx automatically)
import { getBillingResourceHints } from '@nextsparkjs/core/lib/billing/gateways/factory'
const { preconnect, dnsPrefetch } = getBillingResourceHints()

// WRONG: Import from specific provider
import { createCheckoutSession } from '.../gateways/stripe'  // DEPRECATED
```

### Plan Price IDs

Plans use `providerPriceIds` for price configuration (works with any provider):

```typescript
// PlanDefinition in config-types.ts
{
  slug: 'pro',
  providerPriceIds: {
    monthly: 'price_xxx_monthly',
    yearly: 'price_xxx_yearly',
  },
}

// PlanService.getPriceId() reads from providerPriceIds
const priceId = PlanService.getPriceId('pro', 'monthly')
```

## Provider: Stripe

### SDK & Packages

```bash
# Required
pnpm add stripe
```

### Environment Variables

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### StripeGateway Class

```typescript
// core/lib/billing/gateways/stripe.ts
export class StripeGateway implements BillingGateway {
  async createCheckoutSession(params) {
    const session = await getStripe().checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: params.successUrl,
      cancel_url: params.cancelUrl,
      metadata: { teamId, planSlug, billingPeriod },
    })
    return { id: session.id, url: session.url }  // Provider-agnostic
  }

  async createPortalSession(params) {
    const session = await getStripe().billingPortal.sessions.create({
      customer: params.customerId,
      return_url: params.returnUrl,
    })
    return { url: session.url }
  }

  verifyWebhookSignature(payload, signature) {
    const event = getStripe().webhooks.constructEvent(payload, signature, secret)
    return { id: event.id, type: event.type, data: event.data }
  }

  // ... other methods
}
```

### Stripe Webhook Events

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Create/update subscription with Stripe IDs |
| `invoice.paid` | Update period dates, sync invoice |
| `invoice.payment_failed` | Mark subscription as `past_due` |
| `customer.subscription.updated` | Sync status and plan changes |
| `customer.subscription.deleted` | Mark subscription as `canceled` |

### Stripe Webhook Route (Provider-Specific)

```typescript
// app/api/v1/billing/webhooks/stripe/route.ts
// NOTE: Webhook routes stay provider-specific by design.
// They need raw provider types for proper type narrowing.
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: NextRequest) {
  const payload = await request.text()
  const signature = request.headers.get('stripe-signature')!
  const event = stripe.webhooks.constructEvent(
    payload, signature, process.env.STRIPE_WEBHOOK_SECRET!
  )

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object as Stripe.Checkout.Session
      // Handle with full Stripe types
      break
  }
}
```

## Provider: Polar.sh

### SDK & Packages

```bash
# Core SDK
pnpm add @polar-sh/sdk

# Next.js adapter (optional - pre-built route handlers)
pnpm add @polar-sh/nextjs

# Better Auth plugin (optional - auth-integrated billing)
pnpm add @polar-sh/better-auth
```

### Environment Variables

```env
POLAR_ACCESS_TOKEN=pat_...          # Organization Access Token
POLAR_WEBHOOK_SECRET=whsec_...
POLAR_SERVER=sandbox                 # 'sandbox' or 'production'
```

### Integration Path A: PolarGateway (via our factory)

This is the primary integration path. Consistent with Stripe, goes through `getBillingGateway()`.

```typescript
// core/lib/billing/gateways/polar.ts
import { Polar } from '@polar-sh/sdk'
import { validateEvent, WebhookVerificationError } from '@polar-sh/sdk/webhooks'
import type { BillingGateway } from './interface'

let polarInstance: Polar | null = null

function getPolar(): Polar {
  if (!polarInstance) {
    polarInstance = new Polar({
      accessToken: process.env.POLAR_ACCESS_TOKEN!,
      server: (process.env.POLAR_SERVER as 'sandbox' | 'production') || 'production',
    })
  }
  return polarInstance
}

export class PolarGateway implements BillingGateway {
  async createCheckoutSession(params) {
    const priceId = getPriceIdFromRegistry(params.planSlug, params.billingPeriod)
    const result = await getPolar().checkouts.create({
      productPriceId: priceId,           // Polar uses productPriceId
      successUrl: params.successUrl,
      returnUrl: params.cancelUrl,       // Polar calls it returnUrl
      customerEmail: params.customerEmail,
      metadata: { teamId: params.teamId, planSlug: params.planSlug },
    })
    return { id: result.id, url: result.url }
  }

  async createPortalSession(params) {
    const result = await getPolar().customerSessions.create({
      customerId: params.customerId,
      returnUrl: params.returnUrl,
    })
    return { url: result.customerPortalUrl }  // Different field name
  }

  async getCustomer(customerId) {
    const customer = await getPolar().customers.get({ id: customerId })
    return { id: customer.id, email: customer.email, name: customer.name }
  }

  async createCustomer(params) {
    const customer = await getPolar().customers.create({
      email: params.email,
      name: params.name,
      externalId: params.metadata?.userId,  // Map to app userId
    })
    return { id: customer.id, email: customer.email, name: customer.name }
  }

  async updateSubscriptionPlan(params) {
    const result = await getPolar().subscriptions.update({
      id: params.subscriptionId,
      subscriptionUpdate: { productPriceId: params.newPriceId },
    })
    return {
      id: result.id,
      status: result.status,
      cancelAtPeriodEnd: result.cancelAtPeriodEnd,
    }
  }

  async cancelSubscriptionAtPeriodEnd(subscriptionId) {
    // Polar: customer portal cancel = cancel at period end
    const result = await getPolar().subscriptions.update({
      id: subscriptionId,
      subscriptionUpdate: { cancelAtPeriodEnd: true },
    })
    return { id: result.id, status: result.status, cancelAtPeriodEnd: true }
  }

  async cancelSubscriptionImmediately(subscriptionId) {
    // Polar: revoke = immediate cancel
    const result = await getPolar().subscriptions.revoke({ id: subscriptionId })
    return { id: result.id, status: 'canceled', cancelAtPeriodEnd: false }
  }

  async reactivateSubscription(subscriptionId) {
    const result = await getPolar().subscriptions.update({
      id: subscriptionId,
      subscriptionUpdate: { cancelAtPeriodEnd: false },
    })
    return { id: result.id, status: result.status, cancelAtPeriodEnd: false }
  }

  verifyWebhookSignature(payload, signature) {
    // Polar validates against headers object, not a single signature string
    // The signature param here carries the headers as JSON for compatibility
    const headers = JSON.parse(signature as string)
    const event = validateEvent(payload, headers, process.env.POLAR_WEBHOOK_SECRET!)
    return { id: event.data.id, type: event.type, data: event.data as any }
  }
}
```

### Polar Webhook Events

| Event | Action |
|-------|--------|
| `checkout.created` | Checkout started |
| `checkout.updated` | Checkout updated |
| `order.created` | Order placed |
| `order.paid` | Payment confirmed - create/update subscription |
| `order.refunded` | Refund processed |
| `subscription.created` | New subscription |
| `subscription.updated` | Subscription changed |
| `subscription.active` | Subscription activated |
| `subscription.canceled` | Subscription canceled |
| `subscription.revoked` | Subscription immediately revoked |
| `subscription.uncanceled` | Cancellation reversed |
| `customer.created` | New customer |
| `customer.state_changed` | Customer state updated |

### Polar Webhook Route (Provider-Specific)

```typescript
// app/api/v1/billing/webhooks/polar/route.ts
import { validateEvent, WebhookVerificationError } from '@polar-sh/sdk/webhooks'

export async function POST(request: NextRequest) {
  const payload = await request.text()
  const headers = Object.fromEntries(request.headers.entries())

  try {
    const event = validateEvent(payload, headers, process.env.POLAR_WEBHOOK_SECRET!)

    switch (event.type) {
      case 'order.paid':
        await handleOrderPaid(event.data)
        break
      case 'subscription.active':
        await handleSubscriptionActive(event.data)
        break
      case 'subscription.canceled':
        await handleSubscriptionCanceled(event.data)
        break
      case 'subscription.revoked':
        await handleSubscriptionRevoked(event.data)
        break
      case 'subscription.uncanceled':
        await handleSubscriptionUncanceled(event.data)
        break
    }

    return NextResponse.json({ received: true })
  } catch (error) {
    if (error instanceof WebhookVerificationError) {
      return NextResponse.json({ error: 'Invalid signature' }, { status: 403 })
    }
    throw error
  }
}
```

### Polar Next.js Adapter (Shortcut)

Pre-built route handlers for simple setups:

```typescript
// app/api/polar/checkout/route.ts
import { Checkout } from '@polar-sh/nextjs'

export const GET = Checkout({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  successUrl: process.env.NEXT_PUBLIC_APP_URL + '/dashboard/settings/billing?success=true',
  server: 'sandbox',
})

// app/api/polar/portal/route.ts
import { CustomerPortal } from '@polar-sh/nextjs'

export const GET = CustomerPortal({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  getCustomerId: (req) => getCustomerIdFromSession(req),
  returnUrl: process.env.NEXT_PUBLIC_APP_URL + '/dashboard/settings/billing',
})

// app/api/polar/webhooks/route.ts
import { Webhooks } from '@polar-sh/nextjs'

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET!,
  onOrderPaid: async (payload) => { /* sync subscription */ },
  onSubscriptionActive: async (payload) => { /* activate */ },
  onSubscriptionCanceled: async (payload) => { /* cancel */ },
  onSubscriptionRevoked: async (payload) => { /* revoke */ },
})
```

### Integration Path B: Better Auth Plugin

For projects using Better Auth, Polar provides a first-party plugin that auto-creates customers on signup and provides client-side billing methods.

```typescript
// lib/auth.ts (server)
import { betterAuth } from 'better-auth'
import { polar, checkout, portal, usage, webhooks } from '@polar-sh/better-auth'
import { Polar } from '@polar-sh/sdk'

const polarClient = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  server: 'sandbox',
})

export const auth = betterAuth({
  plugins: [
    polar({
      client: polarClient,
      createCustomerOnSignUp: true,   // Auto-create Polar customer
      use: [
        checkout({
          products: [
            { productId: 'prod_xxx', slug: 'pro' },
            { productId: 'prod_yyy', slug: 'enterprise' },
          ],
          successUrl: '/dashboard/settings/billing?success=true',
          authenticatedUsersOnly: true,
        }),
        portal(),
        usage(),
        webhooks({
          secret: process.env.POLAR_WEBHOOK_SECRET!,
          onOrderPaid: (payload) => { /* handle */ },
          onCustomerStateChanged: (payload) => { /* handle */ },
        }),
      ],
    }),
  ],
})
```

```typescript
// lib/auth-client.ts (client)
import { createAuthClient } from 'better-auth/react'
import { polarClient } from '@polar-sh/better-auth/client'

export const authClient = createAuthClient({
  plugins: [polarClient()],
})

// Usage in components:
await authClient.checkout({ products: ['prod_xxx'], slug: 'pro' })
await authClient.customer.portal()
const { data: state } = await authClient.customer.state()
const { data: subs } = await authClient.customer.subscriptions.list({ query: { active: true } })

// Usage-based billing
await authClient.usage.ingest({ event: 'api-call', metadata: { endpoint: '/api/v1/products' } })
const { data: meters } = await authClient.usage.meters.list()
```

### When to Use Path A vs Path B

| | Path A: PolarGateway | Path B: Better Auth Plugin |
|---|---|---|
| **Use when** | Multi-provider support needed | Polar-only project |
| **Architecture** | Goes through gateway factory | Bypasses factory, auth-integrated |
| **Customer creation** | Manual via gateway | Automatic on signup |
| **Client-side API** | Custom hooks + API routes | `authClient.checkout()` etc. |
| **Usage metering** | UsageService (our own) | `authClient.usage.ingest()` |
| **Webhook handling** | Custom route | Better Auth plugin handles it |
| **Recommended for** | NextSpark core (multi-provider) | Theme-specific Polar-only apps |

**For NextSpark core:** Use Path A (PolarGateway) to maintain provider abstraction. Optionally layer Path B for customer auto-creation on signup.

## Provider Comparison: API Mapping

| Operation | Stripe | Polar |
|-----------|--------|-------|
| **SDK init** | `new Stripe(secretKey)` | `new Polar({ accessToken })` |
| **Checkout** | `stripe.checkout.sessions.create()` | `polar.checkouts.create()` |
| **Portal** | `stripe.billingPortal.sessions.create()` | `polar.customerSessions.create()` |
| **Get customer** | `stripe.customers.retrieve(id)` | `polar.customers.get({ id })` |
| **Create customer** | `stripe.customers.create(params)` | `polar.customers.create({ externalId })` |
| **Update sub** | `stripe.subscriptions.update()` (needs item ID) | `polar.subscriptions.update({ productPriceId })` |
| **Soft cancel** | `subscriptions.update({ cancel_at_period_end })` | Customer portal cancel / update |
| **Hard cancel** | `subscriptions.cancel()` | `polar.subscriptions.revoke()` |
| **Verify webhook** | `constructEvent(body, signature, secret)` | `validateEvent(body, headers, secret)` |
| **Env key** | `STRIPE_SECRET_KEY` | `POLAR_ACCESS_TOKEN` |
| **Env webhook** | `STRIPE_WEBHOOK_SECRET` | `POLAR_WEBHOOK_SECRET` |
| **Price ref** | `priceId` (string) | `productPriceId` (string) |

### Key Differences

1. **Webhook verification:** Stripe validates against a single `stripe-signature` header. Polar validates against ALL request headers.
2. **Cancel semantics:** Stripe uses `cancel_at_period_end` flag + `cancel()`. Polar uses `revoke()` for immediate, update for period-end.
3. **Customer identity:** Polar supports `externalId` to map customers to your app's userId. Stripe uses `metadata`.
4. **Subscription update:** Stripe requires finding the subscription item ID first. Polar just takes the new `productPriceId` directly.
5. **Better Auth:** Polar has a first-party Better Auth plugin. Stripe does not.

## Three-Layer Permission Model

The billing system uses a three-layer model (provider-agnostic):

```
RESULT = Permission (RBAC) AND Feature (Plan) AND Quota (Limits)
```

### Layer 1: RBAC Permissions

```typescript
actionMappings: {
  permissions: {
    'team.billing.manage': 'team.billing.manage',
    'team.settings.edit': 'team.settings.edit',
  }
}
```

### Layer 2: Plan Features

```typescript
features: {
  advanced_analytics: { name: 'billing.features.advanced_analytics' },
  api_access: { name: 'billing.features.api_access' },
}

actionMappings: {
  features: {
    'analytics.view_advanced': 'advanced_analytics',
    'api.generate_key': 'api_access',
  }
}
```

### Layer 3: Usage Limits (Quotas)

```typescript
limits: {
  team_members: { name: 'billing.limits.team_members', unit: 'count', resetPeriod: 'never' },
  api_calls: { name: 'billing.limits.api_calls', unit: 'calls', resetPeriod: 'monthly' },
}

actionMappings: {
  limits: {
    'team.members.invite': 'team_members',
    'api.call': 'api_calls',
  }
}
```

## Plans Configuration

### Plan Definition Structure

```typescript
// contents/themes/default/config/billing.config.ts
import type { BillingConfig } from '@/core/lib/billing/config-types'

export const billingConfig: BillingConfig = {
  provider: 'stripe',  // or 'polar'
  currency: 'usd',
  defaultPlan: 'free',

  plans: [
    {
      slug: 'free',
      name: 'billing.plans.free.name',
      type: 'free',
      visibility: 'public',
      price: { monthly: 0, yearly: 0 },
      features: ['basic_analytics'],
      limits: { team_members: 3, tasks: 50, api_calls: 1000 },
      // No price IDs for free plan
    },
    {
      slug: 'pro',
      name: 'billing.plans.pro.name',
      type: 'paid',
      visibility: 'public',
      price: { monthly: 2900, yearly: 29000 },  // in cents
      trialDays: 14,
      features: ['basic_analytics', 'advanced_analytics', 'api_access'],
      limits: { team_members: 15, tasks: 1000, api_calls: 100000 },

      // Price IDs from your payment provider dashboard
      providerPriceIds: {
        monthly: 'price_pro_monthly',
        yearly: 'price_pro_yearly',
      },
    },
    {
      slug: 'enterprise',
      name: 'billing.plans.enterprise.name',
      type: 'enterprise',
      visibility: 'hidden',
      features: ['*'],
      limits: { team_members: -1, tasks: -1, api_calls: -1 },
    },
  ],
}
```

## Team-Based Subscriptions

Subscriptions are tied to teams, not users (provider-agnostic DB schema):

```typescript
{
  id: string
  teamId: string
  planId: string
  status: SubscriptionStatus   // 'active' | 'trialing' | 'past_due' | 'canceled' | 'expired' | 'paused'
  billingInterval: 'monthly' | 'yearly'
  paymentProvider: PaymentProvider | null  // 'stripe' | 'polar' | 'paddle' | 'lemonsqueezy'
  externalSubscriptionId?: string         // Provider subscription ID
  externalCustomerId?: string             // Provider customer ID
  currentPeriodStart: Date
  currentPeriodEnd: Date
  cancelAtPeriodEnd: boolean
}
```

## Checkout Flow (Provider-Agnostic)

```typescript
// app/api/v1/billing/checkout/route.ts
import { getBillingGateway } from '@nextsparkjs/core/lib/billing/gateways/factory'

export async function POST(request: NextRequest) {
  // 1. Authenticate + validate + check permissions
  // ...

  // 2. Create checkout session via gateway (works for any provider)
  const session = await getBillingGateway().createCheckoutSession({
    teamId,
    planSlug,
    billingPeriod,
    successUrl: `${appUrl}/dashboard/settings/billing?success=true`,
    cancelUrl: `${appUrl}/dashboard/settings/billing?canceled=true`,
    customerEmail: user.email,
    customerId: existingCustomerId,
  })

  return Response.json({
    success: true,
    data: { url: session.url, sessionId: session.id }
  })
}
```

## Customer Portal (Provider-Agnostic)

```typescript
// app/api/v1/billing/portal/route.ts
import { getBillingGateway } from '@nextsparkjs/core/lib/billing/gateways/factory'

const session = await getBillingGateway().createPortalSession({
  customerId: subscription.externalCustomerId,
  returnUrl: `${appUrl}/dashboard/settings/billing`,
})

return Response.json({ success: true, data: { url: session.url } })
```

## Webhook Security

```typescript
// CRITICAL: Always verify webhook signatures regardless of provider

// Stripe: single signature header
const event = getStripeInstance().webhooks.constructEvent(payload, signature, secret)

// Polar: validates against all headers
import { validateEvent } from '@polar-sh/sdk/webhooks'
const event = validateEvent(payload, headers, secret)

// NOTE: Webhooks bypass RLS (no user context)
// Use direct query() calls, not queryWithRLS()
```

## Database Schema

### Why Plans/Subscriptions Use Inline JSONB

| Entity Pattern | Storage | Why |
|----------------|---------|-----|
| Regular entities | Separate `{entity}_metas` table | Dynamic, user-extensible |
| `plans` | Inline `features JSONB`, `limits JSONB` | Fixed structure, read-heavy |
| `subscriptions` | No metas needed | All data is structured |

### Migrations

```sql
-- Plans table
CREATE TABLE plans (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  type plan_type NOT NULL DEFAULT 'free',
  visibility plan_visibility NOT NULL DEFAULT 'public',
  "priceMonthly" INTEGER DEFAULT 0,
  "priceYearly" INTEGER DEFAULT 0,
  "trialDays" INTEGER DEFAULT 0,
  features JSONB DEFAULT '[]',
  limits JSONB DEFAULT '{}',
  -- Price IDs stored in providerPriceIds (via billing.config.ts)
  -- Legacy: stripePriceIdMonthly/Yearly columns may exist in older migrations but are unused
  "createdAt" TIMESTAMPTZ DEFAULT NOW(),
  "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions table (provider-agnostic)
CREATE TABLE subscriptions (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "teamId" TEXT REFERENCES teams(id) ON DELETE CASCADE,
  "planId" TEXT REFERENCES plans(id),
  status subscription_status NOT NULL DEFAULT 'active',
  "billingInterval" TEXT DEFAULT 'monthly',
  "paymentProvider" TEXT,                -- 'stripe' | 'polar' | etc.
  "externalSubscriptionId" TEXT,         -- Provider sub ID
  "externalCustomerId" TEXT,             -- Provider customer ID
  "currentPeriodStart" TIMESTAMPTZ,
  "currentPeriodEnd" TIMESTAMPTZ,
  "cancelAtPeriodEnd" BOOLEAN DEFAULT false,
  "createdAt" TIMESTAMPTZ DEFAULT NOW(),
  "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);
```

## Environment Variables

```env
# Provider selection (in billing.config.ts, not env)
# provider: 'stripe' | 'polar'

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Polar
POLAR_ACCESS_TOKEN=pat_...
POLAR_WEBHOOK_SECRET=whsec_...
POLAR_SERVER=sandbox                  # 'sandbox' or 'production'
```

## Anti-Patterns

```typescript
// NEVER: Import from specific provider in consumers
import { createCheckoutSession } from '.../gateways/stripe'  // REMOVED

// CORRECT: Use factory
import { getBillingGateway } from '.../gateways/factory'
await getBillingGateway().createCheckoutSession(params)

// NEVER: Use Stripe-specific types in consumer code
const session: Stripe.Checkout.Session = ...

// CORRECT: Use provider-agnostic types
const session: CheckoutSessionResult = ...

// NEVER: Use getStripePriceId (removed)
PlanService.getStripePriceId('pro', 'monthly')

// CORRECT: Use generic getPriceId
PlanService.getPriceId('pro', 'monthly')

// NEVER: Hardcode plan prices in frontend
const price = '$29.00'

// CORRECT: Use plan config
const price = formatCurrency(plan.price.monthly / 100)

// NEVER: Check plan features manually
if (plan.slug === 'pro' || plan.slug === 'business')

// CORRECT: Use feature checks
const hasFeature = membership.hasFeature('advanced_analytics')

// NEVER: Skip webhook signature verification
const event = JSON.parse(payload)  // UNSAFE!

// CORRECT: Always verify signatures
// Stripe: constructEvent(payload, signature, secret)
// Polar:  validateEvent(payload, headers, secret)

// NEVER: Store prices in dollars
price: { monthly: 29.00 }

// CORRECT: Store prices in cents
price: { monthly: 2900 }

// NEVER: Forget to handle -1 (unlimited)
if (current >= limit) return false

// CORRECT: Check for unlimited
if (limit === -1) return true
if (current >= limit) return false
```

## Checklist

### General (all providers)

- [ ] Provider selected in `billing.config.ts`
- [ ] Plans defined with price IDs (providerPriceIds)
- [ ] Features and limits defined
- [ ] Action mappings configured
- [ ] Team-based subscription created on team creation
- [ ] Checkout flow tested (monthly and yearly)
- [ ] Portal flow tested
- [ ] Webhook endpoint configured in provider dashboard
- [ ] All webhook events handled and tested
- [ ] Usage tracking implemented
- [ ] Limit enforcement working
- [ ] Translations added for plan names/descriptions

### Stripe-specific

- [ ] `STRIPE_SECRET_KEY` configured
- [ ] `STRIPE_WEBHOOK_SECRET` configured
- [ ] Stripe price IDs set in plan definitions
- [ ] Invoice sync working

### Polar-specific

- [ ] `POLAR_ACCESS_TOKEN` configured (Organization Access Token)
- [ ] `POLAR_WEBHOOK_SECRET` configured
- [ ] `POLAR_SERVER` set to `sandbox` or `production`
- [ ] Polar product price IDs set in plan definitions
- [ ] Customer `externalId` mapping to userId working
- [ ] (Optional) Better Auth plugin configured for auto customer creation

## Testing

### Unit Tests

Both gateway implementations have comprehensive Jest unit tests:

```
packages/core/tests/jest/lib/billing/
├── stripe.test.ts    # 38 tests - StripeGateway, factory, deprecated compat
├── polar.test.ts     # 26 tests - PolarGateway, getPolarInstance
└── (billing-queries.test.ts)  # Billing query tests
```

**Mock pattern:** Mock the provider SDK, `PlanService`, and `BILLING_REGISTRY` before importing the gateway class.

```typescript
// Example: Polar test mocks
jest.mock('@polar-sh/sdk', () => ({
  Polar: jest.fn().mockImplementation(() => ({
    checkouts: { create: mockCheckoutsCreate },
    customerSessions: { create: mockCustomerSessionsCreate },
    // ...
  }))
}))

jest.mock('@polar-sh/sdk/webhooks', () => ({
  validateEvent: mockValidateEvent,
  WebhookVerificationError: MockWebhookVerificationError,
}))

jest.mock('@/core/lib/services/plan.service', () => ({
  PlanService: { getPriceId: mockGetPriceId }
}))
```

**Running tests:**
```bash
# All billing tests
cd packages/core && npx jest --config jest.config.cjs tests/jest/lib/billing/

# Specific provider
npx jest --config jest.config.cjs tests/jest/lib/billing/polar.test.ts
npx jest --config jest.config.cjs tests/jest/lib/billing/stripe.test.ts
```

## Related Skills

- `permissions-system` - RBAC integration
- `better-auth` - Authentication patterns (Polar Better Auth plugin)
- `entity-api` - API patterns for billing endpoints
- `service-layer` - Service class patterns
- `database-migrations` - Billing table migrations
