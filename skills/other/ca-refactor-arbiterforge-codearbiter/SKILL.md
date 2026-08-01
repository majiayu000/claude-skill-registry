---
name: ca-refactor
description: Restructure code with behavioral parity proven through unmodified pre-existing tests, then refactor. No behavior change.
argument-hint: "<surface and motivation>"
---

# $ca-refactor — behavior-preserving restructure

The only permitted entry to refactor work. A refactor that cannot prove parity through unmodified pre-existing tests is a feature change in disguise and routes to `$ca-feature`. Two required parts: the **surface** (exact files, functions, classes, or methods — vague surfaces like "the auth module" are rejected) and the **motivation** (why the restructure is worth doing).

## Flow

Routes to the `refactor` skill — six phases:

1. **Surface identification** — lock the exact files, symbols, and public signatures.
2. **Parity coverage proof** — demonstrate pre-existing tests already cover the named surface, with at
   least one direct test per public method.
3. **Red parity tests (conditional)** — if the refactor exposes a new test seam, route to `tdd`
   Phase 1 to write failing tests pinning the seam's contract first.
4. **Implementation** — apply the restructure mechanically within the surface table; no new behavior,
   branches, error paths, or side effects.
5. **Parity verification** — the full pre-existing suite passes with zero edits to any pre-existing
   test file.
6. **Lint / coverage gate** — lint, type-check, and coverage clear; surface coverage MUST NOT regress.

## Routes to

`refactor` (`${CLAUDE_PLUGIN_ROOT}/routines/refactor/SKILL.md`) — all six phases.

## When NOT to use

- New behavior — a new branch, error path, side effect, public method beyond a Phase 3 seam, or a
  change to what any input maps to → `$ca-feature`.
- A change motivated by "the current behavior is wrong" → `$ca-fix`.
- Questions or discussion → `$ca-btw`.
- Persisting an already-completed refactor → `$ca-commit`.

## Hard gate

No refactor proceeds without behavioral-parity coverage proof in Phase 2; if the surface is
under-covered, the skill halts and routes to `tdd` Phase 1 to backfill before resuming. A Phase 4 diff
that would classify as `feat`, or a Phase 5 verification that depends on edits to a pre-existing test,
terminates the refactor and re-routes to `$ca-feature` or `$ca-fix`.
