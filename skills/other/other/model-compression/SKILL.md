---
name: model-compression
description: Pruning, knowledge distillation, quantization-aware training, and edge deployment patterns for reducing model size and latency.
---

# Model Compression

## When to Use

Compress models when deploying to resource-constrained environments (mobile, edge, embedded), reducing serving costs, or meeting latency SLAs that the full model cannot hit.

## Technique Selection

### Decision Table: Compression Technique by Constraint

| Primary Constraint | Technique | Typical Compression | Accuracy Drop | Implementation Effort |
|-------------------|-----------|-------------------|---------------|----------------------|
| Memory (model size) | Quantization (PTQ INT8) | 2-4x | 0.1-1% | Low |
| Memory (extreme) | Quantization (INT4/GPTQ) | 4-8x | 1-5% | Medium |
| Latency (structured) | Structured pruning | 1.5-3x speedup | 1-5% | Medium |
| Latency + memory | Distillation | 2-10x smaller | 1-10% | High |
| Latency (hardware-specific) | QAT + target runtime | 2-4x speedup | 0.5-2% | High |
| All constraints (extreme) | Pruning + distillation + quantization | 10-50x | 3-15% | Very High |

### Decision Table: When to Use Each Pruning Approach

| Scenario | Pruning Type | Granularity | Speedup Without Sparse Hardware |
|----------|-------------|-------------|-------------------------------|
| General size reduction | Unstructured | Weight-level | None (need sparse kernels) |
| Actual inference speedup | Structured | Channel/head/layer | Yes |
| Transformer attention heads | Structured | Head-level | Yes |
| Conv-heavy vision models | Structured | Filter-level | Yes |
| NLP with hardware support | Semi-structured (2:4) | Block pattern | Yes (Ampere+ GPUs) |

## Structured Pruning

### Channel Pruning by L1 Norm

```python
import torch
import torch.nn as nn
import torch.nn.utils.prune as prune

def prune_conv_channels(model, amount=0.3):
    """Prune conv2d filters by L1 norm (structured)."""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            prune.ln_structured(module, name="weight", amount=amount, n=1, dim=0)
            prune.remove(module, "weight")  # Make pruning permanent
    return model

def prune_transformer_heads(model, heads_to_prune):
    """Prune attention heads from a transformer.

    Args:
        heads_to_prune: dict of {layer_idx: [head_indices]}
            e.g., {0: [0, 3], 2: [1, 5, 7]}
    """
    for layer_idx, heads in heads_to_prune.items():
        layer = model.encoder.layer[layer_idx]
        attention = layer.attention.self

        num_heads = attention.num_attention_heads
        head_size = attention.attention_head_size

        # Build index of heads to keep
        keep_heads = sorted(set(range(num_heads)) - set(heads))
        keep_indices = torch.cat([
            torch.arange(h * head_size, (h + 1) * head_size) for h in keep_heads
        ])

        # Slice query, key, value projections
        for proj in [attention.query, attention.key, attention.value]:
            proj.weight = nn.Parameter(proj.weight.index_select(0, keep_indices))
            proj.bias = nn.Parameter(proj.bias.index_select(0, keep_indices))

        # Update output projection
        attention.output.dense.weight = nn.Parameter(
            attention.output.dense.weight.index_select(1, keep_indices)
        )
        attention.num_attention_heads = len(keep_heads)
        attention.all_head_size = len(keep_heads) * head_size

    return model
```

## Knowledge Distillation

### Training Loop

```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, labels, temperature=4.0, alpha=0.5):
    """Combined hard-label and soft-label distillation loss."""
    hard_loss = F.cross_entropy(student_logits, labels)
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=-1),
        F.softmax(teacher_logits / temperature, dim=-1),
        reduction="batchmean",
    ) * (temperature ** 2)
    return alpha * soft_loss + (1 - alpha) * hard_loss

def train_distillation(teacher, student, train_loader, optimizer, epochs=10, device="cuda"):
    """Standard distillation training loop."""
    teacher.eval().to(device)
    student.train().to(device)

    for epoch in range(epochs):
        total_loss = 0
        for batch in train_loader:
            inputs = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            with torch.no_grad():
                teacher_out = teacher(inputs, attention_mask=attention_mask)

            student_out = student(inputs, attention_mask=attention_mask)

            loss = distillation_loss(
                student_logits=student_out.logits,
                teacher_logits=teacher_out.logits,
                labels=labels,
                temperature=4.0,
                alpha=0.7,
            )

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(student.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss / len(train_loader):.4f}")
```

