---
name: architecture-decision-recorder
description: Create and manage Architecture Decision Records (ADRs) for documenting important architectural decisions, tradeoffs, and rationale.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Architecture Decision Recorder

Systematically document architectural decisions using the ADR pattern.

## When to Use

- Documenting significant architectural decisions
- Recording technology choices
- Tracking design tradeoffs
- Maintaining architectural history
- Facilitating team communication

## ADR Template

```markdown
# ADR-NNNN: [Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Decision Makers:** [Names]

## Context

What is the issue we're trying to solve? What are the forces at play?

### Business Context
- Business goal or requirement
- Constraints (time, budget, team)
- Stakeholder concerns

### Technical Context  
- Current system state
- Technical constraints
- Integration requirements

## Decision

We will [decision statement].

### Rationale
Why this approach over alternatives?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative  
- Tradeoff 1
- Tradeoff 2

### Risks
- Risk 1 → Mitigation strategy
- Risk 2 → Mitigation strategy

## Alternatives Considered

### Option 1: [Name]
**Pros:** [List]
**Cons:** [List]  
**Rejected because:** [Reason]

### Option 2: [Name]
**Pros:** [List]
**Cons:** [List]
**Rejected because:** [Reason]

## Implementation

- [ ] Action item 1
- [ ] Action item 2

## References

- [Link to research]
- [Related ADR]
```

## Best Practices

- ✅ Create ADRs for all major decisions
- ✅ Keep ADRs immutable (supersede, don't edit)
- ✅ Store in version control
- ✅ Link related ADRs
- ✅ Review quarterly
- ✅ Include quantitative data

## Related Commands

- `/adr-create` - Create new ADR
