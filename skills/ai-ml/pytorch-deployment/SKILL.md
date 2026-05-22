---
name: PyTorch Deployment
description: Comprehensive guide for deploying PyTorch models to production, covering export formats, optimization techniques, and deployment patterns.
---

# PyTorch Deployment

## Overview

PyTorch deployment involves exporting models to production-ready formats, optimizing for inference performance, and serving models through various deployment patterns. This skill covers TorchScript, ONNX export, TorchServe, model optimization techniques, inference optimization, FastAPI deployment, model versioning, A/B testing, monitoring, error handling, and performance benchmarking.

## Prerequisites

- Understanding of PyTorch and deep learning models
- Knowledge of model training and evaluation
- Familiarity with web frameworks (FastAPI, Flask)
- Understanding of Docker and containerization
- Basic knowledge of cloud deployment concepts

## Key Concepts

### Model Export Formats

- **TorchScript**: PyTorch's intermediate representation for production deployment
- **Tracing**: Captures computation path from example inputs
- **Scripting**: Captures entire Python code including control flow
- **ONNX**: Open Neural Network Exchange for cross-framework compatibility
- **TorchServe**: PyTorch's model serving framework

### Model Optimization

- **Quantization**: Reducing precision (FP32 → FP16/INT8) for efficiency
- **Pruning**: Removing less important weights from models
- **Knowledge Distillation**: Training smaller models from larger teacher models
- **Model Compression**: Techniques to reduce model size

### Inference Optimization

- **Batching**: Processing multiple inputs together for efficiency
- **GPU Utilization**: Multi-GPU inference for throughput
- **Mixed Precision**: Using FP16 for faster computation
- **Caching**: Repeated computation results

### Deployment Patterns

- **FastAPI Server**: REST API for model serving
- **TorchServe**: Production-ready model serving framework
- **ONNX Runtime**: High-performance inference engine
- **Docker Deployment**: Containerized model deployment

## Implementation Guide

### Model Export Formats

#### TorchScript

TorchScript is an intermediate representation of a PyTorch model that can be run in a high-performance environment such as C++.

**Tracing vs Scripting:**

```python
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 64, 3)
        self.fc = nn.Linear(64 * 26 * 26, 10)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

model = MyModel()
model.eval()

# Method 1: Tracing (captures actual computation path)
example_input = torch.randn(1, 3, 28, 28)
traced_model = torch.jit.trace(model, example_input)
traced_model.save("model_traced.pt")

# Method 2: Scripting (captures entire Python code)
scripted_model = torch.jit.script(model)
scripted_model.save("model_scripted.pt")

# Loading and inference
loaded_model = torch.jit.load("model_traced.pt")
output = loaded_model(example_input)
```

**Handling Control Flow with Scripting:**

```python
class ConditionalModel(nn.Module):
    def forward(self, x):
        if x.sum() > 0:
            return x * 2
        else:
            return x / 2

# Use scripting for models with control flow
model = ConditionalModel()
scripted_model = torch.jit.script(model)
```

#### ONNX Export

Open Neural Network Exchange (ONNX) enables interoperability between different frameworks.

```python
import torch
import torch.onnx

# Export to ONNX
model = MyModel()
model.eval()
dummy_input = torch.randn(1, 3, 28, 28)

torch.onnx.export(
    model,                      # Model to export
    dummy_input,                # Example input
    "model.onnx",               # Output file
    export_params=True,         # Store trained parameters
    opset_version=17,           # ONNX opset version
    do_constant_folding=True,   # Optimize constants
    input_names=['input'],      # Input names
    output_names=['output'],    # Output names
    dynamic_axes={              # Dynamic axes for variable batch size
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)

# Verify ONNX model
import onnx
onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)

# Run inference with ONNX Runtime
import onnxruntime as ort

session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

outputs = session.run([output_name], {input_name: dummy_input.numpy()})
```

**Custom ONNX Operators:**

```python
from torch.onnx import register_custom_op_symbolic

def custom_gsymbolic(g, input, alpha):
    return g.op("CustomOp", input, alpha_f=alpha)

register_custom_op_symbolic("aten::gelu", custom_gsymbolic, 17)
```

#### TorchServe

