---
name: time-series-forecaster
description: |
  Time series forecasting with ARIMA, Prophet, LSTM, and statistical methods. Activates for "time series", "forecasting", "predict future", "trend analysis", "seasonality", "ARIMA", "Prophet", "sales forecast", "demand prediction", "stock prediction". Handles trend decomposition, seasonality detection, multivariate forecasting, and confidence intervals with SpecWeave increment integration.
---

# Time Series Forecaster

## Overview

Specialized forecasting pipelines for time-dependent data. Handles trend analysis, seasonality detection, and future predictions using statistical methods, machine learning, and deep learning approaches—all integrated with SpecWeave's increment workflow.

## Why Time Series is Different

**Standard ML assumptions violated**:
- ❌ Data is NOT independent (temporal correlation)
- ❌ Data is NOT identically distributed (trends, seasonality)
- ❌ Random train/test split is WRONG (breaks temporal order)

**Time series requirements**:
- ✅ Temporal order preserved
- ✅ No data leakage from future
- ✅ Stationarity checks
- ✅ Autocorrelation analysis
- ✅ Seasonality decomposition

## Forecasting Methods

### 1. Statistical Methods (Baseline)

**ARIMA (AutoRegressive Integrated Moving Average)**:
```python
from specweave import TimeSeriesForecaster

forecaster = TimeSeriesForecaster(
    method="arima",
    increment="0042"
)

# Automatic order selection (p, d, q)
forecaster.fit(train_data)

# Forecast next 30 periods
forecast = forecaster.predict(horizon=30)

# Generates:
# - Trend analysis
# - Seasonality decomposition
# - Autocorrelation plots (ACF, PACF)
# - Residual diagnostics
# - Forecast with confidence intervals
```

**Seasonal Decomposition**:
```python
# Decompose into trend + seasonal + residual
decomposition = forecaster.decompose(
    data=sales_data,
    model='multiplicative',  # Or 'additive'
    period=12  # Monthly seasonality
)

# Creates:
# - Trend component plot
# - Seasonal component plot
# - Residual component plot
# - Strength of trend/seasonality metrics
```

### 2. Prophet (Facebook)

**Best for**: Business time series (sales, website traffic, user growth)

```python
from specweave import ProphetForecaster

forecaster = ProphetForecaster(increment="0042")

# Prophet handles:
# - Multiple seasonality (daily, weekly, yearly)
# - Holidays and events
# - Missing data
# - Outliers

forecaster.fit(
    data=sales_data,
    holidays=us_holidays,  # Built-in holiday effects
    seasonality_mode='multiplicative'
)

forecast = forecaster.predict(horizon=90)

# Generates:
# - Trend + seasonality + holiday components
# - Change point detection
# - Uncertainty intervals
# - Cross-validation results
```

**Prophet with Custom Regressors**:
```python
# Add external variables (marketing spend, weather, etc.)
forecaster.add_regressor("marketing_spend")
forecaster.add_regressor("temperature")

# Prophet incorporates external factors into forecast
```

### 3. Deep Learning (LSTM/GRU)

**Best for**: Complex patterns, multivariate forecasting, non-linear relationships

```python
from specweave import LSTMForecaster

forecaster = LSTMForecaster(
    lookback_window=30,  # Use 30 past observations
    horizon=7,  # Predict 7 steps ahead
    increment="0042"
)

# Automatically handles:
# - Sequence creation
# - Train/val/test split (temporal)
# - Scaling
# - Early stopping

forecaster.fit(
    data=sensor_data,
    epochs=100,
    batch_size=32
)

forecast = forecaster.predict(horizon=7)

# Generates:
# - Training history plots
# - Validation metrics
# - Attention weights (if using attention)
# - Forecast uncertainty estimation
```

### 4. Multivariate Forecasting

**VAR (Vector AutoRegression)** - Multiple related time series:
```python
from specweave import VARForecaster

# Forecast multiple related series simultaneously
forecaster = VARForecaster(increment="0042")

# Example: Forecast sales across multiple stores
# Each store's sales affects others
forecaster.fit(data={
    'store_1_sales': store1_data,
    'store_2_sales': store2_data,
    'store_3_sales': store3_data
})

forecast = forecaster.predict(horizon=30)
# Returns forecasts for all 3 stores
```

## Time Series Best Practices

### 1. Temporal Train/Test Split

```python
# ❌ WRONG: Random split (data leakage!)
X_train, X_test = train_test_split(data, test_size=0.2)

# ✅ CORRECT: Temporal split
split_date = "2024-01-01"
train = data[data.index < split_date]
test = data[data.index >= split_date]

# Or use last N periods as test
train = data[:-30]  # All but last 30 observations
test = data[-30:]   # Last 30 observations
```

### 2. Stationarity Testing

