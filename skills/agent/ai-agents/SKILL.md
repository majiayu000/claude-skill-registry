---
name: ai-agents
description: Production-grade AI agent patterns with MCP integration, agentic RAG, handoff orchestration, multi-layer guardrails, and observability (modern best practices)
---

# AI Agents Development — Production Skill Hub

**Modern Best Practices (December 2025)**: deterministic control flow, bounded tools, auditable state, MCP-based tool integration, handoff-first orchestration, multi-layer guardrails, OpenTelemetry tracing, and human-in-the-loop controls (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

This skill provides **production-ready operational patterns** for designing, building, evaluating, and deploying AI agents.
It centralizes **procedures**, **checklists**, **decision rules**, and **templates** used across RAG agents, tool-using agents, OS agents, and multi-agent systems.

No theory. No narrative. Only what Claude can execute.

---

## When to Use This Skill

Claude should activate this skill whenever the user asks for:

- Designing an agent (LLM-based, tool-based, OS-based, or multi-agent).
- Scoping capability maturity and rollout risk for new agent behaviors.
- Creating action loops, plans, workflows, or delegation logic.
- Writing tool definitions, MCP tools, schemas, or validation logic.
- Generating RAG pipelines, retrieval modules, or context injection.
- Building memory systems (session, long-term, episodic, task).
- Creating evaluation harnesses, observability plans, or safety gates.
- Preparing CI/CD, rollout, deployment, or production operational specs.
- Producing any template in `/resources/` or `/templates/`.
- Implementing MCP servers or integrating Model Context Protocol.
- Setting up agent handoffs and orchestration patterns.
- Configuring multi-layer guardrails and safety controls.
- For prompt scaffolds, retrieval tuning, or security depth, see Scope Boundaries below.

## Scope Boundaries (Use These Skills for Depth)

- **Prompt scaffolds & structured outputs** → [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)
- **RAG retrieval & chunking** → [ai-rag](../ai-rag/SKILL.md)
- **Search tuning (BM25/HNSW/hybrid)** → [ai-rag](../ai-rag/SKILL.md)
- **Security/guardrails** → [ai-mlops](../ai-mlops/SKILL.md)
- **Inference optimization** → [ai-llm-inference](../ai-llm-inference/SKILL.md)

---

## Quick Reference

| Agent Type | Core Control Flow | Interfaces | MCP/A2A | When to Use |
|------------|-----------|------------|---------|-------------|
| **Workflow Agent (FSM/DAG)** | Explicit state transitions | State store, tool allowlist | MCP | Deterministic, auditable flows |
| **Tool-Using Agent** | Route → call tool → observe | Tool schemas, retries/timeouts | MCP | External actions (APIs, DB, files) |
| **RAG Agent** | Retrieve → answer → cite | Retriever, citations, ACLs | MCP | Knowledge-grounded responses |
| **Planner/Executor** | Plan → execute steps with caps | Planner prompts, step budget | MCP (+A2A) | Multi-step problems with bounded autonomy |
| **Multi-Agent (Orchestrated)** | Delegate → merge → validate | Handoff contracts, eval gates | A2A | Specialization with explicit handoffs |
| **OS Agent** | Observe UI → act → verify | Sandbox, UI grounding | MCP | Desktop/browser control under strict guardrails |
| **Code/SWE Agent** | Branch → edit → test → PR | Repo access, CI gates | MCP | Coding tasks with review/merge controls |

---

## Decision Tree: Choosing Agent Architecture

```text
What does the agent need to do?
    ├─ Answer questions from knowledge base?
    │   ├─ Simple lookup? → RAG Agent (LangChain/LlamaIndex + vector DB)
    │   └─ Complex multi-step? → Agentic RAG (iterative retrieval + reasoning)
    │
    ├─ Perform external actions (APIs, tools, functions)?
    │   ├─ 1-3 tools, linear flow? → Tool-Using Agent (LangGraph + MCP)
    │   └─ Complex workflows, branching? → Planning Agent (ReAct/Plan-Execute)
    │
    ├─ Write/modify code autonomously?
    │   ├─ Single file edits? → Tool-Using Agent with code tools
    │   └─ Multi-file, issue resolution? → Code/SWE Agent (HyperAgent pattern)
    │
    ├─ Delegate tasks to specialists?
    │   ├─ Fixed workflow? → Multi-Agent Sequential (A → B → C)
    │   ├─ Manager-Worker? → Multi-Agent Hierarchical (Manager + Workers)
    │   └─ Dynamic routing? → Multi-Agent Group Chat (collaborative)
    │
    ├─ Control desktop/browser?
    │   └─ OS Agent (Anthropic Computer Use + MCP for system access)
    │
    └─ Hybrid (combination of above)?
        └─ Planning Agent that coordinates:
            - Tool-using for actions (MCP)
            - RAG for knowledge (MCP)
            - Multi-agent for delegation (A2A)
            - Code agents for implementation
```

**Protocol Selection**:

- Use **MCP** for: Tool access, data retrieval, single-agent integration
- Use **A2A** for: Agent-to-agent handoffs, multi-agent coordination, task delegation

---

## Core Concepts (Vendor-Agnostic)

### Control Flow Options

- **Reactive**: direct tool routing per user request (fast, brittle if unbounded).
- **Workflow (FSM/DAG)**: explicit states and transitions (default for deterministic production).
- **Planner/Executor**: plan with strict budgets, then execute step-by-step (use when branching is unavoidable).
- **Orchestrated multi-agent**: separate roles with validated handoffs (use when specialization is required).

### Memory Types (Tradeoffs)

- **Short-term (session)**: cheap, ephemeral; best for conversational continuity.
- **Episodic (task)**: scoped to a case/ticket; supports audit and replay.
- **Long-term (profile/knowledge)**: high risk; requires consent, retention limits, and provenance.

### Failure Handling (Production Defaults)

- **Classify errors**: retriable vs fatal vs needs-human.
- **Bound retries**: max attempts, backoff, jitter; avoid retry storms.
- **Fallbacks**: degraded mode, smaller model, cached answers, or safe refusal.

## Do / Avoid

**Do**
- Do keep state explicit and serializable (replayable runs).
- Do enforce tool allowlists, scopes, and idempotency for side effects.
- Do log traces/metrics for model calls and tool calls (OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/).

**Avoid**
- Avoid runaway autonomy (unbounded loops or step counts).
- Avoid hidden state (implicit memory that cannot be audited).
- Avoid untrusted tool outputs without validation/sanitization.

## Navigation: Core Concepts & Patterns

### Governance & Maturity

- **Agent Maturity & Governance** - [`resources/agent-maturity-governance.md`](resources/agent-maturity-governance.md)
  - Capability maturity levels (L0-L4)
  - Identity & policy enforcement
  - Fleet control and registry management
  - Deprecation rules and kill switches

### Modern Best Practices

- **Modern Best Practices** - [`resources/modern-best-practices.md`](resources/modern-best-practices.md)
  - Model Context Protocol (MCP)
  - Agent-to-Agent Protocol (A2A)
  - Agentic RAG (Dynamic Retrieval)
  - Multi-layer guardrails
  - LangGraph over LangChain
  - OpenTelemetry for agents

### Context Management

- **Context Engineering** - [`resources/context-engineering.md`](resources/context-engineering.md)
  - Progressive disclosure
  - Session management
  - Memory provenance
  - Retrieval timing
  - Multimodal context

### Core Operational Patterns

- **Operational Patterns** - [`resources/operational-patterns.md`](resources/operational-patterns.md)
  - Agent loop pattern (PLAN → ACT → OBSERVE → UPDATE)
  - OS agent action loop
  - RAG pipeline pattern
  - Tool specification
  - Memory system pattern
  - Multi-agent workflow
  - Safety & guardrails
  - Observability
  - Evaluation patterns
  - Deployment & CI/CD

---

## Navigation: Protocol Implementation

- **MCP Practical Guide** - [`resources/mcp-practical-guide.md`](resources/mcp-practical-guide.md)
  Building MCP servers, tool integration, and standardized data access

- **MCP Server Builder** - [`resources/mcp-server-builder.md`](resources/mcp-server-builder.md)
  End-to-end checklist for workflow-focused MCP servers (design → build → test)

- **A2A Handoff Patterns** - [`resources/a2a-handoff-patterns.md`](resources/a2a-handoff-patterns.md)
  Agent-to-agent communication, task delegation, and coordination protocols

- **Protocol Decision Tree** - [`resources/protocol-decision-tree.md`](resources/protocol-decision-tree.md)
  When to use MCP vs A2A, decision framework, and selection criteria

---

## Navigation: Agent Capabilities

- **Agent Operations** - [`resources/agent-operations-best-practices.md`](resources/agent-operations-best-practices.md)
  Action loops, planning, observation, and execution patterns

- **RAG Patterns** - [`resources/rag-patterns.md`](resources/rag-patterns.md)
  Contextual retrieval, agentic RAG, and hybrid search strategies

- **Memory Systems** - [`resources/memory-systems.md`](resources/memory-systems.md)
  Session, long-term, episodic, and task memory architectures

- **Tool Design & Validation** - [`resources/tool-design-specs.md`](resources/tool-design-specs.md)
  Tool schemas, validation, error handling, and MCP integration

### Skill Packaging & Sharing

- **Skill Lifecycle** - [`resources/skill-lifecycle.md`](resources/skill-lifecycle.md)
  Scaffold, validate, package, and share Claude skills with teams (Slack-ready)

- **API Contracts for Agents** - [`resources/api-contracts-for-agents.md`](resources/api-contracts-for-agents.md)
  Request/response envelopes, safety gates, streaming/async patterns, error taxonomy

- **Multi-Agent Patterns** - [`resources/multi-agent-patterns.md`](resources/multi-agent-patterns.md)
  Manager-worker, sequential, handoff, and group chat orchestration

- **OS Agent Capabilities** - [`resources/os-agent-capabilities.md`](resources/os-agent-capabilities.md)
  Desktop automation, UI grounding, and computer use patterns

- **Code/SWE Agents** - [`resources/code-swe-agents.md`](resources/code-swe-agents.md)
  SE 3.0 paradigm, autonomous coding patterns, SWE-Bench, HyperAgent architecture

---

## Navigation: Production Operations

- **Evaluation & Observability** - [`resources/evaluation-and-observability.md`](resources/evaluation-and-observability.md)
  OpenTelemetry GenAI, metrics, LLM-as-judge, and monitoring

- **Deployment, CI/CD & Safety** - [`resources/deployment-ci-cd-and-safety.md`](resources/deployment-ci-cd-and-safety.md)
  Multi-layer guardrails, HITL controls, NIST AI RMF, production checklists

---

## Navigation: Templates (Copy-Paste Ready)

### Checklists

- **Agent Design & Safety Checklist** - [`templates/checklists/agent-safety-checklist.md`](templates/checklists/agent-safety-checklist.md)
  Go/No-Go safety gate: permissions, HITL triggers, eval gates, observability, rollback

### Core Agent Templates

- **Standard Agent Template** - [`templates/core/agent-template-standard.md`](templates/core/agent-template-standard.md)
  Full production spec: memory, tools, RAG, evaluation, observability, safety

- **Specialized Agent Template** - [`templates/core/agent-template-specialized.md`](templates/core/agent-template-specialized.md)
  Domain-specific agents with custom capabilities and constraints

- **Quick Agent Template** - [`templates/core/agent-template-quick.md`](templates/core/agent-template-quick.md)
  Minimal viable agent for rapid prototyping

### RAG Templates

- **Basic RAG** - [`templates/rag/rag-basic.md`](templates/rag/rag-basic.md)
  Simple retrieval-augmented generation pipeline

- **Advanced RAG** - [`templates/rag/rag-advanced.md`](templates/rag/rag-advanced.md)
  Contextual retrieval, reranking, and agentic RAG patterns

- **Hybrid Retrieval** - [`templates/rag/hybrid-retrieval.md`](templates/rag/hybrid-retrieval.md)
  Semantic + keyword search with BM25 fusion

### Tool Templates

- **Tool Definition** - [`templates/tools/tool-definition.md`](templates/tools/tool-definition.md)
  MCP-compatible tool schemas with validation and error handling

- **Tool Validation Checklist** - [`templates/tools/tool-validation-checklist.md`](templates/tools/tool-validation-checklist.md)
  Testing, security, and production readiness checks

### Multi-Agent Templates

- **Manager-Worker Template** - [`templates/multi-agent/manager-worker-template.md`](templates/multi-agent/manager-worker-template.md)
  Orchestration pattern with task delegation and result aggregation

- **Evaluator-Router Template** - [`templates/multi-agent/evaluator-router-template.md`](templates/multi-agent/evaluator-router-template.md)
  Dynamic routing with quality assessment and domain classification

### Service Layer Templates

- **FastAPI Agent Service** - [`../dev-api-design/templates/fastapi/fastapi-complete-api.md`](../dev-api-design/templates/fastapi/fastapi-complete-api.md)
  Auth, pagination, validation, error handling; extend with model lifespan loads, SSE, background tasks

---

## External Sources Metadata

- **Curated References** - [`data/sources.json`](data/sources.json)
  Authoritative sources spanning standards, protocols, and production agent frameworks

---

## Shared Utilities (Centralized patterns — extract, don't duplicate)

- [../software-clean-code-standard/utilities/llm-utilities.md](../software-clean-code-standard/utilities/llm-utilities.md) — Token counting, streaming, cost estimation
- [../software-clean-code-standard/utilities/error-handling.md](../software-clean-code-standard/utilities/error-handling.md) — Effect Result types, correlation IDs
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) — p-retry v6, circuit breaker for API calls
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) — pino v9 + OpenTelemetry integration
- [../software-clean-code-standard/utilities/observability-utilities.md](../software-clean-code-standard/utilities/observability-utilities.md) — OpenTelemetry SDK, tracing, metrics
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) — Test factories, fixtures, mocks
- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) — Canonical clean code rules (`CC-*`) for citation

