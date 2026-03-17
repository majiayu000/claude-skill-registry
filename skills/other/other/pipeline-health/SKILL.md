---
name: pipeline-health
description: Analyze pipeline coverage and forecast accuracy
role_groups: [sales, leadership]
jtbd: |
  You need to forecast accurately and ensure you have enough pipeline to hit quota. 
  This reviews deal velocity (time in each stage), identifies forecast gaps, and 
  suggests actions to move deals forward so you can report confidently on where 
  you'll land.
time_investment: "10-15 minutes per review"
---

## Purpose

Analyze pipeline coverage, conversion rates, velocity, and forecast accuracy to ensure you're on track to hit targets and identify where to focus attention.

## Usage

- `/pipeline-health` - Full pipeline analysis
- `/pipeline-health [timeframe]` - Focus on specific period (e.g., "this quarter", "Q1")
- `/pipeline-health forecast` - Forecast-focused view

---

## Step 1: Gather Pipeline Data

Collect deal information from 04-Projects/:

### For Each Deal Extract:
- Company name
- Deal value/size
- Current stage
- Entry date to current stage (or last modified date)
- Close date (if specified)
- Confidence level (if mentioned)

### Read Targets:
- Check 01-Quarter_Goals/Quarter_Goals.md or user files for revenue targets
- Check for quota information
- Typical sales cycle length (or calculate from historical data)

---

## Step 2: Calculate Pipeline Metrics

### Coverage Metrics

**Pipeline coverage ratio** = Total pipeline value / Target
- 3x coverage = Healthy
- 2-3x coverage = Adequate
- <2x coverage = At Risk

**Weighted pipeline** = Sum of (Deal value × Stage probability)
- Discovery: 10%
- Demo: 25%
- Proposal: 50%
- Negotiation: 75%
- Contract: 90%

### Velocity Metrics

**Average time in stage:**
- For each stage, calculate average days deals spend there
- Flag deals exceeding average by 50%+

**Average sales cycle:**
- From discovery to close
- Compare current deals to average

### Conversion Metrics

**Stage conversion rates:**
- Discovery → Demo: X%
- Demo → Proposal: X%
- Proposal → Negotiation: X%
- Negotiation → Contract: X%
- Contract → Close: X%

(Calculate from historical closed deals if data available)

---

## Step 3: Analyze Forecast

### Commit vs Best Case vs Pipeline

**Commit forecast:**
- Contract stage deals (90% probability)
- Total commit value

**Best case forecast:**
- Negotiation + Contract (75%+ probability)
- Total best case value

**Pipeline forecast:**
- All active deals weighted by stage probability

### Gap Analysis

**Target:** [Quota or goal]
**Commit:** [Amount] - [Gap to target]
**Best case:** [Amount] - [Gap to target]
**Coverage:** [Pipeline / Target ratio]

---

## Step 4: Identify Issues

### Red Flags

1. **Insufficient coverage** - Pipeline < 3x target
2. **Slow velocity** - Deals stuck in stages too long
3. **Low conversion** - Stages with poor conversion rates
4. **Forecast risk** - Heavy reliance on few large deals
5. **Stage bunching** - Too many deals in one stage
6. **Aging deals** - Deals past typical sales cycle

### Opportunities

1. **Quick wins** - Deals close to closing that need push
2. **Stuck deals** - Deals that could move with attention
3. **New pipeline needed** - If coverage insufficient

---

## Step 5: Generate Pipeline Health Report

Present findings in this format:

