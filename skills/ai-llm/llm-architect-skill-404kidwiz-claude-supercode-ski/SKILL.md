---
name: llm-architect
description: Use when user needs LLM system architecture, model deployment, optimization strategies, and production serving infrastructure. Designs scalable large language model applications with focus on performance, cost efficiency, and safety.
---

# LLM Architect

## Purpose

Provides expert large language model system architecture for designing, deploying, and optimizing LLM applications at scale. Specializes in model selection, RAG (Retrieval Augmented Generation) pipelines, fine-tuning strategies, serving infrastructure, cost optimization, and safety guardrails for production LLM systems.

## When to Use

- Designing end-to-end LLM systems from requirements to production
- Selecting models and serving infrastructure for specific use cases
- Implementing RAG (Retrieval Augmented Generation) pipelines
- Optimizing LLM costs while maintaining quality thresholds
- Building safety guardrails and compliance mechanisms
- Planning fine-tuning vs RAG vs prompt engineering strategies
- Scaling LLM inference for high-throughput applications

## Quick Start

**Invoke this skill when:**
- Designing end-to-end LLM systems from requirements to production
- Selecting models and serving infrastructure for specific use cases
- Implementing RAG (Retrieval Augmented Generation) pipelines
- Optimizing LLM costs while maintaining quality thresholds
- Building safety guardrails and compliance mechanisms

**Do NOT invoke when:**
- Simple API integration exists (use backend-developer instead)
- Only prompt engineering needed without architecture decisions
- Training foundation models from scratch (almost always wrong approach)
- Generic ML tasks unrelated to language models (use ml-engineer)

## Decision Framework

### Model Selection Quick Guide

| Requirement | Recommended Approach |
|-------------|---------------------|
| Latency <100ms | Small fine-tuned model (7B quantized) |
| Latency <2s, budget unlimited | Claude 3 Opus / GPT-4 |
| Latency <2s, domain-specific | Claude 3 Sonnet fine-tuned |
| Latency <2s, cost-sensitive | Claude 3 Haiku |
| Batch/async acceptable | Batch API, cheapest tier |

### RAG vs Fine-Tuning Decision Tree

```
Need to customize LLM behavior?
│
├─ Need domain-specific knowledge?
│  ├─ Knowledge changes frequently?
│  │  └─ RAG (Retrieval Augmented Generation)
│  └─ Knowledge is static?
│     └─ Fine-tuning OR RAG (test both)
│
├─ Need specific output format/style?
│  ├─ Can describe in prompt?
│  │  └─ Prompt engineering (try first)
│  └─ Format too complex for prompt?
│     └─ Fine-tuning
│
└─ Need latency <100ms?
   └─ Fine-tuned small model (7B-13B)
```

### Architecture Pattern

```
[Client] → [API Gateway + Rate Limiting]
              ↓
         [Request Router]
          (Route by intent/complexity)
              ↓
    ┌────────┴────────┐
    ↓                 ↓
[Fast Model]    [Powerful Model]
(Haiku/Small)   (Sonnet/Large)
    ↓                 ↓
[Cache Layer] ← [Response Aggregator]
    ↓
[Logging & Monitoring]
    ↓
[Response to Client]
```

## Core Workflow: Design LLM System

### 1. Requirements Gathering

Ask these questions:
- **Latency**: What's the P95 response time requirement?
- **Scale**: Expected requests/day and growth trajectory?
- **Accuracy**: What's the minimum acceptable quality? (measurable metric)
- **Cost**: Budget constraints? ($/request or $/month)
- **Data**: Existing datasets for evaluation? Sensitivity level?
- **Compliance**: Regulatory requirements? (HIPAA, GDPR, SOC2, etc.)

### 2. Model Selection

```python
def select_model(requirements):
    if requirements.latency_p95 < 100:  # milliseconds
        if requirements.task_complexity == "simple":
            return "llama2-7b-finetune"
        else:
            return "mistral-7b-quantized"
    
    elif requirements.latency_p95 < 2000:
        if requirements.budget == "unlimited":
            return "claude-3-opus"
        elif requirements.domain_specific:
            return "claude-3-sonnet-finetuned"
        else:
            return "claude-3-haiku"
    
    else:  # Batch/async acceptable
        if requirements.accuracy_critical:
            return "gpt-4-with-ensemble"
        else:
            return "batch-api-cheapest-tier"
```

### 3. Prototype & Evaluate

```bash
# Run benchmark on eval dataset
python scripts/evaluate_model.py \
  --model claude-3-sonnet \
  --dataset data/eval_1000_examples.jsonl \
  --metrics accuracy,latency,cost

# Expected output:
# Accuracy: 94.3%
# P95 Latency: 1,245ms
# Cost per 1K requests: $2.15
```

### 4. Iteration Checklist

- [ ] Latency P95 meets requirement? If no → optimize serving (quantization, caching)
- [ ] Accuracy meets threshold? If no → improve prompts, fine-tune, or upgrade model
- [ ] Cost within budget? If no → aggressive caching, smaller model routing, batching
- [ ] Safety guardrails tested? If no → add content filters, PII detection
- [ ] Monitoring dashboards live? If no → set up Prometheus + Grafana
- [ ] Runbook documented? If no → document common failures and fixes

## Cost Optimization Strategies

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Semantic caching | 40-80% | 60%+ similar queries |
| Multi-model routing | 30-50% | Mixed complexity queries |
| Prompt compression | 10-20% | Long context inputs |
| Batching | 20-40% | Async-tolerant workloads |
| Smaller model cascade | 40-60% | Simple queries first |

## Safety Checklist

- [ ] Content filtering tested against adversarial examples
- [ ] PII detection and redaction validated
- [ ] Prompt injection defenses in place
- [ ] Output validation rules implemented
- [ ] Audit logging configured for all requests
- [ ] Compliance requirements documented and validated

## Red Flags - When to Escalate

| Observation | Action |
|-------------|--------|
| Accuracy <80% after prompt iteration | Consider fine-tuning |
| Latency 2x requirement | Review infrastructure |
| Cost >2x budget | Aggressive caching/routing |
| Hallucination rate >5% | Add RAG or stronger guardrails |
| Safety bypass detected | Immediate security review |

## Quick Reference: Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| P95 Latency | <2x requirement | <3x requirement |
| Accuracy | >90% | >80% |
| Cache Hit Rate | >60% | >40% |
| Error Rate | <1% | <5% |
| Cost/1K requests | Within budget | <150% budget |

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
  - RAG implementation workflow
  - Semantic caching patterns
  - Deployment configurations
  
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
  - Anti-patterns (fine-tuning when prompting suffices, no fallback)
  - Quality checklist for LLM systems
  - Resilient LLM call patterns
