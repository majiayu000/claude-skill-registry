# treido-payments — Stripe Payments Skill

> **Scope:** Stripe integration, checkout flows, webhooks, subscriptions, Connect payouts, fee model  
> **Triggers:** `stripe`, `payment`, `checkout`, `subscription`, `billing`, `webhook`, `price`, `customer`, `invoice`, `refund`, `payout`, `connect`, `transfer`, `card`, `payment method`, `payment intent`, `checkout session`, `customer portal`, `boost`, `fee`, `buyer protection`

---

## NOT For (Delegate To)

| Topic | Delegate To |
|-------|-------------|
| UI components, styling, Tailwind | `treido-design` |
| Routing, caching, Server Components | `treido-frontend` |
| Database schema, RLS, migrations | `treido-backend` |
| i18n, translations | `treido-rails` |

---

## ⚠️ PAUSE CONDITIONS

**STOP and request approval before:**

| Operation | Risk | Why |
|-----------|------|-----|
| New payment flow | Money flows change | New checkout types affect revenue |
| Fee structure changes | Platform revenue | Buyer/seller fee adjustments |
| Webhook endpoint changes (prod) | Order/subscription failures | Missing events = lost data |
| Connect payout changes | Seller funds | Affects seller earnings |
| Subscription tier changes | Billing | Affects recurring revenue |
| Refund automation | Revenue loss | Manual review preferred |

---

## Core Principles

| ID | Rule | Rationale |
|----|------|-----------|
| `pay-server-only` | All Stripe API calls server-side only | Secret key exposure = account compromise |
| `pay-webhook-verify` | Verify webhook signatures with rotation support | Prevents spoofed events |
| `pay-idempotent` | Idempotency via `stripe_*_id` columns | Prevents duplicate orders/subscriptions |
| `pay-metadata` | Store reconstruction data in session metadata | Webhook has all info to create records |
| `pay-admin-client` | Use `createAdminClient()` in webhooks | Service role bypasses RLS |
| `checkout-session` | Use Stripe hosted Checkout, not custom forms | PCI compliance, less code |
| `connect-destination` | Destination charges with `application_fee_amount` | Platform takes fee, seller gets rest |

---

## ❌ CRITICAL: Forbidden Patterns

| Pattern | Risk | Fix |
|---------|------|-----|
| `STRIPE_SECRET_KEY` in client code | Account takeover | Server actions/API routes only |
| Webhook without signature verification | Spoofed events | Always verify with `constructEvent()` |
| Hardcoded price amounts | Price drift | Use Price IDs or database |
| Direct Stripe API from `"use client"` | Key exposure | Server actions with redirect |
| Single webhook secret (no rotation) | Downtime on rotation | Support comma-separated secrets |
| Missing `stripe_*_id` unique constraint | Duplicate records | Add DB constraint |
| `createClient()` in webhooks | RLS blocks inserts | Use `createAdminClient()` |

---

## Quick Reference: Checkout Flows

| Flow | Action/Route | Mode | Webhook |
|------|--------------|------|---------|
| Product purchase | `createCheckoutSession()` | `payment` | `/api/checkout/webhook` |
| Subscription | `createSubscriptionCheckoutSession()` | `subscription` | `/api/subscriptions/webhook` |
| Listing boost | `POST /api/boost/checkout` | `payment` | `/api/payments/webhook` |
| Save card | `createPaymentMethodSetupSession()` | `setup` | `/api/payments/webhook` |
| Connect onboarding | `POST /api/connect/onboarding` | — | `/api/connect/webhook` |

→ Details: [references/checkout.md](references/checkout.md)

---

## Quick Reference: Webhook Endpoints

| Endpoint | Events | Purpose |
|----------|--------|---------|
| `/api/checkout/webhook` | `checkout.session.completed`, `payment_intent.*` | Order creation |
| `/api/payments/webhook` | `checkout.session.completed` (boost/setup), `payment_method.detached` | Boosts, saved cards |
| `/api/subscriptions/webhook` | `checkout.session.completed`, `customer.subscription.*`, `invoice.*` | Subscription lifecycle |
| `/api/connect/webhook` | `account.updated`, `account.application.deauthorized` | Seller payout status |

→ Details: [references/webhooks.md](references/webhooks.md)

---

## Quick Reference: Supabase Client Selection

| Context | Client | Why |
|---------|--------|-----|
| Server Actions | `createClient()` | User session, RLS applies |
| API Routes | `createRouteHandlerClient(req)` | Request cookies |
| Webhooks | `createAdminClient()` | Service role, bypasses RLS |

---

## Fee Model (Vinted-style Hybrid)

