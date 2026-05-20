---
name: edge-and-mobile-ml
description: "Use when deploying ML models to edge devices, mobile, or browser. Covers ONNX export, CoreML conversion, TensorRT optimization, quantization (PTQ/QAT), and model profiling."
---

# Edge and Mobile ML

## Export Format Selection

| Format | Target | From | Strengths |
|--------|--------|------|-----------|
| **ONNX** | Cross-platform, server, edge | PyTorch, TF, JAX | Universal interchange, wide runtime support |
| **CoreML** | iOS, macOS, Apple Silicon | PyTorch (via coremltools) | Neural Engine acceleration, on-device privacy |
| **TensorRT** | NVIDIA GPUs | ONNX, PyTorch | Fastest GPU inference, kernel fusion |
| **TFLite** | Android, microcontrollers | TensorFlow | Small runtime, NNAPI/GPU delegate |
| **ONNX Runtime Web** | Browser (WASM/WebGPU) | ONNX | No server needed, client-side inference |
| **ExecuTorch** | iOS, Android | PyTorch | PyTorch-native mobile, replaces TorchScript |

**Decision rule**: ONNX for cross-platform or server deployment. CoreML for Apple ecosystem. TensorRT when you need maximum throughput on NVIDIA hardware. TFLite for Android/microcontrollers. ExecuTorch if you want to stay fully in PyTorch ecosystem for mobile.

## ONNX Export from PyTorch

```python
import torch
import torch.onnx

model = MyModel()
model.eval()

# Create dummy input matching your model's expected shape
dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["image"],
    output_names=["logits"],
    dynamic_axes={
        "image": {0: "batch_size"},
        "logits": {0: "batch_size"},
    },
    opset_version=17,
)
```

### Verify and Optimize

```python
import onnx
from onnxruntime import InferenceSession
import numpy as np

# Verify
onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)

# Test inference matches PyTorch
session = InferenceSession("model.onnx")
ort_input = {"image": dummy_input.numpy()}
ort_output = session.run(None, ort_input)[0]

torch_output = model(dummy_input).detach().numpy()
np.testing.assert_allclose(torch_output, ort_output, rtol=1e-3, atol=1e-5)
print("Outputs match!")
```

### ONNX Graph Optimization

```python
import onnxruntime as ort

# Session-level optimization
options = ort.SessionOptions()
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
options.optimized_model_filepath = "model_optimized.onnx"

session = ort.InferenceSession("model.onnx", options)
```

## CoreML Conversion

```python
import coremltools as ct
import torch

model = MyModel()
model.eval()

# Trace the model
traced = torch.jit.trace(model, torch.randn(1, 3, 224, 224))

# Convert to CoreML
mlmodel = ct.convert(
    traced,
    inputs=[ct.ImageType(name="image", shape=(1, 3, 224, 224), scale=1/255.0, bias=[0, 0, 0])],
    outputs=[ct.TensorType(name="logits")],
    compute_units=ct.ComputeUnit.ALL,  # CPU + GPU + Neural Engine
    minimum_deployment_target=ct.target.iOS16,
)

mlmodel.save("model.mlpackage")
```

### Adding Metadata

```python
mlmodel.author = "Your Name"
mlmodel.short_description = "Image classification model"
mlmodel.input_description["image"] = "Input image (224x224 RGB)"
mlmodel.output_description["logits"] = "Class logits (1000 classes)"
```

### CoreML Performance Tips
- Use `compute_units=ct.ComputeUnit.ALL` to leverage Neural Engine
- Float16 is default on Neural Engine and sufficient for most tasks
- Use `ct.ImageType` for image inputs to avoid manual preprocessing on device
- Test on actual hardware; simulator performance differs significantly

## TensorRT Optimization

