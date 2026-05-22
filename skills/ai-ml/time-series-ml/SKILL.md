---
name: time-series-ml
description: Build time series forecasting and anomaly detection with transformers and classical methods
---

# Time Series ML

## Method Selection

| Method | Data Size | Horizon | Seasonality | Multivariate | Training Time |
|--------|-----------|---------|-------------|--------------|---------------|
| **ARIMA/ETS** | <10K points | Short (1-30) | Manual config | No | Seconds |
| **Prophet** | 1K-1M points | Medium (30-365d) | Auto-detected | Limited | Seconds |
| **XGBoost/LightGBM** | Any | Any | Via features | Yes | Minutes |
| **PatchTST** | >10K points | Long (96-720) | Learned | Yes (channel-indep) | Hours |
| **TimesFM** | Any (zero-shot) | Any | Learned | Per-channel | None (pretrained) |
| **N-BEATS** | >5K points | Short-medium | Learned | No (univariate) | Hours |

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Quick baseline, <10K points | Prophet | Auto seasonality, interpretable, fast |
| Tabular features matter | XGBoost + temporal features | Handles mixed feature types well |
| Long horizon, enough data | PatchTST | SOTA on long-horizon benchmarks |
| No training data/budget | TimesFM (zero-shot) | Foundation model, no fine-tuning needed |
| Anomaly detection | Isolation Forest or Autoencoder | Unsupervised, no labeled anomalies needed |

## PatchTST Transformer Forecasting

```python
import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    """Split time series into patches (like ViT patches for images)."""
    def __init__(self, patch_len: int = 16, stride: int = 8, d_model: int = 128):
        super().__init__()
        self.patch_len = patch_len
        self.stride = stride
        self.proj = nn.Linear(patch_len, d_model)

    def forward(self, x):
        B, L, C = x.shape                            # (batch, seq_len, channels)
        x = x.unfold(dimension=1, size=self.patch_len, step=self.stride)
        x = x.permute(0, 3, 1, 2).reshape(B * C, -1, self.patch_len)
        return self.proj(x), C

class PatchTSTBlock(nn.Module):
    """Simplified PatchTST: patch embedding + transformer encoder."""
    def __init__(self, seq_len: int, pred_len: int, channels: int,
                 d_model: int = 128, n_heads: int = 8, n_layers: int = 3,
                 patch_len: int = 16, stride: int = 8, dropout: float = 0.1):
        super().__init__()
        self.pred_len = pred_len
        self.patch_emb = PatchEmbedding(patch_len, stride, d_model)
        num_patches = (seq_len - patch_len) // stride + 1
        self.pos_emb = nn.Parameter(torch.randn(1, num_patches, d_model))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=d_model * 4,
            dropout=dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.head = nn.Linear(d_model * num_patches, pred_len)

    def forward(self, x):
        B = x.shape[0]
        x, C = self.patch_emb(x)                     # (B*C, num_patches, d_model)
        x = self.encoder(x + self.pos_emb)
        x = self.head(x.flatten(start_dim=1))         # (B*C, pred_len)
        return x.reshape(B, C, self.pred_len).permute(0, 2, 1)
```

## Prophet Configuration

```python
from prophet import Prophet
import pandas as pd

def build_prophet(df: pd.DataFrame, country: str = "US") -> Prophet:
    """df must have columns: ds (datetime), y (target), plus any regressor columns."""
    m = Prophet(
        growth="linear",                              # "logistic" for saturating growth
        changepoint_prior_scale=0.05,                 # 0.01=rigid, 0.5=flexible
        seasonality_prior_scale=10.0,
        yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False,
    )
    m.add_country_holidays(country_name=country)
    m.add_seasonality(name="monthly", period=30.5, fourier_order=5)
    if "temperature" in df.columns:
        m.add_regressor("temperature", mode="additive")
    if "promo" in df.columns:
        m.add_regressor("promo", mode="multiplicative")
    m.fit(df)
    return m

def prophet_forecast(m: Prophet, periods: int = 90, freq: str = "D") -> pd.DataFrame:
    future = m.make_future_dataframe(periods=periods, freq=freq)
    forecast = m.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
```

## ARIMA/ETS with Statsmodels

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pmdarima as pm

def auto_arima_forecast(series: pd.Series, periods: int = 30) -> pd.DataFrame:
    model = pm.auto_arima(
        series, seasonal=True, m=7,                   # m=7 weekly, 12 monthly
        stepwise=True, suppress_warnings=True,
        max_p=5, max_q=5, max_P=2, max_Q=2,
    )
    forecast = model.predict(n_periods=periods, return_conf_int=True)
    return pd.DataFrame({"yhat": forecast[0], "lower": forecast[1][:, 0], "upper": forecast[1][:, 1]})

def ets_forecast(series: pd.Series, periods: int = 30, seasonal_periods: int = 7):
    """Holt-Winters exponential smoothing."""
    model = ExponentialSmoothing(
        series, trend="add", seasonal="add", seasonal_periods=seasonal_periods,
    ).fit(optimized=True)
    return model.forecast(periods)
