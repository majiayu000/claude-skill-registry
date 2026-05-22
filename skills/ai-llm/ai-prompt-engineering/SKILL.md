---
name: ai-prompt-engineering
description: Operational prompt engineering patterns, templates, and validation flows for Claude Code.
---

# Prompt Engineering — Operational Skill

**Modern Best Practices (December 2025)**: versioned prompts, explicit output contracts, regression tests, and safety threat modeling for tool/RAG prompts (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

This skill provides **operational guidance** for building production-ready prompts across standard tasks, RAG workflows, agent orchestration, structured outputs, hidden reasoning, and multi-step planning.

All content is **operational**, not theoretical. Focus on patterns, checklists, and copy-paste templates.

**Claude 4+ Updates**: This skill includes Claude 4.x and 4.5-specific optimizations:

- **Action directives**: Frame for implementation, not suggestions
- **Parallel tool execution**: Independent tool calls can run simultaneously
- **Long-horizon task management**: State tracking, incremental progress, context compaction resilience
- **Positive framing**: Describe desired behavior rather than prohibitions
- **Style matching**: Prompt formatting influences output style
- **Domain-specific patterns**: Specialized guidance for frontend, research, and agentic coding
- **Style-adversarial resilience**: Stress-test refusals with poetic/role-play rewrites; normalize or decline stylized harmful asks before tool use

**Claude 4.5 Communication**: Claude 4.5 is more concise by default. Request explicit summaries when needed for visibility into reasoning or work completed.

---

## When to Use This Skill

**Activate this skill when the user asks to**:

- Write or improve a production-ready prompt
- Debug prompt failures or inconsistent outputs
- Create structured outputs (JSON, tables, schemas)
- Build deterministic extractors
- Design RAG pipelines with context grounding
- Implement agent workflows with tool calling
- Add hidden reasoning (CoT) without visible output
- Convert user tasks into reusable templates
- Validate prompt quality against operational checklists
- Standardize output formats across systems

**Do NOT use this skill for**:

- LLM theory or model architecture explanations
- General educational content about AI
- Historical background on prompt engineering

**See Also**: For specialized AI/LLM implementations, see "Related Skills" section at the end of this document.

---

## Quick Reference

| Task | Pattern to Use | Key Components | When to Use |
|------|----------------|----------------|-------------|
| **Machine-parseable output** | Structured Output | JSON schema, "JSON-only" directive, no prose | API integrations, data extraction |
| **Field extraction** | Deterministic Extractor | Exact schema, missing→null, no transformations | Form data, invoice parsing |
| **Use retrieved context** | RAG Workflow | Context relevance check, chunk citations, explicit missing info | Knowledge bases, documentation search |
| **Internal reasoning** | Hidden Chain-of-Thought | Internal reasoning, final answer only | Classification, complex decisions |
| **Tool-using agent** | Tool/Agent Planner | Plan-then-act, one tool per turn | Multi-step workflows, API calls |
| **Text transformation** | Rewrite + Constrain | Style rules, meaning preservation, format spec | Content adaptation, summarization |
| **Classification** | Decision Tree | Ordered branches, mutually exclusive, JSON result | Routing, categorization, triage |

---

## Decision Tree: Choosing the Right Pattern

```text
User needs: [Prompt Type]
    ├─ Output must be machine-readable?
    │   ├─ Extract specific fields only? → **Deterministic Extractor Pattern**
    │   └─ Generate structured data? → **Structured Output Pattern (JSON)**
    │
    ├─ Use external knowledge?
    │   └─ Retrieved context must be cited? → **RAG Workflow Pattern**
    │
    ├─ Requires reasoning but hide process?
    │   └─ Classification or decision task? → **Hidden Chain-of-Thought Pattern**
    │
    ├─ Needs to call external tools/APIs?
    │   └─ Multi-step workflow? → **Tool/Agent Planner Pattern**
    │
    ├─ Transform existing text?
    │   └─ Style/format constraints? → **Rewrite + Constrain Pattern**
    │
    └─ Classify or route to categories?
        └─ Mutually exclusive rules? → **Decision Tree Pattern**
```

---

## Core Concepts vs Implementation Practices

### Core Concepts (Vendor-Agnostic)

- **Prompt contract**: inputs, allowed tools, output schema, max tokens, and refusal rules.
- **Determinism controls**: temperature/top_p, constrained decoding/structured outputs, and strict formatting.
- **Cost & latency budgets**: prompt length and max output drive tokens and tail latency; enforce hard limits and measure p95/p99.
- **Evaluation**: golden sets + regression gates + A/B + post-deploy monitoring.
- **Security**: prompt injection, data exfiltration, and tool misuse are primary threats (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

### Implementation Practices (Model/Platform-Specific)

- Use model-specific structured output features when available; keep a schema validator as the source of truth.
- Align tracing/metrics with OpenTelemetry GenAI semantic conventions (https://opentelemetry.io/docs/specs/semconv/gen-ai/).

## Do / Avoid

**Do**
- Do keep prompts small and modular; centralize shared fragments (policies, schemas, style).
- Do add a prompt eval harness and block merges on regressions.
- Do prefer “brief justification” over requesting chain-of-thought; treat hidden reasoning as model-internal.

**Avoid**
- Avoid prompt sprawl (many near-duplicates with no owner or tests).
- Avoid brittle multi-step chains without intermediate validation.
- Avoid mixing policy and product copy in the same prompt (harder to audit and update).

## Navigation: Core Patterns

- **[Core Patterns](resources/core-patterns.md)** - 7 production-grade prompt patterns
  - Structured Output (JSON), Deterministic Extractor, RAG Workflow
  - Hidden Chain-of-Thought, Tool/Agent Planner, Rewrite + Constrain, Decision Tree
  - Each pattern includes structure template and validation checklist

## Navigation: Best Practices

- **[Best Practices (Core)](resources/best-practices-core.md)** - Foundation rules for production-grade prompts
  - System instruction design, output contract specification, action directives
  - Context handling, error recovery, positive framing, style matching, style-adversarial red teaming
  - Anti-patterns, Claude 4+ specific optimizations

- **[Production Guidelines](resources/production-guidelines.md)** - Deployment and operational guidance
  - Evaluation & testing (Prompt CI/CD), model parameters, few-shot selection
  - Safety & guardrails, conversation memory, context compaction resilience
  - Answer engineering, decomposition, multilingual/multimodal, benchmarking

- **[Quality Checklists](resources/quality-checklists.md)** - Validation checklists before deployment
  - Prompt QA, JSON validation, agent workflow checks
  - RAG workflow, safety & security, performance optimization
  - Testing coverage, anti-patterns, quality score rubric

- **[Domain-Specific Patterns](resources/domain-specific-patterns.md)** - Claude 4+ optimized patterns for specialized domains
  - Frontend/visual code: Creativity encouragement, design variations, micro-interactions
  - Research tasks: Success criteria, verification, hypothesis tracking
  - Agentic coding: No speculation rule, principled implementation, investigation patterns
  - Cross-domain best practices and quality modifiers

## Navigation: Specialized Patterns

- **[RAG Patterns](resources/rag-patterns.md)** - Retrieval-augmented generation workflows
  - Context grounding, chunk citation, missing information handling

- **[Agent and Tool Patterns](resources/agent-patterns.md)** - Tool use and agent orchestration
  - Plan-then-act workflows, tool calling, multi-step reasoning, generate–verify–revise chains with role-play + few-shot + targeted CoT per sub-agent

- **[Extraction Patterns](resources/extraction-patterns.md)** - Deterministic field extraction
  - Schema-based extraction, null handling, no hallucinations

- **[Reasoning Patterns (Hidden CoT)](resources/reasoning-patterns.md)** - Internal reasoning without visible output
  - Hidden reasoning, final answer only, classification workflows

- **[Additional Patterns](resources/additional-patterns.md)** - Extended prompt engineering techniques
  - Advanced patterns, edge cases, optimization strategies

---

## Navigation: Templates

Templates are copy-paste ready and organized by complexity:

### Quick Templates

- **[Quick Template](templates/quick/template-quick.md)** - Fast, minimal prompt structure

### Standard Templates

- **[Standard Template](templates/standard/template-standard.md)** - Production-grade operational prompt
- **[Agent Template](templates/standard/template-agent.md)** - Tool-using agent with planning
- **[RAG Template](templates/standard/template-rag.md)** - Retrieval-augmented generation
- **[Chain-of-Thought Template](templates/standard/template-cot.md)** - Hidden reasoning pattern
- **[JSON Extractor Template](templates/standard/template-json-extractor.md)** - Deterministic field extraction
- **[Prompt Evaluation Template](templates/eval/prompt-eval-template.md)** - Regression tests, A/B testing, rollout gates

---

## External Resources

External references are listed in [data/sources.json](data/sources.json):

- Official documentation (OpenAI, Anthropic, Google)
- LLM frameworks (LangChain, LlamaIndex)
- Vector databases (Pinecone, Weaviate, FAISS)
- Evaluation tools (OpenAI Evals, HELM)
- Safety guides and standards
- RAG and retrieval resources

---

## Related Skills

This skill provides foundational prompt engineering patterns. For specialized implementations:

**AI/LLM Skills**:

- [AI Agents Development](../ai-agents/SKILL.md) - Production agent patterns, MCP integration, orchestration
- [AI LLM Engineering](../ai-llm/SKILL.md) - LLM application architecture and deployment
- [AI LLM RAG Engineering](../ai-rag/SKILL.md) - Advanced RAG pipelines and chunking strategies
- [AI LLM Search & Retrieval](../ai-rag/SKILL.md) - Search optimization, hybrid retrieval, reranking
- [AI LLM Development](../ai-llm/SKILL.md) - Fine-tuning, evaluation, dataset creation

**Software Development Skills**:

- [Software Architecture Design](../software-architecture-design/SKILL.md) - System design patterns
- [Software Backend](../software-backend/SKILL.md) - Backend implementation
- [Foundation API Design](../dev-api-design/SKILL.md) - API design and contracts

---

## Usage Notes

**For Claude Code**:

- Reference this skill when building prompts for agents, commands, or integrations
- Use Quick Reference table for fast pattern lookup
- Follow Decision Tree to select appropriate pattern
- Validate outputs with Quality Checklists before deployment
- Use templates as starting points, customize for specific use cases
