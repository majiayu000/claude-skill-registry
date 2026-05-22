---
name: alphaear-predictor
description: Market prediction skill using Kronos. Use when user needs time-series forecasting or news-aware market adjustments.
---

# AlphaEar Predictor Skill

## Overview

This skill utilizes the Kronos model (via `KronosPredictorUtility`) to perform time-series forecasting and adjust predictions based on news sentiment.

## Capabilities

### 1. Forecast Market Trends

Use `scripts/kronos_predictor.py` to generate forecasts.

**Key Methods:**

-   `predict(ticker, horizon)`: Generate price forecast.
-   `adjust_forecast(original_forecast, news_sentiment)`: Adjust forecast based on recent news sentiment.

**Example Usage (Python):**

```python
from scripts.utils.kronos_predictor import KronosPredictorUtility
from scripts.utils.database_manager import DatabaseManager

db = DatabaseManager()
predictor = KronosPredictorUtility()

# Forecast
forecast = predictor.predict("600519", horizon="7d")
print(forecast)
```


## Configuration

This skill requires the **Kronos** model and an embedding model.

1.  **Kronos Model**:
    -   Ensure `exports/models` directory exists in the project root.
    -   Place trained news projector weights (e.g., `kronos_news_v1.pt`) in `exports/models/`.
    -   Or depend on the base model (automatically downloaded).

2.  **Environment Variables**:
    -   `EMBEDDING_MODEL`: Path or name of the embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`).
    -   `KRONOS_MODEL_PATH`: Optional path to override model loading.

## Dependencies

-   `torch`
-   `transformers`
-   `sentence-transformers`
-   `pandas`
-   `numpy`
-   `scikit-learn`
