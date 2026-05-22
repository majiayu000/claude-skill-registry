---
name: analytics-metrics-kpi
version: "2.0.0"
description: Master metrics definition, KPI tracking, dashboarding, A/B testing, and data-driven decision making. Use data to guide product decisions.
sasmp_version: "1.3.0"
bonded_agent: 06-analytics-metrics
bond_type: PRIMARY_BOND
parameters:
  - name: product_stage
    type: string
    enum: [pre-launch, growth, mature]
    required: true
  - name: metric_category
    type: string
    enum: [acquisition, activation, retention, revenue, referral]
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Analytics & Metrics Skill

Become data-driven. Define meaningful metrics, build dashboards, run experiments, and make decisions based on data, not intuition.

## Metrics Framework (Acquisition → Revenue)

### North Star Metric

**Definition:** One metric that best captures the value your product delivers.

**Characteristics:**
- Directly tied to business success
- Driven by product improvements
- Leading indicator of revenue
- Understandable to whole company

**Examples:**
- Slack: Daily Active Users (DAU)
- Airbnb: Booked Nights
- YouTube: Watch Time
- Uber: Rides Completed
- Stripe: Payment Volume Processed

### Funnel Metrics (Acquisition)

```
Total Visitors: 100,000/month
↓ 20% conversion
Free Signups: 20,000
↓ 10% free-to-paid
Paid Customers: 2,000

CAC: $50 (marketing + sales spend / customers acquired)
LTCAC: $100 (all customer acquisition costs)
```

**Metrics to Track:**
- **Traffic** - Total visitors to website/app
- **Signup Rate** - % who sign up (target: 10-15%)
- **Free-to-Paid Conversion** - % free users who pay (target: 2-5%)
- **CAC** - Cost per acquired customer
- **CAC Payback** - Months to recover CAC from revenue (target: < 12 months)

### Activation Metrics

**Goal:** New users become active users

```
Free Signups: 2,000
↓ 30% onboard successfully
Activated: 600
↓ 60% remain active Day 7
Day 7 Active: 360
```

**Metrics to Track:**
- **Onboarding Completion Rate** - % who complete setup (target: 50-80%)
- **Time to First Value** - Hours to first successful use
- **Feature Adoption** - % who try key features
- **Day 1/7/30 Retention** - % active those days (target: 40/25/15)

### Engagement Metrics

**Goal:** Users regularly use product

**Daily/Monthly Metrics:**
- **DAU/MAU** - Daily/Monthly Active Users
- **DAU/MAU Ratio** - Stickiness (target: 20-30%)
- **Feature Usage** - % using key features
- **Session Length** - Minutes per session
- **Session Frequency** - Times per week

**Cohort Analysis Example:**
```
Jan Cohort (1,000 signups):
- Day 1: 600 active (60%)
- Day 7: 360 active (36%)
- Day 30: 180 active (18%)
- Month 3: 90 active (9%)

Feb Cohort (1,500 signups):
- Day 1: 1050 active (70%) ← Improving!
- Day 7: 630 active (42%)
- Day 30: 300 active (20%)
```

### Retention Metrics

**Goal:** Users stay and continue paying

```
Month 1: 1,000 customers
Month 2: 900 active (90% retained)
Month 3: 810 active (90% of month 2)
Month 12: 314 active (31% annual retention)
```

**Churn Rate:** % lost each period
- Monthly churn: (Customers Lost / Month Start) × 100
- Annual churn: 1 - (Ending / Starting)
- Target for SaaS: < 5% monthly churn

**NPS (Net Promoter Score)**
- Question: "How likely to recommend (0-10)?"
- Score = % Promoters (9-10) - % Detractors (0-6)
- Range: -100 to +100
- Target: 50+ (world-class)

### Revenue Metrics

**Monthly Recurring Revenue (MRR)**
```
MRR = (Total paid customers) × (average subscription price)
Growth MRR = New MRR + Expansion MRR - Churn MRR
```

**Annual Run Rate (ARR)**
```
ARR = MRR × 12
```

**Average Revenue Per User (ARPU)**
```
ARPU = MRR / Total Users
```

**Customer Lifetime Value (LTV)**
```
LTV = (ARPU × Gross Margin %) / Monthly Churn %

Example:
ARPU: $100
Gross Margin: 80%
Monthly Churn: 5%
LTV = ($100 × 80%) / 5% = $1,600

If CAC = $400: LTV/CAC = 4x ✓ (target: 3x+)
```

## Dashboard Architecture

### Executive Dashboard (C-Level)

