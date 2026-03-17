---
name: unsloth-gguf
description: Exporting fine-tuned models to GGUF format for deployment in llama.cpp, Ollama, and local serving tools. Triggers: gguf, quantization export, llama.cpp, ollama, save_pretrained_gguf, modelfile.
---

## Overview
Unsloth provides a streamlined method to export fine-tuned models directly to GGUF format. It features "Dynamic 2.0" quantization, which protects sensitive weights to maintain high accuracy, and automates the merging of LoRA adapters.

## When to Use
- When deploying models to local serving platforms like Ollama, llama.cpp, or LM Studio.
- When model size needs to be minimized for CPU-based inference or low-VRAM GPUs.
- When sharing models with the community via GGUF format.

## Decision Tree
1. Is target VRAM very low?
   - Yes: Use `quantization_method = 'q4_k_m'` or higher compression.
   - No: Use `q8_0` or `f16` for maximum quality.
2. Deploying to Ollama?
   - Yes: Export to GGUF and then create a `Modelfile` with a `FROM` command.

## Workflows

### Exporting Fine-tuned Models to GGUF
1. After training, call `model.save_pretrained_gguf("name", tokenizer, quantization_method='q4_k_m')`.
2. Specify quantization method (e.g., `q4_k_m`, `q8_0`, `f16`) based on target VRAM.
3. Wait for the script to download llama.cpp and perform conversion automatically.

### Deploying to Ollama
1. Export model to GGUF using the native Unsloth save function.
2. Create a 'Modelfile' containing: `FROM ./model-q4_k_m.gguf`.
3. Run `ollama create my-model -f Modelfile` to import and serve.

## Non-Obvious Insights
- Unsloth 'Dynamic 2.0' GGUFs are superior to standard GGUFs because they dynamically identify and protect weights that are sensitive to quantization, leading to higher MMLU scores.
- The GGUF export process handles the complex task of merging LoRA layers back into the base weights automatically, ensuring the resulting file is a standalone model.
- Unsloth supports direct Hub uploading for GGUFs, removing the need for local storage during the export-to-share pipeline.

## Evidence
- "model.save_pretrained_gguf(\"model\", tokenizer, quantization_method = \"q4_k_m\")" [Source](https://github.com/unslothai/unsloth)
- "Unsloth Dynamic 4-bit Quantization! We dynamically opt not to quantize certain parameters and this greatly increases accuracy." [Source](https://github.com/unslothai/unsloth)

## Scripts
- `scripts/unsloth-gguf_tool.py`: Python helper for automated GGUF export.
- `scripts/unsloth-gguf_tool.js`: Utility to generate Ollama Modelfiles.

## Dependencies
- unsloth
- llama-cpp-python (or local llama.cpp binary)
- huggingface_hub

## References
- [[references/README.md]]