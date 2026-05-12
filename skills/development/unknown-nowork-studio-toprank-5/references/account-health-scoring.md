# Meta Ads Account Health — Scoring Rubric

The 7 dimensions scored 0–5 in `/meta-ads-audit`. Each dimension represents a distinct question the audit needs to answer. Overall score = `round(sum × 100 / 35)`.

The dimensions are ordered from upstream (signal infrastructure) to downstream (scaling) — fix in this order, because fixes downstream of broken upstream are worthless.

---

## Dimension 1 — Pixel + CAPI Health

*"Can Meta see what's happening?"*

If signals are broken, every decision downstream is built on lies — and Smart Bidding can't optimize what it can't measure.

### Scoring

| Score | Criteria |
|---|---|
| 5 | Pixel + CAPI deployed, EMQ ≥ 8.0, deduplicated by event_id, all key events firing (View, AddToCart, InitiateCheckout, Purchase) |
| 4 | Pixel + CAPI deployed, EMQ 7.0–7.9, dedup correct, key events firing |
| 3 | Pixel + CAPI deployed, EMQ 6.0–6.9, dedup correct |
| 2 | Pixel only OR CAPI without dedup OR EMQ 5.0–5.9 |
| 1 | Pixel only with EMQ < 5.0, OR CAPI broken, OR key events missing (e.g. Purchase event not firing) |
| 0 | Pixel not firing OR no purchases recorded over 30 days despite spend ≥ 5× account CPA |

### Red Flags

- Reported conversions ≥ 50% of clicks (tag firing on page load, not real conversions)
- Conversion attribution mismatched between Meta and Shopify by > 50% (Shopify is ground truth; Meta should be within ±30%)
- iOS share of conversions disproportionately low vs. impression share (ATT decline + missing CAPI)
- All conversions show as `offsite_conversion.fb_pixel_custom` instead of named events (Pixel deployed without standard event mapping)

---

## Dimension 2 — Attribution & Measurement Setup

*"Are we measuring success the right way?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | Attribution window matches sales cycle, off-platform truth source connected (Shopify, GA4, MMM), holdout test or incrementality study run within last 12 months |
| 4 | Attribution matches sales cycle; off-platform truth source loosely reconciled monthly |
| 3 | Default attribution (7DC1DV) used without explicit consideration; some off-platform reconciliation |
| 2 | No off-platform truth source consulted; Meta-reported numbers used directly for budget decisions |
| 1 | Attribution window mismatched to sales cycle (e.g. 1-day click on a high-consideration purchase) |
| 0 | Last-touch attribution used as the only measure; no awareness of modeled conversion premium |

### Red Flags

- Reported ROAS used to scale into unprofitability because of modeled-conversion inflation
- Attribution window changed mid-campaign without re-baselining (creates apples-to-oranges comparisons)
- Multi-touch journey ignored (Meta gets full credit for the conversion when Google or organic was the real driver)

---

## Dimension 3 — Campaign Structure

*"Is the account organized for the bidding LLM to learn?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | 2–4 campaigns, prospecting/retargeting cleanly split, CBO default, no audience overlap > 25%, ASC running and outperforming |
| 4 | Clean structure; minor overlap or one fragmentation issue |
| 3 | Functional; some fragmentation or anti-patterns |
| 2 | Multiple anti-patterns: campaigns split by creative/placement, > 5 campaigns, single-ad-set dependency |
| 1 | Heavy fragmentation: 8+ campaigns, ad sets with > 50% mutual overlap, no funnel logic |
| 0 | Special Ad Category misclassified, or campaign-level structure prevents Learning Phase exit on the majority of ad sets |

### Red Flags

- > 50% audience overlap between active ad sets in the same campaign
- One ad set > 70% of campaign spend (fragility, not concentration)
- Branded campaigns running on Meta (almost always wasted spend — Meta is discovery, not search)
- Campaign split by creative type or placement (anti-pattern; consolidate)
- Special Ad Category vertical without proper classification

---

## Dimension 4 — Creative Health

*"Is the creative giving the bidding LLM enough to optimize over?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | 4–6 distinct concepts per active ad set, all aspect ratios uploaded, weekly creative refresh cadence, top concept's hook rate > 30% |
| 4 | Adequate diversity; refresh cadence appropriate to spend velocity |
| 3 | Functional creative, occasional refresh; some fatigue patterns |
| 2 | Limited concept diversity (1–2 concepts per ad set), infrequent refresh, hook rate 15–25% |
| 1 | Single concept across most ad sets, no refresh in 6+ weeks, hook rate < 15%, frequency > 4.0 with declining CTR |
| 0 | Creative pool exhausted, declining performance for 4+ weeks, no replacement creative in pipeline |

### Red Flags

