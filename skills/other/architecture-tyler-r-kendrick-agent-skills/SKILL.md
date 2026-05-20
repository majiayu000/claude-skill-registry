---
name: architecture
description: |
    Use when selecting architecture styles, evaluating system decomposition strategies, or analyzing architecture characteristics (quality attributes) for a system.
    USE FOR: architecture style selection, comparing monolith vs microservices, architecture characteristics analysis, system decomposition strategy
    DO NOT USE FOR: specific style details (use sub-skills: microservices, monoliths, event-driven, etc.), code-level patterns (use dev/design-patterns), integration messaging (use dev/integration-patterns)
license: MIT
metadata:
  displayName: "Architecture"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Martin Fowler — Software Architecture Guide"
    url: "https://martinfowler.com/architecture/"
  - title: "Software Architecture — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Software_architecture"
---

# Software Architecture

## Overview
Software architecture is the set of significant decisions about the organization of a software system -- the selection of structural elements, their interfaces, composition, and the guiding principles that constrain design and evolution over time. Choosing the right architecture style is one of the highest-leverage decisions a team makes; it shapes every subsequent technical and organizational choice.

This skill covers how to reason about architecture styles, evaluate architecture characteristics (quality attributes), and make informed tradeoffs. For deep dives into specific styles, see the sub-skills below.

## Canonical Works

| Book | Author(s) | Focus |
|------|-----------|-------|
| *Fundamentals of Software Architecture* | Mark Richards & Neal Ford | Architecture styles, characteristics, decisions, metrics |
| *Software Architecture: The Hard Parts* | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani | Tradeoff analysis, decomposition, data ownership, contracts |
| *Building Evolutionary Architectures* | Ford, Parsons, Kua | Fitness functions, incremental change, governed evolution |
| *Documenting Software Architectures* | Clements et al. | Views, viewpoints, architecture documentation |

## The Monolith-to-Microservices Spectrum

Architecture is not a binary choice between monolith and microservices. It is a spectrum of modularity:

```
 Monolith                                                    Microservices
    |                                                             |
    |  Big Ball    Layered    Modular      Service-    Micro-     |
    |  of Mud      Monolith   Monolith     Based       services   |
    |                                                             |
    ◄─────────────────────────────────────────────────────────────►
    Less distributed                          More distributed
    Simpler operations                        Complex operations
    Easier consistency                        Eventual consistency
    Tighter coupling                          Loose coupling
```

**Key insight (Richards & Ford):** Move along the spectrum only when the pain of your current position exceeds the cost of the next step. Start simple; evolve when you have evidence.

## Architecture Characteristics (Quality Attributes)

Architecture characteristics -- also called "-ilities" -- are the non-functional requirements that shape which style fits. They are inherently in tension; optimizing one often degrades another.

| Characteristic | Description | Tension With |
|---------------|-------------|--------------|
| **Scalability** | Ability to handle growing load | Simplicity, Cost |
| **Reliability** | System uptime and fault tolerance | Performance, Cost |
| **Performance** | Latency and throughput | Scalability, Maintainability |
| **Security** | Protection against threats | Usability, Performance |
| **Maintainability** | Ease of change and evolution | Performance, Time-to-Market |
| **Deployability** | Ease and frequency of deployment | Simplicity, Reliability |
| **Testability** | Ease of verifying correctness | Time-to-Market |
| **Elasticity** | Ability to scale up AND down dynamically | Cost, Simplicity |
| **Fault Tolerance** | Graceful degradation under failure | Performance, Complexity |
| **Modularity** | Degree of separation between components | Performance (indirection cost) |

### Identifying Driving Characteristics
Not every characteristic matters equally. Richards & Ford recommend identifying the **top 3-5 driving characteristics** for a system and using those to select an architecture style.

## Architecture Style Comparison

| Style | Scalability | Simplicity | Deployability | Data Consistency | Cost | Best For |
|-------|:-----------:|:----------:|:-------------:|:----------------:|:----:|----------|
| **Layered Monolith** | Low | High | Low | High | Low | Small teams, simple domains |
| **Modular Monolith** | Medium | Medium | Medium | High | Low | Medium complexity, single team |
| **Service-Based** | Medium | Medium | Medium | Medium | Medium | Domain-separated teams |
| **Microservices** | High | Low | High | Low | High | Large orgs, independent teams |
| **Event-Driven** | High | Low | High | Low | Medium | Async workflows, event streams |
| **Space-Based** | Very High | Low | Medium | Low | High | Extreme elastic scalability |
| **Orchestration-Driven** | Medium | Medium | Medium | Medium | Medium | Complex workflows |
| **Pipeline (Pipes & Filters)** | Medium | Medium | Medium | Medium | Low | Data processing, ETL |

## Architecture Decision Records (ADRs)

Every significant architecture decision should be captured in an Architecture Decision Record. ADRs provide context for future developers about why a decision was made, what alternatives were considered, and what tradeoffs were accepted.

See: `specs/documentation/adr` for ADR templates and practices.

**ADR structure (Michael Nygard format):**
- **Title** -- Short noun phrase (e.g., "Use PostgreSQL for order data")
- **Status** -- Proposed, Accepted, Deprecated, Superseded
- **Context** -- The forces at play, the problem, the constraints
- **Decision** -- What was decided and why
- **Consequences** -- What becomes easier, what becomes harder

## Architecture Decision Process

1. **Identify the driving characteristics** -- What are the top 3-5 quality attributes?
2. **Identify the domain partitioning** -- How does the domain decompose? (see `dev/architecture/domain-driven-design`)
3. **Select a candidate style** -- Use the comparison table above to narrow options.
4. **Evaluate tradeoffs** -- Every style has strengths and weaknesses. Make tradeoffs explicit.
5. **Record the decision** -- Write an ADR capturing context, decision, and consequences.
6. **Validate with fitness functions** -- Define measurable criteria that the architecture must satisfy over time.

## Common Anti-Patterns

- **Accidental architecture** -- No deliberate style; the system evolves into a Big Ball of Mud.
- **Resume-driven architecture** -- Choosing microservices (or any style) because it looks good on a resume, not because the problem demands it.
- **Architecture by analogy** -- "Netflix uses microservices, so we should too." Your context is not Netflix's context.
- **Ignoring the First Law of Software Architecture** -- "Everything in software architecture is a tradeoff" (Richards & Ford). If you think you found something that isn't a tradeoff, you haven't identified the tradeoff yet.

## Best Practices
- Start with the simplest architecture that meets your driving characteristics. Evolve when evidence demands it.
- Make architecture decisions explicit and documented (ADRs).
- Architecture is not a one-time activity -- it is continuous. Revisit decisions as the system and context evolve.
- Align architecture boundaries with team boundaries (see Conway's Law and the Inverse Conway Maneuver).
- Use fitness functions to objectively measure whether the architecture meets its goals over time.
- Understand that the "best" architecture depends on your specific context: team size, domain complexity, scale requirements, and organizational structure.

## Sub-Skills
- `dev/architecture/microservices` -- Service decomposition, inter-service communication, saga patterns
- `dev/architecture/monoliths` -- Modular monolith, monolith-first strategy, Strangler Fig migration
- `dev/architecture/well-architected` -- AWS, Azure, and GCP well-architected frameworks
- `dev/architecture/event-driven` -- Event-driven architecture, event sourcing, CQRS
- `dev/architecture/domain-driven-design` -- Bounded contexts, aggregates, strategic and tactical DDD
- `dev/architecture/hexagonal` -- Ports and adapters, onion architecture, dependency inversion
