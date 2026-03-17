---
name: churn-prediction
description: Identify at-risk customers using behavioral signals, engagement patterns, and health indicators before they cancel
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Churn Prediction

> Detect early warning signals of customer churn through systematic analysis of usage patterns, support interactions, and relationship health.

## When to Use This Skill

- Monthly/quarterly churn risk reviews
- Prioritizing CSM intervention
- Building early warning systems
- Post-mortem analysis on lost customers
- Executive churn reporting

## Methodology Foundation

Based on **Lincoln Murphy's Churn Analysis** and **ProfitWell Retention Research**, analyzing:
- Product engagement decay
- Support sentiment trends
- Payment behavior changes
- Relationship deterioration
- Competitive signals

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Identifies risk signals | Save vs. let go decisions |
| Calculates risk scores | Resource allocation |
| Suggests interventions | Discount/concession offers |
| Prioritizes at-risk accounts | Executive escalation timing |
| Analyzes churn patterns | Retention strategy changes |

## What This Skill Does

1. **Signal detection** - Identify behavioral indicators of churn risk
2. **Risk scoring** - Calculate churn probability
3. **Root cause analysis** - Why are they likely to leave?
4. **Intervention planning** - What actions could save them?
5. **Pattern recognition** - Learn from past churned accounts

## How to Use

```
Assess churn risk for this customer:

Account: [Company Name]
Contract: $[ARR], Renewal: [Date]
Tenure: [Months]

Usage Signals:
- Login frequency: [trend]
- Feature adoption: [% and trend]
- Active users: [current vs licensed]
- Key feature usage: [specific metrics]

Support Signals:
- Recent tickets: [count and nature]
- CSAT trend: [improving/stable/declining]
- Escalations: [any open or recent]
- Sentiment: [last few interactions]

Relationship Signals:
- Champion status: [engaged/disengaged/left]
- Exec sponsor: [status]
- NPS response: [score and comments]
- QBR attendance: [pattern]

Financial Signals:
- Payment status: [current/late]
- Contract discussions: [any mentions of changes]
- Competitor mentions: [any signals]
```

## Instructions

### Step 1: Evaluate Leading Indicators

**30-60 Day Warning Signs:**
| Signal | Risk Level | Weight |
|--------|------------|--------|
| Login drop >50% | High | 15 |
| Feature usage stopped | High | 15 |
| Support tickets spike | Medium | 10 |
| Champion left | Critical | 20 |
| Negative NPS | High | 12 |
| Payment late | Medium | 8 |
| No QBR attendance | Medium | 8 |
| Competitor mentioned | High | 12 |

### Step 2: Calculate Churn Probability

**Risk Score Formula:**
```
Churn Risk = Sum of weighted signals / 100

Score Ranges:
- 0-20: Low Risk (normal attention)
- 21-40: Moderate Risk (proactive outreach)
- 41-60: High Risk (intervention required)
- 61-80: Critical Risk (executive escalation)
- 81-100: Imminent Churn (save or plan exit)
```

### Step 3: Identify Root Cause Category

| Category | Indicators | Typical Save Rate |
|----------|------------|-------------------|
| Product Fit | Low adoption, wrong use case | 30% |
| Value Gap | Not seeing ROI, budget pressure | 45% |
| Service Issue | Support failures, unresolved bugs | 60% |
| Relationship | Champion left, no engagement | 35% |
| Competition | Actively evaluating others | 25% |
| Business Change | M&A, budget cuts, pivot | 15% |

### Step 4: Prescribe Intervention

**By Root Cause:**

| Cause | Primary Action | Secondary Action |
|-------|----------------|------------------|
| Product Fit | Success planning | Right-size contract |
| Value Gap | ROI review | Executive sponsor call |
| Service Issue | Escalation + resolution | Service credits |
| Relationship | New champion dev | Executive mapping |
| Competition | Competitive defense | Pricing review |
| Business | Flexible terms | Pause option |

### Step 5: Create Save Plan

**90-Day Save Framework:**
- **Days 1-7**: Triage and stabilize
- **Days 8-30**: Address root cause
- **Days 31-60**: Rebuild value perception
- **Days 61-90**: Secure commitment

## Examples

### Example 1: High-Risk Account

