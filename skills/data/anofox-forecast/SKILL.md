---
name: anofox-forecast
description: >
  Comprehensive reference for the Anofox Forecast DuckDB extension (v0.4.6).
  Use when working with ts_* or anofox_fcst_ts_* functions, time series
  forecasting in DuckDB, or the anofox_forecast extension. Provides API
  signatures, model selection, common workflows, and critical gotchas.
version: 0.4.6
user-invocable: false
---

# Anofox Forecast DuckDB Extension — Cheat Sheet

**Extension:** `anofox_forecast` v0.4.6 | **DuckDB:** v1.4.x+ | **Dual naming:** `ts_*` and `anofox_fcst_ts_*`

## Installation

```sql
LOAD anofox_forecast;
-- All functions available as ts_* and anofox_fcst_ts_* (identical)
```

---

## Critical Gotchas

1. **Seasonality is NOT auto-detected.** You must pass `seasonal_period` explicitly.
   Detect first with `ts_detect_periods_by`, then pass to forecasting.

2. **DO NOT chain `_by` table functions in CTEs.** Returns 0 rows silently under parallel execution.
   Always `CREATE TABLE` between pipeline steps:
   ```sql
   -- BROKEN (0 rows):
   WITH step1 AS (SELECT * FROM ts_fill_gaps_by(...))
   SELECT * FROM ts_fill_nulls_const_by('step1', ...);

   -- CORRECT:
   CREATE TABLE step1 AS SELECT * FROM ts_fill_gaps_by(...);
   SELECT * FROM ts_fill_nulls_const_by('step1', ...);
   ```

3. **Model names are case-sensitive.** `'AutoETS'` works, `'autoets'` errors.

4. **`ts_cv_forecast_by` requires pre-created folds.** Input table must have `fold_id` and `split` columns
   (from `ts_cv_folds_by` or `ts_cv_split_by`). Passing raw data throws a clear error.

5. **`ts_forecast_by` requires frequency as 7th positional parameter.** No default — you must specify it:
   ```sql
   -- WRONG: missing frequency
   SELECT * FROM ts_forecast_by('sales', id, date, val, 'Naive', 12);
   -- CORRECT:
   SELECT * FROM ts_forecast_by('sales', id, date, val, 'Naive', 12, '1d');
   ```

6. **Metric `_by` table macros are deprecated.** Use scalar functions with `GROUP BY`:
   ```sql
   -- Deprecated: SELECT * FROM ts_mae_by(...)
   -- Use instead:
   SELECT id, ts_mae(LIST(y ORDER BY ds), LIST(yhat ORDER BY ds)) AS mae
   FROM results GROUP BY id;
   ```

7. **Always use `ORDER BY` in `LIST()` for temporal correctness:**
   ```sql
   LIST(value ORDER BY date)  -- correct
   LIST(value)                -- wrong: order not guaranteed
   ```

---

## Three API Styles

### 1. Table Macros (primary — use these)
Operate on table names as strings. Handle grouping automatically.
```sql
SELECT * FROM ts_forecast_by('sales', product_id, date, revenue, 'AutoETS', 14, '1d',
    MAP{'seasonal_period': '7'});
```

### 2. Scalar Functions
Operate on arrays. Use with `LIST()` aggregation and `GROUP BY`.
```sql
SELECT product_id,
    ts_mae(LIST(actual ORDER BY date), LIST(forecast ORDER BY date)) AS mae
FROM results GROUP BY product_id;
```

### 3. Aggregate Functions
Return structs. Access fields with `(result).field_name`.
```sql
SELECT product_id, (ts_stats(LIST(value ORDER BY date))).*
FROM sales GROUP BY product_id;
```

---

## Parameter Syntax

### STRUCT (recommended)
```sql
MAP{'seasonal_period': '7'}
MAP{'seasonal_periods': '[7, 365]'}
MAP{'method': 'autoperiod', 'max_period': '28'}
```

All param values are strings (even numbers). Arrays use JSON syntax: `'[7, 365]'`.

### Frequency Strings
| Format | Examples |
|--------|---------|
| Polars style | `'1d'`, `'1h'`, `'30m'`, `'1w'`, `'1mo'`, `'1q'`, `'1y'` |
| DuckDB INTERVAL | `'1 day'`, `'1 hour'` |
| Raw integer | `'1'`, `'7'` (interpreted as days) |

---

## Common Workflows

### 1. Basic Forecast

