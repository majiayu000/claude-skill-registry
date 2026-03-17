---
name: memory-hierarchy
description: Complete reference for Claude Code's memory management system including all file types, locations, import syntax, and best practices. Use when planning or managing CLAUDE.md and related memory files.
---

# Claude Code Memory Hierarchy

Complete reference for Claude Code's memory management system.

## Memory Locations (Highest to Lowest Priority)

| Memory Type | Location | Purpose | Shared With |
|-------------|----------|---------|-------------|
| **Enterprise policy** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Organization-wide standards (IT/DevOps managed) | All org users |
| **Project memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared project instructions | Team via git |
| **Project rules** | `./.claude/rules/*.md` | Modular, topic-specific instructions | Team via git |
| **User memory** | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Just you |
| **User rules** | `~/.claude/rules/*.md` | Personal modular rules | Just you |
| **Project local** | `./CLAUDE.local.md` | Personal project-specific preferences | Just you (gitignored) |

**Key:** Files higher in hierarchy load first; more specific memories take precedence.

## Memory Discovery

Claude Code discovers memory files by:

1. **Upward recursion**: From `cwd` up to (not including) root `/`
2. **Subtree discovery**: Nested CLAUDE.md loaded when reading files in those subtrees
3. **Automatic loading**: All `.claude/rules/*.md` files loaded with same priority as `.claude/CLAUDE.md`

**View loaded memories:** Run `/memory` command

## Import Syntax

CLAUDE.md files can import other files using `@path/to/file`:

```markdown
# Project Instructions

See @README.md for project overview.
See @docs/architecture.md for system design.
API reference: @docs/api/README.md

# Personal preferences (not in git)
@~/.claude/my-project-prefs.md
```

**Features:**
- Relative and absolute paths supported
- Home directory imports (`@~/...`) for personal preferences
- Not evaluated inside code blocks or code spans
- Recursive imports (max 5 hops)

## Modular Rules (`.claude/rules/`)

### Basic Structure

```
project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       ├── security.md     # Security requirements
│       └── api/
│           └── validation.md  # API-specific rules
```

### Path-Specific Rules

Use YAML frontmatter to scope rules to specific files:

```markdown
---
paths: src/api/**/*.ts
---

# API Development Rules

- All endpoints must include input validation
- Use the standard error response format
```

### Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/**/*` | All files under src/ |
| `*.md` | Markdown files in root |
| `src/**/*.{ts,tsx}` | TS and TSX in src/ |
| `{src,lib}/**/*.ts` | TS in src/ or lib/ |
| `tests/**/*.test.ts` | Test files |

**Multiple patterns:**
```yaml
---
paths: {src,lib}/**/*.ts, tests/**/*.test.ts
---
```

### Subdirectory Organization

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

All `.md` files discovered recursively.

### Symlink Support

Share rules across projects:

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

## User-Level Configuration

### User Memory (`~/.claude/CLAUDE.md`)

Personal preferences applying to ALL projects:
- Code style preferences
- Tooling shortcuts
- Workflow habits

### User Rules (`~/.claude/rules/`)

```
~/.claude/rules/
├── preferences.md    # Personal coding preferences
└── workflows.md      # Preferred workflows
```

User rules load before project rules; project rules take higher priority.

## Quick Memory Addition

### `#` Shortcut

Start input with `#`:
```
# Always use descriptive variable names
```
Prompts for which memory file to store in.

### `/memory` Command

Opens memory file in system editor for extensive additions.

### `/init` Command

Bootstrap a CLAUDE.md for your codebase.

## When to Use Each Memory Type

| Scenario | Recommended Location |
|----------|---------------------|
| Team coding standards | `./CLAUDE.md` |
| Build/test/lint commands | `./CLAUDE.md` |
| Topic-specific rules (testing, API, security) | `./.claude/rules/{topic}.md` |
| File-type-specific patterns | `./.claude/rules/` with `paths:` |
| Personal code style | `~/.claude/CLAUDE.md` |
| Your local dev URLs/setup | `./CLAUDE.local.md` |
| Org-wide compliance | Enterprise policy (IT managed) |

## Decision Tree: Choosing Memory Structure

```
Project Analysis
│
├─ Small project (<500 files, <50 dirs)?
│   └─ Single ./CLAUDE.md
│       └─ Use @imports for large documentation
│
├─ Medium project with topic diversity?
│   └─ ./CLAUDE.md + .claude/rules/
│       ├─ testing.md
│       ├─ code-style.md
│       └─ {topic}.md
│
├─ Monorepo / microservices?
│   └─ Multiple ./CLAUDE.md (one per package/service)
│       └─ Each can have own .claude/rules/
│
├─ File-type-specific patterns?
│   └─ Path-specific rules with paths: frontmatter
│
└─ Personal dev setup needed?
    └─ ./CLAUDE.local.md (gitignored automatically)
```

## Best Practices

### Content Guidelines

- **Be specific**: "Use 2-space indentation" > "Format code properly"
- **Use structure**: Bullet points under descriptive headings
- **Review periodically**: Update as project evolves

### Rules Organization

- **Keep rules focused**: Each file covers one topic
- **Use descriptive filenames**: `testing.md`, `api-design.md`, `security.md`
- **Use paths: sparingly**: Only when rules truly apply to specific file types
- **Organize with subdirectories**: Group related rules

### Project vs Personal

- **Project memory**: What the team needs to know
- **User memory**: Your personal preferences
- **Local memory**: Your dev environment specifics

## File Priority Summary

When the same topic is covered in multiple files:

1. Enterprise policy (highest)
2. Project `.claude/rules/` (path-specific first)
3. Project `CLAUDE.md`
4. User `~/.claude/rules/`
5. User `~/.claude/CLAUDE.md`
6. Project `CLAUDE.local.md` (lowest, but most specific to you)

## Common Patterns

### Imports for Documentation

```markdown
# Project Overview

See @README.md for getting started.
Architecture details: @docs/architecture.md
API reference: @docs/api/README.md
```

### Topic-Specific Rules

```
.claude/rules/
├── testing.md          # Test patterns, mocking, coverage
├── api-design.md       # REST conventions, error handling
├── database.md         # Query patterns, migrations
└── security.md         # Auth, validation, secrets
```

### Path-Specific API Rules

```markdown
---
paths: src/api/**/*.ts, src/routes/**/*.ts
---

# API Endpoint Rules

- Validate all inputs with zod
- Use consistent error response format
- Include OpenAPI documentation comments
```

### Personal Local Setup

`./CLAUDE.local.md`:
```markdown
# My Local Setup

## Dev URLs
- API: http://localhost:3001
- Frontend: http://localhost:3000
- Database: postgresql://localhost:5432/mydb

## Debug Commands
```bash
DEBUG=api:* npm run dev
```
```
