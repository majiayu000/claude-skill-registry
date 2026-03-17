---
name: init-deep
description: Generates hierarchical context files (CLAUDE.md) throughout a project directory tree, providing AI agents with directory-specific knowledge for better code understanding. Use when setting up a new project for AI-assisted development.
---

# Init Deep — Hierarchical Context Generator

Automatically generates layered context files throughout a project's directory tree, giving AI agents directory-specific knowledge without loading the entire codebase into context.

## When to Use This Skill

- Setting up a new project for AI-assisted development
- Onboarding AI agents to an existing codebase
- After major restructuring when context files are outdated
- When AI agents lack understanding of project-specific conventions

## What This Skill Does

### Concept

Create an `CLAUDE.md` file at each significant directory level:

```
project/
├── CLAUDE.md              # Project-wide: overview, conventions, anti-patterns
├── src/
│   ├── CLAUDE.md          # src-specific: architecture, module boundaries
│   ├── api/
│   │   └── CLAUDE.md      # API-specific: routes, middleware, auth patterns
│   └── components/
│       └── CLAUDE.md      # Component-specific: naming, props, styling
├── tests/
│   └── CLAUDE.md          # Test-specific: frameworks, fixtures, patterns
└── infra/
    └── CLAUDE.md          # Infra-specific: deployment, configs, secrets
```

When an AI reads `src/api/routes/auth.ts`, it automatically picks up context from:
1. `project/CLAUDE.md` (project-wide)
2. `project/src/CLAUDE.md` (source conventions)
3. `project/src/api/CLAUDE.md` (API patterns)

### Generation Process

1. **Scan** the project structure (respect `.gitignore`)
2. **Analyze** each directory:
   - What files are here? What do they do?
   - What patterns/conventions are used?
   - What are the key dependencies?
   - What should an AI know before editing files here?
3. **Generate** CLAUDE.md with:
   - OVERVIEW: What this directory contains
   - STRUCTURE: Key files and their purposes
   - WHERE TO LOOK: Task-to-file mapping table
   - CONVENTIONS: Naming, patterns, style rules
   - ANTI-PATTERNS: What NOT to do here
   - COMMANDS: Relevant build/test/run commands

### Content Guidelines

Each CLAUDE.md should be:
- **Concise** — Under 100 lines. AI context window is precious.
- **Actionable** — "WHERE TO LOOK" tables, not prose descriptions
- **Specific** — Conventions for THIS directory, not general advice
- **Current** — Regenerate after major restructuring

### Root CLAUDE.md Template

```markdown
# PROJECT KNOWLEDGE BASE

## OVERVIEW
[1-2 sentences: what this project is]

## STRUCTURE
[Directory tree with annotations]

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Add a feature | src/features/ | One dir per feature |
| Fix a bug | src/core/ | Core logic here |
| Add a test | tests/ | Mirror src/ structure |

## CONVENTIONS
- [Naming rules]
- [Pattern rules]
- [Import rules]

## ANTI-PATTERNS
- Do NOT [common mistake 1]
- Do NOT [common mistake 2]

## COMMANDS
[Build, test, lint, deploy commands]
```

## Options

- `--max-depth=N` — Limit directory depth (default: 3)
- `--create-new` — Only create new files, don't overwrite existing

## Example

**User**: "Set up CLAUDE.md files for this project"

**Output**: Scans project, generates 6 CLAUDE.md files across the directory tree. Root file has project overview, src/ file has architecture notes, each major subdirectory gets specific conventions and anti-patterns.

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) /init-deep command
