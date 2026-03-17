---
name: llama-cpp
description: Secondary local LLM inference engine via llama.cpp. This skill should be used when running GGUF models directly, loading LoRA adapters for Kothar, benchmarking inference speed, or serving models via llama-server. Complements Ollama (which remains primary for RLAMA and general use).
user-invocable: false
---

# llama.cpp - Secondary Inference Engine

Direct access to llama.cpp for faster inference, LoRA adapter loading, and benchmarking on Apple Silicon. Ollama remains primary for RLAMA and general use; llama.cpp is the power tool.

## Prerequisites

```bash
brew install llama.cpp
```

Binaries: `llama-cli`, `llama-server`, `llama-embedding`, `llama-quantize`

## Quick Reference

### Resolve Ollama Model to GGUF Path

To avoid duplicating model files, resolve an Ollama model name to its GGUF blob path:

```bash
~/.claude/skills/llama-cpp/scripts/ollama_model_path.sh qwen2.5:7b
```

### Run Inference

```bash
GGUF=$(~/.claude/skills/llama-cpp/scripts/ollama_model_path.sh qwen2.5:7b)
llama-cli -m "$GGUF" -p "Your prompt here" -n 128 --n-gpu-layers all --single-turn --simple-io --no-display-prompt
```

### Start API Server

To start an OpenAI-compatible server (port 8081, avoids Ollama's 11434):

```bash
~/.claude/skills/llama-cpp/scripts/llama_serve.sh <model.gguf>

# Or with options:
PORT=8082 CTX=8192 ~/.claude/skills/llama-cpp/scripts/llama_serve.sh <model.gguf>
```

Test the server:
```bash
curl http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"Hello"}]}'
```

### Serve Qwen3.5 (MoE-Optimized)

Dedicated server for Qwen3.5 models with asymmetric KV cache, jinja templates, and thinking mode:

```bash
# Default: Qwen3.5-35B-A3B, thinking mode, 16K context
~/.claude/skills/llama-cpp/scripts/llama_serve_qwen35.sh

# Non-thinking mode, shorter context
THINK=0 CTX=8192 ~/.claude/skills/llama-cpp/scripts/llama_serve_qwen35.sh

# Different model
~/.claude/skills/llama-cpp/scripts/llama_serve_qwen35.sh qwen3.5:27b
```

Memory-optimized for M4 Max 36GB: asymmetric KV cache (q8_0 keys + q4_0 values) saves ~60% KV memory vs FP16.

### Benchmark (llama.cpp vs Ollama)

```bash
~/.claude/skills/llama-cpp/scripts/llama_bench.sh qwen2.5:7b
```

Reports prompt processing and generation tok/s for both engines side by side.

### LoRA Adapter Inference

Load a LoRA adapter dynamically on top of a base GGUF model (no merge required):

```bash
~/.claude/skills/llama-cpp/scripts/llama_lora.sh <base.gguf> <lora.gguf> "Your prompt"
```

This is the key advantage over Ollama: hot-swap LoRA adapters without rebuilding models.

### Convert Kothar LoRA to GGUF

Convert HuggingFace LoRA adapters from the Kothar training pipeline into a merged GGUF model:

```bash
python3 ~/.claude/skills/llama-cpp/scripts/convert_lora_to_gguf.py \
  --base NousResearch/Hermes-2-Mistral-7B-DPO \
  --lora <path-or-hf-id> \
  --output kothar-q4_k_m.gguf \
  --quantize q4_k_m
```

## When to Use llama.cpp vs Ollama

| Task | Use |
|------|-----|
| RLAMA queries | Ollama (native integration) |
| Quick model chat | Ollama (`ollama run`) |
| LoRA adapter testing | llama.cpp (`llama_lora.sh`) |
| Benchmarking tok/s | llama.cpp (`llama_bench.sh`) |
| Maximum inference speed | llama.cpp (10-20% faster) |
| Custom server config | llama.cpp (`llama_serve.sh`) |
| Embedding generation | Either (Ollama simpler, llama-embedding more control) |
| Kothar GGUF conversion | llama.cpp (`convert_lora_to_gguf.py`) |

## Architecture

```
Ollama (primary, port 11434)          llama.cpp (secondary, port 8081)
├── RLAMA RAG queries                 ├── LoRA adapter hot-loading
├── Model management (pull/list)      ├── Benchmarking
├── General chat                      ├── Custom server configs
└── Embeddings (nomic-embed-text)     └── Kothar GGUF conversion

Both share the same GGUF model files (~/.ollama/models/blobs/)
```

## Subprocess Best Practices (Build 7940+)

When calling llama-cli from scripts or subprocesses:
- **Always use `--single-turn`** — generates one response then exits (prevents interactive chat mode hang)
- **Always use `--simple-io`** — suppresses ANSI spinner that floods redirected output
- **Always use `--no-display-prompt`** — suppresses prompt echo
- **Use `--n-gpu-layers all`** instead of legacy `-ngl 999`
- **Use `--flash-attn on`** (not bare `--flash-attn`) — now takes argument
- **Timing stats** appear in stdout as `[ Prompt: X t/s | Generation: Y t/s ]` (via `--show-timings`, default: on)
- **Redirect stderr to file, not variable** — spinner output can overflow bash variables