TorchServe is a flexible, easy-to-use tool for serving PyTorch models.

**Installation:**

```bash
pip install torchserve torch-model-archiver torch-workflow-archiver
```

**Model Archiving:**

```python
# Create model handler (handler.py)
class ModelHandler:
    def __init__(self):
        self.model = None
        self.mapping = None
        self.device = None
        self.initialized = False

    def initialize(self, context):
        """Initialize model and load weights."""
        properties = context.system_properties
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        model_dir = properties.get("model_dir")
        model_pt_path = os.path.join(model_dir, "model.pth")

        self.model = torch.load(model_pt_path, map_location=self.device)
        self.model.eval()
        self.initialized = True

    def preprocess(self, requests):
        """Preprocess input data."""
        inputs = []
        for req in requests:
            data = req.get("data") or req.get("body")
            inputs.append(torch.tensor(data))
        return torch.stack(inputs)

    def inference(self, input_data):
        """Run inference."""
        with torch.no_grad():
            output = self.model(input_data)
        return output

    def postprocess(self, inference_output):
        """Postprocess output."""
        return inference_output.cpu().numpy().tolist()

    def handle(self, data, context):
        """Main handler function."""
        try:
            data = self.preprocess(data)
            data = data.to(self.device)
            output = self.inference(data)
            return self.postprocess(output)
        except Exception as e:
            return [{"error": str(e)}]
```

**Archive and Serve:**

```bash
# Archive model
torch-model-archiver \
  --model-name mymodel \
  --version 1.0 \
  --serialized-file model.pth \
  --handler handler.py \
  --extra-files config.json,index_to_name.json \
  --export-path model_store

# Start TorchServe
torchserve --start --ncs --model-store model_store --models mymodel=mymodel.mar

# Make prediction
curl -X POST http://localhost:8080/predictions/mymodel \
  -H "Content-Type: application/json" \
  -d '{"data": [[...]]}'
```

### Model Optimization

#### Quantization

Quantization reduces model size and improves inference speed by using lower precision numbers.

**Post-Training Quantization (PTQ):**

```python
import torch
from torch.quantization import quantize_dynamic

# Dynamic quantization (weights quantized, activations computed in float)
model = MyModel()

# Quantize specific layers
quantized_model = quantize_dynamic(
    model,
    {nn.Linear, nn.LSTM},  # Layers to quantize
    dtype=torch.qint8      # Quantization dtype
)

# Save quantized model
torch.jit.save(torch.jit.script(quantized_model), "model_quantized.pt")
```

**Static Quantization:**

```python
import torch
from torch.quantization import (
    quantize,
    prepare,
    convert,
    get_default_qconfig,
)

# Prepare model for static quantization
model = MyModel()
model.eval()

# Set quantization configuration
model.qconfig = get_default_qconfig('fbgemm')

# Prepare model with calibration data
prepared_model = prepare(model)

# Calibrate with representative data
with torch.no_grad():
    for data in calibration_dataloader:
        prepared_model(data)

# Convert to quantized model
quantized_model = convert(prepared_model)

# Save
torch.jit.save(torch.jit.script(quantized_model), "model_static_quantized.pt")
```

**Quantization-Aware Training (QAT):**

```python
import torch
from torch.quantization import prepare_qat, convert

# Prepare model for QAT
model = MyModel()
model.train()
model.qconfig = get_default_qconfig('fbgemm')

# Prepare for QAT
model_prepared = prepare_qat(model, inplace=True)

# Fine-tune with quantization simulation
optimizer = torch.optim.SGD(model_prepared.parameters(), lr=0.01)

for epoch in range(num_epochs):
    for batch in train_dataloader:
        optimizer.zero_grad()
        loss = criterion(model_prepared(batch[0]), batch[1])
        loss.backward()
        optimizer.step()

# Convert to quantized model
model_prepared.eval()
quantized_model = convert(model_prepared)
```

#### Pruning

Pruning removes less important weights from model.

**Structured Pruning:**

```python
import torch.nn.utils.prune as prune
import torch

model = MyModel()

# Prune 30% of weights in linear layers
for name, module in model.named_modules():
    if isinstance(module, nn.Linear):
        prune.l1_unstructured(module, name='weight', amount=0.3)

# Make pruning permanent
for name, module in model.named_modules():
    if isinstance(module, nn.Linear):
        prune.remove(module, 'weight')
```

