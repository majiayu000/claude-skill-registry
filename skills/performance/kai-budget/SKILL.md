---
name: kai-budget
description: Marketing budget planning and forecasting — channel allocation, CAC targets, ROI projections, and spend optimization. Use when "marketing budget", "budget planning", "channel allocation", "marketing spend", "CAC forecast", "budget forecast", "how much should I spend", "allocate budget", or any request to plan, forecast, or optimize marketing spend.
---

# kai-budget — Marketing Budget Planning & Forecasting

Build a data-driven marketing budget: channel allocation, CAC/LTV modeling, ROI projections, and spend optimization by stage.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## References

Load these files as context before starting:

- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\marketing-budget-forecasting.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\saas-metrics-guide.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`

## Phase 1 — Discovery

1. Read from `MARKETING.md`. Only ask about things not covered there:
   - Business model (SaaS, ecommerce, services, marketplace)
   - Current MRR/ARR or revenue
   - Growth stage (pre-launch, early, growth, scale)
   - Current marketing spend (total and by channel, if known)
   - Target growth rate or revenue goal
   - Sales cycle length and average deal size
   - Current CAC and LTV (if known)
   - Team size (in-house marketers, agencies, contractors)
2. If user lacks metrics, estimate ranges based on industry benchmarks.
3. Identify which channels are currently active and their rough performance.

## Phase 2 — Analysis

### Unit Economics Model
1. Calculate or estimate:
   - **CAC** (Customer Acquisition Cost) — total spend / new customers
   - **LTV** (Lifetime Value) — ARPU x average lifespan
   - **LTV:CAC ratio** — target 3:1 or better
   - **Payback period** — months to recover CAC
   - **Gross margin** — to validate spend capacity
2. Benchmark against industry standards for their business model.
3. Flag any broken economics (LTV:CAC below 1:1, payback > 18 months).

### Channel Performance Audit
For each active channel, assess:
- Current spend
- Volume (leads, signups, purchases)
- CAC for that channel
- Trend direction (improving, stable, degrading)
- Saturation risk (diminishing returns at current spend)

## Phase 3 — Produce

Build these deliverables:

### Budget Allocation Model
- Total recommended monthly/quarterly marketing budget
- Percentage of revenue benchmark (stage-appropriate)
- Channel-by-channel allocation with rationale:

| Channel | Monthly Spend | Expected CAC | Expected Volume | Confidence |
|---------|--------------|-------------|-----------------|------------|
| [channel] | $X | $Y | Z leads | High/Med/Low |

### ROI Projections (3 scenarios)
- **Conservative**: 80% of target performance
- **Base case**: expected performance
- **Aggressive**: 120% of target with increased spend

Each scenario includes: spend, leads, customers, revenue, ROI, payback period.

### Spend Ramp Plan
- Month-by-month ramp schedule (don't dump budget all at once)
- Testing budget allocation (10-20% for experiments)
- Kill criteria: when to stop spending on a channel
- Scale criteria: when to increase spend on a channel

### Optimization Recommendations
- Channels to increase (high ROI, not saturated)
- Channels to decrease (poor CAC, saturated)
- Channels to test (untapped, stage-appropriate)
- Budget reserved for testing new channels

## Phase 4 — Output

1. Deliver the complete budget model as a structured document.
2. Include a one-page executive summary with:
   - Total recommended spend
   - Expected customer acquisition volume
   - Blended CAC target
   - Projected ROI
   - Top 3 risks and mitigations
3. Provide a quarterly review cadence recommendation.
4. Flag any assumptions that need validation with real data.

## Constraints

- Never recommend spending more than the user can sustain for 6 months.
- Always include a testing budget (10-20% of total).
- Stage-appropriate recommendations only — no enterprise tactics for pre-launch.
- All projections must include confidence levels (High/Medium/Low).
- CAC targets must be validated against LTV — never recommend unprofitable acquisition.
- Round budget numbers to practical amounts (not $4,731.28 — use $4,700 or $5,000).
