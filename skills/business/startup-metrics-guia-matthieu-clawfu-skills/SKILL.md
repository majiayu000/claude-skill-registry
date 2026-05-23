---
name: startup-metrics
description: "Know the metrics that matter at each stage and what investors actually look for. Master the A16Z and YC frameworks for measuring startup progress. Use when: **Fundraising prep** to know which metrics to highlight; **Board meetings** to report on the right KPIs; **Strategic planning** to set goals that matter; **Product decisions** to understand what to optimize; **Diagnosing problems** to find what's broken"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Startup Metrics

> Know the metrics that matter at each stage and what investors actually look for. Master the A16Z and YC frameworks for measuring startup progress.

## When to Use This Skill

- **Fundraising prep** to know which metrics to highlight
- **Board meetings** to report on the right KPIs
- **Strategic planning** to set goals that matter
- **Product decisions** to understand what to optimize
- **Diagnosing problems** to find what's broken
- **Benchmarking** to know if your metrics are good

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | A16Z (Andreessen Horowitz), YC (Y Combinator), SaaS metrics best practices |
| **Core Principle** | "Measure what matters. Vanity metrics feel good but don't predict success. Focus on metrics that indicate real product-market fit and sustainable growth." |
| **Why This Matters** | Wrong metrics lead to wrong decisions. Right metrics reveal truth about your business—good or bad—before it's too late to course-correct. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Strategic priorities |
| Synthesizes market data | Competitive positioning |
| Identifies opportunities | Resource allocation |
| Creates strategic options | Final strategy selection |
| Suggests implementation approaches | Execution decisions |

## What This Skill Does

1. **Identifies key metrics by stage** - What to measure when
2. **Calculates core SaaS metrics** - ARR, MRR, churn, LTV, CAC
3. **Benchmarks performance** - Good vs. great vs. concerning
4. **Diagnoses metric problems** - What poor metrics indicate
5. **Prepares investor-ready dashboards** - What VCs want to see
6. **Prioritizes metric improvement** - What to fix first

## How to Use

### Get Stage-Appropriate Metrics
```
I'm a [stage] startup in [industry].
What metrics should I be tracking?
What benchmarks should I aim for?
```

### Calculate Core Metrics
```
Help me calculate my SaaS metrics:
[Provide: MRR, customer count, churn data, acquisition costs]
```

### Diagnose Metric Problems
```
My metrics: [list metrics]
What's concerning? What should I focus on fixing?
```

## Instructions

### Step 1: Understand Metrics by Stage

```
## Metrics Framework by Stage

### Pre-Seed (Validation Stage)
**Focus:** Is this a real problem worth solving?

| Metric | Why It Matters | Good Signal |
|--------|---------------|-------------|
| Problem interviews | Validate problem exists | 10+ interviews, 70%+ confirm |
| Solution interviews | Validate solution fits | 60%+ would use |
| LOIs/Waitlist | Real interest signal | Signed commitments |
| Engagement (if prototype) | People want to use it | Daily active usage |

**Not important yet:** Revenue, CAC, LTV, growth rate

---

### Seed (Product-Market Fit Stage)
**Focus:** Do people want this? Will they pay?

| Metric | Why It Matters | Good Signal |
|--------|---------------|-------------|
| **MRR/ARR** | Revenue traction | Any consistent revenue |
| **MoM Growth** | Trajectory | 15-20%+ MoM |
| **Retention** | PMF indicator | >80% monthly retention |
| **NPS** | Customer love | >50 NPS |
| **Engagement** | Product usage | DAU/MAU >20% |

**Emerging importance:** Early unit economics, CAC/LTV ratio

---

### Series A (Scale Stage)
**Focus:** Can this scale? Are unit economics viable?

| Metric | Why It Matters | Good Signal |
|--------|---------------|-------------|
| **ARR** | Revenue scale | $1-2M+ |
| **ARR Growth** | YoY trajectory | 3x YoY |
| **Net Revenue Retention** | Expansion + churn | >100% (ideally >120%) |
| **LTV/CAC** | Unit economics | >3:1 |
| **CAC Payback** | Efficiency | <18 months |
| **Gross Margin** | Business viability | >70% (SaaS) |

---

### Series B+ (Optimization Stage)
**Focus:** Efficiency and path to profitability

| Metric | Why It Matters | Good Signal |
|--------|---------------|-------------|
| **Magic Number** | Sales efficiency | >0.75 |
| **Rule of 40** | Growth + profitability | >40% |
| **Burn Multiple** | Cash efficiency | <2x |
| **Net Dollar Retention** | Account growth | >120% |
| **Quick Ratio** | Growth quality | >4 |
```

