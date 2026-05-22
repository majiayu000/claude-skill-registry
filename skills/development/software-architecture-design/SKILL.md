---
name: software-architecture-design
description: System design, architecture patterns, scalability tradeoffs, and distributed systems for production-grade software. Covers microservices, event-driven, CQRS, modular monoliths, and reliability patterns.
---

# Software Architecture Design — Quick Reference

Use this skill for **system-level design decisions** rather than implementation details within a single service or component.

## Quick Reference

| Task | Pattern/Tool | Key Resources | When to Use |
|------|-------------|---------------|-------------|
| Choose architecture style | Layered, Microservices, Event-driven, Serverless | [modern-patterns.md](resources/modern-patterns.md) | Greenfield projects, major refactors |
| Design for scale | Load balancing, Caching, Sharding, Read replicas | [scalability-reliability-guide.md](resources/scalability-reliability-guide.md) | High-traffic systems, performance goals |
| Ensure resilience | Circuit breakers, Retries, Bulkheads, Graceful degradation | [modern-patterns.md](resources/modern-patterns.md) | Distributed systems, external dependencies |
| Document decisions | Architecture Decision Record (ADR) | [adr-template.md](templates/planning/adr-template.md) | Major technical decisions, tradeoff analysis |
| Define service boundaries | Domain-Driven Design (DDD), Bounded contexts | [microservices-template.md](templates/patterns/microservices-template.md) | Microservices decomposition |
| Model data consistency | ACID vs BASE, Event sourcing, CQRS, Saga patterns | [event-driven-template.md](templates/patterns/event-driven-template.md) | Multi-service transactions |
| Plan observability | SLIs/SLOs/SLAs, Distributed tracing, Metrics, Logs | [architecture-blueprint.md](templates/planning/architecture-blueprint.md) | Production readiness |

## When to Use This Skill

Invoke when working on:

- **System decomposition**: Deciding between monolith, modular monolith, microservices
- **Architecture patterns**: Event-driven, CQRS, layered, hexagonal, serverless
- **Data architecture**: Consistency models, sharding, replication, CQRS patterns
- **Scalability design**: Load balancing, caching strategies, database scaling
- **Resilience patterns**: Circuit breakers, retries, bulkheads, graceful degradation
- **API contracts**: Service boundaries, versioning, integration patterns
- **Architecture decisions**: ADRs, tradeoff analysis, technology selection

## Decision Tree: Choosing Architecture Pattern

```text
Project needs: [New System or Major Refactor]
    ├─ Single team, evolving domain?
    │   ├─ Start simple → Modular Monolith (clear module boundaries)
    │   └─ Need rapid iteration → Layered Architecture
    │
    ├─ Multiple teams, clear bounded contexts?
    │   ├─ Independent deployment critical → Microservices
    │   └─ Shared data model → Modular Monolith with service modules
    │
    ├─ Event-driven workflows?
    │   ├─ Asynchronous processing → Event-Driven Architecture (Kafka, queues)
    │   └─ Complex state machines → Saga pattern + Event Sourcing
    │
    ├─ Variable/unpredictable load?
    │   ├─ Pay-per-use model → Serverless (AWS Lambda, Cloudflare Workers)
    │   └─ Batch processing → Serverless + queues
    │
    └─ High consistency requirements?
        ├─ Strong ACID guarantees → Monolith or Modular Monolith
        └─ Distributed data → CQRS + Event Sourcing
```

**Decision Factors:**

