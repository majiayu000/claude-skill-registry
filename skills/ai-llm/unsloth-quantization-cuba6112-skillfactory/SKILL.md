---
name: unsloth-quantization
description: Utilizing Dynamic 4-bit quantization, FP8 training, and 8-bit optimizers to minimize VRAM usage without sacrificing accuracy. Triggers: quantization, dynamic 4-bit, fp8, bitsandbytes, adamw_8bit, qat.
---

## Overview
Unsloth utilizes advanced quantization techniques to reduce the memory footprint of LLM fine-tuning. This includes "Dynamic 4-bit" loading (protecting sensitive layers), FP8 training for modern GPUs, and the use of 8-bit optimizers to save gigabytes of VRAM.

## When to Use
- When training on GPUs with limited VRAM (e.g., 8GB, 12GB, or 16GB).
- When aiming for the fastest possible training speeds on H100 or RTX 40 series GPUs.
- When trying to balance model size and reasoning performance.

## Decision Tree
1. Is your GPU RTX 40 series or newer (Ada/Hopper)?
   - Yes: Use FP8 Dynamic for 2x faster training.
   - No: Use BF16/FP16.
2. Running out of VRAM?
   - Yes: Ensure `load_in_4bit=True` and use `adamw_8bit` optimizer.
3. Is accuracy dropping significantly?
   - Yes: Use "Dynamic" variants that protect the first and last layers.

## Workflows

### FP8 Training Configuration
1. Select a model variant ending in '-FP8-Dynamic'.
2. Configure the trainer to use the FP8 backend (available for H100 and Ada Lovelace architectures).
3. Verify speedup, which typically reaches 2x compared to standard BF16.

### VRAM-Constrained Training Setup
1. Set `load_in_4bit=True` and `use_gradient_checkpointing='unsloth'`.
2. Apply 'adamw_8bit' optimizer in `TrainingArguments`.
3. Set `per_device_train_batch_size` to 1 and maximize `gradient_accumulation_steps`.

## Non-Obvious Insights
- Unsloth's "Dynamic 4-bit" (unsloth-bnb-4bit) differs from standard BNB 4-bit by protecting the first and last layers, which are critical for reasoning and output quality.
- Quantization-Aware Training (QAT) is implicitly supported through Unsloth's specialized kernels, allowing the model to adapt to the lower precision during the LoRA update process.
- Switching to the `adamw_8bit` optimizer can save up to 2GB of VRAM on optimizer states alone for a 7B parameter model.

## Evidence
- "load_in_4bit = True – Enables 4-bit quantization, reducing memory use 4× for fine-tuning." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "FP8 Dynamic offers slightly faster training and lower VRAM usage than FP8 Block." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-quantization_tool.py`: Script to check GPU compatibility and suggest quantization settings.
- `scripts/unsloth-quantization_tool.js`: Memory usage estimator for different quantization levels.

## Dependencies
- unsloth
- bitsandbytes
- torch

## References
- [[references/README.md]]