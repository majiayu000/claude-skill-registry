---
name: local-llm-gpu-selection
description: |
  Guide for selecting GPUs and hardware for local LLM inference on Dell R730 and
  comparing to Apple Silicon alternatives. Use when: (1) user asks about running
  local models (Ollama, llama.cpp), (2) user asks which GPU to buy for LLMs,
  (3) user wants to compare local models to Claude for coding, (4) user asks about
  quantized model selection, (5) user asks about Mac Mini/Studio vs GPU server for
  LLMs. Covers VRAM requirements, memory bandwidth as key metric, R730 GPU compatibility,
  multi-GPU considerations, and realistic quality comparisons to Claude models.
author: Claude Code
version: 1.0.0
date: 2025-06-11
---

# Local LLM GPU Selection & Performance Guide

## Problem
Choosing the right hardware for local LLM inference requires understanding the
relationship between VRAM capacity, memory bandwidth, GPU compatibility with
server chassis, and realistic model quality expectations.

## Context / Trigger Conditions
- User asks about running quantized models locally (Ollama, llama.cpp)
- User wants to know which GPU fits their server (Dell R730 or similar 2U)
- User asks about Apple Silicon (Mac Mini/Studio) vs datacenter GPUs for LLMs
- User wants to compare local model quality to Claude (Opus/Sonnet/Haiku) for coding

## Key Principle: Memory Bandwidth Is Everything

LLM token generation is **memory-bandwidth bound**, not compute bound. The formula:
```
approx tokens/sec = memory_bandwidth_GB_s / model_size_GB
```
This is why Apple Silicon (high bandwidth unified memory) competes with datacenter GPUs
despite having less raw compute.

## VRAM Requirements by Model Size

| Model Size | Quant | VRAM Needed | Examples |
|------------|-------|-------------|----------|
| 7-8B | Q4_K_M | ~5 GB | Llama 3.1 8B, Mistral 7B |
| 7-8B | Q8_0 | ~8 GB | |
| 13-14B | Q4_K_M | ~8 GB | Qwen 2.5 Coder 14B |
| 22-24B | Q4_K_M | ~13-14 GB | Mistral Small, Codestral |
| 32B | Q4_K_M | ~20 GB | Qwen 2.5 Coder 32B |
| 32B | Q8_0 | ~34 GB | |
| 70B | Q4_K_M | ~40 GB | Llama 3.1 70B |
| 70B | Q8_0 | ~70 GB | |

Add ~1-2 GB overhead for KV cache and context. Longer conversations use more.

## Dell R730 GPU Compatibility

### Constraints
- **2U chassis**: Full-height cards fit, but limited to dual-slot width
- **PCIe 3.0 x16 slots**: 2-3 usable slots depending on riser configuration
- **Power**: Needs Dell GPU power cable (P/N 0D4J0T) for GPUs >75W TDP
- **PSU**: Check wattage headroom (dual 750W or 1100W typical)

### Compatible GPUs

**No external power needed (<=75W):**
- Tesla T4: 16 GB, 320 GB/s, 70W — best drop-in option
- Tesla P4: 8 GB, 192 GB/s, 75W — too little VRAM for modern LLMs
- NVIDIA L4: 24 GB, 300 GB/s, 72W — T4 successor, Ada Lovelace, expensive
- NVIDIA A2: 16 GB, 200 GB/s, 60W — worse than T4 in every way, avoid

**Requires power cable (>75W):**
- Tesla P40: 24 GB, 346 GB/s, 250W — best value per GB
- Tesla V100 PCIe: 32 GB, 900 GB/s, 250W — excellent bandwidth
- Tesla P100 PCIe: 16 GB, 732 GB/s, 250W — same VRAM as T4, not worth it

**Won't fit:**
- RTX 3090/4090: Too thick (3-slot), too long
- A100: Fits physically but very expensive
- Any consumer RTX: Generally too large for 2U

### Multi-GPU Considerations
- Ollama splits model layers across GPUs automatically
- PCIe 3.0 cross-GPU transfer adds ~30-40% latency penalty
- Mismatched GPUs (e.g., T4 + P40) work but the slower card bottlenecks
- R730 PCIe 3.0 limits newer GPU bandwidth (L4 runs at half its rated speed)

## Apple Silicon Comparison

Apple Silicon unified memory means ALL system RAM = VRAM with no bus penalty.

| Device | Memory | Bandwidth | Advantage |
|--------|--------|-----------|-----------|
| Mac Mini M4 Pro 48 GB | 48 GB | 273 GB/s | Silent, 25W, no PCIe penalty |
| Mac Studio M4 Max 128 GB | 128 GB | 546 GB/s | Run 100B+ models |
| Mac Studio M4 Ultra 192 GB | 192 GB | 819 GB/s | Run anything |

A Mac Mini M4 Pro 48GB often matches or beats a T4+L4 multi-GPU setup for
LLM inference due to zero cross-GPU overhead and high unified bandwidth.

## Best Coding Models (for Ollama)

For coding tasks specifically, prefer dedicated coding models:
1. **Qwen 2.5 Coder 32B** — best open-source coding model in this size class
2. **Codestral 22B** — Mistral's dedicated coding model
3. **DeepSeek Coder V2** — good quality, efficient
4. **Llama 3.1 70B** — strong general purpose but needs ~40 GB

## Realistic Quality Comparison to Claude

For Claude Code-style agentic coding workflows:

| Capability | Opus/Sonnet | Haiku | Qwen 2.5 Coder 32B | 70B General |
|-----------|-------------|-------|---------------------|-------------|
| Single function gen | Excellent | Good | Good | Decent |
| Multi-file refactoring | Excellent | Decent | Weak | Weak |
| Tool use / agentic loops | Excellent | Good | Poor | Poor |
| Long context (large codebases) | Excellent | Good | Weak | Weak |

Local models work for simple completions and code questions. They struggle badly
with Claude Code's complex multi-step tool-use workflows, long context windows,
and self-correction capabilities.

## Quantization Quality Guide

From best to worst quality (and largest to smallest):
- FP16: Full precision, baseline quality
- Q8_0: Near-lossless, ~50% size reduction
- Q6_K: Minimal quality loss
- Q5_K_M: Good balance
- Q4_K_M: **Recommended default** — best quality/size tradeoff
- Q3_K_M: Noticeable degradation on complex reasoning
- Q2_K: Significant quality loss, emergency only

## Verification
- Check GPU compatibility: `lspci | grep -i nvidia` on the host
- Check available VRAM: `nvidia-smi` inside the GPU VM
- Check model fit: Ollama shows VRAM usage during `ollama run`
- Check inference speed: Count tokens/sec in Ollama output

## Notes
- GPU prices fluctuate significantly in the used market; check current prices
- The T4 is PCIe 3.0 only; newer GPUs in PCIe 3.0 slots run at reduced bandwidth
- Power consumption matters for 24/7 homelab use (electricity cost)
- For Claude Code specifically, API-based Claude models remain significantly
  superior to any local model for agentic coding workflows
