---
name: account-health
description: Assess customer account health using product usage, support sentiment, payment status, and relationship signals
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Account Health Scoring

> Evaluate customer account health through multi-dimensional analysis to predict retention, identify expansion opportunities, and prevent churn.

## When to Use This Skill

- Monthly/quarterly account reviews
- Building customer health dashboards
- Prioritizing CSM attention
- Identifying expansion opportunities
- Churn risk assessment

## Methodology Foundation

Based on **Gainsight Customer Health methodology** and **Lincoln Murphy's Customer Success principles**, combining:
- Product adoption metrics
- Support/sentiment signals
- Financial health (payments, expansion)
- Relationship strength (engagement)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs health score framework | Weight of each factor |
| Calculates composite scores | Threshold for intervention |
| Identifies risk signals | Resource allocation |
| Suggests actions by score | Escalation decisions |
| Tracks trend direction | Account save vs. let go |

## What This Skill Does

1. **Framework design** - Multi-factor health scoring model
2. **Score calculation** - Weighted composite health score
3. **Risk identification** - Early warning signals
4. **Trend analysis** - Health trajectory over time
5. **Action recommendations** - Interventions by health status

## How to Use

```
Assess health for this account:

Account: [Company Name]
Contract: $[ARR], [Renewal Date]
Tenure: [Months as customer]

Product Usage:
- Daily active users: X / Y licensed
- Feature adoption: X% of features used
- Login frequency: [Daily/Weekly/Monthly]
- Last login: [Date]

Support:
- Tickets this quarter: X
- CSAT score: X/5
- Open escalations: X
- Last interaction sentiment: [Positive/Neutral/Negative]

Financial:
- Payment status: [Current/Late/At Risk]
- Expansion conversations: [Yes/No]
- Contract modifications: [None/Downgrade/Upgrade]

Relationship:
- Executive sponsor: [Active/Passive/Gone]
- Champion status: [Strong/Weak/Churned]
- NPS score: X
- QBR attendance: [Regular/Sporadic/None]
```

## Instructions

### Step 1: Define Health Dimensions (4 Pillars)

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Product | 30% | Are they using the product? |
| Support | 20% | Are they happy with service? |
| Financial | 25% | Are they paying and growing? |
| Relationship | 25% | Do we have strong contacts? |

### Step 2: Score Each Dimension (0-100)

**Product Health (30%):**
| Metric | Score |
|--------|-------|
| DAU/MAU > 70% | +30 |
| DAU/MAU 50-70% | +20 |
| DAU/MAU 30-50% | +10 |
| DAU/MAU < 30% | +0 |
| Feature adoption > 60% | +25 |
| Feature adoption 40-60% | +15 |
| Feature adoption < 40% | +5 |
| No login 7+ days | -20 |
| No login 30+ days | -40 |
| Usage trending up | +15 |
| Usage trending down | -15 |

**Support Health (20%):**
| Metric | Score |
|--------|-------|
| CSAT > 4.5 | +30 |
| CSAT 4.0-4.5 | +20 |
| CSAT 3.5-4.0 | +10 |
| CSAT < 3.5 | +0 |
| No escalations | +25 |
| Resolved escalations | +15 |
| Open escalations | -20 |
| Negative sentiment | -25 |
| Tickets trending down | +10 |
| Tickets trending up | -10 |

**Financial Health (25%):**
| Metric | Score |
|--------|-------|
| Payment current | +30 |
| Payment 30 days late | +10 |
| Payment 60+ days late | -20 |
| Expansion discussion | +20 |
| Upgrade completed | +30 |
| Downgrade risk | -30 |
| Multi-year contract | +20 |
| Month-to-month | -10 |

**Relationship Health (25%):**
| Metric | Score |
|--------|-------|
| Exec sponsor active | +30 |
| Champion engaged | +25 |
| NPS Promoter (9-10) | +25 |
| NPS Passive (7-8) | +10 |
| NPS Detractor (0-6) | -20 |
| Regular QBR attendance | +20 |
| No QBR in 6 months | -15 |
| Champion left company | -30 |

### Step 3: Calculate Composite Score

