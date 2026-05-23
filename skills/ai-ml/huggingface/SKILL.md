---
name: huggingface
description: |
  Import GGUF models from HuggingFace into Ollama. Pull models directly
  using the hf.co/ prefix, track download progress, and use imported
  models for inference.
---

# HuggingFace Model Import

## Overview

Ollama can directly pull GGUF models from HuggingFace using the `hf.co/` prefix. This enables access to thousands of quantized models beyond the official Ollama library.

## Quick Reference

| Action | Syntax |
|--------|--------|
| Pull model | `hf.co/{org}/{repo}:{quantization}` |
| List models | `ollama.list()` |
| Use model | Same as any Ollama model |
| Delete model | `ollama.delete("hf.co/...")` |

## Model Naming Format

```
hf.co/{organization}/{repository}-GGUF:{quantization}
```

**Examples:**

```
hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M
hf.co/TheBloke/Llama-2-7B-Chat-GGUF:Q4_K_M
hf.co/microsoft/Phi-3-mini-4k-instruct-gguf:Q4_K_M
```

## Common Quantizations

| Quantization | Size | Quality | Use Case |
|--------------|------|---------|----------|
| Q2_K | Smallest | Lowest | Testing only |
| Q4_K_M | Medium | Good | Recommended default |
| Q5_K_M | Larger | Better | Quality-focused |
| Q6_K | Large | High | Near-original quality |
| Q8_0 | Largest | Highest | Maximum quality |

## Pull Model from HuggingFace

### With Progress Tracking

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

print(f"Pulling {HF_MODEL}...")

last_status = ""
for progress in ollama.pull(HF_MODEL, stream=True):
    status = progress.get("status", "")
    digest = progress.get("digest", "")
    total = progress.get("total")

    # Only print when status changes
    if status != last_status:
        if status == "pulling manifest":
            print(f"  {status}")
        elif status.startswith("pulling") and digest:
            short_digest = digest.split(":")[-1][:12] if ":" in digest else digest[:12]
            size_mb = (total / 1024 / 1024) if total else 0
            if size_mb > 100:
                print(f"  pulling {short_digest}... ({size_mb:.0f} MB)")
        elif status in ["verifying sha256 digest", "writing manifest", "success"]:
            print(f"  {status}")

        last_status = status

print("Model pulled successfully!")
```

### Simple Pull

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

# Non-streaming (blocks until complete)
ollama.pull(HF_MODEL)
print("Model pulled!")
```

## Verify Installation

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

models = ollama.list()
model_names = [m.get("model", "") for m in models.get("models", [])]

# Check for the HF model
hf_model_installed = any(
    "Nous-Hermes" in name or HF_MODEL in name
    for name in model_names
)

if hf_model_installed:
    print("Model is installed!")
    for name in model_names:
        if "Nous-Hermes" in name or "hf.co" in name:
            print(f"  Name: {name}")
else:
    print("Model not found")
```

## Show Model Details

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

model_info = ollama.show(HF_MODEL)

print(f"Model: {HF_MODEL}")
if "details" in model_info:
    details = model_info["details"]
    print(f"Family: {details.get('family', 'N/A')}")
    print(f"Parameter Size: {details.get('parameter_size', 'N/A')}")
    print(f"Quantization: {details.get('quantization_level', 'N/A')}")
```

## Use Imported Model

### Generate Text

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

result = ollama.generate(
    model=HF_MODEL,
    prompt="What is the capital of France?"
)
print(result["response"])
```

### Chat Completion

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

# Nous-Hermes-2 uses ChatML format natively
response = ollama.chat(
    model=HF_MODEL,
    messages=[
        {"role": "system", "content": "You are Hermes 2, a helpful AI assistant."},
        {"role": "user", "content": "Explain quantum computing in two sentences."}
    ]
)
print(response["message"]["content"])
```

## Delete Imported Model

```python
import ollama

HF_MODEL = "hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M"

ollama.delete(HF_MODEL)
print("Model deleted!")
```

## Popular HuggingFace Models

### General Purpose

| Model | HuggingFace Path | Size |
|-------|------------------|------|
| Nous-Hermes-2-Mistral | `hf.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF:Q4_K_M` | 4.4 GB |
| Llama-2-7B-Chat | `hf.co/TheBloke/Llama-2-7B-Chat-GGUF:Q4_K_M` | 4.1 GB |
| Mistral-7B-Instruct | `hf.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF:Q4_K_M` | 4.4 GB |

### Code Models

| Model | HuggingFace Path | Size |
|-------|------------------|------|
| CodeLlama-7B | `hf.co/TheBloke/CodeLlama-7B-Instruct-GGUF:Q4_K_M` | 4.1 GB |
| Phind-CodeLlama | `hf.co/TheBloke/Phind-CodeLlama-34B-v2-GGUF:Q4_K_M` | 20 GB |
| WizardCoder | `hf.co/TheBloke/WizardCoder-Python-7B-V1.0-GGUF:Q4_K_M` | 4.1 GB |

### Small/Fast Models

| Model | HuggingFace Path | Size |
|-------|------------------|------|
| Phi-3-mini | `hf.co/microsoft/Phi-3-mini-4k-instruct-gguf:Q4_K_M` | 2.4 GB |
| TinyLlama | `hf.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF:Q4_K_M` | 0.7 GB |

## Finding Models on HuggingFace

1. Go to [huggingface.co/models](https://huggingface.co/models)
2. Filter by:
   - **Library:** GGUF
   - **Task:** Text Generation
3. Look for models with `-GGUF` suffix
4. Check the "Files" tab for available quantizations

## Troubleshooting

### Model Not Found

**Symptom:** Error pulling model

**Check:**
- Repository exists on HuggingFace
- Repository has GGUF files
- Quantization tag is correct

```python
# Verify HuggingFace URL
# https://huggingface.co/{org}/{repo}/tree/main
```

### Download Fails

**Symptom:** Download interrupted or fails

**Fix:**
- Check internet connection
- Try again (Ollama resumes partial downloads)
- Check disk space

### Wrong Prompt Format

**Symptom:** Model gives poor responses

**Fix:**
- Check model card for correct prompt template
- Some models require specific formats (ChatML, Alpaca, etc.)

```python
# ChatML format example (Nous-Hermes-2)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

# The ollama library handles format conversion automatically
```

## When to Use This Skill

Use when:
- You need a model not in the official Ollama library
- Testing specific model variants
- Using specialized/fine-tuned models
- Comparing different quantizations

## Resources

- [Ollama Import Docs](https://docs.ollama.com/import)
- [HuggingFace Ollama Integration](https://huggingface.co/docs/hub/ollama)
- [TheBloke's GGUF Models](https://huggingface.co/TheBloke)

## Cross-References

- `bazzite-ai-jupyter:ollama` - Using imported models
- `bazzite-ai-jupyter:chat` - REST API for model management
