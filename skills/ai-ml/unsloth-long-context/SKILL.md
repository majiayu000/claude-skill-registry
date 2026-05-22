---
name: unsloth-long-context
description: Training models on extended context lengths using optimized RoPE scaling and memory-efficient attention kernels. Triggers: long context, max_seq_length, rope scaling, large context window, flex attention.
---

## Overview
Unsloth enables training on extreme context lengths (up to 89K+ on a single 80GB GPU) by utilizing manually derived Triton kernels for RoPE and attention. It optimizes memory usage by a further 30% compared to Flash Attention 2, allowing for 4x longer context windows.

## When to Use
- When training on long documents, codebases, or books.
- When building models that require large retrieval windows or multi-document reasoning.
- When standard Flash Attention 2 results in OOM errors on long sequences.

## Decision Tree
1. Is context > 32K?
   - Yes: Set `use_gradient_checkpointing = 'unsloth'` (mandatory for stability).
2. Are you seeing quality degradation on long context?
   - Yes: Ensure your dataset includes samples with long-range dependencies and adjust RoPE base frequency.
3. Using A100/H100 80GB?
   - Yes: You can push context lengths toward 89K tiers.

## Workflows

### Setting Up Extreme Context Training
1. Load model with high `max_seq_length` (e.g., 65536+).
2. Ensure `use_gradient_checkpointing='unsloth'` is passed to `get_peft_model`.
3. Use high-VRAM GPUs (A100/H100 80GB) to enable the highest context tiers.

### RoPE Scaling Configuration
1. Set `max_seq_length` in `from_pretrained`; Unsloth automatically adjusts the base frequency internally.
2. Include samples with long dependencies in the dataset to prevent performance degradation.
3. Increase batch size or accumulation to ensure sufficient tokens per step for stable long-range learning.

## Non-Obvious Insights
- Unsloth's performance in long context comes from custom Triton kernels that handle RoPE scaling more efficiently than standard libraries, allowing for 13x longer context than the HF+FA2 combination.
- The 'unsloth' gradient checkpointing mode is not optional for long contexts; it is mandatory for sequences exceeding 32K to prevent activation memory from crashing the system.
- Flex Attention is an experimental feature in Unsloth that allows training massive models (like 120B) on reduced VRAM by optimizing the attention patterns specifically for memory efficiency.

## Evidence
- "Unsloth supports 89K context for Meta's Llama 3.3 (70B) on a 80GB GPU - 13x longer than HF+FA2." [Source](https://github.com/unslothai/unsloth)
- "We cut memory usage by a further 30% and now support 4x longer context windows!" [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-long-context_tool.py`: Script to initialize models with specific RoPE and context length settings.
- `scripts/unsloth-long-context_tool.js`: Utility to calculate token counts for long documents.

## Dependencies
- unsloth
- triton
- torch

## References
- [[references/README.md]]