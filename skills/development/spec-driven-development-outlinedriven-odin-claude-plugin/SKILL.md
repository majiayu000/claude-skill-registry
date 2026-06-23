---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
---

# Spec-driven development

Write a structured specification before writing any code. The spec is the shared source of truth between you and the engineer who asked for the work: it fixes what is being built, why, and how completion will be judged. Code written without a spec is a guess.

## When to apply

- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- An architectural decision is about to be made
- The task would take more than 30 minutes to implement

## When NOT to apply

Single-line fixes, typo corrections, or changes whose requirements are unambiguous and self-contained.

## The gated workflow

Four phases. Do not advance to the next phase until the current one is validated by the human.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### Phase 1: Specify

Start from a high-level vision. Ask clarifying questions until the requirements are concrete.

**Surface assumptions first.** Before writing any spec content, list what you are assuming and force a correction:

```
ASSUMPTIONS I'M MAKING:
1. Runtime target is a long-running service (not a CLI or batch job)
2. Auth uses signed session cookies (not bearer tokens)
3. Persistence is a relational store, inferred from the existing schema
4. Only current language/runtime versions are supported (no legacy targets)
→ Correct me now or I proceed with these.
```

Do not silently fill in ambiguous requirements. The spec exists to surface misunderstandings before code is written; an unstated assumption is the most dangerous form of misunderstanding.

**Write a spec covering six core areas:**

1. **Objective** — what is being built and why, who the user is, what success looks like.

2. **Commands** — full executable commands with flags, not bare tool names. Record them for the stack the project actually uses:
   ```
   # Node / npm
   Build: npm run build
   Test:  npm test -- --coverage
   Lint:  npm run lint --fix
   Dev:   npm run dev

   # Rust / cargo
   Build: cargo build --release
   Test:  cargo test
   Lint:  cargo clippy -- -D warnings
   Run:   cargo run
   ```

3. **Project structure** — where source lives, where tests go, where docs belong. The layout is stack-specific; capture the one that applies:
   ```
   # TypeScript service
   src/      application source
   src/lib/  shared utilities
   tests/    unit + integration tests
   e2e/      end-to-end tests
   docs/     documentation

   # Python package
   src/pkg/       package source
   tests/         unit + integration tests
   docs/          documentation
   pyproject.toml build + dependency config
   ```

4. **Code style** — one real snippet of the project's style beats paragraphs describing it. Include naming conventions, formatting rules, and an example of accepted output in the project's language.

5. **Testing strategy** — which framework, where tests live, coverage expectations, and which test level covers which concern.

6. **Boundaries** — three tiers:
   - **Always:** run tests before commits, follow naming conventions, validate inputs
   - **Ask first:** schema changes, adding dependencies, changing CI config
   - **Never:** commit secrets, edit vendored directories, delete failing tests without approval

**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What is being built and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How completion is judged — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

**Reframe instructions as success criteria.** Translate vague requirements into measurable conditions, whatever the domain:

```
REQUIREMENT: "Make the dashboard faster"
REFRAMED:
- LCP < 2.5s on a 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)

REQUIREMENT: "The batch job is too slow"
REFRAMED:
- Processes 1M records in < 90s on the reference host
- Peak resident memory < 512 MB
- Exits non-zero on any partial failure
→ Are these the right targets?
```

Concrete targets let you loop, retry, and solve toward a defined goal instead of guessing what "faster" means.

### Phase 2: Plan

From the validated spec, produce a technical implementation plan:

1. Identify the major components and their dependencies
2. Determine implementation order (what must exist first)
3. Note risks and mitigation strategies
4. Separate work that can run in parallel from work that must be sequential
5. Define verification checkpoints between phases

The plan must be reviewable: the human reads it and either approves the approach or names the part to change.

### Phase 3: Tasks

Break the plan into discrete, implementable tasks:

- Each task is completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, or manual check)
- Tasks are ordered by dependency, not by perceived importance
- No task changes more than ~5 files

**Task template:**
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```

### Phase 4: Implement

Execute tasks one at a time, test-first: turn each task's acceptance criteria into a failing test, then write the code that makes it pass. At each step, load only the spec sections and source files the current task needs; do not flood the working context with the entire spec. Verify each task against its acceptance criteria before starting the next.

## Keeping the spec alive

The spec is a living document, not a one-time artifact:

- **Update when decisions change** — if the data model has to change, update the spec first, then implement.
- **Update when scope changes** — features added or cut are reflected in the spec.
- **Commit the spec** — it belongs in version control alongside the code.
- **Reference the spec in PRs** — link each PR back to the spec section it implements.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. A two-line spec is fine. |
| "I'll write the spec after I code it" | That is documentation, not specification. The spec's value is forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. Fifteen minutes of waterfall beats fifteen hours of debugging. |
| "Requirements will change anyway" | That is why the spec is a living document. An outdated spec still beats no spec. |
| "The user knows what they want" | Even clear requests carry implicit assumptions. The spec surfaces them. |

## Red flags

- Writing code with no written requirements
- Asking "should I just start building?" before defining what "done" means
- Implementing features absent from any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"

## Verification

Before proceeding to implementation, confirm:

- [ ] The spec covers all six core areas
- [ ] The human has reviewed and approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The spec is saved to a file in the repository
