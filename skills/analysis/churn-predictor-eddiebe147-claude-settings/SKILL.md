---
name: Churn Predictor
slug: churn-predictor
description: Predict customer churn risk using behavioral signals, engagement data, and predictive analytics
category: customer-support
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "churn prediction"
  - "churn risk"
  - "customer retention"
  - "at-risk customers"
  - "churn analysis"
  - "retention modeling"
tags:
  - churn
  - prediction
  - retention
  - analytics
  - customer-success
---

# Churn Predictor

Expert churn prediction system that identifies at-risk customers before they leave using behavioral signals, engagement patterns, and predictive analytics. This skill provides structured workflows for building churn models, monitoring risk signals, and executing retention interventions.

Churn is the silent killer of growth. By the time a customer announces they're leaving, it's often too late. This skill helps you identify churn risk early when intervention can still make a difference, prioritize retention efforts, and systematically reduce churn.

Built on data science best practices and customer success methodologies, this skill combines leading indicator analysis, risk scoring, and intervention playbooks to predict and prevent churn before it happens.

## Core Workflows

### Workflow 1: Churn Signal Identification
**Map the behaviors that predict churn**

1. **Behavioral Signals**
   | Signal Type | Examples | Risk Level |
   |-------------|----------|------------|
   | Usage Decline | 30%+ drop in logins, sessions, actions | High |
   | Feature Abandonment | Stopped using key features | Medium-High |
   | Engagement Drop | No response to emails, missed meetings | Medium |
   | Support Patterns | Spike in tickets, negative sentiment | High |
   | Billing Issues | Failed payments, downgrade requests | High |

2. **Account Signals**
   - Champion departure (key user leaves)
   - Company layoffs or restructuring
   - Merger/acquisition announcements
   - Budget cuts affecting your category
   - Competitor evaluation signals
   - Contract not renewed on auto-renew

3. **Relationship Signals**
   - NPS score decline (9-10 → 7 or below)
   - Missed QBRs or check-ins
   - Unresponsive to outreach
   - Escalated support issues
   - Negative sentiment in communications

4. **Time-Based Signals**
   - Approaching renewal (90/60/30 days)
   - End of trial or pilot
   - Anniversary of bad experience
   - Post-implementation plateau
   - Seasonal usage patterns

### Workflow 2: Risk Scoring Model
**Build a composite churn risk score**

1. **Score Components**
   ```
   Churn Risk Score =
     (Usage Score × 0.30) +
     (Engagement Score × 0.25) +
     (Support Score × 0.20) +
     (Relationship Score × 0.15) +
     (Account Score × 0.10)

   Scale: 0-100 (higher = more at risk)
   ```

2. **Usage Score Factors**
   - Login frequency vs. baseline
   - Feature adoption breadth
   - Active users vs. licensed seats
   - Time in product
   - Core action completion

3. **Engagement Score Factors**
   - Email open/click rates
   - Meeting attendance
   - Resource downloads
   - Training completion
   - Community participation

4. **Risk Categories**
   | Score | Risk Level | Action |
   |-------|------------|--------|
   | 0-20 | Low | Standard monitoring |
   | 21-40 | Moderate | Proactive outreach |
   | 41-60 | Elevated | Intervention needed |
   | 61-80 | High | Urgent save attempt |
   | 81-100 | Critical | Executive escalation |

### Workflow 3: Cohort & Trend Analysis
**Understand churn patterns across customer segments**

1. **Cohort Analysis**
   - Analyze by signup month/quarter
   - Track retention curves over time
   - Identify cohorts with worse retention
   - Correlate with product/market changes
   - Find patterns in successful cohorts

2. **Segment Analysis**
   - By customer size (SMB/Mid/Enterprise)
   - By industry vertical
   - By use case/persona
   - By acquisition source
   - By pricing tier

3. **Churn Timing Patterns**
   - When in customer lifecycle does churn occur?
   - Renewal vs. mid-contract churn
   - Time from warning signs to churn
   - Seasonal patterns
   - Correlation with contract length

4. **Leading Indicator Validation**
   - Track signals → churn correlation
   - Calculate signal lead time
   - Measure false positive rate
   - Refine scoring weights
   - A/B test interventions

### Workflow 4: Alert & Escalation System
**Surface risk at the right time to the right people**

1. **Alert Triggers**
   - Score crosses threshold (e.g., into "elevated")
   - Rapid score increase (10+ points in 7 days)
   - Critical signal detected (payment failed, champion left)
   - Renewal approaching with elevated risk
   - Multiple signals converging

2. **Escalation Matrix**
   | Risk Level | Owner | Escalation | Response SLA |
   |------------|-------|------------|--------------|
   | Moderate | CSM | None | 5 days |
   | Elevated | CSM | Manager copy | 48 hours |
   | High | CSM + Manager | VP briefed | 24 hours |
   | Critical | Manager | VP/Exec sponsor | Same day |

3. **Alert Content**
   - Customer name and risk score
   - Specific signals triggering alert
   - Score trend (improving/declining)
   - Renewal date and ARR at risk
   - Recommended actions

4. **Alert Channels**
   - Slack/Teams notifications
   - Email digests
   - CRM dashboards
   - Weekly risk reports
   - Executive summaries

### Workflow 5: Intervention Playbooks
**Systematic approaches to save at-risk customers**

1. **Intervention Matching**
   | Root Cause | Intervention |
   |------------|--------------|
   | Low adoption | Training, onboarding redo |
   | Technical issues | Engineering escalation, workarounds |
   | Value unclear | ROI analysis, executive alignment |
   | Champion left | Relationship rebuild with new stakeholders |
   | Pricing concerns | Discount, plan adjustment, payment terms |
   | Competitive | Feature comparison, roadmap preview |