```python
from specweave import TimeSeriesAnalyzer

analyzer = TimeSeriesAnalyzer(increment="0042")

# Check stationarity (required for ARIMA)
stationarity = analyzer.check_stationarity(data)

if not stationarity['is_stationary']:
    # Make stationary via differencing
    data_diff = analyzer.difference(data, order=1)
    
    # Or detrend
    data_detrended = analyzer.detrend(data)
```

**Stationarity Report**:
```markdown
# Stationarity Analysis

## ADF Test (Augmented Dickey-Fuller)
- Test Statistic: -2.15
- P-value: 0.23
- Critical Value (5%): -2.89
- Result: ❌ NON-STATIONARY (p > 0.05)

## Recommendation
Apply differencing (order=1) to remove trend.

After differencing:
- ADF Test Statistic: -5.42
- P-value: 0.0001
- Result: ✅ STATIONARY
```

### 3. Seasonality Detection

```python
# Automatic seasonality detection
seasonality = analyzer.detect_seasonality(data)

# Results:
# - Daily: False
# - Weekly: True (period=7)
# - Monthly: True (period=30)
# - Yearly: False
```

### 4. Cross-Validation for Time Series

```python
# Time series cross-validation (expanding window)
cv_results = forecaster.cross_validate(
    data=data,
    horizon=30,  # Forecast 30 steps ahead
    n_splits=5,  # 5 expanding windows
    metric='mape'
)

# Visualizes:
# - MAPE across different time periods
# - Forecast vs actual for each fold
# - Model stability over time
```

### 5. Handling Missing Data

```python
# Time series-specific imputation
forecaster.handle_missing(
    method='interpolate',  # Or 'forward_fill', 'backward_fill'
    limit=3  # Max consecutive missing values to fill
)

# For seasonal data
forecaster.handle_missing(
    method='seasonal_interpolate',
    period=12  # Use seasonal pattern to impute
)
```

## Common Time Series Patterns

### Pattern 1: Sales Forecasting

```python
from specweave import SalesForecastPipeline

pipeline = SalesForecastPipeline(increment="0042")

# Handles:
# - Weekly/monthly seasonality
# - Holiday effects
# - Marketing campaign impact
# - Trend changes

pipeline.fit(
    sales_data=daily_sales,
    holidays=us_holidays,
    regressors={
        'marketing_spend': marketing_data,
        'competitor_price': competitor_data
    }
)

forecast = pipeline.predict(horizon=90)  # 90 days ahead

# Generates:
# - Point forecast
# - Prediction intervals (80%, 95%)
# - Component analysis (trend, seasonality, regressors)
# - Anomaly flags for past data
```

### Pattern 2: Demand Forecasting

```python
from specweave import DemandForecastPipeline

# Inventory optimization, supply chain planning
pipeline = DemandForecastPipeline(
    aggregation='daily',  # Or 'weekly', 'monthly'
    increment="0042"
)

# Multi-product forecasting
forecasts = pipeline.fit_predict(
    products=['product_A', 'product_B', 'product_C'],
    horizon=30
)

# Generates:
# - Demand forecast per product
# - Confidence intervals
# - Stockout risk analysis
# - Reorder point recommendations
```

### Pattern 3: Stock Price Prediction

```python
from specweave import FinancialForecastPipeline

# Stock prices, crypto, forex
pipeline = FinancialForecastPipeline(increment="0042")

# Handles:
# - Volatility clustering
# - Non-linear patterns
# - Technical indicators

pipeline.fit(
    price_data=stock_prices,
    features=['volume', 'volatility', 'RSI', 'MACD']
)

forecast = pipeline.predict(horizon=7)

# Generates:
# - Price forecast with confidence bands
# - Volatility forecast (GARCH)
# - Trading signals (optional)
# - Risk metrics
```

### Pattern 4: Sensor Data / IoT

```python
from specweave import SensorForecastPipeline

# Temperature, humidity, machine metrics
pipeline = SensorForecastPipeline(
    method='lstm',  # Deep learning for complex patterns
    increment="0042"
)

# Multivariate: Multiple sensor readings
pipeline.fit(
    sensors={
        'temperature': temp_data,
        'humidity': humidity_data,
        'pressure': pressure_data
    }
)

forecast = pipeline.predict(horizon=24)  # 24 hours ahead

# Generates:
# - Multi-sensor forecasts
# - Anomaly detection (unexpected values)
# - Maintenance alerts
```

## Evaluation Metrics

**Time series-specific metrics**:

```python
from specweave import TimeSeriesEvaluator

evaluator = TimeSeriesEvaluator(increment="0042")

metrics = evaluator.evaluate(
    y_true=test_data,
    y_pred=forecast
)

# Metrics:
# - MAPE (Mean Absolute Percentage Error) - business-friendly
# - RMSE (Root Mean Squared Error) - penalizes large errors
# - MAE (Mean Absolute Error) - robust to outliers
# - MASE (Mean Absolute Scaled Error) - scale-independent
# - Directional Accuracy - did we predict up/down correctly?
```

