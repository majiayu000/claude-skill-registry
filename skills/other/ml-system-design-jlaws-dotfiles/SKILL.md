---
name: ml-system-design
description: "Use when designing end-to-end ML systems, choosing batch vs streaming inference, preventing training/serving skew, building data flywheels, or planning ML infrastructure scaling."
---

# ML System Design

## Serving Pattern Decision Table

| Factor | Batch | Online (Real-time) | Streaming |
|--------|-------|---------------------|-----------|
| Latency tolerance | Hours | <100ms | Seconds |
| Request pattern | Scheduled/bulk | Per-request | Continuous |
| Freshness need | Stale OK | Must be fresh | Near-real-time |
| Compute cost | Low (off-peak) | High (always-on) | Medium |
| Example | Recommendation email | Search ranking | Fraud detection |
| Infra complexity | Low | Medium | High |
| Failure mode | Retry whole job | Per-request retry | Checkpoint + replay |

## System Design Template

Work through these phases sequentially. Skip none.

### Phase 1: Problem and Metrics

```
1. Business problem → ML problem mapping
   - "Increase engagement" → ranking/recommendation
   - "Reduce fraud" → binary classification
   - "Extract info" → NER/sequence labeling

2. Metrics
   - Business: revenue, CTR, churn rate
   - Model: precision, recall, AUC, NDCG
   - System: p50/p99 latency, throughput, availability

3. Constraints
   - Latency budget (e.g., <50ms for serving)
   - Cost ceiling (e.g., <$0.001 per inference)
   - Data privacy (PII handling, GDPR)
```

### Phase 2: Data Pipeline

```
Raw Sources → Ingestion → Validation → Feature Engineering → Feature Store
                                |
                          Data Quality Checks
                          - Schema validation
                          - Distribution checks
                          - Freshness checks
```

```python
# Data validation with Pandera
import pandera as pa

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, nullable=False),
    "event_ts": pa.Column(pa.DateTime, nullable=False),
    "amount": pa.Column(float, checks=[
        pa.Check.ge(0),
        pa.Check.le(1_000_000),
    ]),
})

validated_df = schema.validate(raw_df)
```

### Phase 3: Feature Engineering

```python
# Shared feature transforms -- used in BOTH training and serving
# This is the single most important thing for preventing skew

class UserFeatures:
    """Feature definitions shared between training and serving."""

    def txn_velocity(self, user_id: str, window_hours: int = 24) -> float:
        """Transaction count in rolling window."""
        # In training: computed from historical log
        # In serving: computed from feature store (pre-aggregated)
        ...

    def avg_order_value(self, user_id: str, window_days: int = 30) -> float:
        ...

    def transform(self, raw: dict) -> dict:
        """Single transform function used everywhere."""
        return {
            "txn_velocity_24h": self.txn_velocity(raw["user_id"], 24),
            "avg_order_30d": self.avg_order_value(raw["user_id"], 30),
            "hour_of_day": raw["timestamp"].hour,
            "day_of_week": raw["timestamp"].weekday(),
            "log_amount": math.log1p(raw["amount"]),
        }
```

### Phase 4: Model Selection

| Problem Type | Start With | Scale To |
|-------------|-----------|---------|
| Tabular classification | XGBoost | XGBoost (usually stays best) |
| Tabular regression | XGBoost | XGBoost + feature engineering |
| Text classification | Fine-tuned BERT-small | Distilled model from larger LLM |
| Ranking | LambdaMART | Two-tower + cross-encoder reranker |
| Recommendation | Matrix factorization | Two-tower retrieval + ranking |
| Time series | Prophet / statsmodels | Temporal fusion transformer |

### Phase 5: Training Pipeline

```python
# Training pipeline skeleton
from dataclasses import dataclass

@dataclass
class TrainConfig:
    experiment_name: str
    data_version: str          # DVC or artifact version
    model_type: str
    hyperparams: dict
    train_split_date: str      # Time-based split, never random for time data
    val_split_date: str
    test_split_date: str

def train(config: TrainConfig):
    # 1. Load versioned data
    df = load_data(config.data_version)

    # 2. Time-based split (NEVER random for temporal data)
    train = df[df.date < config.train_split_date]
    val = df[(df.date >= config.val_split_date) & (df.date < config.test_split_date)]
    test = df[df.date >= config.test_split_date]

    # 3. Transform with shared feature code
    features = UserFeatures()
    X_train = train.apply(features.transform, axis=1)

    # 4. Train
    model = fit_model(config.model_type, X_train, train.label, config.hyperparams)

    # 5. Evaluate on test
    metrics = evaluate(model, X_test, test.label)

    # 6. Log everything
    log_experiment(config, metrics, model)

    return model, metrics
```

## Training/Serving Skew Prevention

The #1 cause of ML system failures in production.

| Skew Type | Cause | Prevention |
|-----------|-------|------------|
| Feature skew | Different code paths | Shared transform library |
| Data skew | Different data sources | Feature store (Feast, Tecton) |
| Label skew | Label definition change | Versioned label pipelines |
| Time skew | Future data leakage | Strict time-based splits |

```python
# Feature store pattern (Feast example)
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Training: get historical features (point-in-time correct)
training_df = store.get_historical_features(
    entity_df=entity_df_with_timestamps,
    features=["user_features:txn_velocity_24h", "user_features:avg_order_30d"],
).to_df()

# Serving: get latest features (same definitions, same code)
online_features = store.get_online_features(
    features=["user_features:txn_velocity_24h", "user_features:avg_order_30d"],
    entity_rows=[{"user_id": "abc123"}],
).to_dict()
```

