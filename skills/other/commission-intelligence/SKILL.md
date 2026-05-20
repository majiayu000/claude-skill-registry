---
name: commission-intelligence
description: Explain sales commission calculations, resolve discrepancies, and model compensation scenarios for quota planning
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Commission Intelligence

> Demystify sales compensation by explaining commission calculations, identifying discrepancies, and modeling payout scenarios.

## When to Use This Skill

- Reps questioning commission statements
- Designing or updating comp plans
- Modeling quota and OTE scenarios
- Resolving payout disputes
- Planning territory changes

## Methodology Foundation

Based on **Alexander Group Sales Compensation Design** and **WorldatWork Incentive Compensation principles**, covering:
- Base + variable structures
- Quota attainment mechanics
- Accelerators and decelerators
- Split and overlay rules

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Explains calculation logic | Final payout approvals |
| Identifies discrepancies | Exception handling |
| Models scenarios | Plan design choices |
| Documents rules clearly | Policy changes |
| Calculates examples | Quota assignments |

## What This Skill Does

1. **Calculation explanation** - Break down how commission was computed
2. **Discrepancy identification** - Find calculation errors or data issues
3. **Scenario modeling** - Project earnings under different assumptions
4. **Plan documentation** - Clarify complex comp plan rules
5. **Dispute resolution** - Provide clear audit trail

## How to Use

```
Explain this commission calculation:

Rep: [Name]
Role: [AE, SDR, etc.]
Quota: $[Amount]/[Period]
Closed this period: $[Amount]

Comp plan rules:
- Base: $X
- OTE: $X
- Variable: X% of base
- Commission rate: X% up to quota
- Accelerator: X% above quota

Deals closed:
- [List deals with amounts and close dates]

Statement shows: $[Commission Amount]
Rep expected: $[Expected Amount]
```

## Instructions

### Step 1: Understand the Comp Plan Structure

**Common Structures:**
| Type | Description |
|------|-------------|
| Revenue Commission | % of deal value |
| Quota-Based | % payout based on attainment |
| Tiered | Different rates at different levels |
| Draw | Advance against future commissions |
| MBO | Bonus for specific objectives |

### Step 2: Calculate Attainment

```
Attainment % = (Closed Revenue / Quota) × 100

Example:
- Quota: $500,000
- Closed: $450,000
- Attainment: 90%
```

### Step 3: Apply Commission Rules

**Standard Calculation:**
```
Base Commission = Closed Revenue × Commission Rate

With Quota Thresholds:
- Below 50% attainment: 0% payout (common)
- 50-100% attainment: Linear payout
- Above 100%: Accelerator rate kicks in
```

**Accelerator Example:**
```
Plan: 10% up to quota, 15% above quota
Quota: $500K, Closed: $600K

Commission:
- First $500K × 10% = $50,000
- Next $100K × 15% = $15,000
- Total: $65,000
```

### Step 4: Handle Special Cases

| Scenario | Rule |
|----------|------|
| Split deals | Divide credit per agreement |
| Multi-year | Recognize per year or upfront |
| Churn/Clawback | Deduct if customer cancels |
| Ramped quota | Reduced quota for new hires |
| SPIFs | One-time bonus amounts |

### Step 5: Reconcile Discrepancies

**Common Issues:**
| Issue | Cause | Resolution |
|-------|-------|------------|
| Missing deal | Not in CRM | Add deal, recalculate |
| Wrong amount | Incorrect ACV | Verify contract value |
| Wrong rate | Tier confusion | Check attainment level |
| Split error | Credit allocation | Review split agreement |
| Timing | Revenue recognition | Check close date vs. pay period |

## Examples

### Example 1: Commission Explanation

**Input:**
```
Explain why Sarah's commission is $12,500:

Rep: Sarah (AE)
Quota: $200,000/quarter
Q4 Closed: $175,000

Comp plan:
- OTE: $200,000 (50/50 split)
- Variable: $100,000/year = $25,000/quarter
- At 100% attainment: Full $25K variable
- Linear payout from 50-100%
- Accelerator: 1.5x above 100%

Deals:
- Acme Corp: $80,000 (Oct 15)
- Beta Inc: $45,000 (Nov 3)
- Gamma LLC: $50,000 (Dec 20)
Total: $175,000
```

**Output:**
```
## Commission Breakdown: Sarah - Q4

### Step 1: Verify Closed Revenue
| Deal | Amount | Close Date | ✓ |
|------|--------|------------|---|
| Acme Corp | $80,000 | Oct 15 | ✓ Q4 |
| Beta Inc | $45,000 | Nov 3 | ✓ Q4 |
| Gamma LLC | $50,000 | Dec 20 | ✓ Q4 |
| **Total** | **$175,000** | | ✓ |

### Step 2: Calculate Attainment
```
Attainment = $175,000 / $200,000 = 87.5%
```

### Step 3: Apply Commission Formula

**Plan Rules:**
- 50% threshold: Below 50% = $0
- 50-100%: Linear from $0 to $25,000
- 100%+: 1.5x accelerator

**Calculation:**
```
Sarah is at 87.5% (between 50% and 100%)

