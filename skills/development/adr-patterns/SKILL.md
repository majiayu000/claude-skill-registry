---
name: adr-patterns
description: Architecture Decision Records patterns including templates, naming conventions, and lifecycle management. Use when documenting significant architectural decisions.
durability: encoded-preference
---

# ADR (Architecture Decision Records)

## When to Create ADR

**Create ADR when:**
- Technology stack changes (new framework, database, language)
- Architecture pattern decisions (microservices, event-driven, etc.)
- Significant design decisions with long-term impact

**Do NOT create ADR for:**
- Daily implementation decisions
- Small feature additions
- Bug fixes
- Refactoring without architecture changes

## Directory Structure

```
docs/adr/
├── index.md          # ADR registry
├── 0001-title.md     # First ADR
├── 0002-title.md     # Second ADR
└── ...
```

## Decision Principles

- **No architecture astronautics** -- Every abstraction must justify its complexity. If you cannot explain why a layer exists to a new team member in one sentence, remove it.
- **Trade-offs over best practices** -- Name what you are giving up, not just what you are gaining. Every ADR "Consequences" section must have both Positive and Negative entries.
- **Domain first, technology second** -- Understand the business problem before picking tools or frameworks.
- **Reversibility as criterion** -- Prefer decisions that are easy to change over ones that are "optimal" right now. When two options are close, choose the more reversible one. Note reversibility explicitly in the ADR.

## DDD Considerations

Evaluate options against bounded context boundaries, aggregate consistency, and domain event flows.

## Context Mapping

When ADRs involve integration between contexts, identify the context mapping pattern (Shared Kernel, Customer/Supplier, Conformist, Anti-Corruption Layer, Open Host Service, Separate Ways) in the ADR.

## Architecture Pattern Decision Matrix

When an ADR evaluates architectural patterns, use this matrix as a starting point for trade-off analysis:

| Pattern | Use When | Avoid When | Key Trade-off |
|---------|----------|------------|---------------|
| Modular Monolith | Small team, unclear domain boundaries, early-stage | Independent scaling or deployment needed per module | Simplicity vs deployment flexibility |
| Microservices | Clear domain boundaries, team autonomy needed, independent scaling | Small team, early-stage product, unclear boundaries | Autonomy vs operational complexity |
| Event-Driven | Loose coupling, async workflows, audit trail needed | Strong consistency required, simple request-response | Decoupling vs eventual consistency complexity |
| CQRS | Read/write asymmetry, complex query requirements | Simple CRUD domains, small data volume | Query optimization vs system complexity |

This matrix belongs in the "Considered Options" section of an ADR. Customize rows and trade-offs for the specific project context.

## Communication

- Use the C4 model (Context, Containers, Components, Code) to communicate architecture at the right level of abstraction in ADR diagrams or descriptions.
- Always present at least two options with explicit trade-offs in the "Considered Options" section.

## ADR Template

```markdown
# [Title of the Architectural Decision]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-NNNN]

## Context and Problem Statement
[Describe the context and problem statement in 2-3 sentences]

## Considered Options
* [Option 1] - Brief description
* [Option 2] - Brief description
* [Option 3] - Brief description

## Decision Outcome
Chosen option: "[Option X]", because [justification].

## Consequences

### Positive
* [Benefit 1]
* [Benefit 2]

### Negative
* [Drawback 1]
* [Drawback 2]

### Reversibility
[How easy is it to change this decision later? What would reversal cost?]
```

## Naming Convention

- Format: `NNNN-title-with-hyphens.md`
- Example: `0001-use-redis-for-vector-search.md`

## Lifecycle

- ADRs are **immutable** once accepted
- If a decision changes, create a **new ADR** that supersedes the old one
- **Never delete ADRs**, even if superseded
