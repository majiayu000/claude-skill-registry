---
name: create-memory
description: Create memory files to track important learnings, decisions, and system changes. Use when implementing major features, making architectural decisions, or learning important project patterns.
allowed-tools: [Write, Edit, Read, Grep]
---

# Create Memory Files

Track important learnings and decisions in .claude/memory/ files.

## When to Use

- Just implemented major feature or system
- Made important architectural decision
- Discovered critical project patterns
- User says "remember this" or "track this"
- Solved complex bug with important learnings
- Established new workflow or standard

## Current Memory Files

```
.claude/memory/
├── research-first-enforcement.md  # How research-first is enforced
├── coding-standards.md            # TypeScript, style, errors
├── testing-standards.md           # NO MOCKS, Bun, Playwright
├── architecture-patterns.md       # Tech stack, patterns
├── common-workflows.md            # DB migrations, API, 3D, git
├── build-commands.md              # Dev, build, test commands
├── asset-forge-guide.md           # Project specifics
└── security-protocols.md          # Auth, API security, secrets
```

All imported in `CLAUDE.md` at root.

## Memory File Template

```markdown
# [Topic Name]

**Status**: [ACTIVE/DEPRECATED/IN-PROGRESS]
**Date**: [YYYY-MM-DD]
**Related**: [Other memory files, if any]

## Purpose

[Why this memory file exists - what problem does it solve?]

## Key Learnings

### 1. [Major Learning]
[Detailed explanation]

**Why it matters**: [Impact/importance]

### 2. [Major Learning]
[Detailed explanation]

**Example**:
\```[language]
[code example if applicable]
\```

## Implementation Details

[How this is actually implemented in the project]

**Files affected**:
- path/to/file1.ts
- path/to/file2.tsx

## Common Pitfalls

- ❌ [What NOT to do]
- ❌ [What NOT to do]
- ✅ [What to DO instead]

## Examples

### Good Example
\```[language]
[code showing correct pattern]
\```

### Bad Example
\```[language]
[code showing incorrect pattern]
\```

## Related Commands/Skills

- `/command-name` - [What it does]
- `skill-name` - [What it does]

## Future Considerations

[Things to watch out for, potential improvements]
```

## Example Memory Files to Create

**hyperscape-engine-integration.md**
- How Hyperscape engine integrates with asset-forge
- Game world architecture
- Asset loading patterns

**three-js-optimization-patterns.md**
- LOD strategies
- Instancing for repeated models
- Material reuse
- Disposal patterns

**privy-auth-integration.md**
- JWT verification patterns
- User session management
- Auth middleware setup

**drizzle-migration-workflow.md**
- How we create migrations
- Schema change patterns
- Rollback strategies

**api-testing-patterns.md**
- How we test Elysia routes
- No-mock testing approach
- Integration test setup

## After Creating Memory File

1. Add to CLAUDE.md imports:
```markdown
## [Section Name]

@.claude/memory/new-file-name.md
```

2. Verify import:
```bash
grep "new-file-name" CLAUDE.md
```

## Best Practices

- **Be specific** - Don't create vague "notes.md" files
- **Include examples** - Code examples make it memorable
- **Date it** - Track when learnings happened
- **Update existing** - Prefer updating existing memory over creating new
- **Reference files** - Link to actual code files affected
- **Mark status** - Is this current? Deprecated? In progress?

## Memory File Lifecycle

1. **Create** - When major learning happens
2. **Update** - As patterns evolve
3. **Reference** - Import in CLAUDE.md
4. **Deprecate** - Mark outdated when patterns change
5. **Archive** - Delete if truly obsolete (rare)

## Memory vs Documentation

**Memory files are for Claude**, not users:
- Internal patterns and decisions
- "Why we do X instead of Y"
- Critical learnings from past mistakes
- Project-specific conventions

**Documentation is for users**:
- README.md
- API docs
- User guides

Keep them separate.
