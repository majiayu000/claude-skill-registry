---
name: architecture-decision-records-(adrs)
model: reasoning
---

# Architecture Decision Records (ADRs)

## WHAT
Lightweight documentation capturing the context, decision, and consequences of significant technical choices. ADRs become the institutional memory of why things are built the way they are.

## WHEN
- Adopting new frameworks or technologies
- Choosing between architectural approaches
- Making database or infrastructure decisions
- Defining API design patterns
- Any decision that would be hard to reverse or understand later

## KEYWORDS
ADR, architecture decision record, technical documentation, decision log, MADR, RFC, design decisions, trade-offs


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install architecture-decision-records
```


---

## Quick Decision: Should I Write an ADR?

| Write ADR | Skip ADR |
|-----------|----------|
| New framework/language adoption | Minor version upgrades |
| Database technology choice | Bug fixes |
| API design patterns | Implementation details |
| Security architecture | Routine maintenance |
| Integration patterns | Configuration changes |
| Breaking changes | Code formatting |

---

## ADR Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

**Never modify accepted ADRs** - write new ones to supersede.

---

## Templates

### Template 1: Standard (Copy This)

```markdown
# ADR-NNNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context
[What is the issue? What forces are at play? 2-3 paragraphs max.]

## Decision
We will [decision statement].

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Risks
- [Risk and mitigation]

## Related
- ADR-XXXX: [Related decision]
```

### Template 2: Full (For Major Decisions)

```markdown
# ADR-0001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need to select a primary database for our e-commerce platform handling:
- ~10,000 concurrent users
- Complex product catalog with hierarchical categories
- Transaction processing for orders and payments
- Full-text search for products

The team has experience with MySQL, PostgreSQL, and MongoDB.

## Decision Drivers
- **Must have** ACID compliance for payment processing
- **Must support** complex queries for reporting  
- **Should support** full-text search to reduce infrastructure
- **Should have** good JSON support for flexible product attributes

## Considered Options

### Option 1: PostgreSQL
**Pros**: ACID compliant, excellent JSONB support, built-in full-text search, PostGIS
**Cons**: Slightly more complex replication than MySQL

### Option 2: MySQL
**Pros**: Familiar to team, simple replication
**Cons**: Weaker JSON support, no built-in full-text search

### Option 3: MongoDB
**Pros**: Flexible schema, native JSON
**Cons**: No ACID for multi-document transactions, team has limited experience

## Decision
We will use **PostgreSQL 15** as our primary database.

## Rationale
PostgreSQL provides the best balance of ACID compliance (essential for e-commerce), 
built-in capabilities (reduces infrastructure), and team familiarity.

## Consequences

### Positive
- Single database handles transactions, search, and geospatial
- Reduced operational complexity
- Strong consistency for financial data

### Negative
- Need PostgreSQL-specific training for team
- Vertical scaling limits may require read replicas

### Risks
- Full-text search may not scale as well as Elasticsearch
- **Mitigation**: Design for potential ES addition if needed

## Implementation Notes
- Use JSONB for flexible product attributes
- Implement connection pooling with PgBouncer
- Set up streaming replication for read replicas

## Related
- ADR-0002: Caching Strategy (Redis)
- ADR-0005: Search Architecture
```

### Template 3: Lightweight (For Smaller Decisions)

```markdown
# ADR-0012: Adopt TypeScript for Frontend

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: @alice, @bob

## Context
React codebase has 50+ components with increasing bugs from prop type mismatches.

## Decision
Adopt TypeScript for all new frontend code. Migrate existing code incrementally.

## Consequences
**Good**: Catch type errors at compile time, better IDE support  
**Bad**: Learning curve, initial slowdown  
**Mitigation**: Training sessions, `allowJs: true` for gradual adoption
```

### Template 4: Y-Statement (One-Liner)

```markdown
# ADR-0015: API Gateway Selection

In the context of **building a microservices architecture**,
facing **the need for centralized API management and rate limiting**,
we decided for **Kong Gateway**
and against **AWS API Gateway and custom Nginx**,
to achieve **vendor independence and plugin extensibility**,
accepting that **we need to manage Kong infrastructure ourselves**.
```

### Template 5: Deprecation ADR

```markdown
# ADR-0020: Deprecate MongoDB in Favor of PostgreSQL

## Status
Accepted (Supersedes ADR-0003)

## Context
ADR-0003 (2021) chose MongoDB for user profiles. Since then:
- MongoDB transactions remain problematic for our use case
- Our schema has stabilized and rarely changes
- Maintaining two databases increases operational burden

## Decision
Deprecate MongoDB and migrate user profiles to PostgreSQL.

## Migration Plan
1. **Week 1-2**: Create PostgreSQL schema, enable dual-write
2. **Week 3-4**: Backfill historical data, validate consistency
3. **Week 5**: Switch reads to PostgreSQL
4. **Week 6**: Remove MongoDB writes, decommission

## Lessons Learned
- Schema flexibility benefits were overestimated
- Operational cost of multiple databases was underestimated
```

---

## Directory Structure

```
docs/
└── adr/
    ├── README.md              # Index and guidelines
    ├── template.md            # Team's ADR template
    ├── 0001-use-postgresql.md
    ├── 0002-caching-strategy.md
    ├── 0003-mongodb-user-profiles.md  # [DEPRECATED]
    └── 0020-deprecate-mongodb.md      # Supersedes 0003
```

### ADR Index (README.md)

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-use-postgresql.md) | Use PostgreSQL | Accepted | 2024-01-10 |
| [0002](0002-caching-strategy.md) | Caching with Redis | Accepted | 2024-01-12 |
| [0003](0003-mongodb-user-profiles.md) | MongoDB for Profiles | Deprecated | 2023-06-15 |
| [0020](0020-deprecate-mongodb.md) | Deprecate MongoDB | Accepted | 2024-01-15 |

## Creating a New ADR
1. Copy `template.md` to `NNNN-title-with-dashes.md`
2. Fill in template, submit PR for review
3. Update this index after approval
```

---

## Tooling: adr-tools

```bash
# Install
brew install adr-tools

# Initialize
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL as Primary Database"

# Supersede an ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# Generate index
adr generate toc > docs/adr/README.md
```

---

## Review Checklist

Before submission:
- [ ] Context clearly explains the problem
- [ ] All viable options considered
- [ ] Pros/cons balanced and honest
- [ ] Consequences documented (positive AND negative)

During review:
- [ ] At least 2 senior engineers reviewed
- [ ] Affected teams consulted
- [ ] Security implications considered
- [ ] Reversibility assessed

After acceptance:
- [ ] Index updated
- [ ] Team notified
- [ ] Implementation tickets created

---

## NEVER

- **Modify accepted ADRs**: Write new ones to supersede
- **Skip context**: Future readers need the "why"
- **Hide failures**: Rejected decisions are valuable learning
- **Be vague**: Specific decisions, specific consequences
- **Forget implementation**: ADR without action is waste
- **Over-document**: Keep to 1-2 pages max
- **Document too late**: Write BEFORE implementation starts
