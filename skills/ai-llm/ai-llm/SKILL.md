---
name: ai-llm
description: Production LLM engineering skill. Covers strategy selection (prompting vs RAG vs fine-tuning), dataset design, PEFT/LoRA, evaluation workflows, deployment handoff to inference serving, and lifecycle operations with cost/safety controls.
---

# LLM Development & Engineering — Complete Reference

Build, evaluate, and deploy LLM systems with **modern production standards**.

This skill covers the full LLM lifecycle:

- **Development**: Strategy selection, dataset design, instruction tuning, PEFT/LoRA fine-tuning
- **Evaluation**: Automated testing, LLM-as-judge, metrics, rollout gates
- **Deployment**: Serving handoff, latency/cost budgeting, reliability patterns (see `ai-llm-inference`)
- **Operations**: Quality monitoring, change management, incident response (see `ai-mlops`)
- **Safety**: Threat modeling, data governance, layered mitigations (NIST AI RMF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)

**Modern Best Practices (January 2026)**:

- Treat the model as a **component** with contracts, budgets, and rollback plans (not “magic”).
- Separate **core concepts** (tokenization, context, training vs adaptation) from **implementation choices** (providers, SDKs).
- Gate upgrades with repeatable evals and staged rollout; avoid blind model swaps.

**For detailed patterns:** See [Resources](#resources-best-practices--operational-patterns) and [Templates](#templates-copy-paste-ready) sections below.

---

## Quick Reference

| Task | Tool/Framework | Command/Pattern | When to Use |
|------|----------------|-----------------|-------------|
| Choose architecture | Prompt vs RAG vs fine-tune | Start simple; add retrieval/adaptation only if needed | New products and migrations |
| Model selection | Scoring matrix | Quality/latency/cost/privacy/license weighting | Provider changes and procurement |
| Prompt contracts | Structured output + constraints | JSON schema, max tokens, refusal rules | Reliability and integration |
| RAG integration | Hybrid retrieval + grounding | Retrieve → rerank → pack → cite → verify | Fresh/large corpora, traceability |
| Fine-tuning | PEFT/LoRA (when justified) | Small targeted datasets + regression suite | Stable domains, repeated tasks |
| Evaluation | Offline + online | Golden sets + A/B + canary + monitoring | Prevent regressions and drift |

---

## Decision Tree: LLM System Architecture

```text
Building LLM application: [Architecture Selection]
    ├─ Need current knowledge?
    │   ├─ Simple Q&A? → Basic RAG (page-level chunking + hybrid retrieval)
    │   └─ Complex retrieval? → Advanced RAG (reranking + contextual retrieval)
    │
    ├─ Need tool use / actions?
    │   ├─ Single task? → Simple agent (ReAct pattern)
    │   └─ Multi-step workflow? → Multi-agent (LangGraph, CrewAI)
    │
    ├─ Static behavior sufficient?
    │   ├─ Quick MVP? → Prompt engineering (CI/CD integrated)
    │   └─ Production quality? → Fine-tuning (PEFT/LoRA)
    │
    └─ Best results?
        └─ Hybrid (RAG + Fine-tuning + Agents) → Comprehensive solution
```

**See [Decision Matrices](resources/decision-matrices.md) for detailed selection criteria.**

---

## Core Concepts (Vendor-Agnostic)

- **Model classes**: encoder-only, decoder-only, encoder-decoder, multimodal; choose based on task and latency.
- **Tokenization & limits**: context window, max output, and prompt/template overhead drive both cost and tail latency.
- **Adaptation options**: prompting → retrieval → adapters (LoRA) → full fine-tune; choose by stability and ROI (LoRA: https://arxiv.org/abs/2106.09685).
- **Evaluation**: metrics must map to user value; report uncertainty and slice performance, not only global averages.
- **Governance**: data retention, residency, licensing, and auditability are product requirements (EU AI Act: https://eur-lex.europa.eu/eli/reg/2024/1689/oj; NIST GenAI Profile: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).

## Implementation Practices (Tooling Examples)

- Use a **provider abstraction** (gateway/router) to enable fallbacks and staged upgrades.
- Instrument requests with tokens, latency, and error classes (OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/).
- Maintain **prompt/model registries** with versioning, changelogs, and rollback criteria.

## Do / Avoid

**Do**
- Do pin model + prompt versions in production, and re-run evals before any change.
- Do enforce budgets at the boundary: max tokens, max tools, max retries, max cost.
- Do plan for degraded modes (smaller model, cached answers, “unable to answer”).

**Avoid**
- Avoid model sprawl (unowned variants with no eval coverage).
- Avoid blind upgrades based on anecdotal quality; require measured impact.
- Avoid training on production logs without consent, governance, and leakage controls.

## When to Use This Skill

Claude should invoke this skill when the user asks about:

- LLM preflight/project checklists, production best practices, or data pipelines
- Building or deploying RAG, agentic, or prompt-based LLM apps
- Prompt design, chain-of-thought (CoT), ReAct, or template patterns
- Troubleshooting LLM hallucination, bias, retrieval issues, or production failures
- Evaluating LLMs: benchmarks, multi-metric eval, or rollout/monitoring
- LLMOps: deployment, rollback, scaling, resource optimization
- Technology stack selection (models, vector DBs, frameworks)
- Production deployment strategies and operational patterns

---

## Scope Boundaries (Use These Skills for Depth)

- **Prompt design & CI/CD** → [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)
- **RAG pipelines & chunking** → [ai-rag](../ai-rag/SKILL.md)
- **Search tuning (BM25, HNSW, hybrid)** → [ai-rag](../ai-rag/SKILL.md)
- **Agent architectures & tools** → [ai-agents](../ai-agents/SKILL.md)
- **Serving optimization/quantization** → [ai-llm-inference](../ai-llm-inference/SKILL.md)
- **Production deployment/monitoring** → [ai-mlops](../ai-mlops/SKILL.md)
- **Security/guardrails** → [ai-mlops](../ai-mlops/SKILL.md)

---

## Resources (Best Practices & Operational Patterns)

Comprehensive operational guides with checklists, patterns, and decision frameworks:

### Core Operational Patterns

- **[Project Planning Patterns](resources/project-planning-patterns.md)** - Stack selection, FTI pipeline, performance budgeting
  - AI engineering stack selection matrix
  - Feature/Training/Inference (FTI) pipeline blueprint
  - Performance budgeting and goodput gates
  - Progressive complexity (prompt → RAG → fine-tune → hybrid)

- **[Production Checklists](resources/production-checklists.md)** - Pre-deployment validation and operational checklists
  - LLM lifecycle checklist (modern production standards)
  - Data & training, RAG pipeline, deployment & serving
  - Safety/guardrails, evaluation, agentic systems
  - Reliability & data infrastructure (DDIA-grade)
  - Weekly production tasks

- **[Common Design Patterns](resources/common-design-patterns.md)** - Copy-paste ready implementation examples
  - Chain-of-Thought (CoT) prompting
  - ReAct (Reason + Act) pattern
  - RAG pipeline (minimal to advanced)
  - Agentic planning loop
  - Self-reflection and multi-agent collaboration

- **[Decision Matrices](resources/decision-matrices.md)** - Quick reference tables for selection
  - RAG type decision matrix (naive → advanced → modular)
  - Production evaluation table with targets and actions
  - Model selection matrix (GPT-4, Claude, Gemini, self-hosted)
  - Vector database, embedding model, framework selection
  - Deployment strategy matrix

- **[Anti-Patterns](resources/anti-patterns.md)** - Common mistakes and prevention strategies
  - Data leakage, prompt dilution, RAG context overload
  - Agentic runaway, over-engineering, ignoring evaluation
  - Hard-coded prompts, missing observability
  - Detection methods and prevention code examples

### Domain-Specific Patterns

- **[LLMOps Best Practices](resources/llmops-best-practices.md)** - Operational lifecycle and deployment patterns
- **[Evaluation Patterns](resources/eval-patterns.md)** - Testing, metrics, and quality validation
- **[Prompt Engineering Patterns](resources/prompt-engineering-patterns.md)** - Quick reference (canonical skill: [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md))
- **[Agentic Patterns](resources/agentic-patterns.md)** - Quick reference (canonical skill: [ai-agents](../ai-agents/SKILL.md))
- **[RAG Best Practices](resources/rag-best-practices.md)** - Quick reference (canonical skill: [ai-rag](../ai-rag/SKILL.md))

**Note:** Each resource file includes preflight/validation checklists, copy-paste reference tables, inline templates, anti-patterns, and decision matrices.

---

## Templates (Copy-Paste Ready)

Production templates by use case and technology:

### Selection & Governance

- **[Model Selection Matrix](templates/selection/model-selection-matrix.md)** - Documented selection, scoring, licensing, and governance

### RAG Pipelines

- **[Basic RAG](templates/rag-pipelines/template-basic-rag.md)** - Simple retrieval-augmented generation
- **[Advanced RAG](templates/rag-pipelines/template-advanced-rag.md)** - Hybrid retrieval, reranking, contextual embeddings

### Prompt Engineering

- **[Chain-of-Thought](templates/prompt-engineering/template-cot.md)** - Step-by-step reasoning pattern
- **[ReAct](templates/prompt-engineering/template-react.md)** - Reason + Act for tool use

### Agentic Workflows

- **[Reflection Agent](templates/agentic-workflows/template-reflection.md)** - Self-critique and improvement
- **[Multi-Agent](templates/agentic-workflows/template-multi-agent.md)** - Manager-worker orchestration

### Data Pipelines

- **[Data Quality](templates/data-pipelines/template-data-quality.md)** - Validation, deduplication, PII detection

### Deployment

- **[LLM Deployment](templates/deployment/template-llm-deployment.md)** - Production deployment with monitoring

### Evaluation

- **[Multi-Metric Evaluation](templates/evaluation/template-multi-metric.md)** - Comprehensive testing suite

---

## Shared Utilities (Centralized patterns — extract, don't duplicate)

- [../software-clean-code-standard/utilities/llm-utilities.md](../software-clean-code-standard/utilities/llm-utilities.md) — Token counting, streaming, cost estimation
- [../software-clean-code-standard/utilities/error-handling.md](../software-clean-code-standard/utilities/error-handling.md) — Effect Result types, correlation IDs
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) — p-retry v6, circuit breaker for LLM API calls
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) — pino v9 + OpenTelemetry integration
- [../software-clean-code-standard/utilities/observability-utilities.md](../software-clean-code-standard/utilities/observability-utilities.md) — OpenTelemetry SDK, tracing, metrics
- [../software-clean-code-standard/utilities/config-validation.md](../software-clean-code-standard/utilities/config-validation.md) — Zod 3.24+, secrets management for API keys
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) — Test factories, fixtures, mocks
- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) — Canonical clean code rules (`CC-*`) for citation

