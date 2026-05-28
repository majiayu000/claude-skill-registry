---
name: forecast-scenarios
description: Model best-case, worst-case, and likely revenue scenarios with sensitivity analysis for strategic planning
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Forecast Scenario Modeling

> Create multiple revenue scenarios with variable assumptions to support strategic planning, board presentations, and risk management.

## When to Use This Skill

- Annual and quarterly planning
- Board meeting preparations
- Fundraising projections
- Risk assessment and contingency planning
- Evaluating strategic initiatives

## Methodology Foundation

Based on **McKinsey Scenario Planning** and **FP&A best practices**, combining:
- Base/Bull/Bear case modeling
- Sensitivity analysis (variable impact)
- Monte Carlo probability distributions
- Driver-based forecasting

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures scenario framework | Assumption values |
| Calculates scenario outcomes | Which scenario to plan for |
| Identifies key sensitivities | Risk tolerance levels |
| Models variable impacts | Strategic responses |
| Presents range of outcomes | Final forecast commitment |

## What This Skill Does

1. **Scenario definition** - Base, upside, downside cases
2. **Variable modeling** - Test impact of changing assumptions
3. **Sensitivity analysis** - Which variables matter most
4. **Probability weighting** - Expected value calculations
5. **Action planning** - What to do in each scenario

## How to Use

```
Model revenue scenarios for [Period]:

Current Status:
- YTD Revenue: $X
- Current Pipeline: $X
- Run Rate: $X/month

Key Variables to Model:
- Win rate: [Current: X%, Range: X-X%]
- Average deal size: [Current: $X, Range: $X-$X]
- Sales cycle: [Current: X days, Range: X-X]
- New pipeline creation: [Current: $X/month]
- Churn rate: [Current: X%]

Create best, likely, and worst case scenarios.
```

## Instructions

### Step 1: Define Scenario Framework

| Scenario | Definition | Probability |
|----------|------------|-------------|
| **Best Case** (Bull) | Everything goes right | 15-20% |
| **Likely Case** (Base) | Realistic expectations | 50-60% |
| **Worst Case** (Bear) | Major headwinds | 20-25% |

### Step 2: Identify Key Drivers

Rank variables by revenue impact:

| Driver | Impact | Controllability |
|--------|--------|-----------------|
| Win rate | High | Medium |
| Pipeline volume | High | High |
| Deal size | Medium | Low |
| Sales cycle | Medium | Medium |
| Churn rate | Medium | Medium |
| Pricing | Low | High |

### Step 3: Set Variable Ranges

For each driver, define realistic bounds:

```
Win Rate:
- Best: 35% (team is hitting stride)
- Likely: 25% (current performance)
- Worst: 18% (market headwinds)

Pipeline:
- Best: $5M (strong marketing)
- Likely: $4M (normal cadence)
- Worst: $2.5M (budget cuts)
```

### Step 4: Calculate Scenarios

**Revenue Formula (simplified):**
```
Quarterly Revenue =
  (Pipeline × Win Rate) +
  (Expansion Revenue) -
  (Churn)
```

**Apply to each scenario:**
```
Best Case:
$5M × 35% = $1.75M new + $200K expansion - $50K churn
= $1.9M

Likely Case:
$4M × 25% = $1M new + $150K expansion - $80K churn
= $1.07M

Worst Case:
$2.5M × 18% = $450K new + $100K expansion - $120K churn
= $430K
```

### Step 5: Sensitivity Analysis

Test: "What if X changes by 10%?"

| Variable | +10% Impact | -10% Impact | Sensitivity |
|----------|-------------|-------------|-------------|
| Win Rate | +$100K | -$100K | High |
| Pipeline | +$90K | -$90K | High |
| Deal Size | +$50K | -$50K | Medium |
| Churn | -$30K | +$30K | Medium |

### Step 6: Calculate Expected Value

```
Expected Revenue =
  (Best × Probability) +
  (Likely × Probability) +
  (Worst × Probability)

= ($1.9M × 20%) + ($1.07M × 55%) + ($430K × 25%)
= $380K + $589K + $108K
= $1.077M
```

## Examples

### Example 1: Quarterly Forecast Scenarios

**Input:**
```
Model Q2 scenarios:

Current Status:
- Q1 Revenue: $850K
- Q2 Pipeline: $4.2M
- Monthly run rate: $280K

Variables:
- Win rate: Current 24%, Range 18-32%
- Avg deal: Current $45K, Range $38K-$55K
- New monthly pipeline: Current $800K, Range $500K-$1.2M
- Monthly churn: Current $25K, Range $15K-$40K
- Expansion: Current $50K/month, Range $30K-$80K
```

