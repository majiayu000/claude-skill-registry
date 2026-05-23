---
name: implementation-planning
description: >-
  Create technical implementation plans and architecture designs. Use when someone needs a detailed
  technical approach before coding begins — "create a plan", "plan this ticket", "how should we
  implement this", "technical design", "architect this", "design the approach", "plan the migration",
  "refactor plan", "how should we structure this", or when shaped work or a groomed ticket needs
  a concrete implementation strategy with phases, file changes, and verification steps.
---

# Implementation Planning

Take a ticket, shaped work, or technical challenge and create a detailed implementation plan that any developer or agent can follow.

## Plan Mode

**Multi-phase plans** → use plan mode:
1. If not already in plan mode, call `EnterPlanMode`
2. Research using sub-agents (see below)
3. Write plan to BOTH locations:
   - The internal plan file (path in system message)
   - `thoughts/plans/YYYY-MM-DD-descriptive-name.md` (persistent)
4. Call `ExitPlanMode` when done

**Simple designs** (single-phase, quick approach discussion) → skip plan mode, just discuss.

### Plan File Storage

Save plans to `thoughts/plans/` — this is the persistent, shareable location. The internal Claude Code plan file is temporary.

```
thoughts/plans/YYYY-MM-DD-descriptive-name.md
```

Use TODAY'S DATE from system context as prefix (e.g., "Today's date" in env info).

## Design Philosophy

Before writing plans, read [references/software-design-philosophy.md](references/software-design-philosophy.md). Apply these principles when designing module boundaries, interfaces, and decomposition. Key checks: modules should be deep, information hiding, define errors out of existence, design it twice.

## Principles

- **Research first** — understand the codebase before proposing solutions
- **Be specific** — include file paths, function names, code snippets
- **Be skeptical** — question assumptions, identify risks early
- **Be practical** — focus on incremental, testable changes
- **Agent-agnostic** — plan should work for any implementer
- **Follow patterns** — match existing codebase conventions

## Process

### 1. Gather Context

Launch parallel `Explore` sub-agents before planning. Each serves a different purpose:

```
# 1. LOCATE — find where relevant files live (don't read contents, just map locations)
Agent(subagent_type="Explore", prompt="Find all files related to [feature/domain].
  Group by: routes, use-cases/business logic, components, DB schema, tests.
  Report file paths and directory structure only, don't read contents.")

# 2. PATTERNS — find similar implementations to model after (read code, extract complete examples)
Agent(subagent_type="Explore", prompt="Find similar implementations to [what we're building].
  Read the code thoroughly. Extract complete working examples with imports.
  Note file organization, naming conventions, error handling approach.")

# 3. ANALYZE — trace how an existing related feature works end-to-end
Agent(subagent_type="Explore", prompt="Analyze how [related feature] is implemented.
  Trace the data flow from entry point to DB/API.
  Map key functions, their inputs/outputs, and error handling paths.")
```

Use all three when the feature is complex. For simpler tasks, locate + patterns may suffice.

**Also gather:**
- Related research docs in `thoughts/research/`
- The tech stack:

```markdown
**Package manager:** pnpm/npm/yarn
**Build tool:** turbo/nx/none
**Language:** TypeScript (strict mode?)
**Runtime:** Node.js/Bun/Deno
**Framework:** Fastify/Express/Hono
**Database:** Postgres + Drizzle/Prisma
**Testing:** Vitest/Jest
**Patterns to follow:** [reference existing implementations]
```

**For monorepo projects:**
- Package structure from `pnpm-workspace.yaml`
- Build configuration from `turbo.json`
- Existing packages for patterns to follow

Ask clarifying questions if requirements are ambiguous.

### 2. Present Options (If Multiple Approaches Exist)

Present trade-offs clearly:
- Option A: [approach] — Pros/Cons
- Option B: [approach] — Pros/Cons
- Recommendation: [which and why]

Get alignment before detailed planning.

### 3. Write the Plan

Create a structured plan following the output format below.

## Output Format