---

## Related Skills

This skill integrates with complementary Claude Code skills:

### Core Dependencies

- **[ai-rag](../ai-rag/SKILL.md)** - Retrieval pipelines: chunking, hybrid search, reranking, evaluation
- **[ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)** - Systematic prompt design, evaluation, testing, and optimization
- **[ai-agents](../ai-agents/SKILL.md)** - Agent architectures, tool use, multi-agent systems, autonomous workflows

### Production & Operations

- **[ai-llm-inference](../ai-llm-inference/SKILL.md)** - Production serving, quantization, batching, GPU optimization
- **[ai-mlops](../ai-mlops/SKILL.md)** - Deployment, monitoring, incident response, security, and governance

---

## External Resources

See **[data/sources.json](data/sources.json)** for 50+ curated authoritative sources:

- **Official LLM platform docs** - OpenAI, Anthropic, Gemini, Mistral, Azure OpenAI, AWS Bedrock
- **Open-source models and frameworks** - HuggingFace Transformers, open-weight models, PEFT/LoRA, distributed training/inference stacks
- **RAG frameworks and vector DBs** - LlamaIndex, LangChain 1.2+, LangGraph, LangGraph Studio v2, Haystack, Pinecone, Qdrant, Chroma
- **Agent frameworks (examples)** - LangGraph, Semantic Kernel, AutoGen, CrewAI
- **RAG innovations (examples)** - Graph-based retrieval, hybrid retrieval, online evaluation loops
- **Prompt engineering** - Anthropic Prompt Library, Prompt Engineering Guide, CoT/ReAct patterns
- **Evaluation and monitoring** - OpenAI Evals, HELM, Anthropic Evals, LangSmith, W&B, Arize Phoenix
- **Production deployment** - Model gateways/routers, self-hosted serving, managed endpoints

