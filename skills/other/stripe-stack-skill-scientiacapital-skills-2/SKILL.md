---
name: "stripe-stack"
description: "Stripe integration patterns for Next.js + Supabase - payments, subscriptions, webhooks, credit systems, checkout. Use when: stripe, payments, billing, subscription, webhook, checkout, add payments to project."
---

<objective>
Guide Stripe payment integration for Next.js + Supabase projects with production-ready patterns for webhooks, subscriptions, and credit systems. Ensures idempotency, proper test/live mode separation, and secure key handling.
</objective>

<quick_start>
**Add payments to a Next.js + Supabase project:**

1. Install Stripe: `npm install stripe @stripe/stripe-js`
2. Add env vars (see quick_reference below)
3. Create idempotency table (see schema below)
4. Choose workflow: `setup-new-project.md` or `add-webhook-handler.md`

```typescript
// Lazy-loaded Stripe client
import Stripe from 'stripe';
let _stripe: Stripe | null = null;
export function getStripe(): Stripe {
  if (!_stripe) {
    _stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2025-12-15.clover' });
  }
  return _stripe;
}
```
</quick_start>

<success_criteria>
Integration is successful when:
- Webhook handler uses database-backed idempotency (not in-memory)
- All keys in environment variables (never hardcoded)
- Test mode fully working before any live mode deployment
- Signature verification on all webhook endpoints
- Event logging before processing (insert-before-process pattern)
- Go-live checklist completed before production deployment
</success_criteria>

<essential_principles>

## Core Principles

1. **Idempotency is Non-Negotiable**
   - ALL webhook handlers MUST use database-backed idempotency
   - Never use in-memory Sets (lost on serverless cold starts)
   - Insert event record BEFORE processing, not after

2. **Test/Live Mode Separation**
   - Use environment variables for ALL keys (never hardcode)
   - Test keys: `sk_test_`, `pk_test_`, `whsec_test_`
   - Live keys: `sk_live_`, `pk_live_`, `whsec_live_`
   - Products/prices must be recreated in live mode

3. **Shared Stripe Account**
   - All NetZero Suite projects share ONE Stripe account
   - Same webhook secret can be used across projects
   - Each project has its own webhook endpoint URL

4. **Lazy Client Initialization**
   - Never initialize Stripe at module level (build errors)
   - Use factory function pattern for server-side client
   - Check for API key before creating instance

</essential_principles>

<intake>

## What Are You Building?

Before proceeding, identify your use case:

| Use Case | Workflow | Description |
|----------|----------|-------------|
| **New project** | `setup-new-project.md` | Fresh Stripe integration from scratch |
| **Add webhooks** | `add-webhook-handler.md` | Add webhook handler to existing project |
| **Subscriptions** | `implement-subscriptions.md` | Recurring billing with plans |
| **Credit system** | `add-credit-system.md` | Pay-as-you-go credits |
| **Go live** | `go-live-checklist.md` | Test → Production migration |

</intake>

<routing>

## Workflow Routing

**If setting up Stripe in a new project:**
→ Read `workflows/setup-new-project.md`
→ Then read `reference/environment-vars.md`
→ Use `templates/stripe-client.ts` and `templates/env-example.txt`

**If adding webhook handling:**
→ Read `workflows/add-webhook-handler.md`
→ Then read `reference/webhook-patterns.md`
→ Use `templates/webhook-handler-nextjs.ts` and `templates/idempotency-migration.sql`

**If implementing subscription billing:**
→ Read `workflows/implement-subscriptions.md`
→ Then read `reference/pricing-models.md`
→ Use `templates/plans-config.ts`

**If adding credit/usage-based system:**
→ Read `workflows/add-credit-system.md`
→ Then read `reference/pricing-models.md`

**If migrating test → production:**
→ Read `workflows/go-live-checklist.md`

</routing>

<quick_reference>

## Quick Reference

### Environment Variables (Standard)

