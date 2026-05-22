---
name: nixtla-batch-forecaster
description: "Forecast multiple time series in parallel using TimeGPT. Use when processing 10-100+ contracts efficiently. Trigger with 'batch forecast' or 'parallel forecasting'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Batch Forecaster

Process multiple time series forecasts in parallel with optimized throughput.

## Overview

Leverages TimeGPT API to generate forecasts for many time series concurrently. Features parallel batch processing with rate limiting, automatic fallback for failed batches, and optional portfolio-level aggregation. Produces individual forecasts per series plus combined outputs.

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla`, `pandas`, `tqdm` packages

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY`: Your TimeGPT API key

**Installation**:
```bash
pip install nixtla pandas tqdm
```

## Instructions

### Step 1: Prepare Input Data

Your CSV must have the Nixtla schema columns:

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | string | Series identifier (contract ID) |
| `ds` | datetime | Timestamp |
| `y` | numeric | Value to forecast |

Analyze your data:
```bash
python {baseDir}/scripts/prepare_data.py your_data.csv
```

### Step 2: Set API Key

```bash
export NIXTLA_TIMEGPT_API_KEY=your_api_key_here
```

### Step 3: Run Batch Forecast

Execute the batch forecasting engine:
```bash
python {baseDir}/scripts/batch_forecast.py your_data.csv --horizon 14 --freq D
```

**Available options**:
- `--horizon`: Forecast horizon (default: 14)
- `--freq`: Frequency D/H/W/M (default: D)
- `--batch-size`: Series per batch (default: 20)
- `--output-dir`: Output directory (default: forecasts)
- `--aggregate`: Create portfolio aggregation
- `--delay`: Rate limit delay in seconds (default: 1.0)

### Step 4: Generate Report

Create a summary report:
```bash
python {baseDir}/scripts/generate_report.py forecasts/
```

## Output

- **forecasts/all_forecasts.csv**: Combined forecasts for all series
- **forecasts/{series}_forecast.csv**: Individual series forecasts
- **forecasts/summary.json**: Processing metadata
- **forecasts/aggregated_forecast.csv**: Portfolio aggregation (if --aggregate)
- **forecasts/batch_report.md**: Human-readable summary

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `API Rate Limit Exceeded`
   **Solution**: Increase `--delay` or reduce `--batch-size`

3. **Error**: `Missing required columns`
   **Solution**: Ensure CSV has `unique_id`, `ds`, `y` columns

4. **Error**: `Batch failed, falling back to individual`
   **Solution**: Normal behavior - some series may have issues

## Examples

### Example 1: Forecast 50 Daily Contracts

```bash
python {baseDir}/scripts/batch_forecast.py contracts.csv \
    --horizon 14 \
    --freq D \
    --batch-size 10 \
    --output-dir forecasts/
```

**Output**:
```
Batch Forecast Complete
Series forecasted: 50/50
Success rate: 100.0%
```

### Example 2: Hourly Portfolio with Aggregation

```bash
python {baseDir}/scripts/batch_forecast.py portfolio.csv \
    --horizon 24 \
    --freq H \
    --aggregate \
    --output-dir portfolio_forecasts/
```

## Resources

- Scripts:
  - `{baseDir}/scripts/prepare_data.py` - Data validation and analysis
  - `{baseDir}/scripts/batch_forecast.py` - Main forecasting engine
  - `{baseDir}/scripts/generate_report.py` - Report generation
- Nixtla Docs: https://nixtla.github.io/
