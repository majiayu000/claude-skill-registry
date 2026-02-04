---
name: adr
description: "Create Architecture Decision Records through interactive conversation. Use when making technology choices, architecture patterns, or third-party service selections."
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
---

# /adr

Create Architecture Decision Records through interactive conversation.

## Usage

```bash
/adr                                      # Start conversation
/adr "database selection for coordinatr"  # Provide topic
```

## Output Location

ADRs live with code in `spaces/`:

```
spaces/[project]/docs/project/adrs/
├── ADR-001-database-choice.md
├── ADR-002-auth-strategy.md
└── ADR-003-testing-strategy.md
```

## Execution Flow

### 1. Gather Context

```bash
# Current architecture
Read: spaces/[project]/docs/project/architecture-overview.md

# Existing ADRs
Glob: spaces/[project]/docs/project/adrs/ADR-*.md

# Project context
Read: ideas/[project]/project-brief.md

# Relevant research
Glob: resources/research/*.md
```

### 2. Interactive Conversation

Ask one at a time:

1. **What decision needs to be made?**
2. **Why is this decision needed now?**
3. **What options are you considering?** (2-4 alternatives)
4. **What are the constraints?** (time, budget, skills)
5. **What are the trade-offs for each?**
6. **Which option do you prefer and why?**

### 3. Research Support

If user unsure about options:
- Check existing research in `resources/research/`
- Suggest `/research` for deeper dive
- Use WebSearch for current best practices

### 4. Create ADR Document

```markdown
# ADR-###: [Decision Title]

**Status**: Accepted
**Date**: YYYY-MM-DD
**Decision Makers**: [who was involved]

## Context
[Why this decision is needed]

## Decision
We will use **[chosen option]** because [rationale].

## Options Considered

### Option 1: [Name]
**Pros**: ...
**Cons**: ...

### Option 2: [Name]
**Pros**: ...
**Cons**: ...

## Consequences

### Positive
- What we gain

### Negative
- What we lose
- Technical debt accepted

### Risks
- Risk and mitigation

## Related Decisions
- Links to related ADRs/specs

## References
- Documentation links
```

## When to Use

- Technology/framework selection
- Architecture patterns
- Third-party service choices
- Data modeling approaches
- Cross-project standards

**Not for**: Implementation details, temporary decisions, already-decided standards

## ADR Lifecycle

1. **Accepted** - Decision made, actively followed
2. **Deprecated** - No longer relevant
3. **Superseded** - Replaced by newer ADR

## Workflow

```
/brief -> /research -> /adr -> /spec
```
