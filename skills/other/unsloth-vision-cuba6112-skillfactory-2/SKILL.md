---
name: unsloth-vision
description: Fine-tuning multimodal vision-language models (Llama 3.2 Vision, Qwen2.5 VL) using optimized vision layers (triggers: vision models, multimodal, Llama 3.2 Vision, Qwen2.5 VL, UnslothVisionDataCollator, finetune_vision_layers).
---

## Overview
Unsloth-vision provides optimized support for fine-tuning multimodal models like Llama 3.2 Vision and Qwen2.5 VL. It allows granular control over which layers (vision, language, or both) are updated and includes specialized data collators to handle image padding.

## When to Use
- When adapting models for specialized visual tasks like medical imaging or OCR-to-code.
- When fine-tuning Llama 3.2 Vision models on consumer hardware.
- When needing to train specifically on assistant responses in a multimodal context.

## Decision Tree
1. Do you need to update visual feature extraction?
   - Yes: Set `finetune_vision_layers = True` in `get_peft_model`.
2. Are your images varying in size?
   - Yes: Standardize to 300-1000px and use `UnslothVisionDataCollator`.
3. Should the model ignore system/user prompts during loss calculation?
   - Yes: Use `train_on_responses_only = True` in the collator.

## Workflows
1. **Vision Model Setup**: Load models via `FastVisionModel.from_pretrained` and enable PEFT targeting `all-linear` modules.
2. **Multimodal Dataset Preparation**: Format data as 'user'/'assistant' conversations with `{'type': 'image'}` content and standardized dimensions (300-1000px).
3. **Training for Response Accuracy**: Initialize `UnslothVisionDataCollator` with `train_on_responses_only = True` and specified chat template headers.

## Non-Obvious Insights
- Unsloth allows selective fine-tuning of just the vision layers, just the language layers, or specific components like attention/MLP layers.
- The `UnslothVisionDataCollator` automatically masks out padding vision tokens, which is essential for stabilizing loss during training.
- Standardizing image resolution to the 300-1000px range is the optimal balance between detail preservation and VRAM efficiency.

## Evidence
- "To finetune vision models, we now allow you to select which parts of the mode to finetune... You can select to only finetune the vision layers, or the language layers..." [Source](https://docs.unsloth.ai/basics/vision-fine-tuning)
- "It is best to ensure your dataset has images of all the same size/dimensions. Use dimensions of 300-1000px..." [Source](https://docs.unsloth.ai/basics/vision-fine-tuning)

## Scripts
- `scripts/unsloth-vision_tool.py`: Loading and configuring FastVisionModel.
- `scripts/unsloth-vision_tool.js`: Dataset formatter for multimodal conversations.

## Dependencies
- `unsloth`
- `pillow` (for image processing)
- `torch`

## References
- [references/README.md](references/README.md)