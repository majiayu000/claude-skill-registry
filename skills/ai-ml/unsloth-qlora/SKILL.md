---
name: unsloth-qlora
description: Advanced 4-bit quantization techniques using Unsloth and BitsAndBytes for extreme VRAM efficiency (triggers: QLoRA, 4-bit, load_in_4bit, bnb-4bit, VRAM optimization, dynamic quantization).
---

## Overview
Unsloth-qlora enables the fine-tuning of large-scale models (up to 70B parameters) on consumer-grade hardware. It utilizes dynamic 4-bit quantization which selectively preserves critical weights to maintain higher accuracy than standard quantization methods.

## When to Use
- When training on limited VRAM hardware (e.g., 24GB or 48GB cards).
- When seeking to match full fine-tuning performance while using 4-bit precision.
- When accuracy loss from standard BitsAndBytes quantization is unacceptable.

## Decision Tree
1. Do you need maximum VRAM savings?
   - Yes: Set `load_in_4bit = True`.
2. Is accuracy the priority over VRAM?
   - Yes: Use LoRA (16-bit) if VRAM permits; otherwise use `unsloth-bnb-4bit` models.
3. Are you training on all layers?
   - Yes: Target `q, k, v, o, gate, up, down` modules for optimal performance.

## Workflows
1. **Setting Up QLoRA**: Load models with the `-unsloth-bnb-4bit` suffix and initialize with `load_in_4bit = True`.
2. **Optimizing Batch Size**: Use low `per_device_train_batch_size` (e.g., 2) with high `gradient_accumulation_steps` (e.g., 8) to maintain stability on low VRAM.
3. **Verifying Weight Updates**: Compare pre and post-training tensors using MD5 hashes or absolute differences instead of standard `np.allclose()`.

## Non-Obvious Insights
- Unsloth's Dynamic 4-bit quantization recovers approximately 70% of accuracy lost during standard quantization by preserving critical parameters.
- Masking out input tokens and training specifically on assistant completions can boost QLoRA accuracy by roughly 1%.
- To match full fine-tuning (FFT) performance, LoRA must be applied to all major linear layers (q, k, v, o, gate, up, down).

## Evidence
- "Unsloth dynamic 4-bit quants... consume slightly more VRAM than standard BitsAndBytes 4-bit models but offer significantly higher accuracy." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "QLoRA allows a 70B parameter model to fit in less than 48GB of VRAM." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-qlora_tool.py`: Script for 4-bit model loading and linear layer targeting.
- `scripts/unsloth-qlora_tool.js`: Node.js helper for batch size calculation.

## Dependencies
- `unsloth`
- `bitsandbytes`
- `accelerate`

## References
- [references/README.md](references/README.md)