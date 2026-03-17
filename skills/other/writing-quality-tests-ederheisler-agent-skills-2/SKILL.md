---
name: writing-quality-tests
description: Use when designing or refactoring automated tests to make them high-signal, reliable, and maintainable across unit, integration, and end-to-end suites.
license: Complete terms in LICENSE.txt
metadata:
  author: eder
  version: "1.0"
---

# Writing Quality Tests

## Overview

High-signal tests prove behavior, not implementation. Favor stable interfaces, explicit oracles, and fast feedback. Default to the lowest level that proves the behavior; climb the pyramid only when integration proof is required.

**Core rule:** If a test is nondeterministic or tied to internals, it is debt. Fix it.

## When to Use

- Designing or refactoring tests for new features, bug fixes, or regressions
- Hardening flaky tests or slow suites
- Reviewing test submissions for clarity, coverage, and maintainability
- Choosing between unit, contract, integration, or end-to-end coverage for a change
- Not for manual exploratory testing or load/perf-only work; use this for automated behavioral/regression checks

## Non-Negotiables

- Deterministic: same input -> same result; no hidden time/network randomness
- Behavioral oracles: assertions map to business behavior or contracts, never incidental internals
- Minimal coupling: tests fail for product changes, not helper refactors
- Focused scope: one behavior per test; isolated fixtures; clear names
- Fast feedback: prefer fast layers; cache expensive setup; parallelize safely

## Workflow

0) Prove it fails: capture the regression input or wished-for case and watch the test fail first (or reproduce the bug) before code changes.
1) Clarify behavior: preconditions, action, postconditions, invariants. Capture regression input if fixing a bug.
2) Pick level: unit for pure logic; contract for external calls; integration for seams; E2E only to prove flows or contracts end-to-end.
3) Design oracle: assert outputs, state, events, and invariants; avoid implementation details or transient UI.
4) Shape fixtures: use builders/factories; avoid globals; randomize with seeds only when helpful and log the seed.
5) Write the test: AAA (arrange-act-assert) or GWT; table-driven for variants; property-based for algebraic invariants.
6) Validate: run focused test first, then suite. If flaky, hunt nondeterminism (time, randomness, order, network) and remove it.
7) Document intent: name states behavior; failure message points to the expected contract.

## Patterns to Prefer

- Boundary and mutation pairs: min/max/empty/null plus one mutated variation to prove invariants.
- Table-driven cases: enumerate input/output pairs to avoid duplicate tests and improve diffability.
- Property-based checks: algebraic properties (idempotence, reversibility, ordering), round-trips, monotonic counters.
- Contracts at seams: mock at boundaries you own; for third-party calls, pin to contract tests or recorded fixtures.
- Guarded goldens: only for complex structured output; require explicit review of golden updates.

## Coverage Strategy

- Coverage is opt-in: never run coverage unless explicitly requested by the user in the current session (e.g., "improve coverage on file X to Y%"). PM/teammate/CI pressure does not override this rule.
- Pyramid discipline: many unit tests, fewer integration, very few E2E. Use E2E to prove cross-service flow or UI contract.
- Change-based coverage: every test should fail without the code change and pass with it; capture the regression input/output.
- Critical paths first: auth, billing, migrations, data loss, irreversible actions. Add invariants that must never be violated.
- Data and time: cover time zones, DST, leap years, ordering, pagination, idempotency, and retry semantics.
- Observability: log seeds for randomized tests; emit diagnostics on failure (inputs, seed, environment versions).

**Example (explicit coverage request):** User: "improve coverage on file X to 80%". Run targeted coverage for that file only, add behavior-driven tests to hit missing branches, and avoid coverage runs outside that request.

```bash
pytest --cov=path/to/file.py --cov-report=term-missing
```

## Flake Prevention

- Remove time races: replace sleeps with waits on explicit conditions; freeze or inject clocks.
- Isolate state: fresh fixtures per test; unique temp dirs/ports; clean databases; no shared singletons.
- Control randomness: seed RNG, capture seed in failure output, prefer deterministic builders.
- Network and IO: stub external calls; if unavoidable, record/replay; set tight timeouts and retries with jitter disabled in tests.
- Parallel safety: ensure fixtures are parallel-safe or mark tests serial; avoid global mutable state.

## Review Checklist

- Name states behavior and level (e.g., "adds item to cart (integration)").
- Single reason to fail; assertions map to user-visible behavior or contract.
- Fixtures minimal and local; builders hide irrelevant details; no shared hidden state.
- Negative and edge cases present; regression case for the original bug captured.
- Tests run quickly; slow/expensive flows justified and focused.

## Hygiene (adaptable patterns)

- Structure: Given–When–Then or AAA so intent is obvious.
- Hypothesis: fix generators or code instead of suppressing health checks; log seeds for repro.
- Async correctness: use real async paths/fakes; don’t hide missing awaits with sync doubles.
- Assertion scope: assert behavior/contract fields; avoid brittle full-payload snapshots unless testing a contract.
- Coverage as health, not blocker: focus on low-coverage behavior-heavy files; be pragmatic with legacy or infra-heavy areas.

### Marks (for selective runs)

- unit: isolated logic with external deps mocked
- contract/integration: cross-component seams with real wiring or adapters
- async: true async paths; avoid sync fakes masking awaits
- property: Hypothesis-based invariants in dedicated property files
- slow: >1s or real infra; justify and keep focused

## Common Anti-Patterns

- Brittle UI or text snapshots without intent; prefer semantic assertions or scoped snapshots.
- Over-mocking internals; mocking within the module under test; asserting call order that is not part of the contract.
- Sleep-based waits; reliance on wall-clock time; unseeded randomness.
- Combined scenarios covering multiple behaviors in one test; global fixtures that hide setup.
- Golden files updated blindly; tests that assert logging implementation rather than outcomes.
- Running coverage by default instead of waiting for explicit coverage requests.

## Red Flags - Stop and Fix

- Tests pass or fail intermittently
- Assertions tied to private methods or call order instead of observable behavior
- Unseeded randomness, sleeps instead of explicit waits, or shared mutable fixtures
- Golden updates accepted without review of intent
- A test never failed before the code change
- Running coverage without the user explicitly asking
- Running coverage due to PM/teammate/CI pressure
