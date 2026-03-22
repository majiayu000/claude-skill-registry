---
name: scan-frontend-patterns
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/frontend-patterns-reference.md with component base classes, state management, forms, API services, routing, and styling conventions.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan frontend codebase and populate `docs/project-reference/frontend-patterns-reference.md` with component base classes, state management patterns, form handling, API service patterns, routing conventions, and directory structure.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover frontend patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate code examples reference real files

**Key Rules:**

- Generic — works with any frontend framework (Angular, React, Vue, Svelte, etc.)
- Detect framework first, then scan for framework-specific patterns
- Every code example must come from actual project files with file:line references

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Frontend Patterns

## Phase 0: Read & Assess

1. Read `docs/project-reference/frontend-patterns-reference.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Detect frontend framework:

- `angular.json` / `nx.json` → Angular (check for standalone components, signals, NgRx)
- `package.json` with `react` / `next` → React (check for hooks, context, state libs)
- `package.json` with `vue` / `nuxt` → Vue (check for Composition API, Pinia)
- `package.json` with `svelte` / `sveltekit` → Svelte
- Multiple frameworks → document each separately

Use `docs/project-config.json` contextGroups/modules if available for app paths.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **3 Explore agents** in parallel:

### Agent 1: Component & Form Patterns

- Grep for component base classes (`extends.*Component`, `@Component`, `React.Component`)
- Find form handling patterns (reactive forms, form builders, validation patterns)
- Discover component lifecycle conventions (init, destroy, cleanup patterns)
- Find template/JSX conventions (structural patterns, conditional rendering)
- Look for component communication patterns (inputs/outputs, props/events, signals)

### Agent 2: State Management & API Services

- Grep for state management patterns (stores, reducers, signals, observables)
- Find API service base classes (`extends.*Service`, `HttpClient`, `fetch` wrappers)
- Discover data fetching patterns (interceptors, error handling, caching)
- Find subscription/cleanup patterns (unsubscribe, dispose, cleanup callbacks)
- Look for shared/common service patterns

### Agent 3: Routing, Directives & Directory Structure

- Grep for routing configuration (route definitions, guards, resolvers, lazy loading)
- Find custom directives/pipes/hooks (reusable behavior patterns)
- Discover module/library organization (shared modules, feature modules)
- Map the directory structure conventions (where components, services, models live)
- Find build configuration patterns (environment configs, proxy configs)

Write all findings to: `plans/reports/scan-frontend-patterns-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                    | Content                                                                |
| -------------------------- | ---------------------------------------------------------------------- |
| **Component Base Classes** | Base class hierarchy, what each base provides, when to use which       |
| **State Management**       | Store pattern, reactivity approach, data flow conventions              |
| **Forms**                  | Form creation pattern, validation approach, error display conventions  |
| **API Services**           | Service base class, HTTP call pattern, error handling, caching         |
| **Routing**                | Route definition pattern, guards, lazy loading, navigation conventions |
| **Directives & Pipes**     | Custom reusable behaviors, naming conventions, registration            |
| **Directory Structure**    | Where things live: components, services, models, shared code           |
| **Subscription Cleanup**   | How subscriptions/listeners are managed and cleaned up                 |
| **Styling Conventions**    | Component styling approach (scoped, modules, BEM, utility classes)     |

### Content Rules

- Show actual code snippets (5-15 lines) from the project with `file:line` references
- Include "DO" and "DON'T" examples where anti-patterns are clear
- Use tables for convention summaries (base classes, file locations, naming)
- Group patterns by developer task (not by framework concept)

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 5 code example file paths exist (Glob check)
3. Verify: class/function names in examples match actual definitions
4. Report: sections updated, patterns discovered, coverage gaps

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
