---
name: ts-testing
type: standard
depth: extended
description: >-
  Generates dense law-driven test suites for Effect modules via algebraic PBT
  using Vitest, @effect/vitest, fast-check. Enforces 175 LOC cap, 95% per-file
  coverage, mutation kill-ratio via Stryker. Use when writing/reviewing spec
  files, adding coverage, generating property tests, debugging flakes, or
  scaffolding unit/integration/E2E tests from templates.
---

# [H1][TS-TESTING]
>**Dictum:** *Algebraic property-based testing eliminates circular AI-generated tests by construction.*

<br>

Generate dense, law-driven test suites. Pure transformations tested via algebraic laws; effectful boundaries tested via properties. Density over quantity -- few powerful tests, not many trivial ones.

**Tasks:**
1. Read [index.md](./index.md) -- reference file listing.
2. Classify test category via [section 4](#4category_routing).
3. For unit PBT: read [->laws.md](./references/laws.md), [->density.md](./references/density.md).
4. For integration/E2E: read [->categories.md](./references/categories.md).
5. Author spec following workflow in [section 1](#1workflow).
6. Validate against [section 8](#8validation) and [->validation.md](./references/validation.md).

**Versions:** Vitest (inline projects), fast-check (PBT + model-based), @effect/vitest (Effect bridge), Stryker (mutation), testcontainers (integration), Playwright (E2E).

---
## [1][WORKFLOW]
>**Dictum:** *Systematic workflow ensures complete, dense, non-circular tests.*

<br>

1. **Read source module** -- Inventory exported functions, Effect dependencies (R channel), error types (E channel), schemas, branded types.
2. **Classify test category** -- Walk routing table from [section 4](#4category_routing). Most `packages/server/` modules are unit PBT. Boundary modules (database, HTTP) are integration.
3. **Select applicable laws** -- Walk matrix from [section 5](#5law_selection) per exported function. List each law with formula.
4. **Design arbitraries** -- Schema-derived (`Arbitrary.make(Schema)`) preferred over hand-rolled. Apply safety filters (proto pollution, length bounds). Use `_` prefix.
5. **Plan LOC budget** -- Allocate lines per section within 175 cap: imports 5-7, constants 8-15, layer 3-6, algebraic 80-120, edge cases 15-25.
6. **Pack properties** -- Combine 2-4 laws sharing same arbitrary shape into single `it.effect.prop`. Use `Effect.all` for independent checks within one body.
7. **Select density technique** -- Walk table from [section 6](#6density_selection). Choose highest-multiplier technique that fits.
8. **Author spec from template** -- Pick `unit-pbt` or `integration` template from `templates/`.
9. **Verify oracle independence** -- Walk guardrails checklist from [->guardrails.md](./references/guardrails.md). Expected values come from laws, external refs, or standards -- never from re-deriving source logic.
10. **Verify coverage** -- Predict branch coverage from properties. Add `[EDGE_CASES]` section if <95% predicted. Run `pnpm exec nx test -- --coverage` to confirm.

---
## [2][HARD_CONSTRAINTS]
>**Dictum:** *Numeric thresholds are non-negotiable.*

<br>

[CRITICAL]:
- [ALWAYS] **175 LOC flat cap** per spec file. No exceptions.
- [ALWAYS] **95% per-file coverage** (V8 provider, statements + branches + functions). Each file measured independently.
- [ALWAYS] **Mutation thresholds**: break=50 (build fails), low=60 (investigate), high=80 (target).
- [ALWAYS] **One spec per source module per category**. No splitting, no combining.
- [ALWAYS] **Density over quantity** -- pack laws into properties, aggregate with Effect.all, leverage generation.

| [INDEX] | [METRIC]        | [VALUE] | [NOTE]                               |
| :-----: | --------------- | :-----: | ------------------------------------ |
|   [1]   | Max file LOC    |   175   | Flat cap, enforced by PostToolUse    |
|   [2]   | Coverage target |   95%   | Per-file V8 (statements+branches+fn) |
|   [3]   | Mutation break  |   50    | Build fails below this               |
|   [4]   | Mutation low    |   60    | Investigation trigger                |
|   [5]   | Mutation high   |   80    | Target -- contract-driven tests      |

---
## [3][FILE_STRUCTURE]
>**Dictum:** *Canonical section order enables rapid navigation.*

<br>

**Import Order** (enforced by hook):
1. `@effect/vitest` -- `it`, `layer`
2. `@parametric-portal/*` -- source module under test
3. `effect` -- `Effect`, `FastCheck as fc`, `Schema as S`, `Array as A`
4. `vitest` -- `expect`
5. External oracles (e.g., `node:crypto`) -- after vitest

**Section Order** (omit unused, separators padded to column 80):

```
// --- [CONSTANTS] -------------------------------------------------------------
// --- [LAYER] -----------------------------------------------------------------
// --- [ALGEBRAIC] -------------------------------------------------------------
// --- [EDGE_CASES] ------------------------------------------------------------
```

**Constants Convention:**

| [INDEX] | [PREFIX]   | [PURPOSE]              | [EXAMPLE]                               |
| :-----: | ---------- | ---------------------- | --------------------------------------- |
|   [1]   | `_`        | Fast-check arbitraries | `_json`, `_text`, `_nonempty`           |
|   [2]   | `_`        | Schema-derived arbs    | `_item = Arbitrary.make(ItemSchema)`    |
|   [3]   | `UPPER`    | Static constants       | `CIPHER`, `RFC6902_OPS`, `NIST_VECTORS` |
|   [4]   | `as const` | All static constants   | `{ iv: 12, tag: 16 } as const`          |

**File Comment:** `/** [Module] tests: [brief description]. */`

**Topology:** See [section 4](#4category_routing) for file locations per category.

---
## [4][CATEGORY_ROUTING]
>**Dictum:** *Category selection determines environment, tools, and patterns.*

<br>

**Categories:** Unit PBT (`tests/packages/`), Integration (`tests/integration/`), System (`tests/system/`), E2E (`tests/e2e/`).

**Quick route:** Most `packages/server/` modules are Unit PBT. Boundary modules (database, HTTP, Redis) are Integration. Cross-service orchestration is System. User-facing flows are E2E (Playwright agent pipeline -- do not manually author).

[REFERENCE] Full routing matrix, Vitest inline projects, and patterns per category: [->categories.md](./references/categories.md).

---
## [5][LAW_SELECTION]
>**Dictum:** *Laws define WHAT to test; density techniques define HOW.*

<br>

Walk the law taxonomy per exported function. Select all applicable laws. Pack laws sharing the same arbitrary shape into a single `it.effect.prop`.

**Core laws:** Identity, Inverse, Idempotent, Commutative, Associative, Homomorphism, Annihilation, Monotonicity.
**Equivalence relations:** Reflexive, Symmetric, Transitive.
**Structural properties:** Immutability, Determinism, Non-determinism, Length formula, Preservation.
**Domain invariants:** Security (proto pollution, tenant isolation, tampering), Boundary limits, Known-answer vectors.

[REFERENCE] Full law taxonomy, selection procedure, and code patterns: [->laws.md](./references/laws.md).

---
## [6][DENSITY_SELECTION]
>**Dictum:** *Parametric generation multiplies coverage per LOC.*

<br>

**Top techniques:** `it.effect.prop` PBT (50-200x), property packing (2-4x), `Effect.all` aggregation (Nx1), statistical batching, symmetric iteration, model-based commands.

**Decision heuristic:** Start at highest multiplier. Drop to lower-multiplier techniques only when property shape or cost prevents a higher one.

[CRITICAL] **Block syntax rule:** `it.effect.prop` callbacks must return `void | Effect<void>`. Use `{ expect(...); }` not bare `expect(...)`. Expression-form returns an Assertion object, causing false failures.

[REFERENCE] Full technique catalog, decision rules, and code patterns: [->density.md](./references/density.md).

---
## [7][THESIS]
>**Dictum:** *Three pillars eliminate circular AI-generated tests.*

<br>

- **Algebraic PBT as External Oracle** -- Laws (identity, inverse, homomorphism) are domain-independent mathematical truths. AI cannot fabricate a law that "happens to pass" -- law correctness is provable independent of implementation.
- **Parametric Generation Multiplies Coverage** -- Single `it.effect.prop` invocation generates 50-200 cases per run, replacing hundreds of hand-written assertions with single universally-quantified property.
- **Mutation Testing Detects Circular Tests** -- Stryker injects code mutants (operator swaps, conditional negations, statement deletions). Circular tests re-deriving expected values from source code fail to kill mutants.

**Seven-Layer Defense:**

| [INDEX] | [LAYER]              | [MECHANISM]                         | [STATUS] |
| :-----: | -------------------- | ----------------------------------- | -------- |
|   [1]   | Algebraic PBT        | Laws are external oracles by nature | Active   |
|   [2]   | Model-Based Testing  | fc.commands() stateful verification | Active   |
|   [3]   | Differential Testing | Cross-validation vs reference impls | Active   |
|   [4]   | Mutation Testing     | Stryker kill-ratio enforcement      | Active   |
|   [5]   | External Oracles     | NIST FIPS 180-4, RFC 4231, RFC 6902 | Active   |
|   [6]   | PostToolUse Hook     | 13-rule awk validator               | Active   |
|   [7]   | Human Review         | Final gate for spec correctness     | Always   |

---
## [8][VALIDATION]
>**Dictum:** *Gates prevent non-compliant output.*

<br>

[VERIFY]:
- [ ] Thresholds met (section 2 above)
- [ ] File structure matches (section 3 above)
- [ ] No forbidden patterns (13 hook rules)
- [ ] Properties return `void | Effect<void>` (block syntax)
- [ ] Oracle independence verified -- no re-derivation of source logic

[REFERENCE] Detailed checklists, error symptoms, and commands: [->validation.md](./references/validation.md). Hook rules and anti-patterns: [->guardrails.md](./references/guardrails.md).
