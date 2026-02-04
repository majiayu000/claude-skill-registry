---
name: acc-adr-template
description: Generates Architecture Decision Records (ADR) for PHP projects. Creates structured decision documentation with context, decision, and consequences.
---

# ADR Template Generator

Generate Architecture Decision Records following the standard format.

## ADR Format

```markdown
# ADR-{number}: {Title}

**Status:** {Proposed | Accepted | Deprecated | Superseded}
**Date:** {YYYY-MM-DD}
**Deciders:** {names or roles}

## Context

{What is the issue that we're seeing that motivates this decision?}

## Decision

{What is the change that we're proposing/doing?}

## Consequences

### Positive

{What becomes easier?}

### Negative

{What becomes harder?}

### Risks

{What could go wrong?}

## Alternatives Considered

{What other options were evaluated?}

## References

{Links to relevant resources}
```

## Section Guidelines

### Title

```markdown
# ADR-001: Use Domain-Driven Design Architecture

Format: "ADR-{NNN}: {Verb} {Noun/Concept}"

Good:
- Use Domain-Driven Design
- Implement CQRS Pattern
- Adopt PostgreSQL for Primary Storage
- Separate Read and Write Models

Bad:
- DDD (too short)
- Architecture Decision (too vague)
- We should use DDD (conversational)
```

### Status Values

```markdown
**Proposed** — Under discussion, not yet decided
**Accepted** — Decided and implemented
**Deprecated** — No longer recommended
**Superseded by ADR-XXX** — Replaced by newer decision
```

### Context Section

```markdown
## Context

Describe the situation that led to this decision:

- What problem are we solving?
- What forces are at play?
- What constraints exist?
- What is the current state?

Example:
---
The system has grown to 50+ controllers with business logic scattered
across controllers, services, and repositories. This leads to:

- Code duplication across features
- Difficulty testing business rules
- Unclear ownership of business logic
- Tight coupling to Symfony framework

We need a clear structure to organize business logic.
```

### Decision Section

```markdown
## Decision

State the decision clearly:

- Use active voice
- Be specific about what changes
- Include key implementation details

Example:
---
We will adopt Domain-Driven Design (DDD) with the following structure:

1. **Domain Layer** — Contains entities, value objects, domain events,
   and repository interfaces. No framework dependencies.

2. **Application Layer** — Contains use cases that orchestrate domain
   objects. Defines DTOs for input/output.

3. **Infrastructure Layer** — Implements repository interfaces,
   integrates with database, cache, and external services.

4. **Presentation Layer** — Handles HTTP requests/responses using
   ADR pattern (Action-Domain-Responder).
```

### Consequences Section

```markdown
## Consequences

### Positive

List benefits gained:
- Clearer separation of concerns
- Domain logic independent of framework
- Easier to test business rules
- Better code organization

### Negative

List drawbacks accepted:
- More files and directories
- Learning curve for team
- Initial refactoring effort
- More boilerplate code

### Risks

List potential issues:
- Team may over-engineer simple features
- Boundaries may be drawn incorrectly initially
- Refactoring existing code may introduce bugs
```

### Alternatives Section

```markdown
## Alternatives Considered

### Alternative 1: {Name}

**Description:** {What is it?}

**Pros:**
- {benefit 1}
- {benefit 2}

**Cons:**
- {drawback 1}
- {drawback 2}

**Why Rejected:** {reason}

### Alternative 2: {Name}

...
```

## Complete Example

```markdown
# ADR-003: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2025-01-15
**Deciders:** Tech Lead, Backend Team

## Context

We need to select a primary database for the new order management system.
Requirements include:

- Support for complex queries on order data
- JSONB storage for flexible product attributes
- Strong ACID compliance for financial transactions
- Good performance at 10K orders/day scale
- Team familiarity and ecosystem support

Current tech stack uses MySQL 5.7 for legacy systems.

## Decision

We will use PostgreSQL 16 as the primary database for the following reasons:

1. **JSONB Support** — Native JSON storage with indexing for product
   attributes that vary by category

2. **Advanced Types** — UUID, arrays, enums as native types reduce
   application-level validation

3. **Better Query Optimizer** — Handles complex JOINs across order,
   item, and inventory tables more efficiently

4. **Extensibility** — PostGIS for future location features,
   full-text search without external service

Implementation notes:
- Use Doctrine ORM with PostgreSQL-specific types
- Enable UUID generation at database level
- Configure connection pooling with PgBouncer

## Consequences

### Positive

- Native JSONB eliminates need for EAV pattern
- Better query performance for complex reports
- Strong typing catches data issues early
- Modern features reduce application complexity

### Negative

- Team needs PostgreSQL training (2-3 days)
- Different SQL dialect from MySQL
- Hosting costs slightly higher
- No existing internal DBA expertise

### Risks

- Migration from MySQL may surface data issues
- Performance tuning requires new expertise
- Backup/recovery procedures need updating

## Alternatives Considered

### MySQL 8.0

**Description:** Upgrade existing MySQL infrastructure

**Pros:**
- Team familiarity
- Existing tooling and procedures
- Lower migration effort

**Cons:**
- JSON support less mature than PostgreSQL
- Missing advanced types
- Query optimizer less capable

**Why Rejected:** Long-term technical debt outweighs short-term convenience

### MongoDB

**Description:** Document database for flexibility

**Pros:**
- Schema flexibility
- Native JSON
- Horizontal scaling

**Cons:**
- No ACID for multi-document transactions
- Team has no experience
- Complex queries harder

**Why Rejected:** Financial data requires strong ACID guarantees

## References

- [PostgreSQL vs MySQL Comparison](https://example.com/comparison)
- [PostgreSQL 16 Release Notes](https://www.postgresql.org/docs/16/release-16.html)
- Internal RFC: Database Selection Criteria
```

## File Naming Convention

```
docs/adr/
├── 000-adr-template.md      # Template file
├── 001-use-ddd.md           # First decision
├── 002-implement-cqrs.md    # Second decision
├── 003-use-postgresql.md    # Third decision
└── README.md                # Index of all ADRs
```

## ADR Index Template

```markdown
# Architecture Decision Records

## Active Decisions

| ADR | Date | Title | Status |
|-----|------|-------|--------|
| [001](001-use-ddd.md) | 2025-01-10 | Use Domain-Driven Design | Accepted |
| [002](002-implement-cqrs.md) | 2025-01-12 | Implement CQRS Pattern | Accepted |
| [003](003-use-postgresql.md) | 2025-01-15 | Use PostgreSQL | Accepted |

## Deprecated Decisions

| ADR | Date | Title | Superseded By |
|-----|------|-------|---------------|
| [000](000-monolith.md) | 2024-06-01 | Monolith Architecture | ADR-010 |
```

## Generation Instructions

When generating an ADR:

1. **Determine** next ADR number from existing files
2. **Clarify** the decision being made
3. **Document** context thoroughly
4. **State** decision clearly with specifics
5. **List** consequences (positive, negative, risks)
6. **Include** alternatives that were considered
7. **Add** references to relevant resources
8. **Update** ADR index file
