---
name: health-score-monitor
description: Design and maintain customer health scoring systems with automated alerts and trending analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Health Score Monitor

> Build systematic customer health monitoring with composite scores, trend tracking, and automated alerting for proactive customer success.

## When to Use This Skill

- Designing health score frameworks
- Setting up monitoring dashboards
- Creating alert thresholds
- Analyzing health trends across portfolio
- Optimizing existing health models

## Methodology Foundation

Based on **Gainsight Health Score Design** and **Totango Customer Success metrics**, focusing on:
- Multi-dimensional scoring
- Leading vs lagging indicators
- Score normalization
- Trend analysis
- Alert prioritization

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs scoring framework | Dimension weights |
| Calculates composite scores | Alert thresholds |
| Identifies trending patterns | Intervention triggers |
| Suggests monitoring cadence | Resource allocation |
| Recommends improvements | Business rule exceptions |

## What This Skill Does

1. **Framework design** - Multi-factor health model
2. **Score calculation** - Weighted composite scores
3. **Trend analysis** - Direction and velocity
4. **Alert rules** - When to notify teams
5. **Portfolio view** - Aggregate health visibility

## How to Use

```
Design a health score monitor for my customer portfolio:

Business Context:
- Product type: [SaaS/Platform/Service]
- Contract model: [Annual/Monthly/Multi-year]
- Key value metric: [What shows customer success?]
- CSM:Account ratio: [1:X]

Available Data Points:
- Product: [List usage metrics available]
- Support: [List support metrics available]
- Financial: [List financial signals]
- Relationship: [List engagement data]

Current Challenges:
- [What's not working with current approach?]
```

## Instructions

### Step 1: Define Health Dimensions

**Standard 4-Pillar Model:**

| Dimension | Weight | What It Answers |
|-----------|--------|-----------------|
| **Product** | 30-40% | Are they using it? |
| **Support** | 15-25% | Are they happy? |
| **Financial** | 20-25% | Are they paying/growing? |
| **Relationship** | 20-25% | Are we connected? |

Adjust weights based on your business:
- High-touch: Increase Relationship
- Usage-based pricing: Increase Product
- Support-intensive: Increase Support

### Step 2: Select Metrics per Dimension

**Product Health Metrics:**
| Metric | Type | Scoring |
|--------|------|---------|
| DAU/MAU | Leading | % of benchmark |
| Feature adoption | Leading | % features used |
| Time in product | Leading | Minutes vs avg |
| Key feature usage | Leading | Yes/No or frequency |
| Usage trend | Leading | Up/Flat/Down |

**Support Health Metrics:**
| Metric | Type | Scoring |
|--------|------|---------|
| CSAT score | Lagging | 1-5 scale |
| Ticket volume | Leading | vs baseline |
| Escalations | Leading | Count (negative) |
| Response sentiment | Leading | Positive/Neutral/Negative |
| Time to resolution | Lagging | vs SLA |

**Financial Health Metrics:**
| Metric | Type | Scoring |
|--------|------|---------|
| Payment status | Lagging | Current/Late |
| Expansion | Leading | Pipeline/Discussion |
| Contract type | Lagging | Multi-year bonus |
| Renewal date | Context | Days remaining |
| ARR trend | Lagging | Growth/Flat/Decline |

**Relationship Health Metrics:**
| Metric | Type | Scoring |
|--------|------|---------|
| Champion engaged | Leading | Active/Passive/None |
| Exec sponsor | Leading | Yes/No |
| NPS/CSAT | Lagging | Score |
| QBR attendance | Leading | Regular/Sporadic/None |
| Last touch | Leading | Days since contact |

### Step 3: Create Scoring Rules

**Example Scoring Matrix:**

```
Product Score (0-100):
+30: DAU/MAU > 70%
+20: DAU/MAU 50-70%
+10: DAU/MAU 30-50%
+0:  DAU/MAU < 30%

+25: Feature adoption > 60%
+15: Feature adoption 40-60%
+5:  Feature adoption < 40%

+20: Usage trending up
+10: Usage stable
-10: Usage trending down

+15: Key feature used weekly
+5:  Key feature used monthly
-10: Key feature abandoned

Max: 100 (or normalize)
```

### Step 4: Set Alert Thresholds

| Condition | Alert Level | Action |
|-----------|-------------|--------|
| Score drops >15 pts | 🔴 Critical | Immediate CSM review |
| Score below 40 | 🟠 High | Intervention required |
| Score 40-60 | 🟡 Medium | Proactive outreach |
| Renewal <60 days + <60 score | 🔴 Critical | Save plan |
| Usage drop >30% WoW | 🟡 Medium | Check-in call |

### Step 5: Define Monitoring Cadence

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Score refresh | Daily/Weekly | Automated |
| Alert review | Daily | CSM |
| Portfolio review | Weekly | CS Manager |
| Model calibration | Quarterly | CS Ops |

## Examples

### Example 1: SaaS Health Score Design