```sql
-- Forecast 14 days ahead with weekly seasonality
SELECT * FROM ts_forecast_by(
    'sales', product_id, date, revenue,
    'HoltWinters', 14, '1d',
    MAP{'seasonal_period': '7'}
);
```

### 2. Data Preparation Pipeline (CREATE TABLE between steps!)

```sql
-- Step 1: Fill gaps
CREATE TABLE gaps_filled AS
SELECT * FROM ts_fill_gaps_by('raw_data', product_id, date, value, '1d');

-- Step 2: Impute NULLs
CREATE TABLE nulls_filled AS
SELECT * FROM ts_fill_nulls_const_by('gaps_filled', product_id, date, value, 0.0);

-- Step 3: Drop short series
CREATE TABLE clean_data AS
SELECT * FROM ts_drop_short_by('nulls_filled', product_id, 20);
```

### 3. Detect Seasonality → Forecast

```sql
-- Step 1: Detect
SELECT id, (periods).primary_period
FROM ts_detect_periods_by('sales', product_id, date, value, MAP{});
-- Returns e.g. primary_period = 7 (weekly)

-- Step 2: Forecast with detected period
SELECT * FROM ts_forecast_by(
    'sales', product_id, date, value,
    'AutoETS', 14, '1d', MAP{'seasonal_period': '7'}
);
```

### 4. Cross-Validation & Model Comparison

```sql
-- Step 1: Create folds
CREATE TABLE cv_folds AS
SELECT * FROM ts_cv_folds_by('data', unique_id, ds, y, 3, 12, MAP{});

-- Step 2: Forecast per fold (for each model)
CREATE TABLE cv_naive AS
SELECT * FROM ts_cv_forecast_by('cv_folds', unique_id, ds, y, 'Naive', MAP{});

CREATE TABLE cv_autoets AS
SELECT * FROM ts_cv_forecast_by('cv_folds', unique_id, ds, y, 'AutoETS',
    MAP{'seasonal_period': '7'});

-- Step 3: Compare metrics
SELECT 'Naive' AS model,
    ts_mae(LIST(y ORDER BY ds), LIST(yhat ORDER BY ds)) AS mae,
    ts_rmse(LIST(y ORDER BY ds), LIST(yhat ORDER BY ds)) AS rmse
FROM cv_naive GROUP BY ALL
UNION ALL
SELECT 'AutoETS',
    ts_mae(LIST(y ORDER BY ds), LIST(yhat ORDER BY ds)),
    ts_rmse(LIST(y ORDER BY ds), LIST(yhat ORDER BY ds))
FROM cv_autoets GROUP BY ALL;
```

### 5. Full Production Pipeline

```sql
-- 1. Quality check
SELECT id, (stats).length, (stats).n_nulls, (stats).n_gaps
FROM ts_stats_by('raw', product_id, date, value, '1d');

-- 2. Prep (materialize each step!)
CREATE TABLE step1 AS
SELECT * FROM ts_fill_gaps_by('raw', product_id, date, value, '1d');

CREATE TABLE step2 AS
SELECT * FROM ts_fill_nulls_const_by('step1', product_id, date, value, 0.0);

CREATE TABLE clean AS
SELECT * FROM ts_drop_short_by('step2', product_id, 20);

-- 3. Detect seasonality
SELECT id, (periods).primary_period
FROM ts_detect_periods_by('clean', product_id, date, value, MAP{});

-- 4. Backtest
CREATE TABLE cv_folds AS
SELECT * FROM ts_cv_folds_by('clean', product_id, date, value, 5, 14, MAP{});

CREATE TABLE backtest AS
SELECT * FROM ts_cv_forecast_by('cv_folds', product_id, date, value, 'AutoETS',
    MAP{'seasonal_period': '7'});

-- 5. Evaluate
SELECT product_id,
    ts_mae(LIST(y ORDER BY date), LIST(yhat ORDER BY date)) AS mae,
    ts_rmse(LIST(y ORDER BY date), LIST(yhat ORDER BY date)) AS rmse
FROM backtest GROUP BY product_id;

-- 6. Forecast
CREATE TABLE forecasts AS
SELECT * FROM ts_forecast_by('clean', product_id, date, value,
    'AutoETS', 14, '1d', MAP{'seasonal_period': '7'});

-- 7. Conformal intervals
CREATE TABLE calibration AS
SELECT * FROM ts_conformal_calibrate('backtest', value, yhat, {'alpha': 0.1});

SELECT * FROM ts_conformal_apply_by(
    'forecasts', product_id, yhat,
    (SELECT conformity_score FROM calibration)
);
```

