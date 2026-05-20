---
name: tdd-cycle
description: >-
  Red-green-domain TDD cycle with strict phase boundaries and domain review
  checkpoints. Activate when writing tests, implementing features, or doing
  test-driven development. Teaches one-test-at-a-time discipline with
  mandatory domain modeling review after each phase.
license: CC0-1.0
compatibility: Requires git and a test runner (jest, pytest, cargo test, go test, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [test-files, domain-types, source-files]
  phase: build
  standalone: true
---

# TDD Cycle

**Value:** Feedback -- short cycles with verifiable outcomes keep AI-generated
code honest. Each phase produces evidence (test output, compiler output) that
confirms progress or exposes drift.

## Purpose

Teaches the red-green-domain cycle: write one failing test, review it for
domain integrity, implement minimally, review the implementation. This
four-step rhythm prevents primitive obsession, over-engineering, and
untested complexity from accumulating. Works with any language and test
framework.

## Practices

### Detect the Test Runner

!`if [ -f Cargo.toml ]; then echo "Language: Rust | Test runner: cargo test"; elif [ -f package.json ]; then if grep -q vitest package.json 2>/dev/null; then echo "Language: TypeScript/JavaScript | Test runner: npx vitest"; elif grep -q jest package.json 2>/dev/null; then echo "Language: TypeScript/JavaScript | Test runner: npx jest"; else echo "Language: TypeScript/JavaScript | Test runner: npm test"; fi; elif [ -f pyproject.toml ] || [ -f setup.py ]; then echo "Language: Python | Test runner: pytest"; elif [ -f go.mod ]; then echo "Language: Go | Test runner: go test ./..."; elif [ -f mix.exs ]; then echo "Language: Elixir | Test runner: mix test"; else echo "Language: unknown | Test runner: unknown (configure manually)"; fi`

Use the detected test runner for all "run the test" steps below.

### Start from the Outside In

The TDD cycle begins at the outermost testable layer of the application.
Before writing unit tests, write a BDD-style acceptance test that describes
how the application as a whole should behave for a given scenario. If the
project uses event modeling (see the `event-modeling` skill), GWT scenarios
become these outermost tests directly.

1. Write an acceptance test for the next scenario. Use the test framework's
   mechanism for pending or ignored tests so it does not block the suite:
   ```
   #[ignore = "acceptance: place order with valid cart"]
   ```
   ```python
   @pytest.mark.skip(reason="acceptance: place order with valid cart")
   ```
   ```typescript
   it.skip("places an order with a valid cart", () => { ... });
   ```
2. Run the suite to confirm it is recognized and skipped.
3. Drill down: identify the first unit of behavior the acceptance test
   needs. Write a unit test for that unit and enter the four-step cycle
   below.
4. After the unit tests pass, remove the pending/ignore marker from the
   acceptance test. Run it.
5. If the acceptance test passes, the scenario is complete. If it fails,
   identify the next missing unit and repeat from step 3.

This outside-in rhythm ensures every unit test exists because an acceptance
test demanded it. No speculative unit tests, no untested integration gaps.
The outer loop provides the feedback that keeps the inner loop honest.

### The Four-Step Cycle

Every feature is built by repeating: RED, DOMAIN, GREEN, DOMAIN.

1. **RED** -- Write one failing test with one assertion. Only edit test files.
   Run the test. Paste the failure output. Stop.
2. **DOMAIN (after red)** -- Review the test for primitive obsession and
   invalid-state risks. Create type definitions with stub bodies
   (`unimplemented!()`, `todo!()`, `raise NotImplementedError`). Do not
   implement logic. Stop.
3. **GREEN** -- Write the minimal code to make the test pass. Only edit
   production files. Run the test. Paste the passing output. Stop.
4. **DOMAIN (after green)** -- Review the implementation for domain
   violations: anemic models, leaked validation, primitive obsession that
   slipped through. If violations found, raise a concern and propose a
   revision. If clean, the cycle is complete.

After step 4, commit the working state. Then either start the next test or
tidy the code (structural changes only, separate commit).

### Phase Boundaries

Each phase edits only its own file types. This prevents drift.

| Phase | Can Edit | Cannot Edit |
|-------|----------|-------------|
| RED | Test files (`*_test.*`, `*.test.*`, `tests/`, `spec/`) | Production code, type definitions |
| DOMAIN | Type definitions (structs, enums, interfaces, traits) | Test logic, implementation bodies |
| GREEN | Implementation bodies, filling stubs | Test files, type signatures |

If blocked by a boundary, stop and return to the orchestrator. Never
circumvent boundaries.

### One Test, One Assertion

Write one test at a time. Each test has one assertion. If you need multiple
verifications, write multiple tests. Shared setup belongs in helper functions.

### Minimal Implementation

In GREEN, write only enough code to make the failing test pass. Do not add
error handling, flexibility, or features not demanded by the test. Future
tests will drive future features.

### Domain Review Has Veto Power

The domain review can reject a test or implementation that violates domain
modeling principles. When a concern is raised:

1. The concern is stated with the specific violation and a proposed alternative.
2. The affected phase responds substantively.
3. If consensus is not reached after two rounds, escalate to the human.

Do not dismiss domain concerns. Do not silently accept bad designs.

### Evidence, Not Assumptions

Always run the test. Always paste the output. "I expect it to fail" is not
evidence. "I know it will pass" is not evidence. Run the test. Paste the
output.

### Refactor as Exhale

After a green-domain cycle completes, tidy the code if warranted. Commit
the working state first, then make structural improvements in a separate
commit. Never mix behavioral and structural changes.

### Drill-Down Testing

If a test fails with an unclear error, mark it ignored with a reason, write
a more focused test, and work back up once the lower-level tests pass.

```
#[ignore = "working on: test_balance_calculation"]
```

## Enforcement Note

This skill provides advisory guidance. It instructs the agent on correct
phase boundaries and cycle discipline but cannot mechanically prevent
violations. On harnesses with plugin support (Claude Code hooks, OpenCode
event hooks), enforcement plugins add file-type restrictions and mandatory
domain review gates. On other harnesses, the agent follows these practices
by convention. If you observe the agent editing production code during RED
or skipping domain review, point it out. For available enforcement
plugins, see the [Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing a cycle, verify:

- [ ] RED: Wrote exactly one test with one assertion
- [ ] RED: Ran the test and pasted the failure output
- [ ] DOMAIN (after red): Reviewed test for primitive obsession
- [ ] DOMAIN (after red): Created types with stub bodies, no implementation logic
- [ ] GREEN: Implemented minimal code, nothing beyond what the test demands
- [ ] GREEN: Ran the test and pasted the passing output
- [ ] DOMAIN (after green): Reviewed implementation for domain violations
- [ ] Committed working state before starting next test or refactoring

If any criterion is not met, revisit the relevant phase before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Teaches the principles domain review checks for
  (parse-don't-validate, semantic types, invalid states). Install this to
  strengthen domain review quality.
- **debugging-protocol:** Use when a test fails unexpectedly and the cause
  is not obvious from the error output.
- **architecture-decisions:** Consult ADRs before writing tests that touch
  architectural boundaries.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
