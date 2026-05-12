# Audience Strategy — Targeting, Lookalikes, Overlap

Meta's bidding LLM has gotten good enough that audience strategy has shifted meaningfully since 2022. This reference is the current best-practice playbook, not the 2018 narrow-stack-of-interests approach that's still all over older blog posts.

## The Default: Broad

For Sales / Conversions / Leads objectives at $100+/day with a healthy Pixel + CAPI:

- **Geo** — country level (US, or country grouping)
- **Age** — 18–65+
- **Gender** — All
- **Detailed targeting** — none
- **Custom audiences** — none for prospecting

Yes, really. This is Meta's published recommendation and it tends to outperform interest-stacked targeting for accounts above ~$3k/month. The reason: Meta's bidding LLM has access to hundreds of real-time signals (site behavior, in-platform behavior, device, time, content engaged with, look-back conversions). Pre-filtering with detailed targeting interests strips the LLM of signal density without adding precision the algorithm doesn't already have.

**Exceptions where narrow targeting still wins:**

| Situation | Why narrow targeting wins |
|---|---|
| New account, < $50/day, limited Pixel data | Broad with no signal density just spreads thinly. Lookalike from a small purchaser seed concentrates the signal. |
| Very specialized B2B (e.g. dental practice managers) | Detailed targeting on job titles is faster than waiting for Meta to find them via broad |
| Restricted vertical with policy concerns | Narrow targeting reduces the surface area for personal-attribute violations |
| Heavy local-service business (e.g. plumber in one zip) | Geo radius IS the targeting; broad demographic adds nothing |
| Small custom audience for retargeting | The audience definition is the targeting; no detailed layers |

## Lookalike Strategy

When lookalikes still make sense:

- **Seed quality matters more than seed size.** A 500-person seed of high-LTV customers outperforms a 50,000-person seed of all-time site visitors. Quality > quantity, every time.
- **Best seeds (in priority order):** purchasers (last 180 days) → high-LTV purchasers (top 25% AOV) → email subscribers who opened recently → site engagers who hit a key page → all site visitors.
- **Size:** 1–3% lookalike is the sweet spot for most accounts. 1% = highest similarity, smallest reach. 3–5% = broader, more reach, less similarity. Above 5%, the audience is essentially broad anyway.
- **Stacked lookalikes** (e.g. LAL 1–3% + LAL 1–5% in the same ad set) used to be a tactic — now it's just audience overlap. Don't.

When lookalikes don't make sense:

- Account already on broad with healthy ROAS — adding lookalike layers fragments signal.
- Account has < 100 conversions in the last 180 days — the seed is too small to compute a reliable lookalike.
- Lookalike already shipped 3 weeks ago and is fatigued — re-seed from a different source rather than expanding the same lookalike.

## Custom Audiences for Retargeting

Standard retargeting stack:

| Audience | Lookback | Use |
|---|---|---|
| Purchasers (LTV) | 180 days | Exclude from prospecting. Include in repeat-buyer / cross-sell campaigns. |
| Add-to-Cart, no Purchase | 30 days | Highest-intent retargeting cohort |
| Initiate Checkout, no Purchase | 14 days | Even higher intent than ATC; smaller audience |
| Site visitors, no purchase | 30–90 days | Mid-funnel retargeting |
| Video viewers (75%+) | 30–60 days | Warmer than site visitors for video-led brands |
| Engagers (page / IG profile) | 90–180 days | Coldest of the warm audiences; useful for awareness brands |

**Always exclude purchasers from prospecting.** Otherwise you're paying Meta to remarket to people who already converted on their own. The exception is repeat-purchase verticals (consumables, supplements, subscriptions) where re-engaging recent purchasers is the strategy.

## Audience Overlap

The Audience Overlap tool reports % overlap between any two audiences in the same account. Within a campaign, Meta's auction de-duplicates impressions (one user sees one ad, not two), but the LLM still has to allocate budget across overlapping ad sets — which fragments signal density and slows learning.

### Overlap thresholds

| Overlap | Diagnosis |
|---|---|
| < 15% | Independent audiences; healthy |
| 15–25% | Acceptable for deliberately layered tests |
| 25–50% | Functional overlap; consider consolidating |
| > 50% | Same audience in different wrapping; consolidate immediately |

**Three ad sets with > 50% pairwise overlap is one ad set in disguise.** Consolidating typically:
- Increases per-ad-set conversion volume → speeds Learning Phase exit
- Reduces signal fragmentation → improves LLM optimization
- Eliminates cannibalization in the campaign-level auction
- Costs you the per-audience reporting granularity (this is the only real downside; usually worth it)

## Advantage+ Audience and Detailed Targeting Expansion

Meta's "Advantage+ Audience" / "Detailed Targeting Expansion" toggles tell Meta it can ignore your manual targeting and expand to users it predicts will convert. With these on:

- The audience definition becomes a *suggestion*, not a constraint.
- Performance often improves (especially for Sales objective), but reports get harder to interpret because the served audience may not match the defined audience.
- For accounts mature enough to consider this, just go broad — the toggle and broad targeting converge.

The exception is **Special Ad Categories** — for Credit / Employment / Housing, Advantage+ targeting expansion is restricted by policy regardless of the toggle.

## Auditing the Audience Strategy

When asked "audit my targeting", run this checklist:

1. **Are prospecting and retargeting cleanly separated?** Same campaign with both is rare and usually wrong (except Advantage+ Shopping which intentionally blends them).
2. **Does prospecting exclude purchasers?** Pull the ad set's exclusion list — missing purchaser exclusion is a 5-minute fix worth real money.
3. **Are there 3+ ad sets with > 50% overlap?** Use the Audience Overlap tool. Consolidate.
4. **Is the account stuck on detailed targeting from 2019?** Look for ad sets with 5+ interest layers. These almost always underperform a simple broad version. Recommend an A/B test (broad vs. existing narrow) before recommending wholesale removal.
5. **Lookalike seeds — are any older than 90 days?** Refresh the seed; old seeds drift from current customer profile.
6. **Is there a no-retargeting account that should have one?** Almost any account spending > $1k/month should have at least one retargeting ad set on cart abandoners or site visitors.
