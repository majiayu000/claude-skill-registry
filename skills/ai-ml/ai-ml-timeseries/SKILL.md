---
name: ai-ml-timeseries
description: "Operational patterns, templates, and decision rules for time series forecasting (modern best practices): tree-based methods (LightGBM), deep learning (Transformers, RNNs), future-guided learning, temporal validation, feature engineering, generative TS (Chronos), and production deployment. Emphasizes explainability, long-term dependency handling, and adaptive forecasting."
---

# Time Series Forecasting — Modern Patterns & Production Best Practices

**Modern Best Practices (December 2025)**:

- Treat **time** as a first-class axis: temporal splits, rolling backtests, and point-in-time correctness.
- Default to **strong baselines** (naive/seasonal naive) before complex models.
- Prevent leakage: feature windows and aggregations must use only information available at prediction time.
- Evaluate by **horizon** and **segment**; a single aggregate metric hides failures.
- Define retraining cadence and degraded modes (fallback model, last-known-good forecast).

This skill provides **operational, copy-paste-ready workflows** for forecasting with recent advances: TS-specific EDA, temporal validation, lag/rolling features, model selection, multi-step forecasting, backtesting, generative AI (Chronos, TimesFM), and production deployment with drift monitoring.

It focuses on **hands-on forecasting execution**, not theory.

---

## When to Use This Skill

Claude should invoke this skill when the user asks for **hands-on time series forecasting**, e.g.:

- "Build a time series model for X."
- "Create lag features / rolling windows."
- "Help design a forecasting backtest."
- "Pick the right forecasting model for my data."
- "Fix leakage in forecasting."
- "Evaluate multi-horizon forecasts."
- "Use LLMs or generative models for TS."
- "Set up monitoring for a forecast system."
- "Implement LightGBM for time series."
- "Use transformer models (TimesFM, Chronos) for forecasting."
- "Apply temporal classification/survival modelling for event prediction."

If the user is asking about **general ML modelling, deployment, or infrastructure**, prefer:

- [ai-ml-data-science](../ai-ml-data-science/SKILL.md) - General data science workflows, EDA, feature engineering, evaluation
- [ai-mlops](../ai-mlops/SKILL.md) - Model deployment, monitoring, drift detection, retraining automation
- [ai-mlops](../ai-mlops/SKILL.md) - Security, privacy, governance for ML systems

If the user is asking about **LLM/RAG/search**, prefer:

- [ai-llm](../ai-llm/SKILL.md) - LLM fine-tuning, prompting, evaluation
- [ai-rag](../ai-rag/SKILL.md) - RAG pipeline design and optimization
- [ai-rag](../ai-rag/SKILL.md) - Search and retrieval systems

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| TS EDA & Decomposition | Pandas, statsmodels | `seasonal_decompose()`, `df.plot()` | Identifying trend, seasonality, outliers |
| Lag/Rolling Features | Pandas, NumPy | `df.shift()`, `df.rolling()` | Creating temporal features for ML models |
| Model Training (Tree-based) | LightGBM, XGBoost | `lgb.train()`, `xgb.train()` | Tabular TS with seasonality, covariates |
| Deep Learning (Sequence models) | Transformers, RNNs | `model.forecast()` | Long-term dependencies, complex patterns |
| Event forecasting | Binary/time-to-event models | Temporal labeling + rolling validation | Sparse events and alerts |
| Backtesting | Custom rolling windows | `for window in windows: train(), test()` | Temporal validation without leakage |
| Metrics Evaluation | scikit-learn, custom | `mean_absolute_error()`, MAPE, MASE | Multi-horizon forecast accuracy |
| Production Deployment | MLflow, Airflow | Scheduled pipelines | Automated retraining, drift monitoring |

---

## Decision Tree: Choosing Time Series Approach

