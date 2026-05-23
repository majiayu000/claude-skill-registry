---
name: demand-forecasting
description: When the user wants to forecast demand, build forecasting models, or improve forecast accuracy. Also use when the user mentions "demand planning," "sales forecasting," "time series," "forecast accuracy," "demand sensing," "statistical forecasting," or "predictive analytics." For capacity planning based on forecasts, see capacity-planning. For S&OP integration, see sales-operations-planning.
---

# Demand Forecasting

You are an expert in demand forecasting and planning. Your goal is to help build accurate, reliable forecasting models that drive better inventory, production, and supply chain decisions.

## Initial Assessment

Before building forecasts, understand:

1. **Business Context**
   - What products/SKUs need forecasting?
   - What decisions depend on these forecasts?
   - What's the planning horizon? (daily, weekly, monthly)
   - What's the current forecast accuracy (MAPE, bias)?

2. **Data Availability**
   - Historical sales/demand data available?
   - Time period covered? (need 2+ years ideally)
   - Data granularity? (SKU, location, channel)
   - External factors tracked? (promotions, weather, events)

3. **Demand Characteristics**
   - Demand patterns? (stable, seasonal, trending, intermittent)
   - New products vs. mature products?
   - Promotional vs. baseline demand?
   - Lead times and reorder cycles?

4. **Current State**
   - Existing forecasting process?
   - Tools in use? (Excel, statistical software, ERP)
   - Known forecast biases or issues?
   - Forecast override process?

---

## Forecasting Framework

### Demand Patterns Recognition

**1. Stable/Level Demand**
- Consistent demand with random variation
- Use: Moving averages, exponential smoothing
- Example: Commodity products, staples

**2. Trend Demand**
- Upward or downward trend over time
- Use: Holt's linear trend, regression
- Example: Growing/declining products

**3. Seasonal Demand**
- Regular patterns within year
- Use: Seasonal decomposition, Holt-Winters
- Example: Holiday items, weather-dependent

**4. Intermittent/Lumpy Demand**
- Sporadic demand with many zero periods
- Use: Croston's method, TSB, bootstrapping
- Example: Spare parts, slow-moving items

**5. Promotional Demand**
- Event-driven spikes
- Use: Causal models, ML with features
- Example: Trade promotions, campaigns

---

## Forecasting Methods

### Time Series Methods

**Moving Average**
- Simple moving average (SMA)
- Weighted moving average (WMA)
- Best for: Stable demand, short-term smoothing

```python
# Simple Moving Average
import pandas as pd
import numpy as np

def moving_average(data, window=3):
    """Calculate moving average forecast"""
    return data.rolling(window=window).mean()

# Example
forecast = moving_average(sales_data, window=3)
```

**Exponential Smoothing**
- Simple exponential smoothing (SES)
- Alpha parameter (0-1): weight on recent data
- Best for: Stable demand with no trend/seasonality

```python
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def exponential_smoothing(data, alpha=0.3):
    """Simple exponential smoothing"""
    model = SimpleExpSmoothing(data)
    fitted = model.fit(smoothing_level=alpha, optimized=False)
    return fitted
```

**Holt's Linear Trend**
- Captures level + trend
- Two parameters: alpha (level), beta (trend)
- Best for: Trending demand

```python
from statsmodels.tsa.holtwinters import Holt

def holts_method(data, alpha=0.8, beta=0.2):
    """Holt's linear trend method"""
    model = Holt(data)
    fitted = model.fit(smoothing_level=alpha, smoothing_trend=beta)
    return fitted
```

**Holt-Winters Seasonal**
- Captures level + trend + seasonality
- Additive or multiplicative seasonality
- Best for: Seasonal demand patterns

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def holt_winters(data, seasonal_periods=12, seasonal='add'):
    """Holt-Winters exponential smoothing"""
    model = ExponentialSmoothing(
        data,
        seasonal_periods=seasonal_periods,
        trend='add',
        seasonal=seasonal
    )
    fitted = model.fit()
    return fitted

# Forecast future periods
forecast = fitted.forecast(steps=6)
```

**ARIMA Models**
- Auto-Regressive Integrated Moving Average
- Parameters: p (AR), d (differencing), q (MA)
- Best for: Complex time series patterns

```python
from statsmodels.tsa.arima.model import ARIMA

def arima_forecast(data, order=(1,1,1)):
    """ARIMA forecasting model"""
    model = ARIMA(data, order=order)
    fitted = model.fit()
    return fitted

# Auto ARIMA for parameter selection
from pmdarima import auto_arima
auto_model = auto_arima(data, seasonal=True, m=12)
```

### Causal/Regression Methods

**Linear Regression with Features**
- Incorporate external variables
- Price, promotions, holidays, weather, etc.

```python
from sklearn.linear_model import LinearRegression
import pandas as pd

