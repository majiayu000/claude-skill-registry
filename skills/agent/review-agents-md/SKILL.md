---
name: review-agents-md
description: Creates minimal, effective AGENTS.md files using progressive disclosure. Triggers on "create agents.md", "refactor agents.md", "review my agents.md", "claude.md", or questions about agent configuration files. Also triggers proactively when a project is missing AGENTS.md.
---

# AGENTS.md Skill

## Overview

Creates and refactors AGENTS.md files following progressive disclosure principles. Keeps files minimal and focused—avoiding the "ball of mud" that hurts agent performance.

## When to Use

- **Proactively** when a project has no `AGENTS.md` at the root — check for this when starting work in a new project
- Creating a new AGENTS.md from scratch
- Refactoring a bloated AGENTS.md
- Reviewing an existing file for best practices
- Setting up AGENTS.md for a monorepo
- When `AGENTS.md` exists but `CLAUDE.md` is missing (should be symlinked)

## Core Principles

1. **Minimal by default**: Only include what's relevant to every single task
2. **Progressive disclosure**: Point to separate files, external docs, or agent skills for domain-specific rules
3. **Never document file structure**: It goes stale fast and poisons agent context
4. **Describe capabilities, not locations**: "Auth uses JWT" not "Auth is in src/auth/"

### The Instruction Budget

Frontier LLMs can follow ~150-200 instructions with reasonable consistency. Every token in AGENTS.md loads on **every request**, regardless of relevance. The ideal file should be as small as possible.

### Why Files Get Bloated

Agent does something wrong → you add a rule → repeat hundreds of times → "ball of mud." Different developers add conflicting opinions. Nobody does a full style pass. Auto-generated files make this worse by prioritizing comprehensiveness over restraint.

### Stale Docs Poison Context

Humans can be skeptical of outdated docs. Agents can't — they trust what they read on every request. File paths are especially dangerous since they change constantly. Describe capabilities and domain concepts instead.

## Process

### Phase 0: Detect Missing Files

Check the project root for `AGENTS.md` and `CLAUDE.md`:

1. If **neither** exists, offer to create `AGENTS.md` and symlink `CLAUDE.md` to it
2. If `AGENTS.md` exists but `CLAUDE.md` does not, create the symlink: `ln -s AGENTS.md CLAUDE.md`
3. If `CLAUDE.md` exists but `AGENTS.md` does not, rename it to `AGENTS.md` and create a symlink: `mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md`
4. If both exist but `CLAUDE.md` is not a symlink to `AGENTS.md`, merge any unique content into `AGENTS.md`, remove the standalone `CLAUDE.md`, and create the symlink

### Phase 1: Assess Current State

**For new projects:**
- Ask about the project's purpose (one sentence)
- Ask about package manager (if not npm)
- Ask about non-standard build commands

**For existing files:**
- Read the current AGENTS.md
- Count lines and estimate token cost
- Identify content that belongs elsewhere

### Phase 2: Apply the Essential Test

Only these belong in root AGENTS.md:

| Include | Why |
|---------|-----|
| One-sentence project description | Anchors every agent decision |
| Package manager (if not npm) | Prevents wrong commands |
| Non-standard build/test commands | Saves trial and error |
| Links to domain-specific docs | Progressive disclosure |

Everything else goes in separate files or gets deleted.

### Phase 3: Identify Anti-Patterns

Flag these for removal or relocation:

- **File tree structures**: Always go stale, waste tokens
- **Obvious instructions**: "Write clean code", "Use meaningful names"
- **Contradictory rules**: Often from multiple contributors
- **Language-specific conventions**: Move to `docs/TYPESCRIPT.md` etc.
- **Workflow instructions**: Move to `docs/GIT.md` or `docs/TESTING.md`

### Phase 4: Create Progressive Disclosure Structure

For content that shouldn't be deleted:

```
docs/
├── TYPESCRIPT.md    # TS conventions
├── TESTING.md       # Test patterns
├── API.md           # API design rules
└── GIT.md           # Commit/PR conventions
```

Reference these from AGENTS.md with light-touch pointers. Keep the tone conversational — no "ALWAYS," no all-caps forcing:

```markdown
For TypeScript conventions, see docs/TYPESCRIPT.md
```

Each file can reference the next — agents walk the tree on demand, only loading what's relevant.

Link to external docs when they're the authoritative source rather than restating them:

```markdown
For database migrations, follow the Prisma migration guide.
```

Agent skills are another layer of progressive disclosure. Instead of embedding procedures in AGENTS.md, package them as skills the agent pulls in when needed. The root file stays focused on *what* and *where*; skills handle *how*.

### Phase 5: Handle Monorepos

For monorepos, use nested AGENTS.md files:

**Root AGENTS.md:**
```markdown
Monorepo for [purpose]. Uses [pnpm/yarn] workspaces.
See each package's AGENTS.md for specifics.
```

**Package AGENTS.md** (e.g., `packages/api/AGENTS.md`):
```markdown
GraphQL API using Prisma. See docs/API_CONVENTIONS.md for patterns.
```

### Phase 6: Output

Provide:
1. The new/refactored AGENTS.md content
2. Any new files created for progressive disclosure
3. List of removed content with reasoning

## Output Format

When creating a new AGENTS.md:

```markdown
# [Project Name]

[One-sentence description of what this project does.]

[Package manager if not npm]

[Non-standard commands if any]

[Light-touch pointers to separate docs if needed]
```

## Example: Minimal AGENTS.md

```markdown
# Acme Dashboard

React admin dashboard for managing customer accounts and billing.

Uses pnpm. Run `pnpm check` for type checking.

For API conventions, see docs/API.md
For component patterns, see docs/COMPONENTS.md
```

That's 6 lines. Every token earns its place.

## Refactoring Prompt

When refactoring an existing bloated file, follow these steps:

1. **Find contradictions**: Identify conflicting instructions. Ask which to keep.
2. **Identify essentials**: Extract only what belongs in root — project description, package manager, non-standard commands, content relevant to every task.
3. **Group the rest**: Organize into logical categories. Create separate files.
4. **Create structure**: Output minimal root AGENTS.md with links to separate files.
5. **Flag for deletion**: Identify instructions that are redundant, vague, or obvious.

## Decision Framework

Before adding anything to AGENTS.md:

| Location | When to use |
|----------|-------------|
| Root AGENTS.md | Relevant to every single task |
| Separate file | Relevant to one domain |
| Nested docs | Fits hierarchical organization |
| Delete it | Obvious, redundant, or vague |

## Cross-Tool Compatibility

AGENTS.md is an open standard supported by 20+ tools including:

- **GitHub Copilot** (Coding Agent)
- **Cursor**
- **Codex** (OpenAI)
- **Gemini CLI** (Google)
- **Windsurf**, **Devin** (Cognition)
- **Zed**, **Warp**, **VS Code**
- **Aider**, **goose**, **RooCode**

**Claude Code** uses `CLAUDE.md` instead. `AGENTS.md` is always the source of truth. `CLAUDE.md` must always be a symlink pointing to it:

```bash
ln -s AGENTS.md CLAUDE.md
```

Never create a standalone `CLAUDE.md`. Never put content in `CLAUDE.md` that isn't in `AGENTS.md`.

## Resources

- https://agents.md — The AGENTS.md specification
- https://www.aihero.dev/a-complete-guide-to-agents-md — Guide that informed this skill's best practices
