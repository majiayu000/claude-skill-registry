---
name: nixtla-market-risk-analyzer
description: "Analyze market risk with VaR, volatility, and position sizing using forecast data. Use when assessing investment risk. Trigger with 'analyze market risk' or 'calculate VaR'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Market Risk Analyzer

Calculates key market risk metrics and recommends optimal position sizes using historical data analysis.

## Overview

This skill analyzes market risk using historical price data to calculate Value at Risk (VaR), volatility metrics, maximum drawdown, Sharpe ratios, and optimal position sizing. Provides actionable insights for managing investment risk and optimizing portfolio allocation. Uses four specialized Python scripts for data preparation, risk analysis, position sizing, and report generation.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: Optional `NIXTLA_TIMEGPT_API_KEY` for volatility forecasting (not required for core analysis)

**Packages**:
```bash
pip install pandas numpy scipy matplotlib
# Optional for forecasting:
pip install nixtla
```

**Input Data Format**: CSV file with columns:
- Date column: `ds`, `date`, or `timestamp`
- Price column: `y`, `price`, or `close`

## Instructions

### Step 1: Prepare Price Data

Execute the data preparation script to load prices and calculate returns:

```bash
python {baseDir}/scripts/prepare_data.py prices.csv --method log --output returns.csv
```

**Script**: `{baseDir}/scripts/prepare_data.py`
- Loads price data from CSV
- Calculates log or simple returns
- Detects time series frequency
- Outputs: `returns.csv`

### Step 2: Calculate Risk Metrics

Run comprehensive risk analysis on the price data:

```bash
python {baseDir}/scripts/risk_metrics.py prices.csv --output risk_metrics.json --risk-free-rate 0.05
```

**Script**: `{baseDir}/scripts/risk_metrics.py`
- Calculates VaR at 95% and 99% confidence levels
- Computes historical and rolling volatility
- Analyzes maximum drawdown and recovery periods
- Calculates Sharpe and Sortino ratios
- Outputs: `risk_metrics.json`

**Key Metrics**:
- **VaR**: Maximum expected loss at confidence level
- **CVaR**: Expected loss when VaR is exceeded
- **Volatility**: Daily and annualized, with regime classification
- **Drawdown**: Maximum loss from peak, recovery analysis
- **Sharpe Ratio**: Risk-adjusted return metric

### Step 3: Calculate Position Sizing

Determine optimal position sizes using multiple methodologies:

```bash
python {baseDir}/scripts/position_sizing.py \
  --account-size 100000 \
  --risk-per-trade 0.02 \
  --stop-loss 0.05 \
  --target-volatility 0.15 \
  --asset-volatility 0.25 \
  --var-95 -0.02 \
  --max-var-loss 0.03 \
  --output position_sizing.json
```

**Script**: `{baseDir}/scripts/position_sizing.py`
- **Fixed Fractional**: Risk-based position sizing
- **Volatility Adjusted**: Targets specific portfolio volatility
- **VaR-Based**: Limits maximum VaR loss
- **Kelly Criterion**: Optimal bet sizing (full, half, quarter)
- Outputs: `position_sizing.json` with recommended conservative position

### Step 4: Generate Risk Report

Create comprehensive markdown report with visualizations:

```bash
python {baseDir}/scripts/generate_report.py prices.csv \
  --risk-metrics risk_metrics.json \
  --position-sizing position_sizing.json \
  --output risk_report.md \
  --output-dir .
```

**Script**: `{baseDir}/scripts/generate_report.py`
- Generates markdown report with all metrics
- Creates three visualizations:
  - `drawdown.png`: Price history and drawdown chart
  - `volatility.png`: Rolling volatility over time
  - `var.png`: Return distribution with VaR levels
- Outputs: `risk_report.md`, PNG charts

## Output

**Generated Files**:
- `returns.csv`: Calculated returns series
- `risk_metrics.json`: Complete risk metrics
- `position_sizing.json`: Position sizing recommendations
- `risk_report.md`: Comprehensive markdown report
- `drawdown.png`: Price and drawdown visualization
- `volatility.png`: Rolling volatility chart
- `var.png`: Return distribution with VaR markers

