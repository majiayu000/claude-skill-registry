---
name: portfolio_balancer.generate_report
description: "Compile comprehensive human-readable daily report with all analysis and recommendations"
user-invocable: false
---

# portfolio_balancer.generate_report

**Step 4/4** in **portfolio_balancer** workflow

> Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/portfolio_balancer.collect_portfolio_data`
- `/portfolio_balancer.analyze_allocation`
- `/portfolio_balancer.generate_recommendations`

## Instructions

**Goal**: Compile comprehensive human-readable daily report with all analysis and recommendations

# Generate Daily Report

## Objective

Compile a comprehensive, human-readable daily report that presents the portfolio snapshot, allocation analysis, and rebalancing recommendations in a clear format for manual review.

## Task

Combine all data from previous steps into a well-formatted markdown report following the doc spec quality criteria. The report should be immediately actionable while providing sufficient context for informed decision-making.

### Process

1. **Read all input files**
   Load the following from previous steps:
   - `portfolio_balancer/data/portfolio_snapshot.yml` (from collect_portfolio_data)
   - `portfolio_balancer/data/allocation_analysis.yml` (from analyze_allocation)
   - `portfolio_balancer/data/recommendations.yml` (from generate_recommendations)

2. **Generate report header**
   Include:
   - Current date as title
   - Total portfolio value
   - Data source (Chrome extension or manual upload)
   - Timestamp of data collection

3. **Create allocation table**
   Format the allocation data into a clear table showing:
   - Asset class
   - Target percentage (25%)
   - Current percentage
   - Current value
   - Drift amount

4. **Add stock allocation detail (if satellites enabled)**
   Break down the stock allocation:
   - Core index holdings and value
   - Satellite positions and values
   - Satellite allocation percentage vs target

5. **Write drift analysis section**
   Explain:
   - Which assets exceed the threshold
   - Direction and magnitude of drift
   - Four Seasons economic context

6. **Include margin analysis**
   Present:
   - Current margin usage
   - Monthly fees paid
   - Cost/benefit assessment
   - Efficiency recommendation

7. **Format rebalancing recommendations**
   Present recommendations clearly:
   - Summary of what action is needed (or "no rebalancing needed")
   - Specific buy/sell amounts per asset class
   - Suggested trades with symbols and shares
   - Implementation guidance

8. **Add notes section**
   Include any additional observations or context from the analysis.

9. **Save report with date-stamped filename**
   Output to `portfolio_balancer/reports/YYYY-MM-DD.md` using the current date.

## Output Format

### portfolio_balancer/reports/[DATE].md

A markdown report following the doc spec at `.deepwork/doc_specs/daily_portfolio_report.md`.

**Structure**:
```markdown
# Daily Portfolio Report: 2024-01-15

## Portfolio Summary

| Metric | Value |
|--------|-------|
| **Total Portfolio Value** | $100,000.00 |
| **Data Source** | Claude Chrome Extension |
| **Snapshot Time** | 2024-01-15 09:30:00 |
| **Drift Threshold** | 5% |

## Current Allocation

| Asset Class | Target | Current | Value | Drift |
|-------------|--------|---------|-------|-------|
| Stocks | 25% | 28% | $28,000 | +3% |
| Long-Term Bonds | 25% | 24% | $24,000 | -1% |
| Gold | 25% | 23% | $23,000 | -2% |
| Cash/Treasuries | 25% | 25% | $25,000 | 0% |

## Stock Allocation Detail

**Core Index Holdings**: $25,000 (89.3% of stocks)
- VTI: 100 shares @ $250.00 = $25,000

**Satellite Positions**: $3,000 (10.7% of stocks)
- AAPL: 10 shares @ $300.00 = $3,000

*Satellite target: 15% | Current: 10.7% | Underweight by 4.3%*

## Drift Analysis

**Status**: All allocations within threshold - no immediate rebalancing required.

| Asset | Drift | Threshold | Status |
|-------|-------|-----------|--------|
| Stocks | +3% | 5% | Within threshold |
| Long-Term Bonds | -1% | 5% | Within threshold |
| Gold | -2% | 5% | Within threshold |
| Cash/Treasuries | 0% | 5% | On target |

### Four Seasons Context

Current portfolio positioning:
- **Overweight Stocks (+3%)**: Positioned for prosperity/growth conditions
- **Underweight Gold (-2%)**: Reduced protection against inflation
- **Underweight Bonds (-1%)**: Reduced protection against deflation

*Interpretation: Portfolio slightly favors growth scenarios; consider rebalancing if economic conditions shift toward inflation.*

## Margin Analysis

| Metric | Value |
|--------|-------|
| Margin Balance | $5,000 |
| Monthly Fees Paid | $50.00 |
| Expected Monthly Cost | $25.00 |
| Annual Overpayment | $300.00 |

**Assessment**: POOR efficiency - paying 2x expected margin cost.

**Recommendation**: Review margin account structure. Consider reducing margin balance or negotiating fees with broker.