**Input:**
```
Design health score for our B2B SaaS platform:

Business Context:
- Product: Project management software
- Contract: Annual, avg $50K
- Value metric: Projects completed, team adoption
- CSM ratio: 1:40

Available Data:
- Product: Logins, projects created, tasks completed, integrations used
- Support: Zendesk tickets, CSAT, NPS
- Financial: ARR, payment status, expansion pipeline
- Relationship: Meeting attendance, email engagement

Challenges:
- Too many "yellow" accounts, can't prioritize
- Alerts are noisy, CSMs ignoring them
```

**Output:**
```
## Health Score Framework: Project Management SaaS

### Design Principles

Given 1:40 ratio and "alert fatigue" issue:
1. **Prioritize leading indicators** - Catch issues early
2. **Reduce noise** - Tighter alert thresholds
3. **Enable triage** - Clear Red/Yellow/Green actions

---

### Scoring Model

#### Dimension Weights
| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Product | 40% | Usage = value realization |
| Support | 15% | Lower touch model |
| Financial | 25% | Contract health critical |
| Relationship | 20% | Moderate touch needed |

---

#### Product Score (40 points max)

| Metric | Criteria | Points |
|--------|----------|--------|
| **Weekly Active Users** | | |
| | >70% of seats | 12 |
| | 50-70% | 8 |
| | 30-50% | 4 |
| | <30% | 0 |
| **Projects Created (monthly)** | | |
| | >5 per user | 10 |
| | 2-5 per user | 6 |
| | <2 per user | 2 |
| **Tasks Completed** | | |
| | >80% completion rate | 8 |
| | 50-80% | 5 |
| | <50% | 0 |
| **Integrations** | | |
| | 2+ active | 6 |
| | 1 active | 3 |
| | None | 0 |
| **Usage Trend** | | |
| | Increasing | 4 |
| | Stable | 2 |
| | Declining | -4 |

---

#### Support Score (15 points max)

| Metric | Criteria | Points |
|--------|----------|--------|
| **CSAT** | | |
| | >4.5 | 6 |
| | 4.0-4.5 | 4 |
| | 3.5-4.0 | 2 |
| | <3.5 | 0 |
| **Ticket Volume** | | |
| | Below baseline | 5 |
| | At baseline | 3 |
| | 2x+ baseline | 0 |
| **Escalations** | | |
| | None (90 days) | 4 |
| | Resolved | 2 |
| | Open | -4 |

---

#### Financial Score (25 points max)

| Metric | Criteria | Points |
|--------|----------|--------|
| **Payment Status** | | |
| | Current | 10 |
| | 30 days late | 5 |
| | 60+ days | 0 |
| **Expansion** | | |
| | Closed this year | 8 |
| | In discussion | 5 |
| | No opportunity | 2 |
| **Contract Type** | | |
| | Multi-year | 7 |
| | Annual | 4 |
| | Month-to-month | 0 |

---

#### Relationship Score (20 points max)

| Metric | Criteria | Points |
|--------|----------|--------|
| **Champion Status** | | |
| | Active advocate | 8 |
| | Engaged | 5 |
| | Passive | 2 |
| | Gone/None | 0 |
| **NPS** | | |
| | 9-10 (Promoter) | 6 |
| | 7-8 (Passive) | 4 |
| | 0-6 (Detractor) | 0 |
| **Last Touch** | | |
| | <30 days | 6 |
| | 30-60 days | 4 |
| | 60-90 days | 2 |
| | >90 days | 0 |

---

### Health Bands

| Score | Status | Count Target | CSM Action |
|-------|--------|--------------|------------|
| 80-100 | 🟢 Healthy | 60% | Quarterly touch, expansion |
| 60-79 | 🟡 Monitor | 25% | Monthly touch, watch trends |
| 40-59 | 🟠 At Risk | 12% | Bi-weekly, intervention plan |
| 0-39 | 🔴 Critical | 3% | Weekly, executive escalation |

**Target Distribution** at 1:40 ratio:
- 24 Healthy (quarterly = 8 touches/month)
- 10 Monitor (monthly = 10 touches)
- 5 At Risk (bi-weekly = 10 touches)
- 1 Critical (weekly = 4 touches)
- **Total: 32 touch points/month** (manageable)

---

### Alert Rules (Noise Reduction)

**Only Alert When:**

| Alert | Condition | Frequency |
|-------|-----------|-----------|
| 🔴 Critical New | Score drops below 40 | Immediate |
| 🔴 Renewal Risk | Score <60 AND renewal <60 days | Immediate |
| 🟠 Score Drop | Drops >15 points in 7 days | Daily digest |
| 🟡 Watch | Usage down >30% WoW | Weekly digest |

**Suppress Alerts For:**
- Accounts <30 days old (onboarding)
- Accounts in active implementation
- Known seasonal low periods
- Manual "snooze" by CSM

---

### Dashboard Views

**Portfolio Summary:**
```
┌─────────────────────────────────────┐
│ My Portfolio: 40 accounts           │
├─────────────────────────────────────┤
│ 🟢 24 (60%)  │ 🟡 10 (25%)         │
│ 🟠  5 (12%)  │ 🔴  1 (3%)          │
├─────────────────────────────────────┤
│ ⚠️ 3 accounts dropped this week    │
│ 📈 5 accounts improved             │
└─────────────────────────────────────┘
```

**Account Drill-Down:**
```
┌─────────────────────────────────────┐
│ Account: TechCorp | Score: 62 🟡    │
├─────────────────────────────────────┤
│ Product:      28/40  ████████░░    │
│ Support:      12/15  █████████░    │
│ Financial:    14/25  ██████░░░░    │
│ Relationship: 8/20   ████░░░░░░    │
├─────────────────────────────────────┤
│ Trend: ↘️ -8 pts (30 days)          │
│ Renewal: 90 days                    │
│ Action: Schedule check-in          │
└─────────────────────────────────────┘
```
```

