---
name: nixtla-correlation-mapper
description: |
  Analyzes multi-contract correlations and generates hedge recommendations.
  Use when managing a portfolio of correlated assets and needing to mitigate risk.
  Trigger with "analyze correlations", "suggest hedge", "portfolio risk assessment".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Correlation Mapper

Identifies correlations between multiple contracts and generates hedging strategies for portfolio risk management.

## Overview

Analyzes relationships between assets in a portfolio to suggest hedging strategies. Takes CSV data with multiple time series, calculates correlation matrix, identifies significant relationships, and outputs hedge recommendations with visualizations. Generates correlation heatmap, rolling correlation plots, and hedge effectiveness charts.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: None required (optional: `NIXTLA_TIMEGPT_API_KEY` for forecasted correlations)

**Packages**:
```bash
pip install pandas numpy scipy matplotlib seaborn
```

**Input Format**: CSV with columns: `unique_id` (contract identifier), `ds` (date), `y` (price/value)

## Instructions

### Step 1: Prepare Data

Load multi-series contract data and calculate returns. Uses {baseDir}/scripts/prepare_data.py.

```bash
python scripts/prepare_data.py contracts.csv --method log --output-dir results/
```

**Output**: `prices_wide.csv`, `returns.csv`

### Step 2: Calculate Correlations

Calculate correlation matrix and identify significant pairs. Uses {baseDir}/scripts/correlation_analysis.py.

```bash
python scripts/correlation_analysis.py \
  --returns results/returns.csv \
  --method pearson \
  --threshold 0.5 \
  --rolling-window 30 \
  --output-dir results/
```

**Output**: `correlation_matrix.csv`, `correlation_pvalues.csv`, `high_correlations.json`, `rolling_correlations.csv`

### Step 3: Generate Hedge Recommendations

Calculate optimal hedge ratios using regression or minimum variance methods. Uses {baseDir}/scripts/hedge_recommendations.py.

```bash
python scripts/hedge_recommendations.py \
  --returns results/returns.csv \
  --correlation results/correlation_matrix.csv \
  --method ols \
  --top-n 10 \
  --portfolio-value 100000 \
  --output-dir results/
```

**Output**: `hedge_recommendations.csv`, `hedge_recommendations.json`, `hedged_portfolio.csv`

### Step 4: Create Visualizations

Generate correlation heatmap, rolling correlation plot, and hedge effectiveness chart. Uses {baseDir}/scripts/visualize.py.

```bash
python scripts/visualize.py \
  --correlation results/correlation_matrix.csv \
  --rolling results/rolling_correlations.csv \
  --recommendations results/hedge_recommendations.json \
  --output-dir results/ \
  --top-n 5
```

**Output**: `correlation_heatmap.png`, `rolling_correlation.png`, `hedge_effectiveness.png`

### Step 5: Generate Report

Create comprehensive markdown report with all analysis results. Uses {baseDir}/scripts/generate_report.py.

```bash
python scripts/generate_report.py \
  --correlation results/correlation_matrix.csv \
  --high-correlations results/high_correlations.json \
  --recommendations results/hedge_recommendations.json \
  --output results/correlation_report.md
```

**Output**: `correlation_report.md`

## Output

- **correlation_matrix.csv**: Full pairwise correlation matrix
- **correlation_heatmap.png**: Visual correlation heatmap
- **correlation_pvalues.csv**: Statistical significance p-values
- **high_correlations.json**: Pairs exceeding correlation threshold
- **hedge_recommendations.csv**: Detailed hedging strategies with ratios
- **hedged_portfolio.csv**: Sample portfolio allocation with long/short positions
- **rolling_correlations.csv**: Time-series correlation stability
- **rolling_correlation.png**: Rolling correlation visualization
- **hedge_effectiveness.png**: Variance reduction by contract pair
- **correlation_report.md**: Comprehensive analysis report

## Error Handling

**Error: Input file not found**
- Verify file path with `ls -la`
- Check current directory and use absolute paths

**Error: Missing required columns**
- Ensure CSV has `unique_id`, `ds`, `y` columns
- Verify column names match exactly (case-sensitive)

**Error: Insufficient data points**
- Need at least 30 data points per contract for reliable correlations
- Verify data has sufficient time-series history

**Error: Invalid data format**
- Check that `y` values are numeric (not strings)
- Ensure dates are parseable (ISO format recommended)
- Remove or handle missing values

**Error: Insufficient contracts**
- Need at least 2 contracts for correlation analysis
- Verify `unique_id` column has multiple distinct values

## Examples

### Example 1: Crypto Portfolio

**Input** (portfolio.csv):
```csv
unique_id,ds,y
BTC,2024-01-01,42000
ETH,2024-01-01,2200
BTC,2024-01-02,42500
ETH,2024-01-02,2250
```

**Workflow**:
```bash
python scripts/prepare_data.py portfolio.csv
python scripts/correlation_analysis.py
python scripts/hedge_recommendations.py
python scripts/visualize.py
python scripts/generate_report.py
```

**Result**: Correlation 0.85 between BTC-ETH, hedge ratio -0.95, variance reduction 72%

### Example 2: Prediction Market Contracts

**Input**: 5 election-related prediction market contracts

**Command**:
```bash
python scripts/prepare_data.py elections.csv --output-dir election_analysis/
python scripts/correlation_analysis.py --threshold 0.7 --output-dir election_analysis/
python scripts/hedge_recommendations.py --top-n 5 --output-dir election_analysis/
python scripts/visualize.py --output-dir election_analysis/
python scripts/generate_report.py --output election_analysis/report.md
```

**Result**: Identified 3 pairs with correlation > 0.7, top hedge reduces variance by 62%

## Resources

**Scripts**: All analysis scripts located in `{baseDir}/scripts/`
- `prepare_data.py`: Data loading, pivoting, returns calculation
- `correlation_analysis.py`: Correlation matrix, p-values, rolling correlations
- `hedge_recommendations.py`: Hedge ratios, portfolio allocation
- `visualize.py`: Heatmaps, rolling plots, effectiveness charts
- `generate_report.py`: Comprehensive markdown report

**Correlation Methods**: Pearson (linear), Spearman (rank-based), Kendall (concordance)

**Hedge Methods**: OLS regression (standard), Minimum variance (risk-minimizing)

**Interpretation**:
- Strong correlation: |r| > 0.7 (high co-movement)
- Moderate: 0.3 < |r| < 0.7 (partial relationship)
- Weak: |r| < 0.3 (minimal relationship)
- Negative correlation: r < -0.5 (good hedge potential)