---

## Model Quick Reference (32 Models)

### Automatic Selection (6)
| Model | Optional Params | Best For |
|-------|----------------|----------|
| `AutoETS` | `seasonal_period` | Unknown patterns (default pick) |
| `AutoARIMA` | `seasonal_period` | Unknown patterns, ARIMA family |
| `AutoTheta` | `seasonal_period` | Unknown patterns, Theta family |
| `AutoMFLES` | `seasonal_periods[]` | Multiple seasonalities |
| `AutoMSTL` | `seasonal_periods[]` | Multiple seasonalities |
| `AutoTBATS` | `seasonal_periods[]` | Multiple seasonalities |

### Basic (6)
| Model | Required | Optional | Best For |
|-------|----------|----------|----------|
| `Naive` | — | — | Baseline benchmark |
| `SMA` | — | `window` (def: 5) | Smoothed baseline |
| `SeasonalNaive` | **seasonal_period** | — | Seasonal baseline |
| `SES` | — | `alpha` (def: 0.3) | No trend, no seasonality |
| `SESOptimized` | — | — | Optimized SES |
| `RandomWalkDrift` | — | — | Trend without seasonality |

### Exponential Smoothing (4)
| Model | Required | Optional |
|-------|----------|----------|
| `Holt` | — | `alpha`, `beta` |
| `HoltWinters` | **seasonal_period** | `alpha`, `beta`, `gamma` |
| `SeasonalES` | **seasonal_period** | `alpha`, `gamma` |
| `SeasonalESOptimized` | **seasonal_period** | — |

### Theta Methods (5)
| Model | Optional |
|-------|----------|
| `Theta` | `seasonal_period`, `theta` |
| `OptimizedTheta` | `seasonal_period` |
| `DynamicTheta` | `seasonal_period`, `theta` |
| `DynamicOptimizedTheta` | `seasonal_period` |
| `AutoTheta` | `seasonal_period` |

### State Space & ARIMA (4)
| Model | Required | Optional |
|-------|----------|----------|
| `ETS` | — | `seasonal_period`, `model` |
| `AutoETS` | — | `seasonal_period` |
| `ARIMA` | **p**, **d**, **q** | `P`, `D`, `Q`, `s` |
| `AutoARIMA` | — | `seasonal_period` |

### Multiple Seasonality (6)
| Model | Required | Optional |
|-------|----------|----------|
| `MFLES` | **seasonal_periods[]** | `iterations` |
| `AutoMFLES` | — | `seasonal_periods[]` |
| `MSTL` | **seasonal_periods[]** | `stl_method` |
| `AutoMSTL` | — | `seasonal_periods[]` |
| `TBATS` | **seasonal_periods[]** | `use_box_cox` |
| `AutoTBATS` | — | `seasonal_periods[]` |

### Intermittent Demand (6)
| Model | Optional | Best For |
|-------|----------|----------|
| `CrostonClassic` | — | Sparse demand |
| `CrostonOptimized` | — | Sparse demand |
| `CrostonSBA` | — | Sparse demand (bias-corrected) |
| `ADIDA` | — | Aggregate-Disaggregate |
| `IMAPA` | — | Multiple aggregation |
| `TSB` | `alpha_d`, `alpha_p` | Best intermittent (tunable) |

---

## Model Selection Guide

| Data Characteristics | Recommended Models |
|---------------------|--------------------|
| No trend, no seasonality | `Naive`, `SES`, `SESOptimized` |
| Trend, no seasonality | `Holt`, `Theta`, `RandomWalkDrift` |
| Single seasonal period | `SeasonalNaive`, `HoltWinters`, `SeasonalES` |
| Multiple seasonalities | `MSTL`, `MFLES`, `TBATS` |
| Many zeros (intermittent) | `CrostonClassic`, `CrostonSBA`, `TSB` |
| Unknown characteristics | `AutoETS`, `AutoARIMA`, `AutoTheta` |
| Short series (< 20 pts) | `Naive`, `SES` |

| Scenario | First Try | Alternative |
|----------|-----------|-------------|
| Daily retail sales | `HoltWinters` | `MSTL` |
| Weekly financial data | `Theta` | `AutoETS` |
| Hourly sensor data | `MFLES` | `MSTL` |
| Spare parts demand | `CrostonSBA` | `TSB` |

