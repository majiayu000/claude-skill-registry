---
name: unsloth-sft
description: Supervised fine-tuning using SFTTrainer, instruction formatting, and multi-turn dataset preparation with triggers like sft, instruction tuning, chat templates, sharegpt, alpaca, conversation_extension, and SFTTrainer.
---

## Overview
Supervised Fine-Tuning (SFT) in Unsloth focuses on training models to follow instructions using specific formats. It provides tools for chat template mapping, multi-turn conversation synthesis via `conversation_extension`, and optimized dataset processing.

## When to Use
- When training models on instruction-response datasets (e.g., Alpaca).
- When developing multi-turn conversational agents.
- When you need to standardize various dataset formats (ShareGPT, OpenAI) for training.

## Decision Tree
1. Is your dataset single-turn?
   - Yes: Use `conversation_extension` to synthetically create multi-turn samples.
   - No: Map columns using `standardize_sharegpt`.
2. Are you training on Windows?
   - Yes: Set `dataset_num_proc = 1` in SFTConfig.
   - No: Use multiple processes for faster mapping.
3. Want to increase multi-turn accuracy?
   - Yes: Enable masking of inputs to train on completions only.

## Workflows

### Chat Template Implementation
1. Select a template (e.g., 'chatml', 'llama-3.1') using `get_chat_template(tokenizer, chat_template='...')`.
2. Map dataset columns using the mapping parameter (e.g., `mapping = {'role' : 'from', 'content' : 'value'}`).
3. Apply the formatting function to the dataset using `dataset.map` with `batched=True`.

### Multi-turn Data Preparation
1. Load a standard single-turn dataset like Alpaca.
2. Use `standardize_sharegpt(dataset)` to unify the role and content keys.
3. Apply `conversation_extension=N` to randomly concatenate N rows into single interactive samples.

## Non-Obvious Insights
- Training on completions only (masking out inputs) significantly increases accuracy, particularly for multi-turn conversations where input context is repetitive.
- Standardizing datasets to ShareGPT format before mapping is the most robust way to ensure compatibility with Unsloth's internal formatting kernels.
- On Windows, `dataset_num_proc` must be 1; otherwise, the multi-processing overhead or library incompatibilities will cause trainer crashes.

## Evidence
- "We introduced the conversation_extension parameter, which essentially selects some random rows in your single turn dataset, and merges them into 1 conversation!" [Source](https://docs.unsloth.ai/basics/chat-templates)
- "Training on completions only (masking out inputs) increases accuracy by quite a bit, especially for multi-turn conversational finetunes!" [Source](https://docs.unsloth.ai/basics/lora-parameters-encyclopedia)

## Scripts
- `scripts/unsloth-sft_tool.py`: Python tool for formatting datasets into ShareGPT/ChatML format.
- `scripts/unsloth-sft_tool.js`: JavaScript logic for mapping Alpaca-style datasets to conversation formats.

## Dependencies
- unsloth
- trl
- datasets

## References
- [[references/README.md]]