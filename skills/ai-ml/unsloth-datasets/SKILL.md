---
name: unsloth-datasets
description: Standardizing and formatting datasets for Unsloth, including chat template conversion and synthetic data generation (triggers: chat templates, ShareGPT, Alpaca, conversation_extension, add_new_tokens, standardize_sharegpt, formatting_prompts_func).
---

## Overview
Unsloth-datasets provides tools to prepare and optimize data for fine-tuning. Key features include standardizing external datasets (like ShareGPT/Alpaca) into a unified format, synthetically extending single-turn data into multi-turn conversations, and handling custom special tokens.

## When to Use
- When converting raw datasets from diverse sources (Hugging Face, ShareGPT) into Unsloth-compatible formats.
- When you only have single-turn data but want the model to learn multi-turn conversation logic.
- When adding new domain-specific tokens (e.g., `<THINKING>`) to a model.

## Decision Tree
1. Is your dataset in ShareGPT format?
   - Yes: Use `standardize_sharegpt()`.
2. Do you have only single-turn data but want multi-turn performance?
   - Yes: Use the `conversation_extension` parameter.
3. Are you adding new tokens?
   - Yes: Call `add_new_tokens()` BEFORE calling `get_peft_model()`.

## Workflows
1. **Standardizing External Datasets**: Import `standardize_sharegpt`, apply it to the dataset to map roles (e.g., 'human/gpt'), and apply the chat template using `formatting_prompts_func`.
2. **Adding Custom Domain Tokens**: Load model/tokenizer, use `add_new_tokens` to update matrices, and THEN initialize PEFT adapters to ensure new weights are covered.
3. **Custom Chat Template Design**: Define a Jinja2 template and explicit EOS token, then pass them as a tuple to `get_chat_template`.

## Non-Obvious Insights
- Applying the wrong chat template (e.g., Llama-3 template on a Mistral model) is a leading cause of poor fine-tuning performance.
- The `conversation_extension` tool creates synthetic multi-turn interactions by randomly merging single-turn rows, improving the model's contextual memory.
- The order of operations is critical: Adding tokens *after* initializing LoRA will result in new tokens not being trained by the adapters.

## Evidence
- "We introduced the conversation_extension parameter, which essentially selects some random rows in your single turn dataset, and merges them into 1 conversation!" [Source](https://docs.unsloth.ai/basics/chat-templates)
- "Users must call add_new_tokens BEFORE get_peft_model to properly resize embedding matrices and LoRA adapters." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-datasets_tool.py`: Python tool for standardization and token addition.
- `scripts/unsloth-datasets_tool.js`: JS template for ShareGPT data mapping.

## Dependencies
- `unsloth`
- `datasets`
- `jinja2`

## References
- [references/README.md](references/README.md)