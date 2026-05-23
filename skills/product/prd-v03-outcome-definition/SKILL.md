---
name: prd-v03-outcome-definition
description: Define measurable success metrics (KPIs) tied to product type during PRD v0.3 Commercial Model. Triggers on requests to define success metrics, set KPI targets, determine what to measure, establish go/no-go thresholds, or when user asks "how do we measure success?", "what metrics matter?", "what's our target?", "how do we know if this works?", "define KPIs", "success criteria". Consumes Product Type Classification (BR-) from v0.2. Outputs KPI- entries with thresholds, evidence sources, and downstream gate linkages.
---

# Outcome Definition

Position in HORIZON workflow: v0.2 Product Type Classification → **v0.3 Outcome Definition** → v0.3 Pricing Model Selection

## Metric Quality Hierarchy

Not all metrics are equal. Use this tier system:

| Tier | Metric Types | Why It Matters |
|------|--------------|----------------|
| **Tier 1** | Revenue (MRR, first dollar, ACV), Churn (logo, NRR), LTV:CAC | Revenue validates market fit. "First dollar IS the proof." |
| **Tier 2** | Conversion rates (trial→paid, lead→customer), Time to Value, Activation | Leading indicators that predict Tier 1 outcomes |
| **Tier 3** | Engagement (DAU, sessions), Feature adoption, NPS | "Nice to know" — only track if tied to Tier 1/2 |

**Rule**: Every product needs at least one Tier 1 metric. Tier 3 metrics without Tier 1/2 correlation are vanity metrics.

## Product Type × Metric Selection

Metrics must align with product type from v0.2 classification:

| Product Type | Primary Metrics | Anti-Metrics (Avoid) |
|--------------|-----------------|----------------------|
| **Clone** | Feature parity score, Price delta vs. leader, TTFV vs. leader | Generic engagement (doesn't prove you beat leader) |
| **Undercut** | Price per [unit] vs. leader, Niche conversion rate, CAC in target segment | Broad market share (you're niche by design) |
| **Unbundle** | Category NPS vs. platform, Vertical retention, Feature depth usage | Platform-level metrics (irrelevant to your slice) |
| **Slice** | Marketplace ranking, Install→activate rate, Platform retention lift | TAM metrics (platform owns the market) |
| **Wrapper** | Time saved per workflow, API reliability, Integration adoption | Standalone usage (value is in connection) |
| **Innovation** | Education→activation conversion, Behavioral change rate, Reference customers | User counts without activation (people try, don't convert) |

## Leading vs. Lagging Framework

Every product needs BOTH:

**Leading Indicators** (actionable now, predict outcomes):
- Sequences sent, open rates, trial starts
- Time to first value, activation rate
- Feature adoption in first 7 days

**Lagging Indicators** (confirm strategy worked):
- MRR, churn rate, LTV:CAC
- Net Revenue Retention (NRR)
- Customer count, logo churn

**Pattern**: Track leading weekly, lagging monthly. If leading indicators fail, you can pivot before lagging indicators confirm disaster.

## Target-Setting Rules

Targets must be evidence-based, never arbitrary:

**Good targets** (use these approaches):
- Competitor benchmark × safety margin: "SMB churn benchmark 3-5% → use 5%"
- Revenue gates: "First dollar by Day 14" (Signal → $1: 14 days)
- Ratio thresholds: "LTV:CAC ≥ 3:1"
- Time bounds: "TTFV < 5 minutes for self-serve"

**Bad targets** (anti-patterns):
- Round numbers without evidence: "10% improvement"
- Engagement without revenue tie: "1000 DAU"
- Aspirational without baseline: "Best in class retention"

## Output Template

Create KPI- entries in this format:

```
KPI-XXX: [Metric Name]
Type: [Tier 1 | Tier 2 | Tier 3]
Category: [Leading | Lagging]
Definition: [Exact calculation formula]
Target: [Specific threshold with evidence source]
Evidence: [CFD-XXX or benchmark source]
Downstream Gate: [Which decision uses this — e.g., "v0.5 Red Team kill criteria"]
Measurement: [How/when measured — e.g., "Weekly via Mixpanel"]
```

**Example KPI- entry:**
```
KPI-001: Time to First Revenue
Type: Tier 1
Category: Lagging
Definition: Days from market signal identification to first paying customer
Target: ≤14 days (GearHeart standard: Signal → $1: 14 days)
Evidence: BR-001 (GearHeart methodology)
Downstream Gate: v0.5 Red Team — if not hit by Day 21, evaluate pivot
Measurement: Manual tracking in PRD changelog
```

## Anti-Patterns to Avoid

1. **Vanity metrics as primary**: "50K users" means nothing if only 500 pay
2. **Traffic without quality**: High volume + low engagement = quality problem
3. **Arbitrary targets**: "10% improvement" without baseline or benchmark
4. **All lagging, no leading**: Can't course-correct if you only see outcomes monthly
5. **Ignoring product type**: Clone metrics ≠ Innovation metrics
6. **Unmeasurable outcomes**: "Better experience" — how do you know?

## Downstream Connections

KPI- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.5 Red Team** | Kill thresholds | "If KPI-001 not hit by Day 21, pivot" |
| **v0.7 Build Execution** | EPIC acceptance criteria | "EPIC complete when KPI-002 validated" |
| **v0.9 GTM** | Launch dashboard | Track KPI-001, KPI-003 post-launch |
| **BR- Business Rules** | Derived constraints | "BR-XXX: No launch if LTV:CAC <3:1" |

## Detailed References

- **Good/bad examples**: See `references/examples.md`
- **Benchmark sources**: See `references/benchmarks.md`
- **KPI template worksheet**: See `assets/kpi.md`