---

## Related Skills

This skill integrates with complementary Claude Code skills:

### Core Dependencies

- [`../ai-llm/`](../ai-llm/SKILL.md) - LLM patterns, prompt engineering, and model selection for agents
- [`../ai-rag/`](../ai-rag/SKILL.md) - Deep RAG implementation: chunking, embedding, reranking
- [`../ai-prompt-engineering/`](../ai-prompt-engineering/SKILL.md) - System prompt design, few-shot patterns, reasoning strategies

### Production & Operations

- [`../qa-observability/`](../qa-observability/SKILL.md) - OpenTelemetry, metrics, distributed tracing
- [`../software-security-appsec/`](../software-security-appsec/SKILL.md) - OWASP Top 10, input validation, secure tool design
- [`../ops-devops-platform/`](../ops-devops-platform/SKILL.md) - CI/CD pipelines, deployment strategies, infrastructure

### Supporting Patterns

- [`../dev-api-design/`](../dev-api-design/SKILL.md) - REST/GraphQL design for agent APIs and tool interfaces
- [`../ai-mlops/`](../ai-mlops/SKILL.md) - Model deployment, monitoring, drift detection
- [`../qa-debugging/`](../qa-debugging/SKILL.md) - Agent debugging, error analysis, root cause investigation

**Usage pattern**: Start here for agent architecture, then reference specialized skills for deep implementation details.

