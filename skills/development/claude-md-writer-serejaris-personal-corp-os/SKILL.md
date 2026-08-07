---
name: claude-md-writer
description: Use when creating or refactoring CLAUDE.md files - enforces best practices for size, structure, and content organization
---

# CLAUDE.md Writer

Creates and refactors CLAUDE.md files following official Anthropic best practices (2025).

## Golden Rules

| Rule | Why |
|------|-----|
| **CLAUDE.md < 200 lines** | Loads on EVERY request, costs tokens |
| **Rules files < 500 lines each** | Official recommendation per file |
| **Critical rules FIRST** | Top = highest priority |
| **Modular rules → `.claude/rules/`** | Conditional loading, organized |
| **Use `paths:` frontmatter** | Load rules only for matching files |
| **No linting rules** | Use ESLint/Prettier/Biome instead |
| **Pointers over copies** | Files change, references stay valid |

## Memory Hierarchy

Claude Code loads memory in this order (higher = higher priority):

| Priority | Type | Location |
|----------|------|----------|
| Highest | Enterprise | `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| ↓ | Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| ↓ | Rules | `./.claude/rules/*.md` (conditional) |
| ↓ | User | `~/.claude/CLAUDE.md` |
| Lowest | Local | `./CLAUDE.local.md` (gitignored) |

Use `/memory` command to see currently loaded files.

## 3-Tier Documentation System

Official recommendation for large projects:

| Tier | Location | Loads | Target |
|------|----------|-------|--------|
| **1. Foundation** | `CLAUDE.md` | Always | < 200 lines |
| **2. Component** | `.claude/rules/{component}/` | When working in component | < 500 lines |
| **3. Feature** | Co-located with code | When working on feature | As needed |

Example structure:
```
.claude/
├── CLAUDE.md                 # Tier 1: always loaded
└── rules/
    ├── database.md           # Tier 2: SQL, migrations
    ├── api.md                # Tier 2: API patterns
    └── frontend/             # Tier 2: subdirectory
        ├── components.md     # paths: src/**/*.tsx
        ├── layout.md         # paths: src/pages/**/*.tsx
        └── tokens.md         # paths: **/*.tsx
```

## Structure Template

```markdown
# Project Name

One-line description.

## Commands

- `npm run dev` - Development
- `npm run build` - Production
- `npm run test` - Tests

## Architecture

| Path | Purpose |
|------|---------|
| `lib/` | Core logic |
| `app/api/` | API routes |

## Key Patterns

**Pattern Name**: One-line explanation.

## Database (if applicable)

| Table | Key Fields |
|-------|------------|

## Modular Docs

See `.claude/rules/` for:
- `database.md` - queries, schema
- `deploy.md` - deployment

## Tech Stack

One line: Next.js 15, PostgreSQL, TypeScript
```

## Conditional Rules (Path-Specific)

Use YAML frontmatter for file-type-specific rules:

```markdown
---
paths: "src/api/**/*.ts"
---

# API Rules

- All endpoints must validate input
- Use standard error format
```

### Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All .ts files anywhere |
| `src/**/*` | All files under src/ |
| `*.md` | Markdown in project root |
| `src/components/*.tsx` | Components in specific dir |

### Combining Patterns

```yaml
# Multiple extensions
paths: "src/**/*.{ts,tsx}"

# Multiple directories
paths: "{src,lib}/**/*.ts, tests/**/*.test.ts"
```

**Note:** Wrap patterns in quotes for YAML safety.

Rules with `paths:` only load when working with matching files → saves tokens.

## Workflow: New Project

1. Run `/init` for base CLAUDE.md
2. Review and trim generated content
3. Identify critical rules — what breaks if ignored?
4. Create `.claude/rules/` for domain-specific docs
5. Keep main file < 100 lines

## Workflow: Refactor Existing

1. **Count lines** — if > 300, must split
2. **Find task-specific content** — SQL, debugging, deploy → extract
3. **Create `.claude/rules/`**:
   - `database.md` - queries, schema, connection
   - `deploy.md` - deployment process
   - `messaging.md` - integrations (Telegram, etc.)
4. **Use `@file` references** — don't duplicate
5. **Keep in CLAUDE.md** — only what applies to EVERY task

## What Goes Where

| Content | Location |
|---------|----------|
| Project description | CLAUDE.md |
| Critical constraints | CLAUDE.md (top!) |
| Quick start (3 commands) | CLAUDE.md |
| Architecture overview | CLAUDE.md |
| Key patterns (1-liners) | CLAUDE.md |
| SQL queries/schema | `.claude/rules/database.md` |
| Deployment steps | `.claude/rules/deploy.md` |
| API documentation | `.claude/rules/api.md` |
| Git workflow | `.claude/rules/git.md` |
| Personal preferences | `CLAUDE.local.md` (gitignored) |
| Code style rules | `.eslintrc` / `biome.json` (NOT docs) |

## Import Syntax

Reference files instead of duplicating:

```markdown
@README.md
@docs/architecture.md
@~/.claude/snippets/common.md
```

- Relative: `@docs/file.md`
- Absolute: `@~/path/file.md`
- Max depth: 5 hops

## CLAUDE.local.md

Personal project settings (auto-gitignored):

```markdown
# My Local Settings

- Prefer verbose output
- Run tests after every change
- My worktree location: .trees/
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 500+ lines | Split into `.claude/rules/` |
| SQL examples inline | → `rules/database.md` |
| "Run prettier" rules | Use tool config files |
| Full API docs | → `rules/api.md` |
| Deployment instructions | → `rules/deploy.md` |
| Code in CLAUDE.md | Use `@file:line` references |
| Negative rules only | Add alternatives: "Don't X; use Y instead" |

## Quality Checklist

Before finishing:

- [ ] CLAUDE.md < 200 lines?
- [ ] Each rules file < 500 lines?
- [ ] Critical rules at top?
- [ ] No task-specific content in main file?
- [ ] No code style rules (use ESLint/Prettier)?
- [ ] `.claude/rules/` for domain-specific docs?
- [ ] Subdirectories for components (frontend/, backend/)?
- [ ] `paths:` frontmatter for conditional loading?
- [ ] `@` references instead of duplication?
- [ ] CLAUDE.local.md for personal prefs?

## Useful Commands

| Command | Purpose |
|---------|---------|
| `/init` | Generate initial CLAUDE.md |
| `/memory` | View loaded memory files |

## Sources

Official:
- code.claude.com/docs/en/memory (Memory management, paths, globs)
- anthropic.com/engineering/claude-code-best-practices
- claude.com/blog/using-claude-md-files

Community:
- thedocumentation.org/claude-code-development-kit (3-Tier System)
- claudefa.st/blog/guide/mechanics/rules-directory
- humanlayer.dev/blog/writing-a-good-claude-md

Updated: Jan 2026
