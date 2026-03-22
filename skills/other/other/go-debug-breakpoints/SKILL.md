---
name: go-debug-breakpoints
description: Debug failing Go tests, panics, race reports, and flaky behavior with Delve and a breakpoint-first hypothesis loop. Use when Codex needs runtime evidence instead of more static reasoning, especially after a targeted Go test failure.
---

# Go Breakpoint Debugging

Use `scripts/debug-test.sh <package> [test-regex]` from the target repo root to launch Delve against one failing package or test. If there is only a log file, start with `scripts/triage-failure.sh <logfile>`.

## Breakpoint Strategy

1. Entry breakpoint at the failing test or top-level function.
2. Divergence breakpoint before the state starts differing from expectations.
3. Error-path breakpoint where errors are created, wrapped, or returned.
4. Concurrency breakpoint around channel operations, lock boundaries, or goroutine spawn sites when the bug smells concurrent.

## Hypothesis Loop

1. State what you expect before continuing.
2. Continue to the next breakpoint.
3. Compare actual runtime state with the expectation.
4. Update the hypothesis and repeat.

## Delve Checklist

- Inspect locals and arguments.
- Check the stack.
- Inspect goroutines when concurrency is involved.
- Validate one root-cause hypothesis at a time.

## Exit Criteria

- Root cause is backed by runtime evidence.
- The fix is minimal and safe.
- The exact failing test passes.
- The broader fast loop passes.

Use `references/delve-cheatsheet.md` for the common Delve commands and a short breakpoint planning reminder.
