---
name: docs-generator
description: Generate hierarchical documentation structures (AGENTS.md, agent.d, and custom docs) for codebases. Use when user asks to create documentation files, analyze codebase for AI agent documentation, set up AI-friendly project documentation, or generate context files for AI coding assistants. Triggers on "create documentation", "generate docs", "analyze codebase for AI", "documentation setup", "hierarchical docs".
---

# Documentation Generator

Generate hierarchical documentation structures optimized for AI coding agents with minimal token usage. Supports AGENTS.md, agent.d, and custom documentation formats.

## Core Principles

1. **Root documentation is LIGHTWEIGHT** - Only universal guidance, links to sub-files (~100-200 lines max)
2. **Nearest-wins hierarchy** - Agents read closest documentation to file being edited
3. **JIT indexing** - Provide paths/globs/commands, NOT full content
4. **Token efficiency** - Small, actionable guidance over encyclopedic docs
5. **Sub-folder files have MORE detail** - Specific patterns, examples, commands
6. **Flexible output formats** - Support for AGENTS.md, agent.d, and custom documentation types

## Workflow

### Phase 0: Document Type Confirmation

Before generating, confirm with user:
1. **Document format**: AGENTS.md, agent.d, or custom name?
2. **Target audience**: AI agents, developers, or both?
3. **Scope**: Root only, sub-folders only, or full hierarchy?
4. **Special requirements**: Any specific sections or patterns?

### Phase 1: Repository Analysis

Analyze and report:
1. **Repository type**: Monorepo, multi-package, or simple?
2. **Tech stack**: Languages, frameworks, key tools
3. **Major directories** needing own documentation:
   - Apps (`apps/web`, `apps/api`, `apps/mobile`)
   - Services (`services/auth`, `services/transcribe`)
   - Packages (`packages/ui`, `packages/shared`)
   - Workers (`workers/queue`, `workers/cron`)
4. **Build system**: pnpm/npm/yarn workspaces? Turborepo? Lerna?
5. **Testing setup**: Jest, Vitest, Playwright, pytest?
6. **Key patterns**: Organization, conventions, examples, anti-patterns

Present as structured map before generating files.

### Phase 2: Root Documentation

Create lightweight root (~100-200 lines):

#### For AGENTS.md format:
```markdown
# Project Name

## Project Snapshot
[3-5 lines: repo type, tech stack, note about sub-documentation files]

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

#### For agent.d format:
```d
# Project Name

## project_snapshot
repo_type: "monorepo"
tech_stack: ["typescript", "react", "node"]
note: "See subdirectories for agent.d files"

## root_setup
install: "pnpm install"
build: "pnpm build"
test: "pnpm test"
typecheck: "pnpm typecheck"

## conventions
code_style: "prettier + eslint"
commit_format: "conventional"
branch_strategy: "gitflow"

## jit_index
packages = {
  web_ui = "apps/web/agent.d"
  api = "apps/api/agent.d"
}

## quick_find
search_function = "rg -n \"functionName\" apps/** packages/**"
find_component = "rg -n \"export.*ComponentName\" apps/web/src"
find_api = "rg -n \"export const (GET|POST)\" apps/api"
```

#### For Custom Documentation:
```markdown
# Project Documentation

## Overview
[Brief project description and architecture]

## Getting Started
[Setup instructions for new developers]

## Architecture
[High-level system design and patterns]

## Development Guidelines
[Coding standards and best practices]

## Module Index
[Links to detailed documentation for each module]
```

### Phase 3: Sub-Folder Documentation

For each major package, create detailed documentation:

#### AGENTS.md format:
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

#### agent.d format:
```d
# Package Name

## package_identity
purpose = "React web application"
tech = ["react", "typescript", "tailwind"]

## setup
install = "pnpm install"
dev = "pnpm dev"
build = "pnpm build"
test = "pnpm test"
lint = "pnpm lint"

## patterns
file_organization = """
src/
  components/    # React components
  hooks/         # Custom hooks
  lib/           # Utilities
  types/         # TypeScript types
"""

naming = "PascalCase for components, camelCase for functions"

examples = [
  { do = "Use pattern from src/components/Button.tsx" }
  { dont = "Class components like src/legacy/OldButton.tsx" }
  { forms = "Copy src/components/forms/ContactForm.tsx" }
  { api = "See src/hooks/useUser.ts" }
]

## key_files
auth = "src/auth/provider.tsx"
api_client = "src/lib/api.ts"
types = "src/types/index.ts"

## jit_hints
find_component = "rg -n \"export function .*\" src/components"
find_hook = "rg -n \"export const use\" src/hooks"
find_tests = "find . -name \"*.test.ts\""

## gotchas
[
  "Auth requires NEXT_PUBLIC_ prefix for client-side"
  "Always use @/ imports for absolute paths"
]

## pre_pr_checks
command = "pnpm --filter @repo/web typecheck && pnpm --filter @repo/web test"
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
2. Root documentation (complete)
3. Each Sub-Folder documentation (with file path)

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

Or for agent.d:
```
---
File: `agent.d` (root)
---
[content]

---
File: `apps/web/agent.d`
---
[content]
```

Or for custom documentation:
```
---
File: `README.dev.md` (root)
---
[content]

---
File: `apps/web/README.dev.md`
---
[content]
```

## Quality Checklist

Before generating, verify:
- [ ] Root documentation under 200 lines
- [ ] Root links to all sub-documentation files
- [ ] Each sub-file has concrete examples (actual paths)
- [ ] Commands are copy-paste ready
- [ ] No duplication between root and sub-files
- [ ] JIT hints use actual patterns (ripgrep, find, glob)
- [ ] Every "DO" has real file example
- [ ] Every "DON'T" references real anti-pattern
- [ ] Pre-PR checks are single commands
- [ ] Document format matches user requirements
- [ ] All requested sections are included
