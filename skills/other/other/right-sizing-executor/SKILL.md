---
name: right-sizing-executor
description: |
  Takes a plan or PRD and evaluates each story's size for AI execution.
  Splits oversized stories into context-window-friendly chunks, orders by dependency,
  and provides an execution framework. Use before handing work to autonomous agents.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Right-Sizing Executor

Break down plans into context-window-sized stories ready for execution.

---

## Quick Start

1. **Point it at your plan.** Run `/right-sizing-executor path/to/prd.md` or paste a feature description directly.
2. **Review the output.** The skill produces `tasks/execution-plan-[feature].md` with dependency-ordered, right-sized stories. Each story fits in one context window.
3. **Hand stories to agents (or yourself).** Execute them in order. Each story has acceptance criteria you can verify before moving on.

---

## Overview

AI agents work best on focused, well-scoped tasks. This skill takes any plan, PRD, or feature description and:

1. Evaluates each story/task for size
2. Splits anything too large for a single context window
3. Orders stories by dependency
4. Outputs an execution-ready plan

---

## The Job

### Input

Any of:
- A PRD markdown file (read from path)
- A feature description (pasted text)
- A list of tasks/stories
- A plan file from plan mode

### Output

An execution plan saved to `tasks/execution-plan-[feature].md` with:
- Right-sized stories
- Dependency order
- Size estimates
- Execution notes

---

## Commands

### `/right-sizing-executor [path-or-description]`

Analyze and right-size the given plan.

### `/right-sizing-executor check [path]`

Check an existing execution plan for sizing issues without rewriting it.

---

## The Core Rule

> **Each story must be completable in ONE context window.**
>
> If you cannot describe the change in 2-3 sentences, it is too big.

---

## Sizing Heuristics

### Small (1 context window, no split needed)

- Schema/migration change only
- Add a single UI component to an existing page
- Update one server action or API endpoint
- Add a configuration file
- Write tests for an existing function
- Fix a single bug with known cause

**Signal**: Change touches 1-3 files, logic fits in head.

### Medium (1 context window, might be tight)

- Backend logic with tests
- Full-page UI component with state
- API endpoint with validation and error handling
- Database query optimization with before/after verification

**Signal**: Change touches 3-5 files, has clear boundaries.

### Large (split required)

- Multi-file refactor
- Feature with both backend and frontend
- "Build the entire X"
- Integration with external service
- Anything requiring multiple dependent steps

**Signal**: Change touches 5+ files, has internal dependencies.

---

## Splitting Strategy

### Step 1: Identify the vertical slices

Each slice should be independently verifiable.

**Good slices** (each can be checked independently):
1. Database schema + migration
2. Backend service/action
3. API endpoint
4. UI component
5. Integration/wiring
6. Tests

**Bad slices** (cannot be checked independently):
1. "All the types"
2. "All the utilities"
3. "Half the component"

### Step 2: Order by dependency

```
Schema → Backend → API → UI → Integration → Tests
```

Earlier stories must NOT depend on later ones.

### Step 3: Write acceptance criteria

Each story gets verifiable criteria. Not "works correctly" but specific checks:

- "Column exists in database with correct type and default"
- "API returns 200 with expected JSON shape"
- "Button renders and onClick triggers handler"
- "Typecheck passes"

---

## Output Format

```markdown
# Execution Plan: [Feature Name]

**Source**: [PRD path or description]
**Generated**: [Date]
**Total Stories**: [N]
**Estimated Complexity**: [Low/Medium/High]

---

## Dependency Graph

```
S-001 (schema)
  └─> S-002 (backend)
        └─> S-003 (API)
              └─> S-004 (UI)
```

---

## Stories

### S-001: [Title]
**Size**: Small
**Depends on**: None
**Description**: [2-3 sentences max]
**Files**: [expected files to touch]
**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Typecheck passes

### S-002: [Title]
**Size**: Small
**Depends on**: S-001
**Description**: [2-3 sentences max]
**Files**: [expected files to touch]
**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Typecheck passes

---

## Split Decisions

| Original Item | Decision | Reason |
|---|---|---|
| "Add user dashboard" | Split into 4 stories | Touches schema, API, 2 UI components |
| "Add status field" | Keep as-is | Single migration + column |

---

## Notes

- [Any context for the executor]
```

---

## Size Check Signals

When evaluating if a story is too big, look for these red flags:

| Red Flag | Example | Action |
|---|---|---|
| "and" in description | "Add auth and dashboard" | Split at "and" |
| Multiple file types | ".sql + .ts + .tsx" | Split by layer |
| Words like "entire", "full", "complete" | "Build complete settings page" | Split into components |
| More than 3 acceptance criteria | 6 checkboxes | Consider splitting |
| Vague criteria | "Works correctly" | Rewrite before sizing |
| Dependencies within story | "After creating the table, build the UI" | Split at dependency boundary |

---

## Complexity Scoring

