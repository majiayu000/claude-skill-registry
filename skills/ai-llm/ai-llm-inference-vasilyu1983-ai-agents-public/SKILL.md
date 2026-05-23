---
name: ai-llm-inference
description: "Operational patterns for LLM inference: latency budgeting, tail-latency control, caching, batching/scheduling, quantization/compression, parallelism, and reliable serving at scale. Emphasizes production-grade performance, cost control, and observability."
---

# LLMOps – Inference & Optimization – Production Skill Hub

**Modern Best Practices (January 2026)**:

- Treat inference as a **systems problem**: SLOs, tail latency, retries, overload, and cache strategy.
- Use **continuous batching / smart scheduling** when serving many concurrent requests (Orca scheduling: https://www.usenix.org/conference/osdi22/presentation/yu).
- Use **KV-cache aware serving** (PagedAttention/vLLM: https://arxiv.org/abs/2309.06180) and **efficient attention kernels** (FlashAttention: https://arxiv.org/abs/2205.14135).
- Use **speculative decoding** when latency is critical and draft-model quality is acceptable (speculative decoding: https://arxiv.org/abs/2302.01318).
- Quantize only with **measured** quality impact and rollback plan (quantization must be validated on your eval set).

This skill provides **production-ready operational patterns** for optimizing LLM inference performance, cost, and reliability. It centralizes **decision rules**, **optimization strategies**, **configuration templates**, and **operational checklists** for inference workloads.

No theory. No narrative. Only what Claude can execute.

---

## When to Use This Skill

Claude should activate this skill whenever the user asks for:

- Optimizing LLM inference latency or throughput
- Choosing quantization strategies (FP8/FP4/INT8/INT4)
- Configuring vLLM, TensorRT-LLM, or DeepSpeed inference
- Scaling LLM inference across GPUs (tensor/pipeline parallelism)
- Building high-throughput LLM APIs
- Improving context window performance (KV cache optimization)
- Using speculative decoding for faster generation
- Reducing cost per token
- Profiling and benchmarking inference workloads
- Planning infrastructure capacity
- CPU/edge deployment patterns
- High availability and resilience patterns

## Scope Boundaries (Use These Skills for Depth)

- **Prompting, tuning, datasets** → [ai-llm](../ai-llm/SKILL.md)
- **RAG pipeline construction** → [ai-rag](../ai-rag/SKILL.md)
- **Deployment, APIs, monitoring** → [ai-mlops](../ai-mlops/SKILL.md)
- **Safety, governance** → [ai-mlops](../ai-mlops/SKILL.md)

---

## Quick Reference

| Task | Tool/Framework | Command/Pattern | When to Use |
|------|----------------|-----------------|-------------|
| Latency budget | SLO + load model | TTFT/ITL + P95/P99 under load | Any production endpoint |
| Tail-latency control | Scheduling + timeouts | Admission control + queue caps + backpressure | Prevent p99 explosions |
| Throughput | Batching + KV-cache aware serving | Continuous batching + KV paging | High concurrency serving |
| Cost control | Model tiering + caching | Cache (prefix/response) + quotas | Reduce spend and overload risk |
| Long context | Prefill optimization | Chunked prefill + prompt compression | Long inputs and RAG-heavy apps |
| Parallelism | TP/PP/DP | Choose by model size and interconnect | Models that do not fit one device |
| Reliability | Resilience patterns | Timeouts + circuit breakers + idempotency | Avoid cascading failures |

---

## Decision Tree: Inference Optimization Strategy

```text
Need to optimize LLM inference: [Optimization Path]
    ├─ Primary constraint: Throughput?
    │   ├─ Many concurrent users? → batching + KV-cache aware serving + admission control
    │   └─ Mostly batch/offline? → batch inference jobs + large batches + spot capacity
    │
    ├─ Primary constraint: Cost?
    │   ├─ Can accept lower quality tier? → model tiering (small/medium/large router)
    │   └─ Must keep quality? → caching + prompt/context reduction before quantization
    │
    ├─ Primary constraint: Latency?
    │   ├─ Draft model acceptable? → speculative decoding
    │   └─ Long context? → prefill optimizations + attention kernels + context budgets
    │
    ├─ Large model (>70B)?
    │   ├─ Multiple GPUs? → Tensor parallelism (NVLink required)
    │   └─ Deep model? → Pipeline parallelism (minimize bubbles)
    │
    └─ Edge deployment?
        └─ CPU + quantization → Optimized for constrained resources
```

---

## Core Concepts & Practices

### Core Concepts (Vendor-Agnostic)

- **Latency components**: queueing + prefill + decode; optimize the largest contributor first.
- **Tail latency**: p99 is dominated by queuing and long prompts; fix with admission control and context budgets.
- **Retries**: retries can multiply load; bound retries and use hedged requests only with strict budgets.
- **Caching**: prefix caching helps repeated system/tool scaffolds; response caching helps repeated questions (requires invalidation).
- **Security & privacy**: prompts/outputs can contain sensitive data; scrub logs, enforce auth/tenancy, and rate-limit abuse (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

### Implementation Practices (Tooling Examples)

- **Measure under load**: benchmark TTFT/ITL and p95/p99 with realistic concurrency and prompt lengths.
- **Separate environments**: dev/stage/prod model configs; promote only after passing the inference review checklist.
- **Export telemetry**: request-level tokens, TTFT/ITL, queue depth, GPU memory headroom, and error classes (OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/).

### Do / Avoid

**Do**
- Do enforce `max_input_tokens` and `max_output_tokens` at the API boundary.
- Do cap concurrency and queue depth; return overload errors quickly.
- Do validate quality after any quantization or kernel change.

**Avoid**
- Avoid unbounded retries (amplifies outages).
- Avoid unbounded context windows (OOM + latency spikes).
- Avoid benchmarking on single requests; always test with realistic concurrency.

---

## Resources (Detailed Operational Guides)

For comprehensive guides on specific topics, see:

### Infrastructure & Serving

- [Infrastructure Tuning](resources/infrastructure-tuning.md) - OS, container, Kubernetes optimization for GPU workloads
- [Serving Architectures](resources/serving-architectures.md) - Production serving stack patterns
- [Resilience & HA Patterns](resources/resilience-ha-patterns.md) - Multi-region, failover, traffic management

### Performance Optimization

- [Quantization Patterns](resources/quantization-patterns.md) - FP8/FP4/INT8/INT4 decision trees and validation
- [KV Cache Optimization](resources/kv-cache-optimization.md) - PagedAttention, FlashAttention, prefix caching
- [Parallelism Patterns](resources/parallelism-patterns.md) - Tensor/pipeline/expert parallelism strategies
- [Optimization Strategies](resources/optimization-strategies.md) - Throughput, cost, memory optimization
- [Batching & Scheduling](resources/batching-and-scheduling.md) - Continuous batching and throughput patterns

### Deployment & Operations

- [Edge & CPU Optimization](resources/edge-cpu-optimization.md) - llama.cpp, GGUF, mobile/browser deployment
- [GPU Optimization Checklists](resources/gpu-optimization-checklists.md) - Hardware-specific tuning
- [Speculative Decoding Guide](resources/speculative-decoding-guide.md) - Advanced generation acceleration
- [Profiling & Capacity Planning](resources/profiling-and-capacity-planning.md) - Benchmarking, SLOs, replica sizing

---

## Templates

### Inference Configs

Production-ready configuration templates for leading inference engines:

- [vLLM Configuration](templates/inference/template-vllm-config.md) - Continuous batching, PagedAttention setup
- [TensorRT-LLM Configuration](templates/inference/template-tensorrtllm-config.md) - NVIDIA kernel optimizations
- [DeepSpeed Inference](templates/inference/template-deepspeed-inference.md) - PyTorch-friendly inference

### Quantization & Compression

Model compression templates for reducing memory and cost:

- [GPTQ Quantization](templates/quantization/template-gptq.md) - GPU post-training quantization
- [AWQ Quantization](templates/quantization/template-awq.md) - Activation-aware weight quantization
- [GGUF Format](templates/quantization/template-gguf.md) - CPU/edge optimized formats

### Serving Pipelines

High-throughput serving architectures:

- [LLM API Server](templates/serving/template-llm-api.md) - FastAPI + vLLM production setup
- [High-Throughput Setup](templates/serving/template-high-throughput-setup.md) - Multi-replica scaling patterns

### Caching & Batching

Performance optimization templates:

- [Prefix Caching](templates/caching/template-prefix-caching.md) - KV cache reuse strategies
- [Batching Configuration](templates/batching/template-batching-config.md) - Continuous batching tuning

### Benchmarking

Performance measurement and validation:

- [Latency & Throughput Testing](templates/benchmarking/template-latency-throughput-test.md) - Load testing framework

### Checklists

- [Inference Performance Review Checklist](templates/checklists/inference-review-checklist.md) - Baseline, bottlenecks, rollout readiness

## Navigation

**Resources**
- [resources/serving-architectures.md](resources/serving-architectures.md)
- [resources/profiling-and-capacity-planning.md](resources/profiling-and-capacity-planning.md)
- [resources/gpu-optimization-checklists.md](resources/gpu-optimization-checklists.md)
- [resources/speculative-decoding-guide.md](resources/speculative-decoding-guide.md)
- [resources/resilience-ha-patterns.md](resources/resilience-ha-patterns.md)
- [resources/optimization-strategies.md](resources/optimization-strategies.md)
- [resources/kv-cache-optimization.md](resources/kv-cache-optimization.md)
- [resources/batching-and-scheduling.md](resources/batching-and-scheduling.md)
- [resources/quantization-patterns.md](resources/quantization-patterns.md)
- [resources/parallelism-patterns.md](resources/parallelism-patterns.md)
- [resources/edge-cpu-optimization.md](resources/edge-cpu-optimization.md)
- [resources/infrastructure-tuning.md](resources/infrastructure-tuning.md)

**Templates**
- [templates/serving/template-llm-api.md](templates/serving/template-llm-api.md)
- [templates/serving/template-high-throughput-setup.md](templates/serving/template-high-throughput-setup.md)
- [templates/inference/template-vllm-config.md](templates/inference/template-vllm-config.md)
- [templates/inference/template-tensorrtllm-config.md](templates/inference/template-tensorrtllm-config.md)
- [templates/inference/template-deepspeed-inference.md](templates/inference/template-deepspeed-inference.md)
- [templates/quantization/template-awq.md](templates/quantization/template-awq.md)
- [templates/quantization/template-gptq.md](templates/quantization/template-gptq.md)
- [templates/quantization/template-gguf.md](templates/quantization/template-gguf.md)
- [templates/batching/template-batching-config.md](templates/batching/template-batching-config.md)
- [templates/caching/template-prefix-caching.md](templates/caching/template-prefix-caching.md)
- [templates/benchmarking/template-latency-throughput-test.md](templates/benchmarking/template-latency-throughput-test.md)
- [templates/checklists/inference-review-checklist.md](templates/checklists/inference-review-checklist.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---

## Related Skills

This skill focuses on **inference-time performance**. For related workflows:

- **[ai-llm](../ai-llm/SKILL.md)** - Prompting, fine-tuning, application architecture
- **[ai-rag](../ai-rag/SKILL.md)** - RAG pipeline construction and optimization
- **[ai-mlops](../ai-mlops/SKILL.md)** - Deployment, monitoring, safety, and governance
- **[qa-observability](../qa-observability/SKILL.md)** - Performance monitoring and optimization
- **[ops-devops-platform](../ops-devops-platform/SKILL.md)** - Infrastructure and platform operations

---

## External Resources

See [data/sources.json](data/sources.json) for:

- Serving frameworks (vLLM, TensorRT-LLM, DeepSpeed-MII)
- Quantization libraries (GPTQ, AWQ, bitsandbytes, LLM Compressor)
- FlashAttention, FlashInfer, xFormers
- GPU hardware guides and optimization docs
- Benchmarking frameworks and tools

---

Use this skill whenever the user needs **LLM inference performance, cost reduction, or serving architecture** guidance.