```

## Anomaly Detection

```python
import numpy as np
from sklearn.ensemble import IsolationForest

def isolation_forest_anomalies(features: np.ndarray, contamination: float = 0.05) -> np.ndarray:
    """features: (n_samples, n_features) from temporal feature engineering. Returns bool mask."""
    clf = IsolationForest(contamination=contamination, n_estimators=200, random_state=42)
    return clf.fit_predict(features) == -1            # -1 = anomaly

class AutoencoderAnomalyDetector:
    """Reconstruction-error based anomaly detection."""
    def __init__(self, input_dim: int, latent_dim: int = 16, threshold_pct: float = 99.0):
        self.threshold_pct = threshold_pct
        self.threshold = None
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64), nn.ReLU(),
            nn.Linear(64, latent_dim), nn.ReLU(),     # Encoder
            nn.Linear(latent_dim, 64), nn.ReLU(),
            nn.Linear(64, input_dim),                  # Decoder
        )

    def fit(self, X_train: torch.Tensor, epochs: int = 100, lr: float = 1e-3):
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.model.train()
        for _ in range(epochs):
            recon = self.model(X_train)
            loss = nn.MSELoss()(recon, X_train)
            optimizer.zero_grad(); loss.backward(); optimizer.step()
        self.model.eval()
        with torch.no_grad():
            errors = ((self.model(X_train) - X_train) ** 2).mean(dim=1).numpy()
        self.threshold = np.percentile(errors, self.threshold_pct)

    def predict(self, X: torch.Tensor) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            errors = ((self.model(X) - X) ** 2).mean(dim=1).numpy()
        return errors > self.threshold
```

## Temporal Feature Engineering

```python
def create_temporal_features(df: pd.DataFrame, target: str = "y",
                             lags: list[int] = None, windows: list[int] = None) -> pd.DataFrame:
    if lags is None: lags = [1, 7, 14, 28]
    if windows is None: windows = [7, 14, 30]
    result = df.copy()
    # Lag features
    for lag in lags:
        result[f"lag_{lag}"] = result[target].shift(lag)
    # Rolling statistics (shift to avoid leakage)
    for w in windows:
        rolled = result[target].shift(1).rolling(w)
        result[f"roll_mean_{w}"] = rolled.mean()
        result[f"roll_std_{w}"] = rolled.std()
    # Calendar features
    dt = result.index if pd.api.types.is_datetime64_any_dtype(result.index) else pd.to_datetime(result["ds"])
    result["day_of_week"] = dt.dayofweek
    result["month"] = dt.month
    result["is_weekend"] = (dt.dayofweek >= 5).astype(int)
    # Fourier features for cyclical encoding
    for period, name in [(7, "weekly"), (365.25, "yearly")]:
        for k in range(1, 4):
            result[f"sin_{name}_{k}"] = np.sin(2 * np.pi * k * np.arange(len(dt)) / period)
            result[f"cos_{name}_{k}"] = np.cos(2 * np.pi * k * np.arange(len(dt)) / period)
    return result.dropna()
```

## Walk-Forward Cross-Validation

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def walk_forward_cv(series: np.ndarray, model_fn, train_size: int,
                    horizon: int, step: int = 1) -> dict:
    """model_fn: callable(train_data) -> callable(horizon) -> predictions"""
    errors = {"mae": [], "rmse": []}
    for start in range(train_size, len(series) - horizon, step):
        train, actual = series[:start], series[start:start + horizon]
        preds = model_fn(train)(horizon)
        errors["mae"].append(mean_absolute_error(actual, preds))
        errors["rmse"].append(np.sqrt(mean_squared_error(actual, preds)))
    return {
        "mae_mean": np.mean(errors["mae"]), "mae_std": np.std(errors["mae"]),
        "rmse_mean": np.mean(errors["rmse"]), "rmse_std": np.std(errors["rmse"]),
        "n_folds": len(errors["mae"]),
    }
```

## Gotchas

- **Data leakage in features**: Rolling features must use `.shift(1)` before `.rolling()`; without shift, current value leaks into its own features
- **Prophet on sub-daily data**: Set `daily_seasonality=True` and ensure `ds` has timezone info; naive timestamps cause silent offset errors
- **ARIMA stationarity**: Auto-ARIMA handles differencing, but extreme outliers before differencing distort estimation -- clip or transform first
- **PatchTST channel independence**: Each channel processed independently; cross-channel dependencies require explicit fusion layers
- **Fourier feature period mismatch**: Using `period=365` on hourly data (should be `365*24`) creates meaningless features -- match data frequency
- **Anomaly threshold drift**: Static thresholds degrade as distributions shift; recalibrate monthly or use adaptive percentile on rolling window
- **Walk-forward gap**: With delayed labels, add a gap between train/test windows to simulate real production delay
- **TimesFM context length**: Foundation models have fixed context windows; truncating history loses long-range patterns
