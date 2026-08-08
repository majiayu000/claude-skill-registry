---
name: software-payments
description: Production-grade payment integration for Stripe, Paddle, Adyen, and more. Use when implementing checkout, subscriptions, webhooks, or billing.
---

# Payments & Billing Engineering

Use this skill to design, implement, and debug production payment integrations: checkout flows, subscription management, webhook handling, regional pricing, feature gating, one-time purchases, billing portals, and payment testing.

Defaults bias toward: Stripe as primary processor (most common), webhooks as source of truth, idempotent handlers, lazy-initialized clients, dynamic payment methods, Zod validation at boundaries, structured logging, and fire-and-forget for non-critical tracking. For complex billing, consider a billing orchestrator (Chargebee, Recurly, Lago) on top of Stripe/Adyen.

---

## Quick Reference

| Task | Default Picks | Notes |
|------|---------------|-------|
| Subscription billing | Stripe Checkout (hosted) | Omit `payment_method_types` for dynamic methods |
| MoR / tax compliance | Stripe Managed Payments / Paddle / LemonSqueezy | MoR handles VAT/sales tax for you |
| Mobile subscriptions | RevenueCat | Wraps App Store + Google Play |
| Enterprise / high-volume | Adyen | 250+ payment methods, interchange++ pricing |
| Complex billing logic | Chargebee / Recurly on top of Stripe | Per-seat + usage, contract billing, revenue recognition |
| Usage-based billing | Stripe Billing Meters or Lago (open-source) | API calls, AI tokens, compute metering |
| UK Direct Debit | GoCardless | Bacs/SEPA/ACH DD, lowest involuntary churn |
| EU multi-method | Mollie | iDEAL, Bancontact, SEPA DD, Klarna — 25+ methods |
| Online + POS | Square | Unified commerce: online payments + in-person readers |
| Bank-to-bank (A2A) | Open Banking (TrueLayer / Yapily) | Zero card fees, instant settlement, no chargebacks |
| Webhook handling | Verify signature + idempotent handlers | Stripe retries for 3 days |
| Feature gating | Tier hierarchy + feature matrix | Check at API boundary |
| One-time purchases | Stripe Checkout `mode: 'payment'` | Alongside subscriptions |
| Billing portal | Stripe Customer Portal | Self-service management |
| Regional pricing | PPP-adjusted prices per country | Use `x-vercel-ip-country` or GeoIP |
| PayPal button | Stripe PayPal method or PayPal Commerce Platform | Avoid Braintree — deprecated 2026, EOL Jan 2027 |
| BNPL (e-commerce) | Klarna (via Stripe/Mollie/direct) | Split payments; UK regulation expected 2026-27 |
| Testing | Stripe CLI + test cards | `4242 4242 4242 4242` |

## Scope

Use this skill to:

- Implement checkout flows (hosted, embedded, custom)
- Build subscription lifecycle management (create, upgrade, downgrade, cancel)
- Handle webhooks reliably (signature verification, idempotency, error handling)
- Set up regional/multi-currency pricing (PPP, emerging markets)
- Build feature gating and entitlement systems
- Implement one-time purchases alongside subscriptions
- Create billing portal integrations
- Test payment flows end-to-end
- Debug common payment integration issues

## When NOT to Use This Skill

Use a different skill when:

- **General backend patterns** -> See [software-backend](../software-backend/SKILL.md)
- **API design only (no payments)** -> See [dev-api-design](../dev-api-design/SKILL.md)
- **Conversion optimization** -> See [marketing-cro](../marketing-cro/SKILL.md)
- **Business model / pricing strategy** -> See [startup-business-models](../startup-business-models/SKILL.md)
- **Security audits** -> See [software-security-appsec](../software-security-appsec/SKILL.md)

---

## Decision Tree: Payment Platform Selection

Three platform layers (can be combined):

| Layer | Role | Examples |
|-------|------|----------|
| **Payment Processor** | Moves money, payment methods, fraud | Stripe, Adyen, Mollie, Square |
| **Merchant of Record (MoR)** | Handles tax, legal, disputes for you | Paddle, LemonSqueezy, Stripe Managed Payments |
| **Billing Orchestrator** | Subscription logic, dunning, revenue recognition | Chargebee, Recurly, Lago (open-source) |
| **Direct Debit** | Bank-account recurring pulls | GoCardless (Bacs, SEPA, ACH) |
| **Open Banking (A2A)** | Bank-to-bank instant payments | TrueLayer, Yapily |

