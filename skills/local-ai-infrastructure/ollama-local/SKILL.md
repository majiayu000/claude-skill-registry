---
name: ollama-local
description: Local LLM inference with Ollama. Use when setting up local models for development, CI pipelines, or cost reduction. Covers model selection, LangChain integration, and performance tuning.
context: fork
agent: llm-integrator
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Ollama Local Inference

Run LLMs locally for cost savings, privacy, and offline development.

## When to Use

- CI/CD pipelines (93% cost reduction)
- Development without API costs
- Privacy-sensitive data
- Offline environments
- High-volume batch processing

## Quick Start

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull deepseek-r1:70b      # Reasoning (GPT-4 level)
ollama pull qwen2.5-coder:32b    # Coding
ollama pull nomic-embed-text     # Embeddings

# Start server
ollama serve
```

## Recommended Models (M4 Max 256GB)

| Task | Model | Size | Notes |
|------|-------|------|-------|
| Reasoning | `deepseek-r1:70b` | ~42GB | GPT-4 level |
| Coding | `qwen2.5-coder:32b` | ~35GB | 73.7% Aider benchmark |
| Embeddings | `nomic-embed-text` | ~0.5GB | 768 dims, fast |
| General | `llama3.2:70b` | ~40GB | Good all-around |

## LangChain Integration

```python
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Chat model
llm = ChatOllama(
    model="deepseek-r1:70b",
    base_url="http://localhost:11434",
    temperature=0.0,
    num_ctx=32768,      # Context window
    keep_alive="5m",    # Keep model loaded
)

# Embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434",
)

# Generate
response = await llm.ainvoke("Explain async/await")
vector = await embeddings.aembed_query("search text")
```

## Tool Calling with Ollama

```python
from langchain_core.tools import tool

@tool
def search_docs(query: str) -> str:
    """Search the document database."""
    return f"Found results for: {query}"

# Bind tools
llm_with_tools = llm.bind_tools([search_docs])
response = await llm_with_tools.ainvoke("Search for Python patterns")
```

## Structured Output

```python
from pydantic import BaseModel, Field

class CodeAnalysis(BaseModel):
    language: str = Field(description="Programming language")
    complexity: int = Field(ge=1, le=10)
    issues: list[str] = Field(description="Found issues")

structured_llm = llm.with_structured_output(CodeAnalysis)
result = await structured_llm.ainvoke("Analyze this code: ...")
# result is typed CodeAnalysis object
```

## Provider Factory Pattern

```python
import os

def get_llm_provider(task_type: str = "general"):
    """Auto-switch between Ollama and cloud APIs."""
    if os.getenv("OLLAMA_ENABLED") == "true":
        models = {
            "reasoning": "deepseek-r1:70b",
            "coding": "qwen2.5-coder:32b",
            "general": "llama3.2:70b",
        }
        return ChatOllama(
            model=models.get(task_type, "llama3.2:70b"),
            keep_alive="5m"
        )
    else:
        # Fall back to cloud API
        return ChatOpenAI(model="gpt-4o")

# Usage
llm = get_llm_provider(task_type="coding")
```

## Environment Configuration

```bash
# .env.local
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL_REASONING=deepseek-r1:70b
OLLAMA_MODEL_CODING=qwen2.5-coder:32b
OLLAMA_MODEL_EMBED=nomic-embed-text

# Performance tuning (Apple Silicon)
OLLAMA_MAX_LOADED_MODELS=3    # Keep 3 models in memory
OLLAMA_KEEP_ALIVE=5m          # 5 minute keep-alive
```

## CI Integration

```yaml
# GitHub Actions (self-hosted runner)
jobs:
  test:
    runs-on: self-hosted  # M4 Max runner
    env:
      OLLAMA_ENABLED: "true"
    steps:
      - name: Pre-warm models
        run: |
          curl -s http://localhost:11434/api/embeddings \
            -d '{"model":"nomic-embed-text","prompt":"warmup"}' > /dev/null

      - name: Run tests
        run: pytest tests/
```

## Cost Comparison

| Provider | Monthly Cost | Latency |
|----------|-------------|---------|
| Cloud APIs | ~$675/month | 200-500ms |
| Ollama Local | ~$50 (electricity) | 50-200ms |
| **Savings** | **93%** | **2-3x faster** |

## Best Practices

- **DO** use `keep_alive="5m"` in CI (avoid cold starts)
- **DO** pre-warm models before first call
- **DO** set `num_ctx=32768` on Apple Silicon
- **DO** use provider factory for cloud/local switching
- **DON'T** use `keep_alive=-1` (wastes memory)
- **DON'T** skip pre-warming in CI (30-60s cold start)

## Troubleshooting

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List loaded models
ollama list

# Check model memory usage
ollama ps

# Pull specific version
ollama pull deepseek-r1:70b-q4_K_M
```

## Related Skills

- `embeddings` - Embedding patterns (works with nomic-embed-text)
- `llm-evaluation` - Testing with local models
- `cost-optimization` - Broader cost strategies

## Capability Details

### setup
**Keywords:** setup, install, configure, ollama
**Solves:**
- Set up Ollama locally
- Configure for development
- Install models

### model-selection
**Keywords:** model, llama, mistral, qwen, selection
**Solves:**
- Choose appropriate model
- Compare model capabilities
- Balance speed vs quality

### provider-template
**Keywords:** provider, template, python, implementation
**Solves:**
- Ollama provider template
- Python implementation
- Drop-in LLM provider
