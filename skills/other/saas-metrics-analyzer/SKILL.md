---
name: saas-metrics-analyzer
description: Analyze SaaS business health across all critical metrics (MRR, ARR, churn, LTV:CAC, NRR, ARPU, growth rate) with benchmarks and actionable recommendations. Use for monthly business reviews, health checks, or diagnosing growth problems.
category: business
license: MIT
---

# When to Use This Skill

Use this skill when you need to:

- **Run monthly business health checks** to track progress
- **Benchmark metrics** against relevant peer ranges for your segment
- **Diagnose growth problems** (stuck at plateau, high churn, poor unit
  economics)
- **Calculate missing metrics** from partial data
- **Identify red flags** requiring immediate attention
- **Get actionable recommendations** for metric improvement
- **Prepare for fundraising or acquisition** (know your numbers)

# Core Concepts

## The 5 Metric Categories

1. **Revenue Health** (25% weight): MRR, ARR, ARPU
2. **Unit Economics** (25% weight): LTV, CAC, LTV:CAC, payback period
3. **Retention Health** (25% weight): Monthly/annual churn, NRR
4. **Efficiency** (15% weight): Gross margin, profit margin
5. **Growth** (10% weight): MoM growth, viral coefficient

## Quick Health Assessment

| Score  | Rating    | Interpretation                          |
| ------ | --------- | --------------------------------------- |
| 90-100 | Excellent | Best-in-class across most metrics       |
| 70-89  | Healthy   | Solid business, room for optimization   |
| 50-69  | Warning   | Some red flags, needs attention         |
| <50    | Critical  | Major issues, immediate action required |

# Step-by-Step Analysis Process

## Step 1: Gather Your Metrics

Collect any of these you have available:

- Monthly Recurring Revenue (MRR)
- Customer count
- Monthly churn rate
- Customer Acquisition Cost (CAC)
- Average Revenue Per User (ARPU)
- Gross margin percentage

## Step 2: Calculate Missing Metrics

**ARPU** (if you have MRR and customers):

```
ARPU = MRR ÷ Total customers
```

**LTV** (if you have ARPU, margin, churn):

```
LTV = (ARPU × Gross Margin %) ÷ Monthly churn rate
```

**LTV:CAC** (if you have LTV and CAC):

```
LTV:CAC = LTV ÷ CAC
```

**CAC Payback** (if you have CAC, ARPU, margin):

```
Payback = CAC ÷ (ARPU × Gross Margin %)
```

**Annual churn** (if you have monthly; use monthly churn as decimal):

```
Annual = (1 - (1 - Monthly)^12) × 100
```

## Step 3: Benchmark Against Peer Ranges

Use the benchmark ranges below as directional guidance, not universal truth.
Segment (SMB vs enterprise), price point, geography, and channel mix all matter.

## Step 4: Identify Red Flags and Strengths

Flag metrics outside healthy ranges and highlight areas of strength.

## Step 5: Generate Recommendations

Prioritize actions by impact: churn → pricing → acquisition → operations.

---

# Metric Deep Dives

## Revenue Metrics

### Monthly Recurring Revenue (MRR)

**What it measures**: Predictable monthly revenue from subscriptions

**Benchmarks** (directional for subscription SaaS):

| Stage          | MRR Range   | Timeline    |
| -------------- | ----------- | ----------- |
| Early stage    | $1K-$3K     | 0-6 months  |
| Growth stage   | $3K-$15K    | 6-18 months |
| Sustainable    | $10K+       | 18+ months  |
| Top performers | $30K-$100K+ | Varies      |

**Red flags**:

- ❌ Below $1K MRR after 6 months (possible PMF or distribution issues)
- ❌ Stuck at $3K-$5K for 3+ months (growth plateau)
- ❌ Declining for 2+ consecutive months

**Strengths**:

- ✅ Reaching $10K MRR in <18 months
- ✅ Consistent month-over-month growth

---

### Average Revenue Per User (ARPU)

**What it measures**: Average monthly revenue per customer

**Benchmarks** (segment-sensitive):

| Range          | Assessment                                          |
| -------------- | --------------------------------------------------- |
| <$30/month     | Low-ticket model; requires strong volume/efficiency |
| $30-$300/month | Common SMB SaaS pricing band                        |
| $300+/month    | Higher-ACV model (often more sales/support)         |

**Red flags**:

- ❌ ARPU low relative to CAC and support burden
- ❌ ARPU declining over time

**Improvement levers**:

- Introduce tiered packaging and pricing
- Add annual payment discounts
- Implement usage-based pricing
- Raise prices on new customers first

**Related skill**: `pricing-strategy-designer`

---

## Unit Economics

### Customer Acquisition Cost (CAC)

**What it measures**: Cost to acquire one new customer

**Benchmarks** (highly channel-dependent):

| CAC Range   | Assessment                              |
| ----------- | --------------------------------------- |
| <$200       | Efficient for many SMB/self-serve       |
| $200-$500   | Common in mixed inbound/outbound models |
| $500-$1,000 | Requires stronger payback economics     |
| >$1,000     | Often risky without high ACV/margins    |

**Formula**:

```
CAC = (Sales + Marketing costs) ÷ New customers acquired
```

**Red flags**:

- ❌ CAC rising while ARPU and retention are flat
- ❌ CAC rising over time
- ❌ CAC > LTV × 0.33

**Improvement levers**:

- Focus on community-led growth
- Implement product-led growth
- Optimize onboarding conversion
- Build SEO/content for organic traffic

---

### Customer Lifetime Value (LTV)

**What it measures**: Total revenue from average customer

**Formula**:

```
LTV = (ARPU × Gross Margin %) ÷ Monthly churn rate
```

**Benchmarks** (LTV:CAC ratio, directional):

| Ratio   | Assessment                                     |
| ------- | ---------------------------------------------- |
| <1:1    | Unsustainable                                  |
| 1:1-3:1 | Needs improvement for most SaaS models         |
| 3:1-5:1 | Common target range                            |
| >5:1    | Strong economics (or possible under-investing) |

**Red flags**:

- ❌ LTV:CAC persistently below ~3:1
- ❌ LTV <$500
- ❌ LTV declining over time

**Improvement levers**:

- Reduce churn (biggest lever)
- Increase ARPU through pricing
- Improve onboarding
- Add expansion revenue

---

### CAC Payback Period

**What it measures**: Months to recover acquisition cost

**Benchmarks** (stage-dependent):

| Months | Assessment                                    |
| ------ | --------------------------------------------- |
| <6     | Very efficient                                |
| 6-12   | Healthy for many self-serve products          |
| 12-18  | Often acceptable for sales-assisted SaaS      |
| >18    | Usually a warning sign (unless very high ACV) |

---

## Retention Metrics

### Monthly Churn Rate

**What it measures**: Percentage of customers canceling each month

**Benchmarks** (segment-sensitive):

| Rate | Assessment               |
| ---- | ------------------------ |
| <2%  | Strong for many B2B SaaS |
| 2-5% | Common SMB range         |
| >5%  | Warning zone             |

**Formula**:

```
Monthly Churn = (Customers lost ÷ Total customers) × 100
```

**Red flags**:

- ❌ Monthly churn >5%
- ❌ Churn increasing over time
- ❌ Early customers churning fast

**Improvement tactics**:

- Improve onboarding and shorten time-to-value
- Implement customer success
- Build in-product stickiness
- Exit surveys to identify causes

**Related skill**: `customer-retention-optimizer`

---

### Net Revenue Retention (NRR)

**What it measures**: Revenue retention including expansion

**Formula**:

```
NRR = ((Starting MRR + Expansion - Churn - Downgrades) ÷ Starting MRR) × 100
```

**Benchmarks** (directional):

| NRR      | Assessment                     |
| -------- | ------------------------------ |
| <90%     | Significant contraction        |
| 90-100%  | Net contraction                |
| 100-110% | Healthy to strong              |
| 110-120% | Excellent                      |
| 120%+    | Exceptional (often enterprise) |

**Red flags**:

- ❌ NRR <100%
- ❌ NRR declining

**Improvement tactics**:

- Implement expansion strategies
- Use tiered pricing to encourage upgrades
- Build usage-based pricing
- Proactive customer success

---

For efficiency metrics (gross/profit margin), growth metrics (MoM, K-factor),
and a sample analysis walkthrough, see
[references/metric-benchmarks.md](references/metric-benchmarks.md).

---

# Common Mistakes

**Mistake 1: Ignoring Churn**

- **Problem**: Churn compounds - 5% monthly = 46% annually
- **Solution**: Measure weekly, then improve onboarding, fit, and lifecycle
  engagement before pushing harder on acquisition

**Mistake 2: Vanity Metrics**

- **Problem**: Tracking signups instead of revenue metrics
- **Solution**: Focus on MRR, churn, LTV:CAC

**Mistake 3: Outdated Benchmarks**

- **Problem**: Using generic benchmarks without segment context
- **Solution**: Compare against peers by model, stage, and ACV; many teams use
  3:1-5:1 as a working LTV:CAC band

**Mistake 4: Measuring Infrequently**

- **Problem**: Quarterly reviews miss trends
- **Solution**: Weekly metrics review, monthly deep analysis

---

## Next Steps

After running your metrics checkup:

1. **Address red flags first** - Focus on critical metrics
2. **Use related skills** - Deep-dive into problem areas
3. **Track monthly** - Re-run this analysis every month
4. **Celebrate strengths** - Don't fix what isn't broken

**Recommended skills by problem area**:

- Churn issues → `customer-retention-optimizer`
- Pricing issues → `pricing-strategy-designer`
- Acquisition issues → `community-growth-specialist`
- Operations issues → `solo-operations-manager`

---

## Sources

- [SaaS Benchmarks Report | OpenView](https://openviewpartners.com/saas-benchmarks/)
- [State of the Cloud 2024 | Bessemer Venture Partners](https://www.bvp.com/atlas/state-of-the-cloud-2024)
- [SaaS Metrics: What to Track and Why | Paddle](https://www.paddle.com/resources/saas-metrics)
- [Net MRR Retention | ChartMogul Help](https://help.chartmogul.com/article/163-net-mrr-retention)
- [Churn Rate Benchmarks 2025 | Recurly Research](https://www.recurly.com/research/churn-rate-benchmarks/)