```text
Payment integration needs: [Business Model]

  STEP 1: Choose your processor
    - Default / most common -> Stripe
    - Enterprise, >$1M/yr, 250+ payment methods -> Adyen
    - EU-focused, need iDEAL/Bancontact/SEPA -> Mollie
    - Need PayPal button -> Stripe (PayPal method) or PayPal Commerce Platform
    - WARNING: Do NOT start new projects on Braintree (deprecated 2026, EOL Jan 2027)

  STEP 2: Do you need a MoR?
    - Handle own tax + compliance -> Skip MoR, use processor directly
    - Want tax/VAT/disputes handled -> Stripe Managed Payments, Paddle, LemonSqueezy
    - Indie / small SaaS -> LemonSqueezy (simplest MoR)
    - EU-heavy customer base -> Paddle (strongest EU VAT handling)

  STEP 3: Is billing logic complex?
    - Simple tiers (free/pro/enterprise) -> Stripe Billing is sufficient
    - Per-seat + usage, contract billing, rev-rec -> Chargebee or Recurly on top of Stripe
    - Usage-based (API calls, AI tokens) -> Stripe Billing Meters or Lago (open-source)
    - B2C subscriptions, churn focus -> Recurly (strong revenue recovery)

  STEP 4: Platform-specific needs
    - Mobile app (iOS/Android) -> RevenueCat (wraps both stores)
    - Hybrid (web + app) -> RevenueCat + Stripe (share customer IDs)
    - Marketplace / multi-party -> Stripe Connect
    - UK Direct Debit recurring -> GoCardless (Bacs DD, lowest involuntary churn)
    - Multi-method EU checkout -> Mollie (25+ methods, single integration)
    - Online + in-person POS -> Square (unified commerce)
    - High-value A2A / zero card fees -> Open Banking (TrueLayer)
    - BNPL for e-commerce -> Klarna (via Stripe, Mollie, or direct)
    - One-time digital goods -> Stripe Checkout (payment mode)
    - Physical goods -> Stripe + shipping integration
    - Emerging markets / PPP -> Multiple Stripe Price objects per region
    - Multi-currency -> Stripe multi-currency or Paddle (auto-converts)
    - B2B invoicing -> Stripe Invoicing
```

For detailed platform comparison tables, see [references/platform-comparison.md](references/platform-comparison.md).
For UK/EU-specific platforms (GoCardless, Mollie, Square, Klarna, Open Banking), see [references/uk-eu-payments-guide.md](references/uk-eu-payments-guide.md).

---

## Stripe Integration Patterns (Feb 2026)

### 1. Client Initialization

**CRITICAL: Lazy-initialize the Stripe client.** Import-time initialization fails during build/SSR when env vars aren't available.

```typescript
// CORRECT: Lazy initialization with proxy for backwards compatibility
import Stripe from 'stripe';

let _stripe: Stripe | null = null;

export function getStripeServer(): Stripe {
  if (!_stripe) {
    const secretKey = process.env.STRIPE_SECRET_KEY;
    if (!secretKey) {
      throw new Error('STRIPE_SECRET_KEY is not configured');
    }
    _stripe = new Stripe(secretKey, {
      apiVersion: '2026-01-28.clover', // Pin to specific version
      typescript: true,
    });
  }
  return _stripe;
}

// Proxy for convenience (backwards-compatible named export)
export const stripe = {
  get customers() { return getStripeServer().customers; },
  get subscriptions() { return getStripeServer().subscriptions; },
  get checkout() { return getStripeServer().checkout; },
  get billingPortal() { return getStripeServer().billingPortal; },
  get webhooks() { return getStripeServer().webhooks; },
};
```

```typescript
// WRONG: Crashes during build when STRIPE_SECRET_KEY is undefined
import Stripe from 'stripe';
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!); // Build failure
```

### 2. Checkout Session Creation

**CRITICAL: Do NOT set `payment_method_types`.** Omitting it enables Stripe's dynamic payment method selection (Apple Pay, Google Pay, Link, bank transfers, local methods) based on customer region and device.

