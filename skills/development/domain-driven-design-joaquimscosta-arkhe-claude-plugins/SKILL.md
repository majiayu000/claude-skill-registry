---
name: domain-driven-design
description: Expert guidance for Domain-Driven Design architecture and implementation. Use when designing complex business systems, defining bounded contexts, structuring domain models, choosing between modular monolith vs microservices, implementing aggregates/entities/value objects, or when users mention "DDD", "domain-driven design", "bounded context", "aggregate", "domain model", "ubiquitous language", "event storming", "context mapping", "domain events", "anemic domain model", strategic design, tactical patterns, or domain modeling. Helps make architectural decisions, identify subdomains, design aggregates, and avoid common DDD pitfalls.
spring-boot-version: "4.0"
---

# Domain-Driven Design Skill

DDD manages complexity through alignment between software and business reality. **Strategic design (boundaries, language, subdomains) provides more value than tactical patterns (aggregates, repositories).**

## When to Apply DDD

**Apply DDD when:**
- Domain has intricate business rules
- System is long-lived and high-value
- Domain experts are available
- Multiple teams/departments involved
- Software represents competitive advantage

**DDD is overkill when:**
- Simple CRUD applications
- Tight deadlines, limited budgets
- No domain experts available
- Complexity is purely technical, not business

## Core Workflow

1. Domain Discovery → 2. Bounded Context Definition → 3. Context Mapping → 4. Architecture Selection → 5. Tactical Implementation

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step instructions for each phase.

## Quick Reference

### Subdomain Types (Problem Space)

| Type | Investment | Example |
|------|-----------|---------|
| **Core** | Maximum - competitive advantage | Recommendation engine, trading logic |
| **Supporting** | Custom but quality tradeoffs OK | Inventory management |
| **Generic** | Buy/outsource | Auth, email, payments |

### Key Decision: Entity vs Value Object

- **Entity**: Has identity, tracked through time, mutable → `Customer`, `Order`
- **Value Object**: Defined by attributes, immutable, interchangeable → `Money`, `Address`, `Email`

**Default to value objects.** Only use entities when identity matters.

### Aggregate Design Rules (Vaughn Vernon)

1. Model true invariants in consistency boundaries
2. Design small aggregates (~70% should be root + value objects only)
3. Reference other aggregates by ID only
4. Use eventual consistency outside the boundary

### Architecture Decision

```
Start with modular monolith when:
├── Team < 20 developers
├── Domain boundaries unclear
├── Time-to-market critical
└── Strong consistency required

Consider microservices when:
├── Bounded contexts have distinct languages
├── Teams can own full contexts
├── Independent scaling required
└── DevOps maturity exists
```

## Detailed References

- **Strategic Patterns**: See [references/STRATEGIC-PATTERNS.md](references/STRATEGIC-PATTERNS.md) for subdomains, bounded contexts, context mapping, event storming
- **Tactical Patterns**: See [references/TACTICAL-PATTERNS.md](references/TACTICAL-PATTERNS.md) for entities, value objects, aggregates, services, repositories
- **Architecture Alignment**: See [references/ARCHITECTURE-ALIGNMENT.md](references/ARCHITECTURE-ALIGNMENT.md) for clean/hexagonal architecture, modular monolith, microservices
- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step DDD implementation process
- **Anti-Patterns**: See [references/ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) for common pitfalls and how to avoid them
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for scenario walkthroughs applying DDD concepts
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions

## Critical Reminders

1. **Ubiquitous language first** - Code should read like business language
2. **Strategic before tactical** - Understand boundaries before implementing patterns
3. **Apply tactical patterns selectively** - Only in core domains where complexity warrants
4. **One aggregate per transaction** - Cross-aggregate consistency via domain events
5. **Persistence ignorance** - Domain layer has no infrastructure dependencies

## Related Skills

| Need | Skill |
|------|-------|
| Data layer implementation | `spring-boot-data-ddd` — JPA/JDBC aggregates, repositories, transactions |
| REST API layer | `spring-boot-web-api` — Controllers, validation, exception handling |
| Module boundaries | `spring-boot-modulith` — Module structure, event-driven communication |
| Testing patterns | `spring-boot-testing` — Aggregate tests, module tests, Scenario API |
| Security for domains | `spring-boot-security` — Method-level authorization, role-based access |
