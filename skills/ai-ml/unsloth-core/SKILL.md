---
name: unsloth-core
description: Core fundamentals of Unsloth for fast LLM fine-tuning, covering FastLanguageModel setup, optimized gradient checkpointing, and native inference acceleration (triggers: unsloth, FastLanguageModel, from_pretrained, get_peft_model, for_inference, gradient checkpointing).
---

## Overview
Unsloth-core provides the foundational framework for accelerating Large Language Model (LLM) fine-tuning. It leverages specialized kernels and optimized gradient checkpointing to achieve up to 2x faster native inference and significant VRAM savings compared to standard Hugging Face implementations.

## When to Use
- When fine-tuning Llama-3, Mistral, or Phi models and seeking maximum speed.
- When limited by VRAM and needing optimized gradient checkpointing.
- When deploying models for inference and requiring low-latency responses.

## Decision Tree
1. Are you starting a new fine-tuning run?
   - Yes: Use `FastLanguageModel.from_pretrained()`.
   - No (Inference only): Load with `for_inference=True`.
2. Is your VRAM usage too high?
   - Yes: Set `use_gradient_checkpointing = 'unsloth'`.
3. Are you ready for generation?
   - Yes: Call `FastLanguageModel.for_inference(model)` to enable 2x speed.

## Workflows
1. **Basic Model Initialization**: Import `FastLanguageModel`, load a model with specific `max_seq_length` and `load_in_4bit`, and configure PEFT adapters via `get_peft_model()`.
2. **Optimized Training Configuration**: Configure `SFTTrainer` with `use_gradient_checkpointing = 'unsloth'` and monitor loss values (ideally between 0.5 and 1.0).
3. **Saving and Post-Training Inference**: Save LoRA adapters using `save_pretrained()`, then enable optimized inference via `for_inference(model)` for generation.

## Non-Obvious Insights
- Unsloth's native inference is not automatic; users must explicitly call `FastLanguageModel.for_inference(model)` to see the 2x performance gain.
- The specialized 'unsloth' gradient checkpointing option is 30% more VRAM efficient than the default standard implementation.
- Unsloth fixes known tokenizer and chat template bugs present in official model releases to improve fine-tuning accuracy.

## Evidence
- "Unsloth itself provides 2x faster inference natively as well, so always do not forget to call FastLanguageModel.for_inference(model)." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "We leverage our smart Unsloth gradient checkpointing algorithm... It smartly offloads intermediate activations to system RAM asynchronously whilst being only 1% slower." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-core_tool.py`: Python utility for model initialization and training setup.
- `scripts/unsloth-core_tool.js`: Node.js interface for managing Unsloth training configurations.

## Dependencies
- `unsloth`
- `torch`
- `transformers`
- `peft`
- `trl`

## References
- [references/README.md](references/README.md)