**Output:**
```
## Q2 Revenue Scenario Model

### Scenario Definitions

| Scenario | Probability | Description |
|----------|-------------|-------------|
| 🐂 Bull | 20% | Strong execution, market tailwinds |
| 📊 Base | 55% | Continue current trajectory |
| 🐻 Bear | 25% | Market slowdown, execution challenges |

### Variable Assumptions

| Variable | Bear | Base | Bull |
|----------|------|------|------|
| Starting Pipeline | $4.2M | $4.2M | $4.2M |
| Win Rate | 18% | 24% | 32% |
| Avg Deal Size | $38K | $45K | $55K |
| New Pipeline/mo | $500K | $800K | $1.2M |
| Monthly Churn | $40K | $25K | $15K |
| Expansion/mo | $30K | $50K | $80K |

### Q2 Revenue Calculations

#### 🐂 Bull Case: $1.42M

```
Starting Pipeline Revenue:
$4.2M × 32% = $1.34M

Adjustment for deal size:
$1.34M × ($55K/$45K) = $1.64M effective

New Pipeline Added (Q2):
$1.2M × 3 months × 32% × 50% (partial close) = $576K

Expansion:
$80K × 3 = $240K

Churn:
-$15K × 3 = -$45K

Total Bull: $1.64M (existing) + $576K (new) + $240K (exp) - $45K (churn)
Weighted at Q2 stage: $1.42M
```

#### 📊 Base Case: $980K

```
Starting Pipeline Revenue:
$4.2M × 24% = $1.01M

New Pipeline (partial close):
$800K × 3 × 24% × 50% = $288K

Expansion: $150K
Churn: -$75K

Total Base: $1.01M × 0.9 (timing) + $150K - $75K
= $980K
```

#### 🐻 Bear Case: $580K

```
Starting Pipeline Revenue:
$4.2M × 18% = $756K × 0.85 (pushed deals)
= $643K

New Pipeline: $500K × 3 × 18% × 40% = $108K
Expansion: $90K
Churn: -$120K

Total Bear: $580K
```

### Scenario Summary

| Scenario | Revenue | vs Q1 | Growth |
|----------|---------|-------|--------|
| 🐂 Bull | $1.42M | +$570K | +67% |
| 📊 Base | $980K | +$130K | +15% |
| 🐻 Bear | $580K | -$270K | -32% |

### Expected Value

```
E(Revenue) = ($1.42M × 0.20) + ($980K × 0.55) + ($580K × 0.25)
           = $284K + $539K + $145K
           = $968K
```

**Recommended Forecast: $950K - $1.0M**

### Sensitivity Analysis

| If This Changes... | Revenue Impact |
|--------------------|----------------|
| Win rate +5% | +$210K |
| Win rate -5% | -$210K |
| Pipeline +$500K | +$120K |
| Deal size +$5K | +$80K |
| Churn +$10K/mo | -$30K |

**Highest Sensitivity**: Win rate (focus on deal execution)

### Scenario Action Plans

**If Trending Bull:**
- Accelerate hiring plan
- Increase marketing spend
- Prepare for capacity constraints

**If Trending Base:**
- Stay the course
- Focus on execution
- Build pipeline for Q3

**If Trending Bear:**
- Tighten expense controls
- Extend runway calculations
- Double down on existing customers
- Consider discounting to close deals
```

### Example 2: Annual Planning Scenarios

**Input:**
```
Model 2026 annual scenarios for board:

2025 Results:
- Revenue: $4.2M
- Customers: 85
- ARR Growth: 45%
- NRR: 110%

2026 Planning Variables:
- New customer target: 40-80 new customers
- ACV range: $40K-$60K
- NRR range: 105%-120%
- Churn range: 5%-12%
```

**Output:**
```
## 2026 Annual Revenue Scenarios

### For Board Review

---

### Scenario Summary

| Metric | Bear | Base | Bull |
|--------|------|------|------|
| New Customers | 40 | 60 | 80 |
| New ACV | $40K | $50K | $60K |
| New ARR | $1.6M | $3.0M | $4.8M |
| NRR | 105% | 112% | 120% |
| Existing Base | $4.41M | $4.70M | $5.04M |
| **Total ARR** | **$6.0M** | **$7.7M** | **$9.8M** |
| **Growth** | **43%** | **83%** | **133%** |

### Detailed Calculations

#### 🐻 Bear Case: $6.0M ARR (+43%)

**Assumptions:**
- Conservative new sales (40 customers)
- Lower ACV ($40K avg)
- NRR dips (105%)
- Higher churn (10%)

```
Existing Customer Base:
$4.2M × 105% NRR = $4.41M

