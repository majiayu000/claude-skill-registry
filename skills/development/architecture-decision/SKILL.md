---
name: architecture-decision
description: "Systematically evaluate architecture decisions, document trade-offs, and select appropriate patterns. This skill should be used when the user asks about 'architecture decision', 'ADR', 'design pattern selection', 'technology choice', or needs to evaluate architectural trade-offs. Keywords: architecture, ADR, patterns, trade-offs, technical debt, quality attributes, decision record."
license: MIT
compatibility: Works with any project. Integrates with system-design for ADR templates.
metadata:
  author: jwynia
  version: "1.0"
---

# Architecture Decision

Systematically evaluate architecture decisions, document trade-offs, and select appropriate patterns for context. Provides frameworks for pattern selection, ADR creation, and technical debt management.

## When to Use This Skill

Use this skill when:
- Making technology choices
- Evaluating architectural patterns
- Creating Architecture Decision Records
- Assessing technical debt
- Comparing design alternatives

Do NOT use this skill when:
- Writing implementation code
- Working on requirements (use requirements-analysis)
- Doing full system design (use system-design)

## Core Principle

**Context drives decisions.** No pattern is universally good or bad. The best architecture is not the most elegant—it's the one that best serves its purpose while remaining maintainable and evolvable.

## The Trade-off Triangle

Every architectural decision involves trade-offs:

| Vertex | Maximized By | Cost |
|--------|--------------|------|
| **Simplicity** | Monolith, sync communication, single DB | Scalability limits |
| **Flexibility** | Microservices, event-driven, plugins | Complexity overhead |
| **Performance** | Caching, denormalization, optimized code | Maintainability |

**Balance Strategies:**
- Start simple, add complexity as needed
- Measure before optimizing
- Use abstractions to defer decisions
- Evolve incrementally

## Quality Attributes

### Performance
- Metrics: Response time (p50, p95, p99), throughput, resource utilization
- Tactics: Caching, load balancing, async processing

### Scalability
- Dimensions: Horizontal, vertical, elastic
- Patterns: Stateless services, sharding, event streaming

### Reliability
- Metrics: Uptime, MTBF, MTTR
- Patterns: Circuit breakers, retries, redundancy

### Maintainability
- Factors: Readability, modularity, testability
- Patterns: Clean architecture, DDD, SOLID

## Context-Pattern Mapping

### Team Context

| Context | Preferred Patterns | Avoid |
|---------|-------------------|-------|
| **Small team** | Monolith, vertical slices, shared DB | Microservices, complex abstractions |
| **Multiple teams** | Service boundaries, API contracts | Shared state, tight coupling |

### Scale Context

| Context | Preferred Patterns | Reasoning |
|---------|-------------------|-----------|
| **Startup** | Monolith first, vertical scaling | Optimize for development speed |
| **Enterprise** | Service mesh, horizontal scaling | Optimize for operational scale |

## Decision Matrix Template

| Option | Consistency | Flexibility | Scalability | Complexity | Cost | Total |
|--------|-------------|-------------|-------------|------------|------|-------|
| Option A | 5 | 2 | 3 | 2 | 3 | 15 |
| Option B | 3 | 5 | 4 | 3 | 3 | 18 |
| Option C | 2 | 3 | 5 | 1 | 2 | 13 |

Weight factors based on context priorities.

## Architecture Decision Record (ADR) Template

```markdown
# ADR-[NUMBER]: [TITLE]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the situation requiring a decision?]

### Requirements
- [Requirement 1]
- [Requirement 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

## Decision
[What is the decision?]

### Justification
- [Reason 1]
- [Reason 2]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

## Alternatives Considered

### [Alternative 1]
Reason rejected: [Why]

### [Alternative 2]
Reason rejected: [Why]
```

## Architectural Refactoring Patterns

### Branch by Abstraction
1. Create abstraction over current implementation
2. Implement new solution behind abstraction
3. Switch to new implementation
4. Remove old implementation

### Strangler Fig
1. Identify boundary
2. Implement new solution for new features
3. Gradually migrate old features
4. Retire old system

### Parallel Run
1. Implement new solution
2. Run both old and new
3. Compare results
4. Switch when confident

## Technical Debt Management

### Debt Categories

| Type | Examples | Payment Strategy |
|------|----------|------------------|
| **Design** | Missing abstractions, tight coupling | Refactoring sprints |
| **Code** | Duplication, complexity, poor naming | Continuous cleanup |
| **Test** | Missing tests, flaky tests | Test improvement |
| **Documentation** | Missing docs, outdated diagrams | Documentation sprints |

### Metrics
- **Debt ratio:** Debt work / Total work (target < 20%)
- **Interest rate:** Extra effort due to debt
- **Debt ceiling:** Maximum acceptable debt

## Anti-Patterns

### Big Ball of Mud
**Symptoms:** No clear structure, everything depends on everything
**Remedy:** Identify boundaries, extract modules, establish interfaces

### Distributed Monolith
**Symptoms:** Services must deploy together, sync chains, shared DBs
**Remedy:** Merge related services, async communication, separate DBs

### Golden Hammer
**Symptoms:** One solution for all problems, force-fitting patterns
**Remedy:** Learn alternatives, evaluate objectively, prototype options

## Related Skills

- **system-design** - Full system design with ADRs
- **code-review** - Implementation validation
- **task-decomposition** - Breaking down architectural work
- **requirements-analysis** - Understanding constraints
