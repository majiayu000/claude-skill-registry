---
name: faion-software-architect
description: "Software architecture: system design, patterns, ADRs, quality attributes."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Software Architect Skill

**Communication: User's language. Docs: English.**

## Purpose

Make informed architecture decisions balancing quality attributes (scalability, performance, security, maintainability) with business constraints (time, cost, team skills).

---

## Context Discovery

### Auto-Investigation

Detect existing architecture from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| ADRs | `Glob("**/adr/*.md")` or `Glob("**/docs/decisions/*")` | Architecture decisions documented |
| C4 diagrams | `Glob("**/*.dsl")` or `Grep("C4_", "**/*.puml")` | Architecture visualized |
| constitution.md | `Glob("**/.aidocs/constitution.md")` | Tech stack defined |
| docker-compose | `Glob("**/docker-compose*.yml")` | Service architecture |
| k8s manifests | `Glob("**/k8s/**/*.yaml")` | Kubernetes deployment |
| Multiple services | `Glob("**/services/*/")` | Microservices structure |
| Single app | `Glob("**/src/")` + no services | Monolith structure |

**Read existing architecture:**
- constitution.md for tech decisions
- Any existing ADRs
- docker-compose for service dependencies
- README for architecture overview

### Discovery Questions

#### Q1: Architecture Goal

```yaml
question: "What architecture decision do you need help with?"
header: "Goal"
multiSelect: false
options:
  - label: "Design new system architecture"
    description: "Starting from scratch or major redesign"
  - label: "Choose technology (database, framework, cloud)"
    description: "Technology selection decision"
  - label: "Document existing architecture"
    description: "Create ADRs, diagrams, docs"
  - label: "Evaluate/improve current architecture"
    description: "Review for issues, plan improvements"
  - label: "Migrate or refactor"
    description: "Move to new patterns or technologies"
```

#### Q2: Scale & Team Context

```yaml
question: "What's your scale and team context?"
header: "Context"
multiSelect: false
options:
  - label: "Solo/small team, MVP/early stage"
    description: "Speed matters, keep it simple"
  - label: "Growing team (5-15), scaling product"
    description: "Need modularity, some structure"
  - label: "Large team (15+), multiple teams"
    description: "Independent deployment, team boundaries"
  - label: "Enterprise, compliance requirements"
    description: "Security, audit, formal processes"
```

**Recommendation:**
- "Solo/MVP" → Monolith, simple tech stack
- "Growing" → Modular monolith, prepare for split
- "Large team" → Microservices, clear boundaries
- "Enterprise" → Formal architecture, ADRs, compliance

#### Q3: Quality Priorities (multiSelect)

```yaml
question: "What are your top quality priorities?"
header: "Priorities"
multiSelect: true
options:
  - label: "Scalability (handle growth)"
    description: "10x, 100x load handling"
  - label: "Performance (low latency)"
    description: "Fast response times"
  - label: "Availability (uptime)"
    description: "99.9%+ availability"
  - label: "Security (protect data)"
    description: "Compliance, threat protection"
  - label: "Maintainability (easy changes)"
    description: "Developer productivity"
  - label: "Cost efficiency"
    description: "Minimize infrastructure spend"
```

#### Q4: Constraints

```yaml
question: "What constraints do you have?"
header: "Constraints"
multiSelect: true
options:
  - label: "Limited budget"
    description: "Must minimize cloud costs"
  - label: "Small team / solo"
    description: "Can't manage complexity"
  - label: "Existing tech stack"
    description: "Must work with current systems"
  - label: "Compliance (HIPAA, SOC2, GDPR)"
    description: "Regulatory requirements"
  - label: "No major constraints"
    description: "Flexibility to choose"
```

---

## Quick Decision Reference

| If you need... | Use | File |
|----------------|-----|------|
| **Architecture style** for small team/MVP | Monolith or Modular Monolith | [monolith-architecture.md](monolith-architecture.md), [modular-monolith.md](modular-monolith.md) |
| **Architecture style** for large team | Microservices | [microservices-architecture.md](microservices-architecture.md) |
| **Database** for relational data | PostgreSQL/MySQL | [database-selection.md](database-selection.md) |
| **Database** for documents | MongoDB/DynamoDB | [database-selection.md](database-selection.md) |
| **Database** for cache | Redis | [caching-architecture.md](caching-architecture.md) |
| **API** for external devs | REST + OpenAPI | [patterns.md](patterns.md) |
| **API** for internal | gRPC | [patterns.md](patterns.md) |
| **Communication** async | Kafka/RabbitMQ | [event-driven-architecture.md](event-driven-architecture.md) |
| **Pattern** for distributed transactions | Saga | [distributed-patterns.md](distributed-patterns.md) |
| **Pattern** for resilience | Circuit Breaker | [distributed-patterns.md](distributed-patterns.md) |

---

## Methodologies (30)

**Fundamentals (5):** system-design-process | c4-model | architecture-decision-records | quality-attributes-analysis | trade-off-analysis

**Styles (5):** monolith-architecture | microservices-architecture | modular-monolith | serverless-architecture | event-driven-architecture

**Patterns (5):** creational-patterns | structural-patterns | behavioral-patterns | architectural-patterns | distributed-patterns

**Data (4):** data-modeling | database-selection | caching-architecture | data-pipeline-design

**Infrastructure (4):** cloud-architecture | container-orchestration | api-gateway-design | service-mesh

**Quality (4):** security-architecture | performance-architecture | reliability-architecture | observability-architecture

**Templates (3):** adr-template | quality-attributes | workflows

---

## Quality Attributes

**Scalability:** Handle 10x load? | **Performance:** p95 < 200ms? | **Availability:** 99.9%+ uptime? | **Security:** Threat model done? | **Maintainability:** Deploy daily?

**Framework:** [quality-attributes.md](quality-attributes.md) | **Analysis:** [quality-attributes-analysis.md](quality-attributes-analysis.md)

---

## C4 Model

| Level | Audience | Shows | File |
|-------|----------|-------|------|
| Context (C1) | Business | External systems, users | [c4-model.md](c4-model.md) |
| Container (C2) | Architects | Apps, databases, services | [c4-model.md](c4-model.md) |
| Component (C3) | Developers | Internal components | [c4-model.md](c4-model.md) |

---

## ADR Template

```markdown
# ADR-NNN: Title
## Status: Proposed/Accepted
## Context: Why needed?
## Decision: What we decided
## Consequences: Trade-offs
## Alternatives: Other options
```

**Full template:** [adr-template.md](adr-template.md)

---

## Workflows

**System Design:** Requirements → Scale estimation → High-level design → Components → Quality attributes → Documentation

**Technology Selection:** Define criteria → Research → Evaluate → Decide → Document ADR

**Full workflows:** [workflows.md](workflows.md)

---

*faion-software-architect v1.2*
*30 Methodologies*
