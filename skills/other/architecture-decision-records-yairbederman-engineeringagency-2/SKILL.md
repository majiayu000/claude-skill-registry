---
name: architecture-decision-records
description: Document significant architectural decisions. Use when making significant architectural decisions, documenting technology choices, or recording design trade-offs.
---

# Architecture Decision Records (ADR)

Document significant architectural decisions for posterity and onboarding.

## When to Use

- Making significant architectural decisions
- Choosing between technologies
- Establishing patterns or standards
- Documenting trade-off analysis
- Onboarding new team members

## ADR Template

```markdown
# ADR-{NUMBER}: {TITLE}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-xxx}

## Date
{YYYY-MM-DD}

## Context
What is the issue that we're seeing that motivates this decision?
What are the forces at play (technical, political, social)?

## Decision
What is the change we're proposing and/or doing?

## Rationale
Why is this change being made?
What alternatives were considered?
Why was this option chosen over alternatives?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

### Neutral
- Side effect 1

## Alternatives Considered

### Option A: {Name}
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Why not chosen:** Reason

### Option B: {Name}
...

## References
- [Link to relevant doc]
- [Link to RFC/proposal]
```

## ADR Guidelines

### What to Document

| Document | Don't Document |
|----------|----------------|
| Choice of database | Routine refactoring |
| API design patterns | Bug fixes |
| Authentication approach | Minor dependency updates |
| Service boundaries | Code style choices |
| Framework selection | Obvious decisions |

### Writing Tips

1. **Be Specific**
   - ❌ "We need better performance"
   - ✅ "Current response time is 500ms, target is 100ms"

2. **Document Alternatives**
   - Show what was considered
   - Explain why options were rejected
   - This helps future reviewers

3. **Include Context**
   - What constraints existed?
   - What deadlines affected the decision?
   - What was the team's expertise?

4. **State Consequences Honestly**
   - Both positive and negative
   - Technical debt incurred
   - Future limitations

## Example ADR

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Date
2024-01-15

## Context
We need to select a primary database for the new user management service.
The service will handle 10K concurrent users with complex querying needs.
Team has experience with both PostgreSQL and MongoDB.

## Decision
Use PostgreSQL 15 as the primary database.

## Rationale
- Strong ACID compliance needed for user data integrity
- Complex relational queries required (user → roles → permissions)
- Team has more production experience with PostgreSQL
- Better tooling for schema migrations (Prisma, Drizzle)

## Consequences

### Positive
- Strong consistency guarantees
- Excellent query performance with proper indexing
- Mature ecosystem and tooling

### Negative
- Horizontal scaling more complex than NoSQL
- Schema migrations require careful planning

### Neutral
- Need to set up connection pooling (PgBouncer)

## Alternatives Considered

### MongoDB
**Pros:** Flexible schema, easy horizontal scaling
**Cons:** Eventual consistency, complex transactions
**Why not chosen:** ACID requirements for user data

### MySQL
**Pros:** Similar features, team familiarity
**Cons:** Less advanced features (JSON, arrays)
**Why not chosen:** PostgreSQL's superior feature set

## References
- [PostgreSQL 15 Release Notes](https://postgresql.org)
- [Team RFC: Database Selection](internal-link)
```

## ADR Organization

```
docs/
└── architecture/
    └── decisions/
        ├── README.md           # Index of all ADRs
        ├── 0001-use-postgresql.md
        ├── 0002-adopt-graphql.md
        ├── 0003-microservices-boundary.md
        └── template.md         # ADR template
```

## ADR Lifecycle

```
Proposed → Under Review → Accepted
                              ↓
                         In Effect
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
         Deprecated                    Superseded by new ADR
```

## Checklist

Before finalizing ADR:

- [ ] Context clearly explains the problem
- [ ] Decision is specific and actionable
- [ ] Alternatives were genuinely considered
- [ ] Consequences include negatives
- [ ] Status is correctly set
- [ ] Date is recorded
- [ ] Related ADRs are linked
- [ ] Stakeholders have reviewed