Assign each story a 1-5 complexity score before sizing. This makes split decisions more consistent and gives executors a sense of effort.

### Scoring Rubric

| Factor | Points | How to Count |
|---|---|---|
| Files touched | 1 point per 2 files | Count expected files in the story. 1-2 files = 1pt, 3-4 = 2pt, 5-6 = 3pt |
| Layers crossed | 1 point per layer | Layers: database, backend logic, API/route, UI component, styling. A schema-only change crosses 1 layer. A full-stack feature crosses 4-5 |
| External dependencies | 2 points each | Third-party APIs, new npm packages, external services, auth providers. Each one adds integration risk |
| State management changes | 1 point | Modifying global state, adding new stores, changing state shape, cache invalidation logic |

### Score Interpretation

| Score | Size | Recommendation |
|---|---|---|
| 1-2 | Small | Execute as-is. Single context window, straightforward |
| 3 | Medium | Likely fits one context window but review acceptance criteria carefully. Consider splitting if criteria exceed 4 items |
| 4 | Large | Split required. Find the natural boundary (usually at a layer crossing) |
| 5+ | Too large | Must split. Likely contains multiple independent features combined into one |

### Example Scoring

**"Add user profile page with avatar upload"**
- Files: `schema.sql`, `profile.service.ts`, `upload.service.ts`, `profile.route.ts`, `ProfilePage.tsx`, `AvatarUpload.tsx` = 3 points (6 files)
- Layers: DB + backend + API + UI = 4 points
- External deps: S3 for avatar storage = 2 points
- State: user profile state in store = 1 point
- **Total: 10 points.** Split into at least 3 stories: schema + backend, avatar upload service, UI components.

Add the score to each story in the execution plan output:

```markdown
### S-001: Add profile columns to users table
**Size**: Small | **Complexity**: 2
```

---

## Multi-Language Projects

Monorepos often contain code in multiple languages (TypeScript frontend, Python backend, Go services, SQL migrations). Splitting heuristics need adjustment.

### Language Boundary Rule

Treat each language as a hard split boundary. A single story should not require the executor to context-switch between languages, because:

- Different linting, testing, and build tools per language
- Context window gets consumed faster when loading toolchains for multiple languages
- Errors in one language are harder to debug while thinking in another

### Splitting by Repo Structure

| Monorepo Layout | Split Strategy |
|---|---|
| `apps/web` (TS) + `apps/api` (Python) | One story per app. Wire them together in a separate integration story |
| `packages/shared` + `apps/*` | Change shared package first (its own story), then consumers |
| `services/auth` (Go) + `services/billing` (Go) | Each service is its own story even if same language, because they deploy independently |
| `migrations/` + `src/` | Migrations always get their own story. They run in a different environment |

### Dependency Order Across Languages

```
SQL migrations -> Backend service (any language) -> API layer -> Frontend -> E2E tests
```

If the backend is in Python and the frontend in TypeScript, you still follow this order. The integration story at the end verifies that the contract between languages holds (API request/response shapes match).

---

## Common Mistakes

### Mistake 1: The "God Story"

**Bad**: "Build the settings page"

This story touches the database (new preferences table), backend (CRUD endpoints), frontend (form components, validation, state), and possibly auth (permission checks). Complexity score: 8+.

**Fix**: Split into 4 stories:
- S-001: Add preferences table and migration (Small, complexity 2)
- S-002: Preferences CRUD service + API routes (Small, complexity 2)
- S-003: Settings form UI with client-side validation (Medium, complexity 3)
- S-004: Wire settings page to API, add permission check (Small, complexity 2)

### Mistake 2: The "Horizontal Slice"

**Bad**: "Create all TypeScript types for the project"

Types without implementation cannot be verified. You will discover type errors only when you write the code that uses them, leading to rework.

**Fix**: Include types in each vertical story. S-001 defines the types it needs alongside the implementation that uses them.

### Mistake 3: The "Premature Integration"

**Bad**: "Add Stripe payment flow" as a single story.

This mixes an external API integration (high risk, 2 points per dependency) with UI work and backend logic. If the Stripe sandbox is down, the entire story is blocked.

**Fix**: Split so the external dependency is isolated:
- S-001: Stripe service wrapper with mock responses and tests (isolate the risk)
- S-002: Payment backend logic using the wrapper (works with mocks)
- S-003: Payment UI (works with mock API)
- S-004: Integration test with real Stripe sandbox

### Mistake 4: The "Under-Split"

**Bad**: Splitting a 3-file, single-layer bug fix into 3 stories.

Over-splitting wastes context on loading the same context repeatedly. If a fix is cohesive (same layer, same feature, same test run verifies it), keep it together.

**Fix**: Score it first. If complexity is 1-2, it is already right-sized. Do not split below complexity 2 unless the files are in different repositories.

---

## References

See `references/sizing-guide.md` for detailed examples of well-sized vs poorly-sized stories.