### Example 2: Health Trend Analysis

**Input:**
```
Analyze health trends for my portfolio:

Q4 Scores:
- Oct: 23 Green, 12 Yellow, 4 Orange, 1 Red
- Nov: 20 Green, 14 Yellow, 5 Orange, 1 Red
- Dec: 18 Green, 13 Yellow, 7 Orange, 2 Red

Also:
- 3 accounts churned in Q4
- 2 expansions closed
- NPS survey: 42 average (was 48)
```

**Output:**
```
## Q4 Health Trend Analysis

### Portfolio Drift Summary

| Status | Oct | Nov | Dec | Change |
|--------|-----|-----|-----|--------|
| 🟢 Green | 23 (58%) | 20 (50%) | 18 (45%) | ↘️ -13% |
| 🟡 Yellow | 12 (30%) | 14 (35%) | 13 (33%) | → +3% |
| 🟠 Orange | 4 (10%) | 5 (13%) | 7 (18%) | ↗️ +8% |
| 🔴 Red | 1 (2%) | 1 (2%) | 2 (5%) | ↗️ +3% |

**Trend: ⚠️ Deteriorating**
- 5 accounts moved from Green to lower status
- Orange/Red grew from 12% to 23%
- Portfolio health declining month-over-month

---

### Churn Correlation

| Churned Account | Last Score | Days at Red |
|-----------------|------------|-------------|
| Account A | 28 | 45 days |
| Account B | 35 | 30 days |
| Account C | 41 | 22 days |

**Insight**: All churned accounts were Red/Orange for 20+ days
**Action**: Accounts at Orange >14 days need intervention

---

### Key Drivers of Decline

**Analyzing accounts that dropped:**

| Factor | Accounts Affected | Avg Point Drop |
|--------|-------------------|----------------|
| Usage decline | 8 | -12 pts |
| Champion change | 3 | -18 pts |
| Support issues | 4 | -8 pts |
| Payment delays | 2 | -6 pts |

**Primary Driver**: Usage decline (likely seasonal + holiday)

---

### NPS Correlation

| NPS Segment | Avg Health Score | Q4 Change |
|-------------|------------------|-----------|
| Promoters (9-10) | 78 | -3 |
| Passives (7-8) | 58 | -6 |
| Detractors (0-6) | 38 | -10 |

**Insight**: Detractor scores dropping fastest
**Action**: Prioritize intervention for Detractors

---

### Q1 Recommendations

**Immediate (Week 1):**
1. Save plan for 2 Red accounts
2. Intervention for 7 Orange accounts
3. Outreach to 3 champion-change accounts

**Short-term (Month 1):**
1. Re-engagement campaign for low-usage accounts
2. Proactive support reach-out to ticket-heavy accounts
3. NPS follow-up calls with Detractors

**Strategic (Quarter):**
1. Investigate seasonal patterns (plan for Q4 2026)
2. Champion backup program implementation
3. Revisit Orange threshold (too many?)

---

### Target for Q1

| Status | Dec | Q1 Target | Delta |
|--------|-----|-----------|-------|
| 🟢 Green | 18 | 22 | +4 |
| 🟡 Yellow | 13 | 14 | +1 |
| 🟠 Orange | 7 | 3 | -4 |
| 🔴 Red | 2 | 1 | -1 |

**Success = Move 5 accounts up at least one tier**
```

## Skill Boundaries

### What This Skill Does Well
- Designing health frameworks
- Calculating composite scores
- Identifying trends and patterns
- Setting alert thresholds

### What This Skill Cannot Do
- Access your actual data
- Implement in your systems
- Know your specific business rules
- Replace data engineering

### When to Escalate to Human
- Threshold decisions
- Weight calibration based on churn data
- Alert rule tuning
- Cross-functional alignment

## Iteration Guide

### Follow-up Prompts
- "How should I weight these dimensions differently for enterprise vs SMB?"
- "What metrics should I add for a usage-based pricing model?"
- "Create alert rules that reduce noise by 50%."
- "Design a health score for a high-touch services business."

## References

- Gainsight Health Score Best Practices
- Totango Customer Health Methodology
- ChurnZero Scoring Framework
- Customer Success Benchmarks

## Related Skills

- `churn-prediction` - Deeper churn analysis
- `account-health` - RevOps perspective
- `expansion-signals` - Growth focus

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 2-4 hours for framework design
- **Prerequisites**: Data availability assessment