```
Health Score = (Product × 0.30) + (Support × 0.20) +
               (Financial × 0.25) + (Relationship × 0.25)
```

### Step 4: Assign Health Status

| Score | Status | Color | Action |
|-------|--------|-------|--------|
| 80-100 | Healthy | 🟢 Green | Expand, get referrals |
| 60-79 | Monitor | 🟡 Yellow | Proactive engagement |
| 40-59 | At Risk | 🟠 Orange | Intervention required |
| 0-39 | Critical | 🔴 Red | Executive escalation |

### Step 5: Identify Trend Direction

| Pattern | Signal | Action |
|---------|--------|--------|
| ↗️ Improving | Score up 10+ points | Continue current approach |
| → Stable | Score within 5 points | Monitor for changes |
| ↘️ Declining | Score down 10+ points | Immediate intervention |

## Examples

### Example 1: Healthy Account

**Input:**
```
Account: TechCorp Solutions
Contract: $120K ARR, Renewal: Sep 2026
Tenure: 24 months

Product Usage:
- DAU: 85 / 100 licensed (85%)
- Feature adoption: 72%
- Login frequency: Daily
- Last login: Today

Support:
- Tickets this quarter: 3 (minor issues)
- CSAT: 4.8/5
- Open escalations: 0
- Last interaction: Positive

Financial:
- Payment: Current
- Expansion: Discussing 20 more seats
- Contract: 2-year renewal signed

Relationship:
- Exec sponsor: CTO actively engaged
- Champion: VP Eng, very strong
- NPS: 9
- QBR: Quarterly, well-attended
```

**Output:**
```
## Account Health: TechCorp Solutions

### Overall Score: 92/100 🟢 HEALTHY

### Dimension Scores

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Product | 95 | 30% | 28.5 |
| Support | 90 | 20% | 18.0 |
| Financial | 95 | 25% | 23.8 |
| Relationship | 90 | 25% | 22.5 |
| **Total** | | | **92.8** |

### Score Breakdown

**Product Health: 95/100** ✅
- DAU/MAU at 85% (+30)
- Feature adoption 72% (+25)
- Daily logins (+20)
- Usage trending stable (+10)
- No concerning signals

**Support Health: 90/100** ✅
- CSAT 4.8 (+30)
- Only 3 minor tickets (+25)
- No escalations (+25)
- Positive sentiment (+10)

**Financial Health: 95/100** ✅
- Payment current (+30)
- Expansion in discussion (+20)
- Multi-year renewal signed (+30)
- No downgrade signals (+15)

**Relationship Health: 90/100** ✅
- CTO actively engaged (+30)
- Strong VP Eng champion (+25)
- NPS 9 (Promoter) (+25)
- Regular QBRs (+20)
- Slight gap: Could add more contacts (-10)

### Trend: → Stable (High)

### Recommended Actions

**Expansion Focus:**
1. Close the 20-seat expansion discussion
2. Introduce new product features for upsell
3. Request case study/testimonial

**Relationship Deepening:**
1. Add 1-2 more stakeholder relationships
2. Invite to customer advisory board
3. Offer early access to beta features

**Risk Mitigation:**
- Champion VP Eng is critical - ensure backup contact
- Document success metrics for renewal proof points
```

### Example 2: At-Risk Account

**Input:**
```
Account: RetailMax Inc
Contract: $85K ARR, Renewal: Apr 2026 (3 months)
Tenure: 18 months

Product Usage:
- DAU: 12 / 50 licensed (24%)
- Feature adoption: 35%
- Login frequency: Weekly
- Last login: 8 days ago

Support:
- Tickets this quarter: 12 (several complaints)
- CSAT: 3.2/5
- Open escalations: 2
- Last interaction: Negative (product complaints)

Financial:
- Payment: 15 days late
- Expansion: No discussions
- Contract: Mentioned budget cuts

Relationship:
- Exec sponsor: CFO, never met
- Champion: Original champion left 2 months ago
- NPS: 5 (Detractor)
- QBR: Skipped last 2
```

