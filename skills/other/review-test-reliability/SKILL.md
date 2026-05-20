---
name: review-test-reliability
description: Audit AHK test suite for flaky patterns — blind sleeps, instant asserts, stale signals
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit the AHK test suite for reliability anti-patterns that cause intermittent failures. Use maximum parallelism — spawn explore agents for independent test files.

**Scope**: All test code in `tests/` — unit tests, GUI tests, live tests, pump/watcher tests, test utilities. NOT static analysis checks, NOT production code. This is about test reliability, not coverage (`review-test-coverage`), quality (`review-test-quality`), or speed (`review-test-speed`).

## Anti-Pattern Catalog

### 1. Instant assert after async operation

An external operation (process kill, `schtasks` command, file write, IPC message, pipe disconnect) followed by an immediate assertion without polling for the effect to land.

**Detection**: Look for sequences where `ProcessClose`, `Run`, `FileAppend`, `DllCall("PostMessageW"...)`, `_RunWithTimeout`, or similar is followed by an assertion (`AssertEq`, `if (!...)`, `Log("FAIL:...")`) with no poll loop between them.

**Real example** (fixed in this codebase):
```ahk
; BAD — schtasks /delete returns before Task Scheduler DB updates
DeleteAdminTask(testTaskName)
if (!AdminTaskExists(testTaskName))  ; can still return true

; GOOD — poll for eventual consistency
deleteStart := A_TickCount
while ((A_TickCount - deleteStart) < 3000) {
    if (!AdminTaskExists(testTaskName))
        break
    Sleep(100)
}
```

### 2. Blind Sleep instead of polling

A `Sleep(N)` that waits for something to happen, but never checks whether it actually happened. The sleep duration is a guess — too short causes flakes under load, too long wastes time always.

**Detection**: Look for `Sleep(N)` where N > 50 that is followed by an assertion or state check. The sleep exists to "give time" for an async effect. If removing the sleep would make the assertion fail, it's a blind sleep that should be a poll.

**Exceptions** (NOT anti-patterns):
- `Sleep(20-50)` inside an existing poll loop (throttling between checks)
- Brief settles between sequential operations that don't have a checkable signal (e.g., `Sleep(50)` between two file writes to prevent coalescing)
- Intentional delays that ARE the thing being tested (e.g., testing debounce behavior)

**Real example** (fixed in this codebase):
```ahk
; BAD — 500ms blind wait, hoping GUI initializes in time
Sleep(500)
FileAppend(content, blPath)  ; file watcher may not be ready

; GOOD — poll for readiness signal, proceed immediately
while ((A_TickCount - settleStart) < 8000) {
    if (FileExist(storeLogPath)) {
        settleReady := true
        break
    }
    Sleep(100)
}
```

### 3. ProcessClose without polling for death

`ProcessClose(pid)` followed by `Sleep(N)` instead of polling `ProcessExist(pid)`. The process may not die within the sleep window, causing downstream failures (file locks, stale PIDs, port conflicts).

**Detection**: Search for `ProcessClose` followed by `Sleep` without a `ProcessExist` poll loop.

```ahk
; BAD — process may still hold file handles
ProcessClose(pid)
Sleep(200)

; GOOD — confirm process is actually gone
ProcessClose(pid)
deadStart := A_TickCount
while (ProcessExist(pid) && (A_TickCount - deadStart) < 2000)
    Sleep(50)
```

This is especially critical in cleanup helpers used by multiple tests (e.g., `_Test_KillAllAltTabby`, `_Cleanup` functions).

### 4. Unreliable polling signals

Polling for a condition that doesn't reliably indicate what the test actually needs. The signal can false-positive (stale data from prior runs) or false-negative (signal appears before the actual thing being waited for).

**Detection**: Look for polls that check:
- File existence without checking content (stale file from prior run)
- Log file content that could match stale entries (no timestamp or sequence check)
- Process count instead of specific PID (wrong process matches)

**Real example** (found in this codebase):
```ahk
; RISKY — stale store log from prior run could false-positive
if (FileExist(storeLogPath)) {
    settleReady := true

; BETTER — check for content that proves THIS run's GUI is active
if (FileExist(storeLogPath)) {
    try {
        logContent := FileRead(storeLogPath)
        if (InStr(logContent, "WEH_ProcessBatch"))
            settleReady := true
    }
}
```

### 5. Negative assertions with blind sleep

