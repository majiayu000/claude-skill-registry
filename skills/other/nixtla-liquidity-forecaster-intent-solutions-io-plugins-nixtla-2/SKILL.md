---
name: nixtla-liquidity-forecaster
description: >
  Forecasts orderbook depth and spreads to optimize trade execution timing.
  Use when needing to estimate market liquidity for large orders.
  Trigger with "forecast liquidity", "predict orderbook", "estimate depth".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Liquidity Forecaster

Predicts future orderbook depth and bid-ask spreads using historical market data and TimeGPT.

## Overview

This skill analyzes historical trade data and orderbook snapshots from Polymarket to forecast liquidity conditions. It predicts near-term changes in orderbook depth and bid-ask spreads, helping determine optimal trade execution timing. The workflow fetches data via Polymarket API, preprocesses it for TimeGPT compatibility, and generates forecasts with visualizations and reports.

**When to use**: Determining optimal trade execution timing based on expected liquidity conditions, predicting orderbook depth changes, estimating bid-ask spread evolution.

**Trigger phrases**: "forecast liquidity", "predict orderbook depth", "estimate spread changes", "analyze market liquidity", "forecast trading conditions".

## Prerequisites

**Required environment variables**:
- `NIXTLA_TIMEGPT_API_KEY` - Your Nixtla TimeGPT API key

**Python packages**:
```bash
pip install nixtla pandas requests matplotlib
```

**Required tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Minimum Python version**: 3.8+

## Instructions

### Step 1: Fetch orderbook data

Fetch historical orderbook data from Polymarket API using the market ID. The script retrieves bids and asks, combines them into a single dataset, and saves to CSV format.

**Script**: `{baseDir}/scripts/fetch_data.py`

**Usage**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id <MARKET_ID> [--output orderbook_data.csv]
```

**Parameters**:
- `--market_id` (required): Polymarket market identifier
- `--output` (optional): Output CSV file path (default: orderbook_data.csv)

**Output**: Raw orderbook data CSV with columns: price, quantity, side

### Step 2: Preprocess data

Clean and format orderbook data for TimeGPT input. The script calculates mid-price, spread, and depth metrics, then formats the data according to Nixtla's schema requirements.

**Script**: `{baseDir}/scripts/preprocess_data.py`

**Usage**:
```bash
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv [--output preprocessed_data.csv]
```

**Parameters**:
- `--input_file` (required): Path to raw orderbook CSV from Step 1
- `--output` (optional): Output CSV file path (default: preprocessed_data.csv)

**Output**: Preprocessed data CSV with Nixtla format (unique_id, ds, y, spread, depth)

### Step 3: Execute forecast

Run TimeGPT forecast on preprocessed data. The script generates predictions for the specified horizon, creates visualizations, and produces a summary report.

**Script**: `{baseDir}/scripts/forecast_liquidity.py`

**Usage**:
```bash
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon <PERIODS> [--output depth_forecast.csv] [--plot_prefix depth]
```

**Parameters**:
- `--input_file` (required): Path to preprocessed CSV from Step 2
- `--horizon` (required): Number of periods to forecast
- `--output` (optional): Output forecast CSV path (default: depth_forecast.csv)
- `--plot_prefix` (optional): Prefix for plot filename (default: depth)

**Output**:
- Forecast CSV with predicted values
- PNG plot showing historical data and forecast
- Text report summarizing the forecasting process

### Step 4: Interpret results

Review the generated outputs to understand predicted liquidity conditions. The forecast CSV contains time-indexed predictions, the plot visualizes trends, and the report provides metadata about the forecasting run.

## Output

**Generated files**:
- `depth_forecast.csv` - Time-series predictions for orderbook depth and mid-price
- `depth_forecast.png` - Visualization showing historical data and forecast overlay
- `report.txt` - Summary report with market ID, horizon, and output file paths

**CSV format**: Columns include unique_id, ds (timestamp), y (predicted mid-price), and optional spread/depth metrics.

## Error Handling

**Invalid Polymarket Market ID**
*Cause*: Market ID not recognized by Polymarket API
*Solution*: Verify the market ID at https://polymarket.com or check API documentation

**TimeGPT API Key missing**
*Cause*: `NIXTLA_TIMEGPT_API_KEY` environment variable not set
*Solution*: Export your API key: `export NIXTLA_TIMEGPT_API_KEY=your_key_here`

**Insufficient data from Polymarket API**
*Cause*: Empty or incomplete orderbook data for the specified market
*Solution*: Check data availability for the market ID, try a different market, or verify API endpoint

**TimeGPT forecast failed**
*Cause*: Input data format issues or API connection problems
*Solution*: Verify preprocessed data has required columns (unique_id, ds, y), check API status, ensure data types are correct

**Missing required columns**
*Cause*: Raw orderbook data lacks price, quantity, or side columns
*Solution*: Verify Polymarket API response structure matches expected format, check for API changes

## Examples

### Example 1: Forecast depth for presidential election market

Predict orderbook depth 6 periods ahead for a political prediction market.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id trump_election_2024
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon 6
```

**Expected output**: `depth_forecast.csv` with 6 forecasted depth values, plot showing trend, summary report.

### Example 2: Forecast spread for cryptocurrency market

Predict bid-ask spread 24 periods ahead for an Ethereum price prediction market.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id eth_price_3000 --output eth_orderbook.csv
python {baseDir}/scripts/preprocess_data.py --input_file eth_orderbook.csv --output eth_preprocessed.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file eth_preprocessed.csv --horizon 24 --output eth_spread_forecast.csv --plot_prefix eth_spread
```

**Expected output**: `eth_spread_forecast.csv` with 24 forecasted values, plot named `eth_spread_forecast.png`, summary report.

### Example 3: Quick workflow for sports outcome market

End-to-end workflow for a sports prediction market using default file names.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id superbowl_winner_2025
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon 12
```

**Expected output**: Standard output files (depth_forecast.csv, depth_forecast.png, report.txt) with 12-period forecast.

## Resources

**Nixtla documentation**:
- TimeGPT API reference: https://docs.nixtla.io/
- Data format requirements: https://docs.nixtla.io/docs/tutorials-forecasting_with_timegpt

**Polymarket API**:
- API documentation: https://docs.polymarket.com/
- Market explorer: https://polymarket.com/markets

**Related skills**:
- `nixtla-timegpt-lab` - General TimeGPT forecasting workflows
- `nixtla-schema-mapper` - Data format transformation utilities
