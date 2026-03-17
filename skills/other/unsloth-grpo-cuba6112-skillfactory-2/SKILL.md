---
name: unsloth-grpo
description: Implementation of Group Relative Policy Optimization (GRPO) for training reasoning models, optimized for 8x memory savings (triggers: GRPO, reasoning, DeepSeek-R1, reinforcement learning, RLVR, GRPOTrainer, thinking tokens).
---

## Overview
Unsloth-grpo enables training of reasoning models using Group Relative Policy Optimization (GRPO). This technique replaces traditional PPO Reward and Value models with group statistics, achieving 8x memory savings and allowing long-context RL training on limited VRAM.

## When to Use
- When building DeepSeek-R1 style reasoning models.
- When performing Reinforcement Learning with Verifiable Rewards (RLVR) for math or code.
- When training models with long context lengths (e.g., 20K tokens) on single GPUs.

## Decision Tree
1. Is your model size < 1.5B?
   - Yes: Model may struggle with consistent thinking tokens; consider 1.5B-8B.
2. Is the reward verifiable (e.g., math answer)?
   - Yes: Use RLVR with regex-based reward functions.
3. Are you training on a single GPU with long context?
   - Yes: Use `GRPOTrainer` to benefit from the 8x memory reduction.

## Workflows
1. **Converting to Reasoning LLM**: Load a base model with `fast_inference = True`, define a reward function for `<thought>` and `<answer>` tags, and train with `GRPOTrainer`.
2. **Implementing Verifiable Rewards (RLVR)**: Create a correctness function using regex to extract answers and assign rewards (e.g., 2.0) or penalties (-1.0) based on ground truth.
3. **Speed Optimization with FP8**: Select an FP8 Dynamic model and use `optim = 'adamw_8bit'` to further reduce memory during the RL rollout phase.

## Non-Obvious Insights
- GRPO eliminates the need for both the Reward Model and the Value Model, relying purely on group generation statistics for policy updates.
- Unsloth's GRPO implementation allows training 20K context reasoning models with only ~9.8GB of additional VRAM.
- For stable training, `num_generations` should be set to 8 per prompt to provide sufficient statistical variance for the reward calculation.

## Evidence
- "Unsloth shaves 8x memory usage for long context GRPO, so we need only an extra 9.8GB in extra VRAM for 20K context lengths!" [Source](https://docs.unsloth.ai/basics/reasoning-grpo-and-rl)
- "Introducing Long-context Reasoning (GRPO) in Unsloth. Train your own reasoning model with just 5GB VRAM." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-grpo_tool.py`: Template for GRPOTrainer and verifiable reward functions.
- `scripts/unsloth-grpo_tool.js`: Node.js utility for monitoring RL training metrics.

## Dependencies
- `unsloth`
- `trl`
- `vllm` (recommended for faster generation in rollouts)

## References
- [references/README.md](references/README.md)