- Team size and structure (Conway's Law)
- Deployment independence needs
- Consistency vs availability tradeoffs (CAP theorem)
- Operational maturity (monitoring, orchestration)

See [resources/modern-patterns.md](resources/modern-patterns.md) for detailed pattern descriptions.

---

## Modern Architecture Patterns (Dec 2025)

### Data Mesh Architecture

Use when data silos impede cross-functional analytics.

**Principles:**

- Domain-oriented data ownership
- Data as a product
- Self-serve data platform
- Federated computational governance

| Do | Avoid |
|----|-------|
| Assign data ownership to domain teams | Centralized data lake without ownership |
| Publish data with SLAs and documentation | Schema changes without consumer notification |
| Use standard interfaces (APIs, SQL) | Proprietary formats without discoverability |

### Composable Architecture

Use when business demands rapid capability assembly.

**Characteristics:**

- Packaged business capabilities (PBCs)
- API-first integration
- Low-code/no-code composition layer
- Event-driven coordination

| Do | Avoid |
|----|-------|
| Design components with clear contracts | Tightly coupled monolithic modules |
| Use standard protocols (REST, GraphQL, gRPC) | Custom integration patterns |
| Enable runtime composition | Build-time-only assembly |

### Continuous Architecture

Architecture evolves with software, not separate from it.

**Practices:**

- Just-enough upfront design
- Delay decisions to responsible moment
- Architect roles on delivery teams
- Architecture fitness functions (automated checks)

### Edge Computing Patterns

Use when latency or bandwidth constraints require local processing.

| Pattern | Use Case |
|---------|----------|
| Edge gateway | Protocol translation, local caching |
| Edge compute workloads | Validation, transforms, local control loops |
| Edge-cloud hybrid | Local processing, cloud aggregation |

### Platform Engineering

Internal developer platforms (IDPs) for self-service infrastructure.

**Components:**

- Service catalog (Backstage, Port)
- Golden paths (templates, scaffolding)
- Developer portals (documentation, APIs)
- Self-service infrastructure (Terraform, Crossplane)

---

### Optional: AI/Automation Extensions

> **Note**: This section covers AI-specific architectural patterns. Skip if building traditional systems.

#### RAG Architecture Patterns

Retrieval-Augmented Generation for enterprise AI.

| Component | Purpose |
|-----------|---------|
| Vector store | Embedding storage (Pinecone, Weaviate, pgvector) |
| Retriever | Semantic search over documents |
| Generator | LLM produces responses with context |
| Orchestrator | Chains retrieval and generation |

#### Agentic AI Architecture

Multi-agent systems for autonomous workflows.

| Pattern | Description |
|---------|-------------|
| Single agent | One LLM with tools |
| Multi-agent | Specialized agents with coordination |
| Hierarchical | Manager agent delegates to workers |
| Decentralized | Peer agents negotiate tasks |

**Anti-patterns:**

- Unbounded agent loops without termination
- Missing human-in-the-loop for critical decisions
- No observability into agent actions

---

## Navigation

### Core Resources

- [resources/modern-patterns.md](resources/modern-patterns.md) — 10 contemporary architecture patterns with decision trees (microservices, event-driven, serverless, CQRS, modular monolith, service mesh, edge computing)
- [resources/scalability-reliability-guide.md](resources/scalability-reliability-guide.md) — CAP theorem, database scaling, caching strategies, circuit breakers, SRE patterns, observability
- [data/sources.json](data/sources.json) — 42 curated external resources (AWS, Azure, Google Cloud, Martin Fowler, microservices.io, SRE books, 2024-2025 best practices)

### Templates

**Planning & Documentation** ([templates/planning/](templates/planning/)):

- [templates/planning/architecture-blueprint.md](templates/planning/architecture-blueprint.md) — Service blueprint template (dependencies, SLAs, data flows, resilience, security, observability)
- [templates/planning/adr-template.md](templates/planning/adr-template.md) — Architecture Decision Record (ADR) for documenting design decisions with tradeoff analysis

**Architecture Patterns** ([templates/patterns/](templates/patterns/)):

- [templates/patterns/microservices-template.md](templates/patterns/microservices-template.md) — Complete microservices design template (API contracts, resilience, deployment, testing, cost optimization)
- [templates/patterns/event-driven-template.md](templates/patterns/event-driven-template.md) — Event-driven architecture template (event schemas, saga patterns, event sourcing, schema evolution)

**Operations & Scalability** ([templates/operations/](templates/operations/)):

- [templates/operations/scalability-checklist.md](templates/operations/scalability-checklist.md) — Comprehensive scalability checklist (database scaling, caching, load testing, auto-scaling, DR)

### Related Skills

**Implementation Details:**

- [../software-backend/SKILL.md](../software-backend/SKILL.md) — Backend engineering, API implementation, data layer
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Frontend architecture, micro-frontends, state management
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) — REST, GraphQL, gRPC design patterns

**Reliability & Operations:**

<!-- TODO: Add when skills are created
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience patterns, backpressure, failure handling
- [../qa-observability/SKILL.md](../qa-observability/SKILL.md) — Monitoring, tracing, performance optimization
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — Platform engineering, SRE, IaC, deployment strategies
-->

**Security & Data:**

- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Threat modeling, authentication, authorization, secure design
<!-- TODO: Add when skill is created
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — Database design, optimization, indexing strategies
-->

**Quality & Code:**

- [../software-code-review/SKILL.md](../software-code-review/SKILL.md) — Code review practices, architectural review
<!-- TODO: Add when skill is created
- [../qa-refactoring/SKILL.md](../qa-refactoring/SKILL.md) — Refactoring patterns, technical debt management
-->

**Documentation:**

- [../docs-codebase/SKILL.md](../docs-codebase/SKILL.md) — Architecture documentation, C4 diagrams, ADRs

---

## Operational Playbooks

**Shared Foundation**

- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) - Canonical clean code rules (`CC-*`) for citation
- Legacy playbook: [../software-clean-code-standard/resources/code-quality-operational-playbook.md](../software-clean-code-standard/resources/code-quality-operational-playbook.md) - `RULE-01`–`RULE-13`, operational procedures, and design patterns
- [../software-clean-code-standard/resources/design-patterns-operational-checklist.md](../software-clean-code-standard/resources/design-patterns-operational-checklist.md) - GoF pattern triggers and guardrails, when to apply vs avoid patterns

**Architecture-Specific**

- [resources/operational-playbook.md](resources/operational-playbook.md) — Detailed architecture questions, decomposition patterns, security layers, and external references
