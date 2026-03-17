---
name: model-deployment
description: Deploy ML models with FastAPI, Docker, Kubernetes. Use for serving predictions, containerization, monitoring, drift detection, or encountering latency issues, health check failures, version conflicts.
keywords: model deployment, FastAPI, Docker, Kubernetes, ML serving, model monitoring, drift detection, A/B testing, CI/CD, mlops, production ml, model versioning, health checks, Prometheus, containerization, rolling updates, blue-green deployment, canary deployment, model registry
license: MIT
---

# ML Model Deployment

Deploy trained models to production with proper serving and monitoring.

## Deployment Options

| Method | Use Case | Latency |
|--------|----------|---------|
| REST API | Web services | Medium |
| Batch | Large-scale processing | N/A |
| Streaming | Real-time | Low |
| Edge | On-device | Very low |

## FastAPI Model Server

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('model.pkl')

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: float

@app.get('/health')
def health():
    return {'status': 'healthy'}

@app.post('/predict', response_model=PredictionResponse)
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].max()
    return PredictionResponse(prediction=prediction, probability=probability)
```

## Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model.pkl .
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Model Monitoring

```python
class ModelMonitor:
    def __init__(self):
        self.predictions = []
        self.latencies = []

    def log_prediction(self, input_data, prediction, latency):
        self.predictions.append({
            'input': input_data,
            'prediction': prediction,
            'latency': latency,
            'timestamp': datetime.now()
        })

    def detect_drift(self, reference_distribution):
        # Compare current predictions to reference
        pass
```

## Deployment Checklist

- [ ] Model validated on test set
- [ ] API endpoints documented
- [ ] Health check endpoint
- [ ] Authentication configured
- [ ] Logging and monitoring setup
- [ ] Model versioning in place
- [ ] Rollback procedure documented

## Quick Start: Deploy Model in 6 Steps

```bash
# 1. Save trained model
import joblib
joblib.dump(model, 'model.pkl')

# 2. Create FastAPI app (see references/fastapi-production-server.md)
# app.py with /predict and /health endpoints

# 3. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py model.pkl ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 4. Build and test locally
docker build -t model-api:v1.0.0 .
docker run -p 8000:8000 model-api:v1.0.0

# 5. Push to registry
docker tag model-api:v1.0.0 registry.example.com/model-api:v1.0.0
docker push registry.example.com/model-api:v1.0.0

# 6. Deploy to Kubernetes
kubectl apply -f deployment.yaml
kubectl rollout status deployment/model-api
```

## Known Issues Prevention

### 1. No Health Checks = Downtime
**Problem**: Load balancer sends traffic to unhealthy pods, causing 503 errors.

**Solution**: Implement both liveness and readiness probes:
```python
# app.py
@app.get("/health")  # Liveness: Is service alive?
async def health():
    return {"status": "healthy"}

@app.get("/ready")  # Readiness: Can handle traffic?
async def ready():
    try:
        _ = model_store.model  # Verify model loaded
        return {"status": "ready"}
    except:
        raise HTTPException(503, "Not ready")
```

```yaml
# deployment.yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
```

### 2. Model Not Found Errors in Container
**Problem**: `FileNotFoundError: model.pkl` when container starts.

**Solution**: Verify model file is copied in Dockerfile and path matches:
```dockerfile
# ❌ Wrong: Model in wrong directory
COPY model.pkl /app/models/  # But code expects /app/model.pkl

# ✅ Correct: Consistent paths
COPY model.pkl /models/model.pkl
ENV MODEL_PATH=/models/model.pkl

# In Python:
model_path = os.getenv("MODEL_PATH", "/models/model.pkl")
```

### 3. Unhandled Input Validation = 500 Errors
**Problem**: Invalid inputs crash API with unhandled exceptions.

**Solution**: Use Pydantic for automatic validation:
```python
from pydantic import BaseModel, Field, validator

class PredictionRequest(BaseModel):
    features: List[float] = Field(..., min_items=1, max_items=100)

    @validator('features')
    def validate_finite(cls, v):
        if not all(np.isfinite(val) for val in v):
            raise ValueError("All features must be finite")
        return v