```text
User needs time series forecasting for: [Data Type]
    ├─ Strong Seasonality?
    │   ├─ Simple patterns? → LightGBM with seasonal features
    │   ├─ Complex patterns? → LightGBM + Prophet comparison
    │   └─ Multiple seasonalities? → Prophet or TBATS
    │
    ├─ Long-term Dependencies (>50 steps)?
    │   ├─ Transformers (TimesFM, Chronos) → Best for complex patterns
    │   └─ RNNs/LSTMs → Good for sequential dependencies
    │
    ├─ Event Forecasting (binary outcomes)?
    │   └─ Temporal classification / survival modelling → validate with time-based splits
    │
    ├─ Intermittent/Sparse Data (many zeros)?
    │   ├─ Croston/SBA → Classical intermittent methods
    │   └─ LightGBM with zero-inflation features → Modern approach
    │
    ├─ Multiple Covariates?
    │   ├─ LightGBM → Best with many features
    │   └─ TFT/DeepAR → If deep learning needed
    │
    └─ Explainability Required (healthcare, finance)?
        ├─ LightGBM → SHAP values, feature importance
        └─ Linear models → Most interpretable
```

---

## Core Concepts (Vendor-Agnostic)

- **Time axis**: splits, features, and labels must respect time ordering and availability.
- **Non-stationarity**: seasonality, trend, and regime shifts are normal; monitor and retrain intentionally.
- **Evaluation**: rolling/expanding backtests; report horizon-wise and segment-wise performance.
- **Operationalization**: define retraining cadence, fallback models, and data freshness contracts.
- **Data governance**: treat time series as potentially sensitive; enforce access control, retention, and PII scrubbing in logs.

## Implementation Practices (Tooling Examples)

- Build features with explicit time windows; store cutoff timestamps with each training run.
- Backtest with a standardized harness (rolling/expanding windows, horizon-wise metrics).
- Log production forecasts with metadata (model version, horizon, data cut) to enable debugging.
- Implement fallbacks (baseline model, last-known-good, “insufficient data” handling) for outages and anomalies.

## Do / Avoid

