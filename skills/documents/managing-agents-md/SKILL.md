---
name: managing-agents-md
description: Creates and maintains AGENTS.md documentation files that guide AI coding agents through a codebase. Use when adding a significant new feature or directory, changing project architecture, setting up a new project or monorepo, noticing a codebase has no AGENTS.md, or after major refactors that change project structure. Also triggers on "document this for agents", "update agents.md", or "create agents.md".
---

# Managing AGENTS.md

## Overview

**AGENTS.md is a README for AI agents.** It tells any AI coding tool — Claude Code, Copilot, Cursor, Codex — how to navigate and work with your codebase. Keep it updated as the project evolves.

## When to Create or Update

**Create AGENTS.md when:**
- Setting up a new project or monorepo
- Adding a significant new feature directory (5+ related files)
- Introducing an extensible or polymorphic system
- A codebase has no AGENTS.md and you're doing substantial work in it

**Update AGENTS.md when:**
- Changing architectural patterns or project structure
- Adding new build/test/deploy commands
- Modifying base classes, registries, or extension points
- Adding significant new directories

**Do NOT create for:**
- Simple utility directories
- Single-purpose modules
- Non-extensible features
- Directories with fewer than 5 related files

## Tier Structure

For monorepos or large projects, use a hierarchical approach:

```
Root AGENTS.md         → Project overview, tech stack, global conventions
├── app/AGENTS.md      → App-specific architecture, commands, patterns
│   └── feature/AGENTS.md → Feature-specific extension points
```

Each tier adds specificity. Agents read from root down to the most relevant file.

## Template

```markdown
# AGENTS.md — [Project or Directory Name]

Brief one-line description of this part of the codebase.

## Commands

\`\`\`bash
npm run dev      # Start development server
npm test         # Run tests
npm run build    # Production build
\`\`\`

## Project Structure

\`\`\`
src/
├── api/          # REST endpoints (~12 files)
├── services/     # Business logic (~8 files)
├── models/       # Data models (~6 files)
└── utils/        # Shared utilities (~4 files)
\`\`\`

## Key Patterns

[Describe the main architectural patterns, data flow, or conventions]

## Boundaries

### Always
- [Pattern to always follow]
- [Convention to always use]

### Never
- [Anti-pattern to avoid]
- [Dangerous operation]

### Ask First
- [Risky change that needs confirmation]
```

## CLAUDE.md Companion

If the project also uses Claude Code, create a `CLAUDE.md` that imports the AGENTS.md:

```markdown
@AGENTS.md

## Claude-Specific
- [Any Claude Code-specific instructions, hooks, or skill references]
```

This avoids duplicating content while adding Claude-specific configuration.

## Anti-Patterns

**Stale documentation:** An outdated AGENTS.md is worse than none. Update it when the code changes.

**Too granular:** Don't create AGENTS.md for every directory. Only for significant architectural boundaries.

**Duplicating README:** AGENTS.md is for AI agents, not humans. Focus on what an agent needs to navigate and modify code correctly — commands, patterns, boundaries.
