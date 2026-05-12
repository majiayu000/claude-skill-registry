# Meta Ads Industry Benchmarks

Reference benchmarks for "is X good or bad" questions. **Always anchor to the user's vertical and unit economics first** — a "good" CPA in legal services is a disaster in ecom, and vice versa.

These numbers are 2024–2025 vintage from third-party reports (Varos, Madgicx, Common Thread, Northbeam) plus our own observation of NotFair accounts. Adjust upward 10–15% for 2026 (CPMs continue to inflate). The most recent verification date is in `../../shared/policy-registry.json`.

## Vertical Benchmarks (Sales / Conversions Objective)

| Vertical | CPM | Link CTR | CPA | ROAS (target) |
|---|---|---|---|---|
| Ecommerce — apparel / accessories | $9–14 | 1.0–1.6% | $25–45 | ≥ 2.5× |
| Ecommerce — beauty / skincare | $10–15 | 1.1–1.7% | $20–40 | ≥ 3.0× |
| Ecommerce — home / furniture | $11–16 | 0.9–1.4% | $40–80 | ≥ 2.5× |
| Ecommerce — health / supplements | $12–18 | 1.0–1.5% | $30–55 | ≥ 3.0× |
| DTC subscription (food, consumables) | $11–16 | 0.9–1.4% | $35–65 | ≥ 2.0× (LTV-led) |
| Lead-gen B2C — local service | $7–11 | 1.2–2.0% | $12–28 (per lead) | n/a; CPL-led |
| Lead-gen B2C — finance / insurance | $11–17 | 0.8–1.3% | $30–80 (per lead) | n/a; CPL-led |
| B2B SaaS | $14–22 | 0.6–1.0% | $80–180 (per MQL) | n/a; CPL/MQL-led |
| Mobile app install (gaming) | $6–10 | 1.5–2.5% | $1.50–6 (per install) | n/a; ROAS D7-led |
| Mobile app install (utility / fintech) | $10–16 | 1.0–1.6% | $4–12 (per install) | n/a; ROAS D30-led |

**These are ranges, not averages.** Within a vertical, well-managed accounts will sit at the better end of the range; poorly-managed accounts will be 50–100% worse. Compare an account to the lower end (good) to see how much improvement is realistic.

## Adjustments

### Q4 inflation

| Period | CPM Multiplier vs. September |
|---|---|
| October | 1.20–1.40× |
| Black Friday / Cyber Week | 1.60–2.00× |
| Mid-December | 1.30–1.50× |
| Dec 26 → Dec 31 | 0.85–1.05× |
| January (post-holiday) | 0.70–0.85× |

Use these to normalize "is performance dropping" questions. A 30% CPM rise from October to November is below trend; a 30% drop from November to mid-December is normal.

### Geographic adjustments (vs. US)

| Country / Region | CPM Multiplier |
|---|---|
| US | 1.0× (baseline) |
| UK / AU / CA / NZ | 0.85–1.05× |
| Western Europe (DE, FR, IT, ES) | 0.65–0.85× |
| Nordic | 0.95–1.15× |
| LATAM | 0.20–0.40× |
| SEA (high-income — SG, HK) | 0.80–1.00× |
| SEA (mid-income — TH, MY, VN, PH, ID) | 0.10–0.25× |
| India | 0.10–0.20× |

Lower-CPM markets often have lower CVR and AOV that offset the cheaper impressions. Always cross-check ROAS against CPM, not CPM alone.

### Mobile vs. Desktop (Meta is mobile-dominant)

For most accounts > 90% of impressions are mobile. Desktop is occasionally relevant for B2B SaaS (decision-makers researching from work) but should not be the default plan. The split breakdown is available via `getInsights` with `breakdowns=publisher_platform,platform_position`.

### Placement performance ranking (typical, 2025)

| Placement | CPM | Link CTR | Notes |
|---|---|---|---|
| Facebook Feed | Mid | Mid–High | Workhorse placement |
| Instagram Feed | Mid–High | Mid | Strong for visual brands |
| Facebook Reels | Mid–Low | Low–Mid | Cheap impressions; lower intent |
| Instagram Reels | Mid | Low–Mid | Cheap impressions; broad reach |
| Stories (FB + IG) | Mid | Low | Brand impressions; rarely direct response |
| Marketplace | Low | Mid | Surprisingly strong for ecom in some verticals |
| Messenger | Low | Low | Often the weakest; consider excluding |
| Audience Network | Very Low | Very Low | Often spam-tier; consider excluding for direct response |

**Default recommendation:** start with Advantage+ Placements (let Meta choose). Move to manual placement selection only if a clear loser placement emerges in the breakdown report — and only after the ad set has 50+ events per placement to make a meaningful read.

## ROAS Reading Guide

ROAS by itself is incomplete. Always cite:

1. **The number** — e.g. 3.2×
2. **The attribution window** — e.g. 7-day click + 1-day view (7DC1DV)
3. **The source** — Meta-reported, Shopify-attributed, GA4-attributed, MMM-modeled
4. **The denominator window** — last 7 days, last 30 days, lifetime

`Meta-reported 7DC1DV ROAS 3.2× over last 30 days` is meaningful. `ROAS 3.2×` is not.

In post-iOS 14 reality, **Meta-reported ROAS typically exceeds Shopify ROAS by 20–40%** because of modeled conversions. Always footnote this when handing the user a number to make a scaling decision.

## Hook Rate (video creative)

Vertical-agnostic benchmarks for `3-Sec Video Views / Impressions`:

| Hook Rate | Quality |
|---|---|
| > 35% | Excellent — top-decile creative |
| 25–35% | Strong |
| 18–25% | Average |
| 10–18% | Weak — refresh the first 3 seconds |
| < 10% | Broken — viewers skip before any message lands |

Hook rate cuts across all verticals because it measures one thing: did the visual / first frame stop the scroll? If it didn't, nothing else matters.

## Benchmark Disclaimers

1. **Aged numbers.** Verify against current data (Varos / Madgicx public dashboards) for verticals where the user pushes back. CPMs inflate ~10–15% YoY.
2. **Within-vertical variance is huge.** Compare to similar-size accounts (within 0.5–2× spend) for a meaningful read. A $5k/month and a $500k/month brand in the same vertical will have very different benchmarks.
3. **AOV and unit economics override industry benchmarks.** A "high" CPA in absolute terms can be wildly profitable if AOV is high and margin is fat. Always compute Break-Even ROAS first (see `../../shared/meta-math.md`).
4. **Reported numbers ≠ ground truth.** Meta-reported ROAS systematically overstates actual ROAS in ecom. Treat these as Meta-reported benchmarks; reconcile against the user's e-commerce platform before acting on them.
