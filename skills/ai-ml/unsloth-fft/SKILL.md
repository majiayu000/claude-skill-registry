---
name: unsloth-fft
description: Performing full fine-tuning (FFT) in Unsloth with 100% exact weight updates and optimized gradient checkpointing. Triggers include fft, full fine-tuning, full_finetuning, exact fine-tuning, and weight updates.
---

## Overview
Full Fine-Tuning (FFT) in Unsloth allows for 100% exact weight updates, bypassing the low-rank approximations of LoRA. By utilizing Unsloth's optimized gradient checkpointing, FFT can fit significantly larger batch sizes while ensuring total model modification.

## When to Use
- When performing base model pre-training or continued pre-training on large datasets.
- When model-wide behaviors need modification that adapters (LoRA) cannot fully capture.
- When sufficient VRAM is available to handle full model gradients.

## Decision Tree
1. Do you need to modify 100% of the model weights?
   - Yes: Proceed with FFT.
   - No: Use [[unsloth-lora]].
2. Is VRAM limited (e.g., < 24GB for a 7B model)?
   - Yes: Enable `use_gradient_checkpointing = 'unsloth'` and `adamw_8bit`.
   - No: Use standard BF16 and high batch sizes.

## Workflows

### Initializing Full Fine-tuning
1. Load the model using `FastLanguageModel.from_pretrained` with `load_in_4bit=False` and `load_in_8bit=False`.
2. Pass `full_finetuning=True` in the initialization call to unlock all weight updates.
3. Apply the 'unsloth' gradient checkpointing via `FastLanguageModel.get_peft_model(model, use_gradient_checkpointing='unsloth')`.

### FFT Memory Management
1. Set `per_device_train_batch_size` to 1 to accommodate full weight gradients.
2. Increase `gradient_accumulation_steps` to simulate effective batch sizes of 16-32.
3. Use the `adamw_8bit` optimizer to reduce memory consumption by optimizer states.

## Non-Obvious Insights
- Unsloth's gradient checkpointing implementation is critical for FFT, as it uses 30% less VRAM and allows for 2x larger batch sizes compared to standard Hugging Face implementations.
- Full fine-tuning is the preferred method for base model pre-training where the objective is knowledge injection rather than task instruction.
- FFT in Unsloth is strictly 100% exact; there is no numerical drift compared to standard training, only efficiency gains.

## Evidence
- "To enable full fine-tuning (FFT), set full_finetuning = True." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "use_gradient_checkpointing = 'unsloth' uses 30% less VRAM, fits 2x larger batch sizes!" [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-fft_tool.py`: Script to initialize a full fine-tuning session with Unsloth.
- `scripts/unsloth-fft_tool.js`: Node.js utility to generate FFT training parameters.

## Dependencies
- unsloth
- torch
- transformers

## References
- [[references/README.md]]