**Evaluation Report**:
```markdown
# Time Series Forecast Evaluation

## Point Metrics
- MAPE: 8.2% (target: <10%) ✅
- RMSE: 124.5
- MAE: 98.3
- MASE: 0.85 (< 1 = better than naive forecast) ✅

## Directional Accuracy
- Correct direction: 73% (up/down predictions)

## Forecast Bias
- Mean Error: -5.2 (slight under-forecasting)
- Bias: -2.1%

## Confidence Intervals
- 80% interval coverage: 79.2% ✅
- 95% interval coverage: 94.1% ✅

## Recommendation
✅ DEPLOY: Model meets accuracy targets and is well-calibrated.
```

## Integration with SpecWeave

### Increment Structure

```
.specweave/increments/0042-sales-forecast/
├── spec.md (forecasting requirements, accuracy targets)
├── plan.md (forecasting strategy, method selection)
├── tasks.md
├── data/
│   ├── train_data.csv
│   ├── test_data.csv
│   └── schema.yaml
├── experiments/
│   ├── arima-baseline/
│   ├── prophet-holidays/
│   └── lstm-multivariate/
├── models/
│   ├── prophet_model.pkl
│   └── lstm_model.h5
├── forecasts/
│   ├── forecast_2024-01.csv
│   ├── forecast_2024-02.csv
│   └── forecast_with_intervals.csv
└── analysis/
    ├── stationarity_test.md
    ├── seasonality_decomposition.png
    └── forecast_evaluation.md
```

### Living Docs Integration

```bash
/sw:sync-docs update
```

Updates:
```markdown
<!-- .specweave/docs/internal/architecture/time-series-forecasting.md -->

## Sales Forecasting Model (Increment 0042)

### Method Selected: Prophet
- Reason: Handles multiple seasonality + holidays well
- Alternatives tried: ARIMA (MAPE 12%), LSTM (MAPE 10%)
- Prophet: MAPE 8.2% ✅ BEST

### Seasonality Detected
- Weekly: Strong (7-day cycle)
- Monthly: Moderate (30-day cycle)
- Yearly: Weak

### Holiday Effects
- Black Friday: +180% sales (strongest)
- Christmas: +120% sales
- Thanksgiving: +80% sales

### Forecast Horizon
- 90 days ahead
- Confidence intervals: 80%, 95%
- Update frequency: Weekly retraining

### Model Performance
- MAPE: 8.2% (target: <10%)
- Directional accuracy: 73%
- Deployed: 2024-01-15
```

## Commands

```bash
# Create time series forecast
/ml:forecast --horizon 30 --method prophet

# Evaluate forecast
/ml:evaluate-forecast 0042

# Decompose time series
/ml:decompose-timeseries 0042
```

## Advanced Features

### 1. Ensemble Forecasting

```python
# Combine multiple methods for robustness
ensemble = EnsembleForecast(increment="0042")

ensemble.add_forecaster("arima", weight=0.3)
ensemble.add_forecaster("prophet", weight=0.5)
ensemble.add_forecaster("lstm", weight=0.2)

# Weighted average of all forecasts
forecast = ensemble.predict(horizon=30)

# Ensemble typically 10-20% more accurate than single model
```

### 2. Forecast Reconciliation

```python
# For hierarchical time series (e.g., total sales = store1 + store2 + store3)
reconciler = ForecastReconciler(increment="0042")

# Ensures forecasts sum correctly
reconciled = reconciler.reconcile(
    forecasts={
        'total': total_forecast,
        'store1': store1_forecast,
        'store2': store2_forecast,
        'store3': store3_forecast
    },
    method='bottom_up'  # Or 'top_down', 'middle_out'
)
```

### 3. Forecast Monitoring

```python
# Track forecast accuracy over time
monitor = ForecastMonitor(increment="0042")

# Compare forecasts vs actuals
monitor.track_performance(
    forecasts=past_forecasts,
    actuals=actual_values
)

# Alerts when accuracy degrades
if monitor.accuracy_degraded():
    print("⚠️ Forecast accuracy dropped 15% - retrain model!")
```

## Summary

Time series forecasting requires specialized techniques:
- ✅ Temporal validation (no random split)
- ✅ Stationarity testing
- ✅ Seasonality detection
- ✅ Trend decomposition
- ✅ Cross-validation (expanding window)
- ✅ Confidence intervals
- ✅ Forecast monitoring

This skill handles all time series complexity within SpecWeave's increment workflow, ensuring forecasts are reproducible, documented, and production-ready.
