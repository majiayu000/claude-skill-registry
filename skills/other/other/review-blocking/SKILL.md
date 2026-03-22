---
name: review-blocking
description: Discover functions that block the main thread, then micro-audit each for internal optimization opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Two-phase audit: first discover which functions block the main thread using mechanical criteria, then micro-audit each function's internals for optimization opportunities. Use an agent team for the audit phase — the per-function work is embarrassingly parallel.

## How This Differs from review-latency

`review-latency` traces **paths** end-to-end (window change → store, user action → pixels) and cares about ordering, compound cost, and whether something is on the critical path. This skill opens each **function in isolation** and asks "can this be faster internally?" without caring about callers, frequency, or path position. The different framing surfaces different findings — path-tracing skips a function that's "only called once," but micro-auditing still catches the redundant array copy inside it.

## Phase 1 — Discovery

Find functions that block the main thread using these criteria. The criteria are mechanical — use grep and query tools, not judgment.

### Tier 1 — Always audit

These functions block the main thread by definition:

- **Functions containing `Critical "On"`** — they hold an interrupt lock. Every microsecond inside Critical delays pending hotkey/timer callbacks.
- **Timer callbacks** — they interrupt other work. Use `query_timers.ps1` to inventory all timer callbacks in `src/core/` and `src/gui/`.
- **Hotkey callbacks** — entry points for user input. Grep for `Hotkey(` registrations and the callback functions they reference.
- **WinEvent callbacks** — `DllCall("SetWinEventHook"` callbacks. These fire on every focus change, window create/destroy.

### Tier 2 — Audit if non-trivial

These functions have cost that scales:

- **Functions with loops over arrays/maps** — `for` loops, `Loop` blocks iterating collections. Cost scales with collection size.
- **Functions with 3+ DllCalls or ComCalls** — each DllCall/ComCall has marshaling overhead (~1-2μs). Three or more in one function means the overhead is non-trivial. Post-#177, `Shader_PreRender` has 40+ ComCalls per invocation (D3D11 state setup, compute dispatch, Draw, GPU readback) and runs N times per frame (once per active shader layer). `FX_PreRenderShaderLayers` loops over all active layers calling `Shader_PreRender` each.
- **Functions that build or copy collections** — `Array()`, `Map()`, `.Push()`, `.Clone()` inside a function body. Allocation cost.

### Tier 3 — Direct callees of Tier 1/2

For each Tier 1/2 function, identify its direct callees (depth 1 only) using `query_callchain.ps1 -Depth 1` (or `query_function_visibility.ps1`). Add those to the audit list. Do NOT recurse further — if a helper's helper is slow, the parent function's audit will surface the call cost.

### Discovery output

Produce a categorized function list:

| Function | File | Tier | Reason |
|----------|------|------|--------|
| `_WEH_WinEventProc` | `winevent_hook.ahk` | 1 | WinEvent callback + Critical |
| `GUI_Repaint` | `gui_paint.ahk` | 1 | Timer callback |
| `Blacklist_IsMatch` | `blacklist.ahk` | 3 | Called by `Blacklist_IsWindowEligible` (Tier 2) |

### Scope

Only functions in `src/core/` and `src/gui/` (plus `src/shared/` files they call into). Exclude `src/lib/` (third-party), `src/editors/` (not on main thread during Alt-Tab), `src/pump/` (separate process).

Use `query_state.ps1` to determine if a blocking function is only reachable from specific state machine branches — a function that blocks only during `IDLE` is less critical than one that blocks during `ACTIVE`.

## Phase 2 — Micro-Audit

**Use an agent team.** Split the discovery list into batches and assign each batch to a parallel agent. Each agent reads the function body (use `query_function.ps1 <funcName>`) and audits it in isolation.

### What to look for inside each function

**The rule: changes must be invisible to callers.** Same inputs → same outputs → same side effects. Only internal implementation changes.

**Redundant work:**
- Computing a value that's already available (passed as param, stored in a global, computed earlier in the function)
- Re-reading a property/field multiple times when the value can't change mid-function
- Building a string or array that's immediately discarded or only partially used

**Allocation waste:**
- Creating arrays/maps that could be pre-allocated `static` buffers reused across calls — **EXCEPT** in functions reachable during STA pump (paint path, COM callers, QPC). Reentrancy overwrites the static buffer mid-use. See `ahk-patterns.md` Hot Path Resource Rules.
- String concatenation in loops (each concat allocates a new string in AHK)
- `.Push()` in a loop when the final size is known (pre-size with `Array(n)` if AHK supports it, or use a pre-allocated buffer)

