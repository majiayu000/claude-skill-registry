---
name: data-science-tools
description: Documentation of available data science libraries (scipy, numpy, pandas, sklearn) and best practices for statistical analysis, regression modeling, and organizing analysis scripts. **CRITICAL:** All analysis scripts MUST be placed in reports/{topic}/scripts/, NOT in root scripts/ directory.
---

# Data Science Tools Skill

## Purpose

This skill documents the data science ecosystem available in this project, including:
- Which Python libraries are installed and available
- How to use them for statistical analysis and regression
- **WHERE to place analysis scripts** (reports/{topic}/scripts/ - NOT root scripts/)
- Best practices for reproducible data science

## 🚨 CRITICAL: Script Organization Rule

**ALL regression, modeling, and analysis scripts MUST go in:**
```
reports/{topic}_{timestamp}/scripts/
```

**NEVER in:**
```
scripts/  ❌ (root scripts/ is only for reusable utilities)
```

See [Script Organization Best Practices](#script-organization-best-practices) section below.

## Available Libraries

### Installed in `.venv` Virtual Environment

The following data science libraries are installed and ready to use:

| Library | Version | Purpose |
|---------|---------|---------|
| **numpy** | Latest | Numerical computing, arrays, linear algebra |
| **scipy** | 1.16.3+ | Scientific computing, optimization, statistics |
| **pandas** | 2.3.3+ | Data manipulation, DataFrames, time series |
| **scikit-learn** | 1.7.2+ | Machine learning, regression, clustering |

### Activating the Virtual Environment

**All Python scripts must use the virtual environment:**

```bash
source .venv/bin/activate && python scripts/your_script.py
```

Or add shebang to scripts:
```python
#!/usr/bin/env python3
# Then run directly: ./scripts/your_script.py
```

**In Bash tool calls:**
```bash
source .venv/bin/activate && python scripts/analysis.py
```

## Common Use Cases

### 1. Regression Modeling (scipy.optimize.curve_fit)

**Purpose:** Fit non-linear models to data (S-curves, exponential, etc.)

**Example: Logistic Regression**
```python
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Define model
def logistic(t, L, k, t0):
    """Logistic S-curve: L / (1 + exp(-k*(t - t0)))"""
    return L / (1 + np.exp(-k * (t - t0)))

# Prepare data
years = np.array([1993, 1994, ...])  # Time points
shares = np.array([0.004, 0.005, ...])  # Observed values
t = years - 1993  # Normalize time

# Fit model with bounds
p0 = [80, 0.5, 30]  # Initial guess: L=80%, k=0.5, t0=30
bounds = ([50, 0.1, 20], [100, 2.0, 50])  # Parameter bounds

params, covariance = curve_fit(
    logistic, t, shares,
    p0=p0,
    bounds=bounds,
    maxfev=10000
)

L, k, t0 = params

# Validate
predictions = logistic(t, L, k, t0)
r2 = r2_score(shares, predictions)
rmse = np.sqrt(np.mean((shares - predictions)**2))

print(f"Fitted parameters: L={L:.2f}, k={k:.4f}, t0={t0:.2f}")
print(f"R² = {r2:.6f}, RMSE = {rmse:.4f}")
```

**⚠️ Important:** Always use `curve_fit` with:
- Initial guess (`p0`)
- Bounds on parameters (prevents unrealistic values)
- `maxfev` to allow sufficient iterations

### 2. Model Comparison

**Compare multiple models to find best fit:**

```python
models = {
    'logistic': (logistic, [80, 0.5, 30], ([50, 0.1, 20], [100, 2.0, 50])),
    'gompertz': (gompertz, [80, 0.2, 30], ([50, 0.05, 20], [100, 1.0, 50])),
}

results = {}
for name, (func, p0, bounds) in models.items():
    params, _ = curve_fit(func, t, shares, p0=p0, bounds=bounds)
    pred = func(t, *params)
    r2 = r2_score(shares, pred)
    results[name] = {'params': params, 'r2': r2}

# Find best
best_model = max(results.items(), key=lambda x: x[1]['r2'])
print(f"Best model: {best_model[0]} (R² = {best_model[1]['r2']:.6f})")
```

### 3. Data Manipulation with Pandas

**Read CSV, filter, aggregate:**

```python
import pandas as pd

# Read data
df = pd.read_csv('data/ev_annual_bil10.csv')

# Filter
recent = df[df['year'] >= 2015]

# Aggregate
yearly_avg = df.groupby('year')['ev_share_pct'].mean()

# Export
df.to_csv('data/results.csv', index=False)
```

### 4. Statistical Analysis

```python
from scipy import stats

# Correlation
corr, p_value = stats.pearsonr(x, y)

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# T-test
t_stat, p_value = stats.ttest_ind(group1, group2)
```

## Script Organization Best Practices

### Directory Structure

```
dst_skills/
├── scripts/               # Reusable utilities ONLY
│   ├── fetch_and_store.py
│   ├── db/
│   │   └── helpers.py
│   └── utils.py
│
├── data/                 # Raw data and databases
│   ├── dst.db
│   └── *.csv
│
└── reports/              # Generated reports
    └── {topic}_{timestamp}/
        ├── report.html
        ├── visualizations.html
        ├── data/         # Report-specific intermediate data
        │   └── *.csv
        └── scripts/      # ⚠️ ALL analysis scripts go HERE
            ├── README.md
            ├── fit_models.py
            ├── validate.py
            └── requirements.txt
```

**IMPORTANT:** Do NOT create analysis scripts in root `scripts/` directory.
All regression, modeling, and analysis scripts must be in the report's `scripts/` folder.

### When to Place Scripts in `reports/{topic}/scripts/` ✅ ALWAYS for Analysis

**Use this for ALL report-specific analysis:**

1. **Regression modeling** (curve_fit, forecasting, etc.)
2. **Statistical analysis** (hypothesis tests, correlations, etc.)
3. **Data transformation** specific to this report
4. **Validation** and model comparison
5. **Reproducibility** - reader can re-run your exact analysis
6. **Documentation** - shows exactly what was done
7. **Versioning** - freezes code with report at time of publication

**✅ ALL of these belong in reports/{topic}/scripts/:**
- `fit_ev_models.py` - Regression modeling
- `validate_models.py` - Model validation
- `verify_regression_models.py` - scipy verification
- `forecast_scenarios.py` - Forecasting
- `statistical_tests.py` - Hypothesis testing

**Example structure:**
```
reports/elbiler_danmark_20251031/
├── report.html
├── visualizations.html
├── data/                    # Intermediate data for THIS analysis
│   ├── model_fits.csv
│   ├── forecasts.csv
│   └── residuals.csv
└── scripts/                 # ✅ ALL analysis scripts here
    ├── README.md           # Explains how to reproduce
    ├── fit_ev_models.py    # Main regression analysis
    ├── validate_models.py  # Cross-validation
    ├── verify_regression_models.py  # scipy verification
    └── requirements.txt    # Dependencies snapshot
```

### When to Use `scripts/` (Root Level) ⚠️ ONLY for Reusable Utilities

**Root scripts/ is ONLY for infrastructure utilities that are shared across ALL reports:**

1. **Database utilities** (`db/helpers.py`, `db/validate.py`)
2. **Data fetching** (`fetch_and_store.py`)
3. **Generic helpers** (`utils.py`)
4. **NOT for analysis** - no regression, modeling, or statistics

**❌ NEVER put these in root scripts/:**
- Regression models
- Statistical analysis
- Data transformations
- Forecasting
- Model validation

**✅ Root scripts/ should ONLY contain:**
```python
# scripts/db/helpers.py - OK (reusable DB utility)
def safe_numeric_cast(column_name):
    """Helper for casting DST suppressed values."""
    return f"CASE WHEN {column_name} != '..' THEN CAST({column_name} AS NUMERIC) ELSE NULL END"

# scripts/utils.py - OK (generic utility)
def format_timestamp():
    """Standard timestamp format for filenames."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

# scripts/fetch_and_store.py - OK (reusable infrastructure)
def fetch_dst_table(table_id, filters):
    """Fetch data from DST API and store in DuckDB."""
    # ... implementation
```

**If you're doing curve_fit, forecasting, or statistics → reports/{topic}/scripts/ ✅**

### Template: Report Analysis Script

```python
#!/usr/bin/env python3
"""
EV Adoption Model Fitting and Validation
=========================================

Report: Danmarks Elbilsudvikling 2050
Date: 2025-10-31
Author: Claude Code

Purpose:
    Fit multiple regression models to EV adoption data and compare.

Usage:
    cd reports/{report_name}/scripts/
    source ../../../.venv/bin/activate
    python fit_ev_models.py

Outputs:
    - ../data/model_parameters.csv
    - ../data/forecasts.csv
    - stdout: Model comparison table
"""

import sys
import os
import csv
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

def main():
    # 1. Load data using relative path from scripts/ directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../../..')

    # Path to project-level data
    data_path = os.path.join(project_root, 'data/ev_annual_bil10.csv')

    print(f"Loading data from {data_path}...")
    years = []
    shares = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            years.append(int(row['year']))
            shares.append(float(row['ev_share_pct']))

    years = np.array(years)
    shares = np.array(shares)

    # 2. Fit models
    print("\nFitting models...")
    # ... implementation

    # 3. Save results to report's data/ directory
    output_dir = os.path.join(script_dir, '../data')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'model_parameters.csv')
    print(f"\nSaving results to {output_path}...")
    # ... save implementation

if __name__ == '__main__':
    main()
```

**Key points:**
- Use `os.path` for cross-platform compatibility
- Always use relative paths from script's location
- Project data: `../../../data/`
- Report data: `../data/`
- Activate venv before running

### README.md Template for Report Scripts

```markdown
# Analysis Scripts for EV Adoption Report

## Report Details
- **Topic:** Danmarks Elbilsudvikling til 2050
- **Generated:** 2025-10-31
- **Data:** BIL10, BIL52, BIL51 (Danmarks Statistik)

## Reproducibility

### Prerequisites
```bash
# From project root
source .venv/bin/activate
pip install numpy scipy pandas scikit-learn
```

### Run Analysis
```bash
cd reports/elbiler_danmark_20251031/scripts/
python fit_ev_models.py
python validate_models.py
```

### Scripts
- `fit_ev_models.py` - Fits logistic, Gompertz, exponential models
- `validate_models.py` - Cross-validation and residual analysis
- `export_forecasts.py` - Generate 2026-2050 predictions

### Outputs
Results saved to `../data/`:
- `model_parameters.csv` - Fitted parameters (L, k, t0)
- `forecasts.csv` - Year-by-year predictions
- `validation_metrics.csv` - R², RMSE, etc.

## Model Details
See `../report.html` Section 3: Methodology
```

## Common Pitfalls and Solutions

### 1. ModuleNotFoundError

**Problem:**
```bash
ModuleNotFoundError: No module named 'scipy'
```

**Solution:**
```bash
# Always activate venv first
source .venv/bin/activate
python scripts/your_script.py
```

### 2. curve_fit Fails to Converge

**Problem:**
```
OptimizeWarning: Covariance of the parameters could not be estimated
```

**Solutions:**
- Improve initial guess `p0`
- Tighten bounds (e.g., L: [60, 90] instead of [50, 100])
- Increase `maxfev` to 20000
- Normalize/scale your data first
- Try different optimization methods

```python
# Better bounds
bounds = ([65, 0.3, 25], [95, 0.8, 40])  # Tighter

# Or use different method
from scipy.optimize import minimize, differential_evolution
```

### 3. Grid Search vs Optimization

**Bad (inefficient):**
```python
best_r2 = 0
for L in [70, 75, 80, 85, 90, 95]:
    for k in np.arange(0.1, 2.0, 0.05):
        # ... fit and compare
```

**Good (use scipy):**
```python
params, _ = curve_fit(logistic, t, shares, p0=[80, 0.5, 30])
```

**When grid search is acceptable:**
- Quick prototyping to find good `p0`
- Testing specific scenarios (e.g., compare L=70% vs L=90%)
- Educational purposes

### 4. Overfitting

**Warning signs:**
- R² > 0.999 on historical data
- Model fits noise, not signal
- Poor performance on holdout set

**Solutions:**
```python
# Train-test split
from sklearn.model_selection import train_test_split
train, test = train_test_split(data, test_size=0.2, shuffle=False)

# Fit on train, validate on test
params, _ = curve_fit(model, train_t, train_y)
test_pred = model(test_t, *params)
test_r2 = r2_score(test_y, test_pred)

if test_r2 < 0.9:
    print("⚠️ Warning: Poor generalization")
```

## Installation and Verification

### Check Installed Packages

```bash
source .venv/bin/activate
pip list | grep -E "(numpy|scipy|pandas|scikit)"
```

Expected output:
```
numpy          1.x.x
pandas         2.3.3
scikit-learn   1.7.2
scipy          1.16.3
```

### Verify scipy.optimize Works

```bash
source .venv/bin/activate
python -c "from scipy.optimize import curve_fit; print('✓ scipy.optimize available')"
```

### Install Missing Packages

```bash
source .venv/bin/activate
pip install numpy scipy pandas scikit-learn
```

## Integration with DST Skills Workflow

### Typical Workflow

1. **Discovery:** `/dst-discover` → Find tables
2. **Fetch:** `/dst-fetch` → Download data to `data/`
3. **Analysis:** `/dst-analyze` → SQL queries, basic calculations
4. **Modeling:** Create script in `reports/{topic}/scripts/` for regression
5. **Visualize:** `/dst-visualize` → Create charts from results
6. **Report:** `/dst-report` → Generate HTML with all findings

### Where Each Step Happens

| Step | Location | Examples |
|------|----------|----------|
| Data fetching | `data/` | dst.db, *.csv |
| SQL queries | Agent (ephemeral) | Aggregations, joins |
| Regression/modeling | `reports/{topic}/scripts/` ✅ | curve_fit, forecasting |
| Results | `reports/{topic}/data/` | model_parameters.csv |
| Report | `reports/{topic}/` | report.html |

### Example: Complete Regression Analysis

**Step 1: Create analysis script in report folder**

File: `reports/elbiler_danmark_20251031/scripts/fit_logistic_model.py`

```python
#!/usr/bin/env python3
"""
Fit logistic regression to EV adoption data.

Usage:
    cd reports/elbiler_danmark_20251031/scripts/
    source ../../../.venv/bin/activate
    python fit_logistic_model.py
"""

import csv
import os
import numpy as np
from scipy.optimize import curve_fit

def main():
    # Load data from project data/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../../..')
    data_path = os.path.join(project_root, 'data/ev_annual_bil10.csv')

    # 1. Load data
    years = []
    shares = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            years.append(int(row['year']))
            shares.append(float(row['ev_share_pct']))

    years = np.array(years)
    shares = np.array(shares)
    t = years - years.min()

    # 2. Define and fit model
    def logistic(t, L, k, t0):
        return L / (1 + np.exp(-k * (t - t0)))

    params, _ = curve_fit(logistic, t, shares,
                         p0=[80, 0.5, 30],
                         bounds=([50, 0.1, 20], [100, 2.0, 50]))
    L, k, t0 = params

    # 3. Forecast
    future_years = np.arange(years.max() + 1, 2051)
    future_t = future_years - years.min()
    forecast = logistic(future_t, L, k, t0)

    # 4. Export to report's data/ folder
    output_dir = os.path.join(script_dir, '../data')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'forecast.csv')
    with open(output_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['year', 'predicted_share'])
        for year, pred in zip(future_years, forecast):
            writer.writerow([year, pred])

    print(f"✓ Forecast exported: {output_path}")
    print(f"  Model: L={L:.1f}%, k={k:.3f}, t0={t0:.1f}")

if __name__ == '__main__':
    main()
```

**Step 2: Run from report's scripts/ directory**

```bash
cd reports/elbiler_danmark_20251031/scripts/
source ../../../.venv/bin/activate
python fit_logistic_model.py
```

**Step 3: Use results in visualization and report**

The forecast.csv is now in `reports/elbiler_danmark_20251031/data/` and can be used by `/dst-visualize` and `/dst-report`.

**✅ Benefits of this approach:**
- Script stays with report (reproducibility)
- Relative paths work from any machine
- Clear separation: data fetching vs analysis vs reporting
- Easy to version control and share

## References

### Documentation
- **scipy.optimize.curve_fit:** https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
- **sklearn metrics:** https://scikit-learn.org/stable/modules/model_evaluation.html
- **pandas:** https://pandas.pydata.org/docs/

### Regression Theory
- **Logistic growth:** Bass diffusion model, technology adoption
- **Gompertz curve:** Asymmetric S-curve for market saturation
- **Model selection:** AIC, BIC, cross-validation

### Best Practices
- **Script placement:** ALWAYS put analysis scripts in `reports/{topic}/scripts/`
- **Validation:** Use train-test split for model validation
- **Reporting:** Always report R², RMSE, and residual plots
- **Documentation:** Document assumptions and limitations in script docstrings
- **Reproducibility:** Version-control analysis scripts WITH the report they generate
- **Data paths:** Use relative paths with `os.path` for cross-platform compatibility
- **Virtual env:** Always activate `.venv` before running scipy/numpy code

### Quick Reference: Where Does It Go?

| What | Where | Example |
|------|-------|---------|
| **Regression scripts** | `reports/{topic}/scripts/` | `fit_models.py` |
| **Validation scripts** | `reports/{topic}/scripts/` | `verify_regression_models.py` |
| **Forecasting scripts** | `reports/{topic}/scripts/` | `forecast_scenarios.py` |
| **Statistical tests** | `reports/{topic}/scripts/` | `hypothesis_tests.py` |
| **Intermediate results** | `reports/{topic}/data/` | `model_parameters.csv` |
| **Raw data** | `data/` (project root) | `dst.db`, `ev_annual_bil10.csv` |
| **Reusable utilities** | `scripts/` (project root) | `db/helpers.py`, `fetch_and_store.py` |

**Simple rule:** If it uses scipy/curve_fit/statistics → `reports/{topic}/scripts/` ✅