**Input:**
```
Account: MediaTech Corp
Contract: $96K ARR, Renewal: April 15 (45 days)
Tenure: 18 months

Usage Signals:
- Logins: Down 65% last 30 days
- Feature adoption: 35% (was 60%)
- Active users: 8 of 25 licensed
- Core feature: Stopped using analytics module

Support Signals:
- Tickets: 8 this month (normally 2)
- CSAT: Dropped from 4.5 to 3.2
- Escalation: 1 open (data export issue)
- Sentiment: Last 3 interactions negative

Relationship Signals:
- Champion: VP Marketing left 6 weeks ago
- Exec sponsor: Never established
- NPS: 4 (was 8 six months ago)
- QBR: Cancelled last two

Financial Signals:
- Payment: Current
- Mentions: "Evaluating options" in last call
- Competitor: Saw CompetitorX demo on their calendar
```

**Output:**
```
## Churn Risk Assessment: MediaTech Corp

### 🔴 CRITICAL RISK - 78/100

**Churn Probability: 75-85%**
**Time to Action: Immediate**

---

### Risk Signal Analysis

| Signal | Finding | Points |
|--------|---------|--------|
| Usage drop 65% | Critical | 15/15 |
| Feature stopped | Analytics abandoned | 15/15 |
| Champion left | No replacement | 20/20 |
| NPS Detractor | Dropped 4 points | 12/12 |
| Competitor eval | Demo scheduled | 12/12 |
| No QBR | 2 cancelled | 8/8 |
| **Total** | | **78/100** |

### Root Cause Analysis

**Primary: Relationship Void** (Champion departure)
- VP Marketing left 6 weeks ago
- No executive sponsor ever established
- Organizational knowledge lost
- No one internally championing value

**Secondary: Value Gap** (Product not delivering)
- Usage collapse suggests not getting value
- Analytics module abandoned = key feature unused
- May have been champion-dependent usage

**Tertiary: Active Competition**
- CompetitorX demo on calendar
- "Evaluating options" language
- Classic exit signals

### Competitor Intelligence

**CompetitorX Positioning:**
- Likely pitching: Simpler interface, lower price
- Their weakness: Less robust analytics
- Our defense: Depth of features, integration

### 90-Day Save Plan

**WEEK 1: Emergency Triage**

| Day | Action | Owner |
|-----|--------|-------|
| 1 | Resolve data export escalation | Support |
| 1 | CSM call to understand situation | CSM |
| 2 | Identify new potential champion | CSM |
| 3 | VP CS call to express commitment | VP CS |
| 5 | Executive sponsor outreach (their CMO) | CRO |

**WEEK 2-4: Stabilize**
- [ ] Close escalation completely
- [ ] Meet new champion (find one!)
- [ ] Re-onboard inactive users
- [ ] Document value delivered to date
- [ ] Competitive battle card preparation

**WEEK 5-8: Rebuild Value**
- [ ] ROI review presentation
- [ ] Success planning session
- [ ] Showcase new features
- [ ] Get 3 quick wins documented

**WEEK 9-12: Secure Renewal**
- [ ] QBR with exec attendance
- [ ] Renewal discussion
- [ ] Multi-year incentive if appropriate
- [ ] Reference/case study request (confidence signal)

### Save Probability Assessment

| If We... | Save Probability |
|----------|------------------|
| Do nothing | 15% |
| Standard outreach | 25% |
| Execute full plan | 45% |
| Add discount/concession | 55% |
| Exec-to-exec + plan | 60% |

### Decision Point

**Recommended: Full save effort**
- $96K ARR worth 60-90 hours of CSM time
- Cost to acquire replacement: ~$30K
- Reputation risk if churns

**If No Traction by Day 30:**
- Prepare for graceful offboarding
- Offer reduced contract if budget issue
- Maintain relationship for potential return
```

### Example 2: Cohort Churn Analysis

**Input:**
```
Analyze churn patterns from these 10 churned accounts:

1. AlphaCo: Left after 8 months, champion left, low usage
2. BetaTech: Left after 14 months, pricing, competitor win
3. GammaCorp: Left after 6 months, wrong fit, never adopted
4. DeltaInc: Left after 24 months, budget cuts, loved product
5. EchoSys: Left after 10 months, support issues, 3 escalations
6. FoxtrotLLC: Left after 18 months, competitor, champion left
7. GolfCo: Left after 4 months, implementation failed
8. HotelGrp: Left after 12 months, didn't see ROI
9. IndiaInc: Left after 9 months, champion left, low NPS
10. JulietCorp: Left after 20 months, M&A, product deprecated
```

