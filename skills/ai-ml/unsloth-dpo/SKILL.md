---
name: unsloth-dpo
description: Direct Preference Optimization (DPO) for aligning models with preference data without separate reward models. Triggers: dpo, preference optimization, rlhf, ref_model=none, patchdpotrainer, dpotrainer.
---

## Overview
Direct Preference Optimization (DPO) in Unsloth provides a way to align models with human preferences using paired data (chosen/rejected). Unsloth optimizes this process by allowing `ref_model=None`, significantly reducing memory requirements while maintaining high performance.

## When to Use
- When you have preference pairs (a better and worse response to the same prompt).
- When RLHF is desired but VRAM is limited (preventing the loading of a second reference model).
- When aligning reasoning or tone after a standard SFT phase.

## Decision Tree
1. Do you have a reference model already loaded?
   - No: Set `ref_model = None` in `DPOTrainer` to save VRAM.
2. Is your GPU RTX 40 series or H100?
   - Yes: Use FP8 preference optimization for faster training.
3. Is the model collapsing or losing its original abilities?
   - Yes: Lower the learning rate to 5e-6 and adjust the beta parameter (e.g., 0.1).

## Workflows

### DPO Trainer Initialization
1. Run `PatchDPOTrainer()` before importing `DPOTrainer` from TRL.
2. Load the base model in 4-bit with `FastLanguageModel` and set `ref_model=None` in trainer arguments.
3. Specify the beta parameter (typically 0.1) to control the strength of preference adaptation.

### Optimizing DPO VRAM Use
1. Enable `use_gradient_checkpointing='unsloth'` within `get_peft_model`.
2. Utilize FP8 precision if using L4 or RTX 40 series GPUs for further memory reduction.
3. Set `gradient_accumulation_steps` to 8 or 16 to maintain stability with low batch sizes.

## Non-Obvious Insights
- Setting `ref_model=None` is an Unsloth-specific trick; the trainer internally calculates the log-probs from the base model instead of needing a separate frozen model copy.
- DPO requires much lower learning rates (e.g., 5e-6) than SFT (e.g., 2e-4). Higher rates often lead to catastrophic forgetting or model collapse.
- Unsloth provides specialized Triton kernels for preference optimization that support FP8 even on consumer hardware like the RTX 4090.

## Evidence
- "PatchDPOTrainer () is required to use the reward modelling functions for DPO with Unsloth." [Source](https://docs.unsloth.ai/basics/reward-modelling-dpo-and-orpo)
- "dpo_trainer = DPOTrainer(model = model, ref_model = None, ...)" [Source](https://docs.unsloth.ai/basics/reward-modelling-dpo-and-orpo)

## Scripts
- `scripts/unsloth-dpo_tool.py`: Python script for configuring DPOTrainer with Unsloth patches.
- `scripts/unsloth-dpo_tool.js`: Configuration builder for DPO training runs.

## Dependencies
- unsloth
- trl
- torch

## References
- [[references/README.md]]