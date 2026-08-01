---
name: tdd
description: The test-first gate. Routed to by /feature (after the spec is approved), /fix, and /refactor before any implementation code is written. Six gated phases — obligation scan, red, green, obligation verify, coverage, lint. No feature code exists before Phase 1 clears; nothing reaches commit-gate until all six are green.
---

# tdd

Test-first, or it does not ship. Routed to by `/feature` (after spec approval), `/fix`, and `/refactor`.

## Pre-flight

Read these, or STOP and surface the gap — never guess a command or a threshold:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — the `stage:` frontmatter (the maturity value) and project context.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/tech-stack.md` — test, coverage, and lint invocations; file layout; mock patterns.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/coding-standards.md` — style, structure, naming. Required for Phase 3.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/specs/<slug>.md` — the approved spec, when `/feature` produced one. It is the primary obligation source.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/security-controls.md` — only when the change touches a security boundary (auth, crypto, secrets, a trust boundary). Optional; absent on most changes.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/code-map.md` — if present, a coarse concern→path→role map to orient before writing tests and code. Absent is fine — it is read-on-demand, populated by context-creation or commit-gate heal.

## Phase 1 — Obligation scan · gate: BLOCK

An **obligation** is one verifiable claim about the change: (a) a unique ID, (b) a source citation,
(c) a status. Status moves `OPEN → MAPPED → COVERED`; an obligation Phase 4 cannot tie to a passing
test is `MISSING`. "We should test X" is not an obligation.

Derive every obligation before any code is written, and record each as `ID · source · OPEN`:

- **Spec** — one obligation per acceptance criterion in the approved spec.
- **Contract** — API and input-validation invariants, error responses, boundary conditions.
- **Security** — only when `security-controls.md` applies: the assertion that the security-relevant boundary holds.

Gate: the obligation list is complete. **Auto-pass** when every obligation maps one-to-one onto the
acceptance criteria of an already-approved spec (full-lane spec or small-lane mini-spec) — the user
approved that list once; do not re-ask. **User review is required** only for obligations derived
BEYOND the spec (Contract and Security rows): surface just those additions, not the whole list.
Under `/sprint`, spec-derived obligations auto-pass the same way and beyond-spec additions are
SMARTS-decided and logged like any other auto-decision. A partial list never passes either way.

## Phase 2 — Red · gate: BLOCK

Write one or more failing tests per obligation. Bind each test ID to its obligation ID and move that
obligation `OPEN → MAPPED`. Run the test command from `tech-stack.md`.

- Every new test MUST fail, and fail **for the right reason** — the assertion, not an import error or a typo. A new test that passes with no implementation is wrong; fix it before continuing.
- Every pre-existing test MUST stay green. One that breaks here is a conflict — stop and surface it.

Reject the standard traps: asserting on a mock instead of behavior; a test that can never fail; a
snapshot so broad it asserts nothing; coupling to an implementation detail instead of observable
behavior; asserting on the framework's behavior rather than your own.

Gate: the runner confirms new tests red (for the right reason) and existing tests green, with every
obligation `MAPPED` to a failing test. No implementation code is written until this gate clears.

## Phase 3 — Green · gate: BLOCK

Write the **minimum** implementation that satisfies the Phase 2 tests — no speculative logic, no
gold-plating — to the conventions in `coding-standards.md`. Run the full suite. A broken pre-existing
test is a regression: fix it.

Gate: full suite green, reached by satisfying the Phase 2 tests — not by weakening them. A test's
assertions MUST be unchanged between red and green; only fixtures and setup may move. A relaxed
assertion is a gate violation.

## Phase 4 — Obligation verify · gate: BLOCK

Walk the Phase 1 list item by item. Each `MAPPED` obligation moves to `COVERED` (a real passing test
that exercises the claim) or `MISSING` (no test truly covers it). For security-relevant or
contract-critical logic, dispatch the `coverage-auditor` agent
(`${CLAUDE_PLUGIN_ROOT}/agents/coverage-auditor.md`) to confirm the tests exercise the claim.

A `MISSING` obligation returns the workflow to Phase 2 — author a correct failing test, then re-run
Phase 3 — and loops until it is `COVERED`.

**Stakes:** when you block on a `MISSING` obligation, state what the untested seam leaves exposed, not
just that it is `MISSING` — one line naming the consequence: "this error path is untested; a 500 here
would reach users silently." The block is the rule; the stakes are why it is worth the friction.

Gate: every obligation `COVERED`, each backed by a passing test. Any `MISSING` blocks Phase 5.

## Phase 5 — Coverage · gate: BLOCK

Coverage scales with the maturity value (`stage:` in `CONTEXT.md`) — a rigor knob, not a promotion
gate. The threshold table is the shared `${CLAUDE_PLUGIN_ROOT}/includes/maturity-coverage.md` (the
single source of truth, also used by `refactor` Phase 2).

Run the coverage command from `tech-stack.md`. Below the maturity threshold → add tests until it is met.

**Stakes:** when coverage blocks below threshold, name the class of code left dark — the paths a later
regression could rot unnoticed — not just "below threshold." The number is the rule; the untested paths
are why it matters.

Gate: threshold met for the current maturity value.

## Phase 6 — Lint · gate: BLOCK

Run lint, and the type-check if the project is statically typed, from `tech-stack.md`. Resolve every
error.

Gate: clean lint and type-check, zero errors — this is what clears the path to `commit-gate`.
"Mostly passes" is not passing.

## Hard rules

- MUST NOT skip, suppress, or comment out a test to clear any gate.
- MUST NOT mark an obligation `COVERED` without a passing test that exercises the claim.
- MUST NOT lower a coverage threshold without a decision recorded in `CONTEXT.md`.
- MUST NOT inline-suppress a lint rule without a written reason, and never to bypass a security-relevant rule.
- MUST NOT guess the test, coverage, or lint command — read `tech-stack.md` or STOP.
- MUST, at exit, run the follow-up harvest (`${CLAUDE_PLUGIN_ROOT}/includes/harvest.md`) over any `[NEEDS-TRIAGE]` raised this run — batch-confirm promoting work to `open-tasks.md` and decisions to `open-questions.md` so nothing languishes; nothing auto-promotes interactively.
