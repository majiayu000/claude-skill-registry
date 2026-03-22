---
name: review-test-coverage
description: Find significant gaps in AHK test coverage and propose targeted new tests
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-review production code against existing tests to find significant coverage gaps. Use maximum parallelism — spawn explore agents for independent areas.

**Scope**: AHK tests only — unit, GUI, live, lifecycle tests in `tests/`. NOT static analysis pre-gate checks, NOT query tools. This is about missing test coverage, not test quality (see `review-test-quality`) or test speed (see `review-test-speed`).

## The Bar for a New Test

A proposed test must clear ALL of these:

1. **Significant** — covers a real failure mode that could break the app or cause silent data corruption. Not "this function exists and has no test."
2. **Non-duplicative** — not already covered by an existing test or by static analysis pre-gate checks. Check existing tests AND `tests/check_*.ps1` before proposing.
3. **Effective** — actually tests production code via `#Include`, not a copy that will drift. Uses code inspection or real production functions.
4. **Automatable** — no real windows, no UI interaction, no desktop manipulation (unless `--invasive` flag). Must work in automated agentic runs with no user present.
5. **Fits the architecture** — uses `test_utils.ahk` patterns (`_Test_RunSilent`, `WaitForFlag`, cursor/icon suppression). Respects the parallel, timing-critical pipeline.

If a gap is better covered by a static analysis check (`tests/check_*.ps1`) than an AHK test, say so and skip it.

## Where to Look for Gaps

### Production modules without test coverage

Use `query_interface.ps1` on production files to see their public surface. Cross-reference against test `#Include` directives. Focus on:
- Public functions with complex logic (branching, state transitions, error handling)
- Functions that have caused bugs before (check git log for fix commits)
- Functions on the hot path (keyboard input, state machine, painting)

### Edge cases in covered modules

Even well-tested modules may miss:
- Error/failure paths (what happens when a DllCall fails, a pipe disconnects, a process doesn't exist?)
- Boundary conditions (empty lists, max values, zero-length strings)
- State machine transitions that are rare but valid (e.g., escape during async activation)

### Integration boundaries

Where two modules interact:
- Producer → WindowList store (do upserts handle all field combinations?)
- State machine → overlay (do all state transitions result in correct show/hide?)
- Config changes → runtime behavior (do config reloads actually affect behavior?)

### Regression targets

Code areas that have had recent bugs (check `git log --oneline -50` for fix commits). If a bug was fixed but no regression test was added, that's a gap worth filling.

## What NOT to Propose

- Tests for trivial getters/setters or simple property access
- Tests that require a running komorebi instance (unless gated by `--invasive` or with proper SKIP logic for missing deps)
- Tests for `src/lib/` (third-party code)
- Tests that duplicate what static analysis already catches (global declarations, function visibility, ownership)
- Tests for one-shot init code that only runs at startup and has no branching
- "Test every function" completionism — focus on functions where a bug would actually matter

## Validation

After explore agents report back, **validate every finding yourself**. Coverage gaps are easy to propose and hard to justify. Many "untested" functions are actually exercised indirectly through integration tests, or are simple enough that static analysis is sufficient.

For each proposed test:

1. **Cite the gap**: "I verified by reading `production_file.ahk` lines X–Y" — quote the untested logic. Then "I searched `tests/` for any test covering this" — confirm no existing coverage.
2. **Failure scenario**: What specific bug would this test catch? Describe a concrete failure mode, not a vague "this could break."
3. **Counter-argument**: "What would make this test unnecessary?" — Is the code simple enough that static analysis suffices? Is it exercised by a broader integration test? Is the failure mode so obvious it would be caught immediately?
4. **Observed vs inferred**: Did you confirm the gap by reading all related tests, or infer it from the absence of a test file with a matching name?

## Plan Format

Group by priority (hot-path gaps > integration gaps > edge cases):

| Production File | Function/Area | Gap Description | Failure Mode | Test Type | Fits In |
|----------------|--------------|----------------|-------------|-----------|---------|
| `gui_state.ahk` | `_HandleEscape` during async | No test for escape cancelling pending activation | Stuck overlay after escape | Unit (GUI tests) | `tests/gui_tests.ahk` |

For each proposed test, include:
- Which existing test file it belongs in (prefer extending existing files over creating new ones)
- What to `#Include` from production
- What to mock
- Key assertions

Order by impact: hot-path and state-machine gaps first, edge cases last.

Ignore any existing plans — create a fresh one.