- Frequency > 3.0 with CPM rising ≥ 30% w/w and CTR declining ≥ 30% w/w (active fatigue)
- All ads on one ratio (1:1) when 4:5 + 9:16 are missing — placements unlocked by ratios are not being used
- Hook rate (3-sec views / impressions) < 15% on video ads — viewers skip before any message lands
- Same hero ad running for > 8 weeks at > $200/day (typical fatigue threshold passed)
- "We don't have time to ship new creative" — usually the bottleneck for further scaling

---

## Dimension 5 — Audience Strategy

*"Are we targeting in a way that lets the bidding LLM win?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | Broad-targeting prospecting, lookalikes from quality seeds (purchasers / high-LTV), retargeting with proper exclusions, < 25% overlap |
| 4 | Mostly broad with some targeted lookalikes; clean exclusions |
| 3 | Functional targeting; some legacy interest stacks |
| 2 | Heavy reliance on detailed-targeting interests, no purchasers exclusion in prospecting, audience overlap 25–50% |
| 1 | Narrow interest stacks across all prospecting, multiple lookalike layers stacked, > 50% overlap |
| 0 | No retargeting layer at all, or interest stacks contradict Meta's published guidance with no testing data to justify |

### Red Flags

- Prospecting ad sets do not exclude past purchasers — paying to retarget converted customers
- Lookalike seed > 90 days old (drift from current customer profile)
- Stacked lookalikes (LAL 1–3% + LAL 1–5% in the same ad set) — pure overlap
- No retargeting on cart abandoners despite > $1k/month spend
- Account spending > $5k/month with only narrow-interest targeting (likely leaving Advantage+ Audience / broad gains on the table)

---

## Dimension 6 — Spend Efficiency

*"Are we getting profitable returns on every dollar?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | Account ROAS ≥ 1.5× Break-Even ROAS, < 5% spend on losing ad sets, MER ≥ industry-typical, healthy unit economics confirmed |
| 4 | Account profitable; minor waste pockets |
| 3 | Account roughly at break-even; meaningful waste in 1–2 ad sets |
| 2 | Significant waste (≥ 15% of spend on ad sets below break-even), some campaigns unprofitable |
| 1 | Most spend below break-even; reported ROAS papering over real losses |
| 0 | Account-level losing money even on Meta-reported ROAS; structural unprofitability |

### Red Flags

- > 20% of spend on ad sets with ROAS < 0.7 × Break-Even (waste pockets that survive on inertia)
- Heavy reliance on Meta-reported ROAS for scaling decisions (no MER / Shopify cross-check)
- Branded brand-defense campaigns running (almost always waste on Meta)
- Audience Network not excluded for direct-response brands (often underperforms by 50%+)

---

## Dimension 7 — Scaling Readiness

*"Can we 2× spend without breaking the account?"*

### Scoring

| Score | Criteria |
|---|---|
| 5 | Strong ROAS headroom, fresh creative pipeline, multiple winning ad sets, audience saturation < 30%, ASC tested and working |
| 4 | Headroom present; one constraint to address before aggressive scaling |
| 3 | Some headroom; structural debt would slow scaling |
| 2 | Account near saturation; doubling spend likely doubles CPA |
| 1 | Account at the wall: frequency too high, audience overlap too high, no creative pipeline |
| 0 | Account already losing money — scaling is moot until structural fixes land |

### Red Flags

- Single dominant ad set carrying the account (fragility)
- All winning audiences at > 50% saturation
- No creative pipeline (no new concepts in production / approval queue)
- Pixel + CAPI weak — scaling will starve faster than expected because match quality drops with volume

---

## Impression Share / Reach Saturation Matrix

Meta doesn't publish "impression share" the way Google does. The proxies are **reach saturation** (Reach / Estimated Audience Size) and **frequency trend**:

| | Saturation < 30% | Saturation 30–60% | Saturation > 60% |
|---|---|---|---|
| **Frequency < 2.0** | Healthy; clear scaling room | Healthy; some headroom | Audience nearly maxed; broaden |
| **Frequency 2.0–3.5** | Warming up; monitor | Mature; refresh creative soon | Near saturation; rotate audience |
| **Frequency > 3.5** | Anomalous — check tracking | Late-stage; refresh creative | Saturated; new audience required |

Use this matrix to translate raw frequency / saturation numbers into action recommendations.

## Composite Score Mapping

| Score | Verdict | Default Recommendation |
|---|---|---|
| 90+ | Excellent | Continue cadence; scale within 20% rule; test new creative concepts |
| 75–89 | Good | Address 1–2 dimensions scoring < 4; otherwise hold steady |
| 60–74 | Acceptable | Prioritized fix list across 2–3 dimensions; expect meaningful lift |
| 40–59 | Needs Work | Structural fixes required before scaling; budget freeze advisable |
| < 40 | Critical | STOP further spend until Pixel + CAPI + structure fixed; reset baseline |

A score below 50 on Dimension 1 (Pixel + CAPI) overrides the composite — recommend the user stop scaling decisions until tracking is fixed regardless of how the rest of the account scores. Tracking is upstream of everything.
