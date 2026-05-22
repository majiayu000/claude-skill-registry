---
name: llama
description: Meta Llama open-source LLM family. Use for local AI.
---

# Llama

Meta Llama is the king of Open Weights models. Llama 4 (2025) pushes 405B+ parameters, rivaling closed models like GPT-5.

## When to Use

- **Privacy**: Run it on your own VPC (AWS Bedrock, Azure, or self-hosted).
- **Fine-Tuning**: It is the default base model for fine-tuning on domain data.
- **Cost**: Inference on Groq/Together AI is significantly cheaper than GPT.

## Core Concepts

### Models

- **405B**: Frontier intelligence. Requires massive GPU clusters (or API).
- **70B**: The workhorse. Smart enough for most tasks.
- **8B**: Runs on a laptop (MacBook M3).

### Quantization

Running models at 4-bit or 8-bit precision to fit in VRAM with minimal quality loss (GGUF, EXL2).

### Llama Stack

Standardized tooling for building agentic apps on Llama.

## Best Practices (2025)

**Do**:

- **Use via API**: Groq (LPU) runs Llama Instantaneously (>1000 tok/s).
- **Fine-Tune 8B**: For specific tasks (classification, SQL generation), a fine-tuned 8B beats a generic 70B.

**Don't**:

- **Don't self-host 405B**: Unless you have 8xH100s. Use an API provider.

## References

- [Llama Website](https://www.llama.com/)
