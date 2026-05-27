---
name: writing-rules
description: Use when creating project rules, adding .claude/rules/*.md files, or scoping rules to specific files with globs for token efficiency.
---

# Writing Project Rules

## Overview

Project rules provide context-specific instructions to Claude. This skill covers creating file-scoped rules that minimize token usage by only loading when relevant files are touched.

## When to Use

- Creating new project rules
- Adding `.claude/rules/*.md` files
- Scoping rules to specific files with globs
- Setting up doc-sync reminders (update X when Y changes)

## Rule File Locations

| Location | Scope | Loaded When |
| -------- | ----- | ----------- |
| `.claude/CLAUDE.md` | Project-wide | Always |
| `.claude/rules/*.md` | File-specific | When globs match |
| `~/.claude/CLAUDE.md` | User global | Always (all projects) |
| `~/.claude/rules/*.md` | User file-specific | When globs match |

## Workflow

### 1. Choose Scope

- **Project-wide** (commits, general info) → `.claude/CLAUDE.md`
- **File-specific** (component rules, doc sync) → `.claude/rules/*.md` with globs

### 2. Create File-Scoped Rule

```markdown
---
globs: src/api/**/*.ts
---

# API Rules

- Use Result types for errors
- Validate inputs at boundaries
```

### 3. Use Appropriate Glob Patterns

```
*.ts                    # All .ts files anywhere
src/**/*.ts             # All .ts in src tree
fish/config.fish        # Exact file match
{src,lib}/**/*.ts       # Multiple directories
```

Multiple globs:

```markdown
---
globs:
  - src/api/**/*.ts
  - src/services/**/*.ts
---
```

## Example: Doc Sync Rule

When modifying a file should trigger doc updates:

```markdown
---
globs: fish/config.fish
---

# Git Dashboard

When modifying `_git_*` functions:

- Update `fish/GIT_DASHBOARD_DESIGN.md` after visible changes
```

## Key Principles

1. **Prefer globs over project-wide** - reduces token usage
2. **Keep rules concise** - they consume context tokens
3. **One concern per rule file** - easier to maintain
4. **Multiple rules can match** - all matching rules apply