**Output:**
```
## Account Health: RetailMax Inc

### Overall Score: 31/100 🔴 CRITICAL

⚠️ **IMMEDIATE ATTENTION REQUIRED**
Renewal in 3 months with multiple critical risk factors.

### Dimension Scores

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Product | 20 | 30% | 6.0 |
| Support | 25 | 20% | 5.0 |
| Financial | 30 | 25% | 7.5 |
| Relationship | 20 | 25% | 5.0 |
| **Total** | | | **31** |

### Critical Risk Factors 🚨

1. **🔴 Champion Churned** (-30)
   - Original champion left 2 months ago
   - No replacement identified
   - Institutional knowledge lost

2. **🔴 Low Adoption** (24% DAU)
   - Only 12 of 50 users active
   - Indicates low perceived value
   - Hard to justify renewal

3. **🔴 NPS Detractor** (5)
   - Actively unhappy
   - May influence other buyers
   - Requires executive intervention

4. **🟠 Open Escalations** (2)
   - Unresolved issues damaging trust
   - Need immediate resolution

5. **🟠 Payment Late**
   - Could signal budget issues
   - "Budget cuts" mentioned

### Trend: ↘️ Declining

Score dropped ~25 points since champion departure.

### Save Plan: 90-Day Sprint

**Week 1: Triage**
- [ ] Resolve both open escalations
- [ ] CSM call with current users to assess sentiment
- [ ] Identify new potential champion
- [ ] Check payment status/AR outreach

**Week 2-4: Stabilize**
- [ ] Executive sponsor meeting (your VP + their CFO)
- [ ] Onboard new champion
- [ ] Re-training for low-adoption users
- [ ] Document 3 value proof points

**Week 5-8: Rebuild**
- [ ] Adoption bootcamp for inactive users
- [ ] Success planning session
- [ ] Get CSAT above 4.0
- [ ] Monthly check-ins scheduled

**Week 9-12: Renewal**
- [ ] QBR with full stakeholder group
- [ ] Renewal proposal with options
- [ ] Right-size if needed (reduce seats)
- [ ] Multi-year incentive if healthy

### If Save Fails
- Prepare for graceful offboarding
- Document learnings for post-mortem
- Maintain relationship for potential return
- Collect exit feedback

### Success Probability: 40%
Without new champion, save is difficult.
```

## Skill Boundaries

### What This Skill Does Well
- Structured health assessment framework
- Multi-factor scoring with clear logic
- Risk identification and prioritization
- Action recommendations by health tier

### What This Skill Cannot Do
- Access actual product usage data
- Predict specific churn timing
- Know internal customer politics
- Replace CSM relationship judgment

### When to Escalate to Human
- Accounts with complex multi-product relationships
- Strategic accounts with executive relationships
- Accounts involving legal or contractual disputes
- Save decisions requiring investment approval

## Iteration Guide

### Follow-up Prompts
- "What's the #1 action to improve this score by 20 points?"
- "Compare health scores for my top 10 accounts."
- "Build a 30-60-90 day save plan for this account."
- "What early warning signals should I watch for?"

### Continuous Monitoring
1. Score all accounts monthly
2. Alert on 10+ point drops
3. Segment by health tier
4. Track save success rates
5. Refine weights based on churn correlation

## Checklists & Templates

### Monthly Health Review Checklist
- [ ] Pull usage data for all accounts
- [ ] Update support sentiment scores
- [ ] Check payment status
- [ ] Review relationship changes
- [ ] Calculate health scores
- [ ] Triage critical accounts

### Health Score Template
```markdown
## Account: [Name] | Score: X/100 [Emoji]

**Contract**: $X ARR | Renewal: [Date] | Tenure: X months

### Scores
| Dimension | Score | Key Factor |
|-----------|-------|------------|
| Product | /100 | |
| Support | /100 | |
| Financial | /100 | |
| Relationship | /100 | |

### Top Risks
1.
2.

### Actions This Month
1.
2.
```

## References

- Gainsight Customer Health Best Practices
- Lincoln Murphy's Customer Success Metrics
- ChurnZero Customer Health Framework
- Totango Customer Health Scoring

## Related Skills

- `churn-prediction` - Deeper churn analysis
- `qbr-preparation` - Health-informed QBR prep
- `expansion-signals` - Identify growth opportunities

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 20-30 min per account
- **Prerequisites**: Usage data, support history, relationship context
