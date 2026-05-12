# Creative Fatigue — Diagnosis and Refresh Cadence

Meta is creative-led. The single highest-leverage variable in account performance is creative — not bidding, not audience, not budget. This reference is the diagnostic kit for "is this creative dying, and what do I do about it".

## The Fatigue Stack — Signals in Priority Order

Read these in order. The earliest signal usually leads the others by 3–5 days.

### Signal 1 — Hook Rate (video only)

```
Hook Rate = 3-Sec Video Views / Impressions × 100
```

| Hook Rate | Diagnosis |
|---|---|
| > 30% | Strong; the thumbnail / first frame is doing its job |
| 20–30% | Acceptable for most verticals |
| 10–20% | Weak hook; refresh first frame or thumbnail |
| < 10% | Broken hook; viewer scrolls past before the message lands |

**Trend matters more than absolute number.** A hook rate dropping from 28% to 18% in a week is a clearer signal than a flat 18%. Watch the trend over a rolling 7-day window.

### Signal 2 — Link CTR

```
Link CTR = Inline Link Clicks / Impressions × 100
```

Use **inline_link_clicks**, not all-clicks. Vertical and creative format affect the absolute number — see `industry-benchmarks.md` — but the trend over time is universal.

| Trend | Diagnosis |
|---|---|
| Link CTR steady week-over-week | Creative is healthy at this frequency |
| Link CTR down 15–30% w/w | Early fatigue; plan a refresh in the next 5–10 days |
| Link CTR down ≥ 30% w/w | Active fatigue; ship new creative now |
| Link CTR up week-over-week with stable spend | Creative is gaining traction; do not change anything |

### Signal 3 — CPM Rise

```
CPM = (Spend / Impressions) × 1000
```

CPM rises when (a) the audience is saturating and Meta has to bid higher to reach the next user, (b) competitors are bidding more aggressively (seasonality), or (c) Meta's relevance score for the ad has dropped (creative fatigue).

| Trend | Diagnosis |
|---|---|
| CPM steady or rising < 10% w/w | Healthy |
| CPM rising 10–30% w/w with stable CTR | Likely competitive pressure or seasonality, not creative |
| CPM rising ≥ 30% w/w with declining CTR | Creative-driven fatigue; relevance is dropping |
| CPM rising ≥ 30% w/w with frequency > 3.0 | Audience saturation; rotate audience or refresh creative |

### Signal 4 — Frequency

```
Frequency = Impressions / Reach          (over a rolling 7-day window)
```

Frequency alone doesn't diagnose anything — it's a denominator for the other signals. But these guardrails apply:

| Audience Type | Frequency Cap (weekly) |
|---|---|
| Cold prospecting (broad / lookalike) | ≤ 2.0 |
| Warm retargeting (site visitors / engagers) | 2.0–3.5 |
| Hot retargeting (cart abandoners, post-purchase) | 3.0–5.0 (urgency justifies high frequency) |

Frequency above the cap with declining CTR/CPM is fatigue. Frequency above the cap with stable or rising CTR is rare but not actionable — leave it alone.

## The Refresh Decision Tree

When fatigue signals fire, work down this tree:

1. **Is this a single-ad problem or a campaign-wide problem?**
   - Single ad fatiguing while siblings hold up → pause the fatigued ad, leave the rest. Plan a replacement creative.
   - All ads in the ad set fatiguing simultaneously → audience saturation, not creative fatigue. Move to step 3.
   - All ad sets in the campaign fatiguing → likely a seasonality / competitive pressure issue or a measurement break (Pixel issue). Cross-check.

2. **Single-ad refresh: what kind of new creative?**
   - Same concept, new variation (re-cut, new opening, different testimonial)? Cheap, safe; ~50% chance of matching the fatigued ad's peak.
   - New concept entirely (different angle, different emotion, different format)? More expensive but the only way to reset the fatigue clock cleanly.
   - Avoid refreshing only the headline / primary text on a fatigued visual. Meta's bidding LLM weights the visual heavily — copy tweaks alone rarely reset fatigue.

3. **Audience saturation: rotate or expand?**
   - If the audience is a custom audience or narrow lookalike, expand to LAL 1–3% or LAL 1–5%, or seed a new lookalike from a different source (purchasers vs subscribers vs site engagers).
   - If the audience is already broad, the fatigue is probably creative — go back to step 2.
   - If the audience is a retargeting pool, expand the lookback window (30 → 90 days) before rebuilding.

4. **Campaign-wide fatigue: when to stop refreshing.**
   - If you've shipped 3+ creative refreshes in 6 weeks and nothing is performing close to historical highs, the problem is probably not creative — it's market saturation or a structural issue (offer, landing page, attribution). Run a short-pause test (1–2 weeks of pause), then return with fresh creative + a fresh audience seed.

## Refresh Cadence — Spend-Velocity-Aware

The right refresh cadence depends on how fast the audience is being burned through, not on calendar age.

| Daily Spend per Ad Set | Typical Hero-Creative Lifespan |
|---|---|
| < $50 | 4–8 weeks |
| $50–$200 | 2–4 weeks |
| $200–$1,000 | 7–14 days |
| > $1,000 | 5–10 days |

Use frequency trend as the actual trigger, not these numbers — they're priors. A $1,000/day ad set that holds a 2.0 frequency cap because the audience is genuinely huge can run the same creative for 4 weeks. A $50/day ad set on a 500k-person custom audience burns through in two weeks.

## Concept Diversity — How Many Creatives at Once

Per active ad set, target 4–6 distinct creative concepts running concurrently.

- **Distinct concept**, not distinct variant. UGC of three different customers is one concept. Founder explainer + UGC testimonial + product demo + lifestyle is four concepts.
- Same concept across 1:1, 4:5, and 9:16 aspect ratios counts as one — Meta treats the concept as one for relevance scoring; the ratios just unlock more placements.
- Below 3 concepts per ad set, Meta's bidding LLM has nothing to optimize across — performance volatility increases. Above 8, you're spreading spend too thinly for any one to clear the 50-events-in-7-days Learning bar.

## What "creative fatigue" doesn't fix

- **Bad offer** — no creative refresh saves an unwanted product or an uncompetitive price.
- **Broken landing page** — high CTR with a slow / mismatched LP burns budget twice.
- **Wrong audience** — perfect creative shown to the wrong cohort fatigues fast because it never resonated in the first place.
- **Pixel / CAPI breakage** — fresh creative on broken tracking is invisible to Meta's optimization; the algorithm can't learn what works.

When the user says "performance is dropping", check these structural issues *before* recommending a creative refresh. The cheapest fix is the structural one.
