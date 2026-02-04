---
name: portfolio_balancer.generate_recommendations
description: "Create specific rebalancing recommendations based on drift analysis"
user-invocable: false
---

# portfolio_balancer.generate_recommendations

**Step 3/4** in **portfolio_balancer** workflow

> Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/portfolio_balancer.analyze_allocation`

## Instructions

**Goal**: Create specific rebalancing recommendations based on drift analysis

# Generate Recommendations

## Objective

Create specific, actionable rebalancing recommendations based on the allocation drift analysis to restore the 25/25/25/25 Permanent Portfolio targets.

## Task

Using the allocation analysis, calculate the exact dollar amounts needed to buy or sell in each asset class to restore target allocations. Generate clear, prioritized recommendations for manual execution.

### Process

1. **Read the allocation analysis**
   Load `portfolio_balancer/data/allocation_analysis.yml` from the analyze_allocation step.

2. **Determine if rebalancing is needed**
   - If no asset class exceeds the drift threshold, generate "no action needed" recommendation
   - If rebalancing is needed, proceed to calculate specific actions

3. **Calculate rebalancing amounts**
   For each asset class:
   ```
   target_value = total_portfolio_value * 0.25
   adjustment = target_value - current_value
   ```
   - Positive adjustment = BUY
   - Negative adjustment = SELL

4. **Generate specific trade recommendations**
   For each asset class needing adjustment:
   - Identify the primary ETF/position to trade
   - Calculate shares to buy/sell (if applicable)
   - Consider transaction costs and minimums

5. **Handle satellite adjustments (if enabled)**
   If satellite allocation is off-target:
   - Recommend adjustments within the stock allocation
   - Balance between core index and satellite positions

6. **Generate margin recommendations**
   Based on margin analysis:
   - Recommend reducing margin if cost-ineffective
   - Suggest optimal margin usage if beneficial

7. **Prioritize recommendations**
   Order recommendations by:
   1. Assets exceeding threshold (most urgent)
   2. Largest drift amounts
   3. Satellite adjustments
   4. Margin optimization

8. **Add implementation notes**
   Include practical considerations:
   - Tax implications (wash sale rules, capital gains)
   - Order of operations (sell before buy if needed)
   - Market timing considerations

## Output Format

### portfolio_balancer/data/recommendations.yml

A YAML file containing prioritized rebalancing recommendations.

**Structure**:
```yaml
recommendation_date: "YYYY-MM-DD"
rebalancing_needed: true
urgency: "moderate"  # none, low, moderate, high

summary: "Rebalance stocks and gold to restore 25/25/25/25 allocation"

# Detailed recommendations
recommendations:
  - priority: 1
    action: "SELL"
    asset_class: "stocks"
    amount: 3000.00
    reason: "Stocks overweight by 3% ($3,000)"
    suggested_trade:
      symbol: "VTI"
      shares: 12
      approximate_value: 3000.00
    notes: "Consider tax implications of selling"

  - priority: 2
    action: "BUY"
    asset_class: "gold"
    amount: 2000.00
    reason: "Gold underweight by 2% ($2,000)"
    suggested_trade:
      symbol: "GLD"
      shares: 9
      approximate_value: 2070.00
    notes: "Round up to whole shares"

  - priority: 3
    action: "BUY"
    asset_class: "long_term_bonds"
    amount: 1000.00
    reason: "Long-term bonds underweight by 1% ($1,000)"
    suggested_trade:
      symbol: "TLT"
      shares: 8
      approximate_value: 960.00
    notes: "Slight underbuy due to share price"

# Satellite recommendations (if applicable)
satellite_recommendations:
  - action: "BUY"
    description: "Increase satellite allocation from 10.7% to 15% of stocks"
    amount: 1200.00
    notes: "Consider adding to existing satellite positions or new picks"

# Margin recommendations (if applicable)
margin_recommendations:
  - action: "REVIEW"
    description: "Margin fees ($50/mo) exceed expected cost ($25/mo)"
    recommendation: "Consider reducing margin balance or negotiating fees"
    potential_savings: 300.00  # annual

# Implementation guidance
implementation:
  order_of_operations:
    - "1. Execute SELL orders first to generate cash"
    - "2. Execute BUY orders with proceeds"
    - "3. Adjust satellite positions"

  tax_considerations:
    - "VTI sale may trigger capital gains - check cost basis"
    - "Consider tax-loss harvesting opportunities"

  timing_notes:
    - "Execute during market hours for best liquidity"
    - "Consider limit orders to control execution price"

# No-action scenario (when rebalancing not needed)
# recommendations:
#   - priority: 1
#     action: "HOLD"
#     reason: "All asset classes within 5% drift threshold"
#     notes: "Continue monitoring; next review recommended in 30 days"
```

## Quality Criteria

- Clear determination of whether rebalancing is needed
- Specific dollar amounts calculated for each recommended action
- Suggested trades include symbol, shares, and approximate value
- Recommendations prioritized by urgency
- Satellite recommendations included if satellite tracking enabled
- Margin recommendations included if margin analysis flagged issues
- Implementation guidance with order of operations
- Tax and timing considerations noted
- YAML is valid and parseable
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This step translates analysis into action. The Permanent Portfolio philosophy emphasizes simplicity and discipline - rebalancing only when drift exceeds the threshold, not chasing market movements. Recommendations should be clear enough for manual execution but include enough context for informed decision-making.

**Critical Reminder**: This system generates RECOMMENDATIONS ONLY. No trades are executed automatically. The user must manually review and execute any trades they agree with.


### Job Context

Automated daily portfolio analysis implementing Harry Browne's Permanent Portfolio strategy.

The Permanent Portfolio maintains equal 25% allocations across four asset classes designed
to perform in different economic conditions:
- Stocks (25%): Prosperity/Growth
- Long-Term Bonds (25%): Deflation/Recession
- Gold (25%): Inflation
- Cash/Treasuries (25%): Tight Money/Recession

This workflow:
1. Collects portfolio data via `bin/robinhood positions --save` CLI
2. Analyzes current allocation against 25/25/25/25 targets
3. Tracks satellite stock picks (optional 10-20% of stock allocation)
4. Evaluates margin usage efficiency vs fees paid
5. Generates rebalancing recommendations when drift exceeds user-defined threshold
6. Produces a human-readable daily report for manual review

IMPORTANT: This system is read-only. No trades are executed automatically.
All recommendations require manual review and execution.


## Required Inputs


**Files from Previous Steps** - Read these first:
- `portfolio_balancer/data/allocation_analysis.yml` (from `analyze_allocation`)

## Work Branch

Use branch format: `deepwork/portfolio_balancer-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/portfolio_balancer-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `portfolio_balancer/data/recommendations.yml`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "Step 3/4 complete, outputs: portfolio_balancer/data/recommendations.yml"
3. **Continue workflow**: Use Skill tool to invoke `/portfolio_balancer.generate_report`

---

**Reference files**: `.deepwork/jobs/portfolio_balancer/job.yml`, `.deepwork/jobs/portfolio_balancer/steps/generate_recommendations.md`