**Global Unstructured Pruning:**

```python
# Prune across all layers globally
parameters_to_prune = []
for name, module in model.named_modules():
    if isinstance(module, (nn.Linear, nn.Conv2d)):
        parameters_to_prune.append((module, 'weight'))

prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2
)
```

**Iterative Pruning:**

```python
def iterative_pruning(model, train_loader, num_iterations=5, prune_amount=0.2):
    for iteration in range(num_iterations):
        print(f"Pruning iteration {iteration + 1}/{num_iterations}")

        # Prune
        for name, module in model.named_modules():
            if isinstance(module, nn.Linear):
                prune.l1_unstructured(module, name='weight', amount=prune_amount)

        # Fine-tune
        for epoch in range(5):
            for batch in train_loader:
                # Training code here
                pass

    # Make pruning permanent
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            prune.remove(module, 'weight')

    return model
```

#### Model Compression

**Knowledge Distillation:**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DistillationLoss(nn.Module):
    def __init__(self, alpha=0.5, temperature=2.0):
        super().__init__()
        self.alpha = alpha
        self.temperature = temperature
        self.kl_div = nn.KLDivLoss(reduction='batchmean')

    def forward(self, student_logits, teacher_logits, targets):
        # Hard loss (cross-entropy with true labels)
        hard_loss = F.cross_entropy(student_logits, targets)

        # Soft loss (KL divergence with teacher)
        soft_loss = self.kl_div(
            F.log_softmax(student_logits / self.temperature, dim=1),
            F.softmax(teacher_logits / self.temperature, dim=1)
        ) * (self.temperature ** 2)

        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss

# Training loop
teacher_model = load_teacher_model()
student_model = create_student_model()
criterion = DistillationLoss(alpha=0.7, temperature=3.0)

teacher_model.eval()
student_model.train()

for batch in train_loader:
    inputs, targets = batch

    with torch.no_grad():
        teacher_outputs = teacher_model(inputs)

    student_outputs = student_model(inputs)
    loss = criterion(student_outputs, teacher_outputs, targets)

    loss.backward()
    optimizer.step()
```

### Inference Optimization

#### Batching

```python
import torch
from collections import deque
import threading
import time

class BatchInferenceServer:
    def __init__(self, model, max_batch_size=32, max_wait_time=0.1):
        self.model = model
        self.model.eval()
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.batch_queue = deque()
        self.results = {}
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._process_batches)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def predict(self, input_data):
        request_id = id(input_data)
        with self.lock:
            self.batch_queue.append((request_id, input_data))
        return request_id

    def get_result(self, request_id, timeout=10):
        start_time = time.time()
        while request_id not in self.results:
            if time.time() - start_time > timeout:
                raise TimeoutError("Prediction timeout")
            time.sleep(0.01)
        return self.results.pop(request_id)

    def _process_batches(self):
        while self.running:
            batch = []
            start_time = time.time()

            with self.lock:
                while len(batch) < self.max_batch_size and \
                      (time.time() - start_time) < self.max_wait_time:
                    if self.batch_queue:
                        batch.append(self.batch_queue.popleft())
                    else:
                        time.sleep(0.001)

            if batch:
                request_ids, inputs = zip(*batch)
                batch_tensor = torch.stack(inputs)

                with torch.no_grad():
                    outputs = self.model(batch_tensor)

                with self.lock:
                    for req_id, output in zip(request_ids, outputs):
                        self.results[req_id] = output
```

#### GPU Utilization

```python
import torch
import torch.multiprocessing as mp

def run_inference(rank, model, inputs, outputs):
    """Worker function for multi-GPU inference."""
    torch.cuda.set_device(rank)
    model = model.to(rank)
    model.eval()

    with torch.no_grad():
        outputs[rank] = model(inputs[rank])

def multi_gpu_inference(model, inputs):
    """Distribute inference across multiple GPUs."""
    num_gpus = torch.cuda.device_count()
    outputs = [None] * num_gpus

    # Split inputs across GPUs
    inputs_per_gpu = torch.chunk(inputs, num_gpus)
    inputs = [inp.to(i) for i, inp in enumerate(inputs_per_gpu)]

    # Spawn processes
    mp.spawn(
        run_inference,
        args=(model, inputs, outputs),
        nprocs=num_gpus,
        join=True
    )

    return torch.cat(outputs, dim=0)