```markdown
# 📊 Pipeline Health Report

**Period:** [Timeframe]
**Target:** $[Target amount]
**Report date:** [Today]

---

## 🎯 Forecast Summary

### Current Position

| Forecast Type | Amount | % of Target | Gap to Target |
|---------------|--------|-------------|---------------|
| **Commit** (90%+) | $XXX,XXX | XX% | $XX,XXX |
| **Best Case** (75%+) | $XXX,XXX | XX% | $XX,XXX |
| **Pipeline** (weighted) | $XXX,XXX | XX% | $XX,XXX |

**Overall health:** [On Track / At Risk / Behind]

---

## 📈 Pipeline Coverage

**Total pipeline:** $XXX,XXX
**Coverage ratio:** X.Xx (Total pipeline / Target)

**Status:**
- ✅ 3x+ coverage = Healthy
- ⚠️ 2-3x coverage = Adequate (yours: X.Xx)
- 🚨 <2x coverage = At Risk

**Action needed:** [Yes/No - if <3x, need more pipeline generation]

---

## ⏱️ Velocity Analysis

**Average sales cycle:** XX days
**Deals exceeding cycle:** [X deals] - [List if important]

**Time in stage (average):**
- Discovery: XX days
- Demo: XX days
- Proposal: XX days
- Negotiation: XX days
- Contract: XX days

**Slow movers:** (50%+ over average)
- [Company] - XX days in [stage] (avg: XX days)
- [Company] - XX days in [stage] (avg: XX days)

---

## 🔄 Conversion Health

**Stage conversion rates:**

| From Stage | To Stage | Rate | Benchmark | Status |
|------------|----------|------|-----------|--------|
| Discovery | Demo | XX% | ~50% | ✅/⚠️/🚨 |
| Demo | Proposal | XX% | ~50% | ✅/⚠️/🚨 |
| Proposal | Negotiation | XX% | ~60% | ✅/⚠️/🚨 |
| Negotiation | Contract | XX% | ~75% | ✅/⚠️/🚨 |
| Contract | Close | XX% | ~90% | ✅/⚠️/🚨 |

**Bottleneck stages:** [Stages with low conversion]

---

## 🚨 Risk Factors

### High-Risk Items

1. **Heavy deal concentration**
   - Top 3 deals = XX% of commit
   - Risk: If one slips, major impact

2. **[Deal Name] - $XXX,XXX**
   - Risk: [Specific risk]
   - Mitigation: [Action needed]

### Stage Issues

- **Too many in [stage]:** [X deals]
  - Bottleneck indicator
  - Action: Review what's blocking progression

- **Aging deals:** [X deals over XX days old]
  - May never close
  - Action: Qualify out or re-engage

---

## 💡 Opportunities

### Quick Wins (Focus Here)

**[Company] - $XX,XXX**
- Stage: Contract Review
- Days in stage: 5
- Action: One call away from close
- Impact: Closes gap by XX%

**[Company] - $XX,XXX**
- Stage: Negotiation
- Days in stage: 8
- Action: Address pricing concern
- Impact: High confidence, near close

### Stuck Deals That Could Move

**[Company] - $XX,XXX**
- Stage: Proposal (15 days)
- Issue: Waiting on champion response
- Action: Executive reach-out

---

## 📊 Pipeline Distribution

**By Stage:**
- Discovery: [X deals] - $XXX,XXX
- Demo: [X deals] - $XXX,XXX
- Proposal: [X deals] - $XXX,XXX
- Negotiation: [X deals] - $XXX,XXX
- Contract: [X deals] - $XXX,XXX

**By Close Date:**
- This week: [X deals] - $XXX,XXX
- This month: [X deals] - $XXX,XXX
- This quarter: [X deals] - $XXX,XXX
- Beyond quarter: [X deals] - $XXX,XXX

---

## 🎯 Recommended Actions

### Immediate (This Week)

1. **[Action]** - [Deals affected] - [Impact]
2. **[Action]** - [Deals affected] - [Impact]
3. **[Action]** - [Deals affected] - [Impact]

### Strategic (This Month)

1. **Generate new pipeline** - Coverage at X.Xx, need X.Xx
2. **Accelerate [stage]** - X deals stuck, average XX days
3. **Improve [stage] conversion** - Currently XX%, need XX%

### Health Tracking

- **Next review:** [Suggested date]
- **Metrics to watch:** [Key metrics that need improvement]
```

---

## Step 6: Offer Actions

After presenting the report, ask:

> "Want me to:
> 1. Deep dive on specific deals or stages?
> 2. Create action plan for pipeline generation?
> 3. Draft forecast update for leadership?
> 4. Review deals to qualify out?"

---

## Timeframe Filtering

When user specifies timeframe:

1. **"this quarter"** - Deals closing this quarter
2. **"Q1"** - Deals in Q1 specifically
3. **"this month"** - Deals closing this month

Filter metrics and analysis to that window.

---

## Forecast Mode

When user runs `/pipeline-health forecast`:

Focus exclusively on:
1. Commit vs Best Case vs Target
2. Gap analysis
3. Risk factors in commit deals
4. Actions to close gap
5. Deals likely to slip
6. Upside opportunities

---

## Integration with Other Skills

- **After running:** Suggest `/deal-review` for deal-level deep dive
- **If coverage low:** Suggest reviewing lead generation strategy
- **If velocity slow:** Suggest `/process-audit` on sales process
- **Before leadership meeting:** Run this + prepare summary

---

## Example Output

