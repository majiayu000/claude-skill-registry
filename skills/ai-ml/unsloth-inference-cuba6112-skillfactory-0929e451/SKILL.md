---
name: unsloth-inference
description: Deploying fine-tuned models for production inference using native kernel optimization, vLLM, or SGLang. Triggers: inference, serving, vllm, sglang, for_inference, model merging, openai api.
---

## Overview
Unsloth models can be deployed using native optimized inference or through production serving engines like vLLM and SGLang. Native inference is accelerated 2x via `for_inference()`, while production serving requires merging LoRA weights into the base model.

## When to Use
- When performing local testing or simple application deployment.
- When building high-throughput production endpoints using vLLM or SGLang.
- When creating OpenAI-compatible APIs for drop-in replacement in existing apps.

## Decision Tree
1. Is throughput the priority?
   - Yes: Merge to 16-bit and use vLLM.
2. Is VRAM for serving extremely limited?
   - Yes: Merge to 4-bit or use GGUF via Ollama.
3. Running simple Python inference?
   - Yes: Call `FastLanguageModel.for_inference(model)`.

## Workflows

### Native Optimized Inference
1. Load fine-tuned model and tokenizer using `FastLanguageModel`.
2. Call `FastLanguageModel.for_inference(model)` to enable optimized kernels.
3. Use `model.generate()` with inputs formatted via the chat template.

### Merging LoRA for vLLM Serving
1. Select export method: 'merged_16bit' (quality) or 'merged_4bit' (VRAM).
2. Run `model.save_pretrained_merged("serving_model", tokenizer, save_method='merged_16bit')`.
3. Start vLLM server pointing to the 'serving_model' directory.

## Non-Obvious Insights
- Calling `FastLanguageModel.for_inference(model)` is mandatory for speed; it performs on-the-fly weight fusion and enables specialized Triton kernels for the forward pass.
- Most production serving engines (vLLM, SGLang) cannot use LoRA adapters directly without performance hits; merging them into the base model during export is the standard best practice.
- The `unsloth-cli` provides a pre-built OpenAI-compatible endpoint, making it easy to serve models locally and test with standard API clients.

## Evidence
- "Unsloth itself provides 2x faster inference natively as well, so always do not forget to call FastLanguageModel.for_inference(model)." [Source](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- "model.save_pretrained_merged(\"output\", tokenizer, save_method = \"merged_16bit\")" [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-inference_tool.py`: Script for running local optimized inference.
- `scripts/unsloth-inference_tool.js`: Helper to test OpenAI-compatible endpoints.

## Dependencies
- unsloth
- torch
- vllm (optional for production)
- sglang (optional for production)

## References
- [[references/README.md]]