---
name: pytorch-onnx
description: Exporting PyTorch models to ONNX format for cross-platform deployment. Includes handling dynamic axes, graph optimization in ONNX Runtime, and INT8 model quantization. (onnx, onnxruntime, torch.onnx.export, dynamic_axes, constant-folding, edge-deployment)
---

## Overview

ONNX (Open Neural Network Exchange) is an open format built to represent machine learning models. Exporting PyTorch models to ONNX allows them to be executed in environments without Python or PyTorch, using high-performance engines like ONNX Runtime.

## When to Use

Use ONNX for cross-language deployment (C++, Java, C#), edge deployment (mobile/IoT), or to leverage specialized hardware accelerators (like TensorRT) that support ONNX as an input format.

## Decision Tree

1. Does your model accept variable batch sizes?
   - SPECIFY: `dynamic_axes` in the `torch.onnx.export` call.
2. Do you need the fastest possible inference on a CPU?
   - APPLY: Quantization using the ONNX Runtime quantization tool.
3. Are you deploying to a C++ environment without Python?
   - EXPORT: To ONNX and load using the ONNX Runtime C++ API.

## Workflows

1. **Exporting a Model for Cross-Platform Deployment**
   1. Instantiate the PyTorch model and set it to `.eval()`.
   2. Create a dummy input tensor matching the input shape.
   3. Call `torch.onnx.export()` specifying input/output names and dynamic axes.
   4. Verify the resulting `.onnx` file using a tool like Netron.

2. **Optimizing ONNX Models for Inference**
   1. Load the `.onnx` model into an ONNX Runtime `InferenceSession`.
   2. Choose an appropriate Execution Provider (e.g., `'CUDAExecutionProvider'`, `'TensorrtExecutionProvider'`).
   3. Enable graph optimizations like constant folding and node fusion.
   4. Run inference using the `session.run()` method with input dictionaries.

3. **Reducing Model Footprint via Quantization**
   1. Export the model to standard ONNX format.
   2. Use the ONNX Runtime quantization tool to convert FP32 weights to INT8.
   3. Calibrate the model using a representative dataset to minimize accuracy loss.
   4. Deploy the quantized `.onnx` model to edge devices for lower latency.

## Non-Obvious Insights

- **Static vs. Dynamic**: By default, `torch.onnx.export` captures the shape of the dummy input as a static shape. If your application handles varying inputs, you must explicitly define these as dynamic axes.
- **Graph Optimization**: ONNX Runtime performs "constant folding," which pre-computes parts of the graph that rely on constant values, effectively stripping unnecessary computation before inference starts.
- **Serialization Choice**: While TorchScript is also an option for PyTorch deployment, ONNX is often preferred for cross-vendor compatibility (e.g., running a model on a Web browser using ONNX.js).

## Evidence

- "The first step is to export your PyTorch model to ONNX format using the PyTorch ONNX exporter: torch.onnx.export(model, PATH, example)." (https://onnxruntime.ai/docs/tutorials/accelerate-pytorch/pytorch.html)
- "ONNXRuntime applies a series of optimizations to the ONNX graph, combining nodes where possible and factoring out constant values (constant folding)." (https://onnxruntime.ai/docs/tutorials/accelerate-pytorch/pytorch.html)

## Scripts

- `scripts/pytorch-onnx_tool.py`: Script to export a model with dynamic axes support.
- `scripts/pytorch-onnx_tool.js`: Node.js interface to run inference via ONNX Runtime.

## Dependencies

- torch
- onnx
- onnxruntime

## References

- [PyTorch ONNX Reference](references/README.md)