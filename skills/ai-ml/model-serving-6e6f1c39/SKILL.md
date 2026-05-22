---
name: model-serving
version: "2.0.0"
sasmp_version: "1.3.0"
description: Master model serving - inference optimization, scaling, deployment, edge serving
bonded_agent: 05-model-serving
bond_type: PRIMARY_BOND

# SKILL METADATA
category: deployment
difficulty: intermediate_to_advanced
estimated_hours: 35
prerequisites:
  - mlops-basics
  - training-pipelines

# VALIDATION
validation:
  pre_conditions:
    - "Completed prerequisite skills"
    - "Trained model available"
  post_conditions:
    - "Can deploy models with BentoML/Triton"
    - "Can optimize inference latency"
    - "Can configure auto-scaling"

# OBSERVABILITY
observability:
  metrics:
    - models_deployed
    - inference_latency
    - optimization_speedup
---

# Model Serving Skill

> **Learn**: Deploy ML models for production inference with optimization.

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Bonded Agent** | 05-model-serving |
| **Difficulty** | Intermediate to Advanced |
| **Duration** | 35 hours |
| **Prerequisites** | mlops-basics, training-pipelines |

---

## Learning Objectives

1. **Deploy** models with BentoML and Triton
2. **Optimize** inference with quantization and ONNX
3. **Configure** auto-scaling policies
4. **Implement** batch and streaming inference
5. **Deploy** to edge devices

---

## Topics Covered

### Module 1: Serving Platforms (8 hours)

**Platform Comparison:**

| Platform | Multi-framework | Dynamic Batching | Kubernetes |
|----------|-----------------|------------------|------------|
| TorchServe | PyTorch only | ✅ | ✅ |
| Triton | ✅ | ✅ | ✅ |
| BentoML | ✅ | ✅ | ✅ |
| Seldon | ✅ | ⚠️ | ✅ |

---

### Module 2: BentoML Deployment (10 hours)

**Service Definition:**

```python
import bentoml
from bentoml.io import JSON, NumpyNdarray

@bentoml.service(resources={"gpu": 1, "memory": "4Gi"})
class ModelService:
    def __init__(self):
        self.model = bentoml.pytorch.load_model("model:latest")

    @bentoml.api(route="/predict")
    async def predict(self, input_array: np.ndarray) -> dict:
        with torch.no_grad():
            predictions = self.model(input_array)
        return {"predictions": predictions.tolist()}
```

**Exercises:**
- [ ] Create BentoML service for your model
- [ ] Containerize and deploy to Kubernetes
- [ ] Configure traffic management

---

### Module 3: Inference Optimization (10 hours)

**Optimization Techniques:**

```python
# 1. Dynamic Quantization
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# 2. ONNX Export
torch.onnx.export(model, sample_input, "model.onnx")

# 3. TensorRT Conversion
import tensorrt as trt
# Convert ONNX to TensorRT for NVIDIA GPUs
```

**Expected Speedups:**
| Technique | Speedup | Accuracy Impact |
|-----------|---------|-----------------|
| FP16 | 2-3x | <1% |
| INT8 | 3-4x | 1-2% |
| TensorRT | 5-10x | <1% |

---

### Module 4: Scaling & Monitoring (7 hours)

**Kubernetes HPA:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-serving
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

## Code Templates

### Template: Production Serving

```python
# templates/serving.py
from fastapi import FastAPI
import torch
import numpy as np

app = FastAPI()

class ProductionServer:
    def __init__(self, model_path: str):
        self.model = torch.jit.load(model_path)
        self.model.eval()

    def predict(self, inputs: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            tensor = torch.from_numpy(inputs)
            outputs = self.model(tensor)
        return outputs.numpy()

server = ProductionServer("model.pt")

@app.post("/predict")
async def predict(data: dict):
    inputs = np.array(data["inputs"])
    predictions = server.predict(inputs)
    return {"predictions": predictions.tolist()}
```

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| High latency | No optimization | Apply quantization, batching |
| Cold starts | Serverless | Pre-warming, min replicas |
| OOM | Model too large | Optimize, reduce batch size |

---

## Resources

- [BentoML Documentation](https://docs.bentoml.com/)
- [Triton Inference Server](https://developer.nvidia.com/triton-inference-server)
- [ONNX Runtime](https://onnxruntime.ai/)
- [See: ml-monitoring] - Monitor deployed models

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12 | Production-grade with optimization |
| 1.0.0 | 2024-11 | Initial release |
