---
name: business-model-preferences
description: |
  Pricing philosophy and business model constraints.
  Auto-invoke when: evaluating pricing, checkout flows, subscription logic, tier structures.
user-invocable: false
---

# Business Model Preferences

These are organizational preferences. Apply them when designing or reviewing any billing integration.

## Philosophy

Keep it simple. Complexity in pricing confuses customers and creates engineering debt.

## Pricing Model

**Single tier or nothing.** Either:
- Free and open source (no billing)
- One price point with full access

No multiple tiers. No Basic/Pro/Enterprise. No feature gating. No usage-based pricing.

If annual pricing exists, it's simply "2 months free" — same features, discounted rate.

## Free Trial, Not Free Tier

Offer a trial (14 days standard). After trial: pay or lose access.

No freemium. No "free forever with limits." Trial is the only free path.

## Trial Completion on Upgrade

When a user upgrades mid-trial, honor the remaining trial days.

Pass `trial_end` to Stripe with the remaining time. User finishes their trial, THEN billing starts. Never charge immediately on mid-trial upgrade — that's confusing and feels like a bait-and-switch.

## Simplicity Tests

When reviewing pricing or checkout:
- Can you explain the pricing in one sentence?
- Is there only one "upgrade" button?
- Does the pricing page have comparison tables? (It shouldn't.)
- Would upgrading mid-trial surprise a user with an immediate charge? (It shouldn't.)

## Application

Reference these preferences when:
- Designing new Stripe integrations
- Reviewing checkout flows
- Auditing subscription logic
- Evaluating pricing page designs