```typescript
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: 'subscription',
  // DO NOT set payment_method_types — let Stripe auto-select
  line_items: [{ price: priceId, quantity: 1 }],
  subscription_data: {
    trial_period_days: 7,
    metadata: {
      user_id: userId,
      billing_interval: interval,
    },
  },
  success_url: `${appUrl}/dashboard?checkout=success&tier=${tier}`,
  cancel_url: `${appUrl}/dashboard?checkout=canceled`,
  allow_promotion_codes: true,
  billing_address_collection: 'auto',
  metadata: {
    user_id: userId,
    tier,
    billing_interval: interval,
  },
});
```

```typescript
// WRONG: Limits to cards only, blocks Apple Pay, Google Pay, Link, etc.
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'], // REMOVE THIS
  // ...
});
```

### 3. Webhook Handler Architecture

**Webhooks are the source of truth for subscription state.** Never trust client-side callbacks alone.

Pattern: read raw body as text → verify `stripe.webhooks.constructEvent(body, signature, secret)` → `switch(event.type)` → return `{ received: true }` on success or 500 on handler error (so Stripe retries). Full route implementation in [references/stripe-patterns.md](references/stripe-patterns.md).

#### Essential Webhook Events

| Event | When | Handler Pattern |
|-------|------|-----------------|
| `checkout.session.completed` | Checkout finishes | Link Stripe customer to user, create subscription record |
| `checkout.session.expired` | Abandoned checkout | Fire-and-forget analytics (never fail the response) |
| `customer.subscription.created` | New subscription | Upsert subscription record with tier, status, period |
| `customer.subscription.updated` | Plan change, renewal, cancel-at-period-end | Update tier, status, cancel flags |
| `customer.subscription.deleted` | Subscription ends | Reset to free tier |
| `invoice.payment_succeeded` | Successful charge | Update period dates, process referral rewards |
| `invoice.payment_failed` | Failed charge | Set status to `past_due` |
| `customer.subscription.trial_will_end` | 3 days before trial ends | Trigger retention email |

#### Fire-and-Forget Pattern for Non-Critical Tracking

For `checkout.session.expired` (and similar analytics events): call tracking without `await`, never `throw`. Non-critical tracking must not cause a webhook 500.

### 4. Subscription Tier Model

```typescript
// Type definitions
export type SubscriptionTier = 'free' | 'starter' | 'pro' | 'enterprise';
export type SubscriptionStatus = 'active' | 'trialing' | 'canceled' | 'past_due' | 'incomplete';
export type BillingInterval = 'month' | 'year';

// Tier hierarchy for comparison
export const TIER_HIERARCHY: Record<SubscriptionTier, number> = {
  free: 0,
  starter: 1,
  pro: 2,
  enterprise: 3,
};

// Feature access matrix
export type Feature = 'basic_dashboard' | 'advanced_reports' | 'api_access' | 'priority_support';

const TIER_FEATURES: Record<SubscriptionTier, Feature[]> = {
  free: ['basic_dashboard'],
  starter: ['basic_dashboard', 'advanced_reports'],
  pro: ['basic_dashboard', 'advanced_reports', 'api_access'],
  enterprise: ['basic_dashboard', 'advanced_reports', 'api_access', 'priority_support'],
};

export function hasFeatureAccess(tier: SubscriptionTier, feature: Feature): boolean {
  return TIER_FEATURES[tier].includes(feature);
}

export function isTierUpgrade(current: SubscriptionTier, target: SubscriptionTier): boolean {
  return (TIER_HIERARCHY[target] ?? 0) > (TIER_HIERARCHY[current] ?? 0);
}
```

### 5. Upgrade/Downgrade Flow

Use `stripe.subscriptions.update()` with `proration_behavior: 'create_prorations'` and the new `price` on the existing item. Update local DB immediately; webhook will confirm. See full lifecycle in [references/subscription-lifecycle.md](references/subscription-lifecycle.md).

### 6. Regional / PPP Pricing

Create separate Stripe Price objects per region (standard vs emerging). Use `x-vercel-ip-country` or GeoIP for detection. Full implementation and market list in [references/regional-pricing-guide.md](references/regional-pricing-guide.md).

### 7. One-Time Purchases Alongside Subscriptions

