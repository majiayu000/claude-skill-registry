---
name: time-series-analyst
description: Analyzes time-series data for patterns, trends, seasonality, and anomalies, with forecasting using statistical and machine learning methods.
license: MIT
---

# Time Series Analyst

This skill provides guidance for analyzing temporal data, identifying patterns, and building forecasting models.

## Core Competencies

- **Decomposition**: Trend, seasonality, residual analysis
- **Statistical Methods**: ARIMA, SARIMA, Exponential Smoothing
- **ML Methods**: Prophet, LSTM, Transformer-based models
- **Anomaly Detection**: Statistical and ML approaches

## Time Series Fundamentals

### Data Characteristics

Before analysis, assess:

| Property | Question | Impact |
|----------|----------|--------|
| Stationarity | Is mean/variance constant? | Method selection |
| Seasonality | Are there repeating patterns? | Model components |
| Trend | Is there long-term direction? | Differencing needs |
| Frequency | What's the sampling rate? | Aggregation choices |
| Missing values | Are there gaps? | Imputation needs |

### Stationarity Tests

```python
from statsmodels.tsa.stattools import adfuller, kpss

# Augmented Dickey-Fuller (null: non-stationary)
adf_result = adfuller(series)
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
# p < 0.05 suggests stationarity

# KPSS (null: stationary)
kpss_result = kpss(series, regression='c')
print(f"KPSS Statistic: {kpss_result[0]:.4f}")
print(f"p-value: {kpss_result[1]:.4f}")
# p > 0.05 suggests stationarity
```

### Making Series Stationary

```python
# Differencing for trend
diff_1 = series.diff().dropna()

# Seasonal differencing
seasonal_diff = series.diff(periods=12).dropna()  # Monthly seasonality

# Log transform for varying variance
log_series = np.log(series)

# Box-Cox for optimal transformation
from scipy.stats import boxcox
transformed, lambda_param = boxcox(series)
```

## Time Series Decomposition

### Classical Decomposition

```
Original = Trend + Seasonal + Residual  (Additive)
Original = Trend × Seasonal × Residual  (Multiplicative)
```

```python
from statsmodels.tsa.seasonal import seasonal_decompose, STL

# Classical decomposition
decomposition = seasonal_decompose(
    series,
    model='additive',  # or 'multiplicative'
    period=12
)

# STL (more robust)
stl = STL(series, period=12, robust=True)
result = stl.fit()

# Access components
trend = result.trend
seasonal = result.seasonal
residual = result.resid
```

### Visualization Pattern

```
┌────────────────────────────────────────┐
│ Original Series                        │ ← Raw data
├────────────────────────────────────────┤
│ Trend Component                        │ ← Long-term direction
├────────────────────────────────────────┤
│ Seasonal Component                     │ ← Repeating patterns
├────────────────────────────────────────┤
│ Residual Component                     │ ← Random noise
└────────────────────────────────────────┘
```

## Statistical Forecasting Methods

### ARIMA Model Selection

**ARIMA(p, d, q)**:
- p: Autoregressive order (ACF/PACF)
- d: Differencing order (stationarity)
- q: Moving average order (ACF)

```python
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

# Automatic selection
auto_model = auto_arima(
    series,
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Auto-detect differencing
    seasonal=False,
    information_criterion='aic',
    trace=True
)
print(auto_model.summary())

# Manual ARIMA
model = ARIMA(series, order=(2, 1, 2))
fitted = model.fit()
forecast = fitted.forecast(steps=30)
```

### SARIMA for Seasonal Data

**SARIMA(p, d, q)(P, D, Q, m)**:
- Lowercase: non-seasonal components
- Uppercase: seasonal components
- m: seasonal period

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(
    series,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),  # Monthly seasonality
    enforce_stationarity=False
)
fitted = model.fit()

# Forecast with confidence intervals
forecast = fitted.get_forecast(steps=24)
mean = forecast.predicted_mean
ci = forecast.conf_int(alpha=0.05)
```

### Exponential Smoothing

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Holt-Winters (trend + seasonality)
model = ExponentialSmoothing(
    series,
    trend='add',           # or 'mul', None
    seasonal='add',        # or 'mul', None
    seasonal_periods=12
)
fitted = model.fit()
forecast = fitted.forecast(24)
```

## ML-Based Forecasting

### Facebook Prophet

```python
from prophet import Prophet

# Prepare data (must have 'ds' and 'y' columns)
df = pd.DataFrame({'ds': dates, 'y': values})

# Basic model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

# Add custom seasonality
model.add_seasonality(
    name='monthly',
    period=30.5,
    fourier_order=5
)

# Add regressors
model.add_regressor('holiday_flag')
model.add_regressor('promotion')

model.fit(df)

# Forecast
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
```

### LSTM for Sequences

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Prepare sequences
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data, seq_length=60)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Build model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(60, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)
```

## Anomaly Detection

### Statistical Methods

```python
# Z-score method
def zscore_anomalies(series, threshold=3):
    mean, std = series.mean(), series.std()
    z_scores = (series - mean) / std
    return abs(z_scores) > threshold

# IQR method
def iqr_anomalies(series, multiplier=1.5):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (series < lower) | (series > upper)

# Rolling statistics
def rolling_anomalies(series, window=30, threshold=2):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    lower = rolling_mean - threshold * rolling_std
    upper = rolling_mean + threshold * rolling_std
    return (series < lower) | (series > upper)
```

### Isolation Forest

```python
from sklearn.ensemble import IsolationForest

# Feature engineering for time series
features = pd.DataFrame({
    'value': series,
    'hour': series.index.hour,
    'dayofweek': series.index.dayofweek,
    'rolling_mean': series.rolling(24).mean(),
    'rolling_std': series.rolling(24).std()
}).dropna()

model = IsolationForest(contamination=0.01, random_state=42)
anomalies = model.fit_predict(features)
# -1 = anomaly, 1 = normal
```

## Model Evaluation

### Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| MAE | mean(\|actual - pred\|) | Interpretable error |
| RMSE | sqrt(mean((actual - pred)²)) | Penalize large errors |
| MAPE | mean(\|actual - pred\| / actual) | Percentage error |
| SMAPE | Symmetric MAPE | Handles zeros better |

### Cross-Validation for Time Series

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

for train_idx, test_idx in tscv.split(series):
    train, test = series.iloc[train_idx], series.iloc[test_idx]
    # Fit on train, evaluate on test
```

### Backtesting Pattern

```
├──────────────────────────────────────────────────────▶ Time
│
│  ┌─────────────────┬─────┐
│  │     Train       │ Test│  Fold 1
│  └─────────────────┴─────┘
│  ┌───────────────────────┬─────┐
│  │        Train          │ Test│  Fold 2
│  └───────────────────────┴─────┘
│  ┌─────────────────────────────┬─────┐
│  │           Train             │ Test│  Fold 3
│  └─────────────────────────────┴─────┘
```

## References

- `references/arima-guide.md` - ARIMA model selection and diagnostics
- `references/prophet-tuning.md` - Prophet configuration and custom seasonality
- `references/anomaly-patterns.md` - Anomaly detection techniques and thresholds