## Data Flywheel Design

```
User Interaction
    → Collect implicit labels (clicks, conversions, dwell time)
    → Log predictions + actuals
    → Identify hard examples (low-confidence predictions)
    → Human review queue (prioritized by uncertainty)
    → Curated labels added to training set
    → Retrain on expanded dataset
    → Deploy improved model
    → Better predictions → more user engagement
    → Repeat
```

```python
# Hard example mining for the flywheel
def find_hard_examples(predictions: list[dict], threshold: float = 0.1) -> list[dict]:
    """Find predictions where model was least confident."""
    hard = []
    for pred in predictions:
        confidence = abs(pred["score"] - 0.5)  # Distance from decision boundary
        if confidence < threshold:
            hard.append({
                "input": pred["input"],
                "predicted": pred["label"],
                "confidence": pred["score"],
                "needs_review": True,
            })
    return sorted(hard, key=lambda x: x["confidence"])
```

## Scaling Patterns

### Horizontal Serving

```python
# Model serving with batched inference (key optimization)
import asyncio
from collections import deque

class BatchingPredictor:
    """Collect individual requests, batch them for GPU efficiency."""

    def __init__(self, model, max_batch: int = 32, max_wait_ms: float = 10):
        self.model = model
        self.max_batch = max_batch
        self.max_wait = max_wait_ms / 1000
        self._queue: deque = deque()
        self._loop = asyncio.get_event_loop()
        self._loop.create_task(self._process_loop())

    async def predict(self, input_data: dict) -> dict:
        future = self._loop.create_future()
        self._queue.append((input_data, future))
        return await future

    async def _process_loop(self):
        while True:
            await asyncio.sleep(self.max_wait)
            if not self._queue:
                continue
            batch = []
            futures = []
            while self._queue and len(batch) < self.max_batch:
                data, fut = self._queue.popleft()
                batch.append(data)
                futures.append(fut)
            # Single batched GPU call
            results = self.model.predict_batch(batch)
            for fut, result in zip(futures, results):
                fut.set_result(result)
```

### Model Parallelism Decision

| Model Size | Strategy |
|-----------|----------|
| <2GB | Single GPU, replicate horizontally |
| 2-10GB | Single GPU (A100 80GB), replicate |
| 10-80GB | Tensor parallelism across GPUs |
| >80GB | Pipeline + tensor parallelism |

## Cost Modeling

```
Training cost estimate:
  GPU hours = (dataset_size / batch_throughput) * epochs * hyperparam_trials
  Cost = GPU_hours * hourly_rate

  Example: 10M rows, 50k rows/sec on A100, 10 epochs, 20 trials
  = (10M/50k) * 10 * 20 = 40,000 seconds = ~11 GPU hours
  = 11 * $3.50/hr (A100 spot) = ~$39 per full sweep

Inference cost estimate:
  Cost per request = (GPU_cost_per_second * latency_seconds) / batch_size

  Example: $3.50/hr A100, 20ms latency, batch size 16
  = ($0.00097/sec * 0.02) / 16 = $0.0000012 per request
  = ~$1.20 per million requests
```

## Monitoring

```python
# Model monitoring checks (run on every prediction batch)
from dataclasses import dataclass

@dataclass
class MonitoringAlert:
    metric: str
    current: float
    threshold: float
    severity: str  # "warning" | "critical"

def monitor_predictions(predictions: list[dict], reference_stats: dict) -> list[MonitoringAlert]:
    alerts = []

    # 1. Feature drift (PSI or KS test)
    for feature_name, ref_dist in reference_stats["features"].items():
        current_dist = compute_distribution(predictions, feature_name)
        psi = compute_psi(ref_dist, current_dist)
        if psi > 0.2:
            alerts.append(MonitoringAlert(f"feature_drift:{feature_name}", psi, 0.2, "critical"))
        elif psi > 0.1:
            alerts.append(MonitoringAlert(f"feature_drift:{feature_name}", psi, 0.1, "warning"))

    # 2. Prediction drift
    pred_mean = sum(p["score"] for p in predictions) / len(predictions)
    ref_mean = reference_stats["pred_mean"]
    if abs(pred_mean - ref_mean) / ref_mean > 0.15:
        alerts.append(MonitoringAlert("prediction_drift", pred_mean, ref_mean, "warning"))

    # 3. Latency
    p99 = compute_percentile([p["latency_ms"] for p in predictions], 99)
    if p99 > reference_stats["p99_threshold_ms"]:
        alerts.append(MonitoringAlert("latency_p99", p99, reference_stats["p99_threshold_ms"], "critical"))

    return alerts
```

## Gotchas

- **Random splits on temporal data**: always use time-based splits; random splits leak future info
- **Offline metric obsession**: a model with 0.01 higher AUC often makes zero business impact; A/B test everything
- **Feature store skipped**: "we'll add it later" means training/serving skew ships on day 1
- **No shadow mode**: deploy new models in shadow mode (predict but don't act) before switching traffic
- **Retraining without validation**: automated retraining must include automated quality gates; never auto-deploy a worse model
- **GPU over-provisioning**: most tabular models don't need GPUs at serving time; benchmark CPU first
- **Ignoring data quality**: garbage in, garbage out; 80% of ML work is data; invest in validation early
- **Missing feedback loops**: if you can't measure real-world outcomes, you can't improve the model
- **Serving the training framework**: don't serve with PyTorch if you can export to ONNX; inference runtimes are 2-10x faster
- **Batch predictions going stale**: if batch runs at midnight and user behavior changes by noon, your predictions are wrong