---

## Usage

### For New Projects

1. Start with **[Production Checklists](resources/production-checklists.md)** - Validate all pre-deployment requirements
2. Use **[Decision Matrices](resources/decision-matrices.md)** - Select technology stack
3. Reference **[Project Planning Patterns](resources/project-planning-patterns.md)** - Design FTI pipeline
4. Implement with **[Common Design Patterns](resources/common-design-patterns.md)** - Copy-paste code examples
5. Avoid **[Anti-Patterns](resources/anti-patterns.md)** - Learn from common mistakes

### For Troubleshooting

1. Check **[Anti-Patterns](resources/anti-patterns.md)** - Identify failure modes and mitigations
2. Use **[Decision Matrices](resources/decision-matrices.md)** - Evaluate if architecture fits use case
3. Reference **[Common Design Patterns](resources/common-design-patterns.md)** - Verify implementation correctness

### For Ongoing Operations

1. Follow **[Production Checklists](resources/production-checklists.md)** - Weekly operational tasks
2. Integrate **[Evaluation Patterns](resources/eval-patterns.md)** - Continuous quality monitoring
3. Apply **[LLMOps Best Practices](resources/llmops-best-practices.md)** - Deployment and rollback procedures

---

## Navigation Summary

**Quick Decisions:** [Decision Matrices](resources/decision-matrices.md)
**Pre-Deployment:** [Production Checklists](resources/production-checklists.md)
**Planning:** [Project Planning Patterns](resources/project-planning-patterns.md)
**Implementation:** [Common Design Patterns](resources/common-design-patterns.md)
**Troubleshooting:** [Anti-Patterns](resources/anti-patterns.md)

**Domain Depth:** [LLMOps](resources/llmops-best-practices.md) | [Evaluation](resources/eval-patterns.md) | [Prompts](resources/prompt-engineering-patterns.md) | [Agents](resources/agentic-patterns.md) | [RAG](resources/rag-best-practices.md)

**Templates:** [templates/](templates/) - Copy-paste ready production code

**Sources:** [data/sources.json](data/sources.json) - Authoritative documentation links

---
