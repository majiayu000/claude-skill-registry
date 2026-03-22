---
name: review-dead-code
description: Find and plan removal of dead code (unused functions, variables, unreachable paths)
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Systematically audit the codebase for dead code and write a removal plan.

This project has changed significantly over time. Find code that is no longer serving a purpose: unused functions, unread variables, unreachable branches, orphaned helpers. Use maximum parallelism — spawn explore agents for independent areas of the codebase.

## What Counts as Dead Code

- Functions defined but never called (check ALL callers, including indirect via timer callbacks, hotkeys, and `SetTimer`)
- Global variables declared and written but never read by any consumer
- Local variables assigned but never used after assignment
- Unreachable code after unconditional `return`, `throw`, or `ExitApp`
- Stale parameters that are always passed the same constant or never inspected by the function body
- Orphaned `#Include` files whose exports are entirely unused

## What Does NOT Count

- Functions in `src/lib/` (third-party code — excluded from analysis)
- Public API functions in utility files that have zero callers today but form a coherent interface (e.g., a Map helper with Get/Set/Delete where only Get/Set are used)
- Intentional TODO scaffolding or commented explanations of *why* code was removed
- Test mocks and stubs — they exist to shadow production code
- Config registry entries — even if no code reads them yet, they define the schema

## Methodology

Use the query tools to validate findings — do NOT rely on grep alone:

- `query_function_visibility.ps1 <funcName>` — authoritative caller list (public/private, all call sites)
- `query_global_ownership.ps1 <globalName>` — who declares, writes, and reads a global
- `query_interface.ps1 <filename>` — public surface of a file (spot unused exports)
- `query_visibility.ps1` — lists public functions with 0 or 1 external callers (direct dead code signal)
- `query_includes.ps1` — include tree for finding orphaned `#Include` files whose exports are entirely unused

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the actual code. Vague references without quoting code are not sufficient.
2. **Trace downstream**: "How is this data used downstream?" — for variables and data structures, trace the access pattern, not just creation.
3. **Counter-argument**: "What would make removal counterproductive?" — note if the code is defensive, if removal would break a contract, or if it's wired up indirectly (timers, hotkeys, DllCall callbacks).
4. **Observed vs inferred**: State whether you saw the dead pattern directly or inferred it from similar code elsewhere.

## Explore Strategy

Split the codebase into independent zones and explore in parallel:

- `src/gui/` — GUI rendering, state machine, overlay
- `src/core/` — Producers (WinEventHook, Komorebi, pumps)
- `src/shared/` — Window list, config, IPC, blacklist, theme
- `src/editors/` — Config/blacklist editors
- `src/pump/` — EnrichmentPump subprocess
- Root `src/` files — Entry points, launcher, installation, update

After explore agents report back, **validate every finding yourself** before including it in the plan. Explore agents sometimes identify issues that are handled elsewhere in a larger context. Read the cited lines, trace the usage, and confirm it's genuinely dead.

## Plan Format

Group findings by file. For each item:

| File | Lines | What | Evidence | Counter-argument |
|------|-------|------|----------|-----------------|
| `file.ahk` | 42–58 | `_UnusedHelper()` — 0 callers | `query_function_visibility.ps1` shows no call sites | None — private function, safe to remove |

Then list the removals as action items. Order by risk (safest first). Note any removals that should be tested together because they're interdependent.

Ignore any existing plans — create a fresh one.