2. **Save Play Execution**
   - Diagnose root cause (don't assume)
   - Match intervention to cause
   - Assign owner and resources
   - Set clear timeline and milestones
   - Track outcome (saved, lost, reason)

3. **Intervention Tactics**
   - **Urgent Call**: Same-day executive outreach
   - **Health Check**: Comprehensive account review
   - **Training Blitz**: Intensive enablement sessions
   - **Success Sprint**: Focused value delivery
   - **Executive Alignment**: VP/C-level engagement
   - **Commercial Discussion**: Pricing/terms adjustment

4. **Outcome Tracking**
   - Save rate by risk level
   - Save rate by intervention type
   - Time from intervention to resolution
   - Reasons for unsuccessful saves
   - Long-term retention of saved accounts

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Check risk score | "Show churn risk for [Customer]" |
| List at-risk accounts | "Show accounts above [X] risk score" |
| Analyze churn patterns | "Analyze churn patterns by [segment]" |
| Review alerts | "Show churn alerts this week" |
| Create save plan | "Create intervention plan for [Customer]" |
| Score validation | "Validate churn model accuracy" |
| Cohort analysis | "Analyze retention by cohort" |
| Signal analysis | "Find leading churn indicators" |
| Trend report | "Show risk score trends" |
| Intervention report | "Report on save play outcomes" |

## Best Practices

### Signal Selection
- Focus on behaviors you can observe
- Validate correlation with actual churn
- Use leading indicators (not lagging)
- Combine multiple signal types
- Weight by predictive power

### Scoring Model
- Start simple, add complexity gradually
- Calibrate weights with historical data
- Validate with blind holdout testing
- Recalibrate quarterly
- Document methodology

### Alert Design
- Don't alert on every score change
- Focus on actionable thresholds
- Include context in alerts
- Route to right person
- Avoid alert fatigue

### Intervention
- Diagnose before prescribing
- Match intervention to root cause
- Set clear success criteria
- Track outcomes rigorously
- Learn from failures

### Model Maintenance
- Review accuracy monthly
- Retrain with new churn data
- Adjust for product changes
- Update as customer base evolves
- Document false positives/negatives

## Churn Signals Library

### Usage Signals
| Signal | Calculation | Warning Threshold |
|--------|-------------|-------------------|
| Login decline | % change week-over-week | -30% for 2+ weeks |
| DAU/MAU ratio | Daily active / Monthly active | Below 0.2 |
| Feature breadth | # features used / available | Below 30% |
| Seat utilization | Active users / licensed seats | Below 50% |
| Session depth | Actions per session | Below baseline by 40% |

### Engagement Signals
| Signal | Calculation | Warning Threshold |
|--------|-------------|-------------------|
| Email engagement | Open rate × Click rate | Below 5% |
| Meeting attendance | Attended / Scheduled | Below 60% |
| Response time | Avg days to respond | Above 5 days |
| QBR participation | Attended / Scheduled | Miss 2+ in row |
| Training completion | Completed / Available | Below 25% |

### Support Signals
| Signal | Calculation | Warning Threshold |
|--------|-------------|-------------------|
| Ticket volume | Tickets / month | 3× baseline |
| Sentiment score | Negative / Total | Above 30% |
| Escalation rate | Escalated / Total | Above 20% |
| Resolution satisfaction | CSAT on resolved | Below 3/5 |
| Open ticket age | Avg days open | Above 7 days |

### Relationship Signals
| Signal | Calculation | Warning Threshold |
|--------|-------------|-------------------|
| NPS change | Current - Previous | Drop of 3+ points |
| Health score | Composite score | Below 60 |
| Champion risk | Champion activity decline | Below 50% of baseline |
| Executive access | Exec meetings / quarter | 0 in 2+ quarters |
| Renewal confidence | CSM assessment | Below 70% |

## Risk Report Template

### Weekly At-Risk Summary
```markdown
# Churn Risk Report: Week of [Date]

## Summary
- Accounts at elevated risk or above: [X]
- Total ARR at risk: $[Amount]
- New alerts this week: [X]
- Risk trending up: [X accounts]
- Risk trending down: [X accounts]

## Critical Risk (81-100)
| Account | ARR | Score | Key Signals | Owner | Action |
|---------|-----|-------|-------------|-------|--------|
| [Name] | $X | 87 | [Signals] | [CSM] | [Status] |

## High Risk (61-80)
[Same format]

## Elevated Risk (41-60)
[Same format]

## Interventions in Progress
| Account | Started | Intervention | Progress |
|---------|---------|--------------|----------|
| [Name] | [Date] | [Type] | [Status] |

## Outcomes This Week
- Saved: [X accounts, $ARR]
- Lost: [X accounts, $ARR, reasons]
- De-escalated: [X accounts]
```

## Red Flags

- **Model overfit**: Perfect on training data, poor on new data
- **Signal lag**: Indicators trigger too late for intervention
- **False positive fatigue**: Too many alerts that aren't real risk
- **Missing signals**: Key churn predictors not tracked
- **Score opacity**: Team doesn't understand why scores change
- **Intervention mismatch**: Same playbook for different problems
- **No feedback loop**: Not learning from save attempts
- **Data quality**: Missing or stale underlying data

## Model Validation Metrics

| Metric | What It Measures | Target |
|--------|------------------|--------|
| Accuracy | Overall correct predictions | 80%+ |
| Precision | True positives / All predicted positives | 70%+ |
| Recall | True positives / All actual churns | 85%+ |
| Lead Time | Days from high risk to actual churn | 60+ days |
| False Positive Rate | False alarms / All high-risk alerts | < 30% |
| Save Rate | Saved / Attempted saves | 40%+ |
| AUC-ROC | Model discrimination ability | 0.75+ |
