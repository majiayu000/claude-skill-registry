---
name: portfolio_balancer.analyze_allocation
description: "Calculate current allocation percentages, identify drift from targets, analyze margin efficiency"
user-invocable: false
---

# portfolio_balancer.analyze_allocation

**Step 2/4** in **portfolio_balancer** workflow

> Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/portfolio_balancer.collect_portfolio_data`

## Instructions

**Goal**: Calculate current allocation percentages, identify drift from targets, analyze margin efficiency

# Analyze Allocation

## Objective

Calculate current allocation percentages against the 25/25/25/25 Permanent Portfolio targets, identify drift from targets, and analyze margin efficiency.

## Task

Analyze the portfolio snapshot to determine how current allocations compare to Harry Browne's Permanent Portfolio targets. Identify which asset classes are over or underweight and assess whether margin usage is cost-effective.

### Process

1. **Read the portfolio snapshot**
   Load `portfolio_balancer/data/portfolio_snapshot.yml` from the collect_portfolio_data step.

2. **Calculate current allocation percentages**
   For each asset class, calculate:
   ```
   current_percentage = (asset_class_value / total_portfolio_value) * 100
   ```

3. **Calculate drift from targets**
   The Permanent Portfolio target is 25% for each asset class:
   ```
   drift = current_percentage - 25.0
   ```
   - Positive drift = overweight
   - Negative drift = underweight

4. **Determine if rebalancing is needed**
   Compare each asset class drift against the `drift_threshold` from the snapshot:
   - If any |drift| > drift_threshold, rebalancing is recommended
   - Track which specific asset classes exceed the threshold

5. **Analyze satellite allocation (if enabled)**
   If satellite_tracking is enabled:
   - Calculate satellite % of total stock allocation
   - Compare against target (typically 10-20%)
   - Determine if satellite allocation needs adjustment

6. **Analyze margin efficiency**
   If margin is enabled:
   - Calculate annual margin cost: `margin_balance * interest_rate`
   - Assess cost/benefit: Is the expected return on margined assets > margin cost?
   - Flag if margin fees exceed reasonable thresholds

7. **Apply Four Seasons context**
   Note which economic conditions favor current over/underweight positions:
   - **Spring (Prosperity)**: Stocks benefit
   - **Summer (Inflation)**: Gold benefits
   - **Autumn (Tight Money)**: Cash benefits
   - **Winter (Deflation)**: Long-term bonds benefit

## Output Format

### portfolio_balancer/data/allocation_analysis.yml

A YAML file containing the complete allocation analysis.

**Structure**:
```yaml
analysis_date: "YYYY-MM-DD"
drift_threshold: 5  # from snapshot

total_portfolio_value: 100000.00

# Allocation breakdown
allocations:
  stocks:
    target_percentage: 25.0
    current_percentage: 28.0
    current_value: 28000.00
    drift: 3.0  # overweight by 3%
    exceeds_threshold: false
    status: "overweight"
    # Satellite breakdown (if enabled)
    satellite:
      enabled: true
      core_percentage: 89.3  # % of stocks in core index
      satellite_percentage: 10.7  # % of stocks in satellites
      target_satellite_percentage: 15.0
      satellite_drift: -4.3  # underweight satellites

  long_term_bonds:
    target_percentage: 25.0
    current_percentage: 24.0
    current_value: 24000.00
    drift: -1.0  # underweight by 1%
    exceeds_threshold: false
    status: "underweight"

  gold:
    target_percentage: 25.0
    current_percentage: 23.0
    current_value: 23000.00
    drift: -2.0
    exceeds_threshold: false
    status: "underweight"

  cash_treasuries:
    target_percentage: 25.0
    current_percentage: 25.0
    current_value: 25000.00
    drift: 0.0
    exceeds_threshold: false
    status: "on_target"

# Overall rebalancing assessment
rebalancing:
  needed: false
  reason: "No asset class exceeds 5% drift threshold"
  assets_exceeding_threshold: []

# Margin analysis
margin_analysis:
  enabled: true
  current_balance: 5000.00
  annual_cost: 300.00  # balance * rate
  monthly_cost: 25.00
  monthly_fees_paid: 50.00
  efficiency_rating: "poor"  # paying more in fees than calculated cost
  recommendation: "Review margin fees - paying $50/mo vs $25/mo expected cost"

# Four Seasons context
economic_context:
  current_overweights:
    - asset: "stocks"
      favored_condition: "Prosperity/Growth (Spring)"
      drift: 3.0
  current_underweights:
    - asset: "gold"
      favored_condition: "Inflation (Summer)"
      drift: -2.0
    - asset: "long_term_bonds"
      favored_condition: "Deflation/Recession (Winter)"
      drift: -1.0
  interpretation: "Portfolio currently positioned for prosperity; vulnerable to inflation"
```

## Quality Criteria

- All four asset classes analyzed with current percentage and drift
- Drift calculations are mathematically correct
- Rebalancing threshold comparison is accurate
- Margin efficiency analysis included if margin is enabled
- Satellite analysis included if satellite tracking is enabled
- Four Seasons economic context provided
- All percentages sum to 100% (within rounding tolerance)
- YAML is valid and parseable
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This analysis is the core of Permanent Portfolio management. Harry Browne designed the 25/25/25/25 allocation to provide balance across all economic conditions - the "Four Seasons" of the economic cycle. Drift analysis helps determine when rebalancing is needed to maintain this balance.

The margin analysis helps users understand whether their use of margin is cost-effective, comparing actual fees paid against calculated costs and expected benefits.


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
- `portfolio_balancer/data/portfolio_snapshot.yml` (from `collect_portfolio_data`)

## Work Branch

Use branch format: `deepwork/portfolio_balancer-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/portfolio_balancer-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `portfolio_balancer/data/allocation_analysis.yml`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "Step 2/4 complete, outputs: portfolio_balancer/data/allocation_analysis.yml"
3. **Continue workflow**: Use Skill tool to invoke `/portfolio_balancer.generate_recommendations`

---

**Reference files**: `.deepwork/jobs/portfolio_balancer/job.yml`, `.deepwork/jobs/portfolio_balancer/steps/analyze_allocation.md`