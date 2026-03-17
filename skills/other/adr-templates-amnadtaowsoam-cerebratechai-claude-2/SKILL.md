---
name: Architecture Decision Records (ADR)
description: Documenting significant architectural decisions with context, consequences, and rationale for future reference.
---

# Architecture Decision Records (ADR)

## Overview

Architecture Decision Records (ADRs) are lightweight documents that capture important architectural decisions, their context, and consequences. They create a historical record of why systems are built the way they are.

**Core Principle**: "Document the 'why' behind architectural decisions, not just the 'what'."

---

## 1. What is an ADR?

An ADR documents:
- **What** decision was made
- **Why** it was made (context)
- **What** alternatives were considered
- **What** the consequences are

### When to Write an ADR
- Choosing a database (PostgreSQL vs MongoDB)
- Selecting an architecture pattern (microservices vs monolith)
- Picking a framework (React vs Vue)
- Defining API standards (REST vs GraphQL)
- Security decisions (OAuth2 vs JWT)

---

## 2. ADR Template (MADR Format)

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a database for our e-commerce platform that handles:
- Complex transactions (orders, payments, inventory)
- ACID compliance requirements
- Relational data (users, products, orders)
- Expected scale: 100K users, 10K orders/day

## Decision
We will use PostgreSQL as our primary database.

## Alternatives Considered

### MongoDB
- **Pros**: Flexible schema, horizontal scaling
- **Cons**: Weaker transaction support, eventual consistency
- **Why rejected**: We need strong ACID guarantees for financial transactions

### MySQL
- **Pros**: Mature, widely used, good performance
- **Cons**: Less advanced features than PostgreSQL
- **Why rejected**: PostgreSQL's JSON support and advanced indexing better fit our needs

## Consequences

### Positive
- Strong ACID compliance for financial transactions
- Rich query capabilities (CTEs, window functions)
- JSON support for flexible product attributes
- Mature ecosystem and tooling

### Negative
- Vertical scaling limitations (can be mitigated with read replicas)
- More complex to operate than managed NoSQL solutions
- Learning curve for team members unfamiliar with SQL

## Implementation Notes
- Use Prisma ORM for type-safe database access
- Set up read replicas for scaling reads
- Use connection pooling (PgBouncer)

## Related Decisions
- ADR-002: Use Prisma ORM
- ADR-005: Database migration strategy

## Date
2024-01-15

## Authors
@alice, @bob
```

---

## 3. ADR Statuses

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion |
| **Accepted** | Decision made and approved |
| **Deprecated** | No longer recommended |
| **Superseded** | Replaced by another ADR |
| **Rejected** | Considered but not chosen |

---

## 4. Directory Structure

```
docs/adr/
├── README.md
├── 0001-use-postgresql.md
├── 0002-use-prisma-orm.md
├── 0003-adopt-microservices.md
├── 0004-use-react-frontend.md
└── template.md
```

---

## 5. ADR Tools

### adr-tools (CLI)
```bash
# Install
npm install -g adr-log

# Create new ADR
adr new "Use PostgreSQL for primary database"

# List all ADRs
adr list

# Generate table of contents
adr generate toc
```

### Log4brains (Web UI)
```bash
# Install
npm install -g log4brains

# Initialize
log4brains init

# Preview
log4brains preview

# Build static site
log4brains build
```

---

## 6. Lightweight ADR Template

For smaller decisions:

```markdown
# Use Tailwind CSS for styling

**Status**: Accepted
**Date**: 2024-01-15

## Decision
Use Tailwind CSS for all component styling.

## Rationale
- Utility-first approach speeds up development
- Consistent design system
- Smaller bundle size with PurgeCSS
- Team already familiar with it

## Consequences
- Need to learn Tailwind conventions
- HTML can become verbose
- Harder to share styles across projects
```

---

## 7. Superseding an ADR

```markdown
# ADR-003: Adopt Microservices Architecture

## Status
~~Accepted~~ **Superseded by ADR-010**

## Superseded By
[ADR-010: Return to Modular Monolith](0010-modular-monolith.md)

## Original Decision
[Keep original content for historical reference]

## Why Superseded
After 2 years of microservices:
- Operational complexity exceeded benefits
- Team size (5 engineers) too small to manage 12 services
- Network latency impacting user experience
- Distributed tracing and debugging challenges

See ADR-010 for new approach.
```

---

## 8. ADR Review Process

```markdown
## ADR Review Checklist

- [ ] **Context Clear**: Is the problem well-defined?
- [ ] **Alternatives Listed**: Were other options considered?
- [ ] **Trade-offs Analyzed**: Pros and cons documented?
- [ ] **Consequences Identified**: Both positive and negative?
- [ ] **Stakeholders Consulted**: Relevant teams reviewed?
- [ ] **Implementation Plan**: Next steps clear?
- [ ] **Date and Authors**: Documented?
```

---

## 9. Common ADR Topics

### Technology Choices
- Database selection
- Programming language
- Framework selection
- Cloud provider

### Architecture Patterns
- Microservices vs monolith
- Event-driven architecture
- CQRS and Event Sourcing
- API design (REST vs GraphQL)

### Security
- Authentication method
- Encryption standards
- API security

### Operations
- Deployment strategy
- Monitoring approach
- Logging standards

---

## 10. ADR Best Practices

### Do
✅ Write ADRs for significant decisions
✅ Include alternatives considered
✅ Document trade-offs honestly
✅ Keep ADRs immutable (don't edit, supersede instead)
✅ Make ADRs easy to find (in repo, searchable)

### Don't
❌ Write ADRs for trivial decisions
❌ Make ADRs too long (aim for 1-2 pages)
❌ Skip the "why" (context is crucial)
❌ Delete old ADRs (mark as superseded)
❌ Write ADRs after the fact (document during decision)

---

## 11. ADR Integration with Development

### In Pull Requests
```markdown
## PR Description

This PR implements the decision from [ADR-005: Use Redis for caching](../docs/adr/0005-redis-caching.md)

Changes:
- Add Redis client
- Implement cache layer
- Update documentation
```

### In Code Comments
```typescript
// Per ADR-003, we use JWT for authentication
// See: docs/adr/0003-jwt-authentication.md
export function verifyToken(token: string) {
  // ...
}
```

---

## 12. ADR Checklist

- [ ] **Template Available**: ADR template in repository?
- [ ] **Directory Structure**: Organized and numbered?
- [ ] **Review Process**: Who approves ADRs?
- [ ] **Discoverability**: ADRs linked in README?
- [ ] **Tooling**: CLI or web UI for managing ADRs?
- [ ] **Integration**: ADRs referenced in code/PRs?
- [ ] **Maintenance**: Old ADRs marked as superseded?
- [ ] **Culture**: Team writes ADRs consistently?

---

## Related Skills
* `59-architecture-decision/tradeoff-analysis`
* `59-architecture-decision/tech-stack-selection`
* `59-architecture-decision/architecture-review`
* `00-meta-skills/decision-making`