Testing that something does NOT happen by sleeping and then asserting the absence. The sleep duration is a gamble — the event might arrive after the sleep expires.

**Detection**: Pattern is `Sleep(N)` → `if (!flag)` where the test expects the flag to remain false. Common in file watcher and timer callback tests.

```ahk
; RISKY — 500ms may not be enough under system load
Sleep(500)
if (!callbackFired) {
    Log("PASS: callback correctly did not fire")
}

; BETTER — longer poll confirms absence more convincingly
noFireStart := A_TickCount
while ((A_TickCount - noFireStart) < 2000) {
    if (callbackFired)
        break
    Sleep(50)
}
if (!callbackFired) {
    Log("PASS: callback correctly did not fire (waited 2s)")
}
```

For negative assertions, err on the side of waiting LONGER (not shorter) — false-pass is worse than slow test.

## Where to Look

### Shared test utilities (`test_utils.ahk`)
Cleanup helpers and process management functions. Issues here multiply across every test that uses them.

### Live test suites (`test_live_*.ahk`)
Process launches, IPC, file watchers, subprocess management. These interact with the OS and are the most timing-sensitive.

### File watcher unit tests (`test_unit_file_watcher.ahk`)
Debounce timing, negative assertions (callback should NOT fire), filesystem event propagation.

### GUI tests (`gui_tests*.ahk`)
Timer callbacks, state machine transitions, rendering pipeline interactions. Use `query_timers.ps1` to inventory which timer callbacks tests should exercise.

### Setup/admin tests (`test_unit_setup.ahk`)
Task Scheduler operations, shortcut creation, anything involving Windows system services.

## What NOT to Flag

- `Sleep(20-50)` inside poll loops (throttling, not waiting)
- `Sleep(50)` in test setup before the test begins (filesystem settle before watcher init)
- `Sleep(N)` that IS the thing being tested (e.g., grace period behavior)
- Timeouts on poll loops (these are safety nets, not blind waits)
- Polling with generous timeouts (15s for pump connection is correct — worst-case retry window)

## Validation

After explore agents report back, **validate every finding yourself**. Reliability issues require precise analysis — a pattern that looks like a blind sleep may actually be intentional.

For each finding:

1. **Cite the code**: Quote the exact lines. Show the async operation AND the assertion/check that follows it.
2. **Explain the race**: What specific interleaving causes the flake? "Under system load, X may not complete before Y checks it."
3. **Prove it's not intentional**: Is the sleep documented as testing a specific timing behavior? Is there a comment explaining why polling isn't used?
4. **Assess blast radius**: Does this affect one test, or is it in a shared helper used by many tests?
5. **Propose the fix**: Show the polling replacement. Specify the timeout and what condition to poll for.

## Severity Classification

**P0 — Shared helpers**: Reliability issues in `test_utils.ahk` or cleanup functions that affect multiple test suites. Fix these first — one fix improves many tests.

**P1 — Live test flakes**: Blind sleeps or instant asserts in live tests that interact with external processes. These are the most likely to flake under CI load.

**P2 — Unit test timing**: Blind sleeps in unit tests (file watcher, debounce). Less likely to flake but still unreliable in principle.

**P3 — Negative assertions**: Blind sleeps proving something doesn't happen. Low flake probability (sleeping longer makes it safer) but violates the principle.

## Plan Format

**Section 1 — P0: Shared helpers**

| File | Lines | Pattern | Blast Radius | Fix |
|------|-------|---------|-------------|-----|
| `test_utils.ahk` | 204 | ProcessClose + Sleep(200) | Used by all live tests | Poll ProcessExist with 2s timeout |

**Section 2 — P1: Live test flakes**

| File | Lines | Pattern | Race Condition | Fix |
|------|-------|---------|---------------|-----|
| `test_live_foo.ahk` | 120 | Instant assert after file write | File watcher not initialized | Poll for readiness signal |

**Section 3 — P2: Unit test timing**

| File | Lines | Pattern | Fix |
|------|-------|---------|-----|
| `test_unit_foo.ahk` | 88 | Sleep(600) for debounce settle | Poll for callback count |

**Section 4 — P3: Negative assertions**

| File | Lines | Current Wait | Proposed Wait | Condition |
|------|-------|-------------|--------------|-----------|
| `test_unit_foo.ahk` | 60 | Sleep(500) | Poll 2s | callbackFired stays false |

Order by severity, then blast radius within each level.

Ignore any existing plans — create a fresh one.
