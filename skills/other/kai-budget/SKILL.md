---
name: kai-budget
description: Marketing budget planning and forecasting — channel allocation, CAC targets, ROI projections, and spend optimization. Use when "marketing budget", "budget planning", "channel allocation", "marketing spend", "CAC forecast", "budget forecast", "how much should I spend", "allocate budget", or any request to plan, forecast, or optimize marketing spend.
---

# /kai-budget — Spend Allocated Against Unit Economics, Not Vibes

## Objective

A marketing budget with defensible arithmetic behind every line: unit economics modeled or explicitly estimated, channel-by-channel allocation with expected CAC and volume, three ROI scenarios, a ramp schedule, and the kill/scale criteria that decide what happens next quarter. The number the user leaves with is one they could defend to a board.

Broken economics are the first finding, not a footnote. An LTV:CAC below 1:1 or a payback beyond 18 months changes the whole recommendation.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact budget document. Approving the plan is not authorizing the spend; spend authorization is a separate decision.
- **C3** — `banned_word_check` clean, every projection carries a confidence level, every assumption that needs validation is flagged as such, and someone other than the author read it end to end.
- **O1** — every allocation line names the metric that proves it worked (CAC, volume, payback), its baseline, its threshold, and its owner, recorded before the first dollar moves. A budget with no predeclared thresholds cannot be graded later.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Eight things must be known before allocating anything:** business model (SaaS, ecommerce, services, marketplace); current MRR/ARR; growth stage (pre-launch, early, growth, scale); current spend total and by channel; the target growth rate or revenue goal; sales cycle length and average deal size; current CAC and LTV if known; and team composition (in-house, agency, contractors).
- **Where metrics are missing, use industry benchmark ranges and label them as estimates.** An estimated input never gets presented as a measured one.
- **Never recommend spend the user cannot sustain for 6 months.**
- **Always reserve 10–20% for testing.**
- **CAC targets are validated against LTV.** Never recommend acquisition that loses money at the target volume.
- **Every projection carries a confidence level** — High, Medium, or Low.
- **Stage-appropriate only.** No enterprise tactics for a pre-launch company.
- **Round to practical amounts.** $4,700 or $5,000, not $4,731.28.
- **This document does not authorize spend.** It recommends it.

## Context

| Need | Load |
|---|---|
| Budget models, benchmarks, forecasting method | `knowledge/playbooks/marketing-budget-forecasting.md` |
| Unit economics, benchmarks by business model | `knowledge/playbooks/saas-metrics-guide.md` |
| Persona alignment for channel choice | `knowledge/personas/_persona-index.md` |
| Revenue, stage, current channels | `MARKETING.md` (project root) |

**Unit economics to compute or estimate before allocating:** CAC (total spend / new customers) · LTV (ARPU × average lifespan) · **LTV:CAC, target 3:1 or better** · payback period in months · gross margin, which sets spend capacity. Benchmark each against the business model. Flag broken economics explicitly: **LTV:CAC below 1:1, or payback beyond 18 months.**

**Per active channel, assess:** current spend, volume (leads, signups, purchases), channel CAC, trend direction (improving, stable, degrading), and saturation risk at current spend.

**Deliverables:**

- **Allocation model** — total recommended monthly/quarterly budget, the stage-appropriate percentage-of-revenue benchmark, and a per-channel table: Channel / Monthly Spend / Expected CAC / Expected Volume / Confidence.
- **Three ROI scenarios** — Conservative (80% of target performance), Base case (expected), Aggressive (120% with increased spend). Each states spend, leads, customers, revenue, ROI, and payback period.
- **Spend ramp plan** — month-by-month schedule rather than a single dump, the testing allocation, kill criteria (when to stop spending on a channel), and scale criteria (when to increase).
- **Optimization calls** — which channels to increase (high ROI, unsaturated), decrease (poor CAC, saturated), and test (untapped, stage-appropriate).
- **One-page executive summary** — total recommended spend, expected acquisition volume, blended CAC target, projected ROI, and the top 3 risks with mitigations.
- A quarterly review cadence, and an explicit list of assumptions needing validation against real data.

## Escalate when

- Unit economics come out broken (LTV:CAC below 1:1, payback past 18 months) — the answer is a fix, not a budget.
- The revenue goal requires spend the business cannot sustain for six months.
- No CAC or LTV data exists and the user wants precise projections rather than ranges.
- The requested allocation contradicts the company's stage.
- The plan would be read as spend authorization rather than a recommendation.
