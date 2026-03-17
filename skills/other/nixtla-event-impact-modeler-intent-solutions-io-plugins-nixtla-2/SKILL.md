---
name: nixtla-event-impact-modeler
description: >
  Quantifies the impact of exogenous events on contract prices using TimeGPT and CausalImpact.
  Triggers on "event impact analysis", "model event effects", "quantify event impact", or "causal analysis".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep,WebSearch"
---

# Nixtla Event Impact Modeler

Quantifies the causal impact of exogenous events on contract prices using TimeGPT forecasting and CausalImpact analysis.

## Overview

This skill analyzes how external events (promotions, natural disasters, policy changes) affect contract prices over time. It combines historical price data with event details to quantify causal impacts using MCMC-based counterfactual modeling and TimeGPT forecasting. The skill produces impact estimates, adjusted forecasts, and visualizations for event-driven price changes.

**Use cases**: Promotion effectiveness analysis, disaster impact quantification, policy change assessment, pricing anomaly investigation, event-aware forecasting.

## Prerequisites

**Environment**:
- `NIXTLA_TIMEGPT_API_KEY` (required for TimeGPT forecasting)

**Dependencies**:
```bash
pip install nixtla pandas causalimpact matplotlib
```

**Input requirements**:
- `prices.csv`: Contract prices with columns `ds` (datetime), `price` (numeric)
- `events.csv`: Event data with columns `ds` (datetime), `event` (string description)

## Instructions

### Step 1: Prepare data

Load and validate contract price and event data using the data preparation script.

```bash
python {baseDir}/scripts/prepare_data.py \
  --prices prices.csv \
  --events events.csv \
  --output-prices prepared_prices.csv \
  --output-events prepared_events.csv
```

**To create sample data for testing**:
```bash
python {baseDir}/scripts/prepare_data.py --create-sample
```

**Script actions**:
- Loads CSV files with datetime parsing
- Validates required columns (`ds`, `price`/`event`)
- Renames columns to Nixtla standard (`y` for price)
- Adds default `unique_id` if missing
- Outputs prepared CSVs for analysis

### Step 2: Configure model

Define event windows and mark treatment/control periods in the price data.

```bash
python {baseDir}/scripts/configure_model.py \
  --prices prepared_prices.csv \
  --events prepared_events.csv \
  --window-days 3 \
  --output configured_prices.csv
```

**Script actions**:
- Defines event periods with configurable window (default: 3 days before/after)
- Validates event dates fall within price data range
- Creates `treatment` column (1=treatment period, 0=control period)
- Outputs configured DataFrame with treatment markers

**Parameters**:
- `--window-days`: Event window size in days (default: 3)

### Step 3: Execute analysis

Run CausalImpact analysis with TimeGPT forecasting to quantify event effects.

```bash
python {baseDir}/scripts/analyze_impact.py \
  --prices configured_prices.csv \
  --events prepared_events.csv \
  --niter 1000 \
  --window-days 3 \
  --output-impact impact_results.csv \
  --output-forecast adjusted_forecast.csv \
  --output-summary causal_summary.txt
```

**Script actions**:
- Defines pre-intervention and post-intervention periods
- Runs CausalImpact MCMC analysis (configurable iterations)
- Calculates absolute and relative event effects
- Generates TimeGPT adjusted forecasts
- Outputs impact metrics, forecasts, and summary report

**Parameters**:
- `--niter`: MCMC iterations for CausalImpact (default: 1000)
- `--window-days`: Event window size (must match Step 2)

### Step 4: Generate report

Create visualization and markdown report summarizing the analysis.

```bash
python {baseDir}/scripts/generate_report.py \
  --impact-results impact_results.csv \
  --adjusted-forecast adjusted_forecast.csv \
  --causal-summary causal_summary.txt \
  --output-plot impact_plot.png \
  --output-report impact_report.md \
  --title "Event Impact on Contract Prices"
```

**Script actions**:
- Generates time series plot with actual prices, forecasts, and treatment periods
- Creates markdown report with impact metrics, CausalImpact summary, and methodology
- Outputs high-resolution PNG and structured markdown report

## Output

**Generated files**:
- `impact_results.csv`: Event impact metrics (absolute effect, relative effect, average price)
- `adjusted_forecast.csv`: TimeGPT forecasts with actual prices and predictions
- `causal_summary.txt`: CausalImpact statistical summary
- `impact_plot.png`: Time series visualization with treatment periods highlighted
- `impact_report.md`: Comprehensive markdown report with all results

**Impact metrics**:
- Absolute effect: Total price change attributable to events
- Relative effect: Percentage change relative to mean price
- Counterfactual forecast: What prices would have been without events

## Error Handling

| Error | Solution |
|-------|----------|
| Event dates outside price range | Adjust event dates or expand price data range |
| Missing event descriptions | Ensure `event` column exists in events CSV |
| TimeGPT API request failed | Verify `NIXTLA_TIMEGPT_API_KEY` and internet connection |
| CausalImpact failed to converge | Increase `--niter` parameter or adjust event windows |
| Insufficient pre-intervention data | Expand price history before first event |

## Examples

### Example 1: Promotion impact analysis

**Scenario**: Quantify price increase during promotional campaign.

**Input**:
- `prices.csv`: Daily prices for 30 days
- `events.csv`: Single promotion event on day 15

**Command sequence**:
```bash
python scripts/prepare_data.py --prices prices.csv --events events.csv
python scripts/configure_model.py --prices prepared_prices.csv --events prepared_events.csv --window-days 5
python scripts/analyze_impact.py --prices configured_prices.csv --events prepared_events.csv --niter 2000
python scripts/generate_report.py --impact-results impact_results.csv --adjusted-forecast adjusted_forecast.csv
```

**Output**: `impact_results.csv` shows 15% relative price increase during promotion period.

### Example 2: Natural disaster impact

**Scenario**: Assess price drop following natural disaster.

**Input**:
- `prices.csv`: Weekly prices for 52 weeks
- `events.csv`: Disaster event on week 26

**Command sequence**:
```bash
python scripts/prepare_data.py --prices prices.csv --events events.csv
python scripts/configure_model.py --prices prepared_prices.csv --events prepared_events.csv --window-days 7
python scripts/analyze_impact.py --prices configured_prices.csv --events prepared_events.csv
python scripts/generate_report.py --impact-results impact_results.csv --adjusted-forecast adjusted_forecast.csv --title "Disaster Impact Analysis"
```

**Output**: `impact_report.md` documents price recovery timeline and total economic impact.

## Resources

**Scripts** (all in `{baseDir}/scripts/`):
- `prepare_data.py`: Data loading and validation with argparse CLI
- `configure_model.py`: Event period configuration and treatment/control marking
- `analyze_impact.py`: CausalImpact + TimeGPT analysis engine
- `generate_report.py`: Visualization and markdown report generation

**Documentation**:
- [Nixtla TimeGPT API](https://docs.nixtla.io/)
- [CausalImpact Python](https://github.com/jamalsenouci/causalimpact)
- [StatsForecast Documentation](https://nixtla.github.io/statsforecast/)