---

## Function Quick Reference

### Forecasting
| Function | Purpose |
|----------|---------|
| `ts_forecast_by(table, group, date, value, method, horizon, frequency, params)` | Multi-series forecast |
| `ts_forecast_exog_by(table, group, date, value, x_cols, future_table, future_date, future_x, model, horizon, params, freq)` | Forecast with exogenous variables |

### Data Preparation
| Function | Purpose |
|----------|---------|
| `ts_fill_gaps_by(table, group, date, value, freq)` | Fill missing timestamps with NULL |
| `ts_fill_forward_by(table, group, date, value, target_date, freq)` | Extend series to target date |
| `ts_fill_nulls_const_by(table, group, date, value, fill_val)` | Replace NULLs with constant |
| `ts_fill_nulls_forward_by(table, group, date, value)` | Forward-fill NULLs |
| `ts_fill_nulls_backward_by(table, group, date, value)` | Backward-fill NULLs |
| `ts_fill_nulls_mean_by(table, group, date, value)` | Fill NULLs with mean |
| `ts_drop_constant_by(table, group, value)` | Remove constant series |
| `ts_drop_short_by(table, group, min_len)` | Remove short series |
| `ts_drop_gappy_by(table, group, value, max_gap_ratio)` | Remove gappy series |
| `ts_drop_zeros_by(table, group, value)` | Remove all-zero series |
| `ts_drop_leading_zeros_by(table, group, date, value)` | Trim leading zeros |
| `ts_drop_trailing_zeros_by(table, group, date, value)` | Trim trailing zeros |
| `ts_drop_edge_zeros_by(table, group, date, value)` | Trim both edges |
| `ts_diff_by(table, group, date, value, order)` | Compute differences |

### Statistics & Quality
| Function | Purpose |
|----------|---------|
| `ts_stats_by(table, group, date, value, freq)` | 36 statistics per series |
| `ts_data_quality_by(table, group, date, value, min_len, freq)` | Quality scores (0-1) |
| `ts_quality_report(stats_table, min_len)` | Summary quality report |
| `ts_stats_summary(stats_table)` | Summary across all series |

### Period Detection & Decomposition
| Function | Purpose |
|----------|---------|
| `ts_detect_periods_by(table, group, date, value, params)` | Detect seasonal periods |
| `ts_classify_seasonality_by(table, group, date, value, period)` | Classify seasonality type |
| `ts_mstl_decomposition_by(table, group, date, value, periods[], params)` | MSTL decomposition |
| `ts_detrend_by(table, group, date, value, method)` | Remove trend |
| `ts_detect_peaks_by(table, group, date, value, params)` | Detect peaks |
| `ts_analyze_peak_timing_by(table, group, date, value, period, params)` | Peak timing analysis |

### Cross-Validation
| Function | Purpose |
|----------|---------|
| `ts_cv_folds_by(table, group, date, value, n_folds, horizon, params)` | Create CV folds |
| `ts_cv_forecast_by(folds_table, group, date, value, method, params)` | Forecast on CV folds |
| `ts_cv_split_by(table, group, date, value, cutoff_dates[], horizon, params)` | Custom fold boundaries |
| `ts_cv_hydrate_by(folds, source, group, date, features[], params)` | Add features to folds |

### Evaluation Metrics (scalar — use with GROUP BY)
| Function | Signature | Description |
|----------|-----------|-------------|
| `ts_mae` | `(LIST, LIST) → DOUBLE` | Mean Absolute Error |
| `ts_mse` | `(LIST, LIST) → DOUBLE` | Mean Squared Error |
| `ts_rmse` | `(LIST, LIST) → DOUBLE` | Root Mean Squared Error |
| `ts_mape` | `(LIST, LIST) → DOUBLE` | Mean Absolute Percentage Error |
| `ts_smape` | `(LIST, LIST) → DOUBLE` | Symmetric MAPE |
| `ts_r2` | `(LIST, LIST) → DOUBLE` | R-squared |
| `ts_bias` | `(LIST, LIST) → DOUBLE` | Bias (mean error) |
| `ts_mase` | `(LIST, LIST, LIST) → DOUBLE` | Mean Absolute Scaled Error |
| `ts_rmae` | `(LIST, LIST, LIST) → DOUBLE` | Relative MAE |
| `ts_coverage` | `(LIST, LIST, LIST) → DOUBLE` | Interval coverage |
| `ts_quantile_loss` | `(LIST, LIST, DOUBLE) → DOUBLE` | Quantile loss |

