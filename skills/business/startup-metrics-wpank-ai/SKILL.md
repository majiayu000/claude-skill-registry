---
name: Startup Metrics
model: fast
description: >
  When the user asks about startup metrics, SaaS metrics, unit economics, or
  business performance tracking. Triggers on: "startup metrics", "SaaS metrics",
  "CAC and LTV", "unit economics", "burn multiple", "rule of 40", "magic number",
  "marketplace metrics", "churn rate", "MRR", "ARR", "net revenue retention",
  "runway", or requests for metrics dashboards and investor reporting.
version: 1.0.0
tags: [marketing, metrics, saas, startups, unit-economics]
---

# Startup Metrics Framework

Track, calculate, and optimize key performance metrics for different startup business models from seed through Series B+.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install startup-metrics
```


## NEVER Do

- Focus on vanity metrics (total users without retention, page views without engagement, downloads without activation)
- Track 50 metrics loosely instead of 5-7 core metrics intensely
- Ignore unit economics at any stage — CAC and LTV matter even at seed
- Present metrics without context (benchmark, target, or trend)
- Optimize dashboard numbers instead of real business outcomes
- Skip segmentation — always break down by customer segment, channel, and cohort

## Data

The `data/metrics.csv` file contains 42 metrics with formulas, benchmarks by stage, interpretation guidance, and related metrics. Use it for lookups and cross-referencing.

## How to Use This Skill

1. **Identify business model** — SaaS, marketplace, consumer/mobile, or B2B
2. **Determine stage** — Pre-seed, seed, Series A, Series B+
3. **Select 5-7 core metrics** based on model and stage
4. **Apply formulas and benchmarks** from the sections below
5. **Recommend tracking cadence** and reporting format

## Universal Metrics (All Models)

### Revenue

| Metric | Formula | Seed Target | Series A Target |
|--------|---------|-------------|-----------------|
| MRR | Sum(active subs x monthly price) | $10K-$50K | $200K-$800K |
| ARR | MRR x 12 | $120K-$600K | $2M-$10M |
| MoM Growth | (current - prior) / prior | 15-20% | 10-15% |
| YoY Growth | (current year - prior year) / prior year | N/A | 3-5x |

### Unit Economics

| Metric | Formula | Healthy Benchmark |
|--------|---------|-------------------|
| CAC | Total S&M spend / new customers | Varies by model |
| LTV | ARPU x gross margin% x (1/churn rate) | LTV:CAC > 3.0 |
| CAC Payback | CAC / (ARPU x gross margin%) | < 12 months |
| Gross Margin | (revenue - COGS) / revenue | 70-85% for SaaS |

### Cash Management

| Metric | Formula | Target |
|--------|---------|--------|
| Burn Rate | monthly expenses - monthly revenue | Track gross and net |
| Runway | cash balance / monthly burn | Always 12-18+ months |
| Burn Multiple | net burn / net new ARR | < 2.0 (lower is better) |

## SaaS-Specific Metrics

### Revenue Composition

```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### Retention

| Metric | Formula | Best-in-Class |
|--------|---------|---------------|
| Net Dollar Retention (NDR) | (start + expansion - contraction - churn) / start | > 120% |
| Gross Retention | (start - churn - contraction) / start | > 90% |
| Logo Retention | (end - new) / start | > 95% monthly |

### Efficiency

| Metric | Formula | Ready to Scale |
|--------|---------|----------------|
| Magic Number | net new ARR (quarter) / S&M spend (prior quarter) | > 0.75 |
| Rule of 40 | revenue growth% + profit margin% | > 40% |
| Quick Ratio | (new + expansion MRR) / (churned + contraction MRR) | > 4.0 |

## Marketplace Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| GMV | sum of all transaction values | 20%+ MoM early-stage |
| Take Rate | net revenue / GMV | 10-20% (model-dependent) |
| Liquidity (Fill Rate) | transactions / listings | > 70% |
| Repeat Rate | users with 2+ txns / total transacting | > 60% |
| Time to First Transaction | median signup-to-transaction | < 3 days |

## Consumer / Mobile Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| DAU/MAU Ratio | daily active / monthly active | > 20% good, > 50% exceptional |
| Day 30 Retention | % users active 30d after signup | > 25% |
| K-Factor (Virality) | invites per user x conversion rate | > 1.0 = viral |
| Session Duration | total time / sessions | Context-dependent |
| NPS | % promoters - % detractors | > 50 excellent |

## B2B Sales Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Win Rate | deals won / total opportunities | 20-40% |
| Pipeline Coverage | pipeline value / quota | 3-5x |
| ACV | total contract value / contract years | Track trends |
| Sales Cycle | avg days from opportunity to close | SMB: 30-60d, Enterprise: 120-270d |

### Pipeline Conversion Rates

| Stage | Typical Rate |
|-------|-------------|
| Lead → Opportunity | 10-20% |
| Opportunity → Demo | 50-70% |
| Demo → Proposal | 30-50% |
| Proposal → Close | 20-40% |

