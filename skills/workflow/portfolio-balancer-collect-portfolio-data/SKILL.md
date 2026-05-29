---
name: portfolio_balancer.collect_portfolio_data
description: "Gather current portfolio positions, values, and prices from Robinhood using bin/robinhood CLI"
user-invocable: false
---

# portfolio_balancer.collect_portfolio_data

**Step 1/4** in **portfolio_balancer** workflow

> Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations


## Instructions

**Goal**: Gather current portfolio positions, values, and prices from Robinhood using bin/robinhood CLI

# Collect Portfolio Data

## Objective

Gather current portfolio positions, values, and prices from Robinhood to create a complete snapshot for Permanent Portfolio analysis.

## Task

Collect all portfolio data needed to analyze the Permanent Portfolio allocation using the `bin/robinhood` CLI.

### Process

1. **Ask structured questions to gather user inputs**
   Use the AskUserQuestion tool to collect:
   - `drift_threshold`: Percentage that triggers rebalancing (e.g., 5 or 10)
   - `satellite_enabled`: Whether to track satellite stock picks separately

2. **Collect portfolio data using the Robinhood CLI**

   Run the positions command to save today's snapshot:
   ```bash
   bin/robinhood positions --save
   ```

   This command is **idempotent** - it will skip if today's snapshot already exists.
   Use `--force` to overwrite an existing snapshot.

   If not authenticated, prompt user to run `bin/robinhood auth` first.

   **Snapshot location**: `portfolio_balancer/data/snapshots/YYYY-MM-DD.json`

   **Fallback: Manual Upload**
   If the CLI is unavailable, ask for a Robinhood export file (CSV or PDF).

   **Note**: Chrome extension browser automation is NOT supported - Robinhood blocks automated access.

3. **Categorize holdings into Permanent Portfolio asset classes**
   - **Stocks**: Individual stocks, stock ETFs (e.g., VTI, SPY, VOO)
   - **Long-Term Bonds**: Bond ETFs with long duration (e.g., TLT, VGLT, EDV)
   - **Gold**: Gold ETFs or holdings (e.g., GLD, IAU, SGOL)
   - **Cash/Treasuries**: Cash balance, money market, short-term treasuries (e.g., SHV, BIL)

4. **Identify satellite positions (if enabled)**
   If `satellite_enabled` is true, identify individual stock picks within the Stocks allocation that are not broad index funds.

5. **Capture margin information**
   - Current margin balance (if using margin)
   - Monthly margin fees/interest rate
   - Available margin

6. **Create portfolio snapshot**
   Output all collected data in structured YAML format.

## Output Format

### portfolio_balancer/data/portfolio_snapshot.yml

A YAML file containing the complete portfolio snapshot.

**Structure**:
```yaml
snapshot_date: "YYYY-MM-DD"
snapshot_time: "HH:MM:SS"
data_source: "chrome" | "upload"
drift_threshold: 5  # user-specified percentage

total_portfolio_value: 100000.00

# Permanent Portfolio asset classes
asset_classes:
  stocks:
    total_value: 28000.00
    positions:
      - symbol: "VTI"
        name: "Vanguard Total Stock Market ETF"
        shares: 100
        price: 250.00
        value: 25000.00
        type: "core_index"
      - symbol: "AAPL"
        name: "Apple Inc."
        shares: 10
        price: 300.00
        value: 3000.00
        type: "satellite"  # if satellite_enabled
    core_value: 25000.00
    satellite_value: 3000.00  # if satellite_enabled

  long_term_bonds:
    total_value: 24000.00
    positions:
      - symbol: "TLT"
        name: "iShares 20+ Year Treasury Bond ETF"
        shares: 200
        price: 120.00
        value: 24000.00

  gold:
    total_value: 23000.00
    positions:
      - symbol: "GLD"
        name: "SPDR Gold Shares"
        shares: 100
        price: 230.00
        value: 23000.00

  cash_treasuries:
    total_value: 25000.00
    positions:
      - symbol: "CASH"
        name: "Cash Balance"
        value: 15000.00
      - symbol: "SHV"
        name: "iShares Short Treasury Bond ETF"
        shares: 90
        price: 111.11
        value: 10000.00

# Margin information
margin:
  enabled: true
  current_balance: 5000.00
  monthly_fee: 50.00
  interest_rate: 0.06  # 6% annual
  available_margin: 15000.00

# Satellite tracking (if enabled)
satellite_tracking:
  enabled: true
  target_percentage: 15  # 15% of stock allocation
  positions:
    - symbol: "AAPL"
      value: 3000.00
```

## Quality Criteria

- All four asset classes are represented (even if value is 0)
- Each position has symbol, name, and value at minimum
- Total portfolio value equals sum of all asset class values
- Margin information captured if margin is being used
- Satellite positions identified if satellite_enabled is true
- Data source and timestamp recorded
- Drift threshold stored for use in subsequent steps
- YAML is valid and parseable
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the data collection foundation for Permanent Portfolio analysis. The quality and completeness of this snapshot directly impacts the accuracy of allocation analysis and rebalancing recommendations. Harry Browne's Permanent Portfolio requires equal 25% allocations across stocks, long-term bonds, gold, and cash/treasuries - this step must capture all holdings to enable that analysis.

**Important**: This system is READ-ONLY. We are only collecting data for analysis, not executing any trades.


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

**User Parameters** - Gather from user before starting:
- **drift_threshold**: Percentage drift that triggers rebalancing recommendations (e.g., 5 or 10)
- **satellite_enabled**: Whether to track satellite stock picks separately (true/false)


## Work Branch

Use branch format: `deepwork/portfolio_balancer-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/portfolio_balancer-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `portfolio_balancer/data/snapshots/[DATE].json`
- `portfolio_balancer/data/portfolio_snapshot.yml`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "Step 1/4 complete, outputs: portfolio_balancer/data/snapshots/[DATE].json, portfolio_balancer/data/portfolio_snapshot.yml"
3. **Continue workflow**: Use Skill tool to invoke `/portfolio_balancer.analyze_allocation`

---

**Reference files**: `.deepwork/jobs/portfolio_balancer/job.yml`, `.deepwork/jobs/portfolio_balancer/steps/collect_portfolio_data.md`