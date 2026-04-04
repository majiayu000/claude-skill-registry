---
name: agents-md-generator
description: Generate hierarchical AGENTS.md structures for codebases. Use when user asks to create AGENTS.md files, analyze codebase for AI agent documentation, set up AI-friendly project documentation, or generate context files for AI coding assistants. Triggers on "create AGENTS.md", "generate agents", "analyze codebase for AI", "AI documentation setup", "hierarchical agents".
---

# AGENTS.md Generator

Generate hierarchical AGENTS.md structures optimized for AI coding agents with minimal token usage.

## Core Principles

1. **Root AGENTS.md is LIGHTWEIGHT** - Only universal guidance, links to sub-files (~100-200 lines max)
2. **Nearest-wins hierarchy** - Agents read closest AGENTS.md to file being edited
3. **JIT indexing** - Provide paths/globs/commands, NOT full content
4. **Token efficiency** - Small, actionable guidance over encyclopedic docs
5. **Sub-folder files have MORE detail** - Specific patterns, examples, commands

## Workflow

### Phase 1: Repository Analysis

Analyze and report:
1. **Repository type**: Monorepo, multi-package, or simple?
2. **Tech stack**: Languages, frameworks, key tools
3. **Major directories** needing own AGENTS.md:
   - Apps (`apps/web`, `apps/api`, `apps/mobile`)
   - Services (`services/auth`, `services/transcribe`)
   - Packages (`packages/ui`, `packages/shared`)
   - Workers (`workers/queue`, `workers/cron`)
4. **Build system**: pnpm/npm/yarn workspaces? Turborepo? Lerna?
5. **Testing setup**: Jest, Vitest, Playwright, pytest?
6. **Key patterns**: Organization, conventions, examples, anti-patterns

Present as structured map before generating files.

### Phase 2: Root AGENTS.md

Create lightweight root (~100-200 lines):

```markdown
# Project Name

## Project Snapshot
[3-5 lines: repo type, tech stack, note about sub-AGENTS.md files]

## Root Setup Commands
[5-10 lines: install, build all, typecheck all, test all]

## Universal Conventions
[5-10 lines: code style, commit format, branch strategy, PR requirements]

## Security & Secrets
[3-5 lines: never commit tokens, .env patterns, PII handling]

## JIT Index
### Package Structure
- Web UI: `apps/web/` -> [see apps/web/AGENTS.md](apps/web/AGENTS.md)
- API: `apps/api/` -> [see apps/api/AGENTS.md](apps/api/AGENTS.md)

### Quick Find Commands
- Search function: `rg -n "functionName" apps/** packages/**`
- Find component: `rg -n "export.*ComponentName" apps/web/src`
- Find API routes: `rg -n "export const (GET|POST)" apps/api`

## Definition of Done
[3-5 lines: what must pass before PR]
```

### Phase 3: Sub-Folder AGENTS.md

For each major package, create detailed AGENTS.md:

```markdown
# Package Name

## Package Identity
[2-3 lines: what it does, primary tech]

## Setup & Run
[5-10 lines: install, dev, build, test, lint commands]

## Patterns & Conventions
[10-20 lines - MOST IMPORTANT SECTION]
- File organization rules
- Naming conventions
- Examples with actual file paths:
  - DO: Use pattern from `src/components/Button.tsx`
  - DON'T: Class components like `src/legacy/OldButton.tsx`
  - Forms: Copy `src/components/forms/ContactForm.tsx`
  - API calls: See `src/hooks/useUser.ts`

## Key Files
[5-10 lines: important files to understand package]
- Auth: `src/auth/provider.tsx`
- API client: `src/lib/api.ts`
- Types: `src/types/index.ts`

## JIT Index Hints
[5-10 lines: search commands for this package]
- Find component: `rg -n "export function .*" src/components`
- Find hook: `rg -n "export const use" src/hooks`
- Find tests: `find . -name "*.test.ts"`

## Common Gotchas
[3-5 lines if applicable]
- "Auth requires NEXT_PUBLIC_ prefix for client-side"
- "Always use @/ imports for absolute paths"

## Pre-PR Checks
[2-3 lines: copy-paste command]
pnpm --filter @repo/web typecheck && pnpm --filter @repo/web test
```

### Phase 4: Special Templates

#### Design System / UI Package
```markdown
## Design System
- Components: `packages/ui/src/components/**`
- Use design tokens from `packages/ui/src/tokens.ts`
- Component gallery: `pnpm --filter @repo/ui storybook`
- Examples:
  - Buttons: `packages/ui/src/components/Button/Button.tsx`
  - Forms: `packages/ui/src/components/Input/Input.tsx`
```

#### Database / Data Layer
```markdown
## Database
- ORM: Prisma / Drizzle / TypeORM
- Schema: `prisma/schema.prisma`
- Migrations: `pnpm db:migrate`
- Connection: via `src/lib/db.ts` singleton
- NEVER run migrations in tests
```

#### API / Backend Service
```markdown
## API Patterns
- REST routes: `src/routes/**/*.ts`
- Auth middleware: `src/middleware/auth.ts`
- Validation: Zod schemas in `src/schemas/**`
- Errors: `ApiError` from `src/lib/errors.ts`
- Example: `src/routes/users/get.ts`
```

#### Testing
```markdown
## Testing
- Unit: `*.test.ts` colocated
- Integration: `tests/integration/**`
- E2E: `tests/e2e/**` (Playwright)
- Single test: `pnpm test -- path/to/file.test.ts`
- Mocks: `src/test/mocks/**`
```

## Output Format

Provide files in order:
1. Analysis Summary
2. Root AGENTS.md (complete)
3. Each Sub-Folder AGENTS.md (with file path)

Format:
```
---
File: `AGENTS.md` (root)
---
[content]

---
File: `apps/web/AGENTS.md`
---
[content]
```

## Quality Checklist

Before generating, verify:
- [ ] Root AGENTS.md under 200 lines
- [ ] Root links to all sub-AGENTS.md files
- [ ] Each sub-file has concrete examples (actual paths)
- [ ] Commands are copy-paste ready
- [ ] No duplication between root and sub-files
- [ ] JIT hints use actual patterns (ripgrep, find, glob)
- [ ] Every "DO" has real file example
- [ ] Every "DON'T" references real anti-pattern
- [ ] Pre-PR checks are single commands