| Fee | Payer | Calculation |
|-----|-------|-------------|
| Seller fee | Seller (deducted) | 0% personal, small % business |
| Buyer protection | Buyer (added) | 3-4% + fixed, capped |
| Platform revenue | — | `sellerFee + buyerProtectionFee` |

→ Implementation: [lib/stripe-connect.ts](../../lib/stripe-connect.ts) → `calculateTransactionFees()`

---

## Environment Variables

| Variable | Scope | Purpose |
|----------|-------|---------|
| `STRIPE_SECRET_KEY` | Server | API authentication |
| `STRIPE_WEBHOOK_SECRET` | Server | Checkout + payments webhooks (rotation supported) |
| `STRIPE_SUBSCRIPTION_WEBHOOK_SECRET` | Server | Subscription webhook |
| `STRIPE_CONNECT_WEBHOOK_SECRET` | Server | Connect webhook |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client | Not currently used (hosted checkout) |

**Secret rotation:** Comma or newline-separated values in `STRIPE_WEBHOOK_SECRET`

---

## Subscription Management

| Action | Implementation |
|--------|----------------|
| Create subscription | `createSubscriptionCheckoutSession()` → Stripe hosted |
| Manage billing | `createBillingPortalSession()` → Stripe portal |
| Cancel (end of period) | `cancelSubscription()` → sets `cancel_at_period_end` |
| Reactivate | `reactivateSubscription()` → clears cancel flag |
| Downgrade | `downgradeToFreeTier()` → immediate via portal |

→ Details: [references/subscriptions.md](references/subscriptions.md)

---

## Connect Payouts

| Status | Meaning | Action |
|--------|---------|--------|
| `not_started` | No account | Show onboarding CTA |
| `pending` | Incomplete onboarding | Show "Complete setup" |
| `enabled` | Ready for payouts | Destination charges work |
| `disabled` | Account issue | Show dashboard link |

→ Details: [references/connect.md](references/connect.md)

---

## Key Files

| Category | Files |
|----------|-------|
| Stripe instance | [lib/stripe.ts](../../lib/stripe.ts) |
| Connect utilities | [lib/stripe-connect.ts](../../lib/stripe-connect.ts) |
| Locale URLs | [lib/stripe-locale.ts](../../lib/stripe-locale.ts) |
| Env helpers | [lib/env.ts](../../lib/env.ts) |
| Checkout actions | [app/[locale]/(checkout)/_actions/checkout.ts](../../app/[locale]/(checkout)/_actions/checkout.ts) |
| Subscription actions | [app/actions/subscriptions.ts](../../app/actions/subscriptions.ts) |
| Payment actions | [app/actions/payments.ts](../../app/actions/payments.ts) |

---

## Review Checklist

Before shipping payment changes:

- [ ] All Stripe API calls are server-side only
- [ ] Webhook signature verified with rotation support
- [ ] Idempotency via `stripe_*_id` unique constraints
- [ ] Metadata contains all data for record creation
- [ ] Using `createAdminClient()` in webhooks
- [ ] Success/cancel URLs use locale-safe builders
- [ ] Price IDs from env vars or database (not hardcoded)
- [ ] Fee calculation tested for edge cases
- [ ] Error states handled gracefully
- [ ] Webhook events logged for debugging

---

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_supabase_execute_sql` | Query payment/subscription tables |
| `mcp_supabase_list_tables` | Check payment schema |
| Stripe Dashboard | View payments, subscriptions, webhooks |

---

## References (Progressive Disclosure)

| Doc | Topics |
|-----|--------|
| [references/checkout.md](references/checkout.md) | Sessions, fees, metadata, Connect charges |
| [references/webhooks.md](references/webhooks.md) | Event handling, idempotency, signature verification |
| [references/subscriptions.md](references/subscriptions.md) | Billing portal, plans, lifecycle |
| [references/connect.md](references/connect.md) | Marketplace payouts, Express accounts |
| [references/security.md](references/security.md) | API keys, secrets, PCI, Connect security |

---

## SSOT Documents

| Topic | Location |
|-------|----------|
| Payment spec | [docs/08-PAYMENTS.md](../../docs/08-PAYMENTS.md) |
| Fee model | [lib/stripe-connect.ts](../../lib/stripe-connect.ts) |
| Webhook handlers | `app/api/*/webhook/route.ts` |

---

## Handoffs

| When | Agent |
|------|-------|
| Checkout UI components | → `treido-design` |
| Route protection, caching | → `treido-frontend` |
| Payment tables, RLS | → `treido-backend` |
| Price/plan copy | → `treido-rails` (i18n) |
