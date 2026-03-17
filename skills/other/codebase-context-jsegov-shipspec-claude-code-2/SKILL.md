---
name: codebase-context
description: This skill should be used when the user asks to "analyze the codebase", "understand the tech stack", "extract project patterns", "get codebase context", "what technologies are used", or when preparing context for planning documents, PRDs, or design documentation.
version: 0.1.0
allowed-tools: Read, Glob, Grep, Bash(find:*), Bash(head:*), Bash(cat:*), Bash(ls:*), Bash(wc:*)
---

# Codebase Context Extraction

Extract and summarize codebase context for planning purposes. This skill provides quick analysis approaches for different project types and standardized output formats.

## Quick Analysis Approach

### 1. Detect Tech Stack

**JavaScript/TypeScript Projects:**
```bash
cat package.json 2>/dev/null | head -60
```

Identify from output:
- `dependencies` / `devDependencies` for frameworks
- `scripts` for build/test commands
- `type: "module"` for ESM

**Python Projects:**
```bash
cat pyproject.toml 2>/dev/null || cat requirements.txt 2>/dev/null | head -30
```

**Go Projects:**
```bash
cat go.mod 2>/dev/null | head -15
```

**Rust Projects:**
```bash
cat Cargo.toml 2>/dev/null | head -30
```

### 2. Map Project Structure

```bash
# Get directory tree (excluding noise)
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' -not -path '*/target/*' | sort | head -40
```

```bash
# Count files by type
find . -type f -name "*.ts" -o -name "*.tsx" | wc -l
find . -type f -name "*.py" | wc -l
find . -type f -name "*.go" | wc -l
```

### 3. Find Key Documentation

```bash
# Project docs
ls -la README* CLAUDE* AGENTS* CONTRIBUTING* 2>/dev/null
```

```bash
# Config files
ls -la *.json *.yaml *.toml .env* 2>/dev/null
```

### 4. Identify Patterns

**API Structure:**
```bash
# REST endpoints
grep -r "app\.\(get\|post\|put\|delete\)" --include="*.ts" --include="*.js" | head -10
```

**Component Patterns:**
```bash
# React components
find . -path '*/components/*' -name "*.tsx" | head -10
```

**Database Models:**
```bash
# Schema definitions
find . -name "schema*" -o -name "*model*" | grep -v node_modules | head -10
```

## Output Format

Structure codebase context summaries as:

```markdown
## Technology Stack

**Language:** [e.g., TypeScript 5.x]
**Runtime:** [e.g., Node.js 20, Bun 1.x]
**Framework:** [e.g., Next.js 14 (App Router), FastAPI]
**Database:** [e.g., PostgreSQL with Drizzle ORM]
**Styling:** [e.g., Tailwind CSS]
**Testing:** [e.g., Vitest, Playwright]

## Project Structure

- `src/` - Main source code
  - `components/` - React components
  - `lib/` - Utility functions
  - `app/` - Next.js app router pages
- `tests/` - Test files

## Key Patterns

- [Pattern 1: e.g., "Server components by default, client components marked explicitly"]
- [Pattern 2: e.g., "API routes use zod for validation"]
- [Pattern 3: e.g., "Error handling uses Result types"]

## Conventions

- Package manager: [pnpm/npm/yarn/bun]
- Code style: [ESLint + Prettier config]
- Commit style: [Conventional commits]
- Branch strategy: [main + feature branches]

## Existing Documentation

- README.md: [brief summary]
- CLAUDE.md: [if exists, key points]
- AGENTS.md: [if exists, key points]
```

## Integration Notes

This context should be:
1. Saved to `.shipspec/planning/<feature>/context.md` temporarily during planning
2. Used by PRD and design document generation
3. Referenced when creating implementation tasks

**Note:** The context file is automatically cleaned up after task generation completes. The relevant context is incorporated into the PRD, SDD, and TASKS.md files.

## Common Tech Stack Indicators

| Indicator | Technology |
|-----------|------------|
| `next.config.js` | Next.js |
| `vite.config.ts` | Vite |
| `tailwind.config.js` | Tailwind CSS |
| `drizzle.config.ts` | Drizzle ORM |
| `prisma/schema.prisma` | Prisma ORM |
| `pyproject.toml` | Modern Python |
| `go.mod` | Go modules |
| `Cargo.toml` | Rust |

## Quality Checklist

Before finalizing context extraction:

- [ ] Tech stack versions identified
- [ ] Project structure mapped
- [ ] Key patterns documented
- [ ] Existing documentation referenced
- [ ] Conventions noted
