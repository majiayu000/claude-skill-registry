---
name: Sales Pipeline Manager
slug: sales-pipeline
description: Track sales opportunities, manage deals, forecast revenue, and optimize conversion rates
category: business
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "sales pipeline"
  - "track deals"
  - "sales forecast"
  - "opportunity management"
  - "crm"
  - "sales metrics"
tags:
  - sales
  - crm
  - revenue
  - forecasting
  - business-operations
---

# Sales Pipeline Manager

Expert sales pipeline management system that helps you track opportunities, manage deals through stages, forecast revenue, and optimize your sales process. This skill provides structured workflows for deal tracking, pipeline analysis, conversion optimization, and revenue forecasting based on proven sales methodologies.

Whether you're managing a B2B enterprise sales cycle or a high-velocity transactional pipeline, this skill helps you maintain visibility, identify bottlenecks, and make data-driven decisions to improve close rates and accelerate revenue growth.

Built on best practices from sales operations leaders and CRM systems, this skill combines pipeline hygiene, forecasting rigor, and actionable insights to help you hit your numbers consistently.

## Core Workflows

### Workflow 1: Pipeline Setup & Configuration
**Define your sales stages, qualifying criteria, and tracking metrics**

1. **Stage Definition**
   - Define pipeline stages (e.g., Lead, Qualified, Proposal, Negotiation, Closed-Won/Lost)
   - Set qualifying criteria for each stage transition
   - Establish expected conversion rates per stage
   - Define average time-in-stage benchmarks

2. **Deal Fields & Data Structure**
   - Configure required fields: Company, Contact, Value, Close Date, Probability
   - Add custom fields: Source, Product, Region, Rep, Next Steps
   - Define deal sizing tiers (small, medium, large, enterprise)
   - Set up tagging and categorization

3. **Tracking & Metrics Setup**
   - Define key metrics: Pipeline value, weighted pipeline, velocity, conversion rates
   - Set quota and target thresholds
   - Configure reporting periods (weekly, monthly, quarterly)
   - Establish pipeline coverage ratios (3x-5x quota recommended)

### Workflow 2: Deal Tracking & Management
**Add, update, and move deals through your pipeline**

1. **New Deal Entry**
   - Capture deal basics: Company name, contact, opportunity description
   - Assign deal value and expected close date
   - Set probability/stage (use stage-based probabilities: Lead 10%, Qualified 25%, Proposal 50%, etc.)
   - Document deal source and initial context

2. **Deal Updates & Progression**
   - Log activities: calls, meetings, demos, proposals sent
   - Update stage when qualifying criteria met
   - Adjust close date and value as intelligence improves
   - Document next steps and blockers

3. **Deal Hygiene & Reviews**
   - Weekly pipeline reviews: Validate close dates, update probabilities
   - Identify stale deals (no activity in 14+ days)
   - Push/pull decisions on borderline opportunities
   - Close lost deals with reason codes

### Workflow 3: Pipeline Analysis & Forecasting
**Analyze pipeline health and generate revenue forecasts**

1. **Pipeline Health Metrics**
   - Calculate total pipeline value by stage
   - Measure weighted pipeline (value × probability)
   - Track conversion rates between stages
   - Monitor average deal size and sales cycle length

2. **Revenue Forecasting**
   - Generate commit forecast (high-probability deals)
   - Calculate best-case and worst-case scenarios
   - Identify pipeline gaps vs. quota
   - Project quarterly/annual run rates

3. **Bottleneck Identification**
   - Find stages with low conversion rates
   - Identify deals stuck in stages too long
   - Analyze win/loss patterns by segment
   - Spot trends by source, product, or rep

### Workflow 4: Sales Process Optimization
**Improve conversion rates and accelerate velocity**

1. **Conversion Analysis**
   - Compare actual vs. expected conversion rates by stage
   - Identify drop-off points in the funnel
   - Segment analysis (by size, source, product)
   - A/B test process changes

2. **Velocity Improvement**
   - Measure time-in-stage by deal characteristics
   - Identify accelerators and decelerators
   - Optimize handoffs between stages
   - Reduce friction in approval/legal processes

3. **Win/Loss Analysis**
   - Document win/loss reasons
   - Identify competitive patterns
   - Refine ideal customer profile
   - Adjust pricing and positioning strategies

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Set up new pipeline | "Create sales pipeline structure" |
| Add new deal | "Add deal: [Company] - [Value] - [Stage]" |
| Update deal stage | "Move [Deal] to [Stage]" |
| Pipeline review | "Show pipeline summary" |
| Revenue forecast | "Forecast revenue for [Period]" |
| Conversion analysis | "Analyze conversion rates" |
| Identify at-risk deals | "Show stale deals" |
| Win/loss analysis | "Analyze closed deals [Period]" |
| Pipeline gaps | "Calculate pipeline gap vs quota" |
| Deal velocity | "Show average sales cycle" |

## Best Practices

### Pipeline Hygiene
- Update deals weekly at minimum (daily for high-velocity)
- Close lost deals promptly with documented reasons
- Archive won deals with success factors
- Maintain 3-5x pipeline coverage of quota
- Enforce stage exit criteria rigorously

### Data Quality
- Use consistent naming conventions for companies
- Validate close dates monthly (push forward if unrealistic)
- Update probabilities based on actual activity, not hope
- Document all customer interactions and next steps
- Tag deals with relevant attributes for segmentation

### Forecasting Discipline
- Separate commit, best-case, and pipeline categories
- Only include deals with recent activity in forecast
- Weight by probability, not wishful thinking
- Review forecast accuracy monthly to calibrate
- Adjust stage probabilities based on historical data

### Process Improvement
- Review conversion rates quarterly
- Test process changes on cohorts before broad rollout
- Document what works in repeatable playbooks
- Share wins and lessons across the team
- Continuously refine ideal customer profile

### Communication & Reporting
- Weekly pipeline reviews with clear actions
- Monthly forecast calls with executive stakeholders
- Quarterly business reviews analyzing trends
- Real-time dashboards for visibility
- Automated alerts for at-risk deals

### Common Pitfalls to Avoid
- Sandbaggin (hiding deals to beat expectations)
- Happy ears (inflating probabilities without evidence)
- Zombie deals (keeping dead deals alive artificially)
- Inconsistent stage definitions across reps
- Lack of activity logging making deals opaque
- Poor close date hygiene (everything closes end of quarter)

## Integration Points

- **CRM Systems**: Salesforce, HubSpot, Pipedrive
- **Communication**: Slack/Teams alerts for deal milestones
- **Calendar**: Link meetings to deal activities
- **Email**: Track proposal sends and customer responses
- **Analytics**: Export data for deeper analysis in BI tools
- **Forecasting Tools**: Sync with financial planning systems

## Metrics to Track

**Pipeline Metrics:**
- Total pipeline value
- Weighted pipeline (probability-adjusted)
- Pipeline coverage ratio (pipeline ÷ quota)
- Number of opportunities by stage
- Average deal size

**Velocity Metrics:**
- Average sales cycle length
- Time-in-stage by stage
- Deal velocity (value ÷ days in pipeline)
- Stage progression rate

**Conversion Metrics:**
- Lead → Qualified conversion rate
- Qualified → Proposal conversion rate
- Proposal → Closed-Won conversion rate
- Overall win rate
- Win rate by segment/product

**Forecasting Metrics:**
- Forecast accuracy (actual vs. predicted)
- Commit attainment rate
- Quarter-over-quarter growth
- Pipeline generation rate
- Pipeline decay rate
