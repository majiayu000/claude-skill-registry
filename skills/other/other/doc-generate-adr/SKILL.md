---
name: doc-generate-adr
description: Generate Architecture Decision Records (ADRs) to document significant architectural decisions. Use when making important technical decisions that need documentation.
mcp_fallback: none
category: doc
user-invocable: false
---

# Generate ADR Skill

Create Architecture Decision Records for technical decisions.

## When to Use

- Making significant architectural decisions
- Choosing between technical alternatives
- Documenting design trade-offs
- Recording rationale for future reference

## Quick Reference

```bash
./scripts/create_adr.sh "Decision Title"
# Creates: docs/adr/ADR-XXX-decision-title.md
```

## Workflow

1. **Identify decision** - What choice needs documentation?
2. **Research alternatives** - Gather evidence and performance data
3. **Create ADR** - Run script with title
4. **Fill sections** - Context, Decision, Rationale, Consequences, Alternatives
5. **Review** - Get team approval
6. **Update status** - Change from "Proposed" to "Accepted"

## ADR Format

All ADRs follow this structure:

```markdown
# ADR-XXX: Title

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Deciders**: Names/roles

## Context
What is the issue we're facing?

## Decision
What decision are we making?

## Rationale
Why this decision? Key reasons.

## Consequences
### Positive
- Benefit 1

### Negative
- Drawback 1

### Neutral
- Other impact 1

## Alternatives Considered
### Alternative 1
Why not chosen.
```

## Status Lifecycle

- **Proposed** - Under consideration
- **Accepted** - Decision made and active
- **Deprecated** - No longer recommended
- **Superseded** - Replaced by newer ADR

## Storage Location

```text
docs/adr/
├── ADR-001-language-selection.md
├── ADR-002-testing-strategy.md
└── README.md
```

## Error Handling

| Issue | Fix |
|-------|-----|
| Missing context | Add background and constraints |
| Unclear decision | Make decision more specific |
| Missing alternatives | Document at least 2 alternatives |
| No consequences | Think through positive and negative impacts |

## References

- See existing ADRs in `/docs/adr/` for examples
- Related skill: `phase-plan-generate` for planning