---

### Step 2: Calculate Core SaaS Metrics

```
## Metric Calculations

### Revenue Metrics

**MRR (Monthly Recurring Revenue):**
MRR = Sum of all recurring revenue per month

**ARR (Annual Recurring Revenue):**
ARR = MRR × 12

**MRR Components:**
- New MRR: Revenue from new customers
- Expansion MRR: Upgrades and cross-sells
- Contraction MRR: Downgrades
- Churned MRR: Lost customers

**Net New MRR:**
Net New MRR = New + Expansion - Contraction - Churned

---

### Growth Metrics

**MoM Growth Rate:**
Growth = (MRR this month - MRR last month) / MRR last month × 100

**YoY Growth Rate:**
YoY = (ARR this year - ARR last year) / ARR last year × 100

**CMGR (Compound Monthly Growth Rate):**
CMGR = (Ending MRR / Starting MRR)^(1/months) - 1

---

### Retention Metrics

**Gross Revenue Retention (GRR):**
GRR = (MRR - Churned MRR - Contraction MRR) / MRR × 100
Maximum: 100% (doesn't include expansion)

**Net Revenue Retention (NRR) / Net Dollar Retention (NDR):**
NRR = (MRR + Expansion - Contraction - Churned) / MRR × 100
Can be >100% (good!)

**Logo Churn:**
Logo Churn = Customers lost / Customers at start of period × 100

**Revenue Churn:**
Revenue Churn = Churned MRR / MRR at start of period × 100

---

### Unit Economics

**Customer Acquisition Cost (CAC):**
CAC = Total Sales & Marketing Spend / New Customers Acquired

**Lifetime Value (LTV):**
Simple: LTV = ARPU × Gross Margin × Customer Lifetime
With churn: LTV = (ARPU × Gross Margin) / Monthly Churn Rate

**LTV/CAC Ratio:**
LTV/CAC = LTV / CAC
Good: >3:1

**CAC Payback Period:**
Payback = CAC / (ARPU × Gross Margin)
Good: <18 months

---

### Efficiency Metrics

**Magic Number:**
Magic Number = Net New ARR this quarter / S&M Spend last quarter
>1.0 = Very efficient
0.75-1.0 = Good
<0.5 = Inefficient

**Rule of 40:**
Rule of 40 = Revenue Growth Rate + Profit Margin
>40% = Healthy balance of growth and profitability

**Burn Multiple:**
Burn Multiple = Net Burn / Net New ARR
<1x = Excellent
1-2x = Good
>2x = Concerning

**Quick Ratio:**
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
>4 = Excellent growth quality
```

---

### Step 3: Benchmark Against Standards

```
## Metric Benchmarks

### SaaS Benchmarks by Stage

| Metric | Seed | Series A | Series B |
|--------|------|----------|----------|
| ARR | <$1M | $1-5M | $5-15M |
| MoM Growth | 15-25% | 10-15% | 5-10% |
| YoY Growth | 3x+ | 2-3x | 1.5-2x |
| Gross Margin | >60% | >70% | >75% |
| LTV/CAC | >3x | >3x | >4x |
| CAC Payback | <24 mo | <18 mo | <12 mo |
| NRR | >100% | >110% | >120% |
| Logo Churn | <5%/mo | <3%/mo | <2%/mo |

### What "Good" Looks Like by Company Type

**SMB SaaS (low touch):**
- Logo churn: 3-5% monthly
- NRR: 80-100%
- LTV/CAC: >3x
- CAC: <$1,000

**Mid-Market SaaS:**
- Logo churn: 1-2% monthly
- NRR: 100-120%
- LTV/CAC: >4x
- CAC: $5,000-20,000

**Enterprise SaaS:**
- Logo churn: <1% monthly
- NRR: 110-150%
- LTV/CAC: >5x
- CAC: $20,000-100,000+

### Engagement Benchmarks

| Metric | Consumer | B2B SaaS |
|--------|----------|----------|
| DAU/MAU | >20% | >40% |
| D1 Retention | >40% | >50% |
| D7 Retention | >20% | >30% |
| D30 Retention | >10% | >20% |
```

---

### Step 4: Diagnose Problems

