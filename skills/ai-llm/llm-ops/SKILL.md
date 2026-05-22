---
name: llm-ops
description: >
  Local LLM health checks and cache management.
  Probe Ollama/vLLM/SGLang endpoints, clean model caches.
triggers:
  - check llm
  - is ollama running
  - llm health
  - vllm status
  - clean llm cache
  - free gpu memory
  - clear huggingface cache
  - ollama status
allowed-tools: Bash
metadata:
  short-description: Local LLM health checks and cache management
---

# LLM Ops

Manage local LLM runtimes and caches.

## Commands

```bash
# Check all common LLM endpoints (Ollama, vLLM, SGLang)
./scripts/health.sh

# Check specific endpoint
./scripts/health.sh --target ollama:http://127.0.0.1:11434

# Continue even if some fail
./scripts/health.sh --warn-only

# Show cache sizes (dry-run)
./scripts/cache-clean.sh

# Actually clean caches
./scripts/cache-clean.sh --execute

# Clean additional path
./scripts/cache-clean.sh --path ~/.cache/torch --execute
```

## Default Endpoints Checked

- Ollama: `http://127.0.0.1:11434`
- vLLM: `http://127.0.0.1:8000`
- SGLang: `http://127.0.0.1:30000`

## Default Cache Directories

- `~/.cache/ollama`
- `~/.cache/huggingface`
- `~/.cache/vllm`

## Environment Variables

| Variable             | Default     | Description                  |
| -------------------- | ----------- | ---------------------------- |
| `LLM_HEALTH_TIMEOUT` | 2           | Seconds to wait per endpoint |
| `LLM_CACHE_DIRS`     | (see above) | Space-separated cache paths  |
