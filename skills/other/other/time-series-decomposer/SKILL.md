---
name: time-series-decomposer
description: Decompose time series into trend, seasonal, and residual components. Use for forecasting, pattern analysis, and seasonality detection.
---

# Time Series Decomposer

Extract trend, seasonal, and residual components from time series data with visualization and basic forecasting.

## Features

- **Decomposition**: Additive and multiplicative models
- **Trend Extraction**: Moving averages, polynomial fitting
- **Seasonality Detection**: Auto-detect and extract periodic patterns
- **Residual Analysis**: Identify anomalies in residuals
- **Visualization**: Component plots, ACF/PACF
- **Basic Forecasting**: Trend extrapolation, seasonal naive

## Quick Start

```python
from ts_decomposer import TimeSeriesDecomposer

decomposer = TimeSeriesDecomposer()
decomposer.load_csv("sales.csv", date_col="date", value_col="revenue")

# Decompose
result = decomposer.decompose(period=12)  # Monthly seasonality

print(f"Trend strength: {result['trend_strength']:.2f}")
print(f"Seasonal strength: {result['seasonal_strength']:.2f}")

# Plot components
decomposer.plot_components("decomposition.png")
```

## CLI Usage

```bash
# Basic decomposition
python ts_decomposer.py --input data.csv --date date --value sales --period 12

# Multiplicative model
python ts_decomposer.py --input data.csv --date date --value sales --period 12 --model multiplicative

# With forecast
python ts_decomposer.py --input data.csv --date date --value sales --period 12 --forecast 6

# Auto-detect period
python ts_decomposer.py --input data.csv --date date --value sales --auto-period

# Generate plots
python ts_decomposer.py --input data.csv --date date --value sales --period 12 --plot components.png

# Output JSON
python ts_decomposer.py --input data.csv --date date --value sales --period 12 --json
```

## API Reference

### TimeSeriesDecomposer Class

```python
class TimeSeriesDecomposer:
    def __init__(self)

    # Data loading
    def load_csv(self, filepath: str, date_col: str, value_col: str,
                date_format: str = None) -> 'TimeSeriesDecomposer'
    def load_series(self, series: pd.Series) -> 'TimeSeriesDecomposer'
    def load_dataframe(self, df: pd.DataFrame, date_col: str,
                      value_col: str) -> 'TimeSeriesDecomposer'

    # Decomposition
    def decompose(self, period: int = None, model: str = "additive") -> dict
    def detect_period(self) -> int
    def extract_trend(self, method: str = "moving_average",
                     window: int = None) -> pd.Series
    def extract_seasonal(self, period: int) -> pd.Series

    # Analysis
    def analyze_trend(self) -> dict
    def analyze_seasonality(self) -> dict
    def analyze_residuals(self) -> dict
    def detect_anomalies(self, threshold: float = 2.0) -> pd.DataFrame

    # Forecasting
    def forecast(self, periods: int, method: str = "trend") -> pd.DataFrame

    # Visualization
    def plot_components(self, output: str) -> str
    def plot_acf_pacf(self, output: str, lags: int = 40) -> str
    def plot_seasonal(self, output: str) -> str

    # Export
    def to_dataframe(self) -> pd.DataFrame
    def summary(self) -> str
```

## Decomposition Models

### Additive Model
Y(t) = Trend(t) + Seasonal(t) + Residual(t)

Best when seasonal variations are roughly constant.

```python
result = decomposer.decompose(period=12, model="additive")
```

### Multiplicative Model
Y(t) = Trend(t) * Seasonal(t) * Residual(t)

Best when seasonal variations scale with the level of the series.

```python
result = decomposer.decompose(period=12, model="multiplicative")
```

## Output Format

### Decomposition Result

```python
{
    "model": "additive",
    "period": 12,
    "trend_strength": 0.85,      # 0-1, higher = stronger trend
    "seasonal_strength": 0.72,   # 0-1, higher = stronger seasonality
    "components": {
        "observed": [...],       # Original values
        "trend": [...],          # Trend component
        "seasonal": [...],       # Seasonal component
        "residual": [...]        # Residual component
    },
    "seasonal_pattern": {        # Average seasonal effect by period
        1: 0.12,
        2: -0.05,
        ...
    },
    "statistics": {
        "trend_slope": 0.023,
        "trend_r_squared": 0.91,
        "residual_std": 0.15,
        "residual_mean": 0.002
    }
}
```

