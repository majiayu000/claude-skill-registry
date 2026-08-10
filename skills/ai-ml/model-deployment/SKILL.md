---
name: model-deployment
description: Deploy trained machine learning models as production-ready services using REST APIs, containers, serverless functions, and orchestration platforms. Use when the user requests model deployment or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills
  version: 1.0.0
---

# Model Deployment

This skill enables an AI agent to deploy trained machine learning models into production environments. It covers packaging models into serving APIs with FastAPI or Flask, containerizing with Docker, orchestrating with Kubernetes, and deploying to serverless platforms. The agent handles model versioning, health checks, input validation, logging, and monitoring to ensure reliable and scalable inference in production.

## Workflow

1. **Serialize and package the model:** Export the trained model to a portable format such as ONNX, TorchScript, SavedModel, or joblib pickle. Bundle the model artifact with its preprocessing pipeline and any required configuration files so inference is self-contained.

2. **Build the serving API:** Create a REST API using FastAPI or Flask that loads the model at startup and exposes prediction endpoints. Include a health check endpoint, request/response schemas with input validation (Pydantic models), structured logging, and error handling that returns meaningful HTTP status codes.

3. **Containerize with Docker:** Write a Dockerfile that installs dependencies from a pinned `requirements.txt`, copies the model artifact and serving code, and sets the entrypoint to the API server. Use multi-stage builds to minimize image size and avoid including training-only dependencies.

4. **Configure orchestration and scaling:** Define Kubernetes Deployment and Service manifests (or equivalent for your platform) with resource requests/limits, readiness and liveness probes pointing at the health check endpoint, and a Horizontal Pod Autoscaler to scale based on CPU, memory, or custom metrics like request latency.

5. **Deploy and verify:** Push the container image to a registry, apply the Kubernetes manifests or deploy to the serverless platform, and run smoke tests against the live endpoint. Validate that responses match expected outputs for a set of known inputs.

6. **Monitor and iterate:** Integrate with monitoring tools like Prometheus and Grafana to track request latency, error rates, throughput, and model-specific metrics like prediction distribution drift. Set up alerts for anomalies and establish a redeployment workflow for updated model versions using blue-green or canary strategies.

## Supported Technologies

- **API frameworks:** FastAPI, Flask, TorchServe, TensorFlow Serving, Triton Inference Server
- **Containerization:** Docker, Podman
- **Orchestration:** Kubernetes, Docker Compose, AWS ECS, Google Cloud Run
- **Serverless:** AWS Lambda, Google Cloud Functions, Azure Functions
- **Monitoring:** Prometheus, Grafana, Datadog, AWS CloudWatch
- **Model registries:** MLflow Model Registry, AWS SageMaker Model Registry, Weights & Biases

## Usage

Provide the agent with a trained model artifact, its dependencies, and the target deployment environment (local Docker, Kubernetes cluster, serverless). The agent will generate all necessary serving code, container configuration, and deployment manifests, then guide you through the deployment process.

## Examples

### Example 1: Deploying a Model with FastAPI

```python
# app.py
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from contextlib import asynccontextmanager
from typing import List

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load("model.pkl")
    yield

app = FastAPI(title="ML Model API", version="1.0.0", lifespan=lifespan)

class PredictionRequest(BaseModel):
    features: List[float]

    @validator("features")
    def validate_features(cls, v):
        if len(v) != 4:
            raise ValueError("Expected exactly 4 features")
        return v

class PredictionResponse(BaseModel):
    prediction: int
    probability: List[float]

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = int(model.predict(features)[0])
        probability = model.predict_proba(features)[0].tolist()
        return PredictionResponse(prediction=prediction, probability=probability)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Example 2: Docker + Kubernetes Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY app.py model.pkl ./
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**k8s-deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model-api
  template:
    metadata:
      labels:
        app: ml-model-api
    spec:
      containers:
        - name: api
          image: registry.example.com/ml-model-api:v1.0.0
          ports:
            - containerPort: 8000
          resources:
            requests: { cpu: "250m", memory: "512Mi" }
            limits: { cpu: "1000m", memory: "1Gi" }
          readinessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 15
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-api
spec:
  selector:
    app: ml-model-api
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Best Practices

- **Pin all dependency versions** in `requirements.txt` and use deterministic Docker builds to guarantee reproducibility across environments.
- **Separate model artifacts from code** so you can update models without rebuilding the entire container image. Use a model registry or cloud storage with versioned paths.
- **Implement input validation** with Pydantic or JSON Schema to reject malformed requests before they reach the model and produce confusing errors.
- **Use readiness probes** in Kubernetes to prevent traffic from reaching pods that haven't finished loading the model, which can take significant time for large models.
- **Adopt canary deployments** when releasing new model versions — route a small percentage of traffic to the new version and compare metrics before full rollout.
- **Log predictions and inputs** (with PII redacted) to enable debugging, auditing, and data drift detection in production.

## Edge Cases

- **Large model files (> 1 GB):** Avoid baking them into Docker images. Instead, download from cloud storage (S3, GCS) at startup or mount a persistent volume. Use lazy loading if the model takes a long time to initialize.
- **Cold start latency on serverless:** Serverless functions may take 10-30 seconds to load large models. Mitigate with provisioned concurrency (AWS Lambda), min-instances (Cloud Run), or by using optimized formats like ONNX Runtime.
- **Inconsistent preprocessing at inference:** The preprocessing pipeline used at training must exactly match what runs at inference time. Serialize the full pipeline (e.g., with scikit-learn Pipeline + joblib) rather than reimplementing transformations separately.
- **Graceful shutdown and in-flight requests:** Handle SIGTERM signals to finish processing in-flight requests before shutting down. Configure Kubernetes `terminationGracePeriodSeconds` to allow enough time for pending requests to complete.
- **GPU vs CPU inference mismatches:** Models trained on GPU may fail if deployed to CPU-only environments. Explicitly map model tensors to CPU during loading (`torch.load(path, map_location="cpu")`) and test inference on the target hardware before deployment.
