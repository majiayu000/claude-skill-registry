---
name: unsloth-orpo
description: One-step preference alignment using Odds Ratio Preference Optimization (ORPO) (triggers: ORPO, preference optimization, alignment, ORPOTrainer, log_odds_ratio, binary preference).
---

## Overview
Unsloth-orpo facilitates one-step preference alignment using Odds Ratio Preference Optimization (ORPO). Unlike DPO, which requires a separate reference model, ORPO incorporates a penalty for disfavored generations directly into the training process, making it more efficient and faster.

## When to Use
- When aligning models with human preferences (Chosen vs. Rejected) in a single step.
- When seeking an efficient alternative to DPO or RLHF.
- When training on preference datasets like `ultrafeedback_binarized`.

## Decision Tree
1. Do you have a reference model?
   - No: Use ORPO for one-step alignment.
2. Is the model diverging from language patterns?
   - Yes: Monitor `nll_loss` (the SFT component) and adjust learning rate.
3. Is the preference gap widening?
   - Monitor `rewards/margins` and `log_odds_ratio` in logs.

## Workflows
1. **One-Step Preference Alignment**: Load a model in 4-bit, apply LoRA, and initialize `ORPOTrainer` with a low learning rate (approx. 8e-6).
2. **Monitoring ORPO Metrics**: Connect to Weights & Biases to track the `log_odds_ratio` (preference for chosen) and `nll_loss` (language modeling stability).
3. **Exporting ORPO Models**: Merge trained LoRA weights into the 16-bit base and export as GGUF (e.g., `q4_k_m`) for deployment.

## Non-Obvious Insights
- ORPO eliminates the need for a separate Reward Model and Reference Model by penalizing the log-odds ratio of rejected responses directly.
- While SFT can accidentally increase the probability of bad responses by simply learning language patterns, ORPO widens the gap between "good" and "bad" from the first step.
- Optimal learning rates for ORPO are typically much lower than SFT (e.g., 8e-6 vs 2e-4).

## Evidence
- "Traditional approaches like DPO require two steps... With ORPO, we can do it all in one step, which is great and more efficient." [Source](https://www.stephendiehl.com/posts/orpo/)
- "ORPOConfig(learning_rate = 8e-6, beta = 0.1, lr_scheduler_type = 'cosine_with_restarts')." [Source](https://www.stephendiehl.com/posts/orpo/)

## Scripts
- `scripts/unsloth-orpo_tool.py`: Setup for ORPOTrainer and preference datasets.
- `scripts/unsloth-orpo_tool.js`: Metric tracker for odds ratio changes.

## Dependencies
- `unsloth`
- `trl` (ORPOTrainer)
- `wandb` (recommended for monitoring)

## References
- [references/README.md](references/README.md)