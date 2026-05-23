---
name: product-analyst
description: Track user metrics and provide data-driven insights for product decisions. Use when measuring product health, analyzing user behavior, conducting cohort analysis, or optimizing key metrics. Covers acquisition, engagement, retention, revenue metrics, and data-driven decision making.
---

# Product Analyst

Measure user behavior and product health to inform data-driven decisions.

## Core Principle

**What gets measured gets improved.** Define the right metrics, track them relentlessly, and act on insights quickly.

## North Star Metric

**The ONE metric that best captures value delivered to users.**

Your North Star should:

- ✅ Represent real customer value
- ✅ Correlate with revenue
- ✅ Be measurable frequently (daily/weekly)
- ✅ Rally the entire team around one goal

**Examples by Product Type**:

```yaml
Communication:
  Slack: Messages Sent (weekly active)
  Zoom: Weekly Meeting Minutes
  Discord: Active Servers

Marketplace:
  Airbnb: Nights Booked
  Uber: Completed Rides
  Etsy: Gross Merchandise Value (GMV)

Media/Content:
  Spotify: Time Listening
  Netflix: Hours Watched
  Medium: Total Time Reading

SaaS/B2B:
  Asana: Weekly Active Teams
  Notion: Collaborative Documents
  Salesforce: Deals Closed (CRM value)

Social:
  Facebook: Daily Active Users (DAU)
  Instagram: Posts Shared
  Twitter: Tweets per User
```

**How to choose your North Star**:

1. What action represents core value?
2. If users do this more, do they get more value?
3. Does this predict revenue?
4. Can the entire team influence it?

## Key Metrics by Category

### Acquisition Metrics

**Goal**: Get users into the product

```yaml
Traffic Sources:
  - Organic Search: SEO traffic
  - Paid Ads: Google Ads, Facebook Ads
  - Referral: Word of mouth, links
  - Direct: Typed URL, bookmarked
  - Social: Twitter, LinkedIn posts

Key Metrics:
  - Unique Visitors: Total website visitors
  - Sign-ups: Users who created account
  - Conversion Rate: Visitors → Sign-ups
  - Cost Per Acquisition (CPA): Ad spend / sign-ups
  - Source Quality: Which sources convert best?

Targets:
  - Visitor → Sign-up: 2-5% (good), 5-10% (excellent)
  - CPA: < $50 (B2C), < $200 (B2B), depends on LTV
```

### Activation Metrics

**Goal**: Get users to "aha moment"

```yaml
Activation Definition:
  - User completes onboarding
  - User takes first core action
  - User experiences product value

Examples:
  Slack: Sent 2,000 messages (team is active)
  Dropbox: Added file to folder
  Twitter: Followed 30 accounts
  Airbnb: Completed first booking

Key Metrics:
  - Activation Rate: Sign-ups → Activated
  - Time to Activation: How long to aha moment?
  - Onboarding Completion: % who finish setup

Targets:
  - Activation Rate: >40% (good), >60% (excellent)
  - Time to Activation: <24 hours (ideal)
```

### Engagement Metrics

**Goal**: Keep users coming back

```yaml
Key Metrics:
  - Daily Active Users (DAU)
  - Weekly Active Users (WAU)
  - Monthly Active Users (MAU)
  - DAU/MAU Ratio (Stickiness): How often users return
  - Session Frequency: Times per week user logs in
  - Session Duration: Time spent per visit
  - Feature Adoption: % using each feature

DAU/MAU Stickiness:
  Excellent: >40% (Facebook, Slack)
  Good: 20-40% (most SaaS)
  Needs Work: <20%

Session Frequency Targets:
  B2C Social: 5-7 times per week
  B2B Tools: 3-5 times per week
  E-commerce: 1-2 times per week
```

### Retention Metrics

**Goal**: Prevent churn

```yaml
Cohort Retention:
  - Day 1: % still active 1 day after sign-up
  - Day 7: % still active 7 days after
  - Day 30: % still active 30 days after

Good Retention Curves:
  Consumer B2C:
    - D1: 60-80%
    - D7: 40-60%
    - D30: 30-50%
    - Flattening curve (good!)

  Enterprise B2B:
    - D1: 80-90%
    - D7: 70-80%
    - D30: 60-70%
    - Very flat curve

Bad Retention:
  - D1: 40%
  - D7: 10%
  - D30: 2%
  - Steep drop-off = product-market fit issue

Churn Rate:
  - Monthly Churn: % users who stop using each month
  - Target: <5% (consumer), <1% (enterprise)
  - Churn = Revenue Leak

Net Retention:
  - (Starting Users + New - Churned) / Starting Users
  - Target: >100% (growth despite churn)
```

