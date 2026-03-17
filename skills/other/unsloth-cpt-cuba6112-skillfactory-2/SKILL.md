---
name: unsloth-cpt
description: Strategies for continued pretraining and domain adaptation in Unsloth (triggers: continued pretraining, CPT, domain adaptation, lm_head, embed_tokens, rsLoRA, embedding_learning_rate).
---

## Overview
Unsloth-cpt provides specific optimizations for Continued Pretraining (CPT) and domain adaptation. It addresses the critical need for training embedding layers and language modeling heads while stabilizing the training process using Rank Stabilized LoRA (rsLoRA) and differentiated learning rates.

## When to Use
- When teaching a model a new language or highly specialized domain (e.g., legal, medical).
- When updating the `embed_tokens` or `lm_head` layers.
- When using high LoRA ranks (e.g., r=256) which can become unstable without rsLoRA.

## Decision Tree
1. Are you training on a new domain with unique vocabulary?
   - Yes: Include `lm_head` and `embed_tokens` in `target_modules`.
2. Are you using a LoRA rank > 64?
   - Yes: Set `use_rslora = True`.
3. Are you training embeddings?
   - Yes: Set `embedding_learning_rate` to 1/10th of the standard learning rate.

## Workflows
1. **New Language Adaptation**: Load the base model and configure `get_peft_model` to target `lm_head`, `embed_tokens`, and `gate_proj` with `use_rslora = True`.
2. **Stabilizing Embedding Updates**: Use `UnslothTrainer` and set `learning_rate = 5e-5` with a significantly lower `embedding_learning_rate` (e.g., 5e-6).
3. **Continued Finetuning from Adapters**: Load existing adapters using `from_pretrained` and resume training on refined domain data.

## Non-Obvious Insights
- Training on `lm_head` and `embed_tokens` with the standard learning rate often degrades performance; a 2-10x smaller learning rate is required for stability.
- Including the `gate_proj` matrix in LoRA modules is essential for CPT; omitting it leads to significantly faster catastrophic forgetting.
- Rank Stabilized LoRA (rsLoRA) is mathematically necessary to maintain scaling stability when using very high ranks (r=256) for broad domain adaptation.

## Evidence
- "Blindly training on the lm_head and embed_tokens does even worse! We must use a smaller learning rate for the lm_head and embed_tokens." [Source](https://unsloth.ai/blog/contpretraining)
- "The paper showed how Llama-2 performed well on maths, but not code - this is because the lm_head & embed_tokens weren't trained." [Source](https://unsloth.ai/blog/contpretraining)

## Scripts
- `scripts/unsloth-cpt_tool.py`: Configuration for rsLoRA and embedding learning rates.
- `scripts/unsloth-cpt_tool.js`: Helper for calculating rank-scaled learning rates.

## Dependencies
- `unsloth`
- `torch`
- `peft`

## References
- [references/README.md](references/README.md)