**Loop inefficiencies:**
- Hoistable work inside loop bodies (expressions that don't depend on the loop variable)
- Map/array lookups repeated per-iteration that could be cached in a local
- Redundant `HasOwnProp()` / `.Has()` checks before access when the key is guaranteed to exist

**DllCall overhead:**
- Multiple DllCalls that could be combined (e.g., separate Get/Set calls that could be one call with more params)
- Missing `"Cdecl"` on callbacks (forces slower marshaling)
- String parameters that could be pre-encoded to avoid per-call UTF-16 conversion

**Critical section duration:**
- Work inside `Critical "On"` ... `Critical "Off"` that doesn't need the interrupt lock
- Computations that could be moved before Critical or after Critical
- Note: Do NOT suggest removing Critical sections or restructuring them — that's `review-criticals` territory. Only suggest moving non-critical work outside the existing boundaries.

**Cache opportunities:**
- Pure computations (same input → same output) that are called repeatedly with the same arguments
- `static` locals for values computed once and reused across calls (DPI scaling factors, compiled regex patterns, etc.)

### What NOT to flag

- **Algorithmic changes that alter the function's contract** — changing sort order, filtering differently, returning different data
- **Moving work to a different function or restructuring call patterns** — that's `review-latency` territory
- **Removing Critical sections or changing their scope** — that's `review-criticals` territory
- **Buffer loops suitable for MCode** — that's `review-mcode` territory (but do note if you spot one, as a cross-reference)

### Micro-audit output (per function)

For each function, agents report:

| Finding | Line(s) | Current | Proposed | Est. Saving | Complexity |
|---------|---------|---------|----------|-------------|------------|
| `title` local read twice from `rec.title` | 45, 52 | Two property accesses | Cache in local `t := rec.title` | ~0.5μs | Trivial |
| String concat in 30-iteration loop | 60-65 | `s .= item.name ","` per iteration | Pre-size or use Array+Join | ~5-15μs | Low |

**Est. Saving** — be honest. If it's sub-microsecond, say so. The user wants the full picture, not a filtered one.

**Complexity** — Trivial (one-line), Low (few lines, obvious), Medium (structural change within function), High (requires new static/cache infrastructure).

## Validation

After the agent team reports, **validate every finding yourself**. Read the actual function code.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted.
2. **Confirm invisibility**: Verify the change doesn't alter the function's output or side effects. If there's any doubt, flag it.
3. **Check for existing optimization**: This codebase has been through optimization passes. The "redundant" lookup might be intentional (value can change mid-function due to callbacks). The "unnecessary" allocation might be required (buffer reuse would be unsafe due to STA pump reentrancy — COM calls dispatch arbitrary callbacks through `Critical "On"`, so static buffers in any function reachable from the paint/COM path can be overwritten mid-use).
4. **Counter-argument**: "What would make this optimization counterproductive?" — Does caching a value risk staleness? Does hoisting out of a loop change behavior when the loop body has side effects?
5. **Observed vs inferred**: Did you read the function body, or infer the issue from the function name?

## Plan Format

**Section 1 — Discovery results:**

| Function | File | Tier | Reason |
|----------|------|------|--------|
| ... | ... | ... | ... |

Total: N functions across M files.

**Section 2 — Micro-audit findings (grouped by file):**

For each file, list all findings across its functions:

### `winevent_hook.ahk`

| Function | Finding | Line(s) | Est. Saving | Complexity | Fix |
|----------|---------|---------|-------------|------------|-----|
| `_WEH_WinEventProc` | Redundant `WinGetTitle` call | 88 | ~50μs | Trivial | Cache in local |

### `gui_paint.ahk`

| Function | Finding | Line(s) | Est. Saving | Complexity | Fix |
|----------|---------|---------|-------------|------------|-----|

**Section 3 — Cross-references to other review skills:**

| Finding | Function | Relevant Skill | Note |
|---------|----------|---------------|------|
| NumGet loop over icon buffer | `_ExtractAlpha` | `review-mcode` | Candidate for native C |
| Critical section holds through file I/O | `_SaveState` | `review-race-conditions` | Scope may be too wide |

Order Section 2 by estimated total savings per file (sum of all findings in that file), highest first.

Ignore any existing plans — create a fresh one.