# FastAPI auto-validates and returns 422 for invalid requests
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Request is guaranteed valid here
    pass
```

### 4. No Drift Monitoring = Silent Degradation
**Problem**: Model performance degrades over time, no one notices until users complain.

**Solution**: Implement drift detection (see references/model-monitoring-drift.md):
```python
monitor = ModelMonitor(reference_data=training_data, drift_threshold=0.1)

@app.post("/predict")
async def predict(request: PredictionRequest):
    prediction = model.predict(features)
    monitor.log_prediction(features, prediction, latency)

    # Alert if drift detected
    if monitor.should_retrain():
        alert_manager.send_alert("Model drift detected - retrain recommended")

    return prediction
```

### 5. Missing Resource Limits = OOM Kills
**Problem**: Pod killed by Kubernetes OOMKiller, service goes down.

**Solution**: Set memory/CPU limits and requests:
```yaml
resources:
  requests:
    memory: "512Mi"  # Guaranteed
    cpu: "500m"
  limits:
    memory: "1Gi"    # Max allowed
    cpu: "1000m"

# Monitor actual usage:
kubectl top pods
```

### 6. No Rollback Plan = Stuck on Bad Deploy
**Problem**: New model version has bugs, no way to revert quickly.

**Solution**: Tag images with versions, keep previous deployment:
```bash
# Deploy with version tag
kubectl set image deployment/model-api model-api=registry/model-api:v1.2.0

# If issues, rollback to previous
kubectl rollout undo deployment/model-api

# Or specify version
kubectl set image deployment/model-api model-api=registry/model-api:v1.1.0
```

### 7. Synchronous Prediction = Slow Batch Processing
**Problem**: Processing 10,000 predictions one-by-one takes hours.

**Solution**: Implement batch endpoint:
```python
@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    # Process all at once (vectorized)
    features = np.array(request.instances)
    predictions = model.predict(features)  # Much faster!
    return {"predictions": predictions.tolist()}
```

### 8. No CI/CD Validation = Deploy Bad Models
**Problem**: Deploying model that fails basic tests, breaking production.

**Solution**: Validate in CI pipeline (see references/cicd-ml-models.md):
```yaml
# .github/workflows/deploy.yml
- name: Validate model performance
  run: |
    python scripts/validate_model.py \
      --model model.pkl \
      --test-data test.csv \
      --min-accuracy 0.85  # Fail if below threshold
```

## Best Practices

- **Version everything**: Models (semantic versioning), Docker images, deployments
- **Monitor continuously**: Latency, error rate, drift, resource usage
- **Test before deploy**: Unit tests, integration tests, performance benchmarks
- **Deploy gradually**: Canary (10%), then full rollout
- **Plan for rollback**: Keep previous version, document procedure
- **Log predictions**: Enable debugging and drift detection
- **Set resource limits**: Prevent OOM kills and resource contention
- **Use health checks**: Enable proper load balancing

## When to Load References

Load reference files for detailed implementations:

- **FastAPI Production Server**: Load `references/fastapi-production-server.md` for complete production-ready FastAPI implementation with error handling, validation (Pydantic models), logging, health/readiness probes, batch predictions, model versioning, middleware, exception handlers, and performance optimizations (caching, async)

- **Model Monitoring & Drift**: Load `references/model-monitoring-drift.md` for ModelMonitor implementation with KS-test drift detection, Jensen-Shannon divergence, Prometheus metrics integration, alert configuration (Slack, email), continuous monitoring service, and dashboard endpoints

- **Containerization & Deployment**: Load `references/containerization-deployment.md` for multi-stage Dockerfiles, model versioning in containers, Docker Compose setup, A/B testing with Nginx, Kubernetes deployments (rolling update, blue-green, canary), GitHub Actions CI/CD, and deployment checklists

- **CI/CD for ML Models**: Load `references/cicd-ml-models.md` for complete GitHub Actions pipeline with model validation, data validation, automated testing, security scanning, performance benchmarks, automated rollback, and deployment strategies
