---
name: ml-deployment-helper
description: |
  Prepares ML models for production deployment with containerization, API creation, monitoring setup, and A/B testing. Activates for "deploy model", "production deployment", "model API", "containerize model", "docker ml", "serving ml model", "model monitoring", "A/B test model". Generates deployment artifacts and ensures models are production-ready with monitoring, versioning, and rollback capabilities.
---

# ML Deployment Helper

## Overview

Bridges the gap between trained models and production systems. Generates deployment artifacts, APIs, monitoring, and A/B testing infrastructure following MLOps best practices.

## Deployment Checklist

Before deploying any model, this skill ensures:

- ✅ Model versioned and tracked
- ✅ Dependencies documented (requirements.txt/Dockerfile)
- ✅ API endpoint created
- ✅ Input validation implemented
- ✅ Monitoring configured
- ✅ A/B testing ready
- ✅ Rollback plan documented
- ✅ Performance benchmarked

## Deployment Patterns

### Pattern 1: REST API (FastAPI)

```python
from specweave import create_model_api

# Generates production-ready API
api = create_model_api(
    model_path="models/model-v3.pkl",
    increment="0042",
    framework="fastapi"
)

# Creates:
# - api/
#   ├── main.py (FastAPI app)
#   ├── models.py (Pydantic schemas)
#   ├── predict.py (Prediction logic)
#   ├── Dockerfile
#   ├── requirements.txt
#   └── tests/
```

Generated `main.py`:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="Recommendation Model API", version="0042-v3")

model = joblib.load("model-v3.pkl")

class PredictionRequest(BaseModel):
    user_id: int
    context: dict

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        prediction = model.predict([request.dict()])
        return {
            "recommendations": prediction.tolist(),
            "model_version": "0042-v3",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}
```

### Pattern 2: Batch Prediction

```python
from specweave import create_batch_predictor

# For offline scoring
batch_predictor = create_batch_predictor(
    model_path="models/model-v3.pkl",
    increment="0042",
    input_path="s3://bucket/data/",
    output_path="s3://bucket/predictions/"
)

# Creates:
# - batch/
#   ├── predictor.py
#   ├── scheduler.yaml (Airflow/Kubernetes CronJob)
#   └── monitoring.py
```

### Pattern 3: Real-Time Streaming

```python
from specweave import create_streaming_predictor

# For Kafka/Kinesis streams
streaming = create_streaming_predictor(
    model_path="models/model-v3.pkl",
    increment="0042",
    input_topic="user-events",
    output_topic="predictions"
)

# Creates:
# - streaming/
#   ├── consumer.py
#   ├── predictor.py
#   ├── producer.py
#   └── docker-compose.yaml
```

## Containerization

```python
from specweave import containerize_model

# Generates optimized Dockerfile
dockerfile = containerize_model(
    model_path="models/model-v3.pkl",
    framework="sklearn",
    python_version="3.10",
    increment="0042"
)
```

Generated `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy model and dependencies
COPY models/model-v3.pkl /app/model.pkl
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY api/ /app/api/

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring Setup

```python
from specweave import setup_model_monitoring

# Configures monitoring for production
monitoring = setup_model_monitoring(
    model_name="recommendation-model",
    increment="0042",
    metrics=[
        "prediction_latency",
        "throughput",
        "error_rate",
        "prediction_distribution",
        "feature_drift"
    ]
)

# Creates:
# - monitoring/
#   ├── prometheus.yaml
#   ├── grafana-dashboard.json
#   ├── alerts.yaml
#   └── drift-detector.py
```

## A/B Testing Infrastructure

```python
from specweave import create_ab_test

# Sets up A/B test framework
ab_test = create_ab_test(
    control_model="model-v2.pkl",
    treatment_model="model-v3.pkl",
    traffic_split=0.1,  # 10% to new model
    success_metric="click_through_rate",
    increment="0042"
)

# Creates:
# - ab-test/
#   ├── router.py (traffic splitting)
#   ├── metrics.py (success tracking)
#   ├── statistical-tests.py (significance testing)
#   └── dashboard.py (real-time monitoring)
```

A/B Test Router:
```python
import random

def route_prediction(user_id, control_model, treatment_model):
    """Route to control or treatment based on user_id hash"""
    
    # Consistent hashing (same user always gets same model)
    user_bucket = hash(user_id) % 100
    
    if user_bucket < 10:  # 10% to treatment
        return treatment_model.predict(features), "treatment"
    else:
        return control_model.predict(features), "control"
```

## Model Versioning

```python
from specweave import ModelVersion

# Register model version
version = ModelVersion.register(
    model_path="models/model-v3.pkl",
    increment="0042",
    metadata={
        "accuracy": 0.87,
        "training_date": "2024-01-15",
        "data_version": "v2024-01",
        "framework": "xgboost==1.7.0"
    }
)

# Easy rollback
if production_metrics["error_rate"] > threshold:
    ModelVersion.rollback(to_version="0042-v2")
```

## Load Testing

```python
from specweave import load_test_model

# Benchmark model performance
results = load_test_model(
    api_url="http://localhost:8000/predict",
    requests_per_second=[10, 50, 100, 500, 1000],
    duration_seconds=60,
    increment="0042"
)
```

Output:
```
Load Test Results:
==================

| RPS  | Latency P50 | Latency P95 | Latency P99 | Error Rate |
|------|-------------|-------------|-------------|------------|
| 10   | 35ms        | 45ms        | 50ms        | 0.00%      |
| 50   | 38ms        | 52ms        | 65ms        | 0.00%      |
| 100  | 45ms        | 70ms        | 95ms        | 0.02%      |
| 500  | 120ms       | 250ms       | 400ms       | 1.20%      |
| 1000 | 350ms       | 800ms       | 1200ms      | 8.50%      |

Recommendation: Deploy with max 100 RPS per instance
Target: <100ms P95 latency (achieved at 100 RPS)
```

## Deployment Commands

```bash
# Generate deployment artifacts
/ml:deploy-prepare 0042

# Create API
/ml:create-api --increment 0042 --framework fastapi

# Setup monitoring
/ml:setup-monitoring 0042

# Create A/B test
/ml:create-ab-test --control v2 --treatment v3 --split 0.1

# Load test
/ml:load-test 0042 --rps 100 --duration 60s

# Deploy to production
/ml:deploy 0042 --environment production
```

## Deployment Increment

The skill creates a deployment increment:

```
.specweave/increments/0043-deploy-recommendation-model/
├── spec.md (deployment requirements)
├── plan.md (deployment strategy)
├── tasks.md
│   ├── [ ] Containerize model
│   ├── [ ] Create API
│   ├── [ ] Setup monitoring
│   ├── [ ] Configure A/B test
│   ├── [ ] Load test
│   ├── [ ] Deploy to staging
│   ├── [ ] Validate staging
│   └── [ ] Deploy to production
├── api/ (FastAPI app)
├── monitoring/ (Grafana dashboards)
├── ab-test/ (A/B testing logic)
└── load-tests/ (Performance benchmarks)
```

## Best Practices

1. **Always load test** before production
2. **Start with 1-5% traffic** in A/B test
3. **Monitor model drift** in production
4. **Version everything** (model, data, code)
5. **Document rollback plan** before deploying
6. **Set up alerts** for anomalies
7. **Gradual rollout** (canary deployment)

## Integration with SpecWeave

```bash
# After training model (increment 0042)
/sw:inc "0043-deploy-recommendation-model"

# Generates deployment increment with all artifacts
/sw:do

# Deploy to production when ready
/ml:deploy 0043 --environment production
```

Model deployment is not the end—it's the beginning of the MLOps lifecycle.