```markdown
# [Title] - Implementation Plan

## Overview
[1-2 sentences: what we're building and why]

## Current State
[What exists now, what's missing, relevant code locations]

## Desired End State
[What should work when done, how to verify — include example commands/usage]

## Out of Scope
[Explicitly list what we're NOT doing — prevents scope creep]

## Implementation Approach
[High-level strategy and reasoning]

---

## Phase 1: [Descriptive Name]

### What This Accomplishes
[Summary of this phase's goal]

### Changes

**File**: `path/to/file.ext`

```[language]
// Complete code to add or modify
// Not snippets — full implementation
```

**File**: `path/to/another.ext`

```[language]
// Complete code
```

### Verification
- [ ] [Specific command to run]
- [ ] [Expected output or behavior]

---

## Phase 2: [Descriptive Name]
[Same structure as Phase 1]

---

## Testing Strategy

### Manual Verification
```bash
# Step-by-step commands to verify everything works
command1
command2
```

### Automated (if applicable)
- [ ] Unit tests: [what to test]
- [ ] Integration tests: [what scenarios]

## File Summary
```
directory/
├── file1.ext           # Purpose
├── file2.ext           # Purpose
└── subdirectory/
    └── file3.ext       # Purpose
```

**Total new files:** N files

## Related Research
- `thoughts/research/YYYY-MM-DD-name.md` — [what it covers]

## Open Questions
[List any unresolved questions — or "None" if all resolved]
```

## Phase Guidelines

**Good phases:**
- Each phase is independently verifiable
- Earlier phases don't break existing functionality
- Later phases build on earlier ones
- Can pause between phases if needed

**Phase sizing:**
- Small enough to verify quickly
- Large enough to be meaningful
- Typically 1-3 files per phase
- Each phase should have clear verification steps

**Code in phases:**
- Include COMPLETE code, not snippets
- Show the full file content or the full function
- Never use "..." or "// rest of code"
- Someone should be able to copy-paste and have it work

## What Makes a Good Plan

**Good** (specific, actionable):
- File paths exist or clearly describe where to create
- Code snippets show COMPLETE implementation
- Verification steps are concrete commands
- Expected outputs documented

**Bad** (vague, hand-wavy):
- "Update the relevant components"
- "Add appropriate error handling"
- "Test thoroughly"
- Code snippets with "..." placeholders

## Example

**Input ticket**: "Add database package with Drizzle ORM"

**Output plan** (abbreviated):

```markdown
# Database Package - Implementation Plan

## Overview
Create `packages/db` with Drizzle ORM for PostgreSQL, following monorepo patterns from jp-partner-platform.

## Current State
- Monorepo exists with Fastify API + Temporal worker
- Postgres in docker-compose (port 5462)
- No database package yet

## Desired End State
```bash
# Package builds successfully
pnpm --filter=@repo/db build

# Migrations work
pnpm --filter=@repo/db generate
pnpm --filter=@repo/db migrate

# Types available in other packages
import { users } from "@repo/db/schema"
```

## Out of Scope
- API endpoints using the database
- Seed data
- Production deployment config

---

## Phase 1: Package Setup

### What This Accomplishes
Create the package skeleton with Drizzle configuration.

### Changes

**File**: `packages/db/package.json`
```json
{
  "name": "@repo/db",
  "type": "module",
  "exports": {
    ".": { "default": "./dist/index.js" },
    "./schema": { "default": "./dist/schema/index.js" }
  },
  "scripts": {
    "build": "tsc",
    "generate": "drizzle-kit generate",
    "migrate": "drizzle-kit migrate"
  },
  "dependencies": {
    "drizzle-orm": "^0.44.0",
    "postgres": "^3.4.7"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.0"
  }
}
```

**File**: `packages/db/drizzle.config.ts`
```typescript
import { defineConfig } from "drizzle-kit"

export default defineConfig({
  schema: "./src/schema/index.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL ?? "postgresql://postgres:postgres@localhost:5462/mydb",
  },
})
```

### Verification
- [ ] `pnpm install` succeeds
- [ ] `pnpm --filter=@repo/db build` succeeds

---

## Phase 2: Schema Definition
[...]
```

## Handoffs

- After plan approval, use `/dev-skills:implement-change` to execute phase by phase
- The plan in `thoughts/plans/` serves as the source of truth during implementation