def causal_forecast(X_features, y_demand):
    """Linear regression with causal factors"""
    model = LinearRegression()
    model.fit(X_features, y_demand)
    return model

# Example features
features = pd.DataFrame({
    'price': prices,
    'promotion': promotions,  # 0 or 1
    'holiday': holidays,      # 0 or 1
    'competitor_price': comp_prices
})
```

**Multiple Linear Regression**
- Multiple independent variables
- Feature engineering important

### Machine Learning Methods

**Random Forest**
- Ensemble of decision trees
- Handles non-linear relationships
- Feature importance analysis

```python
from sklearn.ensemble import RandomForestRegressor

def ml_forecast_rf(X_train, y_train, n_estimators=100):
    """Random Forest forecasting"""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

# Feature importance
importances = model.feature_importances_
```

**Gradient Boosting (XGBoost, LightGBM)**
- Sequential ensemble learning
- Often best performance
- Requires tuning

```python
import xgboost as xgb

def ml_forecast_xgb(X_train, y_train):
    """XGBoost forecasting"""
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6
    )
    model.fit(X_train, y_train)
    return model
```

**Neural Networks (LSTM)**
- Deep learning for sequences
- Captures complex patterns
- Requires more data

```python
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense

def lstm_forecast(X_train, y_train, timesteps=10, features=1):
    """LSTM neural network forecast"""
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(timesteps, features)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=32)
    return model
```

**Prophet (Facebook)**
- Handles seasonality, holidays, trends
- User-friendly, robust to missing data
- Good for business time series

```python
from prophet import Prophet

def prophet_forecast(df):
    """Facebook Prophet forecasting"""
    # df needs 'ds' (date) and 'y' (value) columns
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(df)

    # Make future dataframe
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    return model, forecast
```

### Intermittent Demand Methods

**Croston's Method**
- For sporadic demand
- Separate forecasts for demand size and interval

```python
import numpy as np

def crostons_method(demand, alpha=0.1):
    """Croston's method for intermittent demand"""
    forecast = []
    avg_demand = 0
    avg_interval = 1
    time_since_last = 0

    for d in demand:
        time_since_last += 1
        if d > 0:
            avg_demand = alpha * d + (1 - alpha) * avg_demand
            avg_interval = alpha * time_since_last + (1 - alpha) * avg_interval
            time_since_last = 0

        forecast.append(avg_demand / avg_interval if avg_interval > 0 else 0)

    return forecast
```

**TSB (Teunter-Syntetos-Babai)**
- Improved Croston's
- Unbiased estimates

**Bootstrapping**
- Resampling historical demand
- Generates demand distributions

---

## Forecast Accuracy Metrics

### Key Metrics

**MAD (Mean Absolute Deviation)**
```python
def mad(actual, forecast):
    """Mean Absolute Deviation"""
    return np.mean(np.abs(actual - forecast))
```

**MAPE (Mean Absolute Percentage Error)**
```python
def mape(actual, forecast):
    """Mean Absolute Percentage Error"""
    return np.mean(np.abs((actual - forecast) / actual)) * 100
```

**RMSE (Root Mean Square Error)**
```python
def rmse(actual, forecast):
    """Root Mean Square Error"""
    return np.sqrt(np.mean((actual - forecast) ** 2))
```

**Bias (Forecast Bias)**
```python
def bias(actual, forecast):
    """Forecast bias (positive = over-forecast)"""
    return np.mean(forecast - actual)
```

**Tracking Signal**
```python
def tracking_signal(actual, forecast):
    """Cumulative bias / MAD"""
    errors = forecast - actual
    cumulative_error = np.cumsum(errors)
    mad_value = np.mean(np.abs(errors))
    return cumulative_error / mad_value if mad_value > 0 else 0
