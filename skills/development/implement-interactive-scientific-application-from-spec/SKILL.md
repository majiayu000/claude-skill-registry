---
name: implement-interactive-scientific-application-from-spec
description: >
  Implement an interactive scientific Datagrok application (simulation,
  mathematical model, ODE/PDE solver, computational tool) from an approved
  specification (spec.md). NOT for regular CRUD/data apps — use build-app
  for those. Reads the spec and architecture guide, then builds the application
  following strict hexagonal architecture: model types, core computation,
  validation, workers, UI, coordinator, tests. Use this skill when a spec.md
  already exists and the user wants to implement it. Triggers on: "implement
  from spec", "implement-from-spec", "code the scientific application",
  "implement spec.md", or when the user references an existing spec.md file
  and asks to build/implement it.
---

# Implement Datagrok Scientific Application from Specification

This skill takes an approved specification (`spec.md`) and produces a
complete, working Datagrok application.

**Input:** `spec.md` — created by the `create-interactive-scientific-application-spec` skill or written manually.
**Output:** fully implemented application with tests.

**Base path:** `.claude/skills/implement-interactive-scientific-application-from-spec/` (relative to repo root).
All file paths below use `{SKILL}/` as shorthand.

---

## Step 1: Locate and read the specification

Find `spec.md`:
- If the user provides a path — use it.
- If the current directory is inside an application directory — look for
  `spec.md` there.
- Otherwise — ask the user where the spec is.

Read `spec.md` in full. Verify it contains at minimum:
- Section 1.0 (General Information) with app name and package.
- Section 1.1 (Core) with computation formulas and reference examples.
- Section 3 (Controls) with complete control definitions.
- Section 4 (Display Elements).

If the spec is incomplete or missing critical sections — tell the user
and suggest running the `create-interactive-scientific-application-spec` skill first.

---

## Step 2: Read the architecture guide and references

Read the following files. Read only what is relevant to the current
application — check the spec's complexity level to decide.

**Always read:**

| File | Purpose |
|------|---------|
| `{SKILL}/references/guide.md` | Full implementation guide |
| `{SKILL}/references/reference/datagrok-api-reference.md` | Datagrok inputs, viewers, layouts, subscriptions |
| `{SKILL}/references/reference/datagrok-coding-conventions.md` | File structure, naming, formatting, error handling |

**Read the reference example (complete working implementation):**

| File | Purpose |
|------|---------|
| `{SKILL}/references/examples/lotka-volterra-spec/lotka-volterra-spec.md` | Example spec |
| `{SKILL}/references/examples/lotka-volterra-spec/code/` | Complete implementation following this architecture |

**Read if the spec uses workers (Sections 1.2–1.3 are not N/A):**

| File | Purpose |
|------|---------|
| `{SKILL}/references/reference/WORKER-GUIDE.md` | Worker-utils infrastructure and lifecycle |

**Read if the spec uses parallel execution (e.g., grid search, sensitivity):**

| File | Purpose |
|------|---------|
| `{SKILL}/references/reference/PARALLEL-EXECUTION.md` | Distribution across worker pools |

**Read if the spec involves array-heavy computations:**

| File | Purpose |
|------|---------|
| `{SKILL}/references/reference/COMPUTATION-PATTERNS.md` | Raw data and null handling |
| `{SKILL}/references/reference/ARRAY-OPERATIONS.md` | Efficient typed array operations |

---

## Step 3: Implement in order

Follow this implementation sequence strictly:

1. **Project structure** — create files and directories per the guide.
2. **Model types** — interfaces for input/output ports (Section 1.2 of spec).
3. **Core computation** — implement each task in isolation, no UI imports
   (Section 1.1 of spec). The core must NOT import `datagrok-api` or `ui`.
4. **Validation** — implement `validate()` returning `Map<InputId, string>`
   (Section 7 of spec).
5. **Workers** (if applicable) — worker files in `src/<app-name>/workers/`
   (Section 1.3 of spec). Each worker must be added as a separate entry
   point in `webpack.config.js`:
   ```
   '<worker-name>': {filename: '<worker-name>.js', import: './src/<app-name>/workers/<worker-name>.ts'}
   ```
   Workers are loaded at runtime via
   `new Worker(_package.webRoot + 'dist/<worker-name>.js')`.
6. **UI controls** — create inputs with all options from the spec
   (Section 3 of spec).
7. **Display elements** — viewers, custom panels (Section 4 of spec).
8. **CSS** — all styles in `css/<app-name>.css` with app-specific prefix.
   No inline styles (Section 5.3 of spec).
9. **Coordinator** — connect everything: reactivity, validation triggering,
   computation, result display, resource lifecycle (Section 1.4 of spec).
10. **Tests** — implement test categories from Section 15 of spec.

---

## Step 4: Implementation rules

Follow the architecture guide strictly. Key principles:

- **Hexagonal architecture:** Core ↔ Ports ↔ Adapters ↔ Coordinator.
- **Independence principle:** UI behavior does not depend on computation.
  The core receives a ready, validated parameter set.
- **CSS isolation:** all classes use `<app-name>-` prefix. No generic names.
- **Computation blocking:** use `computationsBlocked` flag for batch updates.
- **Resource cleanup:** collect all subscriptions in `subs[]`, terminate
  workers on close, cancel pending operations.
- **Tooltips:** every control and action button must have a tooltip.
- **Validators:** add Datagrok validators to every input via `addValidators()`.
- **No artificial delays:** if examples contain a `busy wait` loop for demo
  purposes — never reproduce this pattern.
- **Domain names in core:** the core should use domain names (`alpha`, `beta`),
  not UI-prefixed identifiers (`ctrl_alpha`). The coordinator maps between
  domain names and control IDs. Similarly, `RANGES` (slider min/max) belongs
  to the UI adapter, not the core — the core should only define mathematical
  domains (e.g., `> 0`).

---

## When the spec is insufficient

If during implementation you discover that the specification is incomplete,
ambiguous, or inconsistent:

- **STOP coding.**
- Tell the user exactly what is missing or unclear.
- Propose a fix.
- Wait for approval before continuing.

Do NOT improvise or fill gaps silently.

---

## Quality checklist (before presenting the final result)

- [ ] Every computation matches the formulas in the spec exactly.
- [ ] All controls have correct defaults, ranges, formats, and tooltips.
- [ ] Validation covers all rules from the spec with correct error messages.
- [ ] CSS file exists with app-prefixed classes; no inline styles.
- [ ] All event subscriptions collected in `subs[]` array.
- [ ] All workers terminated on close.
- [ ] `onViewRemoved` handler cleans up all resources.
- [ ] Tests cover: validation (boundary + invalid), formula verification,
      output properties, numerical method (if applicable).

---

## Reference files summary

| File | Required | When |
|------|----------|------|
| `references/guide.md` | Yes | Always |
| `references/reference/datagrok-api-reference.md` | Yes | Always |
| `references/reference/datagrok-coding-conventions.md` | Yes | Always |
| `references/reference/WORKER-GUIDE.md` | Conditional | Spec uses workers |
| `references/reference/PARALLEL-EXECUTION.md` | Conditional | Spec uses parallel execution |
| `references/reference/COMPUTATION-PATTERNS.md` | Conditional | Array-heavy computations |
| `references/reference/ARRAY-OPERATIONS.md` | Conditional | Typed array operations |
| `references/examples/lotka-volterra-spec/` | Yes | Complete reference implementation with spec |