New Customer Revenue:
40 customers × $40K = $1.6M

Total: $6.0M
```

**When This Happens:**
- Market downturn
- Sales execution issues
- Product-market fit challenges
- Key competitor gains ground

---

#### 📊 Base Case: $7.7M ARR (+83%)

**Assumptions:**
- Target new sales (60 customers)
- Target ACV ($50K)
- Maintain NRR (112%)
- Normal churn (7%)

```
Existing Customer Base:
$4.2M × 112% NRR = $4.70M

New Customer Revenue:
60 customers × $50K = $3.0M

Total: $7.7M
```

**This Is Likely If:**
- Execute at current pace
- Market conditions stable
- Product roadmap delivers
- Team retention healthy

---

#### 🐂 Bull Case: $9.8M ARR (+133%)

**Assumptions:**
- Exceed targets (80 customers)
- Premium ACV ($60K)
- Strong NRR (120%)
- Low churn (5%)

```
Existing Customer Base:
$4.2M × 120% NRR = $5.04M

New Customer Revenue:
80 customers × $60K = $4.8M

Total: $9.8M
```

**Required For This:**
- Strong product releases
- Successful enterprise push
- Favorable market timing
- Key hires perform

---

### Expected Value & Recommendation

```
E(ARR) = ($6.0M × 0.20) + ($7.7M × 0.55) + ($9.8M × 0.25)
       = $1.2M + $4.24M + $2.45M
       = $7.89M
```

### Board Recommendation

**Target: $7.5M ARR** (+79% growth)

| Metric | Target | Confidence |
|--------|--------|------------|
| New Customers | 55-60 | Medium-High |
| New ARR | $2.75M | Medium |
| NRR | 110%+ | High |
| Total ARR | $7.5M | Medium |

### Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sales hiring delays | -$1M | Recruit pipeline now |
| Enterprise deals push | -$800K | Parallel SMB motion |
| Key customer churn | -$500K | CSM investment |
| Competitor pricing | -$600K | Value selling training |

### Monthly Checkpoints

| Month | Bear | Base | Bull |
|-------|------|------|------|
| Q1 End | $4.8M | $5.2M | $5.8M |
| Q2 End | $5.3M | $6.2M | $7.4M |
| Q3 End | $5.6M | $7.0M | $8.6M |
| Q4 End | $6.0M | $7.7M | $9.8M |

Track monthly and adjust Q3 if trending to Bear.
```

## Skill Boundaries

### What This Skill Does Well
- Structuring scenario frameworks
- Calculating outcomes from assumptions
- Identifying key sensitivities
- Presenting range of possibilities

### What This Skill Cannot Do
- Predict which scenario will occur
- Know your specific business dynamics
- Account for black swan events
- Replace expert judgment on probabilities

### When to Escalate to Human
- Setting official targets
- Board/investor commitments
- Major strategic pivots
- Assumptions requiring domain expertise

## Iteration Guide

### Follow-up Prompts
- "What win rate do we need to hit Base case?"
- "Show me monthly revenue trajectory for each scenario."
- "Add a 'catastrophic' case if we lose our biggest customer."
- "What's the probability-weighted forecast?"

### Scenario Planning Cycle
1. Set variables and ranges
2. Calculate scenarios
3. Identify early warning signals
4. Define trigger points for action
5. Review monthly against actuals

## Checklists & Templates

### Annual Planning Template
```markdown
## [Year] Revenue Scenarios

### Scenarios
| Case | Revenue | Growth | Probability |
|------|---------|--------|-------------|
| Bull | | | 20% |
| Base | | | 55% |
| Bear | | | 25% |

### Key Assumptions
| Variable | Bear | Base | Bull |
|----------|------|------|------|

### Sensitivity Analysis
| Variable | Impact per 10% |
|----------|----------------|

### Risk Register
| Risk | Scenario Impact | Mitigation |
|------|-----------------|------------|
```

## References

- McKinsey Scenario Planning Guide
- FP&A Forecasting Best Practices
- SaaS Metrics and Financial Modeling
- CFO.com Revenue Forecasting

## Related Skills

- `pipeline-forecasting` - Feed into scenario models
- `lead-scoring` - Input for pipeline assumptions
- `account-health` - NRR/churn inputs

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 60-90 min for full model
- **Prerequisites**: Historical data, variable assumptions
