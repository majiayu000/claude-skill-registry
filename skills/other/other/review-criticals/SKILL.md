---
name: review-criticals
description: Audit every Critical section for necessity, scope, and duration — find stale or overly broad holds that block the main thread
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Two-phase audit: first inventory every Critical hold in the codebase, then evaluate each for necessity and scope. Use maximum parallelism — spawn explore agents for independent file groups.

## Why This Matters

`Critical "On"` prevents timer, hotkey, and callback interruption — it's the only synchronization primitive in AHK v2. But every Critical hold **blocks the main thread**. Keyboard hooks, timer callbacks, and WinEvent callbacks all queue up behind it. Critical sections accumulate over time as defenses against bugs, but the conditions that required them can change: a refactor moves shared state into a single producer, a Map iteration gets replaced with a snapshot copy, yet the Critical stays.

This is the mirror of `review-race-conditions`:
- `review-race-conditions`: "where should Critical exist but doesn't?" (additive)
- `review-criticals`: "where does Critical exist but shouldn't, or is wider than needed?" (subtractive)

## Phase 1 — Inventory

Find every `Critical "On"` / `Critical "Off"` pair in `src/core/` and `src/gui/` (plus `src/shared/` files they include). For each hold, document:

| Function | File:Lines | Protected Code Summary | Hold Duration | Shared State Touched |
|----------|-----------|----------------------|---------------|---------------------|
| `_WEH_WinEventProc` | `winevent_hook.ahk:196+` | Check eligibility, upsert window, update MRU | Medium (~50-200μs) | `gWS_*` store globals |

**Hold Duration estimates:**
- **Trivial** (~1-5μs): Single assignment, counter increment, flag set
- **Short** (~5-50μs): Few property accesses, simple if/else, Map Has+Set
- **Medium** (~50-500μs): Loop over small collection, multiple DllCalls, string building
- **Long** (~500μs+): Loop over unbounded collection, file I/O, large data structure rebuild

Also note any `Critical "On"` without a matching `Critical "Off"` on every exit path (early returns, continues). These are bugs regardless of whether the Critical is necessary — but that's `review-race-conditions` territory. Just flag them as cross-references.

## Phase 2 — Evaluate Each Hold

For each Critical section, answer one question: **What specific race would occur if this Critical were removed?**

This is not "is this a good idea" — it's "name the exact interleaving." What interrupt source fires, at what point in the protected code, modifying what shared state, causing what corruption?

### Classification

**Still necessary** — A concrete race exists:
- Name the interrupt source (which timer, hotkey, or callback)
- Name the interleaving point (between which two operations)
- Name the corruption (stale read, lost write, partial state, collection modified during iteration)
- Verdict: keep as-is

**Narrowable** — The Critical protects more than it needs to:
- The hold spans N lines but only M lines (M < N) contain the actual shared state access
- Work before or after the critical shared state access could be moved outside
- Computations, local variable setup, string formatting, DllCalls that read (not write) local state — these don't need interrupt protection
- Verdict: shrink the scope, move non-critical work outside

**Stale** — The condition that required this Critical no longer exists:
- The protected variable is no longer shared (only one callback type accesses it now)
- The dangerous interleaving was eliminated by a refactor (e.g., Map iteration replaced with snapshot copy that happens outside Critical)
- The function is no longer called from an interruptible context
- Verdict: remove

**Defensive but unverifiable** — Can't name a specific race, but:
- The pattern *looks* like it could race in theory
- The code has a comment explaining the Critical but the explanation references old architecture
- Similar code elsewhere uses Critical for the same pattern
- Verdict: flag for human review with honest "I cannot name the specific race" assessment

## Known Safe — Do NOT Flag

These Critical sections have been deliberately designed, tested, and documented. Do not propose removing, narrowing, or questioning them:

- **`Critical "On"` through the entire `GUI_OnInterceptorEvent` handler including GDI+ rendering** (~16ms). This was previously narrowed and reverted — releasing before render causes partial glass background, window mapping corruption, and stale projection data. See `keyboard-hooks.md` "CRITICAL: Critical Sections During Rendering (Context-Dependent)." No internal abort points — unsafe to interrupt. This is the most important Critical section in the codebase.
- **`Critical "On"` in `_INT_Alt_Down`, `_INT_Alt_Up`, `_INT_Tab_Down`, `_INT_Tab_Up`, `_INT_Tab_Decide`, `_INT_Ctrl_Down`, `_INT_Escape_Down`** — all hotkey callbacks require Critical to prevent callback-interrupting-callback corruption.
- **`Critical "On"` in `_Anim_FrameLoop`** — covers `_Anim_UpdateTweens()` → `GUI_Repaint()` → DComp sync. Phase 1 (#177) deliberately moved the long blocking wait (compositor clock / waitable swap chain) OUTSIDE Critical so the AHK message pump runs during the wait. The Critical section is only held during the render + present + commit sequence. This is the intended design.
- **`Critical "Off"` before `_GUI_ShowOverlayWithFrozen()` in `_GUI_GraceTimerFired`** — must release before the 1-2s first paint or Windows' `LowLevelHooksTimeout` (~300ms) silently removes hooks (#303). This is safe because the show path has 3 RACE FIX abort points that detect `gGUI_State != "ACTIVE"`. This is the deliberate opposite of `GUI_OnInterceptorEvent` — context-dependent rule, see `keyboard-hooks.md`.
- **Async activation event buffer** (`gGUI_EventBuffer`) — Critical around buffer push/pop is necessary by design.
- **Flight recorder `FR_Record()`** — if it uses Critical, it's protecting the ring buffer write pointer. Pre-allocated, intentional.

If you encounter these, classify as "Still necessary — known safe, documented" and move on. Spend your tokens on the holds that *aren't* on this list.

## Explore Strategy

Split by file group (run in parallel):

- **Producer callbacks** — `src/core/winevent_hook.ahk`, `komorebi_sub.ahk`, `komorebi_state.ahk`, `komorebi_lite.ahk`, `mru_lite.ahk`, `winenum_lite.ahk`
- **GUI hot path** — `src/gui/gui_state.ahk`, `gui_interceptor.ahk`, `gui_input.ahk`, `gui_data.ahk`, `gui_paint.ahk`
- **GUI support** — `src/gui/gui_overlay.ahk`, `gui_pump.ahk`, `gui_workspace.ahk`, `gui_win.ahk`, `gui_monitor.ahk`
- **Shared infrastructure** — `src/shared/window_list.ahk`, `blacklist.ahk`, `ipc_pipe.ahk`, `stats.ahk`

Use `query_timers.ps1` to cross-reference — timer callbacks are the primary interrupt source for non-hotkey Critical sections. Use `query_mutations.ps1 <globalName>` to see which functions mutate a given global — reveals whether all writers are inside Critical sections without reading full files.

## Validation

After explore agents report back, **validate every finding yourself**. Removing or narrowing a Critical section is high-risk — a wrong call creates a race condition that may only manifest under specific timing.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the protected code quoted. Show what's inside the Critical boundaries.
2. **Name the race (or admit you can't)**: For "still necessary" — state the specific interleaving. For "stale" or "narrowable" — explain why the race no longer exists or why the moved code is safe outside Critical. For "defensive but unverifiable" — be honest that you can't name the race.
3. **Check interrupt sources**: Use `query_timers.ps1` and grep for `SetTimer` / `Hotkey(` to identify what could actually interrupt this function. If nothing can interrupt it (function is only called from within an already-Critical context), the Critical may be redundant.
4. **Check callers**: A Critical section might look unnecessary in isolation but be required because callers invoke it from non-Critical contexts. Use `query_function_visibility.ps1` to check all call sites.
5. **Counter-argument**: "What timing scenario would make removing/narrowing this Critical dangerous?" — Even if you can't name one, consider: could a future change re-introduce the race? Is the Critical cheap enough that the safety margin is worth it?

## Plan Format

**Section 1 — Inventory:**

| # | Function | File:Lines | Hold Duration | Shared State | Classification |
|---|----------|-----------|---------------|-------------|----------------|
| 1 | `_WEH_WinEventProc` | `winevent_hook.ahk:196+` | Medium | `gWS_*` | Still necessary |
| 2 | `KSub_CacheFocusedHwnds` | `komorebi_state.ahk` | Long | `gKS_Cache`, `gWS_*` | Narrowable |
| 3 | `_OldHelper` | `some_file.ahk:30-35` | Trivial | `gFoo` (no longer shared) | Stale |

Total: N Critical sections. X still necessary, Y narrowable, Z stale, W unverifiable.

**Section 2 — Narrowable holds (recommended changes):**

| Function | File:Lines | Current Scope | Proposed Scope | Lines Moved Out | Est. Time Saved | Risk |
|----------|-----------|--------------|---------------|----------------|----------------|------|
| `KSub_CacheFocusedHwnds` | `komorebi_state.ahk` | 60 lines | 15 lines | JSON parse (before), log write (after) | ~100μs | Low — moved work is purely local |

**Section 3 — Stale holds (recommended removal):**

| Function | File:Lines | Why Stale | Evidence |
|----------|-----------|----------|---------|
| `_OldHelper` | `some_file.ahk:30-35` | `gFoo` is only written by this function now (confirmed via `query_global_ownership.ps1`) | No other writers, no timer/hotkey accesses this path |

**Section 4 — Defensive/unverifiable (human review needed):**

| Function | File:Lines | What It Protects | Why Unverifiable | Recommendation |
|----------|-----------|-----------------|-----------------|----------------|
| `_SomeFunc` | `file.ahk:90-95` | `gBar` increment | Only one known interrupt source, but pattern suggests historical race | Keep — trivial duration, safety margin worth it |

Order by hold duration within each section (longest first — the most blocking holds are the highest value targets for narrowing/removal).

Ignore any existing plans — create a fresh one.