### Revenue Metrics

**Goal**: Monetize effectively

```yaml
Key Metrics:
  - MRR (Monthly Recurring Revenue): Predictable monthly income
  - ARR (Annual Recurring Revenue): MRR × 12
  - ARPU (Average Revenue Per User): Revenue / # users
  - LTV (Lifetime Value): Total revenue from user over lifetime
  - CAC (Customer Acquisition Cost): Sales + marketing / new customers
  - LTV:CAC Ratio: Must be > 3:1
  - Payback Period: Months to recover CAC

Calculations:
  LTV = ARPU × Average Lifetime (months)
  Average Lifetime = 1 / Churn Rate

  Example:
    ARPU: $50/month
    Churn: 5% per month
    Average Lifetime: 1 / 0.05 = 20 months
    LTV: $50 × 20 = $1,000

  CAC: $300
  LTV:CAC = $1,000 / $300 = 3.3:1 (Good!)

Targets:
  - LTV:CAC: >3:1 (minimum), >4:1 (healthy)
  - Payback Period: <12 months
  - MRR Growth: >10% month-over-month (early stage)
```

### Satisfaction Metrics

**Goal**: Keep customers happy

```yaml
NPS (Net Promoter Score):
  Question: "How likely are you to recommend us?" (0-10)
  - Promoters: 9-10
  - Passives: 7-8
  - Detractors: 0-6

  NPS = % Promoters - % Detractors

  Benchmarks:
    Excellent: >50
    Good: 30-50
    Needs Work: <30

CSAT (Customer Satisfaction):
  Question: "How satisfied are you?" (1-5)

  Target: >4.0 average

CES (Customer Effort Score):
  Question: "How easy was it to [task]?" (1-7)

  Target: <3.0 (low effort)
```

## Segmentation

**Don't treat all users the same.** Different cohorts behave differently.

```yaml
Segment by Engagement:
  Power Users (Top 10%):
    - Use daily
    - High engagement
    - Understand product deeply
    → Interview them for feature ideas

  Casual Users (Middle 60%):
    - Use occasionally
    - Basic feature adoption
    → What prevents them from power usage?

  At-Risk Users (Bottom 20%):
    - Haven't logged in 7+ days
    - Low engagement
    → Re-engagement campaign

  Churned Users:
    - No activity 30+ days
    → Exit survey, understand why

Segment by Acquisition Source:
  - Organic vs Paid
  - Which source has best retention?
  - Which source has best LTV?

Segment by Plan:
  - Free vs Paid
  - Starter vs Pro vs Enterprise
  - Which tier has best retention?

Segment by Cohort (Sign-up Date):
  - Week 1 users vs Week 2 users
  - Did product changes improve metrics?
```

## Funnel Analysis

**Track conversion at each stage:**

```yaml
Sign-up Funnel Example:
  1. Land on homepage:        10,000 users (100%)
  2. Click "Sign Up":          2,000 users (20%)
  3. Fill sign-up form:        1,200 users (12%)
  4. Verify email:               800 users (8%)
  5. Complete onboarding:        400 users (4%)

Analysis:
  Biggest drop-off: Homepage → Sign Up (80% lost)
  Fix: Clarify value prop, add social proof, improve CTA

  Second drop-off: Form → Email verify (33% lost)
  Fix: Simplify form, reduce friction

Optimize biggest drop-offs first for max impact.
```

## Cohort Analysis

**Compare user groups over time:**

```yaml
Example: Retention by Sign-up Week

Week 1 Cohort (Jan 1-7):
  100 users signed up
  - D1: 80 active (80%)
  - D7: 40 active (40%)
  - D30: 20 active (20%)

Week 2 Cohort (Jan 8-14):
  120 users signed up
  - D1: 102 active (85%)  ← +5% improvement!
  - D7: 60 active (50%)   ← +10% improvement!
  - D30: 36 active (30%)  ← +10% improvement!

Insight: Onboarding changes in Week 2 improved retention!

Action: Roll out Week 2 changes to all users.
```

## A/B Testing

**Test hypotheses systematically:**

