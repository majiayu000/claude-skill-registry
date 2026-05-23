---
name: writing-tech-plans
description: Architectural planning and ADR creation. Use when evaluating feasibility, making technology choices, or defining system integration.
---

# Technical Planning

Plan architecture and document decisions. Default to creating ADRs for significant decisions.

## Architectural Focus

1. **System impact** - What existing systems does this touch?
2. **Boundaries** - Where does this feature start and end?
3. **Integration** - How does it connect to existing components?
4. **Data flow** - How does information move through the system?
5. **Trade-offs** - What are we gaining and giving up?

## ADRs

Create an ADR when choosing between technologies, selecting authentication approaches, introducing new patterns, or making trade-offs with long-term implications.

### ADR Format

```markdown
# ADR-{NNN}: {Decision Title}

**Status**: Proposed | Accepted | Rejected | Superseded
**Date**: YYYY-MM-DD

## Context

[Why is this decision needed?]

## Decision

[Clear statement of what was decided]

## Alternatives Considered

### {Alternative 1}
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## Consequences

### Positive
- [Benefit]

### Negative
- [Trade-off]
- **Mitigation**: [How handled]
```

Scan `docs/adr/` for existing ADRs and increment the highest number.

## Technical Overview

Location: `specs/YYYY-MM-DD-feature-name/technical-details.md`

### Structure

```markdown
# Technical Overview: {Feature Name}

## Summary
[2-3 sentences]

## Architecture

### System Context
[How this fits into the broader system]

### Component Boundaries
[Components involved and responsibilities]

### Data Flow
[How data moves through the system]

## Integration Points
- **{System A}**: [How it integrates]

## Decisions
| Decision | ADR |
|----------|-----|
| [Choice] | [ADR-NNN](../docs/adr/NNNN-title.md) |

## Security Considerations
[Auth, authorization, data protection]

## Risks and Constraints
- **{Risk}**: [Description and mitigation]

## Open Questions
- [Unresolved questions]
```

## Exclusions

Do not include: specific file paths, implementation order, code snippets, line-by-line details, time estimates, or timeline references.

## Guidelines

Confirm feasibility before designing. Document decisions as ADRs. Trust implementers with the how. Think in systems and ripple effects. Address security by default.

## Templates

- `templates/technical-details.md` - Technical overview
- `templates/adr-template.md` - ADR template
- `references/adr-guide.md` - ADR guidelines