## Rebalancing Recommendations

### Summary
No immediate rebalancing required - all asset classes within the 5% drift threshold.

### Satellite Adjustment (Optional)
Consider increasing satellite allocation from 10.7% to 15% of stock holdings:
- Add ~$1,200 to satellite positions
- Options: Add to AAPL or select new satellite pick

### Next Actions
1. Continue monitoring - next review in 30 days
2. Review margin fee structure
3. Consider satellite allocation adjustment

## Notes

- Portfolio is well-balanced for current economic conditions
- Minor drift toward growth positioning is acceptable
- Margin costs warrant attention separate from rebalancing

---

*This report is for informational purposes only. No trades are executed automatically. Review recommendations and execute manually if you agree.*
```

## Quality Criteria

The report must satisfy the doc spec criteria at `.deepwork/doc_specs/daily_portfolio_report.md`:

1. **Portfolio Snapshot**: Includes date, total value, all position values
2. **Allocation Table**: Shows current vs target (25%) with percentage drift
3. **Drift Analysis**: Clearly identifies assets exceeding threshold
4. **Satellite Breakdown**: Shows core vs satellite if satellites enabled
5. **Margin Efficiency**: Includes usage, fees, and cost/benefit assessment
6. **Actionable Recommendations**: Specific buy/sell amounts (or "no action needed")
7. **Four Seasons Context**: References economic conditions for positioning

Additional criteria:
- Report is well-formatted markdown
- All numbers are properly formatted (currency, percentages)
- Report filename uses current date: `YYYY-MM-DD.md`
- Disclaimer about manual execution included
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This report is the primary deliverable of the portfolio_balancer workflow. It should be comprehensive enough for the user to make informed decisions, yet concise enough to review quickly. The Permanent Portfolio philosophy values simplicity - the report should reflect that by being clear and actionable rather than overwhelming.

**Critical Reminder**: Always include the disclaimer that this is a read-only system and no trades are executed automatically. The user must manually review and execute any recommendations.


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
- `portfolio_balancer/data/allocation_analysis.yml` (from `analyze_allocation`)
- `portfolio_balancer/data/recommendations.yml` (from `generate_recommendations`)

## Work Branch

Use branch format: `deepwork/portfolio_balancer-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/portfolio_balancer-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `portfolio_balancer/reports/[DATE].md`
  **Doc Spec**: Daily Portfolio Report
  > Human-readable daily analysis of Permanent Portfolio allocation, drift, and rebalancing recommendations
  **Definition**: `.deepwork/doc_specs/daily_portfolio_report.md`
  **Target Audience**: Portfolio owner for manual review before executing any trades
  **Quality Criteria**:
  1. **Portfolio Snapshot**: Must include current date, total portfolio value, and all position values
  2. **Allocation Table**: Must show current vs target allocation (25/25/25/25) for all four asset classes with percentage drift
  3. **Drift Analysis**: Must clearly identify which assets exceed the drift threshold and by how much
  4. **Satellite Breakdown**: If satellites exist, must show core index vs satellite allocation within the stocks portion
  5. **Margin Efficiency**: Must include margin usage amount, monthly fees paid, and cost/benefit assessment
  6. **Actionable Recommendations**: Must provide specific buy/sell amounts to restore target allocations (or state no rebalancing needed)
  7. **Four Seasons Context**: Should reference which economic conditions favor current over/underweight positions

  <details>
  <summary>Example Document Structure</summary>

  ```markdown
  # Daily Portfolio Report: [DATE]

  ## Portfolio Summary
  - Total portfolio value
  - Data source (Chrome extension / manual upload)
  - As-of timestamp

  ## Current Allocation

  | Asset Class | Target | Current | Value | Drift |
  |-------------|--------|---------|-------|-------|
  | Stocks | 25% | X% | $X | +/-X% |
  | Long-Term Bonds | 25% | X% | $X | +/-X% |
  | Gold | 25% | X% | $X | +/-X% |
  | Cash/Treasuries | 25% | X% | $X | +/-X% |

  ## Stock Allocation Detail
  If satellites are configured:
  - Core Index: X% of stocks ($X)
  - Satellite Picks: X% of stocks ($X)
    - Individual satellite positions listed

  ## Drift Analysis
  - Assets exceeding threshold
  - Direction of drift (over/underweight)
  - Economic conditions that favor current positioning (Four Seasons context)

  ## Margin Analysis
  - Current margin usage
  - Monthly margin fees
  - Cost/benefit assessment
  - Recommendation on margin efficiency

  ## Rebalancing Recommendations
  Specific actions needed (or statement that no rebalancing required):
  - Buy/sell amounts per asset class
  - Order of operations if relevant
  - Notes on tax implications or timing considerations

  ## Notes
  Any additional context or observations
  ```

  </details>

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "Step 4/4 complete, outputs: portfolio_balancer/reports/[DATE].md"
3. **Workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/portfolio_balancer/job.yml`, `.deepwork/jobs/portfolio_balancer/steps/generate_report.md`