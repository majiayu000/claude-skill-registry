---
name: revenue-attribution
description: Analyze marketing and sales touchpoints to attribute revenue credit using multi-touch models and channel contribution analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Revenue Attribution

> Determine which marketing and sales activities drive revenue using multi-touch attribution models, enabling smarter budget allocation and campaign optimization.

## When to Use This Skill

- Justifying marketing spend to leadership
- Optimizing channel mix allocation
- Evaluating campaign ROI
- Resolving marketing/sales credit disputes
- Building attribution reports

## Methodology Foundation

Based on **Bizible/Marketo Multi-Touch Attribution** and **Google Analytics Attribution Models**, covering:
- First-touch attribution (awareness credit)
- Last-touch attribution (conversion credit)
- Linear attribution (equal credit)
- Time-decay attribution (recency-weighted)
- Position-based (U-shaped, W-shaped)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Explains attribution models | Which model fits your business |
| Calculates credit distribution | How to act on insights |
| Identifies top-performing channels | Budget reallocation amounts |
| Shows model comparison | Final attribution policy |
| Highlights discrepancies | Exception handling |

## What This Skill Does

1. **Model education** - Explain different attribution approaches
2. **Credit calculation** - Apply models to touchpoint data
3. **Channel analysis** - Compare performance by source
4. **Model comparison** - Show how results differ by model
5. **Optimization recommendations** - Where to invest more/less

## How to Use

```
Analyze attribution for this closed-won deal:

Deal: [Company Name]
Value: $[Amount]
Close Date: [Date]
Sales Cycle: [Days]

Touchpoint Journey:
1. [Date] - [Channel] - [Action]
2. [Date] - [Channel] - [Action]
...
[List all touchpoints chronologically]

Questions:
- Which channels deserve credit?
- Compare first-touch vs last-touch
- Recommend budget allocation
```

## Instructions

### Step 1: Understand Attribution Models

| Model | Logic | Best For |
|-------|-------|----------|
| **First-Touch** | 100% to first interaction | Awareness measurement |
| **Last-Touch** | 100% to final conversion | Direct response |
| **Linear** | Equal split across all | Long consideration cycles |
| **Time-Decay** | More credit to recent | Sales-assisted journeys |
| **Position-Based** | 40/20/40 (first/middle/last) | Balanced view |
| **W-Shaped** | 30/30/30 + 10 remainder | Include MQL moment |

### Step 2: Map the Customer Journey

Document all touchpoints with:
- **Timestamp** - When it occurred
- **Channel** - Source (Paid, Organic, Email, Event, etc.)
- **Action** - What happened (visit, download, demo, etc.)
- **Stage** - Awareness, Consideration, Decision

### Step 3: Apply Attribution Model

**First-Touch Example:**
```
Journey: Paid Search → Email → Webinar → Demo → Close
Revenue: $50,000

First-Touch Attribution:
- Paid Search: $50,000 (100%)
- All others: $0
```

**Linear Example:**
```
Same journey, 4 touchpoints:
- Paid Search: $12,500 (25%)
- Email: $12,500 (25%)
- Webinar: $12,500 (25%)
- Demo: $12,500 (25%)
```

**Position-Based (40/20/40):**
```
- Paid Search: $20,000 (40% - first)
- Email: $5,000 (10% - middle)
- Webinar: $5,000 (10% - middle)
- Demo: $20,000 (40% - last)
```

### Step 4: Aggregate by Channel

Sum attribution across all deals to see total channel contribution:

```
Channel Performance (Position-Based):
- Paid Search: $500K attributed (35%)
- Events: $300K attributed (21%)
- Organic: $280K attributed (19%)
- Email: $220K attributed (15%)
- Referral: $150K attributed (10%)
```

### Step 5: Calculate ROI by Channel

```
Channel ROI = Attributed Revenue / Channel Spend

Example:
- Paid Search: $500K revenue / $100K spend = 5x ROI
- Events: $300K revenue / $200K spend = 1.5x ROI
```

## Examples

### Example 1: Deal-Level Attribution