```typescript
// Some products are one-time (e.g., PDF reports, credits)
// but subscribers get unlimited access
export function hasUnlimitedProductAccess(
  tier: SubscriptionTier,
  status: SubscriptionStatus,
  product: OneTimeProduct
): boolean {
  const isActive = status === 'active' || status === 'trialing';
  if (!isActive) return false;
  const productConfig = ONE_TIME_PRODUCTS[product];
  if (!productConfig.unlimitedFeature) return false;
  return hasFeatureAccess(tier, productConfig.unlimitedFeature);
}
```

### 8. Billing Portal

Use `stripe.billingPortal.sessions.create()` to redirect customers to Stripe's self-service portal for plan changes, payment method updates, and cancellation. See [references/stripe-patterns.md](references/stripe-patterns.md) for portal configuration checklist.

### 9. Referral/Coupon Integration

Key constraint: `allow_promotion_codes` and `discounts` are mutually exclusive in Stripe Checkout. If a referral coupon applies, set `discounts: [{ coupon: REFERRAL_COUPON_ID }]` and omit `allow_promotion_codes`. On `invoice.payment_succeeded` with `billing_reason === 'subscription_create'`, reward the referrer via `stripe.customers.createBalanceTransaction()`.

---

## Feature Gating Patterns

Every paid feature requires enforcement at 3 layers: **Feature Registry** (maps features to tiers), **API Enforcement** (returns 403), **UI Paywall** (shows upgrade CTA). Missing any layer creates a security hole or broken UX.

Key anti-patterns:
- **Gate on Wrong Key**: If the feature key is in the free tier, the gate is a permanent no-op.
- **Polymorphic Field Shapes**: `transits: Transit[] | { __gated: true }` crashes `(data.transits || []).sort()`. Use consistent shapes with an explicit `transitsGated: boolean` flag.
- **Checkout Mutual Exclusivity**: `allow_promotion_codes` + `discounts` together = Stripe rejects.

**Always verify Stripe SDK TypeScript types** (`node_modules/stripe/types/`), not documentation examples.

For detailed gating architecture (consumables, fraud prevention, discriminated unions), see [references/feature-gating-patterns.md](references/feature-gating-patterns.md).

---

## Stripe API Version Notes

Current version: `2026-01-28.clover`. Key breaking change: `invoice.subscription` replaced by `invoice.parent.subscription_details` since `2025-11-17.clover`. Full version table and migration code in [references/stripe-patterns.md](references/stripe-patterns.md).

---

## Common Mistakes and Anti-Patterns

| FAIL Avoid | PASS Instead | Why |
|------------|--------------|-----|
| `payment_method_types: ['card']` | Omit the field entirely | Blocks Apple Pay, Google Pay, Link, local methods |
| Trusting client-side checkout callback | Use webhooks as source of truth | Client can close browser before callback |
| `new Stripe(key)` at module top level | Lazy-initialize in a function | Build fails when env var is undefined |
| Catching webhook errors silently | Log + return 500 so Stripe retries | Lost events = lost revenue |
| Storing subscription state only client-side | Sync from webhook to DB | Single source of truth |
| Hardcoding prices in code | Use Stripe Price objects via env vars | Prices change, regional variants |
| Skipping webhook signature verification | Always verify with `constructEvent()` | Prevents replay/spoofing attacks |
| Using `invoice.subscription` (2025+) | Use `invoice.parent.subscription_details` | Breaking change since 2025-11-17.clover |
| `await` on fire-and-forget analytics | Don't await, don't throw | Non-critical tracking must not fail webhooks |
| Missing UUID validation on `user_id` from metadata | Validate with regex before DB operations | Prevents injection and corrupt data |
| Creating checkout without checking existing subscription | Check and use upgrade flow if active | Prevents duplicate subscriptions |
| Using `--no-verify` for Stripe webhook testing | Use Stripe CLI: `stripe listen --forward-to` | Real signature verification in dev |

---

## E2E Testing Patterns

Quick reference — full patterns in [references/testing-patterns.md](references/testing-patterns.md).

```bash
# Stripe CLI: forward events to local webhook endpoint
stripe listen --forward-to localhost:3001/api/stripe/webhook

# Trigger specific events
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
```

