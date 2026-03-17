---
name: mistral
description: Mistral AI efficient open models. Use for efficient AI.
---

# Mistral

Mistral AI focuses on **efficiency** and **coding** capabilities. Their "Mixture of Experts" (MoE) architecture (Mixtral) changed the game.

## When to Use

- **Coding**: Mistral Large 2 (Codestral) is specifically optimized for code generation.
- **Efficiency**: Mixtral 8x7B offers GPT-3.5+ performance at a fraction of the inference cost.
- **Open Weights**: Apache 2.0 licenses (for smaller models).

## Core Concepts

### MoE (Mixture of Experts)

Only a subset of parameters (experts) are active per token. High quality, low compute.

### Codestral

A model trained specifically on 80+ programming languages.

### Le Chat

Mistral's chat interface (`chat.mistral.ai`).

## Best Practices (2025)

**Do**:

- **Use `codestral-mamba`**: For infinite context window coding tasks (linear time complexity).
- **Deploy via vLLM**: Mistral models run exceptionally well on vLLM.

**Don't**:

- **Don't ignore small models**: Mistral NeMo (12B) is surprisingly capable for RAG.

## References

- [Mistral AI Documentation](https://docs.mistral.ai/)