---

## Usage Notes for Claude

- **Modern Standards**: Default to MCP for tools, agentic RAG for retrieval, handoff-first for multi-agent
- **Lightweight SKILL.md**: Use this file for quick reference and navigation
- **Drill-down resources**: Reference detailed resources for implementation guidance
- **Copy-paste templates**: Use templates when the user asks for structured artifacts
- **External sources**: Reference `data/sources.json` for authoritative documentation links
- **No theory**: Never include theoretical explanations; only operational steps

---

## Key Modern Migrations

**Traditional → Modern**:

- Custom APIs → Model Context Protocol (MCP)
- Static RAG → Agentic RAG with contextual retrieval
- Ad-hoc handoffs → Versioned handoff APIs with JSON Schema
- Single guardrail → Multi-layer defense (5+ layers)
- LangChain agents → LangGraph stateful workflows
- Custom observability → OpenTelemetry GenAI standards
- Model-centric → Context engineering-centric

---

## AI-Native SDLC Pattern (Delegate → Review → Own)

- **Plan**: Have the agent draft `PLAN.md` or use a planning tool; require code-path trace, dependency map, and risk/edge-case list before build starts.
- **Design**: Convert mocks to components; enforce design tokens/style guides; surface accessibility gaps; keep MCP-linked component libraries in context.
- **Build**: Let the agent scaffold end-to-end (models/APIs/UI/tests/docs); enforce long-run guardrails (time cap, allowed commands/tools, commit/PR gating, kill switch).
- **Test**: Demand failing test first; agent generates and runs suites; require coverage deltas and flaky-test notes; human reviews assertions and fixtures.
- **Review**: Agent runs first-pass review tuned for P0/P1; human focuses on architecture, performance, safety, and migration risk; always own final merge.
- **Document**: Agent drafts PR summaries, module/file notes, and mermaid diagrams; require doc updates in the same run; human adds “why” and approvals.
- **Deploy & Maintain**: Agent links logs/metrics via MCP for triage; propose hotfixes with rollback plans; human approves rollouts; track drift/regressions with evals.

## Executive Briefing (Optional)

- **Value**: Coding agents compress SDLC time; delegate mechanical work, keep humans on intent/architecture; measurable gains come from tight guardrails plus eval loops.
- **Cost & Risk**: Training vs inference economics; long runs need caps/kill switches; data/secret handling and supply-chain policies stay human-owned.
- **Governance**: Multi-layer guardrails (policy prompt, tool allowlist, auth scopes, eval gates, audit logs); require human sign-off for deploys and safety-sensitive changes.
