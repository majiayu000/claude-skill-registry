---
name: unsloth-models
description: Guidance on selecting and configuring supported model architectures like Llama 4, DeepSeek-R1, and Qwen3. Triggers: llama 4, deepseek-r1, qwen3, gemma 3, model selection, instruct vs base.
---

## Overview
Unsloth supports a wide range of state-of-the-art model architectures, providing pre-quantized Hub variants and optimized kernels for models like Llama 4, DeepSeek-R1, and Qwen3. Selecting the right variant (Instruct vs Base) is critical for training success.

## When to Use
- When starting a new fine-tuning project and deciding on a base architecture.
- When utilizing reasoning-heavy models (DeepSeek-R1) on consumer hardware.
- When performing continued pre-training on domain-specific data.

## Decision Tree
1. Is the task conversational or instruction-following?
   - Yes: Use 'Instruct' variants.
2. Is the task raw knowledge injection or domain pre-training?
   - Yes: Use 'Base' variants.
3. Is reasoning/logic a priority?
   - Yes: Select DeepSeek-R1 Distills or similar architectures.

## Workflows

### Selecting the Right Model
1. Use 'Instruct' models for conversational tasks or when data is limited.
2. Use 'Base' models for domain-specific knowledge injection or raw text pre-training.
3. Select 'unsloth-bnb-4bit' variants to leverage pre-calculated quantization statistics.

### Fine-tuning DeepSeek-R1 Distills
1. Load the specific distilled variant (e.g., Llama-8B).
2. Use datasets including reasoning paths (Chain of Thought) to preserve logic capabilities.
3. Apply optimized Llama 3.1 kernels during the SFT or DPO pipeline.

## Non-Obvious Insights
- Unsloth releases specialized 'distilled' versions of heavy reasoning models (like DeepSeek-R1) that are specifically optimized to fit on consumer hardware while retaining logic performance.
- Choosing the 'unsloth-bnb-4bit' variants on the Hub is not just about speed; these variants include critical tokenizer fixes and pre-calculated quantization statistics that ensure better training stability.
- New reasoning models can be trained from scratch or fine-tuned using GRPO (Group Relative Policy Optimization) natively within the Unsloth framework, bypassing the need for complex PPO setups.

## Evidence
- "Llama 4 by Meta, including Scout & Maverick are now supported." [Source](https://github.com/unslothai/unsloth)
- "Instruct versions are used for inference or fine-tuning, while Base models are usually used for continued pre-training." [Source](https://docs.unsloth.ai/get-started/all-our-models)

## Scripts
- `scripts/unsloth-models_tool.py`: Script to list and download recommended Unsloth-optimized models.
- `scripts/unsloth-models_tool.js`: Comparison helper for model parameter sizes.

## Dependencies
- unsloth
- huggingface_hub

## References
- [[references/README.md]]