```yaml
1. Form Hypothesis: 'Adding social proof to homepage will increase sign-ups by 10%'

2. Design Experiment:
  - Control: Current homepage
  - Treatment: Homepage + customer testimonials
  - Split: 50/50 traffic
  - Primary Metric: Sign-up rate
  - Duration: 2 weeks or 1,000 visitors per variant

3. Run Test:
  - Don't peek early (wait for significance)
  - Monitor for bugs/issues

4. Analyze Results:
  Control: 1,000 visitors → 20 sign-ups (2.0%)
  Treatment: 1,000 visitors → 25 sign-ups (2.5%)

  Lift: +25% relative
  P-value: 0.04 (significant at p<0.05)

  Decision: WIN - Ship it!

5. Document Learning: 'Social proof increases sign-ups by 25%. Apply to all high-intent pages.'

Minimum Sample Size:
  - 100+ conversions per variant minimum
  - More is better for small effects
```

## Dashboard Design

### Executive Dashboard

```yaml
Top Metrics (Big Numbers):
  - North Star Metric: 12,500 WAU
  - MRR: $42,000 (+12% MoM)
  - Users: 1,850 (+15% MoM)

Graphs (Trends):
  - North Star over time
  - Revenue growth
  - User acquisition

Alerts:
  - Churn spike: +20% this week ⚠️
  - Trial conversion down: 10% → 8% ⚠️
```

### Product Dashboard

```yaml
Engagement:
  - DAU: 3,200
  - WAU: 8,500
  - MAU: 15,000
  - Stickiness (DAU/MAU): 21%

Feature Usage:
  - Feature A: 80% adoption
  - Feature B: 45% adoption
  - Feature C: 12% adoption (low!)

Retention:
  - D1: 75%
  - D7: 50%
  - D30: 35%

Funnels:
  - Sign-up → Activation: 45%
  - Trial → Paid: 12%
```

### Marketing Dashboard

```yaml
Acquisition:
  - Visitors: 50,000
  - Sign-ups: 2,000 (4% conversion)
  - Activated: 800 (40% activation)

By Source:
  - Organic: 20,000 visitors, 5% conversion
  - Paid: 15,000 visitors, 3% conversion
  - Referral: 10,000 visitors, 6% conversion (best!)

Cost Efficiency:
  - CPA: $150
  - LTV: $600
  - LTV:CAC: 4:1 (healthy!)
```

## Tools & Software

```yaml
Event Tracking:
  - Mixpanel (best for product analytics)
  - Amplitude (great alternative)
  - PostHog (open-source)
  - Google Analytics 4 (free, basic)

Session Recording:
  - FullStory (see user sessions)
  - LogRocket (debugging + analytics)
  - Hotjar (heatmaps + recordings)

A/B Testing:
  - Optimizely
  - VWO
  - Google Optimize (free, basic)
  - LaunchDarkly (feature flags + testing)

Data Warehouse:
  - Snowflake
  - BigQuery
  - Redshift

Visualization:
  - Tableau
  - Looker
  - Metabase (open-source)
```

## Reporting Cadence

```yaml
Daily:
  - Check North Star Metric
  - Monitor error rates
  - Review yesterday's experiments

Weekly:
  - Funnel analysis
  - Cohort retention
  - Feature adoption
  - Share insights with team

Monthly:
  - MRR/ARR review
  - LTV:CAC ratio
  - Churn analysis
  - Send NPS survey

Quarterly:
  - Deep dive on user segments
  - Competitive benchmarking
  - Strategic planning with leadership
```

## Quick Start Checklist

- [ ] Define North Star Metric
- [ ] Set up event tracking (Mixpanel/Amplitude)
- [ ] Instrument key events (sign-up, activation, core actions)
- [ ] Create acquisition funnel
- [ ] Track retention cohorts
- [ ] Build executive dashboard
- [ ] Set up weekly reporting
- [ ] Run first A/B test

## Common Pitfalls

❌ **Vanity metrics**: Tracking metrics that look good but don't predict success (e.g., page views)
❌ **Too many metrics**: Focus on 3-5 key metrics, not 50
❌ **No North Star**: Team pulls in different directions
❌ **Ignoring segments**: Averages hide important patterns
❌ **Analysis paralysis**: Measure, learn, act quickly
❌ **Not acting on data**: Data without action is worthless

## Summary

Great product analysis:

- ✅ One North Star Metric everyone tracks
- ✅ AARRR framework (Acquisition, Activation, Retention, Revenue, Referral)
- ✅ Cohort analysis over time
- ✅ Segmentation (not all users are the same)
- ✅ Regular A/B testing
- ✅ Share insights widely with team
- ✅ Act on data quickly
