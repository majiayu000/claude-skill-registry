---
name: create-interactive-scientific-application-spec
description: >
  Create a detailed specification for an interactive scientific application
  (simulation, mathematical model, ODE/PDE solver, computational tool) on the
  Datagrok platform. NOT for regular CRUD/data apps — use build-app for those.
  Analyzes the user's request, reads a spec template and architectural guide,
  fills in every section with full detail, and presents the result for staged
  approval. Triggers on: "write a spec for a scientific app", "create
  specification", "spec template", "plan the app before coding", or when the
  user describes a computation-heavy interactive application. The output is an
  approved spec.md file — implementation is handled by the
  implement-interactive-scientific-application-from-spec skill.
---

# Create Specification for Datagrok Scientific Application

This skill produces a complete, implementation-ready specification for an
interactive scientific application on the Datagrok platform.

**Output:** `spec.md` saved to the application directory.
**Next step:** Implementation via the `implement-interactive-scientific-application-from-spec` skill
(separate conversation).

**Base path:** `.claude/skills/create-interactive-scientific-application-spec/` (relative to repo root).
All file paths below use `{SKILL}/` as shorthand.

---

## Step 1: Understand the request

Analyze the user's request and identify:
- The scientific domain and problem being solved.
- Core computational model (formulas, equations, algorithms).
- What the user wants to see and interact with.
- Complexity level: simple (single reactive task, no workers) vs. complex
  (multiple tasks, workers, secondary pipelines).

Determine the target package:
- If the user specifies a package name — use it.
- If the current working directory is inside an existing package
  (has `package.json` with `datagrok-api` dependency) — add the
  application to that package.
- Otherwise — ask the user whether to create a new package or add
  to an existing one.

If the request is vague (e.g., "build a Lotka-Volterra app"), ask clarifying
questions before proceeding — but keep it to 2–3 focused questions, not an
interrogation.

---

## Step 2: Read reference materials

Read these files **once**, in this order:

1. **Spec template** (mandatory):
   `{SKILL}/references/spec-template.md` — read in full.

2. **Architectural guide** (mandatory):
   `{SKILL}/references/guide-for-spec.md` — read in full.
   This is a condensed version of the implementation guide, containing only
   what is needed to write a correct specification: architecture concepts,
   port/adapter/coordinator roles, naming conventions, section expectations.

3. **Completed examples** (if available):
   `{SKILL}/references/examples/` — list subdirectories, then read the
   example spec(s) that are closest to the user's request.

**Do NOT read** the full implementation guide, worker guides, API references,
or coding conventions — those belong to the implementation skill.

---

## Step 3: Fill in the specification

Fill in every section of the template. Follow these rules:

### Critical sections — fill with maximum detail

- **1.0 General Information** — application name, package, entry function,
  description.
- **1.1 Core** — task list, computation formulas (Level 1 is MANDATORY before
  approval), input/output parameters, implementation approach.
- **3. Controls** — every control must have: ID, label, type, data type,
  default value, min, max, format, tooltip. No placeholders.
- **4. Display Elements** — every viewer/element with ID, type, associated data.
- **7. Validation** — concrete rules with conditions and error messages.
- **15. Testing** — test categories, reference examples, expected coverage.

### Sections that may be N/A for simple apps

For applications with a single reactive task, no workers, and no secondary
pipelines, the following sections can be marked N/A with a one-line explanation:
- 1.2 Ports (application-level: Progress, Cancellation)
- 8.2 Secondary Pipelines
- 8.4 Computation Blocking
- 12.2 Worker Termination

Never mark a section N/A without explanation. If unsure whether a section
applies — include it.

### Computation formulas (Section 1.1) — special attention

This is the most important section. Level 1 must contain:
- All variables with meaning, units, and valid domains.
- All equations/relationships connecting inputs to outputs — unambiguously,
  so that another developer could implement from this description alone.
- Output properties (invariants): bounds, monotonicity, conservation laws,
  limiting cases.
- At least one reference example per computational path: concrete inputs →
  expected output with source (manual calculation / literature).

Level 2 (full formalization) can be marked as "to be developed incrementally"
for the first iteration, but note what it will eventually contain.

### Control IDs — naming convention

Use a consistent prefix: `ctrl_` for inputs (e.g., `ctrl_alpha`, `ctrl_x0`),
`btn_` for buttons (e.g., `btn_optimize`, `btn_reset`), `view_` for viewers
(e.g., `view_line_chart`, `view_phase_plot`).

---

## Step 4: Present for approval

Present the specification to the user in stages:

1. **First:** Sections 1.0–1.5 (architecture, computation model, ports,
   adapters, coordinator, independence principle).
   Ask for feedback before continuing — this is the foundation.
2. **Then:** Sections 2–5 (main view, controls, display, layout).
3. **Then:** Sections 6–15 (feedback, validation, pipeline, reactivity,
   data lifecycle, errors, resources, closure, UX, testing).

At each stage, ask: "Does this look correct? Anything to change?"

---

## Step 5: Save and hand off

When the user approves the full specification:

1. Save the specification as `spec.md` in the application source directory
   (e.g., `src/<app-name>/spec.md`).
2. Confirm explicitly:

   > **Specification approved and saved to `src/<app-name>/spec.md`.**
   >
   > To implement, start a new conversation and use the
   > `implement-interactive-scientific-application-from-spec` skill, or run:
   >
   > `/implement-interactive-scientific-application-from-spec`

Do NOT proceed to implementation in this conversation.

---

## Iteration rules

- If the user requests changes — update the spec and re-present the changed
  sections.
- If you discover ambiguities or inconsistencies while filling in later
  sections — go back and fix earlier sections, noting the changes.
- The specification is the single source of truth for implementation.

---

## Reference files summary

| File | Purpose | Required |
|------|---------|----------|
| `references/spec-template.md` | Section structure and expectations | Yes |
| `references/guide-for-spec.md` | Architecture concepts for correct spec writing | Yes |
| `references/examples/` | Completed spec examples | If available |

### What `guide-for-spec.md` should contain

This file is a trimmed version of the full implementation guide. **Keep:**

- Hexagonal architecture overview (Core ↔ Ports ↔ Adapters ↔ Coordinator)
- Independence principle explanation
- Task taxonomy (reactive vs. on-demand, simple vs. complex)
- Port types and their roles (Input, Output, Progress, Cancellation)
- Adapter responsibilities (what UI adapters do, what worker adapters do)
- Coordinator responsibilities (high-level, not implementation details)
- Naming conventions (control IDs, CSS prefixes, file structure)
- Section-by-section expectations for the spec template
- Computation blocking concept (what it is, when to specify it)
- Resource lifecycle concept (subscriptions, workers — what to plan for)

**Remove:**

- Code examples and implementation patterns
- Webpack configuration details
- CSS implementation rules (selectors, specificity)
- Worker message protocol and lifecycle management code
- TypeScript interface definitions
- Subscription management code (`subs[]` array patterns)
- `addValidators()` implementation
- `onViewRemoved` implementation patterns
- Testing framework setup and test runner details
- Any section that answers "how to code this" rather than "what to specify"

Target size: ~30–40% of the full guide.