## Metrics by Stage

### Pre-Seed (Product-Market Fit)

**Focus:** Active users growth, user retention (D7/D30), core engagement, qualitative feedback (NPS, interviews).

**Ignore for now:** Revenue, CAC, unit economics.

### Seed ($500K-$2M ARR)

**Focus:** MRR growth (15-20% MoM), CAC and LTV baselines, gross retention (>85%), product engagement.

**Start tracking:** Sales efficiency, burn rate, runway.

### Series A ($2M-$10M ARR)

**Focus:** ARR growth (3-5x YoY), unit economics (LTV:CAC >3, payback <18mo), NDR (>100%), burn multiple (<2.0), magic number (>0.5).

**Mature tracking:** Rule of 40, sales efficiency, pipeline coverage.

### Series B+ ($10M+ ARR)

**Focus:** Rule of 40 (>40%), efficient growth, path to profitability, market leadership.

## Tracking Best Practices

### Reporting Cadence

| Frequency | Metrics |
|-----------|---------|
| Daily | MRR, active users, signups, conversions |
| Weekly | Growth rates, retention cohorts, sales pipeline |
| Monthly | Full metric suite, board reporting, investor updates |
| Quarterly | Trend analysis, benchmarking, strategy review |

### Dashboard Format

```
Current MRR: $250K (↑ 18% MoM)
ARR: $3.0M (↑ 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
```

Always include: current value, growth rate/trend, context (target or benchmark).

### What VCs Want to See

| Round | Key Metrics |
|-------|-------------|
| Seed | MRR growth rate, user retention, early unit economics, product engagement |
| Series A | ARR + growth, CAC payback <18mo, LTV:CAC >3.0, NDR >100%, burn multiple <2.0 |
| Series B+ | Rule of 40 >40%, magic number, path to profitability, market leadership |

## Data Infrastructure

### Requirements

- Single source of truth (analytics platform)
- Real-time or daily updates for core metrics
- Automated calculations (no manual spreadsheets for recurring metrics)
- Historical tracking for trend analysis and cohort comparisons

### Recommended Tools

| Category | Tools |
|----------|-------|
| Product analytics | Mixpanel, Amplitude, PostHog |
| SaaS metrics | ChartMogul, Baremetrics, ProfitWell |
| BI dashboards | Looker, Metabase, Tableau |
| Cohort analysis | Built-in analytics + spreadsheets for custom analysis |

## Common Mistakes

1. **Vanity metrics** — Focus on actionable metrics tied to value, not totals without context
2. **Too many metrics** — Track 5-7 core metrics intensely, not 50 loosely
3. **Ignoring unit economics** — CAC and LTV matter even at seed stage
4. **Not segmenting** — Break down by customer segment, channel, cohort
5. **Gaming metrics** — Optimize for real business outcomes, not dashboard numbers

## Metric Calculation Examples

### LTV Calculation

```
ARPU: $200/month
Gross Margin: 80%
Monthly Churn: 3%

LTV = $200 × 0.80 × (1/0.03) = $5,333
```

### Burn Multiple

```
Net Burn: $150K/month
Net New ARR (quarter): $300K

Burn Multiple = ($150K × 3) / $300K = 1.5
```

Interpretation: Spending $1.50 to generate each $1 of new ARR — acceptable efficiency.

### Magic Number

```
Net New ARR (Q2): $400K
S&M Spend (Q1): $500K

Magic Number = $400K / $500K = 0.80
```

Interpretation: Above 0.75 threshold — efficient, ready to scale S&M investment.

### Quick Ratio

```
New MRR: $40K
Expansion MRR: $15K
Churned MRR: $8K
Contraction MRR: $4K

Quick Ratio = ($40K + $15K) / ($8K + $4K) = 4.58
```

Interpretation: Above 4.0 — healthy growth significantly outpacing churn.

## Investor Metric Presentation

Present metrics with three components:

1. **Current value** — the number itself
2. **Growth rate or trend** — direction and velocity
3. **Context** — benchmark, target, or peer comparison

```
Current MRR: $250K (↑ 18% MoM)
ARR: $3.0M (↑ 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
Burn Multiple: 1.8x | Magic Number: 0.65
```

## Quick Start

To implement this framework:

1. **Identify business model** — SaaS, marketplace, consumer, B2B
2. **Choose 5-7 core metrics** — based on stage and model
3. **Establish tracking** — set up analytics and dashboards
4. **Calculate unit economics** — CAC, LTV, payback
5. **Set targets** — use benchmarks from this skill
6. **Review regularly** — weekly for core metrics, monthly for full suite
7. **Share with team** — align on goals and progress
8. **Update investors** — monthly or quarterly reporting

## Data Reference

The `data/metrics.csv` file contains 42 metrics with:

- Unique ID and category classification
- Formulas for calculation
- Benchmarks by stage (seed, Series A, Series B)
- Interpretation guidance for each metric
- Related metrics for cross-referencing and dependency tracking