Linear formula:
Payout = (Attainment - 50%) / 50% × Full Variable
Payout = (87.5% - 50%) / 50% × $25,000
Payout = 37.5% / 50% × $25,000
Payout = 75% × $25,000
Payout = $18,750
```

### ⚠️ Discrepancy Found!

**Statement shows**: $12,500
**Calculated**: $18,750
**Difference**: $6,250 underpaid

### Likely Cause

If system shows $12,500, it may be calculating:
```
$12,500 / $25,000 = 50% payout
```

This would happen if:
1. One deal not credited (Beta Inc $45K?)
2. Wrong formula (% of revenue vs % of variable)
3. Deal attributed to different quarter

### Recommended Action
1. Verify all 3 deals in commission system
2. Check if Beta Inc close date is in Q4
3. Confirm formula is linear 50-100%, not flat rate
4. Escalate to compensation admin with this breakdown
```

### Example 2: Scenario Modeling

**Input:**
```
Model commission scenarios for Mike:

Current:
- Quota: $400,000/quarter
- OTE: $240,000 (60/40 split)
- Variable: $96,000/year = $24,000/quarter
- Rate: 6% of revenue up to quota
- Accelerator: 9% above quota

Q1 pipeline:
- Committed: $320,000
- Best case: $450,000
- Upside: $600,000

What would Mike earn in each scenario?
```

**Output:**
```
## Commission Scenarios: Mike - Q1

### Plan Summary
- Quota: $400,000
- At-quota commission: $24,000 (6% × $400K)
- Accelerator: 9% above quota

### Scenario Analysis

#### Scenario 1: Commit Only ($320K)
```
Attainment: 80%
Revenue: $320,000

Commission at 6%: $320,000 × 6% = $19,200

Quarterly Variable: $19,200
Annualized: $76,800
vs OTE Variable ($96K): -$19,200
```
**Status**: Below quota, standard rate applies

---

#### Scenario 2: Best Case ($450K)
```
Attainment: 112.5%
Revenue: $450,000

Below quota: $400,000 × 6% = $24,000
Above quota: $50,000 × 9% = $4,500

Total Commission: $28,500

Quarterly Variable: $28,500
vs At-Quota ($24K): +$4,500 (19% bonus)
```
**Status**: Accelerator kicks in, strong quarter

---

#### Scenario 3: Upside ($600K)
```
Attainment: 150%
Revenue: $600,000

Below quota: $400,000 × 6% = $24,000
Above quota: $200,000 × 9% = $18,000

Total Commission: $42,000

Quarterly Variable: $42,000
vs At-Quota ($24K): +$18,000 (75% bonus)
```
**Status**: Excellent quarter, maximizing accelerator

---

### Summary Table

| Scenario | Revenue | Attainment | Commission | vs Plan |
|----------|---------|------------|------------|---------|
| Commit | $320K | 80% | $19,200 | -$4,800 |
| Best Case | $450K | 112% | $28,500 | +$4,500 |
| Upside | $600K | 150% | $42,000 | +$18,000 |

### Key Insights

1. **Break-even point**: $400K (100% attainment)
2. **Accelerator value**: Each $10K above quota = $900 extra
3. **Commit gap**: Need $80K more to hit quota
4. **Upside potential**: 75% more commission if pipeline converts

### Recommendations for Mike
1. Focus on moving $80K from Best Case to Commit
2. Push for upside deals - 9% rate is lucrative
3. Prioritize larger deals for accelerator impact
```

## Skill Boundaries

### What This Skill Does Well
- Explaining commission math step-by-step
- Identifying calculation discrepancies
- Modeling what-if scenarios
- Documenting plan rules clearly

### What This Skill Cannot Do
- Access actual payout systems
- Make policy exceptions
- Override approved calculations
- Handle edge cases without rules

### When to Escalate to Human
- Policy exceptions or special approvals
- Historical adjustments requiring audit
- Plan design decisions
- Legal or HR compensation issues

## Iteration Guide

### Follow-up Prompts
- "What if Mike closes an extra $50K deal?"
- "Show me the break-even point to hit OTE."
- "Compare this plan to a flat 8% rate."
- "Model the impact of increasing Mike's quota by 20%."

### Refinement Cycle
1. Document plan rules clearly
2. Run sample calculations
3. Verify against actual statements
4. Build exception handling guide
5. Create rep-facing FAQ

## Checklists & Templates

### Commission Dispute Resolution Checklist
- [ ] Verify all deals in calculation
- [ ] Confirm close dates in pay period
- [ ] Check split/overlay credits
- [ ] Validate attainment tier
- [ ] Review for clawbacks/adjustments
- [ ] Compare to plan document

### Comp Plan Documentation Template
```markdown
## [Role] Compensation Plan - [Year]

### Structure
- Base Salary: $X
- OTE: $X
- Variable: $X (X% of OTE)
- Pay Period: [Monthly/Quarterly]

### Commission Mechanics
- Quota: $X/[period]
- Base Rate: X%
- Accelerator: X% above quota
- Threshold: X% minimum attainment

### Special Rules
- Splits: [Policy]
- Clawbacks: [Policy]
- Ramping: [New hire policy]

### Examples
[Include 3 scenarios at 80%, 100%, 120%]
```

## References

- Alexander Group Sales Compensation Design
- WorldatWork Incentive Compensation Handbook
- Salesforce Sales Cloud Commission Documentation
- Xactly Commission Best Practices

## Related Skills

- `pipeline-forecasting` - Project commission from forecast
- `deal-risk-scoring` - Prioritize high-commission deals
- `quota-planning` - Set achievable targets

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 15-30 min per analysis
- **Prerequisites**: Comp plan document, deal data
