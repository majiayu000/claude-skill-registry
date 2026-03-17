---
name: startup-metrics
model: fast
version: 1.0.0
description: >
  Track, calculate, and optimize key performance metrics for startups from seed
  through Series A. Covers unit economics, growth efficiency, and business models.
tags: [startup, metrics, saas, kpis, unit-economics, growth, fundraising]
---

# Startup Metrics Framework

Comprehensive guide to tracking, calculating, and optimizing key performance metrics for different startup business models from seed through Series A.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install startup-metrics
```


## WHAT This Skill Does

Provides formulas, benchmarks, and guidance for:
- Revenue metrics (MRR, ARR, growth rates)
- Unit economics (CAC, LTV, payback period)
- Cash efficiency (burn rate, runway, burn multiple)
- SaaS-specific metrics (NDR, magic number, Rule of 40)
- Marketplace and consumer metrics
- Stage-appropriate focus areas

## WHEN To Use

- Setting up startup analytics and dashboards
- Calculating CAC, LTV, or unit economics
- Preparing investor updates or pitch materials
- Evaluating business health and efficiency
- Understanding what metrics matter at each stage

## KEYWORDS

startup metrics, saas metrics, cac, ltv, arr, mrr, burn rate, burn multiple, rule of 40, net dollar retention, magic number, unit economics, marketplace gmv, dau mau

## Universal Startup Metrics

### Revenue Metrics

```
MRR = Σ (Active Subscriptions × Monthly Price)
ARR = MRR × 12

MoM Growth = (This Month MRR - Last Month MRR) / Last Month MRR
YoY Growth = (This Year ARR - Last Year ARR) / Last Year ARR
```

**Benchmarks:**
| Stage | Growth Target |
|-------|---------------|
| Seed | 15-20% MoM |
| Series A | 10-15% MoM, 3-5x YoY |
| Series B+ | 100%+ YoY (Rule of 40) |

### Unit Economics

```
CAC = Total S&M Spend / New Customers Acquired
LTV = ARPU × Gross Margin% × (1 / Churn Rate)
LTV:CAC Ratio = LTV / CAC
CAC Payback = CAC / (ARPU × Gross Margin%)
```

**Benchmarks:**
| Metric | Excellent | Good | Concerning |
|--------|-----------|------|------------|
| LTV:CAC | > 3.0 | 1.0-3.0 | < 1.0 |
| CAC Payback | < 12 months | 12-18 months | > 24 months |

### Cash Efficiency

```
Monthly Burn = Monthly Revenue - Monthly Expenses
Runway (months) = Cash Balance / Monthly Burn Rate
Burn Multiple = Net Burn / Net New ARR
```

**Burn Multiple Benchmarks:**
| Score | Assessment |
|-------|------------|
| < 1.0 | Exceptional efficiency |
| 1.0-1.5 | Good |
| 1.5-2.0 | Acceptable |
| > 2.0 | Inefficient |

**Target:** Always maintain 12-18 months runway.

## SaaS Metrics

### Revenue Composition

```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### Retention Metrics

```
NDR (Net Dollar Retention) = (ARR Start + Expansion - Contraction - Churn) / ARR Start
Gross Retention = (ARR Start - Churn - Contraction) / ARR Start
Logo Retention = (Customers End - New Customers) / Customers Start
```

**NDR Benchmarks:**
| Range | Assessment |
|-------|------------|
| > 120% | Best-in-class |
| 100-120% | Good |
| < 100% | Needs work |

### Efficiency Metrics

```
Magic Number = Net New ARR (quarter) / S&M Spend (prior quarter)
Rule of 40 = Revenue Growth Rate% + Profit Margin%
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
```

**Magic Number:**
- > 0.75 = Efficient, ready to scale
- 0.5-0.75 = Moderate efficiency
- < 0.5 = Inefficient, don't scale yet

## Marketplace Metrics

```
GMV = Σ (Transaction Value)
Take Rate = Net Revenue / GMV
```

**Typical Take Rates:**
| Type | Range |
|------|-------|
| Payment processors | 2-3% |
| E-commerce marketplaces | 10-20% |
| Service marketplaces | 15-25% |
| High-value B2B | 5-15% |

**Liquidity Indicators:**
- Fill rate > 80% = Strong liquidity
- Repeat rate > 60% = Strong retention

## Consumer/Mobile Metrics

```
DAU/MAU Ratio = DAU / MAU
K-Factor = Invites per User × Invite Conversion Rate
```

**DAU/MAU Benchmarks:**
| Ratio | Assessment |
|-------|------------|
| > 50% | Exceptional (daily habit) |
| 20-50% | Good |
| < 20% | Weak engagement |

**Retention Benchmarks (Day 30):**
| Rate | Assessment |
|------|------------|
| > 40% | Excellent |
| 25-40% | Good |
| < 25% | Weak |

## B2B Sales Metrics

```
Win Rate = Deals Won / Total Opportunities
Pipeline Coverage = Total Pipeline Value / Quota (target: 3-5x)
ACV = Total Contract Value / Contract Length (years)
```

**Sales Cycle Benchmarks:**
| Segment | Typical Duration |
|---------|------------------|
| SMB | 30-60 days |
| Mid-market | 60-120 days |
| Enterprise | 120-270 days |

## Metrics by Stage

### Pre-Seed (Product-Market Fit)

**Focus:** Active users, retention (Day 7/30), engagement, qualitative feedback

**Don't worry about:** Revenue, CAC, unit economics

### Seed ($500K-$2M ARR)

**Focus:**
- MRR growth rate (15-20% MoM)
- CAC and LTV baselines
- Gross retention (> 85%)
- Core product engagement

**Start tracking:** Sales efficiency, burn rate, runway

### Series A ($2M-$10M ARR)

**Focus:**
- ARR growth (3-5x YoY)
- LTV:CAC > 3, payback < 18 months
- NDR > 100%
- Burn multiple < 2.0
- Magic number > 0.5

## What Investors Want to See

### Seed Round
- MRR growth rate
- User retention
- Early unit economics
- Product engagement

### Series A
- ARR and growth rate
- CAC payback < 18 months
- LTV:CAC > 3.0
- NDR > 100%
- Burn multiple < 2.0

### Series B+
- Rule of 40 > 40%
- Efficient growth (magic number)
- Path to profitability

**Dashboard Format:**
```
Current MRR: $250K (↑ 18% MoM)
ARR: $3.0M (↑ 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
```

## Common Mistakes

1. **Vanity Metrics** — Focus on actionable metrics, not total users or page views
2. **Too Many Metrics** — Track 5-7 core metrics intensely, not 50 loosely
3. **Ignoring Unit Economics** — CAC and LTV matter even at seed stage
4. **Not Segmenting** — Break down by customer segment, channel, cohort
5. **Gaming Metrics** — Optimize for real business outcomes, not dashboards

## NEVER Do

1. **NEVER ignore** unit economics at any stage — CAC and LTV are always critical
2. **NEVER track** vanity metrics (total users, page views) without retention context
3. **NEVER report** growth rates without absolute numbers — 100% growth from $1K is different from $1M
4. **NEVER skip** segmentation — aggregate metrics hide important patterns
5. **NEVER confuse** correlation with causation — investigate before concluding
6. **NEVER set** targets without understanding your stage benchmarks
7. **NEVER present** metrics without trend context — current value + growth rate + benchmark
8. **NEVER optimize** for the metric instead of the underlying business outcome
