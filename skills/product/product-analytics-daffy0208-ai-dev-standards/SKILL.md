---
name: product-analytics
description: Measure what matters with proper event tracking, funnels, cohorts, and metrics. Use when setting up analytics, tracking features, or understanding behavior.
license: Complete terms in LICENSE.txt
---

# Product Analytics

Measure what matters and make data-driven decisions.

## North Star Metric

**The ONE metric that represents customer value**

```yaml
Examples:
  Slack: Weekly Active Users
  Airbnb: Nights Booked
  Spotify: Time Listening
  Shopify: GMV

Your North Star should: ✅ Represent customer value
  ✅ Correlate with revenue
  ✅ Be measurable frequently
  ✅ Rally the team
```

## Key Metrics Hierarchy

```
North Star Metric
  ├── Input Metrics (drive North Star)
  │   ├── Acquisition
  │   ├── Activation
  │   └── Retention
  └── KPIs (business health)
      ├── Revenue
      ├── Churn
      └── LTV
```

## Event Tracking

```typescript
// Track user actions
analytics.track('Button Clicked', {
  button_name: 'signup',
  page: 'homepage',
  user_id: '123'
})

// Track page views
analytics.page('Homepage', {
  referrer: document.referrer,
  path: window.location.pathname
})

// Identify users
analytics.identify('user-123', {
  email: 'user@example.com',
  plan: 'pro',
  created_at: '2024-01-15'
})
```

## Funnel Analysis

```yaml
Sign-up Funnel:
  1. Land on homepage: 10,000 (100%)
  2. Click signup: 2,000 (20%)
  3. Fill form: 1,000 (10%)
  4. Verify email: 800 (8%)
  5. Complete onboarding: 400 (4%)

Insights:
  - Biggest drop: Homepage to signup (80% lost)
  - Fix: Clarify value prop, add social proof
```

## Cohort Analysis

```yaml
Week 1 Cohort (Jan 1-7):
  - D1: 80% active
  - D7: 40% active
  - D30: 20% active

Week 2 Cohort (Jan 8-14):
  - D1: 85% active (+5%)
  - D7: 50% active (+10%)
  - D30: 30% active (+10%)

Insight: Onboarding changes improved retention!
```

## Retention Curves

```yaml
Good Retention:
  - D1: 60-80%
  - D7: 40-60%
  - D30: 30-50%
  - Flattening curve (good!)

Bad Retention:
  - D1: 40%
  - D7: 10%
  - D30: 2%
  - Steep drop-off (bad!)
```

## Key Metrics to Track

### Acquisition

- Traffic sources (organic, paid, referral)
- Cost per click (CPC)
- Conversion rate (visitor → signup)

### Activation

- Signup → first core action
- Time to value
- Onboarding completion rate

### Retention

- DAU / MAU (stickiness)
- Retention rate D1, D7, D30
- Churn rate

### Revenue

- MRR / ARR
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)
- LTV:CAC ratio

### Referral

- Viral coefficient
- Referral signups
- NPS (Net Promoter Score)

````

## Tools

```yaml
Event Tracking:
  - Mixpanel (best for products)
  - Amplitude (good alternative)
  - PostHog (open-source)

Session Recording:
  - FullStory
  - LogRocket
  - Hotjar

A/B Testing:
  - Optimizely
  - VWO
  - Google Optimize (free)
````

## Dashboard Design

```yaml
Executive Dashboard:
  - North Star Metric (big number)
  - Revenue (MRR/ARR)
  - Key metric trends (graphs)

Product Dashboard:
  - Active users (DAU/WAU/MAU)
  - Feature usage
  - Retention cohorts
  - Funnels

Marketing Dashboard:
  - Traffic sources
  - Conversion rates
  - Cost per acquisition
  - ROI by channel
```

## Summary

Great analytics:

- ✅ One North Star Metric
- ✅ Track everything
- ✅ Regular review (weekly)
- ✅ Share insights widely
- ✅ Act on data quickly
