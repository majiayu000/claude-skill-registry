---
name: nixtla-demo-generator
description: "Generate production-ready Jupyter notebooks showcasing Nixtla forecasting workflows for statsforecast, mlforecast, and TimeGPT. Use when creating demos, building examples, or showcasing forecasting capabilities. Trigger with 'generate demo notebook', 'create Jupyter demo', or 'build forecasting example'."
allowed-tools: "Write,Read,Glob,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Demo Generator

Generate interactive, production-ready Jupyter notebooks that showcase Nixtla forecasting workflows with complete data pipelines, model training, evaluation, and visualization.

## Overview

This skill creates high-quality demonstration notebooks:

- **Three library support**: StatsForecast, MLForecast, TimeGPT
- **Complete workflows**: Data loading, preprocessing, model training, forecasting, evaluation, visualization
- **Production patterns**: Best practices, error handling, performance optimization
- **Instant demos**: Ready for Nixtla CEO presentations, customer POCs, and documentation
- **Customizable templates**: Modify for specific use cases and datasets

## Prerequisites

**Required**:
- Python 3.8+
- Jupyter notebook (`pip install jupyter`)
- At least one Nixtla library:
  - `statsforecast` - Statistical models (ARIMA, ETS, etc.)
  - `mlforecast` - Machine learning models (LightGBM, XGBoost)
  - `nixtla` - TimeGPT API access

**Optional**:
- `NIXTLA_API_KEY`: For TimeGPT demos
- Sample datasets (M4, custom time series)

**Installation**:
```bash
pip install jupyter statsforecast mlforecast nixtla pandas matplotlib
```

## Instructions

### Step 1: Choose Library

Select which Nixtla library to demonstrate:
```bash
# Options: statsforecast, mlforecast, timegpt
export DEMO_LIBRARY=statsforecast
```

### Step 2: Generate Notebook

Run the generator script:
```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-daily \
    --output demo_statsforecast_m4.ipynb
```

### Step 3: Customize (Optional)

Edit the generated notebook to:
- Add custom datasets
- Modify model configurations
- Adjust visualizations
- Include domain-specific context

### Step 4: Execute Notebook

Run the generated notebook:
```bash
jupyter notebook demo_statsforecast_m4.ipynb
```

Or execute non-interactively:
```bash
jupyter nbconvert --to notebook --execute demo_statsforecast_m4.ipynb
```

### Step 5: Export Results

Export to various formats:
```bash
# HTML for sharing
jupyter nbconvert --to html demo_statsforecast_m4.ipynb

# PDF for presentations
jupyter nbconvert --to pdf demo_statsforecast_m4.ipynb

# Python script for automation
jupyter nbconvert --to python demo_statsforecast_m4.ipynb
```

## Output

- **[library]_demo.ipynb**: Complete Jupyter notebook with:
  - Introduction and setup
  - Data loading and exploration
  - Model configuration
  - Training and forecasting
  - Evaluation metrics (SMAPE, MASE, MAE)
  - Visualizations (forecasts, residuals, comparisons)
  - Next steps and resources

## Error Handling

1. **Error**: `ModuleNotFoundError: No module named 'statsforecast'`
   **Solution**: Install required library: `pip install statsforecast mlforecast nixtla`

2. **Error**: `NIXTLA_API_KEY not set` (TimeGPT demos)
   **Solution**: Export API key: `export NIXTLA_API_KEY=your_key` or skip TimeGPT demo

3. **Error**: `Dataset file not found`
   **Solution**: Use `--generate-sample-data` flag to create synthetic dataset

4. **Error**: `nbformat.validator.ValidationError`
   **Solution**: Check Jupyter version compatibility: `pip install --upgrade jupyter nbformat`

5. **Error**: `Kernel died while executing notebook`
   **Solution**: Reduce dataset size or increase memory allocation

## Examples

### Example 1: StatsForecast M4 Daily Demo

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-daily \
    --models AutoETS,AutoARIMA,SeasonalNaive \
    --horizon 14 \
    --output demo_statsforecast_m4_daily.ipynb
```

**Generated notebook includes**:
```python
# Import libraries
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive
import pandas as pd
import matplotlib.pyplot as plt

# Load M4 Daily data
df = pd.read_csv('m4_daily_sample.csv')
print(f"Loaded {len(df)} rows, {df['unique_id'].nunique()} series")

# Configure models
sf = StatsForecast(
    models=[AutoETS(), AutoARIMA(), SeasonalNaive(season_length=7)],
    freq='D',
    n_jobs=-1
)

# Generate forecasts
forecasts = sf.forecast(df=df, h=14)

# Evaluate
from statsforecast.utils import calculate_metrics
metrics = calculate_metrics(df, forecasts, metrics=['smape', 'mase'])
print(metrics)

# Visualize
sf.plot(df, forecasts)
plt.show()
```

### Example 2: MLForecast with Exogenous Features

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library mlforecast \
    --dataset retail-sales \
    --models LightGBM,XGBoost \
    --features lag,rolling_mean,date_features \
    --output demo_mlforecast_retail.ipynb
```

**Generated notebook features**:
- Lag features (1, 7, 14 days)
- Rolling statistics (mean, std, min, max)
- Date features (day of week, month, is_weekend)
- LightGBM and XGBoost model comparison
- Feature importance plots

### Example 3: TimeGPT API Demo

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library timegpt \
    --dataset custom \
    --api-key $NIXTLA_API_KEY \
    --horizon 30 \
    --confidence-levels 80,90,95 \
    --output demo_timegpt_api.ipynb
```

**Generated notebook demonstrates**:
- TimeGPT API client initialization
- Data upload and validation
- Forecast generation with confidence intervals
- Probabilistic forecasting
- Anomaly detection integration

### Example 4: Batch Generate All Three Libraries

```bash
for library in statsforecast mlforecast timegpt; do
    python {baseDir}/scripts/generate_demo_notebook.py \
        --library $library \
        --dataset m4-hourly \
        --output "demo_${library}_m4_hourly.ipynb"
done
```

### Example 5: Custom Template with Branding

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-weekly \
    --template {baseDir}/assets/templates/custom_branded_template.ipynb \
    --logo company_logo.png \
    --output demo_branded.ipynb
```

## Resources

- **StatsForecast Docs**: https://nixtla.github.io/statsforecast/
- **MLForecast Docs**: https://nixtla.github.io/mlforecast/
- **TimeGPT Docs**: https://docs.nixtla.io/
- **Jupyter Tutorial**: https://jupyter.org/try
- **M4 Competition**: https://github.com/Mcompetitions/M4-methods

**Related Skills**:
- `nixtla-timegpt-lab`: Interactive TimeGPT experimentation
- `nixtla-experiment-architect`: Multi-model experiment design
- `nixtla-schema-mapper`: Data transformation for Nixtla format

**Scripts**:
- `{baseDir}/scripts/generate_demo_notebook.py`: Main notebook generator
- `{baseDir}/assets/templates/statsforecast_template.ipynb`: StatsForecast base template
- `{baseDir}/assets/templates/mlforecast_template.ipynb`: MLForecast base template
- `{baseDir}/assets/templates/timegpt_template.ipynb`: TimeGPT base template