```

#### Mixed Precision

```python
import torch
from torch.cuda.amp import autocast, GradScaler

# For inference with mixed precision
def mixed_precision_inference(model, inputs):
    model.eval()
    with autocast():
        with torch.no_grad():
            outputs = model(inputs)
    return outputs

# For training with mixed precision
scaler = GradScaler()

for batch in train_loader:
    inputs, targets = batch
    inputs, targets = inputs.to(device), targets.to(device)

    optimizer.zero_grad()

    with autocast():
        outputs = model(inputs)
        loss = criterion(outputs, targets)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Deployment Patterns

#### FastAPI Server

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io

app = FastAPI(title="PyTorch Model API")

# Load model
class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(64 * 13 * 13, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)

model = ImageClassifier()
model.load_state_dict(torch.load("model.pth"))
model.eval()

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class PredictionResponse(BaseModel):
    class_id: int
    class_name: str
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)

        # Inference
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)

        return PredictionResponse(
            class_id=predicted.item(),
            class_name=f"class_{predicted.item()}",
            confidence=confidence.item()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/model/info")
async def model_info():
    return {
        "model_type": "ImageClassifier",
        "parameters": sum(p.numel() for p in model.parameters()),
        "input_shape": "(batch, 3, 28, 28)",
        "output_shape": "(batch, 10)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### TorchServe Configuration

**config.properties:**

```properties
inference_address=http://0.0.0.0:8080
management_address=http://0.0.0.0:8081
metrics_address=http://0.0.0.0:8082
number_of_netty_threads=4
job_queue_size=10
model_store=model_store
load_models=all
number_of_gpu=1
default_response_timeout=120
```

**Docker Deployment:**

```dockerfile
FROM pytorch/torchserve:latest

# Copy model archive
COPY model_store /home/model-server/model-store

# Copy config
COPY config.properties /home/model-server/config.properties

# Expose ports
EXPOSE 8080 8081 8082

# Start TorchServe
CMD ["torchserve", \
     "--start", \
     "--model-store", "/home/model-server/model-store", \
     "--models", "mymodel=mymodel.mar", \
     "--ts-config", "/home/model-server/config.properties"]
```

#### ONNX Runtime Server

**Python ONNX Runtime Server:**

```python
from fastapi import FastAPI
import numpy as np
import onnxruntime as ort
from pydantic import BaseModel

app = FastAPI()

# Load ONNX model
session = ort.InferenceSession("model.onnx")

class InputData(BaseModel):
    data: list

@app.post("/predict")
async def predict(input_data: InputData):
    input_array = np.array(input_data.data, dtype=np.float32)

    # Run inference
    outputs = session.run(
        None,
        {session.get_inputs()[0].name: input_array}
    )

    return {"output": outputs[0].tolist()}
```

### Model Versioning

#### Versioning Strategy

```python
import os
import json
from datetime import datetime
import torch

class ModelVersionManager:
    def __init__(self, base_path="models"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_model(self, model, version, metadata=None):
        """Save model with version and metadata."""
        version_path = os.path.join(self.base_path, f"v{version}")
        os.makedirs(version_path, exist_ok=True)

        # Save model weights
        model_path = os.path.join(version_path, "model.pth")
        torch.save(model.state_dict(), model_path)

        # Save metadata
        metadata = metadata or {}
        metadata.update({
            "version": version,
            "saved_at": datetime.now().isoformat(),
            "model_path": model_path
        })

        metadata_path = os.path.join(version_path, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        return version_path

    def load_model(self, version, model_class):
        """Load model by version."""
        version_path = os.path.join(self.base_path, f"v{version}")
        model_path = os.path.join(version_path, "model.pth")

        model = model_class()
        model.load_state_dict(torch.load(model_path))
        model.eval()

        return model

    def list_versions(self):
        """List all available versions."""
        versions = []
        for item in os.listdir(self.base_path):
            if item.startswith("v"):
                version_path = os.path.join(self.base_path, item)
                metadata_path = os.path.join(version_path, "metadata.json")
                if os.path.exists(metadata_path):
                    with open(metadata_path) as f:
                        versions.append(json.load(f))
        return sorted(versions, key=lambda x: x["version"])
```

### A/B Testing Models

```python
import random
from typing import Dict, Optional
import torch

class ABTestModelRouter:
    def __init__(self, models: Dict[str, torch.nn.Module], traffic_split: Dict[str, float]):
        """
        Args:
            models: Dictionary of model_name -> model
            traffic_split: Dictionary of model_name -> traffic_percentage (sum must be 1.0)
        """
        self.models = models
        self.traffic_split = traffic_split
        self.model_names = list(traffic_split.keys())
        self.cumulative_split = []
        cumulative = 0
        for name in self.model_names:
            cumulative += traffic_split[name]
            self.cumulative_split.append(cumulative)

    def get_model(self, request_id: Optional[str] = None) -> torch.nn.Module:
        """Select model based on traffic split."""
        # Use request_id for consistent routing (same request always goes to same model)
        if request_id:
            hash_val = hash(request_id) % 1000
            rand_val = hash_val / 1000.0
        else:
            rand_val = random.random()

        for i, threshold in enumerate(self.cumulative_split):
            if rand_val < threshold:
                return self.models[self.model_names[i]]

        return self.models[self.model_names[-1]]

    def predict(self, input_data, request_id: Optional[str] = None):
        """Run prediction with A/B testing."""
        model = self.get_model(request_id)
        model.eval()

        with torch.no_grad():
            output = model(input_data)

        return output

# Usage
model_a = create_model_v1()
model_b = create_model_v2()

router = ABTestModelRouter(
    models={"v1": model_a, "v2": model_b},
    traffic_split={"v1": 0.7, "v2": 0.3}
)

# Predictions will be routed 70% to v1 and 30% to v2
output = router.predict(input_data, request_id="user_123")
```

### Model Monitoring

```python
import time
import json
from collections import defaultdict
from datetime import datetime
import torch

class ModelMonitor:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.metrics = defaultdict(list)
        self.start_time = time.time()

    def log_prediction(self, request_id: str, input_shape: tuple,
                       output_shape: tuple, latency: float,
                       model_version: str):
        """Log prediction metrics."""
        self.metrics["predictions"].append({
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "input_shape": input_shape,
            "output_shape": output_shape,
            "latency_ms": latency,
            "model_version": model_version
        })

    def log_error(self, request_id: str, error_type: str, error_message: str):
        """Log prediction errors."""
        self.metrics["errors"].append({
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message
        })

    def get_summary(self):
        """Get monitoring summary."""
        predictions = self.metrics["predictions"]
        errors = self.metrics["errors"]

        if predictions:
            avg_latency = sum(p["latency_ms"] for p in predictions) / len(predictions)
            total_predictions = len(predictions)
        else:
            avg_latency = 0
            total_predictions = 0

        return {
            "model_name": self.model_name,
            "uptime_seconds": time.time() - self.start_time,
            "total_predictions": total_predictions,
            "total_errors": len(errors),
            "average_latency_ms": avg_latency,
            "error_rate": len(errors) / max(total_predictions, 1) * 100
        }

# Usage with FastAPI
monitor = ModelMonitor("image_classifier")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Preprocess and predict
        output = model(input_tensor)
        latency = (time.time() - start_time) * 1000

        monitor.log_prediction(
            request_id=request_id,
            input_shape=tuple(input_tensor.shape),
            output_shape=tuple(output.shape),
            latency=latency,
            model_version="1.0"
        )

        return {"output": output.tolist()}

    except Exception as e:
        monitor.log_error(request_id, type(e).__name__, str(e))
        raise HTTPException(status_code=500, detail=str(e))
```

### Error Handling

```python
import logging
from functools import wraps
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelInferenceError(Exception):
    """Base exception for model inference errors."""
    pass

class ModelLoadError(ModelInferenceError):
    """Exception raised when model fails to load."""
    pass

class InputValidationError(ModelInferenceError):
    """Exception raised when input validation fails."""
    pass

def handle_inference_errors(func):
    """Decorator for handling inference errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ModelLoadError as e:
            logger.error(f"Model load error: {e}")
            raise
        except InputValidationError as e:
            logger.warning(f"Input validation error: {e}")
            raise
        except torch.cuda.OutOfMemoryError:
            logger.error("CUDA out of memory")
            raise ModelInferenceError("GPU memory exhausted")
        except Exception as e:
            logger.error(f"Unexpected error during inference: {e}")
            raise ModelInferenceError(f"Inference failed: {str(e)}")
    return wrapper

class SafeModelWrapper:
    """Wrapper for safe model inference with error handling."""
    def __init__(self, model_path, device="cuda"):
        self.model_path = model_path
        self.device = device
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load model with error handling."""
        try:
            self.model = torch.load(self.model_path, map_location=self.device)
            self.model.eval()
            logger.info(f"Model loaded successfully from {self.model_path}")
        except FileNotFoundError:
            raise ModelLoadError(f"Model file not found: {self.model_path}")
        except Exception as e:
            raise ModelLoadError(f"Failed to load model: {str(e)}")

    @handle_inference_errors
    def predict(self, input_data):
        """Safe prediction with error handling."""
        if not isinstance(input_data, torch.Tensor):
            raise InputValidationError("Input must be a torch.Tensor")

        if input_data.dim() != 4:
            raise InputValidationError(f"Expected 4D input, got {input_data.dim()}D")

        with torch.no_grad():
            output = self.model(input_data.to(self.device))

        return output.cpu()

    def get_model_info(self):
        """Get model information."""
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)

        return {
            "model_path": self.model_path,
            "device": str(self.device),
            "total_parameters": total_params,
            "trainable_parameters": trainable_params
        }
```

### Performance Benchmarking

```python
import time
import torch
import numpy as np
from typing import List, Dict
import json

class ModelBenchmark:
    def __init__(self, model, input_shape, warmup_runs=10, benchmark_runs=100):
        self.model = model
        self.model.eval()
        self.input_shape = input_shape
        self.warmup_runs = warmup_runs
        self.benchmark_runs = benchmark_runs
        self.device = next(model.parameters()).device

    def _generate_input(self, batch_size=1):
        """Generate random input for benchmarking."""
        return torch.randn(batch_size, *self.input_shape, device=self.device)

    def benchmark_latency(self, batch_sizes: List[int] = [1, 8, 16, 32]):
        """Benchmark inference latency for different batch sizes."""
        results = {}

        for batch_size in batch_sizes:
            # Warmup
            for _ in range(self.warmup_runs):
                input_data = self._generate_input(batch_size)
                with torch.no_grad():
                    _ = self.model(input_data)

            # Benchmark
            latencies = []
            for _ in range(self.benchmark_runs):
                input_data = self._generate_input(batch_size)

                torch.cuda.synchronize() if self.device.type == 'cuda' else None
                start_time = time.perf_counter()

                with torch.no_grad():
                    _ = self.model(input_data)

                torch.cuda.synchronize() if self.device.type == 'cuda' else None
                end_time = time.perf_counter()

                latencies.append((end_time - start_time) * 1000)  # Convert to ms

            results[batch_size] = {
                "mean_ms": np.mean(latencies),
                "std_ms": np.std(latencies),
                "min_ms": np.min(latencies),
                "max_ms": np.max(latencies),
                "p50_ms": np.percentile(latencies, 50),
                "p95_ms": np.percentile(latencies, 95),
                "p99_ms": np.percentile(latencies, 99)
            }

        return results

    def benchmark_throughput(self, duration_seconds=30):
        """Benchmark throughput over a duration."""
        input_data = self._generate_input(1)

        start_time = time.time()
        predictions = 0

        while (time.time() - start_time) < duration_seconds:
            with torch.no_grad():
                _ = self.model(input_data)
            predictions += 1

        elapsed = time.time() - start_time
        throughput = predictions / elapsed

        return {
            "duration_seconds": elapsed,
            "total_predictions": predictions,
            "throughput_per_second": throughput
        }

    def benchmark_memory(self, batch_sizes: List[int] = [1, 8, 16, 32]):
        """Benchmark GPU memory usage."""
        if self.device.type != 'cuda':
            return {"error": "GPU memory benchmarking requires CUDA"}

        results = {}
        torch.cuda.reset_peak_memory_stats()

        for batch_size in batch_sizes:
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()

            input_data = self._generate_input(batch_size)

            with torch.no_grad():
                _ = self.model(input_data)

            results[batch_size] = {
                "allocated_mb": torch.cuda.max_memory_allocated() / 1024 / 1024,
                "reserved_mb": torch.cuda.max_memory_reserved() / 1024 / 1024
            }

        return results

    def run_full_benchmark(self):
        """Run comprehensive benchmark."""
        print("Running Model Benchmark...")
        print("=" * 50)

        # Latency benchmark
        print("\n1. Latency Benchmark:")
        latency_results = self.benchmark_latency()
        for batch_size, metrics in latency_results.items():
            print(f"  Batch {batch_size}: {metrics['mean_ms']:.2f}ms (p95: {metrics['p95_ms']:.2f}ms)")

        # Throughput benchmark
        print("\n2. Throughput Benchmark:")
        throughput_results = self.benchmark_throughput()
        print(f"  {throughput_results['throughput_per_second']:.2f} predictions/second")

        # Memory benchmark
        print("\n3. Memory Benchmark:")
        memory_results = self.benchmark_memory()
        for batch_size, metrics in memory_results.items():
            print(f"  Batch {batch_size}: {metrics['allocated_mb']:.2f} MB allocated")

        # Model info
        print("\n4. Model Info:")
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"  Total parameters: {total_params:,}")

        return {
            "latency": latency_results,
            "throughput": throughput_results,
            "memory": memory_results,
            "parameters": total_params
        }

# Usage
model = load_model()
benchmark = ModelBenchmark(model, input_shape=(3, 224, 224))
results = benchmark.run_full_benchmark()

# Save results
with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Best Practices

### Pre-Deployment Checklist

- **Model Export**
  - Model exported to production format (TorchScript/ONNX)
  - Exported model tested and verified
  - Model size optimized (quantization/pruning)

- **Performance**
  - Inference latency meets SLA (< 100ms for real-time)
  - Throughput tested with expected load
  - GPU memory usage optimized
  - Batch processing configured

- **Reliability**
  - Error handling implemented
  - Graceful degradation for failures
  - Circuit breaker pattern for external dependencies
  - Retry logic for transient failures

- **Monitoring**
  - Metrics collection (latency, throughput, errors)
  - Logging configured
  - Health check endpoint
  - Alert thresholds set

- **Security**
  - Input validation implemented
  - Rate limiting configured
  - Authentication/authorization for API
  - Model files stored securely

- **Deployment**
  - Docker container created
  - Environment variables configured
  - CI/CD pipeline set up
  - Blue-green deployment strategy

### Post-Deployment Checklist

- **Validation**
  - Smoke tests passed
  - A/B test started
  - Model performance monitored
  - Error rates within acceptable range

- **Documentation**
  - API documentation updated
  - Model version documented
  - Known issues documented
  - Runbook created

### Performance Optimization Tips

1. **Use TorchScript for Production**
   - Export models to TorchScript for faster inference
   - Use tracing for models without control flow
   - Use scripting for models with dynamic control flow

2. **Apply Quantization**
   - Use dynamic quantization for quick deployment
   - Use static quantization for better performance
   - Use QAT for minimal accuracy loss

3. **Optimize Batch Size**
   - Find optimal batch size for your hardware
   - Use larger batches for better GPU utilization
   - Consider latency requirements when choosing batch size

4. **Use Mixed Precision**
   - Enable FP16 for faster computation
   - Use GradScaler for training stability
   - Test accuracy impact before deployment

5. **Monitor Model Performance**
   - Track latency, throughput, and error rates
   - Set up alerts for performance degradation
   - Monitor GPU memory usage
   - Track prediction drift

## Related Skills

- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`05-ai-ml-core/model-optimization`](05-ai-ml-core/model-optimization/SKILL.md)
- [`05-ai-ml-core/model-versioning`](05-ai-ml-core/model-versioning/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
- [`15-devops-infrastructure/ci-cd-pipelines`](15-devops-infrastructure/ci-cd-pipelines/SKILL.md)
