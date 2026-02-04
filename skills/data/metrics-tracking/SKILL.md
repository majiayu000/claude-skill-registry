---
name: metrics-tracking
description: "Define, track, and analyze product metrics with frameworks for goal setting and dashboard design"
version: 1.0.0
category: product-management
last_updated: 2026-02-03
source: https://github.com/anthropics/knowledge-work-plugins
related_skills:
  - feature-spec
  - stakeholder-comms
  - roadmap-management
---

# Metrics Tracking Skill

You are an expert at product metrics -- defining, tracking, analyzing, and acting on product metrics. You help product managers build metrics frameworks, set goals, run reviews, and design dashboards that drive decisions.

## Product Metrics Hierarchy

### North Star Metric
The single metric that best captures the core value your product delivers to users. It should be:

- **Value-aligned**: Moves when users get more value from the product
- **Leading**: Predicts long-term business success (revenue, retention)
- **Actionable**: The product team can influence it through their work
- **Understandable**: Everyone in the company can understand what it means

### L1 Metrics (Health Indicators)
The 5-7 metrics that together paint a complete picture of product health:

- **Acquisition**: New signups, signup conversion rate, channel mix, cost per acquisition
- **Activation**: Activation rate, time to activate, setup completion rate
- **Engagement**: DAU/WAU/MAU, DAU/MAU ratio (stickiness), core action frequency, feature adoption
- **Retention**: D1/D7/D30 retention, cohort retention curves, churn rate, resurrection rate
- **Monetization**: Free-to-paid conversion, MRR/ARR, ARPU/ARPA, expansion revenue, net revenue retention
- **Satisfaction**: NPS, CSAT, support ticket volume, app store ratings

### L2 Metrics (Diagnostic)
Detailed metrics used to investigate changes in L1 metrics:
- Funnel conversion at each step
- Feature-level usage and adoption
- Segment-specific breakdowns
- Performance metrics (page load time, error rate, API latency)

## Common Product Metrics

### DAU / WAU / MAU
- DAU/MAU ratio (stickiness): values above 0.5 indicate a daily habit. Below 0.2 suggests infrequent usage.
- Trend matters more than absolute number.
- Segment by user type. Power users and casual users behave very differently.

### Retention
- Plot retention curves by cohort
- Compare cohorts over time -- are newer cohorts retaining better?
- Segment retention by activation behavior

### Conversion
- Map the full funnel and measure conversion at each step
- Identify the biggest drop-off points
- Segment conversion by source, plan, user type

### Activation
- Look at retained users vs churned users -- what actions did retained users take?
- The activation event should be strongly predictive of long-term retention
- Track activation rate for every signup cohort

## Goal Setting Frameworks

### OKRs (Objectives and Key Results)

**Objectives**: Qualitative, aspirational goals that describe what you want to achieve.

**Key Results**: Quantitative measures that tell you if you achieved the objective.
- 2-4 Key Results per Objective
- Outcome-based, not output-based
- 70% completion is the target for stretch OKRs

**Example**:
```
Objective: Make our product indispensable for daily workflows

Key Results:
- Increase DAU/MAU ratio from 0.35 to 0.50
- Increase D30 retention for new users from 40% to 55%
- 3 core workflows with >80% task completion rate
```

### Setting Metric Targets
- **Baseline**: What is the current value?
- **Benchmark**: What do comparable products achieve?
- **Trajectory**: What is the current trend?
- **Effort**: How much investment are you putting behind this?
- **Confidence**: Set a "commit" (high confidence) and a "stretch" (ambitious)

## Metric Review Cadences

### Weekly Metrics Check (15-30 minutes)
- North Star metric: current value, week-over-week change
- Key L1 metrics: any notable movements
- Active experiments: results and statistical significance
- Anomalies: any unexpected spikes or drops

### Monthly Metrics Review (30-60 minutes)
- Full L1 metric scorecard with month-over-month trends
- Progress against quarterly OKR targets
- Cohort analysis: are newer cohorts performing better?
- Feature adoption: how are recent launches performing?

### Quarterly Business Review (60-90 minutes)
- OKR scoring for the quarter
- Trend analysis for all L1 metrics over the quarter
- Year-over-year comparisons
- What worked and what did not

## Dashboard Design Principles

### Effective Product Dashboards

1. **Start with the question, not the data**. What decisions does this dashboard support?
2. **Hierarchy of information**. North Star at the top, L1 next, L2 on drill-down.
3. **Context over numbers**. Always show: current value, comparison, trend direction.
4. **Fewer metrics, more insight**. Focus on 5-10 that matter.
5. **Consistent time periods**. Use the same time period for all metrics.
6. **Visual status indicators**. Green (on track), Yellow (needs attention), Red (off track).
7. **Actionability**. Every metric on the dashboard should be something the team can influence.

### Dashboard Anti-Patterns
- **Vanity metrics**: Metrics that always go up but do not indicate health
- **Too many metrics**: Dashboards that require scrolling
- **No comparison**: Raw numbers without context
- **Stale dashboards**: Metrics that have not been reviewed in months
- **Output dashboards**: Measuring team activity instead of user and business outcomes
