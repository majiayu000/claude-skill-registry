---
name: memory
description: Filesystem-based knowledge management. Triggers on "remember", "save context", "knowledge base", "document decision".
---

# Memory

A filesystem-based knowledge management system where source code IS the memory. Store decisions, patterns, and context in structured markdown files.

## When to Use

- Recording architectural decisions
- Documenting patterns discovered during development
- Saving context about why something was built a certain way
- Tracking known issues and workarounds
- Storing API documentation or integration notes

## When NOT to Use

- Temporary debugging notes (use comments instead)
- Task tracking (use git issues or project board)

## Core Principles

- Source code is the single source of truth
- Store knowledge close to where it's used
- Use structured markdown for consistency
- Keep files focused (one topic per file)

## Storage Locations

| Type | Location | Example |
|------|----------|---------|
| Technical docs | `docs/technical/` | Architecture decisions, patterns |
| Feature docs | `docs/features/` | Feature specifications, requirements |
| API docs | `docs/api/` | API contracts, integration notes |

## Memory Operations

### Remember (Write)

Store new knowledge:

```markdown
# [Topic Title]

## Context
[Why this exists, what problem it solves]

## Decision
[What was decided and why]

## Details
[Technical details, code examples]

## References
- [Related files or URLs]

---
*Created: [date]*
*Last updated: [date]*
```

### Recall (Read)

Retrieve knowledge:
1. Check `docs/` directory structure
2. Read relevant files
3. Search for keywords across docs

### Update

Modify existing knowledge:
1. Read the existing file
2. Update the relevant section
3. Add to evolution history if significant

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| feature-dev | Store architectural decisions during development |
| planning | Document the plan for future reference |
