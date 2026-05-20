---
name: lp-forecast
description: S3 startup 90-day forecaster — build P10/P50/P90 scenario bands from zero operational data
---

# lp-forecast — Startup 90-Day Forecaster

Build P10/P50/P90 scenario bands and first-14-day validation plan for pre-launch or newly launched businesses with zero historical performance data.

## Invocation

```bash
/lp-forecast --business <BIZ> [--horizon-days 90] [--launch-surface pre-website|website-live]
```

- `--business`: Business name (BRIK, intshop, etc.)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

- `--horizon-days`: Forecast horizon in days (default: 90)
- `--launch-surface`: Stage of launch — `pre-website` (MVP planning) or `website-live` (post-launch tracking)

## Operating Mode

READ + RESEARCH + FORECAST

- Read existing business context, offer hypothesis (from lp-offer/MARKET-06), and available market data
- Research competitor benchmarks, channel performance ranges, and market size signals
- Forecast P10/P50/P90 scenario bands with unit economics assumptions
- Generate first-14-day validation plan (THE primary deliverable)

## Differs from lp-do-idea-forecast

This skill is NOT a rename or copy of `lp-do-idea-forecast`. Key differences:

1. **Works from zero operational data**: lp-do-idea-forecast requires historical performance data or existing market intelligence packs. lp-forecast builds forecasts from competitor benchmarks and channel ranges only.

2. **No market intelligence pack prerequisite**: lp-do-idea-forecast blocks when `latest.user.md` market research is stale and requires Deep Research prompt. lp-forecast proceeds with available evidence (competitor pricing, channel benchmarks) and marks confidence accordingly.

3. **Simpler output contract**: lp-do-idea-forecast delivers a full 12-section Output Contract with detailed channel plans and financial models. lp-forecast delivers P10/P50/P90 bands, unit economics assumptions, and a first-14-day validation plan.

4. **No Deep Research gate**: lp-do-idea-forecast stops and requires manual Deep Research when data is insufficient. lp-forecast proceeds with available evidence and tags assumptions as low-confidence when data is sparse.

5. **Validation-first mindset**: Both include first-14-day validation plans, but lp-forecast makes this THE central output — the forecast is a hypothesis to validate, not a plan to execute.

## Inputs

Reads from:
- Business context: `docs/business-os/startup-baselines/<BIZ>/`
- Offer hypothesis: Output from lp-offer (MARKET-06) — `docs/business-os/startup-baselines/<BIZ>/offer.md`
- Channel selection (optional if available): Output from lp-channels (SELL-01) — `docs/business-os/startup-baselines/<BIZ>/channels.md`
- Market data: Any available competitor pricing, channel benchmarks, market size signals (opportunistic)

**Artifact registry**: Canonical producer paths are defined in `docs/business-os/startup-loop/artifact-registry.md`.

No formal market intelligence pack required. If none exists, proceed with web research.

## Workflow

### Stage 1: Gather Available Evidence

- Read offer hypothesis (pricing, target customer, value prop)
- Read channel selection (which channels, why chosen)
- Web research: competitor pricing, channel benchmarks (e.g., Google Ads CPC for niche, email open rates for vertical)
- Market size signals: search volume, competitor traffic estimates, industry reports (opportunistic)
- Tag confidence: high (multiple sources), medium (single source), low (extrapolated/assumed)

### Stage 2: Build Scenario Forecast

Create P10/P50/P90 scenario bands for:
- **Revenue**: 90-day cumulative revenue range
- **Orders**: 90-day order count range
- **Traffic**: 90-day unique visitor range (if website-live)
- **Leads**: 90-day lead count range (if pre-website)

Scenarios:
- **P10** (pessimistic): Low conversion, high CAC, slow ramp
- **P50** (base case): Channel benchmark conversion, median CAC, steady ramp
- **P90** (optimistic): High conversion, low CAC, fast ramp

### Stage 3: Define Unit Economics Assumptions

For each scenario (P10/P50/P90):
- **CAC**: Customer acquisition cost per channel
- **AOV**: Average order value
- **Margin**: Gross margin per order
- **Conversion rate**: Visitor-to-order or lead-to-order
- **Channel mix**: Traffic/spend distribution across selected channels

### Stage 4: Create First-14-Day Validation Plan

THE key output. Define:
- **Metrics to track**: Which KPIs confirm or refute the forecast
- **Measurement cadence**: Daily/weekly/milestone-based
- **Decision gates**: When to pivot, pause, or accelerate
- **Validation thresholds**: What metrics must hit what values by day 7, day 14
- **Data sources**: Where to pull each metric (analytics, CRM, ads dashboard)

Example decision gate: "If Day 7 CAC exceeds P90 CAC by 50%, pause paid channels and pivot to organic."

### Stage 5: Persist Output

Write forecast to:
```
docs/business-os/startup-baselines/<BIZ>/S3-forecast/YYYY-MM-DD-lp-forecast.user.md
```

Output format:
- Scenario summary table (P10/P50/P90 bands)
- Unit economics assumptions per scenario
- Channel-specific ranges (per channel selected in lp-channels)
- First-14-day validation plan (metrics, thresholds, decision gates)
- Assumption register with confidence tags
- Source list with URLs

## Output Contract

