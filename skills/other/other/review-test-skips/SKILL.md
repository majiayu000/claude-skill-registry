---
name: review-test-skips
description: Audit all SKIP statements in the test suite for correctness
user-invocable: true
disable-model-invocation: true
---
Audit every `Log("SKIP:` statement across all `.ahk` test files in `tests/`. For each one, determine whether it is a **legitimate skip** or a **silent failure** that should be `FAIL` + `TestErrors++`.

## Classification Rules

A SKIP is **legitimate** when the test is genuinely not applicable in the current environment:
- **Optional dependency not installed**: komorebi not installed/running, komorebic.exe not found
- **Compilation not done**: compiled exe not found (smart-skip scenario)
- **Elevation required**: test needs admin and process isn't elevated
- **Environmental data insufficient**: not enough windows open, no multiwindow class found, system process not running
- **Parallel worktree collision**: mutex conflict from another test instance running concurrently (worktree-safe design)

A SKIP is a **silent failure** (should be FAIL) when test infrastructure that SHOULD be working isn't:
- Process startup failed (launcher/gui/pump didn't spawn)
- Pump not connected when setup confirmed it connected
- GUI process not found after successful launch
- Any precondition that the test's own setup was supposed to guarantee

## Key Principle

If the test **set up the condition itself** (launched the exe, connected the pump, etc.) and then can't find it — that's a FAIL, not a SKIP. If the condition is **external to the test** (komorebi installed, admin rights, enough windows on desktop) — that's a legitimate SKIP.

## Steps

1. Search all `tests/*.ahk` files for `Log("SKIP:` and `Log('SKIP:` patterns
2. For each occurrence, read the surrounding context (condition, whether `TestErrors++` follows, whether it returns early)
3. Classify each as legitimate or silent failure using the rules above
4. Report findings in a table grouped by file:

| File | Line | Condition | Verdict | Issue |
|------|------|-----------|---------|-------|
| ... | ... | ... | OK / FAIL | description if FAIL |

5. If any silent failures are found, fix them: change `SKIP` to `FAIL` and add `TestErrors++`
6. Run `.\tests\test.ps1 --live` to confirm all tests still pass after changes

Ignore any existing plans — create a fresh one.