## Quantization-Aware Training (QAT)

### PyTorch QAT Pipeline

```python
import torch.quantization as quant

def setup_qat(model, backend="x86"):
    """Prepare model for quantization-aware training."""
    model.train()
    model.qconfig = quant.get_default_qat_qconfig(backend)

    # Fuse common patterns before QAT
    fuse_modules = []
    for name, module in model.named_modules():
        if isinstance(module, nn.Sequential):
            children = list(module.named_children())
            for i in range(len(children) - 1):
                n1, m1 = children[i]
                n2, m2 = children[i + 1]
                if isinstance(m1, nn.Conv2d) and isinstance(m2, nn.BatchNorm2d):
                    fuse_modules.append([f"{name}.{n1}", f"{name}.{n2}"])

    if fuse_modules:
        torch.quantization.fuse_modules(model, fuse_modules, inplace=True)

    quant.prepare_qat(model, inplace=True)
    return model

def convert_and_export(model, sample_input, output_path="model_quantized.pt"):
    """Convert QAT model to quantized and export."""
    model.eval()
    quantized = quant.convert(model.cpu(), inplace=False)
    traced = torch.jit.trace(quantized, sample_input.cpu())
    traced.save(output_path)
    return quantized
```

## ONNX Export for Edge

```python
import torch
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

def export_to_onnx(model, sample_input, path="model.onnx", opset=17):
    """Export PyTorch model to ONNX format."""
    model.eval()
    torch.onnx.export(
        model,
        sample_input,
        path,
        opset_version=opset,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    )
    # Validate
    onnx_model = onnx.load(path)
    onnx.checker.check_model(onnx_model)
    return path

def quantize_onnx_dynamic(input_path, output_path="model_quant.onnx"):
    """Apply dynamic INT8 quantization to ONNX model."""
    quantize_dynamic(
        input_path,
        output_path,
        weight_type=QuantType.QInt8,
    )
    return output_path
```

## Gotchas and Anti-Patterns

### Accuracy Recovery After Pruning
Pruning then fine-tuning often recovers accuracy, but only if you fine-tune long enough. Rule of thumb: fine-tune for 20-30% of original training budget. Pruning >50% of parameters without iterative pruning+retraining cycles causes permanent accuracy loss.

### Teacher-Student Capacity Gap
If the student is too small relative to the teacher, distillation underperforms training from scratch. A 12-layer teacher distilling to a 2-layer student loses too much. **Mitigation**: use progressive distillation (12 -> 6 -> 3) or intermediate layer matching (hint-based distillation).

### Calibration Data Selection
Post-training quantization (PTQ) quality depends heavily on calibration data. Using 100 random samples from training set is usually sufficient, but the samples must be representative of inference distribution. Skewed calibration data causes activation range miscalibration, leading to outsized accuracy drops on underrepresented inputs.

### Hardware-Specific Quantization Pitfalls
INT8 on ARM (via XNNPACK) behaves differently from INT8 on x86 (via FBGEMM). Always profile on the target device. Symmetric vs. asymmetric quantization, per-tensor vs. per-channel -- these choices are hardware-dependent. ONNX Runtime, TensorRT, and Core ML each have different operator support for quantized ops.

### Structured vs. Unstructured Pruning Mismatch
Unstructured pruning (zeroing individual weights) shows great sparsity numbers but provides zero speedup on standard hardware without sparse kernel support. Only structured pruning (removing entire channels/heads/layers) gives wall-clock speedup on commodity GPUs and CPUs.

### Layer Sensitivity
Not all layers tolerate equal compression. First and last layers in vision models, embedding layers in transformers -- these are typically more sensitive. Profile per-layer sensitivity before applying uniform compression ratios. A 10-minute sensitivity scan saves days of failed experiments.

