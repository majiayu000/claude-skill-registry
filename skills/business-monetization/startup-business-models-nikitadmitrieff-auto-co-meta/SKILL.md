---
name: startup-business-models
description: Use when choosing or evaluating a startup revenue model, pricing/value metric, packaging/tier design, or calculating unit economics (LTV, CAC, payback, gross margin, NRR), including usage-based/credit/AI pricing and variable compute/COGS constraints.
---

# Startup Business Models

Systematic workflow for choosing revenue models, pricing, and unit economics.

## Quick Start (Inputs)

Ask for the smallest set of inputs that makes the decision meaningful:

- Business type: SaaS, usage-based/API, marketplace, services, hardware + service
- ICP/segment(s): SMB / mid-market / enterprise (and ACV/ARPA bands)
- Current pricing and packaging: value metric, tiers, limits, discount policy, billing cadence
- Unit economics drivers: fully-loaded CAC, gross margin/COGS (include LLM/infra/third-party), churn/retention, expansion (NRR)
- Constraints: sales motion (PLG vs sales-led), implementation constraints (billing metering, proration), gross margin floor, payback target

If numbers are missing, proceed with ranges + explicit assumptions and highlight what to measure next.

## Workflow

1) Classify the model
- Subscription, usage-based, freemium, marketplace take-rate, transaction fee, ads, outcome-based, credit-based, hybrid.

2) Build a segment-level unit economics snapshot
- Use `references/unit-economics-calculator.md` for formulas, benchmarks, and common pitfalls.
- Prefer cohort/segment views over blended averages.

3) Evaluate model fit and risks
- Align price metric with value delivered and cost incurred (especially usage + AI compute).
- Identify failure modes: margin compression, adverse selection, channel conflict, support cost explosions, metering/overage friction.

4) Propose pricing + packaging changes
- Use `references/pricing-research-guide.md` for WTP methods and pricing interview scripts.
- Use `assets/pricing-tier-design.md` to draft tiers, limits, upgrade triggers, and enforcement rules.

5) Define measurement and roll-out
- Define success metric + guardrails, evaluation design, and explicit lag windows (conversion now, retention later).

6) Deliver a decision-ready output
- Recommendation, rationale, assumptions, scenarios (base/best/worst), and next experiments.

## 2026 Heuristics (Context-Dependent)

- Prioritize payback and gross margin over a single ratio; LTV:CAC is easiest to game.
- Typical SaaS targets (directional, by segment/stage): LTV:CAC 3-5x, payback 6-12 months (PLG) or 12-18 months (sales-led early), NRR >100% (mid-market/enterprise) and gross margin >70% (software-only).
- For usage-based / AI products: model contribution margin per unit (token/job/workflow) and set pricing guardrails (rate limits, minimums, commit tiers, credit expiries).

## Related Skills (Routing)

- [startup-idea-validation](../startup-idea-validation/)
- [startup-competitive-analysis](../startup-competitive-analysis/)
- [startup-fundraising](../startup-fundraising/)
- [startup-go-to-market](../startup-go-to-market/)

## Pricing Change Measurement & Experiment Design
Use this when you are changing pricing, packaging, value metric, limits, discounts, or billing cadence.

### 1) Define success and guardrails (before launch)
| Type | Examples |
|------|----------|
| Primary success metric | Net revenue retention (NRR), ARPA/ARPU, gross margin %, payback period, upgrade rate, expansion MRR |
| Guardrails | New logo conversion, activation rate, refund rate, support load, churn (logo + revenue), sales cycle length |

### 2) Pick an evaluation design
| Design | Best when | How to read results |
|--------|-----------|---------------------|
| A/B (randomized) | Self-serve / PLG flows | Compare conversion, ARPA, refunds, and downstream retention by assignment |
| Holdout/control cohort | Pricing is hard to randomize | Compare treated vs. holdout cohorts matched on segment, channel, and start month |
| Step rollout (time-based) | Enterprise contracts, invoicing cycles | Compare pre/post with a parallel cohort (not exposed yet) to reduce seasonality bias |
| Geo/account rollout | Regions/segments are separable | Compare regions/segments; watch for channel mix shifts |

### 3) Use explicit lag windows (avoid premature conclusions)
- Short lag (days to 2 weeks): checkout conversion, activation, sales cycle friction, refund/support spikes.
- Medium lag (4 to 8 weeks): upgrades, expansion MRR, usage growth, discounting behavior, proration effects.
- Long lag (90 to 180+ days, B2B): churn, net revenue retention, renewal outcomes, contraction risk.

### 4) Report an "all-in" view (not just conversion)
- Revenue quality: net revenue after refunds, discounts, and credits; gross margin impact (including variable compute/COGS).
- Segments: break down by plan, seat band, channel, ACV/ARR band, and customer age (new vs. renewal).
- Decision rule: write a go/no-go threshold (example: "NRR +2pts with no >0.5pt drop in activation and no >10% increase in support load").

## SaaS Metrics (Read When Needed)

Use `references/saas-metrics-playbook.md` for definitions and templates (MRR/ARR, churn, NRR, Quick Ratio, Magic Number, burn multiple, stage focus).

## Resources

| Resource | Purpose |
|----------|---------|
| [unit-economics-calculator.md](references/unit-economics-calculator.md) | LTV, CAC, payback calculations |
| [pricing-research-guide.md](references/pricing-research-guide.md) | WTP research methodology |
| [saas-metrics-playbook.md](references/saas-metrics-playbook.md) | SaaS-specific metrics deep dive |

## Templates

| Template | Purpose |
|----------|---------|
| [business-model-canvas.md](assets/business-model-canvas.md) | Full model design |
| [unit-economics-worksheet.md](assets/unit-economics-worksheet.md) | Calculate and track metrics |
| [pricing-tier-design.md](assets/pricing-tier-design.md) | Pricing & packaging worksheet |

## Data

| File | Purpose |
|------|---------|
| [sources.json](data/sources.json) | Business model resources |

---

## Do / Avoid (Jan 2026)

### Do

- Define your value metric (seat/usage/outcome) and validate willingness-to-pay early.
- Include COGS drivers in pricing decisions (especially usage-based).
- Use discount guardrails and renewal logic (avoid ad-hoc deals).

### Avoid

- Pricing as an afterthought (“we’ll figure it out later”).
- Margin blindness (shipping usage growth that destroys gross margin).
- Misleading LTV calculations from immature cohorts.

## What Good Looks Like

- Packaging: a clear value metric, tier logic, and discount policy (with enforcement rules).
- Unit economics: CAC, gross margin, churn, payback, and retention defined and tied to cohorts.
- Assumptions: one inputs sheet, ranges/sensitivities, and scenarios (base/best/worst).
- Experiments: pricing changes tested with decision rules (not “gut feel” rollouts).
- Risks: margin compression, adverse selection, channel conflict, and support cost modeled.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Summarize pricing research and competitor snapshots; verify manually before acting.
- Draft pricing page copy; humans verify claims and consistency with contracts.
