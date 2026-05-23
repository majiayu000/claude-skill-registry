---
name: memory-management
description: Guide for managing Claude Code memory effectively. Use when setting up project memory, optimizing CLAUDE.md files, configuring rules directories, or establishing cross-session knowledge patterns. Covers memory hierarchy, best practices, and context optimization.
allowed-tools: ["Read", "Write", "Edit", "Glob"]
---

# Memory Management

Master Claude Code's memory system for persistent context across sessions, projects, and teams.

## Quick Reference

| Memory Type | Location | Scope | Priority | Use For |
|-------------|----------|-------|----------|---------|
| Global | `~/.claude/CLAUDE.md` | All projects | Lowest | Personal preferences, global conventions |
| Project Root | `./CLAUDE.md` | Project-wide | Medium | Project context, tech stack, conventions |
| Project Config | `./.claude/CLAUDE.md` | Project-wide | Medium | Same as root (alternative location) |
| Rules | `./.claude/rules/*.md` | Conditional | Highest | Modular, file-specific instructions |

## Memory Hierarchy

Claude Code reads memory files in this order (later overrides earlier):

```
~/.claude/CLAUDE.md           # Your global preferences
  |
  v
./CLAUDE.md                   # Project root instructions
  |
  v
./.claude/CLAUDE.md           # Project config directory
  |
  v
./.claude/rules/*.md          # Conditional rules (when matched)
```

### Priority Rules

1. **Rules always win** - When a rule file matches, its instructions take precedence
2. **Project overrides global** - Project CLAUDE.md supersedes global settings
3. **Later loads override earlier** - Last-loaded content has highest priority
4. **Explicit beats implicit** - Specific rules override general guidelines

## When to Use Each Memory Type

### Use Global Memory (`~/.claude/CLAUDE.md`) For

- Personal coding preferences (tabs vs spaces, quote style)
- Universal tool preferences (Bun over npm, rg over find)
- Cross-project conventions you always follow
- Personal workflow shortcuts

**Example:**
```markdown
# Global Preferences

## Code Style
- Use single quotes for strings
- Prefer for-loops over forEach
- Use Bun instead of npm

## Tools
- Use ripgrep (rg) for searching, not grep
- Prefer Edit over Write for modifications
```

### Use Project Memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`) For

- Project-specific tech stack (React, Bun, Drizzle, etc.)
- Build and test commands
- Architecture overview
- Team conventions
- File structure explanations

**Example:**
```markdown
# Project: E-Commerce API

## Tech Stack
- Runtime: Bun
- Framework: Hono
- Database: PostgreSQL with Drizzle ORM
- Testing: Bun test

## Commands
- `bun dev` - Start development server
- `bun test` - Run all tests
- `bun db:migrate` - Run database migrations

## Architecture
- `/src/routes` - API route handlers
- `/src/services` - Business logic
- `/src/db` - Database schema and queries
```

### Use Rules (`./.claude/rules/*.md`) For

- File-type-specific instructions (TypeScript, React, SQL)
- Conditional guidance based on file paths
- Modular memory that loads only when relevant
- Team standards that apply to specific areas

**Example:**
```
.claude/rules/
  react-components.md     # Globs: src/components/**/*.tsx
  api-routes.md           # Globs: src/routes/**/*.ts
  database.md             # Globs: src/db/**/*.ts, *.sql
  tests.md                # Globs: **/*.test.ts, **/*.spec.ts
```

## CLAUDE.md Structure

A well-structured CLAUDE.md file includes:

```markdown
# Project Name

Brief description (1-2 sentences).

## Commands
- `bun install` - Install dependencies
- `bun dev` - Start development
- `bun test` - Run tests
- `bun build` - Build for production

## Tech Stack
- Runtime/Framework
- Database
- Key libraries

## Architecture
Brief overview of project structure.

## Code Style
Project-specific conventions.

## Important Notes
Critical information Claude should always know.
```

For detailed CLAUDE.md guidance, see [CLAUDE-MD.md](./CLAUDE-MD.md).

## Rules Directory

The `.claude/rules/` directory contains modular memory files that load conditionally.

### Rule File Anatomy

```yaml
---
globs: ["src/components/**/*.tsx", "src/ui/**/*.tsx"]
description: React component conventions for this project
alwaysApply: false
---

# React Components

Follow these patterns for React components...
```