```markdown
# 📊 Pipeline Health Report

**Period:** Q1 2026
**Target:** $500,000
**Report date:** 2026-01-28

---

## 🎯 Forecast Summary

### Current Position

| Forecast Type | Amount | % of Target | Gap to Target |
|---------------|--------|-------------|---------------|
| **Commit** (90%+) | $235,000 | 47% | $265,000 |
| **Best Case** (75%+) | $430,000 | 86% | $70,000 |
| **Pipeline** (weighted) | $580,000 | 116% | +$80,000 |

**Overall health:** At Risk (Commit is 47% of target with 8 weeks left in quarter)

---

## 📈 Pipeline Coverage

**Total pipeline:** $847,000
**Coverage ratio:** 1.7x (Total pipeline / Target)

**Status:** 🚨 At Risk
- ✅ 3x+ coverage = Healthy
- ⚠️ 2-3x coverage = Adequate  
- 🚨 <2x coverage = At Risk **(You are here: 1.7x)**

**Action needed:** YES - Need $400K+ in new pipeline to reach 3x coverage

---

## ⏱️ Velocity Analysis

**Average sales cycle:** 45 days
**Deals exceeding cycle:** 3 deals (TechStart - 62 days, GlobalCo - 58 days, OldCo - 71 days)

**Time in stage (average):**
- Discovery: 7 days
- Demo: 10 days
- Proposal: 12 days ⚠️ (2x typical)
- Negotiation: 10 days
- Contract: 6 days

**Slow movers:** (50%+ over average)
- **TechStart** - 18 days in Proposal (avg: 12 days) - STALE
- **InnovateCo** - 18 days in Discovery (avg: 7 days) - Needs qualification

---

## 🔄 Conversion Health

**Stage conversion rates:**

| From Stage | To Stage | Rate | Benchmark | Status |
|------------|----------|------|-----------|--------|
| Discovery | Demo | 67% | ~50% | ✅ Good |
| Demo | Proposal | 75% | ~50% | ✅ Good |
| Proposal | Negotiation | 40% | ~60% | 🚨 **Issue** |
| Negotiation | Contract | 80% | ~75% | ✅ Good |
| Contract | Close | 100% | ~90% | ✅ Good |

**Bottleneck stages:** Proposal → Negotiation (40% conversion, should be ~60%)
- Issue: Deals getting stuck after proposal sent
- Root cause: Pricing concerns OR lack of follow-up

---

## 🚨 Risk Factors

### High-Risk Items

1. **Heavy deal concentration**
   - Top 3 deals (Acme, DataFlow, TechStart) = 68% of commit
   - Risk: If one slips, we miss target by 20%+

2. **DataFlow - $120,XXX** (25% of commit)
   - Risk: Evaluating ProductX competitor, concerned about dashboards
   - Mitigation: Executive call Friday - prep competitive positioning NOW

3. **TechStart - $75,XXX** (18% of commit)
   - Risk: 18 days stale, no response to proposal
   - Mitigation: Last-chance outreach today

### Stage Issues

- **Too many in Proposal:** 4 deals ($295K)
  - Bottleneck indicator (40% conversion rate)
  - Action: Review what's blocking progression - pricing? timeline? features?

- **Aging deals:** 3 deals over 60 days old ($215K)
  - TechStart, GlobalCo, OldCo - may never close
  - Action: Qualify out or re-engage with fresh approach

---

## 💡 Opportunities

### Quick Wins (Focus Here)

**StartupX - $40,XXX**
- Stage: Contract - Signatures received
- Days in stage: 1
- Action: Process payment today
- Impact: Closes gap to target by 8%

**NewCorp - $55,XXX**
- Stage: Negotiation
- Days in stage: 4
- Action: Final terms call tomorrow
- Impact: High confidence, contract by end of week

### Stuck Deals That Could Move

**GlobalCo - $95,XXX**
- Stage: Discovery (9 days)
- Issue: Waiting on champion Sarah to schedule demo
- Action: Executive reach-out to Sarah's boss to create urgency
- Impact: Could close this quarter if we move fast

---

## 📊 Pipeline Distribution

**By Stage:**
- Discovery: 3 deals - $220,000 (26%)
- Demo: 2 deals - $105,000 (12%)
- Proposal: 4 deals - $295,000 (35%) ⚠️ **Bottleneck**
- Negotiation: 2 deals - $175,000 (21%)
- Contract: 1 deal - $52,000 (6%)

**By Close Date:**
- This week: 1 deal - $40,000
- Rest of month: 1 deal - $55,000
- Feb: 4 deals - $285,000
- March+: 6 deals - $467,000

---

## 🎯 Recommended Actions

### Immediate (This Week)

1. **Save at-risk commit deals** - TechStart ($75K) + DataFlow ($120K) = $195K at risk
2. **Close StartupX** - $40K ready to process, no-brainer
3. **Push NewCorp to contract** - $55K, final call tomorrow

### Strategic (This Month)

1. **Generate $400K+ new pipeline** - Coverage at 1.7x, need 3.0x (gap: $1M in gross pipeline)
2. **Fix Proposal stage** - 4 deals stuck, 40% conversion vs 60% benchmark
3. **Qualify out aging deals** - 3 deals over 60 days, likely dead

### Health Tracking

- **Next review:** Friday (before week ends)
- **Metrics to watch:** 
  - Commit forecast (need to hit 70%+ by mid-Feb)
  - Proposal conversion rate
  - New pipeline adds per week
```
