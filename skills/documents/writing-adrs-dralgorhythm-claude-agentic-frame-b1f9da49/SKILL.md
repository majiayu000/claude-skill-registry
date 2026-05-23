---
name: writing-adrs
description: Document architectural decisions. Use when making significant technical decisions that should be recorded. Covers ADR format and decision documentation.
allowed-tools: Read, Write, Glob, Grep
---

# Writing Architecture Decision Records

## What is an ADR?

An Architecture Decision Record captures an important architectural decision along with its context and consequences.

## When to Write an ADR

- Choosing a framework or library
- Selecting a database or storage solution
- Defining API patterns
- Establishing coding conventions
- Making infrastructure decisions
- Any decision that affects multiple components

## ADR Structure

### Title
Short phrase describing the decision.

### Status
- **Proposed**: Under discussion
- **Accepted**: Decision made
- **Rejected**: Considered but not adopted
- **Deprecated**: No longer valid
- **Superseded**: Replaced by another ADR

### Context
What is the situation? What forces are at play?

### Decision
What is the change we're making?

### Rationale
Why is this the best choice?

### Consequences
What are the trade-offs? Both positive and negative.

## Example ADR

```markdown
# ADR: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a database for our new service. Requirements:
- ACID transactions
- JSON support
- Strong ecosystem
- Team familiarity

## Decision
We will use PostgreSQL 15+ as our primary database.

## Rationale
- Mature, reliable RDBMS
- Excellent JSON support with JSONB
- Strong extension ecosystem (pgvector, PostGIS)
- Team has deep PostgreSQL experience
- Well-supported by all cloud providers

## Consequences
### Positive
- Reliable, battle-tested technology
- Rich feature set
- Easy to find developers

### Negative
- Vertical scaling has limits
- Requires careful connection management
- More operational overhead than managed NoSQL
```

## Best Practices

1. **Keep them short**: 1-2 pages max
2. **Write when deciding**: Not after the fact
3. **Include alternatives**: Show what was considered
4. **Update status**: Mark deprecated/superseded ADRs
5. **Number sequentially**: `ADR-001`, `ADR-002`, etc.