## Trend Analysis

```python
trend_info = decomposer.analyze_trend()

# Returns:
{
    "direction": "increasing",   # "increasing", "decreasing", "flat"
    "slope": 0.023,
    "r_squared": 0.91,
    "change_points": [           # Detected trend changes
        {"index": 24, "date": "2023-01-01", "direction": "up"},
        {"index": 48, "date": "2025-01-01", "direction": "down"}
    ],
    "growth_rate": 0.028,        # Compound growth rate
    "volatility": 0.12
}
```

## Seasonality Analysis

```python
seasonal_info = decomposer.analyze_seasonality()

# Returns:
{
    "detected_period": 12,
    "strength": 0.72,
    "pattern": {
        1: {"value": 0.12, "label": "Jan", "rank": 3},
        2: {"value": -0.05, "label": "Feb", "rank": 8},
        ...
    },
    "peak_period": 12,           # Period with highest seasonal effect
    "trough_period": 2,          # Period with lowest seasonal effect
    "seasonal_range": 0.35       # Max - Min seasonal effect
}
```

## Period Detection

Auto-detect the seasonal period:

```python
# Automatic detection using ACF
period = decomposer.detect_period()
print(f"Detected period: {period}")

# Or with decomposition
result = decomposer.decompose()  # Auto-detects period
```

## Anomaly Detection

Find outliers in residuals:

```python
anomalies = decomposer.detect_anomalies(threshold=2.0)

# Returns DataFrame with anomalous points:
#    date        value    residual    zscore    anomaly_type
# 0  2023-03-15  1250.5   450.2       3.2       high
# 1  2023-08-22  320.1    -380.5      -2.8      low
```

## Basic Forecasting

```python
# Trend extrapolation
forecast = decomposer.forecast(periods=12, method="trend")

# Seasonal naive (last season's values)
forecast = decomposer.forecast(periods=12, method="seasonal_naive")

# Trend + Seasonal
forecast = decomposer.forecast(periods=12, method="combined")

# Returns:
#    date        forecast    lower_bound    upper_bound
# 0  2024-01-01  1050.2      920.5          1180.0
# 1  2024-02-01  1080.5      945.2          1215.8
```

## Visualization

### Component Plot

```python
decomposer.plot_components("components.png")
```

Generates a 4-panel plot:
1. Original series
2. Trend
3. Seasonal
4. Residuals

### ACF/PACF Plot

```python
decomposer.plot_acf_pacf("acf_pacf.png", lags=40)
```

Autocorrelation and partial autocorrelation functions.

### Seasonal Plot

```python
decomposer.plot_seasonal("seasonal.png")
```

Bar chart of seasonal effects by period.

## Example Workflows

### Sales Analysis

```python
decomposer = TimeSeriesDecomposer()
decomposer.load_csv("monthly_sales.csv", "month", "revenue")

# Auto-detect and decompose
result = decomposer.decompose()

# Understand patterns
print(f"Trend: {decomposer.analyze_trend()['direction']}")
print(f"Peak season: Month {decomposer.analyze_seasonality()['peak_period']}")

# Plot
decomposer.plot_components("sales_analysis.png")
```

### Anomaly Detection

```python
decomposer = TimeSeriesDecomposer()
decomposer.load_csv("daily_metrics.csv", "date", "pageviews")
decomposer.decompose(period=7)  # Weekly pattern

# Find unusual days
anomalies = decomposer.detect_anomalies(threshold=2.5)
print(f"Found {len(anomalies)} anomalous days")
```

### Forecasting with Seasonality

```python
decomposer = TimeSeriesDecomposer()
decomposer.load_csv("quarterly_data.csv", "quarter", "value")
decomposer.decompose(period=4, model="multiplicative")

# Forecast next year
forecast = decomposer.forecast(periods=4, method="combined")
print(forecast)
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- scipy>=1.10.0
- statsmodels>=0.14.0
- matplotlib>=3.7.0