File: `docs/business-os/startup-baselines/<BIZ>/S3-forecast/YYYY-MM-DD-lp-forecast.user.md`

**Artifact registry**: Canonical path defined in `docs/business-os/startup-loop/artifact-registry.md` (artifact ID: `forecast`).

Required sections:
1. **Scenario Summary**: P10/P50/P90 bands for revenue, orders, traffic/leads
2. **Unit Economics**: CAC, AOV, margin, conversion rate per scenario
3. **Channel Ranges**: Traffic, spend, CAC per channel (from lp-channels)
4. **First-14-Day Validation Plan**: Metrics, thresholds, decision gates, data sources
5. **Assumption Register**: All assumptions with these mandatory fields:
   - `assumption_id` — stable ID for tracking across review cycles
   - `assumption_statement` — plain-language claim being made
   - `prior_range` — plausible range before evidence
   - `sensitivity` — impact on CAC/CVR/revenue if assumption is wrong (Low/Medium/High)
   - `evidence_source` — URL or artifact reference
   - `confidence_level` — `low` (<60) / `medium` (60–79) / `high` (≥80)
   - `kill_trigger` — observable state that invalidates this assumption (e.g., "Day 7 CAC > 2× P90 estimate")
   - `owner` — named person responsible for monitoring and re-checking
   - `next_review_date` — ISO date for next assumption review
6. **Source List**: URLs for competitor data, channel benchmarks, market signals

## Quality Checks

Self-audit before delivery:
- [ ] All three scenarios (P10/P50/P90) present with numeric ranges
- [ ] Unit economics defined for each scenario
- [ ] Channel-specific ranges match channels selected in lp-channels
- [ ] First-14-day validation plan includes metrics, thresholds, and decision gates
- [ ] Assumption register includes all 9 mandatory fields for every assumption (`assumption_id`, `assumption_statement`, `prior_range`, `sensitivity`, `evidence_source`, `confidence_level`, `kill_trigger`, `owner`, `next_review_date`)
- [ ] Confidence tier declared (low/medium/high) with corresponding spend cap, time cap, cadence, and allowed decision class
- [ ] Source list includes URLs for all claims (no unsourced assertions)
- [ ] Output file persisted to `docs/business-os/startup-baselines/<BIZ>/S3-forecast/`

## Red Flags

Invalid outputs that require rework:
- Single-point forecast (no P10/P50/P90 bands)
- Missing first-14-day validation plan
- Unsourced claims (no URLs in source list)
- Unit economics missing for any scenario
- Channel ranges don't match lp-channels output
- Assumption register missing `kill_trigger`, `owner`, or `next_review_date` for any assumption
- Confidence tier not declared or spend cap / time cap not stated for the tier
- Validation plan has no decision gates

## Integration

- **Consumes**: lp-offer output (MARKET-06); may consume lp-channels output (SELL-01) when available
- **Feeds into**: lp-prioritize (S4 prioritization), startup-loop S4 baseline (first-14-day tracking)
- **Trigger**: Called automatically by startup-loop at S3 stage, or manually via `/lp-forecast`

## Forecast Guardrails (Confidence Tier Policy)

Apply the correct tier based on the overall confidence level of the forecast. Confidence level = the lowest confidence across all P50 scenario assumptions.

| Forecast confidence tier | Spend cap | Operator time cap | Re-check cadence | Allowed decision class |
|---|---|---|---|---|
| `low` (<60) | 10% of planned monthly spend (or fixed micro-budget) | ≤5 hours/week/channel | Every 7 days | `Continue` or `Investigate` only — no `Scale` or `Kill` |
| `medium` (60–79) | 30% of planned monthly spend | ≤10 hours/week/channel | Every 7 days | `Keep`, `Pivot`, or `Continue` — no full `Scale` |
| `high` (≥80) | Up to planned budget | Planned operating cadence | Weekly | Full decision set including `Scale` and `Kill` |

**Guardrail breach handling:**
- If actual spend is at or approaching the cap before the re-check cadence is due, pause and run an ad-hoc review — do not extend the cap unilaterally.
- If confidence improves at re-check (new evidence), tier may be upgraded. Document the upgrade with evidence source.
- Unknown or missing confidence values default to `low` tier — fail closed.

**Reference:** `docs/plans/startup-loop-marketing-sales-capability-gap-audit/fact-find.md` (Sparse-evidence forecast control surface)

## Launch Surface Modes

### pre-website
- Focus on lead generation metrics (email signups, waitlist, pre-orders)
- Traffic forecast not required (no website yet)
- CAC based on pre-launch channels (social, partnerships, waitlist ads)

### website-live
- Focus on traffic, conversion, orders
- CAC based on post-launch channels (SEO, paid ads, email, partnerships)
- Include visitor-to-order funnel metrics

## Notes

- This forecast is a **hypothesis to validate**, not a prediction to execute
- Low-confidence assumptions are acceptable — apply the `low` confidence tier guardrail (10% spend cap, ≤5 hrs/week/channel, Continue/Investigate only). See `## Forecast Guardrails` above.
- First-14-day validation plan is THE critical output (the forecast exists to be tested)
- If evidence is sparse, proceed with low-confidence tags and wide P10-P90 bands
- No Deep Research gate — work with what's available and mark uncertainty
