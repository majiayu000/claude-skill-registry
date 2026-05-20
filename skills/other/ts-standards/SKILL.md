---
name: ts-standards
type: standard
depth: extended
description: >-
  Enforces TypeScript/Effect standards with snippet-first guidance: algebraic data types,
  exhaustive pattern matching, schema-derived types, hard-minimal export surface,
  and auto-integrated internal functionality. Use when writing, refactoring, or reviewing TypeScript code.
---

# [H1][TS-STANDARDS]
>**Dictum:** *Consolidation-first, polymorphic TypeScript. Effect orchestrates; domain computes.*

<br>

Write dense, integrated modules with minimal public APIs. Prefer capability facades, command algebras, and auto-registration over helper proliferation and manual wiring.

**Tasks:**
1. Read [index.md](./index.md).
2. Read [references/snippets.md](references/snippets.md) first.
3. Read domain references as needed: [consolidation.md](references/consolidation.md), [composition.md](references/composition.md), [adts-and-matching.md](references/adts-and-matching.md), [errors-and-services.md](references/errors-and-services.md), [repo-conventions.md](references/repo-conventions.md).
4. Implement by reusing canonical snippet IDs (`SNIP-*`) instead of inventing new patterns.
5. Run validator: `bash ./.claude/skills/ts-standards/scripts/validate-ts-standards.sh --mode check`.
6. Validate against [VERIFY] checklist.

**Versions:** TypeScript 6.0-dev, Effect 3.19+, React 19, Vite 7.

---
## [1][WORKFLOW]
>**Dictum:** *Snippet-first workflow prevents style drift and file bloat.*

<br>

1. Select target behavior and public surface.
2. Route to snippet IDs from [references/snippets.md](references/snippets.md).
3. Compose in this order: command algebra -> service surface -> layer integration -> boundary mapping.
4. Keep internal symbols internal; integrate via registry/layer composition.
5. Run policy validator and fix violations before final output.

---
## [2][CORE_POLICY]
>**Dictum:** *Few powerful interfaces beat many narrow functions.*

<br>

- **Hard-minimal public APIs** -- stable capability entrypoints only.
- **Auto-integration by default** -- new internal logic becomes active via registration, not extra exports.
- **Polymorphism over proliferation** -- one command/config function replaces clusters of near-duplicate methods.
- **Exhaustive branching** -- closed variants require `Match.exhaustive`.
- **Schema-derived types only** -- no parallel manual types.

---
## [3][NON_NEGOTIABLES]
>**Dictum:** *Compiler-visible constraints remove ambiguity.*

<br>

[IMPORTANT]:
- [ALWAYS] Prefix private/internal symbols with `_`.
- [ALWAYS] Gather public exports in final `[EXPORT]` section.
- [ALWAYS] Use `Effect.Service` for services and `Effect.fn('Service.method')` for methods.
- [ALWAYS] Reuse snippet IDs for shared patterns before authoring new variants.
- [ALWAYS] Keep each file in this skill directory at `<=275` LOC.

[CRITICAL]:
- [NEVER] `any`, `let`, `var`, `for`, `while`, `try/catch`, default exports (except config files).
- [NEVER] `if (...)` statements in TypeScript policy scope.
- [NEVER] `Effect.if(...)`.
- [NEVER] Helper/utility file sprawl (`helpers.ts`, `utils.ts`, thin wrappers).
- [NEVER] Export `_`-prefixed symbols.
- [NEVER] Widen package export surface without explicit policy update.

---
## [4][PUBLIC_SURFACE_POLICY]
>**Dictum:** *Packages expose capabilities, not internals.*

<br>

**Server allowed exports:**
- `./api`
- `./runtime`
- `./errors`
- `./testing`

**Database allowed exports:**
- `./runtime`
- `./models`
- `./migrator`
- `./testing`

Everything else is internal-by-default and consumed via internal composition.

---
## [5][SNIPPET_ROUTING]
>**Dictum:** *Use canonical snippets as stable building blocks.*

<br>

| [INDEX] | [PROBLEM]                           | [SNIPPET] |
| :-----: | ----------------------------------- | --------- |
|   [1]   | Too many sibling methods            | `SNIP-01` |
|   [2]   | Manual handler wiring               | `SNIP-02` |
|   [3]   | Wide service object                | `SNIP-03` |
|   [4]   | Weak generic polymorphism           | `SNIP-04` |
|   [5]   | Error union leaks at boundaries     | `SNIP-05` |
|   [6]   | Hook/check validator architecture   | `SNIP-06` |

[REFERENCE] Canonical code snippets: [references/snippets.md](references/snippets.md)

---
## [6][VALIDATION]
>**Dictum:** *Automated gates enforce consistency at scale.*

<br>

[FILE_LAYOUT]: Types -> Schema -> Constants -> Errors -> Services -> Functions -> Layers -> Export.

[VERIFY]:
- [ ] No forbidden syntax (`any`, `let/var`, loops, `try/catch`, default exports, inline export style violations).
- [ ] No `if (...)` and no `Effect.if(...)`.
- [ ] No exported `_`-prefixed symbols.
- [ ] Public export map complies with hard-minimal policy.
- [ ] Deep imports from server/database follow approved allowlist.
- [ ] All files under `/.claude/skills/ts-standards/` are `<=275` LOC.
- [ ] Snippet-first reuse applied before adding custom variants.

**Commands:**
- `bash ./.claude/skills/ts-standards/scripts/validate-ts-standards.sh --mode check`
- `pnpm run check:ts-standards`

[REFERENCE] Script: [scripts/validate-ts-standards.sh](scripts/validate-ts-standards.sh)