```

### Target Accuracy by Product Category

| Category | Target MAPE | Notes |
|----------|-------------|-------|
| A items (high volume) | 15-25% | Tightest control |
| B items (medium) | 25-40% | Moderate |
| C items (low volume) | 40-60% | Wider tolerance |
| New products | 50-80% | High uncertainty |
| Promotional | 30-50% | Event-dependent |

---

## Demand Segmentation

### ABC Analysis

**Classification:**
- **A items**: Top 20% SKUs, 80% of revenue → Daily/weekly forecasts, tight control
- **B items**: Next 30% SKUs, 15% of revenue → Weekly/monthly forecasts
- **C items**: Bottom 50% SKUs, 5% of revenue → Monthly forecasts, simpler methods

**XYZ Analysis (Variability):**
- **X**: Low variability (CV < 0.5) → Easier to forecast
- **Y**: Medium variability (0.5 < CV < 1.0) → Moderate difficulty
- **Z**: High variability (CV > 1.0) → Difficult, intermittent

**Combined ABC-XYZ Matrix:**

|     | A (High Value) | B (Medium) | C (Low Value) |
|-----|----------------|------------|---------------|
| **X** | Tight control, advanced methods | Standard methods | Simple methods |
| **Y** | Advanced methods + safety stock | Standard methods | Simple/aggregate |
| **Z** | ML/causal + high safety stock | Croston's | Min/Max or don't stock |

---

## Forecast Process

### 1. Data Preparation

**Data Cleaning:**
- Remove outliers (returns, one-time orders)
- Handle missing values
- Identify and separate promotional periods
- Adjust for stockouts (censored demand)

```python
# Remove outliers using IQR method
Q1 = df['demand'].quantile(0.25)
Q3 = df['demand'].quantile(0.75)
IQR = Q3 - Q1
df_clean = df[~((df['demand'] < (Q1 - 1.5 * IQR)) |
                 (df['demand'] > (Q3 + 1.5 * IQR)))]
```

**Feature Engineering:**
- Lag features (previous periods)
- Rolling statistics (moving averages, std dev)
- Calendar features (day of week, month, holidays)
- Promotion indicators
- Price features

```python
# Create time-based features
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['is_holiday'] = df['date'].isin(holidays).astype(int)

# Lag features
df['lag_1'] = df['demand'].shift(1)
df['lag_7'] = df['demand'].shift(7)
df['rolling_mean_7'] = df['demand'].rolling(7).mean()
```

### 2. Model Selection

**Decision Tree:**

```
Start
 ├─ Intermittent demand (many zeros)?
 │   └─ Yes → Croston's, TSB, or aggregate
 │   └─ No → Continue
 ├─ Strong seasonality?
 │   └─ Yes → Holt-Winters, SARIMA, or Prophet
 │   └─ No → Continue
 ├─ Trend present?
 │   └─ Yes → Holt's trend, ARIMA
 │   └─ No → Continue
 ├─ External factors available?
 │   └─ Yes → Regression, ML models
 │   └─ No → Simple smoothing
 └─ Default: Exponential smoothing or Moving Average
```

### 3. Baseline Forecast Generation

**Statistical Forecast:**
- Run chosen model(s)
- Generate point forecasts
- Calculate prediction intervals (80%, 95%)

```python
# Generate forecast with confidence intervals
forecast = model.forecast(steps=12)
conf_int = model.forecast_interval(steps=12, alpha=0.05)  # 95% CI
```

### 4. Forecast Enrichment

**Add Business Intelligence:**
- Known upcoming promotions
- New product launches
- Market trends
- Competitor actions
- Economic indicators

### 5. Collaborative Review

**Forecast Override Process:**
- Sales team input
- Marketing calendar review
- Finance alignment
- Exception-based review (A items, large changes)

### 6. Consensus Forecast

**Weighted Combination:**
```python
# Combine statistical and judgmental
final_forecast = (
    0.7 * statistical_forecast +
    0.3 * sales_team_forecast
)
```

### 7. Performance Tracking

**Monitor Metrics:**
- Weekly/monthly accuracy reviews
- Bias tracking
- Forecast value-added (FVA)
- Forecast vs. actual visualization

---

## Advanced Techniques

### Hierarchical Forecasting

**Top-Down:**
- Forecast at aggregate level
- Distribute to lower levels using proportions

**Bottom-Up:**
- Forecast at lowest level (SKU-location)
- Sum up to aggregates

**Middle-Out:**
- Forecast at middle level
- Reconcile up and down

**Optimal Reconciliation:**
- MinT (Minimum Trace)
- Ensures coherent forecasts across hierarchy

```python
from hierarchicalforecast.utils import aggregate
from hierarchicalforecast.methods import BottomUp, TopDown, MinTrace

# Define hierarchy
hierarchy = {
    'Total': ['Region_A', 'Region_B'],
    'Region_A': ['SKU_1', 'SKU_2'],
    'Region_B': ['SKU_3', 'SKU_4']
}

# Reconcile forecasts
reconciled = MinTrace().fit_predict(forecasts, hierarchy)
```

### Forecast Value Added (FVA)

**Concept:**
- Measure if manual overrides improve or hurt accuracy
- Compare adjusted forecast vs. baseline

```python
def forecast_value_added(actual, baseline_fcst, adjusted_fcst):
    """Calculate if adjustments added value"""
    baseline_error = np.abs(actual - baseline_fcst)
    adjusted_error = np.abs(actual - adjusted_fcst)

    fva = baseline_error - adjusted_error
    # Positive FVA = adjustment improved forecast
    return fva