```
## Metric Diagnosis Guide

### If MRR Growth is Slowing...

**Possible causes:**
1. Market saturation (ran out of easy customers)
2. Product-market fit weakening (competition, changing needs)
3. Sales inefficiency (declining magic number)
4. High churn eating new growth

**Diagnostic questions:**
- Is logo churn increasing?
- Is CAC increasing?
- Is conversion rate declining?
- Is expansion revenue flat?

---

### If Churn is High...

**Possible causes:**
1. Onboarding problems (never got value)
2. Product gaps (missing critical features)
3. Wrong customers (sold to people who shouldn't buy)
4. Competition (better alternatives emerged)
5. Pricing mismatch (not worth it)

**Diagnostic questions:**
- When do customers churn? (early = onboarding, late = value)
- What's the churn reason? (survey departures)
- Which segments churn most?
- What's usage pattern before churn?

---

### If CAC is Too High...

**Possible causes:**
1. Wrong channel (expensive acquisition)
2. Poor targeting (low conversion)
3. Weak positioning (hard to differentiate)
4. Long sales cycles (expensive process)
5. Market competition (bidding up costs)

**Diagnostic questions:**
- What's CAC by channel?
- What's conversion rate at each stage?
- How long is sales cycle?
- What's win rate vs. competition?

---

### If LTV is Too Low...

**Possible causes:**
1. High churn (short lifetime)
2. Low ARPU (underpriced or wrong segment)
3. No expansion revenue (no upsell path)
4. Low gross margin (cost too high)

**Diagnostic questions:**
- What's average customer lifespan?
- What's ARPU distribution?
- What's expansion revenue %?
- Are costs scaling with revenue?

---

### Quick Diagnostic Table

| Symptom | Primary Metric | Secondary Checks |
|---------|---------------|------------------|
| Revenue plateau | MRR growth rate | New vs. expansion breakdown |
| Customers leaving | Churn rate | Cohort analysis, exit surveys |
| Expensive growth | CAC, Magic Number | Channel efficiency, conversion |
| Low profitability | Gross margin | COGS breakdown, pricing |
| "Leaky bucket" | Quick Ratio | Churn + expansion balance |
```

---

### Step 5: Create Investor Dashboard

```
## Investor Metrics Dashboard

### What Investors Want to See (by stage)

**Seed Deck Metrics:**
- MRR and growth trajectory
- Customer count and retention
- Engagement metrics
- Early unit economics (if available)

**Series A Deck Metrics:**
- ARR and YoY growth
- Net Revenue Retention
- LTV/CAC ratio
- CAC Payback
- Cohort analysis
- Customer breakdown by segment

**Series B+ Deck Metrics:**
All of above plus:
- Magic Number
- Rule of 40
- Burn Multiple
- Detailed unit economics by segment
- Efficiency trends over time

### Dashboard Template

```
## [Company] Metrics Dashboard
### As of [Date]

### Revenue
- ARR: $[X]
- MRR: $[X]
- MoM Growth: [X]%
- YoY Growth: [X]%

### Customers
- Total Customers: [X]
- New This Month: [X]
- Churned This Month: [X]
- Logo Churn Rate: [X]%

### Retention
- Gross Revenue Retention: [X]%
- Net Revenue Retention: [X]%
- Average Customer Lifespan: [X] months

### Unit Economics
- ARPU: $[X]
- CAC: $[X]
- LTV: $[X]
- LTV/CAC: [X]:1
- Payback: [X] months

### Efficiency
- Gross Margin: [X]%
- Magic Number: [X]
- Burn Multiple: [X]

### Engagement
- DAU: [X]
- DAU/MAU: [X]%
- Feature adoption: [X]%
```
```

---

## Examples

### Example 1: Seed Stage Metrics Analysis

**Input:**
> "I'm raising Seed. Here are my metrics. How do they look?"
> MRR: $15K, 6 months old, 40 customers
> MoM growth: 20% average
> Churn: 5% monthly
> CAC: $200

**Output:**

## Metrics Analysis: Seed Stage

### Current State

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| MRR | $15K | - | Early but positive |
| MoM Growth | 20% | 15-25% | ✅ Good |
| Customer Count | 40 | - | Reasonable for stage |
| Monthly Churn | 5% | <5% | ⚠️ At threshold |
| CAC | $200 | <$500 SMB | ✅ Efficient |

### Calculated Metrics

**ARPU:** $15,000 / 40 = $375/month

