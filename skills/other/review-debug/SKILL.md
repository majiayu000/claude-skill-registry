---
name: review-debug
description: Audit debug logging and diagnostics for ungated disk writes, missing coverage, and overhead
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Systematically audit all debug logging, tooltips, and diagnostic output across the codebase. Use maximum parallelism — spawn explore agents for independent areas.

## Two Questions to Answer

**1. Are any debug outputs ungated?** — Every `FileAppend`, `FileOpen`, `Tooltip`, or diagnostic write must be wrapped in a config check (`cfg.DiagXxx`, `cfg.DebugXxx`, etc.). With all debug config options OFF, the app should have zero disk thrashing and zero unnecessary logging overhead. The only exception is `_GUI_LogError()` which always logs (by design — see `debugging.md`).

**2. Are there important gaps?** — Are there failure paths, error conditions, or diagnostic-worthy events that have no logging at all, where a log would save significant debugging time?

## What to Look For

**Ungated outputs (problem):**
- `FileAppend` / `FileOpen` for log files without a config guard
- `Tooltip` calls outside of `cfg.DiagAltTabTooltips` guard
- `OutputDebug` calls left in production paths (acceptable in dev-only or rarely-hit error paths)
- String concatenation for log messages evaluated before the config guard (see `ahk-patterns.md` caller-side log guards rule)

**Correctly gated (not a problem):**
- `if (cfg.DiagChurnLog)` → `FileAppend ...`
- `if (cfg.DiagAltTabTooltips)` → `Tooltip ...`
- `_GUI_LogError()` — always-on by design, only for actual errors
- Flight recorder `FR_Record()` — near-zero cost by design (pre-allocated ring buffer)

**Coverage gaps (potential improvement):**
- Error/catch blocks that silently swallow failures
- IPC disconnection or reconnection with no trace
- Producer state transitions (start/fail/recover) with no log
- Config validation failures with no user-visible feedback

## Reference

See `.claude/rules/debugging.md` for the full list of diagnostic config flags and their log file paths. All diagnostic options live in the `[Diagnostics]` config section.

## Explore Strategy

Use `query_timers.ps1` to identify timer callbacks — these often contain diagnostic writes for heartbeat, stats, or producer health checks. Use `query_callchain.ps1 <logFunc> -Reverse` to trace all callers of logging functions and verify gate coverage. Use `query_function_visibility.ps1 <logFunc>` to find all call sites of diagnostic output functions.

Split into independent zones and explore in parallel:

- `src/gui/` — Overlay rendering, state machine, flight recorder
- `src/core/` — Producers (WinEventHook, Komorebi, pumps)
- `src/shared/` — IPC, config, blacklist, window list, stats
- `src/editors/` — Config/blacklist editors, WebView2
- `src/pump/` — EnrichmentPump subprocess
- Root `src/` files — Launcher, installation, update

## Validation

After explore agents report back, **validate every finding yourself**. Explore agents sometimes flag code that is actually gated by a check further up the call chain.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the actual code quoted.
2. **Trace the call chain**: Is there a config guard in a caller that gates this entire path? If so, it's not ungated.
3. **Counter-argument**: "What would make this fix unnecessary or counterproductive?" — some logging is intentionally always-on for crash diagnostics.
4. **Observed vs inferred**: State whether you saw the ungated pattern directly or inferred it from similar code.

## Plan Format

**Section 1 — Ungated outputs** (table, grouped by file):

| File | Lines | What | Guard Needed | Counter-argument |
|------|-------|------|-------------|-----------------|
| `file.ahk` | 42–45 | `FileAppend` to error log | `cfg.DiagStoreLog` | None — pure debug output |

**Section 2 — Caller-side log guard violations** (expensive string built before check):

| File | Lines | What | Fix |
|------|-------|------|-----|
| `file.ahk` | 100 | String concat before `if (cfg.DiagX)` | Move concat inside guard |

**Section 3 — Coverage gaps** (suggested additions, lower priority):

| File | Area | What's Missing | Suggested Config Flag |
|------|------|---------------|----------------------|
| `file.ahk` | IPC reconnect | Silent reconnection | `cfg.DiagIPCLog` (existing) |

Order fixes by impact: ungated disk writes first, then log guard violations, then coverage gaps.

Ignore any existing plans — create a fresh one.
