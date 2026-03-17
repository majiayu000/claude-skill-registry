---
name: stripe-connect
description: Implement Stripe Connect OAuth for querying connected accounts. Use when onboarding apps to Connect or querying payment/subscription data on their behalf.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Stripe Connect Integration

Stripe Connect enables the platform to **query** payment and subscription data from connected apps (Total TypeScript, Pro Tailwind, etc.). Each app has their own Stripe account that connects via OAuth.

## Critical Architecture: Query, Don't Execute

**The platform is the orchestrator ("queen of the hive"), not the executor of financial actions.**

```
┌─────────────────────────────────────────────────────────────┐
│                    Support Platform                          │
│                    ("Queen of Hive")                         │
├─────────────────────────────────────────────────────────────┤
│  We QUERY via Connect       │  Apps NOTIFY us via SDK       │
│  ───────────────────        │  ─────────────────────        │
│  • Payment history          │  • Refund processed           │
│  • Subscription status      │  • Access revoked             │
│  • Customer details         │  • License transferred        │
│  • Dispute info             │  • Purchase created           │
└─────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
    Stripe API                    App Integration
    (connected acct)              (SDK webhook)
```

**What we DO with Connect:**
- Query payment history for a customer
- Check subscription status
- Look up charge details for context
- Verify refund status

**What we DON'T do:**
- Process refunds (apps do this)
- Create charges
- Modify subscriptions
- Any financial mutations

**Why?**
- Apps own their financial operations
- Apps notify us when actions complete via SDK
- We provide context/intelligence, not execution
- Simpler, safer, clearer boundaries

## OAuth Flow (Standard Accounts)

### Step 1: Generate Authorization URL