```python
import tensorrt as trt
import numpy as np

logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, logger)

# Parse ONNX model
with open("model.onnx", "rb") as f:
    if not parser.parse(f.read()):
        for i in range(parser.num_errors):
            print(parser.get_error(i))
        raise RuntimeError("ONNX parse failed")

# Configure builder
config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1 GB

# Enable FP16
config.set_flag(trt.BuilderFlag.FP16)

# Build engine
engine_bytes = builder.build_serialized_network(network, config)
with open("model.engine", "wb") as f:
    f.write(engine_bytes)
```

### Dynamic Shapes with TensorRT

```python
profile = builder.create_optimization_profile()
profile.set_shape("image",
    min=(1, 3, 224, 224),
    opt=(8, 3, 224, 224),    # Optimal batch size
    max=(32, 3, 224, 224),
)
config.add_optimization_profile(profile)
```

### torch-tensorrt (Simpler Path)

```python
import torch_tensorrt

model = MyModel().eval().cuda()
inputs = [torch_tensorrt.Input(
    min_shape=[1, 3, 224, 224],
    opt_shape=[8, 3, 224, 224],
    max_shape=[32, 3, 224, 224],
    dtype=torch.float16,
)]

trt_model = torch_tensorrt.compile(
    model,
    inputs=inputs,
    enabled_precisions={torch.float16},
)

# Use like a normal PyTorch model
output = trt_model(input_tensor.half().cuda())
```

## Quantization

### Post-Training Quantization (PTQ)

No retraining needed. Apply after training is complete.

```python
import torch
from torch.ao.quantization import get_default_qconfig, prepare, convert

model = MyModel()
model.eval()

# Static quantization (requires calibration data)
model.qconfig = get_default_qconfig("x86")  # or "qnnpack" for ARM
prepared = prepare(model)

# Calibrate with representative data
with torch.no_grad():
    for batch in calibration_loader:
        prepared(batch)

quantized_model = convert(prepared)

# Check size reduction
torch.save(quantized_model.state_dict(), "model_quantized.pt")
```

### ONNX Runtime PTQ

```python
from onnxruntime.quantization import quantize_dynamic, quantize_static, QuantType, CalibrationDataReader

# Dynamic quantization (no calibration needed, weights only)
quantize_dynamic(
    "model.onnx",
    "model_int8_dynamic.onnx",
    weight_type=QuantType.QInt8,
)

# Static quantization (needs calibration)
class MyCalibrationReader(CalibrationDataReader):
    def __init__(self, data_loader):
        self.data_iter = iter(data_loader)

    def get_next(self):
        try:
            batch = next(self.data_iter)
            return {"image": batch.numpy()}
        except StopIteration:
            return None

quantize_static(
    "model.onnx",
    "model_int8_static.onnx",
    calibration_data_reader=MyCalibrationReader(cal_loader),
    quant_format=QuantFormat.QDQ,  # Preferred for TensorRT compatibility
)
```

### Quantization-Aware Training (QAT)

Higher accuracy than PTQ but requires retraining.

```python
import torch
from torch.ao.quantization import get_default_qat_qconfig, prepare_qat, convert

model = MyModel()
model.train()

model.qconfig = get_default_qat_qconfig("x86")
prepared = prepare_qat(model)

# Fine-tune with fake quantization nodes
optimizer = torch.optim.Adam(prepared.parameters(), lr=1e-5)
for epoch in range(3):
    for batch, targets in train_loader:
        output = prepared(batch)
        loss = criterion(output, targets)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

# Convert to actual quantized model
prepared.eval()
quantized = convert(prepared)
```

### Quantization Tradeoffs

| Method | Accuracy Drop | Size Reduction | Speed Gain | Effort |
|--------|--------------|----------------|------------|--------|
| **FP16** | < 0.1% | 2x | 1.5-2x (GPU) | Trivial |
| **Dynamic INT8** | 0.5-1% | 2-4x | 1.5-3x (CPU) | Low |
| **Static INT8 (PTQ)** | 1-2% | 3-4x | 2-4x | Medium |
| **QAT INT8** | < 0.5% | 3-4x | 2-4x | High |
| **INT4 (GPTQ/AWQ)** | 1-3% | 4-8x | 2-4x | Medium |