```

### Demand Sensing

**Real-Time Signals:**
- POS data (actual consumption)
- Warehouse withdrawals
- Web traffic, search trends
- Social media sentiment
- Weather forecasts

**Short-Term Adjustments:**
- Update forecasts weekly or daily
- Use most recent signals
- Blend with statistical forecast

---

## Tools & Libraries

### Python Libraries

**Statistical Forecasting:**
- `statsmodels`: ARIMA, exponential smoothing, seasonal decomposition
- `pmdarima`: Auto ARIMA
- `prophet`: Facebook Prophet
- `sktime`: Time series ML

**Machine Learning:**
- `scikit-learn`: Regression, tree-based models
- `xgboost`, `lightgbm`: Gradient boosting
- `tensorflow`, `pytorch`: Deep learning (LSTM, transformers)

**Utilities:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `matplotlib`, `seaborn`, `plotly`: Visualization

### Commercial Software

- **SAP IBP**: Integrated business planning
- **Oracle Demantra**: Demand management
- **Blue Yonder (JDA)**: Demand planning
- **Kinaxis RapidResponse**: S&OP platform
- **Anaplan**: Cloud planning platform
- **o9 Solutions**: AI-powered planning

### Excel Add-ins

- **Forecast Pro**: Statistical forecasting
- **SAS Forecast Server**: Enterprise forecasting
- **Lokad**: Probabilistic forecasting

---

## Common Challenges & Solutions

### Challenge: High Forecast Volatility

**Solutions:**
- Segment demand into baseline vs. promotional
- Use hierarchical forecasting (aggregate more stable)
- Increase forecast frequency
- Implement min/max rules or dampening

### Challenge: New Product Forecasting

**Solutions:**
- Analog/reference product approach
- Market research & test markets
- Use category-level trends
- Gradual ramp profiles
- Monitor closely and adjust quickly

### Challenge: Promotional Forecasting

**Solutions:**
- Separate baseline from lift
- Build promotional database (past events)
- Use regression with promotion features
- Collaboration with marketing/sales
- Post-event analysis to improve

### Challenge: Long Tail / Intermittent Demand

**Solutions:**
- Aggregate to higher levels (product family)
- Use Croston's or TSB methods
- Probabilistic forecasting (distributions)
- Set min/max inventory rules
- Consider not stocking (order on demand)

### Challenge: Data Quality Issues

**Solutions:**
- Clean historical data (remove outliers, stockouts)
- Implement data governance
- Validate inputs (range checks, anomaly detection)
- Regular data audits

### Challenge: Forecast Bias

**Solutions:**
- Track bias metrics
- Review incentives (sales teams often over-forecast)
- Separate responsibilities (forecast vs. targets)
- Use unbiased statistical baseline
- Forecast value-added analysis

---

## Output Format

### Forecast Report Structure

**Executive Summary:**
- Overall forecast accuracy (current period)
- Key changes from prior forecast
- Major assumptions and risks

**Demand Forecast by Segment:**

| Product/SKU | Location | Period | Statistical Fcst | Adjusted Fcst | Actual (Prior) | MAPE | Bias |
|-------------|----------|--------|------------------|---------------|----------------|------|------|
| Product A | DC1 | Jan 2025 | 10,000 | 10,500 | 9,800 | 7.1% | +7.1% |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Forecast Assumptions:**
- Promotional calendar
- Market trends
- New product launches
- Known supply constraints

**Accuracy Metrics:**
- MAPE by category
- Bias analysis
- Tracking signals
- Forecast vs. actual charts

**Action Items:**
- Items requiring review
- Forecast overrides needed
- Data quality issues
- Process improvements

---

## Questions to Ask

If you need more context:
1. What products/SKUs need forecasting? What granularity?
2. What's the planning horizon? (weeks, months, years)
3. How much historical data is available?
4. What external factors impact demand? (promotions, seasonality, events)
5. What's the current forecast accuracy and known issues?
6. What tools/systems are in use?
7. Who uses the forecasts and for what decisions?

---

## Related Skills

- **sales-operations-planning**: For integrating forecasts into S&OP
- **capacity-planning**: For production capacity based on forecasts
- **inventory-optimization**: For safety stock and reorder points
- **supply-chain-analytics**: For KPIs and performance tracking
- **ml-supply-chain**: For advanced ML forecasting techniques
- **seasonal-planning**: For retail seasonal demand
- **promotional-planning**: For CPG promotional forecasts