**Do**
- Do start with naive/seasonal naive baselines and compare against learned models (Forecasting: Principles and Practice: https://otexts.com/fpp3/).
- Do backtest with rolling windows and preserve point-in-time correctness.
- Do monitor for data pipeline changes (missing timestamps, level shifts, calendar changes).

**Avoid**
- Avoid random splits for forecasting problems.
- Avoid features that use future information (future aggregates, leakage via target encoding).
- Avoid optimizing only aggregate metrics; always inspect horizon-wise errors and worst segments.

## Navigation: Core Patterns

### Time Series EDA & Data Preparation

- **[TS EDA Best Practices](resources/ts-eda-best-practices.md)**
  - Frequency detection, missing timestamps, decomposition
  - Outlier detection, level shifts, seasonality analysis
  - Granularity selection and stability checks

### Feature Engineering

- **[Lag & Rolling Patterns](resources/lag-rolling-patterns.md)**
  - Lag features (lag_1, lag_7, lag_28 for daily data)
  - Rolling windows (mean, std, min, max, EWM)
  - Avoiding leakage, seasonal lags, datetime features

### Model Selection

- **[Model Selection Guide](resources/model-selection-guide.md)**
  - Decision rules: Strong seasonality → LightGBM, Long-term → Transformers
  - Benchmark comparison: LightGBM vs Prophet vs Transformers vs RNNs
  - Explainability considerations for mission-critical domains

- **[LightGBM TS Patterns](resources/lightgbm-ts-patterns.md)** *(2024-2025 best practices)*
  - Why LightGBM excels: performance + efficiency + explainability
  - Feature engineering for tree-based models
  - Hyperparameter tuning for time series

### Forecasting Strategies

- **[Multi-Step Forecasting Patterns](resources/multistep-forecasting-patterns.md)**
  - Direct strategy (separate models per horizon)
  - Recursive strategy (feed predictions back)
  - Seq2Seq strategy (Transformers, RNNs for long horizons)

- **[Intermittent Demand Patterns](resources/intermittent-demand-patterns.md)**
  - Croston, SBA, ADIDA for sparse data
  - LightGBM with zero-inflation features (modern approach)
  - Two-stage hurdle models, hierarchical Bayesian

### Validation & Evaluation

- **[Backtesting Patterns](resources/backtesting-patterns.md)**
  - Rolling window backtest, expanding window
  - Temporal train/validation split (no IID splits!)
  - Horizon-wise metrics, segment-level evaluation

### Generative & Advanced Models

- **[TS-LLM Patterns](resources/ts-llm-patterns.md)**
  - Chronos, TimesFM, Lag-Llama (Transformer models)
  - Event forecasting patterns (temporal classification, survival modelling)
  - Tokenization, discretization, trajectory sampling

### Production Deployment

- **[Production Deployment Patterns](resources/production-deployment-patterns.md)**
  - Feature pipelines (same code for train/serve)
  - Retraining strategies (time-based, drift-triggered)
  - Monitoring (error drift, feature drift, volume drift)
  - Fallback strategies, streaming ingestion, data governance

---

## Navigation: Templates (Copy-Paste Ready)

### Data Preparation

- **[TS EDA Template](templates/timeseries/template-ts-eda.md)** - Reproducible structure for time series analysis
- **[Resample & Fill Template](templates/timeseries/template-resample-fill.md)** - Handle missing timestamps and resampling

### Feature Templates

- **[Lag & Rolling Features](templates/timeseries/template-lag-rolling.md)** - Create temporal features for ML models
- **[Calendar Features](templates/timeseries/template-calendar-features.md)** - Business calendars, holidays, events

### Model Templates

- **[Forecast Model Template](templates/timeseries/template-forecast-model.md)** - End-to-end forecasting pipeline (LightGBM, transformers, RNNs)
- **[Multi-Step Strategy](templates/timeseries/template-multistep-strategy.md)** - Direct, recursive, and seq2seq approaches

### Evaluation Templates

- **[Backtest Template](templates/timeseries/template-backtest.md)** - Rolling window validation setup
- **[TS Metrics Template](templates/timeseries/template-ts-metrics.md)** - MAPE, MAE, RMSE, MASE, pinball loss

### Advanced Templates

- **[TS-LLM Template](templates/timeseries/template-ts-llm.md)** - Time series foundation model patterns and experimental approaches

---

## Related Skills

For adjacent topics, reference these skills:

- **[ai-ml-data-science](../ai-ml-data-science/SKILL.md)** - EDA workflows, feature engineering patterns, model evaluation, SQLMesh transformations
- **[ai-mlops](../ai-mlops/SKILL.md)** - Production deployment, monitoring, retraining pipelines
- **[ai-llm](../ai-llm/SKILL.md)** - Fine-tuning approaches applicable to time series LLMs (Chronos, TimesFM)
- **[ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)** - Prompt design patterns for time series LLMs
- **[data-sql-optimization](../data-sql-optimization/SKILL.md)** - SQL optimization for time series data storage and retrieval

---

## External Resources

See [data/sources.json](data/sources.json) for curated web resources including:

- Classical methods (statsmodels, Prophet, ARIMA)
- Deep learning frameworks (PyTorch Forecasting, GluonTS, Darts, NeuralProphet)
- Transformer models (TimesFM, Chronos, Lag-Llama, Informer, Autoformer)
- Anomaly detection tools (PyOD, STUMPY, Isolation Forest)
- Feature engineering libraries (tsfresh, TSFuse, Featuretools)
- Production deployment (Kats, MLflow, sktime)
- Benchmarks and datasets (M5 Competition, Monash Time Series, UCI)

---

## Usage Notes

**For Claude:**

- Activate this skill for hands-on forecasting tasks, feature engineering, backtesting, or production setup
- Start with [Quick Reference](#quick-reference) and [Decision Tree](#decision-tree-choosing-time-series-approach) for fast guidance
- Drill into resources/ for detailed implementation patterns
- Use templates/ for copy-paste ready code
- Always check for temporal leakage (future data in training)
- Start with strong baselines; choose model family based on horizon, covariates, and latency/cost constraints
- Emphasize explainability for healthcare/finance domains
- Monitor for data distribution shifts in production

**Key Principle:** Time series forecasting is about temporal structure, not IID assumptions. Use temporal validation, avoid future leakage, and choose models based on horizon length and data characteristics.
