---
name: explain
description: Document the reasoning behind implementation decisions as markdown files. Creates decision records that future developers can reference.
allowed-tools: Read, Grep, Glob, Write
user-invocable: true
---

# Explain (Decision Documentation)

Create decision records that document the reasoning behind implementation choices.

## Philosophy

Good code is self-documenting for *what* it does. But *why* it does it that way? That's lost to time unless we capture it.

> "Six months from now, when someone asks 'Why did we do it this way?', will there be an answer?"

The value of this skill isn't compliance—it's **preserving context** that makes the codebase maintainable.

## Config Integration

Check for `.inclusion-config.md` in the project root.

**Decisions location** (in order of precedence):
1. `Decisions location` setting in config
2. Existing `decisions/` directory
3. Existing `docs/decisions/` or `docs/adr/` directory
4. Default: create `decisions/`

If no config exists, ask the user where to store decisions or use the default.

## When to Use

Run `/explain` after:
- Completing a significant implementation
- Making an architectural decision
- Choosing between multiple valid approaches
- Implementing something counterintuitive
- When future developers might ask "why was it done this way?"

## Input

The user will provide:
- File path(s) to explain, OR
- Feature/change description, OR
- Specific question ("Why did we use X instead of Y?")

If nothing provided, explain recent uncommitted changes.

## Process

### 1. Understand the Decisions

For the code being explained, identify:
- Key architectural choices
- Algorithm or pattern selections
- Library/dependency choices
- Trade-offs that were made
- Constraints that influenced the approach

### 2. Research Context

Gather context before writing:
- What patterns exist elsewhere in the codebase?
- Were there constraints from existing code?
- What does the task file or PR description say?
- What alternatives could have been used?

### 3. Generate File Name

Use the pattern: `NNNN-short-description.md`

- Check existing files in decisions directory
- Use next available number (0001, 0002, etc.)
- Keep description short (2-4 words, kebab-case)

Examples:
- `0001-use-zustand-for-state.md`
- `0002-jwt-over-sessions.md`
- `0003-monorepo-structure.md`

### 4. Write Decision Record

Create the file in the decisions directory.

## Output Format

```markdown
# [Number]. [Decision Title]

**Date**: [YYYY-MM-DD]
**Status**: Accepted
**Context**: [What prompted this decision]

## Decision

[1-2 sentence summary of what was decided]

## Why This Approach

- [Primary reason]
- [Secondary reason]
- [Constraint that influenced this]

## Alternatives Considered

### [Alternative A]

**Pros**: [benefits]
**Cons**: [drawbacks]
**Why not**: [specific reason rejected]

### [Alternative B]

**Pros**: [benefits]
**Cons**: [drawbacks]
**Why not**: [specific reason rejected]

## Trade-offs Accepted

- [What we gave up and why it's acceptable]

## Consequences

- [What this decision means for future development]
- [Things to watch out for]

## Related

- [Links to related code, PRs, or other decisions]
```

## After Writing

Output confirmation:

```markdown
## Decision Record Created

**File**: `decisions/0003-use-zustand-for-state.md`

### Summary
Documented decision to use Zustand over Redux for state management.

### Key Points
- Simpler API reduces boilerplate
- Trade-off: Less ecosystem tooling
- Revisit if: Complex state debugging needed
```

## Why This Matters

Decision records serve multiple purposes:
- **Onboarding**: New developers understand architectural choices
- **Maintenance**: Future changes can respect original constraints
- **Accountability**: Decisions are traceable and reviewable
- **Learning**: The team builds shared understanding over time

Without this context, teams make the same decisions repeatedly, or worse—undo good decisions because they don't understand why they were made.
