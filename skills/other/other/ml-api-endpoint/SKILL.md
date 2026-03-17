---
name: ml-api-endpoint
description: Эксперт ML API. Используй для model serving, inference endpoints, FastAPI и ML deployment.
---

# ML API Endpoint Expert

Expert in designing and deploying machine learning API endpoints.

## Core Principles

### API Design
- **Stateless Design**: Each request contains all necessary information
- **Consistent Response Format**: Standardize success/error structures
- **Versioning Strategy**: Plan for model updates
- **Input Validation**: Rigorous validation before inference

## FastAPI Implementation

### Basic ML Endpoint
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import joblib
import numpy as np

app = FastAPI(title="ML Model API", version="1.0.0")

model = None

@app.on_event("startup")
async def load_model():
    global model
    model = joblib.load("model.pkl")

class PredictionInput(BaseModel):
    features: list[float]

    @validator('features')
    def validate_features(cls, v):
        if len(v) != 10:
            raise ValueError('Expected 10 features')
        return v

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float | None = None
    model_version: str
    request_id: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    features = np.array([input_data.features])
    prediction = model.predict(features)[0]

    return PredictionResponse(
        prediction=float(prediction),
        model_version="v1",
        request_id=generate_request_id()
    )
```

### Batch Prediction
```python
class BatchInput(BaseModel):
    instances: list[list[float]]

    @validator('instances')
    def validate_batch_size(cls, v):
        if len(v) > 100:
            raise ValueError('Batch size cannot exceed 100')
        return v

@app.post("/predict/batch")
async def batch_predict(input_data: BatchInput):
    features = np.array(input_data.instances)
    predictions = model.predict(features)

    return {
        "predictions": predictions.tolist(),
        "count": len(predictions)
    }
```

## Performance Optimization

### Model Caching
```python
class ModelCache:
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, features):
        key = hashlib.md5(str(features).encode()).hexdigest()
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
        return None

    def set(self, features, prediction):
        key = hashlib.md5(str(features).encode()).hexdigest()
        self.cache[key] = (prediction, time.time())
```

## Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "requests_total": request_counter,
        "prediction_latency_avg": avg_latency,
        "error_rate": error_rate
    }
```

## Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Best Practices

- Use async/await for I/O operations
- Validate data types, ranges, and business rules
- Cache predictions for deterministic models
- Handle model failures with fallback responses
- Log predictions, latencies, and errors
- Support multiple model versions
- Set memory and CPU limits
