---
name: plan
description: Senior React/TypeScript architect who creates detailed implementation plans for SpendiaBot's web/PWA surfaces. Validates feature-based architecture (components/hooks/lib/context/types) and React/TypeScript principles. Creates concise, specification-based plans (not code).
---

# /plan - Implementation Planner

Launches the **implementation-planner agent** to create a detailed implementation plan for a React/TypeScript feature before writing code.

## Usage

```bash
# Plan a new feature
/plan Add offline expense capture UI

# Plan a refactoring
/plan Refactor dashboard filters into composable hooks

# Plan with context
/plan Implement PWA sync queue per the requirements in issue #42
```

## What You Get

The planner creates a **concise, actionable plan** that includes:

### Plan Structure
- **Overview**: What we're building and why
- **Affected Files**: Files that will be created/modified
- **Feature Architecture Validation**: Layer placement and dependency direction
- **React Principles Compliance**: How the design follows React/TypeScript principles
- **Implementation Steps**: Numbered, sequential steps
- **Testing Strategy**: What needs to be tested
- **Risk Assessment**: Categorized risks (see below)
- **Open Questions**: Decisions that need clarification

### Planner's Expertise
The planner knows:
- Every file in the SpendiaBot React/PWA codebase
- Feature-based folder conventions (`components/`, `hooks/`, `lib/`, `context/`, `types/`)
- React Router, Suspense, TanStack Query, Dexie, and service worker patterns in the repo
- State management choices (context, Zustand, Redux Toolkit, React Query cache)
- PWA caching/sync flows and IndexedDB constraints
- Testing conventions (Vitest + Testing Library, Playwright smoke flows)
- Current phase from PLAN.md and linked initiatives
- Tech debt highlighted in GitHub issues/retro notes

## Output Location

Plans are saved based on context:

**When working on an issue:**
```
.md/issues/{issue-number}/plan.md
```

**When not on an issue (standalone):**
```
.md/standalone/plan-{feature-name}.md
```

Examples:
- Issue #42: `.md/issues/42/plan.md`
- Standalone feature: `.md/standalone/plan-multi-currency.md`

## Search Tools for Planning

Use targeted code search to understand impact and find patterns:

| Need | Tool | Example |
|------|------|---------|
| Understand component responsibilities | `Grep` | `Grep("<ExpenseList" src/features/**/*.tsx)` |
| Validate hook usage patterns | `ast-grep` | `ast-grep 'useExpense\w+' src/features/**/*.tsx` |
| Inspect prop/type definitions | `LSP` | Go to Definition on `ExpenseListProps` |
| Inventory files by name/glob | `Glob` | `Glob("src/features/**/index.ts")` |

**For planning, combine these tools to:**
- Map how props/data flow across the feature folders
- Identify all hook and lib consumers before proposing changes
- Confirm generated types or API clients already exist before reinventing

## How It Works

1. **Exploration**: Use `Grep` for JSX usage, `Glob` for layout of feature folders
2. **Impact Analysis**: Pair `ast-grep` with `Grep` to find every hook/lib consumer and cross-feature coupling
3. **Architecture Analysis**: Validate layer placement and dependency direction per Feature Architecture rules
3. **Risk Assessment**: Check against React/PWA risk categories below
4. **Planning**: Create sequential implementation/test steps referencing concrete files
5. **Validation**: Final pass against Feature Architecture + React Principles checklist
6. **Output**: Write the plan to the correct markdown path with metadata footer

## Feature Architecture Validation (MANDATORY)

Every plan MUST validate these points:

### Layer Placement
| Layer | Folder | Responsibilities | Never Contains |
|-------|--------|------------------|----------------|
| Component (`components/`) | Present UI, accessibility, motion, route composition | Business rules, data fetching, shared state mutations |
| Hook (`hooks/`) | Encapsulate stateful logic, orchestrate effects/data, expose simple APIs to components | JSX/DOM markup, styling, ad-hoc globals |
| Lib/Service (`lib/`) | Pure functions, API/IndexedDB/Dexie clients, formatting helpers | React imports, mutable UI state, component references |
| Context (`context/`) | Provide shared state and actions, integrate hooks into providers | Direct network calls, derived state persistence without memoization |
| Types (`types/`) | Interfaces, enums, zod schemas, generated clients | Implementation code, side effects, React imports |

### Dependency Direction
```
components → hooks → lib/services → types
        (never reverse; context providers sit between hooks and components and obey the same direction)
```

Questions to validate:
- Do components delegate all logic to hooks/context?
- Do hooks only depend on lib/services and types (never components)?
- Do lib/services stay React-agnostic and avoid importing hooks/components?
- Are shared types referenced from `types/` instead of duplicating local definitions?
- Do context providers expose stable values (memoized) so consumers avoid redundant renders?

## React Principles Compliance Checklist