```typescript
// Build OAuth URL with state for CSRF protection
function buildConnectAuthUrl(appSlug: string): string {
  const state = crypto.randomUUID() // Store in cookie for verification

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.STRIPE_CONNECT_CLIENT_ID!,
    scope: 'read_write',
    redirect_uri: `${process.env.NEXT_PUBLIC_URL}/api/stripe/connect/callback`,
    state,
  })

  return `https://connect.stripe.com/oauth/authorize?${params}`
}
```

### Step 2: Handle OAuth Callback

```typescript
// app/api/stripe/connect/callback/route.ts
export async function GET(request: Request) {
  const url = new URL(request.url)
  const code = url.searchParams.get('code')
  const state = url.searchParams.get('state')

  // Verify state matches cookie (CSRF protection)
  // Exchange code for account ID
  const response = await stripe.oauth.token({
    grant_type: 'authorization_code',
    code: code!,
  })

  const stripeAccountId = response.stripe_user_id // acct_xxx

  // Store in apps table
  await db.update(appsTable)
    .set({
      stripe_account_id: stripeAccountId,
      stripe_connected: true,
    })
    .where(eq(appsTable.slug, appSlug))

  return Response.redirect('/settings/integrations?success=connected')
}
```

## Querying Connected Accounts

### Payment History

```typescript
async function getPaymentHistory(params: {
  stripeAccountId: string
  customerEmail: string
  limit?: number
}) {
  const { stripeAccountId, customerEmail, limit = 10 } = params

  // First find the customer on the connected account
  const customers = await stripe.customers.list(
    { email: customerEmail, limit: 1 },
    { stripeAccount: stripeAccountId }
  )

  if (customers.data.length === 0) {
    return []
  }

  const customerId = customers.data[0].id

  // Get their charges
  const charges = await stripe.charges.list(
    { customer: customerId, limit },
    { stripeAccount: stripeAccountId }
  )

  return charges.data.map(charge => ({
    id: charge.id,
    amount: charge.amount,
    currency: charge.currency,
    status: charge.status,
    refunded: charge.refunded,
    created: new Date(charge.created * 1000),
    description: charge.description,
  }))
}
```

### Subscription Status

```typescript
async function getSubscriptionStatus(params: {
  stripeAccountId: string
  customerEmail: string
}) {
  const { stripeAccountId, customerEmail } = params

  const customers = await stripe.customers.list(
    { email: customerEmail, limit: 1 },
    { stripeAccount: stripeAccountId }
  )

  if (customers.data.length === 0) {
    return null
  }

  const subscriptions = await stripe.subscriptions.list(
    { customer: customers.data[0].id, status: 'all' },
    { stripeAccount: stripeAccountId }
  )

  return subscriptions.data.map(sub => ({
    id: sub.id,
    status: sub.status,
    currentPeriodEnd: new Date(sub.current_period_end * 1000),
    cancelAtPeriodEnd: sub.cancel_at_period_end,
    plan: sub.items.data[0]?.price?.nickname,
  }))
}
```

### Verify Refund Status

```typescript
// When app notifies us of a refund, we can verify it
async function verifyRefund(params: {
  stripeAccountId: string
  refundId: string
}) {
  const refund = await stripe.refunds.retrieve(
    params.refundId,
    { stripeAccount: params.stripeAccountId }
  )

  return {
    id: refund.id,
    status: refund.status,
    amount: refund.amount,
    chargeId: refund.charge,
  }
}
```

## Webhook Monitoring (Minimal)

We only monitor events that require platform awareness:

| Event | Purpose | Action |
|-------|---------|--------|
| `account.application.deauthorized` | App disconnected | Clear `stripe_account_id` |
| `charge.dispute.created` | Dispute opened | Alert + flag conversation |

**We do NOT monitor:**
- `charge.refunded` - Apps notify us via SDK
- `customer.subscription.*` - Query on-demand
- `payment_intent.*` - Not our concern

```typescript
// app/api/stripe/webhooks/route.ts
export async function POST(request: Request) {
  const event = stripe.webhooks.constructEvent(body, sig, webhookSecret)

  // Only handle deauthorization
  if (event.type === 'account.application.deauthorized') {
    const accountId = event.account
    await db.update(appsTable)
      .set({ stripe_account_id: null, stripe_connected: false })
      .where(eq(appsTable.stripe_account_id, accountId))
  }

  return new Response('OK', { status: 200 })
}
```

## Environment Variables

```bash
STRIPE_SECRET_KEY=sk_live_xxx           # Platform secret key (for Connect API)
STRIPE_CONNECT_CLIENT_ID=ca_xxx         # From Connect settings
STRIPE_WEBHOOK_SECRET=whsec_xxx         # For deauth webhook only
```

## Database Schema

```typescript
export const appsTable = pgTable('apps', {
  id: text('id').primaryKey(),
  slug: text('slug').unique().notNull(),
  name: text('name').notNull(),
  stripe_account_id: text('stripe_account_id'),  // acct_xxx from OAuth
  stripe_connected: boolean('stripe_connected').default(false),
  // ...
})
```

## Known Connected Accounts

| App | Account ID | Connected |
|-----|------------|-----------|
| Total TypeScript | `acct_1LFP5yAozSgJZBRP` | ✓ |

## OAuth Error Reference

| Error | Meaning |
|-------|---------|
| `access_denied` | User denied authorization |
| `invalid_grant` | Code expired/used/invalid |
| `invalid_redirect_uri` | Redirect URI not whitelisted |

## File Locations

| File | Purpose |
|------|---------|
| `apps/web/app/api/stripe/connect/authorize/` | Start OAuth flow |
| `apps/web/app/api/stripe/connect/callback/` | Handle OAuth callback |
| `apps/web/app/api/stripe/webhooks/` | Deauth webhook only |
| `packages/core/src/tools/lookup-stripe.ts` | Query tools (future) |

## Reference

- PRD: `docs/support-app-prd/07-stripe-connect.md`
- Stripe Connect OAuth: https://docs.stripe.com/connect/oauth-reference
