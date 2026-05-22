---
name: ml-deployment
description: Deploy ML models to production - APIs, containerization, monitoring, and MLOps
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 07-model-deployment
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: model
      type: object
      validation: "Trained model with predict method"
  optional:
    - name: port
      type: integer
      default: 8000
      validation: "1024 <= port <= 65535"
    - name: workers
      type: integer
      default: 4

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [latency_ms, requests_per_second, error_rate]
---

# ML Deployment Skill

> Take models from development to production.

## Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI(title="ML Model API")
model = joblib.load('model.pkl')

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    prediction: float

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    X = np.array([request.features])
    prediction = model.predict(X)[0]
    return PredictResponse(prediction=float(prediction))

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Key Topics

### 1. Model Export

```python
import torch
import torch.onnx

# Export PyTorch to ONNX
def export_to_onnx(model, sample_input, path='model.onnx'):
    model.eval()
    torch.onnx.export(
        model,
        sample_input,
        path,
        export_params=True,
        opset_version=14,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}}
    )

# ONNX inference
import onnxruntime as ort

session = ort.InferenceSession('model.onnx')
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: input_data})[0]
```

### 2. Docker Containerization

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/models/model.onnx
    volumes:
      - ./models:/models:ro
    restart: unless-stopped
```

### 3. Monitoring with Prometheus

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
REQUESTS = Counter('model_requests_total', 'Total requests', ['status'])
LATENCY = Histogram('model_latency_seconds', 'Latency in seconds')

@app.post("/predict")
async def predict(request: PredictRequest):
    import time
    start = time.time()

    try:
        prediction = model.predict(request.features)
        REQUESTS.labels(status='success').inc()
        return {"prediction": prediction}
    except Exception as e:
        REQUESTS.labels(status='error').inc()
        raise
    finally:
        LATENCY.observe(time.time() - start)
```

### 4. Model Versioning

```python
import mlflow

# Log model
with mlflow.start_run():
    mlflow.log_params({"n_estimators": 100, "max_depth": 10})
    mlflow.log_metrics({"accuracy": 0.95, "f1": 0.93})
    mlflow.sklearn.log_model(model, "model")

# Load model
model_uri = "runs:/abc123/model"
model = mlflow.sklearn.load_model(model_uri)
```

### 5. A/B Testing

```python
import random

class ABTest:
    def __init__(self, variants: dict[str, float]):
        self.variants = variants  # {"A": 0.5, "B": 0.5}
        self.results = {v: {"count": 0, "success": 0} for v in variants}

    def get_variant(self, user_id: str) -> str:
        random.seed(hash(user_id))
        r = random.random()
        cumulative = 0
        for variant, weight in self.variants.items():
            cumulative += weight
            if r <= cumulative:
                return variant
        return list(self.variants.keys())[-1]

    def record(self, variant: str, success: bool):
        self.results[variant]["count"] += 1
        if success:
            self.results[variant]["success"] += 1
```

## Best Practices

### DO
- Version your models
- Implement health checks
- Use async logging
- Set up monitoring day one
- Use canary deployments

### DON'T
- Don't deploy without validation
- Don't skip latency testing
- Don't ignore drift
- Don't hard-code configs

## Exercises

### Exercise 1: FastAPI Service
```python
# TODO: Create a FastAPI service that:
# 1. Loads a model on startup
# 2. Has /predict and /health endpoints
# 3. Validates input with Pydantic
```

### Exercise 2: Docker Deployment
```python
# TODO: Containerize your ML service
# Create Dockerfile and docker-compose.yml
```

## Unit Test Template

```python
import pytest
from fastapi.testclient import TestClient

def test_health_endpoint():
    """Test health check."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    """Test prediction."""
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0]})

    assert response.status_code == 200
    assert "prediction" in response.json()
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| High latency | Model too large | Quantize, use ONNX |
| Memory leaks | Poor cleanup | Implement proper lifecycle |
| API errors | Input validation | Add Pydantic schemas |
| Scaling issues | Blocking I/O | Use async, add workers |

## Related Resources

- **Agent**: `07-model-deployment`
- **Previous**: `computer-vision`
- **Docs**: [FastAPI](https://fastapi.tiangolo.com/)

---

**Version**: 1.4.0 | **Status**: Production Ready
