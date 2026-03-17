---
name: pytorch-quantization
description: Techniques for model size reduction and inference acceleration using INT8 quantization, including Post-Training Quantization (PTQ) and Quantization Aware Training (QAT). (quantization, int8, qat, fbgemm, qnnpack, ptq, dequantize)
---

## Overview

Quantization converts high-precision floating point tensors (FP32) into low-precision integers (INT8). This significantly reduces model size and improves inference speed on supported hardware backends like FBGEMM (x86) and QNNPACK (ARM).

## When to Use

Use quantization when deploying models to edge devices (mobile/IoT) or when seeking to reduce cloud inference costs by using INT8-optimized CPU instances.

## Decision Tree

1. Do you have a representative calibration dataset but no time for training?
   - USE: Post-Training Quantization (PTQ).
2. Is accuracy drop unacceptable with PTQ?
   - USE: Quantization Aware Training (QAT).
3. Are you running on an ARM-based mobile device?
   - SET: `torch.backends.quantized.engine = 'qnnpack'`.

## Workflows

1. **Using a Pre-Quantized Model**
   1. Select a quantized weight enum (e.g., `ResNet50_QuantizedWeights.DEFAULT`).
   2. Instantiate the model with `quantize=True`.
   3. Set the model to `.eval()` mode.
   4. Apply the specific preprocessing transforms provided by the weights.
   5. Perform inference using INT8-optimized backends.

2. **Manual Tensor Quantization**
   1. Determine the min/max range of your float tensor.
   2. Calculate scale and zero_point for INT8 representation.
   3. Apply `torch.quantize_per_tensor()` to the float input.
   4. Perform operations on the quantized tensor and dequantize when necessary.

3. **Post-Training Quantization Preparation**
   1. Fuse modules (e.g., Conv+BN+ReLU) into single blocks to improve efficiency.
   2. Insert observers or use prepared models to collect activation statistics on a calibration dataset.
   3. Convert the model using the backend-specific engine (e.g., 'fbgemm' for server CPUs).

## Non-Obvious Insights

- **Backend Specificity**: Pre-quantized models in TorchVision are optimized for specific backends. A model quantized for FBGEMM may perform poorly on QNNPACK.
- **Per-Channel Accuracy**: Per-channel quantization is typically more accurate for weights than per-tensor quantization because it accounts for varying distributions across different output channels.
- **Learning the Error**: Quantization Aware Training (QAT) allows the model to learn and compensate for the quantization error during training, typically resulting in higher accuracy than post-training methods.

## Evidence

- "resnet50(weights=weights, quantize=True)" (https://pytorch.org/vision/stable/models.html)
- "torch.quantize_per_tensor converts a float tensor to a quantized tensor with given scale and zero point." (https://pytorch.org/docs/stable/quantization.html)

## Scripts

- `scripts/pytorch-quantization_tool.py`: Demo of manual tensor quantization and pre-quantized model loading.
- `scripts/pytorch-quantization_tool.js`: Node.js wrapper to invoke quantization conversion scripts.

## Dependencies

- torch
- torchvision

## References

- [PyTorch Quantization Reference](references/README.md)