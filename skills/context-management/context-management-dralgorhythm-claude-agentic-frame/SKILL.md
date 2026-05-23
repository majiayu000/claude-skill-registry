---
name: context-management
description: Manage project context effectively. Use when onboarding, context switching, or maintaining project knowledge. Covers context capture and sharing.
allowed-tools: Read, Write, Glob, Grep
---

# Context Management

## Why Context Matters

- Reduces ramp-up time
- Prevents repeated mistakes
- Enables informed decisions
- Facilitates collaboration

## Context Types

### Project Context
- What the project does
- Why it exists
- Who uses it
- Key constraints

### Technical Context
- Architecture decisions (ADRs)
- Technology choices
- Coding conventions
- Known issues

### Historical Context
- Why decisions were made
- What was tried before
- Lessons learned

## Context Capture

### Decision Log
```markdown
## Decision: [Title]
**Date**: [Date]
**Context**: [Why this came up]
**Decision**: [What was decided]
**Rationale**: [Why this choice]
**Consequences**: [What changed]
```

### Knowledge Base
- README for project overview
- ADRs for architecture
- CONTRIBUTING for development
- CHANGELOG for history

### Code Comments
```typescript
// CONTEXT: This retry logic exists because the external API
// has intermittent failures. See incident-123 for details.
// We chose exponential backoff after testing showed it
// reduces error rate by 80%.
```

## Context Sharing

### New Team Member
1. Start with README
2. Review key ADRs
3. Pair on first task
4. Introduce to stakeholders

### Handoff
1. Document current state
2. List open questions
3. Identify risks
4. Warm handoff meeting

## Best Practices

1. **Write it down**: Don't rely on memory
2. **Keep it current**: Update as things change
3. **Make it findable**: Organize logically
4. **Be specific**: Include the "why"
5. **Review regularly**: Remove stale info
