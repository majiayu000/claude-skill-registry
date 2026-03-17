---
name: ideas-forecasting
description: Build a 90-day startup forecast and proposed goals from a business idea and product specs using web research (competitor analysis, price bands, channel benchmarks, demand signals). Use when a user provides idea/product inputs and wants the agent to set most targets, assumptions, risks, and validation metrics before SFS-00 or ideas-go-faster.
---

# Ideas Forecasting

Use this skill to invert planning: user provides the business idea and products, then the agent proposes practical 90-day targets from external evidence.

## Invocation

```bash
/ideas-forecasting
/ideas-forecasting --biz=HEAD
/ideas-forecasting --biz=PET --country=IT --horizon-days=90
/ideas-forecasting --biz=PET --launch-surface=pre-website
```

Defaults:
- `horizon-days=90`
- `country=IT` if not provided
- `launch-surface=website-live` unless user states no site is ready
- focus: speed to first sales for startup businesses

## Inputs

Minimum required:
- `Business code`: e.g. `HEAD`, `PET`
- `Business idea`: one-paragraph concept
- `Products`: list of products with short specs

Strongly recommended:
- `Price intent` (if known): target price or range
- `Channels`: DTC site, marketplaces, social commerce, retail, etc.
- `Budget guardrails`: launch budget cap and ad budget guardrail
- `Stock timeline`: date first sellable stock is available
- `Launch surface`: `website-live` or `pre-website`
- `Constraints`: legal, ops, brand, geography, supply chain

## Launch Surface Modes

### `website-live`

Use standard ecommerce funnel forecasting.

Core forecast metrics:
- sessions
- conversion rate
- AOV
- orders
- gross revenue
- gross margin
- CAC

### `pre-website`

Use this when no production website is ready. Forecast around early sales validation channels and assisted commerce.

Core forecast metrics:
- qualified leads
- assisted order attempts
- assisted order conversion rate
- pre-order/deposit count (if used)
- average order value proxy
- gross revenue
- gross margin
- blended acquisition cost proxy

Channel focus for research and recommendations:
- lightweight landing + form capture
- social DM/WhatsApp assisted sales
- marketplace trial listing (if appropriate)
- community/partner channels

## Operating Rules

1. Separate `observed` vs `inferred` in every numeric section.
2. Use scenario ranges (`P10`, `P50`, `P90`), never single-point certainty.
3. Prefer region-relevant recent sources; attach URL + access date.
4. Do not invent competitor metrics when not available.
5. Optimize recommendations for startup speed-to-revenue, not infrastructure perfection.
6. Treat outputs as forecast proposals requiring operator approval.

## Workflow

### Stage 1: Intake and Clarify

1. Capture required inputs.
2. Ask up to 3 high-impact clarification questions if blockers remain.
3. Freeze an intake packet for this run.

### Stage 2: Build Research Prompt

1. Load `references/deep-research-prompt-template.md`.
2. Fill placeholders from intake packet.
3. Set `launch-surface` explicitly and enforce mode-specific metric guidance.
4. Keep expected outputs contract intact.

### Stage 3: Run Research

1. Run Deep Research using the filled prompt (preferred).
2. If Deep Research is unavailable, run equivalent manual web research with citation discipline.
3. Collect evidence in a source table before forecasting.

### Stage 4: Forecast and Goal Proposal

Produce:
1. 90-day scenario forecast (`P10/P50/P90`) using mode-appropriate metrics:
   - if `website-live`: sessions, conversion rate, AOV, orders, gross revenue, gross margin, CAC, payback proxy
   - if `pre-website`: qualified leads, assisted order attempts, assisted conversion, pre-orders/deposits (if used), AOV proxy, gross revenue, gross margin, acquisition cost proxy
2. competitor benchmark table (pricing, offer structure, channel posture)
3. proposed targets for first 90 days and first 4 weeks
4. assumption register with confidence tags (`high/medium/low`)
5. risk register with mitigation actions
6. week-1/week-2 validation checklist to recalibrate forecast quickly

### Stage 5: Persist Outputs

Write:
- `docs/business-os/forecasts/<YYYY-MM-DD>-<BIZ>-forecast.user.md`

If this run is intended to seed SFS-00, also write:
- `docs/business-os/startup-baselines/<BIZ>-forecast-seed.user.md`

## Output Contract

`<YYYY-MM-DD>-<BIZ>-forecast.user.md` must include:

1. `Executive Summary` (<=12 bullets)
2. `Input Packet` (what user provided)
3. `Launch Surface Mode` (`website-live` or `pre-website`) and chosen metric set
4. `Competitor Benchmark Table` (with source links)
5. `90-Day Forecast Table (P10/P50/P90)`
6. `Proposed Outcome Statement`
7. `Proposed Targets`
8. `Assumptions Register`
9. `Risk Register`
10. `First-14-Day Validation Plan`
11. `Source List` (URL + access date)
12. `Confidence and Caveats`

## Definition of Expected Outcomes

An expected outcome in this skill means a measurable 90-day business result with:
- `Outcome statement`: plain-language result
- `Baseline`: starting point now
- `Target`: expected value or range by deadline
- `Deadline`: exact date
- `Leading indicators`: weekly signals proving progress
- `Decision link`: what decision this outcome unlocks

Use forecast evidence to propose these fields; do not leave them blank.

## Integration with Existing Flow

1. Forecasting runs before idea prioritization when startup context is sparse.
2. Approved forecast outcomes seed `SFS-00` business intent baseline.
3. `ideas-go-faster` should use approved forecast outcomes as steering constraints.
4. `fact-find` / `plan-feature` / `build-feature` remain the delivery path for selected go items.

## Red Flags (invalid output)

1. Missing competitor citations for numeric claims.
2. Single-point target claims without scenario ranges.
3. No distinction between observed data and inferred estimates.
4. No first-14-day validation plan.
5. Proposed goals that ignore user budget/stock constraints.
6. Uses website-only metrics in `pre-website` mode without conversion mapping.
