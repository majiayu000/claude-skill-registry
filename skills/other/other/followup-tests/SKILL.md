---
name: followup-tests
description: Evaluate whether changes suggest new tests, modified tests, or new static analysis checks
user-invocable: true
disable-model-invocation: true
---
Review the current plan or recent changes and evaluate whether they suggest new tests, test modifications, or new static analysis checks. This covers both directions:

- **Forward-looking**: Do the planned changes need test coverage?
- **Backward-looking**: Could tests or static analysis have caught these issues earlier or prevented regressions?

## Test Suite Design Constraints

An intense amount of hard work was done to keep the test suite fast. Any proposal MUST respect these patterns:

- **Heavily parallelized** — tests run in parallel across multiple AHK processes. New tests must not introduce serialization bottlenecks or cross-test dependencies.
- **Store reuse** — live tests reuse store launches where possible to avoid startup overhead. New live tests should integrate with existing store lifecycle, not spawn redundant processes.
- **No user interaction** — the suite is designed to run with an agent and no human present. All tests suppress icons, prompts, cursor changes, and other UI artifacts. New tests must follow this pattern using `_Test_RunSilent()` and similar utilities from `test_utils.ahk`.
- **Poll, don't sleep** — use `WaitForFlag(&flag)` adaptive polling, not fixed `Sleep()` delays.
- **Worktree-safe** — scoped process kills, isolated pipes/mutexes, worktree-prefixed logs.

See `.claude/rules/testing.md` for the full test architecture and patterns.

## Static Analysis Design Constraints

If proposing a new static check, evaluate where it fits in the system:

- **Standalone vs batch** — There is a sub-batching system (`check_batch_*.ps1`) that groups many short checks together to reduce PowerShell startup overhead. Short checks also share a single file cache across sub-checks and other optimizations.
  - If the new check is **very short** (single pattern match, simple grep): it benefits from batch overhead amortization and shared file cache → propose adding it to an existing batch file.
  - If the new check is **substantial** (multi-pass, needs its own state, complex logic): standalone is appropriate → propose a new `check_*.ps1` file.
- **Parallelization vs core contention** — standalone checks run in parallel with other checks. Adding too many standalone checks increases core contention. Balance parallelization gains against the overhead of another PowerShell process.
- **Auto-discovery** — new `tests/check_*.ps1` files are auto-discovered by the pre-gate. No registration needed.

## What to Evaluate

For each issue or change in the plan:

1. **Is this testable?** Some issues (race conditions under specific timing, visual polish) are hard to test reliably. Don't propose flaky tests.
2. **Unit test, GUI test, or live test?** Match the test type to what's being tested:
   - Unit: pure logic, data transformation, state transitions
   - GUI: state machine, input handling (uses mock rendering)
   - Live: end-to-end with compiled exe (startup, IPC, activation)
3. **Static analysis check?** Could this class of bug be caught by pattern-matching the source code without running it? If yes, propose a check with the batch/standalone evaluation above.
4. **Existing test gap or new test?** Would modifying an existing test cover this, or is a new test needed?

## Output Format

| Issue from Plan | Testable? | Type | New or Modify | Proposal | Batch/Standalone |
|----------------|-----------|------|---------------|----------|-----------------|
| Stale comment references deleted function | Yes | Static check | New | Grep comments for function names, cross-reference with defined functions | Batch — single-pass grep, fits `check_batch_guards.ps1` pattern |
| Race in timer callback | Marginal | — | — | Timing-dependent, would be flaky. Better caught by `review-race-conditions` skill. | — |

Only propose tests/checks with a clear path to reliable, fast implementation. Don't propose tests that would be flaky, slow, or fight the existing architecture.
