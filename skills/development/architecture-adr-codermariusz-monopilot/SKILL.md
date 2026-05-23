---
name: architecture-adr
description: When making significant architectural decisions that need to be documented. Used by ARCHITECT-AGENT.
version: 1.0.0
tokens: ~400
confidence: high
sources:
  - https://adr.github.io/
  - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [architecture, adr, decisions, documentation]
---

## When to Use
When making significant architectural decisions that need to be documented. Used by ARCHITECT-AGENT.

## Patterns

### ADR Structure
```markdown
# ADR-001: {Decision Title}

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
{What situation requires a decision?}

## Decision Drivers
- {Driver 1}
- {Driver 2}

## Considered Options
1. **Option A** - {brief description}
2. **Option B** - {brief description}
3. **Option C** - {brief description}

## Decision
We will use **Option B** because {reasoning}.

## Consequences
### Positive
- {benefit 1}

### Negative
- {tradeoff 1}
```

### Option Evaluation
```markdown
| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Effort | High | Medium | Low |
| Risk | Low | Medium | High |
| Scalability | Good | Good | Poor |
| Team expertise | Low | High | Medium |
```

### When to Write ADR
```
- Technology choice (framework, database, cloud)
- Architecture pattern (monolith vs microservices)
- Integration approach (sync vs async)
- Security model changes
- Breaking changes to APIs
```

## Anti-Patterns
- Decisions without documented alternatives
- Missing "why not" for rejected options
- No consequences section
- ADR written after implementation
- Superseded ADRs not linked

## Verification Checklist
- [ ] Context explains the problem
- [ ] At least 2 options considered
- [ ] Decision clearly stated with reasoning
- [ ] Both positive and negative consequences
- [ ] Status is current
- [ ] Related ADRs linked