### Conformal Prediction
| Function | Purpose |
|----------|---------|
| `ts_conformal_by(backtest, group, actual, forecast, point_forecast, params)` | One-step conformal intervals |
| `ts_conformal_calibrate(backtest, actual, forecast, params)` | Calibrate conformity score |
| `ts_conformal_apply_by(forecasts, group, forecast_col, score)` | Apply calibrated score |
| `ts_conformal_predict(residuals[], forecasts[], alpha)` | Array-based conformal |
| `ts_conformal_predict_asymmetric(residuals[], forecasts[], alpha)` | Asymmetric intervals |
| `ts_conformal_quantile(residuals[], alpha)` | Compute conformity quantile |
| `ts_conformal_intervals(forecasts[], score)` | Apply score to array |
| `ts_conformal_coverage(actuals[], lower[], upper[])` | Empirical coverage |
| `ts_conformal_evaluate(actuals[], lower[], upper[], alpha)` | Full evaluation |
| `ts_interval_width_by(table, group, lower, upper)` | Mean interval width |

### Feature Extraction
| Function | Purpose |
|----------|---------|
| `ts_features_by(table, group, date, value)` | Extract 117 tsfresh features |
| `ts_features_list()` | List available features |

### Hierarchical
| Function | Purpose |
|----------|---------|
| `ts_combine_keys((SELECT date, val, id1, id2, ...), params)` | Combine ID columns |
| `ts_aggregate_hierarchy((SELECT date, val, id1, id2, ...), params)` | Aggregate at all levels |
| `ts_split_keys((SELECT uid, date, val), ...)` | Split combined keys |
| `ts_validate_separator((SELECT id1, id2, ...), ...)` | Validate separator char |

### Changepoint Detection
| Function | Purpose |
|----------|---------|
| `ts_detect_changepoints_by(table, group, date, value, params)` | Detect structural breaks |

### Timestamp Validation
| Function | Purpose |
|----------|---------|
| `ts_validate_timestamps_by(table, group, date, expected_dates[])` | Validate timestamps exist |
| `ts_validate_timestamps_summary_by(table, group, date, expected_dates[])` | Validation summary |

### Future Value Handling
| Function | Purpose |
|----------|---------|
| `ts_fill_unknown_by(table, group, date, value, cutoff, params)` | Fill unknown future values |
| `ts_mark_unknown_by(table, group, date, cutoff)` | Mark known/unknown rows |

---

## Minimum Data Requirements

| Model Category | Minimum Observations |
|---------------|---------------------|
| Naive, SMA | 1+ |
| SES, Holt | 3+ |
| HoltWinters, SeasonalES | 2 × seasonal_period |
| MSTL, MFLES, TBATS | 2 × max(seasonal_periods) |
| AutoETS, AutoARIMA | 10+ (more is better) |
| Croston variants, TSB | 4+ |
| Cross-validation | horizon × n_folds + initial_train_size |

---

## Testing Queries

Verify generated SQL works against the actual extension:

```bash
bash .claude/skills/anofox-forecast/scripts/test-query.sh "SELECT * FROM ts_features_list() LIMIT 3"
```

Always test SQL before presenting it to the user. The script runs in-memory with the project's built extension.

---

## Deep-Dive References

For full function signatures, all parameters, return columns, and detailed examples:

- [Forecasting Models](references/forecasting-models.md) — All 32 models, exogenous support
- [Data Preparation](references/data-preparation.md) — Filtering, imputation, gap filling
- [Statistics & Quality](references/statistics-and-quality.md) — 36 stats, quality scores
- [Period Detection & Decomposition](references/period-detection-and-decomposition.md) — 12 detection methods, MSTL, detrending
- [Cross-Validation](references/cross-validation.md) — Folds, forecasting, hydration, custom splits
- [Evaluation Metrics](references/evaluation-metrics.md) — All 11 scalar metrics
- [Feature Extraction](references/feature-extraction.md) — 117 tsfresh features
- [Conformal Prediction](references/conformal-prediction.md) — Distribution-free intervals
- [Hierarchical](references/hierarchical.md) — Multi-key combine, aggregate, split
- [Changepoint Detection](references/changepoint-detection.md) — Structural break detection
