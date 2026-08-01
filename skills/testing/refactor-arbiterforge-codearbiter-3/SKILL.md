---
name: refactor
description: The behavior-preserving restructure gate. Routed to by /refactor for a rename, extract, inline, move, dedup, or internal-implementation swap. Six gated phases prove behavioral parity through unmodified pre-existing tests; any diff that classifies as `feat` is not a refactor and is routed to tdd. A modified pre-existing test is rejected as evidence — it is a behavior change in disguise.
---

# refactor

Restructure, do not rewrite. Externally observable behavior before equals after — proven by mechanism, not inspection. Routed to by `/refactor`.

## Pre-flight

Read these, or STOP and surface the gap — never guess a command or a threshold:

- `<project-root>/.codearbiter/CONTEXT.md` — the `stage:` frontmatter (the maturity value) and project context.
- `<project-root>/.codearbiter/tech-stack.md` — the test, coverage, lint, and type-check invocations; file layout.
- `<project-root>/.codearbiter/coding-standards.md` — style, structure, naming. Required for Phase 4.

The working tree MUST be clean over the named surface before Phase 1. A dirty surface conflates the refactor diff with unrelated edits and breaks parity verification — STOP and surface it.

## Phase 1 — Surface identification · gate: BLOCK

Enumerate the exact blast radius before any other work. Restate the planned refactor in one sentence and confirm it back to the user, then record a surface table:

- Files (repo-relative paths).
- Top-level symbols touched — function, class, and exported member names.
- Public method signatures within those symbols.
- External consumers — call sites in other modules.

Reject vague surfaces. "the auth module", "the user service", "some helpers in utils" are categories, not surfaces. A surface is acceptable only when a reader could grep the repo for the listed symbols and arrive at the same file set. The table is the parity contract for Phases 2–6.

Gate: a precise, complete surface table, user-signed-off. A vague or category-level surface does not pass — "the functions `signToken`, `verifyToken`, and `rotateKey` in `src/auth/tokens.ts`" passes; "the auth module" does not.

## Phase 2 — Behavioral parity coverage proof · gate: BLOCK

Prove pre-existing tests already exercise the named surface well enough to detect a behavior change, before any production code is touched. Locate every test that exercises a symbol in the surface table. Run the coverage command from `tech-stack.md` scoped to the surface files; record line, branch, and per-symbol coverage.

Coverage scales with the maturity value (`stage:` in `CONTEXT.md`) — the same knob as `tdd` Phase 5,
using the shared threshold table `${CLAUDE_PLUGIN_ROOT}/includes/maturity-coverage.md`.

Every public method in the surface table MUST have at least one direct test — transitive coverage through a higher-level integration test does not count. A public method with zero direct tests is uncovered for this gate.

If surface coverage is below the maturity threshold, OR any public method has zero direct tests, halt and route to the `tdd` skill Phase 1 to backfill obligations and red tests for the uncovered surface. Resume Phase 2 only after the backfill is green.

Gate: surface coverage at or above the maturity threshold AND every public method backed by a direct test. Otherwise backfill via `tdd` Phase 1 before retrying.

## Phase 3 — Red parity tests (conditional) · gate: BLOCK

Pin any new test seam the refactor exposes before implementation. A new seam is one of: a newly exported symbol that did not exist; a new public method signature on an existing class; a previously private function promoted to module-public.

If the refactor exposes no new seam, record "No new seams" and skip to Phase 4. Otherwise, for each seam write one or more tests that pin its contract. These tests MUST be red before implementation, and every pre-existing test MUST stay green. A seam test is scoped strictly to the restructure — it MUST NOT require behavior beyond what the original code already produced. A seam test that needs new behavior to pass means the work is a feature: route it to `tdd` and abort.

Gate: either "No new seams", or failing seam tests with all pre-existing tests still green. BLOCK if a proposed seam test requires new behavior, or if any pre-existing test breaks as a side effect of writing the seam tests.

## Phase 4 — Implementation · gate: BLOCK

Apply the restructure with zero behavior change, to the conventions in `coding-standards.md`. Confine every edit to the surface table. Acceptable edits: rename symbols (with consumer updates); extract or inline functions and methods; move symbols between files; replace an internal implementation with an equivalent one; collapse or split modules where the public interface is preserved.

Unacceptable inside a refactor: adding a behavior, branch, error path, or side effect; changing the value any public method returns for any pre-existing input; adding a public method beyond a Phase 3 seam; changing observable order of operations (event emission, logging, IO). Classify the resulting staged diff against `commit-gate` classification criteria — a diff that classifies as `feat` is not a refactor; halt and route to `tdd`.

Gate: the refactor confined to the surface table, with any Phase 3 seam tests now green. BLOCK if the diff classifies as `feat`, or if any edit falls outside the Phase 1 surface table without an explicit user-approved amendment.

## Phase 5 — Parity verification · gate: BLOCK

Run the full project test suite from `tech-stack.md`. Every pre-existing test from Phase 2 MUST pass with NO modification to its source — inspect the diff and confirm zero edits to any pre-existing test file. A modified pre-existing test is, by definition, evidence the surface's observable behavior changed: revert it. If it cannot pass after revert, the refactor introduced a behavior change and is routed to `tdd` as a feature or fix. Phase 3 seam tests (if any) MUST pass. Record the pass/fail tally and any modified-test detection.

Gate: full suite green with zero pre-existing tests modified. BLOCK if any pre-existing test was modified to pass, or if any test fails.

## Phase 6 — Lint and coverage · gate: BLOCK

Run lint, the type-check if the project is statically typed, and coverage, all from `tech-stack.md`. Resolve every lint and type error. Confirm surface coverage remains at or above the maturity threshold — a refactor MUST NOT reduce coverage of the surface it touched.

Gate: clean lint and type-check, zero errors, and no coverage regression on the named surface. "Mostly passes" is not passing — this is what clears the path to `commit-gate`.

## Hard rules

- MUST NOT begin Phase 2 without a precise, user-signed-off surface table.
- MUST NOT proceed past Phase 2 if surface coverage is below the maturity threshold or any public method has zero direct tests — route to `tdd` Phase 1 to backfill.
- MUST NOT introduce new behavior in Phase 4. A diff that classifies as `feat` under `commit-gate` is not a refactor.
- MUST NOT modify any pre-existing test to make it pass. A modified test is a behavior change.
- MUST NOT reduce coverage of the named surface during the refactor.
- MUST NOT extend the surface mid-flight without an explicit user-approved amendment to the Phase 1 table.
- MUST NOT inline-suppress a lint rule to clear Phase 6, and never to bypass a security-relevant rule.
- MUST NOT guess the test, coverage, lint, or type-check command — read `tech-stack.md` or STOP.