```bash
# Server-side (never expose to client)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Client-side (safe to expose)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Optional: Price IDs (for test→live switching)
STRIPE_PRICE_STARTER_MONTHLY=price_...
STRIPE_PRICE_PRO_MONTHLY=price_...
```

### Common Webhook Events

| Event | When It Fires | Action |
|-------|---------------|--------|
| `checkout.session.completed` | Customer completes checkout | Create subscription record |
| `customer.subscription.created` | New subscription starts | Initialize user limits |
| `customer.subscription.updated` | Plan change, renewal | Update plan/limits |
| `customer.subscription.deleted` | Cancellation | Downgrade to free |
| `invoice.paid` | Monthly renewal success | Reset usage counters |
| `invoice.payment_failed` | Payment failed | Mark as past_due |

### Stripe Client Pattern

```typescript
let _stripe: Stripe | null = null;

export function getStripe(): Stripe {
  if (!_stripe) {
    const key = process.env.STRIPE_SECRET_KEY;
    if (!key) throw new Error('STRIPE_SECRET_KEY not configured');
    _stripe = new Stripe(key, {
      apiVersion: '2025-12-15.clover',
      typescript: true
    });
  }
  return _stripe;
}
```

### Idempotency Table Schema

```sql
CREATE TABLE stripe_webhook_events (
  id TEXT PRIMARY KEY,           -- Use Stripe event ID directly
  type TEXT NOT NULL,            -- Event type
  data JSONB NOT NULL,           -- Full event payload
  processed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Webhook Handler Structure

```typescript
export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  // 1. Verify signature
  const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);

  // 2. Check idempotency (BEFORE processing)
  const { data: existing } = await supabase
    .from('stripe_webhook_events')
    .select('id')
    .eq('id', event.id)
    .single();

  if (existing) return NextResponse.json({ duplicate: true });

  // 3. Log event (INSERT before processing)
  await supabase.from('stripe_webhook_events').insert({
    id: event.id,
    type: event.type,
    data: event,
  });

  // 4. Process event
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckout(event.data.object);
      break;
    // ... other handlers
  }

  return NextResponse.json({ received: true });
}
```

</quick_reference>

<integration_notes>

## Integration Notes

### Works With
- **Supabase**: Use service role client for webhook handlers (bypasses RLS)
- **Prisma**: Alternative to Supabase for idempotency table
- **Vercel**: Add runtime/maxDuration config for webhook routes
- **Next.js App Router**: Use `request.text()` for raw body

### Related Skills
- `supabase-sql-skill` - For database migrations
- `create-hooks-skill` - For post-deployment notifications

### GitHub Repository
Private templates and examples available at:
`github.com/ScientiaCapital/stripe-stack`

</integration_notes>

<reference_index>

## Reference Files

| File | Purpose |
|------|---------|
| `reference/webhook-patterns.md` | Idempotency, event handling, error recovery |
| `reference/pricing-models.md` | Plans vs Credits vs Usage-based billing |
| `reference/environment-vars.md` | Standard env var conventions |
| `reference/common-errors.md` | Troubleshooting guide |

## Template Files

| File | Purpose |
|------|---------|
| `templates/webhook-handler-nextjs.ts` | Complete webhook route (copy-paste) |
| `templates/stripe-client.ts` | Lazy-loaded client factory |
| `templates/plans-config.ts` | Subscription plan definitions |
| `templates/idempotency-migration.sql` | Supabase migration |
| `templates/webhook-handler.test.ts` | Test template |
| `templates/env-example.txt` | Standard .env template |

## Workflow Files

| File | Purpose |
|------|---------|
| `workflows/setup-new-project.md` | Fresh Stripe integration |
| `workflows/add-webhook-handler.md` | Add webhook to existing project |
| `workflows/implement-subscriptions.md` | Subscription billing |
| `workflows/add-credit-system.md` | Pay-as-you-go credits |
| `workflows/go-live-checklist.md` | Test → Production migration |

</reference_index>