**Implied LTV (simple):**
- Customer lifespan: 1 / 0.05 = 20 months
- LTV = $375 × 20 = $7,500

**LTV/CAC:** $7,500 / $200 = 37.5:1 ✅ Excellent

**CAC Payback:** $200 / $375 = 0.5 months ✅ Excellent

### Analysis

**Strengths:**
- Growth rate is healthy (20% MoM = 8.9x annual)
- CAC is very efficient
- LTV/CAC is strong (though churn may be early-stage noise)

**Concerns:**
- 5% monthly churn = 60% annual churn (high for SaaS)
- Small sample size (40 customers)
- Need to see cohort retention to understand true churn

**Questions to Answer:**
1. Is 5% churn consistent across cohorts or improving?
2. What's the activation rate? (Are churners ever getting value?)
3. What's usage pattern of retained customers?

### Investor Readiness

**For Seed, you need to show:**
- ✅ Growth trajectory (20% MoM is good)
- ✅ Efficient acquisition
- ⚠️ Retention story (need cohort data)
- ❓ Path to scale

**Recommendation:**
- Highlight growth and CAC efficiency
- Show cohort data if recent cohorts retain better
- Explain what you're doing to improve retention
- Project what metrics look like with improved retention

### Projected Growth

| Metric | Now | +6 months (at 20% MoM) | +12 months |
|--------|-----|------------------------|------------|
| MRR | $15K | $45K | $133K |
| ARR | $180K | $540K | $1.6M |
| Customers | 40 | ~100 | ~250 |

---

### Example 2: Diagnose Declining Growth

**Input:**
> "My MoM growth dropped from 25% to 8% over 4 months. What's happening?"

**Output:**

## Growth Decline Diagnosis

### Data Needed

| Metric | 4 months ago | Now | Change |
|--------|--------------|-----|--------|
| New MRR | ? | ? | |
| Expansion MRR | ? | ? | |
| Churned MRR | ? | ? | |
| Logo Churn | ? | ? | |
| New Customers | ? | ? | |
| Sales Pipeline | ? | ? | |
| CAC | ? | ? | |
| Conversion Rate | ? | ? | |

### Diagnostic Framework

**Question 1: Is this a LEAKY BUCKET problem?**
- Are you acquiring the same # of customers but losing more?
- Check: New MRR vs. Churned MRR

**Question 2: Is this an ACQUISITION problem?**
- Are you getting fewer new customers?
- Check: New customer count, pipeline, conversion rate

**Question 3: Is this an EXPANSION problem?**
- Has expansion revenue slowed?
- Check: Expansion MRR trend, upsell rate

### Common Scenarios

**Scenario A: Churn increased**
Symptoms: New MRR stable, but churned MRR grew
Causes: Product issues, wrong customers, competition
Fix: Churn analysis, customer success, product fixes

**Scenario B: New acquisition slowed**
Symptoms: Churned MRR stable, but new MRR decreased
Causes: Market saturation, CAC increased, marketing efficiency dropped
Fix: New channels, positioning, sales optimization

**Scenario C: Expansion stalled**
Symptoms: New + churn stable, but expansion dropped
Causes: Product limits hit, no upsell path, customer saturation
Fix: New features, pricing tiers, account management

**Scenario D: Multiple factors**
Often it's a combination—growth hides problems until it slows

### Investigation Checklist

```
□ Break down MRR: New, Expansion, Contraction, Churned
□ Compare ratios: Quick Ratio trend
□ Cohort analysis: Are newer cohorts worse?
□ Channel breakdown: Which channels slowed?
□ Segment analysis: Which customer type slowed?
□ Funnel metrics: Where is conversion dropping?
□ Win/loss analysis: Why are deals not closing?
□ Churn interviews: Why are customers leaving?
```

### Next Steps

1. **Get the data breakdown** (above table)
2. **Identify primary driver** (acquisition, churn, or expansion)
3. **Root cause analysis** on that driver
4. **Hypothesis and test** solutions
5. **Monitor leading indicators** weekly

---

### Example 3: Series A Readiness Check

**Input:**
> "Am I ready for Series A? ARR: $1.2M, NRR: 108%, LTV/CAC: 4.5x, YoY growth: 180%"

**Output:**

## Series A Readiness Assessment

### Metrics Scorecard

| Metric | Your Value | Series A Bar | Status |
|--------|------------|--------------|--------|
| ARR | $1.2M | $1-2M | ✅ Pass |
| YoY Growth | 180% | 100-200% | ✅ Strong |
| NRR | 108% | >100% | ✅ Pass |
| LTV/CAC | 4.5x | >3x | ✅ Strong |