**Input:**
```
Analyze attribution for TechStart Inc:

Deal: TechStart Inc
Value: $75,000 ARR
Close Date: March 15
Sales Cycle: 62 days

Touchpoint Journey:
1. Jan 12 - Google Ads - Clicked ad, visited pricing
2. Jan 15 - Organic Search - Blog post read
3. Jan 22 - LinkedIn Ad - Whitepaper download (MQL)
4. Feb 1 - Email nurture - Opened 3 emails
5. Feb 10 - Webinar - Attended "Product Demo Day"
6. Feb 18 - Direct - Requested demo (SQL)
7. Mar 5 - Sales - Discovery call
8. Mar 12 - Sales - Proposal review
9. Mar 15 - Direct - Signed contract

Compare first-touch, last-touch, and position-based.
```

**Output:**
```
## Attribution Analysis: TechStart Inc ($75,000)

### Journey Summary
- **Total Touchpoints**: 9
- **Marketing Touchpoints**: 6 (Jan 12 - Feb 18)
- **Sales Touchpoints**: 3 (Mar 5 - Mar 15)
- **Sales Cycle**: 62 days
- **Key Conversion**: LinkedIn whitepaper (MQL), Demo request (SQL)

### Model Comparison

| Channel | First-Touch | Last-Touch | Position-Based | Linear |
|---------|-------------|------------|----------------|--------|
| Google Ads | $75,000 | $0 | $22,500 | $8,333 |
| Organic Search | $0 | $0 | $3,750 | $8,333 |
| LinkedIn Ads | $0 | $0 | $7,500 | $8,333 |
| Email | $0 | $0 | $3,750 | $8,333 |
| Webinar | $0 | $0 | $3,750 | $8,333 |
| Direct (Demo) | $0 | $0 | $7,500 | $8,333 |
| Sales | $0 | $75,000 | $26,250 | $25,000 |

### Position-Based Breakdown (Recommended)

**First Touch (30%): $22,500**
- Google Ads gets full first-touch credit
- Drove initial awareness and pricing interest

**MQL Touch (30%): $22,500**
- LinkedIn Ads: $15,000 (whitepaper = MQL)
- Webinar: $7,500 (influenced SQL)

**Last Touch (30%): $22,500**
- Demo Request: $7,500
- Sales (Close): $15,000

**Middle Touches (10%): $7,500**
- Organic: $2,500
- Email: $2,500
- Other: $2,500

### Insights

1. **Google Ads** initiated the journey - valuable for awareness
2. **LinkedIn Ads** drove the MQL - critical conversion point
3. **Sales** closed but didn't initiate - last-touch overstates
4. **Email** nurtured but didn't convert alone - assist role

### Channel Recommendations

| Channel | Attribution | Action |
|---------|-------------|--------|
| Google Ads | High first-touch | Maintain/increase for awareness |
| LinkedIn Ads | High MQL driver | Invest more for lead gen |
| Webinar | Solid influence | Continue as mid-funnel |
| Email | Assist role | Optimize, don't cut |
```

### Example 2: Multi-Deal Channel Analysis

**Input:**
```
Analyze Q1 attribution across these closed deals:

Deal 1: $50K - Google Ads → Email → Demo → Close
Deal 2: $30K - Event → LinkedIn → Demo → Close
Deal 3: $80K - Referral → Demo → Close
Deal 4: $45K - Organic → Webinar → Email → Demo → Close
Deal 5: $25K - Google Ads → Event → Demo → Close

Total Q1 Revenue: $230K

Channel Spend:
- Google Ads: $15K
- Events: $25K
- LinkedIn: $8K
- Email: $3K
- Webinar: $5K
- Referral: $0

Which channels should we invest more in?
```

