---
name: ollama
description: Ollama local LLM deployment and management. Use for running LLMs locally.
---

# Ollama

Ollama makes running LLMs locally as easy as `docker run`. 2025 updates include **Windows/AMD** support, **Multimodal** input, and Tool Calling.

## When to Use

- **Local Development**: Coding without wifi or API costs.
- **Privacy**: Processing sensitive documents on-device.
- **Integration**: Works with LangChain, LlamaIndex, and Obsidian natively.

## Core Concepts

### Modelfile

Docker-like file to define a custom model (System prompt + Base model).

```dockerfile
FROM llama3
SYSTEM You are Mario from Super Mario Bros.
```

### API

Ollama runs a local server (`localhost:11434`) compatible with OpenAI SDK.

## Best Practices (2025)

**Do**:

- **Use high-speed RAM**: Local LLM speed depends on memory bandwidth.
- **Use Quantized Models**: `q4_k_m` is the sweet spot for speed/quality balance.
- **Unload**: `ollama stop` when done to free VRAM for games/rendering.

**Don't**:

- **Don't expect GPT-4 level**: Smaller local models (8B) are smart but lack deep reasoning.

## References

- [Ollama Website](https://ollama.com/)