**Weekly Updates:**
- MRR / ARR (vs target, vs month ago)
- New customers (weekly, monthly)
- Churn rate (%)
- NPS score
- Engagement (DAU, MAU)
- Key initiatives status

**Frequency:** Weekly

### Product Dashboard (Product Team)

**Daily/Weekly:**
- Funnel metrics (signup → paid)
- Feature adoption
- Engagement metrics
- User feedback score
- A/B test results
- Support ticket volume

**Frequency:** Daily updates

### Financial Dashboard (Finance/Operations)

**Monthly:**
- MRR / ARR
- Customer acquisition cost
- Customer lifetime value
- Gross margin
- CAC payback period
- Revenue by segment
- Churn by cohort

**Frequency:** Monthly

### Health Dashboard (Operations)

**Realtime:**
- System uptime (%)
- Error rate (%)
- Response time (p95)
- Database performance
- Support ticket response time
- Support backlog

**Frequency:** Realtime/hourly

## A/B Testing (Experimentation)

### Test Planning

**Hypothesis:**
"If we change X, then Y will improve, because Z"

**Example:**
"If we move signup button above the fold, then conversion will improve 15%, because users won't scroll."

### Test Structure

**Experiment Design:**
- **Control:** Keep current version
- **Treatment:** New version
- **Sample size:** Enough users to be statistical
- **Duration:** 2-4 weeks minimum
- **Metric:** Clear success metric

### Statistical Significance

**Confidence Level:** 95% (industry standard)
- Means 5% chance of false positive
- Need enough samples (typically 1000-10K per variant)
- Use calculator for exact sample size

**P-Value:** Probability result is random chance
- P < 0.05: Statistically significant
- P > 0.05: Not significant, inconclusive

### Example A/B Test

**Hypothesis:** Moving signup button above fold increases conversion 15%

**Setup:**
- Control: Current design
- Treatment: Button moved above fold
- Success metric: Conversion rate (signup / visit)
- Sample size: 10,000 users per variant
- Duration: 2 weeks
- Confidence: 95%

**Results:**
- Control: 2.0% conversion (200 signups from 10K visitors)
- Treatment: 2.8% conversion (280 signups from 10K visitors)
- Improvement: 40% increase (0.8% / 2% = 40%)
- P-value: 0.02 (statistically significant!)
- Decision: **SHIP IT** - Roll out to 100%

### Test Ideas by Priority

**High Priority (Start Here):**
- Signup flow optimization (biggest funnel)
- Onboarding experience
- Pricing page clarity
- Feature discoverability

**Medium Priority:**
- UI copy optimization
- CTA button colors
- Email subject lines
- Notification triggers

**Low Priority:**
- Micro-copy tweaks
- Animation effects
- Color scheme changes

## Metric Pitfalls to Avoid

### Vanity Metrics
❌ "We have 1M page views!"
✓ "We have 50K daily active users, growing 10% monthly"

### Actionable vs Non-Actionable
❌ "User satisfaction increased" (what changed?)
✓ "Onboarding completion rate 65% → 78% (↑20%)" (clear action)

### Correlation vs Causation
❌ "Ice cream sales correlate with drownings"
✓ Understand actual causation, not just correlation

### Look-Alike Metrics
❌ Track MRR but not Customer LTV (can grow MRR by spending more on acquisition)
✓ Track both acquisition efficiency AND retention

## Metrics Review Cadence

**Daily:**
- System uptime
- Error rates
- Support response time

**Weekly:**
- Funnel metrics
- Feature adoption
- Key engagement metrics
- Test results

**Monthly:**
- Revenue metrics
- Cohort analysis
- Churn breakdown
- LTV/CAC trends

**Quarterly:**
- Strategic metric review
- Long-term trend analysis
- Metric changes needed

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Vanity metrics focus | Wrong KPI selection | North Star alignment |
| Inconclusive A/B test | Low sample size | Extend duration |
| Data inconsistency | Multiple sources | Single source of truth |
| Dashboard unused | Too complex | Simplify to 5-7 KPIs |

### Debug Checklist

```
[ ] North Star metric defined mi?
[ ] Metrics business goals'a aligned mi?
[ ] Data collection accurate mi?
[ ] Dashboard refreshed mi?
[ ] A/B test sample sufficient mi?
[ ] Statistical significance achieved mi?
```

### Recovery Procedures

1. **Data Quality Issues** → Flag affected metrics, exclude
2. **Inconclusive A/B** → Extend test duration
3. **Misleading Metrics** → Add context/segmentation

---

**Master data-driven decision making and grow faster!**