### Glob Matching

- **Exact match**: `src/utils.ts`
- **Directory**: `src/components/**/*`
- **Extension**: `**/*.tsx`
- **Multiple**: `["*.ts", "*.tsx"]`

For complete rules documentation, see [RULES.md](./RULES.md).

## Best Practices

### Do Include

- Commands with exact syntax
- Tech stack overview
- Key architectural decisions
- Non-obvious conventions
- Error-prone areas

### Do NOT Include

- Code that's easily discoverable (read the files instead)
- Verbose documentation (link instead)
- Information that changes frequently
- Full API documentation

### Keep Memory Focused

```markdown
## Good - Actionable and Specific

- Use Drizzle ORM for database queries
- Run `bun test` before committing
- Components go in `src/components/{feature}/`

## Avoid - Vague or Obvious

- Write clean code
- Test your changes
- Follow best practices
```

### Reference, Don't Duplicate

```markdown
## Good - Reference External Docs

See API documentation at `docs/api.md`.
Architecture diagrams in `docs/architecture/`.

## Avoid - Duplicating Content

[Pasting entire API documentation here]
```

## Memory Strategies

### Project Onboarding

When starting with a new project:

1. **Create minimal CLAUDE.md** with commands and tech stack
2. **Add rules** for the main file types you work with
3. **Expand gradually** as you discover project quirks
4. **Update regularly** when conventions change

### Team Conventions

For team projects:

1. **Commit CLAUDE.md** and `.claude/rules/` to version control
2. **Keep personal preferences** in `~/.claude/CLAUDE.md`
3. **Document decisions** in rules files, not code comments
4. **Review memory files** during onboarding

### Cross-Session Continuity

To maintain context across sessions:

1. **Session hooks** can inject recent context at start
2. **Weave framework** captures learnings for future sessions
3. **Project memory** persists architectural decisions
4. **Rules files** encode learned patterns

For advanced memory strategies, see [STRATEGIES.md](./STRATEGIES.md).

## Common Patterns

### Monorepo Pattern

```
project/
  CLAUDE.md                    # Shared conventions
  .claude/
    rules/
      frontend.md              # Globs: apps/web/**/*
      backend.md               # Globs: apps/api/**/*
      packages.md              # Globs: packages/**/*
  apps/
    web/
      CLAUDE.md                # Web-specific context
    api/
      CLAUDE.md                # API-specific context
```

### Feature Flag Pattern

```markdown
# .claude/rules/feature-flags.md
---
globs: ["src/**/*.ts", "src/**/*.tsx"]
---

## Feature Flags

Active flags:
- `ENABLE_NEW_CHECKOUT` - New checkout flow (enabled in staging)
- `DARK_MODE` - Dark mode support (enabled everywhere)

Check flags with: `useFeatureFlag('FLAG_NAME')`
```

### Migration Pattern

```markdown
# .claude/rules/migrations.md
---
globs: ["src/db/migrations/**/*.ts"]
---

## Database Migrations

1. Generate: `bun db:generate`
2. Run: `bun db:migrate`
3. Rollback: `bun db:rollback`

Naming: `NNNN_description.ts`
Always include down migration.
```

## Reference Files

| File | Contents |
|------|----------|
| [CLAUDE-MD.md](./CLAUDE-MD.md) | Deep dive on CLAUDE.md structure and content |
| [RULES.md](./RULES.md) | Complete rules directory documentation |
| [STRATEGIES.md](./STRATEGIES.md) | Advanced memory strategies |

## Validation Checklist

Before finalizing memory setup:

- [ ] Global preferences in `~/.claude/CLAUDE.md`
- [ ] Project context in `./CLAUDE.md` or `./.claude/CLAUDE.md`
- [ ] Modular rules for file-specific guidance
- [ ] Commands section with exact syntax
- [ ] Tech stack clearly documented
- [ ] No duplicated documentation
- [ ] Rules have appropriate glob patterns
- [ ] Memory files committed to version control

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting everything in global | Use project memory for project-specific content |
| Giant CLAUDE.md files | Split into rules files for modular loading |
| Duplicating docs | Reference external documentation instead |
| Vague instructions | Be specific and actionable |
| Stale content | Review and update memory periodically |
| Missing commands | Always include build/test/run commands |
