---
name: sales-metrics
description: Sales metrics frameworks with leading/lagging indicators, benchmarks, and capacity models.
---

# Sales Metrics

Frameworks for measuring and forecasting sales performance.

## Leading vs Lagging Indicators

### Leading Indicators (Predictive)

| Metric | Definition | Target Setting |
|--------|------------|----------------|
| **MQLs** | Marketing qualified leads | Based on conversion rates |
| **SQLs** | Sales qualified leads | MQL × MQL→SQL rate |
| **Opportunities** | Discovery completed | SQL × qualification rate |
| **Pipeline** | Weighted opportunity value | 3-4x quota coverage |
| **Meetings Booked** | First meetings scheduled | Based on rep capacity |
| **Proposals Sent** | Active evaluations | Based on demo→proposal rate |

### Lagging Indicators (Results)

| Metric | Definition | B2B SaaS Benchmark |
|--------|------------|-------------------|
| **Win Rate** | Won ÷ (Won + Lost) | 20-30% |
| **Sales Cycle** | Qualified to Close | 30-90 days (SMB), 90-180 days (Enterprise) |
| **ACV** | Average contract value | Varies |
| **CAC** | Total S&M ÷ New customers | < 1/3 LTV |
| **LTV:CAC** | Customer lifetime value ÷ CAC | > 3:1 |
| **CAC Payback** | Months to recover CAC | < 12 months |

## Conversion Rate Benchmarks

| Stage | Benchmark Range |
|-------|-----------------|
| Visitor → Lead | 1-5% |
| Lead → MQL | 10-30% |
| MQL → SQL | 15-30% |
| SQL → Opportunity | 40-60% |
| Opportunity → Win | 20-30% |

**Overall Funnel:**
- Top of funnel to customer: 0.5-2%
- Outbound response rate: 1-5%
- Cold email reply rate: 3-10%
- Cold call connection rate: 10-20%

## Sales Capacity Model

```
Target Revenue: $X
÷ ACV: $Y
= Deals Needed: N

Deals Needed ÷ Win Rate (25%) = Opportunities Needed
Opportunities ÷ SQL→Opp Rate (50%) = SQLs Needed
SQLs ÷ MQL→SQL Rate (20%) = MQLs Needed

For Rep Planning:
Quota/Rep = $X (typically 4-5x OTE)
Target Revenue ÷ Quota = Reps Needed
Ramp time = 3-6 months to productivity
```

## Activity Metrics (by Role)

### SDR Metrics

| Metric | Daily | Weekly | Monthly |
|--------|-------|--------|---------|
| Emails sent | 50-100 | 250-500 | 1,000-2,000 |
| Calls made | 40-80 | 200-400 | 800-1,600 |
| LinkedIn touches | 20-40 | 100-200 | 400-800 |
| Meetings booked | 0.5-1 | 3-5 | 15-20 |

### AE Metrics

| Metric | Weekly | Monthly | Quarterly |
|--------|--------|---------|-----------|
| Discovery calls | 8-12 | 35-50 | 100-150 |
| Demos | 5-8 | 20-30 | 60-90 |
| Proposals | 3-5 | 12-20 | 35-60 |
| Closes | 1-2 | 4-8 | 12-24 |

## Pipeline Health Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Coverage** | Pipeline ÷ Quota | 3-4x |
| **Velocity** | (Opps × Win Rate × ACV) ÷ Cycle | Trending up |
| **Age** | Days in stage | Below threshold |
| **Progression** | Opps moving forward | 20%+ weekly |

**Pipeline Hygiene Rules:**
- Close dead opps within 2x average cycle
- Update stage within 48 hours of change
- No opportunities without next step scheduled

## Forecasting Framework

| Category | Definition | Weighting |
|----------|------------|-----------|
| **Closed** | Signed contract | 100% |
| **Commit** | Verbal yes, paperwork in flight | 90% |
| **Best Case** | Strong signal, proposal accepted | 50% |
| **Pipeline** | Active, qualified opportunity | 25% |
| **Upside** | Early stage, unqualified | 10% |

**Forecast Formula:**
```
Forecast = Σ(Opportunity Value × Stage Probability)
```

## Revenue Metrics

| Metric | Formula | Why It Matters |
|--------|---------|----------------|
| **MRR** | Monthly recurring revenue | Base health |
| **ARR** | MRR × 12 | Annual run rate |
| **Net New ARR** | New + Expansion - Churn | True growth |
| **NRR** | (Start + Expansion - Churn) ÷ Start | Customer health |
| **Gross Margin** | (Revenue - COGS) ÷ Revenue | Unit economics |

## Sales Efficiency Metrics

| Metric | Formula | Good |
|--------|---------|------|
| **Magic Number** | Net New ARR ÷ Prior S&M Spend | > 0.75 |
| **CAC Payback** | CAC ÷ (ACV × Gross Margin) | < 12 mo |
| **Revenue/Rep** | ARR ÷ Quota-carrying reps | > $500K |
| **Pipeline/Rep** | Pipeline ÷ Reps | > 3x quota |