**Output:**
```
## Churn Cohort Analysis: Q4 Losses

### Summary
- **Total Churned**: 10 accounts
- **Total ARR Lost**: [Calculate from data]
- **Average Tenure**: 12.5 months

---

### Root Cause Distribution

| Root Cause | Count | % | Avg Tenure |
|------------|-------|---|------------|
| Champion Left | 4 | 40% | 11.3 mo |
| Competitor | 3 | 30% | 17.3 mo |
| Product/Fit | 2 | 20% | 5.0 mo |
| Business Change | 2 | 20% | 22.0 mo |
| Service/Support | 1 | 10% | 10.0 mo |
| Value/ROI | 2 | 20% | 10.0 mo |

*Note: Some accounts had multiple causes*

### Key Insights

**1. Champion Dependency is Critical (40%)**
- 4 of 10 churns involved champion departure
- Average: Churned 3-4 months after champion left
- **Action**: Multi-threading program required

**2. Early Churn = Fit Problem**
- 3 accounts churned <6 months
- All had adoption/implementation issues
- **Action**: Improve qualification + onboarding

**3. Competitor Wins Correlate with Tenure**
- Competitor losses at 14, 18, 20 months
- Long enough to evaluate alternatives
- **Action**: Value reinforcement at 12-month mark

**4. Business Change is Uncontrollable**
- 2 churns from M&A/budget cuts
- Both were "happy" customers
- **Action**: Accept, maintain relationship

### Early Warning Signal Validation

| Signal | Present Before Churn | Lead Time |
|--------|---------------------|-----------|
| Champion left | 4/10 (40%) | 3-4 months |
| Usage drop >40% | 7/10 (70%) | 6-8 weeks |
| NPS drop | 6/10 (60%) | 2-3 months |
| Missed QBR | 5/10 (50%) | 3-4 months |
| Support spike | 3/10 (30%) | 4-6 weeks |

**Best Predictor**: Usage drop >40% (70% correlation)

### Preventability Assessment

| Account | Preventable? | What Would Have Helped |
|---------|--------------|------------------------|
| AlphaCo | Likely | Champion backup plan |
| BetaTech | Possibly | Competitive defense earlier |
| GammaCorp | Unlikely | Better qualification |
| DeltaInc | No | Business change |
| EchoSys | Likely | Faster escalation resolution |
| FoxtrotLLC | Possibly | Multi-thread + compete |
| GolfCo | Likely | Implementation oversight |
| HotelGrp | Likely | Proactive ROI review |
| IndiaInc | Likely | Champion backup |
| JulietCorp | No | M&A out of control |

**Preventability Rate**: 60% (6/10 could have been saved)

### Recommendations

**Process Changes:**
1. Implement champion backup contact rule (2+ contacts)
2. Add 12-month value review to CSM playbook
3. Create competitive defense triggers
4. Improve implementation success metrics

**Investment Areas:**
1. CSM capacity for proactive outreach
2. Competitive intelligence
3. Champion development program

**Metrics to Track:**
- Champion backup coverage %
- Time to first value
- Competitive mention alerts
- 12-month NPS trend
```

## Skill Boundaries

### What This Skill Does Well
- Systematic risk signal analysis
- Probability scoring with clear logic
- Root cause categorization
- Intervention planning

### What This Skill Cannot Do
- Access actual customer data
- Predict exact churn timing
- Know internal customer dynamics
- Replace relationship intuition

### When to Escalate to Human
- Strategic accounts (top 10%)
- Complex multi-product relationships
- Escalation requiring legal/exec involvement
- Pricing concession decisions

## Iteration Guide

### Follow-up Prompts
- "Create a 30-60-90 save plan for this account."
- "What competitive response should we prepare?"
- "Which of my at-risk accounts should I prioritize?"
- "Analyze the pattern across all my churned accounts."

### Monitoring Cadence
1. Score all accounts monthly
2. Alert on score drops >15 points
3. Weekly review of Critical/High risk
4. Quarterly pattern analysis

## Checklists & Templates

### At-Risk Account Checklist
- [ ] Usage trend analyzed (30/60/90 day)
- [ ] Support sentiment reviewed
- [ ] Champion status confirmed
- [ ] NPS collected or requested
- [ ] Competitor signals checked
- [ ] Financial health verified
- [ ] Save plan documented

## References

- Lincoln Murphy's Churn Analysis Framework
- ProfitWell Retention Benchmarks
- Gainsight Customer Health Methodology
- ChurnZero Predictive Analytics

## Related Skills

- `account-health` - Broader health scoring
- `health-score-monitor` - Continuous monitoring
- `renewal-management` - Renewal process

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 20-30 min per account
- **Prerequisites**: Customer data, history, context