**Output:**
```
## Q1 Channel Attribution Analysis

### Total Revenue: $230,000

### Attribution by Model

#### Position-Based Attribution (40/20/40)

| Channel | First | Middle | Last | Total | % of Rev |
|---------|-------|--------|------|-------|----------|
| Google Ads | $30,000 | $2,500 | $0 | $32,500 | 14% |
| Events | $12,000 | $5,000 | $0 | $17,000 | 7% |
| LinkedIn | $0 | $6,000 | $0 | $6,000 | 3% |
| Email | $0 | $11,000 | $0 | $11,000 | 5% |
| Webinar | $0 | $9,000 | $0 | $9,000 | 4% |
| Referral | $32,000 | $0 | $0 | $32,000 | 14% |
| Demo | $0 | $0 | $30,500 | $30,500 | 13% |
| Sales/Close | $0 | $0 | $92,000 | $92,000 | 40% |

### ROI Analysis

| Channel | Attributed Rev | Spend | ROI |
|---------|----------------|-------|-----|
| Referral | $32,000 | $0 | ∞ (Best) |
| Google Ads | $32,500 | $15,000 | 2.2x |
| Webinar | $9,000 | $5,000 | 1.8x |
| LinkedIn | $6,000 | $8,000 | 0.75x |
| Events | $17,000 | $25,000 | 0.68x |
| Email | $11,000 | $3,000 | 3.7x |

### Efficiency Ranking

1. **🥇 Referral** - $0 cost, $32K attributed → Infinite ROI
2. **🥈 Email** - 3.7x ROI → High-value nurture
3. **🥉 Google Ads** - 2.2x ROI → Profitable acquisition
4. **Webinar** - 1.8x ROI → Solid mid-funnel
5. **LinkedIn** - 0.75x ROI → Below break-even
6. **Events** - 0.68x ROI → Expensive for return

### Recommendations

**Increase Investment:**
- **Referral Program**: 14% of revenue at $0 cost
  - Formalize referral rewards
  - Target: 2x referral deals in Q2

- **Email Nurture**: 3.7x ROI
  - Expand sequences
  - Add $2K budget for tools

- **Google Ads**: 2.2x ROI
  - Profitable, test 20% budget increase
  - Focus on high-intent keywords

**Optimize/Test:**
- **LinkedIn**: 0.75x is below target
  - Test new audiences before cutting
  - Could be essential for certain segments

**Reduce/Reallocate:**
- **Events**: $25K for $17K attributed
  - Evaluate which events drive pipeline
  - Consider smaller, targeted events
  - Reallocate $10K to Google Ads

### Proposed Q2 Budget Shift

| Channel | Q1 Spend | Q2 Proposed | Change |
|---------|----------|-------------|--------|
| Google Ads | $15K | $20K | +$5K |
| Events | $25K | $15K | -$10K |
| LinkedIn | $8K | $8K | — |
| Email | $3K | $5K | +$2K |
| Webinar | $5K | $6K | +$1K |
| Referral | $0 | $2K (rewards) | +$2K |
| **Total** | **$56K** | **$56K** | Rebalanced |
```

## Skill Boundaries

### What This Skill Does Well
- Explaining attribution model mechanics
- Calculating credit across touchpoints
- Comparing models side-by-side
- Identifying channel efficiency

### What This Skill Cannot Do
- Access actual CRM/analytics data
- Track offline touchpoints automatically
- Account for brand lift effects
- Prove causation (only correlation)

### When to Escalate to Human
- Choosing official attribution model for company
- Budget allocation decisions over $50K
- Complex B2B journeys with multiple stakeholders
- Reconciling attribution across systems

## Iteration Guide

### Follow-up Prompts
- "How would results change with time-decay model?"
- "What if we excluded sales touchpoints?"
- "Show me channel performance by deal size."
- "Build attribution for all Q1 deals (I'll provide data)."

### Attribution Maturity
1. **Basic**: Last-touch only
2. **Intermediate**: First and last comparison
3. **Advanced**: Position-based or custom
4. **Expert**: ML-based algorithmic attribution

## Checklists & Templates

### Attribution Report Template
```markdown
## Attribution Report: [Period]

### Summary
- Total Revenue: $X
- Deals Analyzed: X
- Model Used: [Position-Based]

### Channel Attribution
| Channel | Revenue | % | ROI |
|---------|---------|---|-----|

### Top Insights
1.
2.
3.

### Budget Recommendations
| Channel | Current | Recommended | Rationale |
|---------|---------|-------------|-----------|
```

### Touchpoint Tracking Checklist
- [ ] UTM parameters on all campaigns
- [ ] CRM synced with marketing automation
- [ ] Offline events logged manually
- [ ] Sales activities timestamped
- [ ] Content downloads tracked

## References

- Bizible Multi-Touch Attribution Guide
- Google Analytics Attribution Modeling
- Forrester B2B Attribution Research
- Marketo Revenue Cycle Analytics

## Related Skills

- `pipeline-forecasting` - Predict revenue by source
- `lead-scoring` - Score by attributed channel
- `ad-spend-optimizer` - Automate budget shifts

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 30-60 min for analysis
- **Prerequisites**: Touchpoint data, deal values, channel spend