Every plan MUST consider:

| Principle | Question to Ask |
|-----------|-----------------|
| **S**ingle Responsibility | Does each component/hook do exactly one thing? |
| **O**pen/Closed | Can we extend behavior via props/children/composition instead of editing internals? |
| **L**iskov Substitution | Can interchangeable components accept the same props without breaking behavior/layout? |
| **I**nterface Segregation | Are prop/type interfaces focused instead of mega-props with dozens of optional fields? |
| **D**ependency Inversion | Do components depend on hooks/context abstractions rather than concrete lib implementations? |

## Risk Categories (MANDATORY Assessment)

Every plan MUST evaluate these risk categories:

### 1. Rendering Risks
- Are we triggering unnecessary rerenders (missing `React.memo`, unstable deps)?
- Are expensive computations happening inside render without memoization?
- Is state lifted to the right component (not global when local suffices)?

### 2. Hook Rules Risks
- Any conditional/looped hook usage?
- Are `useEffect` dependencies accurate, or will stale closures surface?
- Are custom hooks hiding rule violations (hook order drift)?

### 3. State Management Risks
- Are we prop drilling vs. adding context selectively?
- Is derived state being stored instead of computed?
- Could async state updates race (multiple `setState` relying on stale snapshots)?

### 4. Data Layer Risks
- Will IndexedDB/Dexie schema changes require migrations/version bumps?
- Are queries bounded/paginated?
- Is error/quota handling (quota exceeded, storage events) defined?

### 5. Side Effect Risks
- Do effects/registers cleanup listeners, intervals, observers, and AbortControllers?
- Are fetches cancelable when components unmount or inputs change?
- Are service worker messages handled idempotently?

### 6. Type Safety Risks
- Any `any` casts/null assertions hiding runtime risk?
- Are unions narrow enough to detect impossible states?
- Are runtime guards needed around external data?

### 7. PWA/Offline Risks
- What is the service worker update strategy and cache invalidation plan?
- How do we reconcile offline data with server truth?
- Are browser storage limits handled (Safari private browsing, quota)?

### Risk Assessment Format in Plan

```markdown
## Risk Assessment

| Category | Risk Level | Notes |
|----------|------------|-------|
| Rendering | Medium | Virtualized list will rerender without memoizing filters |
| Hook Rules | Low | Custom hooks already wrap effects and pass lint rules |
| State Management | High | Current approach prop-drills 5 levels - introduce context |
| Data Layer | Medium | Dexie schema upgrade required - add migration path |
| Side Effects | Low | useEffect cleans up subscriptions |
| Type Safety | Medium | External API returns `unknown` - add zod parsing |
| PWA/Offline | High | Need cache bust + sync queue conflict policy |

### Mitigations
- Rendering: Add `useMemo` + `React.memo` around `ExpenseGrid`
- State: Create `useExpenseFiltersContext` provider consumed by grid + toolbar
- PWA: Define SW version gating + background sync conflict resolution
```

## Example Workflow

```bash
# 1. Create the plan (for issue #42)
/plan Implement offline-first sync queue per the requirements in issue #42

# Agent will:
# - Inspect src/features/expenses_sync/{components,hooks,lib}
# - Search for existing Dexie stores + service worker handlers
# - Check PLAN.md for release constraints + app shell commitments
# - Create detailed plan in .md/issues/42/plan.md

# 2. Review the plan, then execute
npm run lint
npm run build
npm test
npx vitest run src/features/expenses_sync/__tests__/queue.spec.ts
```

```bash
# Standalone plan (no issue)
/plan Add install prompt + manifest polish for SpendiaBot PWA

# Agent will create: .md/standalone/plan-install-prompt.md
```

## When to Use /plan

✅ **Good for:**
- Net-new React features (dashboard widgets, offline flows, service worker changes)
- Large refactors (rewrite to hooks, modularizing feature folders)
- Architecture shifts (introducing new state stack, virtualization, streaming SSR)
- When cross-feature impact or shared components are touched
- When multiple front-end approaches exist and tradeoffs must be explained

❌ **Skip for:**
- Copy tweaks or className updates
- Tiny bug fixes (<10 LOC) with clear diff
- Styling adjustments already specced elsewhere
- Simple data binding additions

## Markdown Metadata Footer (MANDATORY)

Every plan markdown file MUST end with a metadata footer:

```markdown
---

**Model**: <your exact model ID, e.g. claude-opus-4-6>
**Persona**: <your persona name, e.g. Prometheus>
```

## Notes

- The planner creates **specifications**, not code
- Plans are concise—typically 1-2 pages focused on sequential steps + validation
- Plans reference existing React files/hooks/context providers as concrete anchors
- Follow-up questions can refine or scope down the plan before coding
- After approval, use `/implementation-executor` to execute the React plan end-to-end
