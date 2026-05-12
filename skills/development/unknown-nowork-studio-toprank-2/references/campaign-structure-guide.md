# Campaign Structure Guide — CBO, ABO, ASC, Funnel

How to organize a Meta Ads account in 2025–2026. The shape of the account matters less than the underlying signal density — but a chaotic structure costs you both signal density and the ability to reason about what's working.

## The Default Modern Structure

For most ecom and lead-gen accounts spending $1k–$50k/month:

```
Campaign — Prospecting (CBO)
├── Ad Set — Broad
│   └── 4–6 ad creatives (mix of video, static, formats)
├── Ad Set — LAL 1–3% Purchasers
│   └── 4–6 ad creatives
└── Ad Set — Custom audience seed (optional, if specific cohort matters)
    └── 4–6 ad creatives

Campaign — Retargeting (CBO or ABO)
├── Ad Set — Cart abandoners (last 14 days)
│   └── 3–5 retargeting-specific creatives
├── Ad Set — Site visitors no purchase (last 30 days)
│   └── 3–5 creatives
└── Ad Set — Engagers (FB + IG, last 90 days)
    └── 3–5 creatives

Campaign — Advantage+ Shopping (separate, runs parallel for ecom)
└── Single ad set (ASC manages internally)
    └── 8–15 creatives in one pool
```

Three campaigns. Most accounts have between two and five — anything more is usually structural debt, not strategy.

## CBO vs. ABO Decision

**Campaign Budget Optimization (CBO / Advantage Campaign Budget)** — budget is set at the campaign level. Meta distributes across ad sets in real time, optimizing for total events.

**Ad Set Budget Optimization (ABO)** — budget is set per ad set. The manager controls distribution.

| Use CBO when | Use ABO when |
|---|---|
| Prospecting at scale ($500+/day) | Running clean A/B audience tests |
| Multiple ad sets with similar objectives | Retargeting ad sets where you want guaranteed daily spend on each pool |
| You want Meta's bidding LLM to allocate dynamically | You're testing a brand-new audience that needs guaranteed spend to clear Learning |
| You don't care which ad set wins, only that the campaign wins | Each ad set has different unit economics and you need the per-ad-set ceiling |

The defaults Meta nudges you toward (CBO + Advantage+ Audience + Advantage+ Placements) win the median account. ABO + manual everything wins for a specific subset of cases — usually accounts where the user has strong signal that they'd lose money on a specific cohort if Meta's allocator chose it.

**Don't mix CBO and ABO in the same account without a reason.** Pick a default; treat exceptions as exceptions.

## When to Use Advantage+ Shopping (ASC)

ASC consolidates prospecting and retargeting into one campaign with broad targeting and an Existing-Customer Cap (default 15%). Meta treats it as a unit and optimizes across the whole funnel.

| ASC wins when | ASC loses when |
|---|---|
| Ecom with reliable Pixel + CAPI and Catalog | B2B / lead-gen (ASC is built for ecom) |
| Account spends > $5k/month | Account < $1k/month (not enough signal) |
| Brand has 8+ creative concepts ready to upload | Limited creative inventory |
| Existing campaigns are mostly broad anyway | Heavy reliance on narrow custom audiences |

For ecom accounts at scale, the standard recommendation is to run **ASC + a small manual control cell** (one prospecting campaign and one retargeting campaign). If ASC outperforms over a 30-day window, shift more budget to ASC and decommission manual prospecting. Keep retargeting separate if the brand has strong cart-abandoner / engager logic — ASC's existing-customer treatment is opaque.

## Anti-Patterns

### Too many campaigns

Five prospecting campaigns split by audience type, each with one ad set, is fragmentation, not segmentation. Each campaign has to clear its own learning bar; signal density is split; the bidding LLM can't see the full picture. Consolidate.

**Heuristic:** if a campaign has only one or two ad sets and < 20 events / week per ad set, it's probably part of a fragmentation problem. Look for opportunities to merge.

### Campaigns split by creative

"Video Campaign" and "Static Campaign" running on the same audience and objective is a structural mistake — Meta wants creative diversity within ad sets, not isolated by campaign. Consolidate creatives into one ad set per audience.

### Campaigns split by placement

"Reels Campaign" and "Feed Campaign" running on the same audience is similarly wrong. Use Advantage+ Placements (the default) and let Meta choose. Manual placement isolation is worth the cost only when you have a specific, evidence-based reason to exclude a placement.

### One ad set carrying the whole campaign

When one ad set is > 70% of campaign spend, the campaign is fragile. The ad set is probably an outlier the LLM has converged on; when it fatigues, the campaign collapses. Diversify by adding 1–2 sibling ad sets even at lower projected ROAS, to give the LLM a fallback. This is risk management, not optimization.

### Special Ad Category misconfigured

For Credit / Employment / Housing / Social Issues / Politics, the campaign must be marked as a Special Ad Category at creation. Running standard targeting on a covered vertical is policy violation — disapproval and account-level review risk. Always check vertical at audit time.

### Branded campaigns (rare on Meta)

On Search, brand campaigns are mandatory — competitors bid on your name. On Meta, brand-search behavior doesn't apply. Running a Meta campaign for "people searching for [Brand]" misunderstands the platform — Meta is discovery, not search. Don't.

## Naming Conventions

Consistency matters more than the exact convention. A workable default:

```
[Funnel Stage] - [Audience] - [Geo] - [Objective] - [vMonthYear]

Examples:
PROS - Broad - US - Sales - v0526
PROS - LAL 3% Purchasers - US - Sales - v0526
RT - Cart Abandon 14d - US - Sales - v0526
ASC - Sales - US - v0526
```

The version field at the end (`v0526` for May 2026) lets you tell at a glance how old the structure is and helps with QBR-style account history reviews. Avoid generic names like "Test 1" or "New Campaign" — they become permanent debt.

## Restructuring Checklist

When asked to "fix the campaign structure", run this checklist before recommending:

1. **Inventory** — list all active campaigns, ad sets, and ads with last-30-day spend and conversions. Order by spend desc.
2. **Identify the workhorses** — campaigns / ad sets accounting for > 80% of conversions. These are usually working; touch with caution.
3. **Identify the fragmentation** — campaigns spending < 5% of budget with < 20 events / week. These are candidates for consolidation or pause.
4. **Identify the anti-patterns** — overlap > 50% between ad sets, campaigns split by creative or placement, single-ad-set dependency.
5. **Propose the new shape** — show the user the *target* structure (campaigns / ad sets / ads), not just the deletions. Restructuring is migration, not pruning.
6. **Sequence the migration** — never restructure everything in one push. Migrate one campaign per week, monitor performance, accept the Learning Phase relearn cost as part of the budget.