## Model Profiling and Benchmarking

```python
import time
import torch
import numpy as np

def benchmark_pytorch(model, input_shape, device="cuda", n_warmup=10, n_runs=100):
    model.eval().to(device)
    x = torch.randn(*input_shape, device=device)

    # Warmup
    for _ in range(n_warmup):
        with torch.no_grad():
            model(x)
    if device == "cuda":
        torch.cuda.synchronize()

    # Benchmark
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        with torch.no_grad():
            model(x)
        if device == "cuda":
            torch.cuda.synchronize()
        times.append(time.perf_counter() - start)

    times = np.array(times) * 1000  # ms
    print(f"Latency: {np.mean(times):.2f} +/- {np.std(times):.2f} ms")
    print(f"P50: {np.percentile(times, 50):.2f} ms, P99: {np.percentile(times, 99):.2f} ms")
    print(f"Throughput: {1000 / np.mean(times):.1f} inferences/sec")
    return times

def benchmark_onnx(model_path, input_dict, n_warmup=10, n_runs=100):
    import onnxruntime as ort
    session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])

    for _ in range(n_warmup):
        session.run(None, input_dict)

    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        session.run(None, input_dict)
        times.append(time.perf_counter() - start)

    times = np.array(times) * 1000
    print(f"ONNX Latency: {np.mean(times):.2f} +/- {np.std(times):.2f} ms")
    return times
```

### Model Size Analysis

```python
def model_size_mb(model):
    param_size = sum(p.numel() * p.element_size() for p in model.parameters())
    buffer_size = sum(b.numel() * b.element_size() for b in model.buffers())
    total = (param_size + buffer_size) / (1024 ** 2)
    print(f"Parameters: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
    print(f"Size: {total:.1f} MB")
    return total
```

## Browser ML

### ONNX Runtime Web

```javascript
import * as ort from "onnxruntime-web";

// Use WebGPU if available, fall back to WASM
ort.env.wasm.numThreads = 4;

const session = await ort.InferenceSession.create("model.onnx", {
  executionProviders: ["webgpu", "wasm"],
});

const inputTensor = new ort.Tensor("float32", floatArray, [1, 3, 224, 224]);
const results = await session.run({ image: inputTensor });
const logits = results.logits.data; // Float32Array
```

### Transformers.js

```javascript
import { pipeline } from "@xenova/transformers";

// Models are automatically downloaded and cached
const classifier = await pipeline("sentiment-analysis");
const result = await classifier("I love this product!");
// [{ label: "POSITIVE", score: 0.9998 }]

// Text embeddings
const embedder = await pipeline("feature-extraction", "Xenova/all-MiniLM-L6-v2");
const embedding = await embedder("Hello world", { pooling: "mean", normalize: true });
```

## Gotchas

### ONNX Dynamic Axes
Always specify `dynamic_axes` for batch dimension. Without it, the exported model has fixed batch size, breaking batched inference.

### ONNX Opset Version
Use opset 17+ for modern ops. Lower opsets lack support for newer attention patterns, grouped convolutions, etc. Check `torch.onnx.is_onnx_export()` for export-time branching.

### CoreML vs Simulator
CoreML models behave differently on simulator vs real hardware. Always test on device. Neural Engine is not available in simulator.

### TensorRT Engine Portability
TensorRT engines are GPU-specific. An engine built on A100 won't run on T4. Rebuild for each target GPU. Ship ONNX + build script, not the engine file.

### Quantization Sensitive Layers
Not all layers quantize well. Attention layers and the first/last conv layers are sensitive. Use mixed-precision: keep sensitive layers in FP16, quantize the rest to INT8.

### Mobile Memory Constraints
iOS hard-kills apps exceeding ~1.5 GB RAM. Android varies by device. Profile peak memory during inference, not just model size. Use streaming/chunked inference for large models.

### Browser Model Loading
ONNX models in the browser must be downloaded by the user. Compress models aggressively (INT8 + gzip). Consider splitting into chunks for progressive loading. Cache with IndexedDB.
