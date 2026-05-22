---
name: unsloth-lora
description: Configuring and optimizing 16-bit Low-Rank Adaptation (LoRA) and Rank-Stabilized LoRA (rsLoRA) for efficient LLM fine-tuning using triggers like lora, qlora, rslora, rank selection, lora_alpha, lora_dropout, and target_modules.
---

## Overview
Unsloth optimizes Low-Rank Adaptation (LoRA) by providing 16-bit trainable matrices that allow for efficient fine-tuning without updating all model weights. It supports standard LoRA and Rank-Stabilized LoRA (rsLoRA), utilizing specialized kernels to accelerate training and reduce memory overhead.

## When to Use
- When fine-tuning large language models on consumer-grade or limited GPU hardware.
- When aiming to match full fine-tuning performance with significantly lower VRAM usage.
- When specialized scaling (rsLoRA) is required for higher rank stability.

## Decision Tree
1. Need to update all weights? 
   - Yes: Use [[unsloth-fft]].
   - No: Proceed to LoRA.
2. Using high rank (r > 64)? 
   - Yes: Enable `use_rslora = True` for sqrt(r) scaling.
   - No: Use standard LoRA.
3. Maximizing speed? 
   - Yes: Set `lora_dropout = 0` to enable internal kernel optimizations.

## Workflows

### Optimizing LoRA Architecture
1. Target all 7 major linear layers (q, k, v, o, gate, up, down) to match full fine-tuning performance.
2. Initialize rank (r) between 16 and 32 for general tasks, or up to 128 for complex domain adaptation.
3. Set lora_alpha equal to r or 2*r to maintain aggressive learning while ensuring numerical stability.

### Configuring Rank-Stabilized LoRA (rsLoRA)
1. Set `use_rslora = True` in `get_peft_model` to enable sqrt(r) scaling.
2. Increase rank (r) without the typical instability risks associated with high-alpha standard LoRA.
3. Monitor training loss to ensure the model captures underlying patterns without memorization.

## Non-Obvious Insights
- Setting `lora_dropout` to 0 is not just a parameter choice; it explicitly triggers internal Unsloth kernel-level optimizations that significantly speed up the training loop.
- Unsloth includes a custom gradient accumulation fix that ensures results are mathematically identical regardless of the batch size and accumulation step combination.
- For verifying weight updates, MD5 checksums or absolute difference sums are more reliable than `np.allclose()` because LoRA induces subtle Gaussian-distributed changes.

## Evidence
- "LoRA: Fine-tunes small, trainable matrices in 16-bit without updating all model weights." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "For optimal performance, LoRA should be applied to all major linear layers: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj." [Source](https://docs.unsloth.ai/basics/lora-parameters-encyclopedia)
- "Set use_rslora = True... the effective scaling becomes lora_alpha / sqrt(r) instead of the standard lora_alpha / r." [Source](https://docs.unsloth.ai/basics/lora-parameters-encyclopedia)

## Scripts
- `scripts/unsloth-lora_tool.py`: Python utility for configuring LoRA parameters in the Unsloth framework.
- `scripts/unsloth-lora_tool.js`: JavaScript helper for generating LoRA configuration objects.

## Dependencies
- unsloth
- torch
- peft
- bitsandbytes

## References
- [[references/README.md]]