**Key Report Sections**:
1. Executive Summary (VaR, volatility, drawdown, Sharpe)
2. Value at Risk analysis (95%, 99% confidence)
3. Volatility metrics and regime classification
4. Drawdown analysis with recovery periods
5. Risk-adjusted returns (Sharpe, Sortino)
6. Position sizing recommendations with Kelly criterion
7. Visualizations and risk warnings

## Error Handling

**Error**: `No date column found`
**Solution**: Ensure CSV has column named `ds`, `date`, or `timestamp`

**Error**: `No price column found`
**Solution**: Ensure CSV has column named `y`, `price`, or `close`

**Error**: `Insufficient data for analysis`
**Solution**: Provide at least 30 price points for reliable statistical analysis

**Error**: `Module not found: matplotlib`
**Solution**: Install visualization dependencies: `pip install matplotlib`

**Error**: `NIXTLA_TIMEGPT_API_KEY not set`
**Solution**: Only needed for optional volatility forecasting. Core analysis works without it.

## Examples

### Example 1: Analyze Stock Risk

```bash
# Complete workflow for stock analysis
python {baseDir}/scripts/prepare_data.py AAPL_prices.csv
python {baseDir}/scripts/risk_metrics.py AAPL_prices.csv
python {baseDir}/scripts/position_sizing.py --account-size 100000 --asset-volatility 0.28
python {baseDir}/scripts/generate_report.py AAPL_prices.csv

# Expected output:
# VaR (95%): -2.15%
# Max Drawdown: -35.2%
# Sharpe Ratio: 0.95
# Recommended Position: $45,000 (45% of account)
```

### Example 2: Prediction Market Contract Analysis

```bash
# High volatility asset with conservative sizing
python {baseDir}/scripts/risk_metrics.py contract_prices.csv --output contract_risk.json
python {baseDir}/scripts/position_sizing.py \
  --account-size 50000 \
  --risk-per-trade 0.01 \
  --asset-volatility 0.45 \
  --output contract_sizing.json

# Expected output:
# VaR (95%): -8.5%
# Volatility Regime: HIGH
# Recommended Position: $12,000 (24% of account)
```

### Example 3: Custom Risk Parameters

```bash
# Conservative parameters for volatile market
python {baseDir}/scripts/position_sizing.py \
  --account-size 200000 \
  --risk-per-trade 0.01 \
  --stop-loss 0.03 \
  --target-volatility 0.10 \
  --max-var-loss 0.02

# Aggressive parameters for stable market
python {baseDir}/scripts/position_sizing.py \
  --account-size 200000 \
  --risk-per-trade 0.03 \
  --stop-loss 0.07 \
  --target-volatility 0.20 \
  --max-var-loss 0.05
```

## Resources

**Statistical Methods**:
- VaR: Historical simulation, parametric (Gaussian), Monte Carlo
- Volatility: EWMA, GARCH models available in extension
- Drawdown: Peak-to-trough analysis with recovery tracking

**Position Sizing Theory**:
- Kelly Criterion: Optimal bet sizing for known edge
- Fixed Fractional: Fixed percentage risk per trade
- Volatility Targeting: Normalize risk across assets
- VaR-Based: Limit tail risk exposure

**Best Practices**:
- Use Half Kelly for practical trading (Full Kelly too aggressive)
- Combine multiple sizing methods, choose most conservative
- Adjust for liquidity constraints and execution costs
- Monitor regime changes (HIGH/NORMAL/LOW volatility)
- Rebalance positions when volatility regime shifts

**References**:
- VaR methodology: RiskMetrics Technical Document (J.P. Morgan)
- Kelly Criterion: Fortune's Formula (Poundstone)
- Sharpe Ratio: "The Sharpe Ratio" (Sharpe, 1994)
- Position Sizing: "Trade Your Way to Financial Freedom" (Tharp)