| Card | Scenario |
|------|----------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 0002` | Declined |
| `4000 0000 0000 3220` | 3D Secure required |
| `4000 0000 0000 9995` | Insufficient funds |

---

## Checkout Contract Propagation

When checkout API response contracts change, treat it as a cross-surface migration. Enumerate all entrypoints, update every caller, route blocked flows to one shared recovery UX. Full checklist in [references/in-app-browser-checkout-contract.md](references/in-app-browser-checkout-contract.md) and [assets/template-checkout-entrypoint-propagation-checklist.md](assets/template-checkout-entrypoint-propagation-checklist.md).

## Security Checklist

10-point checklist covering webhook signature verification, secrets management, UUID validation, HTTPS, idempotency, and rate limiting. Full checklist in [references/stripe-patterns.md](references/stripe-patterns.md).

---

## Navigation

**References**
- [references/stripe-patterns.md](references/stripe-patterns.md) - Stripe patterns: webhook handlers, idempotency, status mapping, error handling, dunning, usage-based billing, security checklist, API version notes
- [references/platform-comparison.md](references/platform-comparison.md) - Platform comparison: Stripe, Adyen, Paddle, LemonSqueezy, Chargebee, Recurly, Lago, Braintree (deprecated)
- [references/uk-eu-payments-guide.md](references/uk-eu-payments-guide.md) - UK/EU platforms: GoCardless, Mollie, Square, PayPal Commerce, Klarna, Open Banking (TrueLayer, Yapily)
- [references/testing-patterns.md](references/testing-patterns.md) - E2E testing: Stripe CLI, Playwright checkout, test cards, state sync
- [references/subscription-lifecycle.md](references/subscription-lifecycle.md) - Full subscription state machine, trials, upgrades/downgrades, cancellation, dunning, pause/resume, database schema
- [references/regional-pricing-guide.md](references/regional-pricing-guide.md) - PPP implementation, multi-currency Stripe prices, tax by region, fraud prevention, A/B testing pricing
- [references/webhook-reliability-patterns.md](references/webhook-reliability-patterns.md) - Idempotency, retry handling, dead letter queues, monitoring, event ordering, queue-based processing
- [references/feature-gating-patterns.md](references/feature-gating-patterns.md) - Feature gating: consumable vs binary unlocks, spread-then-override filtering, fraud prevention, discriminated union typed responses
- [references/in-app-browser-checkout-contract.md](references/in-app-browser-checkout-contract.md) - Checkout response contract propagation for in-app browser recovery and cross-surface consistency
- [references/ops-runbook-checkout-errors.md](references/ops-runbook-checkout-errors.md) - Checkout 500 debugging: RLS denials, auth policy, incident loop
- [data/sources.json](data/sources.json) - External documentation links (69 sources)

**Templates**
- [assets/template-checkout-entrypoint-propagation-checklist.md](assets/template-checkout-entrypoint-propagation-checklist.md) - Migration checklist for contract changes across all checkout callers

**Related Skills**
- [../software-backend/SKILL.md](../software-backend/SKILL.md) - Backend API patterns, database, auth
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) - API design patterns
- [../marketing-cro/SKILL.md](../marketing-cro/SKILL.md) - Conversion optimization for checkout
- [../startup-business-models/SKILL.md](../startup-business-models/SKILL.md) - Pricing strategy
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) - Payment security
- [../qa-testing-playwright/SKILL.md](../qa-testing-playwright/SKILL.md) - E2E testing patterns

---

## Freshness Protocol

When users ask version-sensitive questions about payment platforms, do a freshness check.

### Trigger Conditions

- "What's the best payment platform for [use case]?"
- "Stripe vs Paddle vs LemonSqueezy?"
- "How do I handle [tax/VAT/sales tax]?"
- "What's new in Stripe [API/Billing/Checkout]?"
- "Is Stripe Managed Payments available?"
- "Best mobile subscription SDK?"

### How to Freshness-Check

1. Start from `data/sources.json` (official docs, changelogs, API versions).
2. Run a targeted web search for the specific platform and feature.
3. Prefer official documentation and changelogs over blog posts.

### What to Report

- **Current landscape**: what is stable and widely used now
- **Emerging trends**: Managed Payments, usage-based billing, entitlements API, Open Banking
- **Deprecated/declining**: hardcoded payment_method_types, top-level invoice.subscription, Braintree
- **Recommendation**: default choice + alternatives with trade-offs

## Ops Runbook

For checkout 500 errors with RLS/authorization denials: 5-step incident loop, required logging fields, and guardrails. See [references/ops-runbook-checkout-errors.md](references/ops-runbook-checkout-errors.md).


## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
