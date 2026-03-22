---
name: tech-debt
description: Systematic tech debt inventory with cost model. Each item gets weekly cost, incident risk, blast radius, and fix effort. Forces cost/benefit decisions instead of vague guilt. Tags Disasters waiting to happen.
user-invocable: true
argument-hint: "[codebase, directory, or specific area]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Tech debt is not a feeling. It's a measurable cost.
- "This code is messy" is not a finding. "This code costs 3 hours/week and will cause an outage within 6 months" is.
- The most expensive debt is the debt you don't know you're paying.
- Some debt is cheap to carry. The inventory tells you which.

## Domain-specific examples

**Debt item — wrong way:**

"The payment service could use some refactoring. The code is a bit messy and hard to follow. We should clean it up when we have time."

**Debt item — right way:**

"**Payment service god class** `Disaster waiting to happen`
- **Location:** `app/services/payment_service.rb` (847 lines)
- **Weekly cost:** ~4 hours. 3 developers touch this file weekly. Average of 80 minutes per person navigating the class, understanding side effects, and resolving merge conflicts (this file has had 14 merge conflicts in the last quarter).
- **Incident risk:** High. The `charge_customer` method (line 234-298) has no test coverage for the concurrent charge path. Race condition: two requests can double-debit. See incident #47.
- **Blast radius:** User-facing. Incorrect charges, refund manual work, customer trust damage.
- **Compounding:** Yes. Every new payment feature adds to this file. It was 400 lines 6 months ago.
- **Fix effort:** 3 days. Extract into `ChargeService`, `RefundService`, `SubscriptionService` with explicit interfaces. Add advisory lock for concurrent charges.
- **Fix risk:** Medium. Payment code. Needs integration tests against Stripe test mode before and after.
- **If you don't fix it:** ~200 hours/year in developer drag, plus a near-certain double-charge incident within 6 months."

## Debt sources to scan

Structural, data/schema, test, dependency, infrastructure, documentation, API debt.

## Per-item measurement

- **Weekly cost** (dev hours, with reasoning)
- **Incident risk** (High/Medium/Low + specific scenario)
- **Blast radius** (function → page → service → system → user data)
- **Compounding?** (getting worse as more code builds on it?)
- **Fix effort** (hours/days/weeks)
- **Fix risk** (could the refactor introduce bugs?)

## Output format

### Debt summary

| Total items | Disasters waiting | Weekly cost | Highest priority |
|---|---|---|---|

### Inventory (priority order)
Each item: location, what, weekly cost, incident risk, blast radius, compounding, fix effort, fix risk, recommended fix, cost of carrying.

### Cost/benefit
Top 5 by ROI (fix first). Bottom 5 by ROI (accept the debt).

### Devil's advocate
For your highest-priority items: could the team be right to defer? What context might justify carrying this?

### What I didn't check
