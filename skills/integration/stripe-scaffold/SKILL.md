---
name: stripe-scaffold
description: |
  Generate Stripe integration code from a design document.
  Produces working code, not just templates.
---

# Stripe Scaffold

Generate the code for a Stripe integration.

## Branching

Assumes you start on `master`/`main`. Before generating code:

```bash
git checkout -b feat/stripe-integration-$(date +%Y%m%d)
```

## Objective

Turn a design document into working code. Delegate implementation to Codex aggressively — that's what it's for.

## Process

**1. Review the Design**

Read the design document from `stripe-design`. Understand:
- Checkout flow
- Webhook events
- State management approach
- Access control logic

**2. Research Current Implementation**

Before generating code:
- Use Gemini to find current Stripe SDK usage patterns
- Check the Stripe docs for your specific use case
- Look at how similar apps implement this

Code patterns change. Don't rely on cached knowledge.

**3. Delegate to Codex**

For each component, delegate to Codex with clear specs:

```bash
codex exec --full-auto "Implement Stripe webhook handler for [events]. \
Follow pattern in [reference]. Use Convex mutations for state updates. \
Verify signature first. Handle idempotency. \
Run pnpm typecheck after." \
--output-last-message /tmp/codex-webhook.md 2>/dev/null
```

Then: `git diff --stat && pnpm typecheck && pnpm test`

**4. Components to Generate**

Typical Next.js + Convex stack:

**Backend:**
- `src/lib/stripe.ts` — Stripe client initialization
- `src/app/api/stripe/checkout/route.ts` — Checkout session creation
- `src/app/api/stripe/webhook/route.ts` — Webhook receiver (signature verification)
- `convex/stripe.ts` — Webhook event processing
- `convex/subscriptions.ts` — Subscription state management
- `convex/billing.ts` — Billing queries and portal session creation
- `convex/schema.ts` updates — Subscription fields on users
- `.env.example` updates — Document required variables

**Subscription Management UX (Required):**
Reference `stripe-subscription-ux` for full requirements.

- `components/billing/SubscriptionCard.tsx` — Current plan overview
- `components/billing/BillingCycleInfo.tsx` — Next billing date, amount
- `components/billing/PaymentMethodDisplay.tsx` — Card on file
- `components/billing/BillingHistory.tsx` — Past invoices
- `components/billing/ManageSubscriptionButton.tsx` — Opens Stripe Portal
- `components/billing/TrialBanner.tsx` — Trial status/countdown
- Settings page section for subscription management

**This UX is non-negotiable.** No Stripe integration is complete without it.

**5. Don't Forget**

- Trial handling: pass `trial_end` when user upgrades mid-trial
- Access control: check subscription status before gated features
- Error handling: webhook should return 200 even on processing errors (to prevent Stripe retries)
- Signature verification: MUST be first thing in webhook handler

## Quality Gates

After generation:
- `pnpm typecheck` — No type errors
- `pnpm lint` — No lint errors
- `pnpm test` — Tests pass (if they exist)
- Manual review of generated code

## Adaptation

Default stack is Next.js + Convex. If different:
- Express/Fastify: Different route setup, same Stripe logic
- Supabase/Postgres: Different ORM, same state management concepts
- No Convex: Webhook processing happens in the API route directly

The Stripe parts are the same; the framework parts adapt.