### What You Have

✅ **Revenue scale:** $1.2M ARR is at the low end of Series A but acceptable with strong growth
✅ **Growth rate:** 180% YoY is excellent (shows demand)
✅ **Retention:** 108% NRR means customers expand (PMF signal)
✅ **Unit economics:** 4.5x LTV/CAC is healthy

### What Investors Will Ask

**You'll need answers to:**

1. **CAC Payback?** (Need to calculate)
2. **Gross Margin?** (Should be >70% for SaaS)
3. **Logo vs. Revenue Churn?** (Both matter)
4. **Cohort data?** (Do later cohorts retain better?)
5. **Segmentation?** (Which customer type is best?)
6. **Magic Number?** (Sales efficiency)
7. **Path to $10M ARR?** (How do you 8x?)

### Additional Metrics Needed

| Metric | Required | Nice to Have |
|--------|----------|--------------|
| CAC Payback | ✅ Yes | |
| Gross Margin | ✅ Yes | |
| MoM Growth Trend | ✅ Yes | |
| Customer Count | ✅ Yes | |
| Cohort Retention | ✅ Yes | |
| Magic Number | | ✅ |
| Burn Multiple | | ✅ |
| ACV Distribution | | ✅ |

### Series A Narrative

**Based on your metrics, your story is:**

"We've found product-market fit in [segment].
$1.2M ARR growing 180% YoY with 108% NRR proves customers want this and expand.
Our 4.5x LTV/CAC shows we can acquire customers profitably.
With Series A, we'll [go-to-market strategy] to reach $5M ARR in 18 months."

### Recommendations

1. **Strengthen weak spots** before raising:
   - Calculate and optimize CAC Payback
   - Document gross margin
   - Build cohort analysis

2. **Prepare growth story:**
   - What drives growth? (channels, segments)
   - Why will this continue?
   - What does $10M ARR look like?

3. **Document efficiency:**
   - Magic Number (if positive)
   - Burn Multiple (if reasonable)

**Verdict:** You're in the range for Series A. Focus on the narrative and missing metrics before starting outreach.

---

## Checklists & Templates

### Metrics Tracking Checklist

```
## Monthly Metrics Review

### Revenue
□ MRR calculated (New + Expansion - Contraction - Churned)
□ ARR updated
□ MoM growth rate
□ YoY comparison (if applicable)

### Customers
□ Customer count
□ New customers
□ Churned customers
□ Logo churn rate

### Retention
□ Gross Revenue Retention
□ Net Revenue Retention
□ Cohort retention updated

### Unit Economics
□ CAC (by channel if possible)
□ LTV updated
□ LTV/CAC ratio
□ Payback period

### Engagement
□ DAU/MAU
□ Feature adoption
□ Key usage metrics

### Efficiency (Series A+)
□ Magic Number
□ Burn Multiple
□ Rule of 40
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring strategic analysis
- Identifying market opportunities
- Creating strategic frameworks
- Synthesizing competitive data

### What This Skill Cannot Do
- Replace market research
- Guarantee strategic success
- Know proprietary competitor info
- Make executive decisions

## References

- A16Z. "16 Startup Metrics" (Andreessen Horowitz)
- YC. "Startup Metrics That Matter" (Y Combinator)
- Tunguz, Tomasz. "SaaS Metrics" (Redpoint Ventures)
- Reforge. "Retention Curves" & "Growth Accounting"
- OpenView Partners. "SaaS Benchmarks"

## Related Skills

- [yc-pitch-deck](../yc-pitch-deck/) - Present metrics to investors
- [lean-canvas](../../validation/lean-canvas/) - Business model context
- [pricing-strategy](../../strategy/pricing-strategy/) - ARPU optimization
- [first-principles](../../strategy/first-principles/) - Challenge metric assumptions

---

## Skill Metadata


- **Mode**: centaur
```yaml
name: startup-metrics
category: startup
subcategory: measurement
version: 1.0
author: MKTG Skills
source_expert: A16Z, YC, SaaS Metrics Community
source_work: 16 Startup Metrics, YC Library
difficulty: intermediate
estimated_value: $5,000 financial modeling consulting
tags: [metrics, SaaS, startup, fundraising, KPIs, A16Z, YC]
created: 2026-01-25
updated: 2026-01-25
```
