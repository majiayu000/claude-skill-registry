---
name: review-latency
description: Audit the two latency-critical paths for blocking work, redundant computation, and micro-optimization opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-audit both latency-critical paths for anything that adds delay — from micro-optimizations to architectural blockers. Use maximum parallelism — spawn explore agents for independent paths.

## Context

This is the highest-priority performance surface. The project's overriding goal is responsiveness — the user must never feel lag when Alt-Tabbing. Every microsecond matters on these paths because costs compound: a 50μs waste in an eligibility check runs 50× per focus event = 2.5ms. A cache miss in display list building runs every paint. Micro-optimizations are not just welcome, they're the point.

The architecture is single-process: producers, window store, and GUI all run in MainProcess. There is no IPC on the critical path — the enrichment pump (icon/process resolution) is async and off the hot path.

### Scope Boundaries

This skill covers the **control flow** around rendering — everything from keypress to "start painting" and from "painting done" to "window visible." It does NOT cover per-frame rendering internals, which have dedicated skills:

- **`/review-paint`** — D2D paint pipeline: pre-render + BeginDraw→EndDraw, 8-layer compositor, effect helpers, per-frame allocations in `gui_paint.ahk`, `gui_effects.ahk`, `gui_bgimage.ahk`, `gui_gdip.ahk`, `gui_math.ahk`
- **`/review-d3d`** — D3D11 shader host: `d2d_shader.ahk` buffer allocations, state calls, GPU readback, compute dispatch
- **`/review-shaders`** — HLSL pixel shader source: ALU, transcendentals, loop optimization in `src/shaders/*.hlsl`

**However**, the frame pacing mechanism IS in scope for this skill — the three-tier pacing in `gui_animation.ahk` (compositor clock → waitable swap chain → QPC spin-wait) directly affects input-to-photon latency. The decision of *when* to render (frame pacing) is latency-critical; *what* to render (paint internals) is not.

Similarly, DComp operations that affect overlay visibility timing are in scope: `D2D_SetClipRect`, `D2D_Commit`, DWM cloaking/uncloaking sequences. Present(0,0) is non-blocking post-Phase 1 — verify this hasn't regressed.

If you find a latency issue that lives inside the rendering pipeline (e.g., "paint takes too long because of X"), note it briefly and defer to the appropriate skill.

## The Two Hot Paths

### Path 1: Window Change → Store

An external event (focus change, window created/destroyed, komorebi workspace switch) must update the window store as fast as possible so the data is fresh when the user Alt-Tabs.

```
WinEventHook callback  ─┐
Komorebi subscription   ─┼──► Eligibility check ──► Store upsert ──► Dirty tracking
WinEnum (on-demand)     ─┘
```

Key files:
- `src/core/winevent_hook.ahk` — primary producer, fires on every focus change
- `src/core/komorebi_sub.ahk`, `komorebi_state.ahk`, `komorebi_lite.ahk` — workspace tracking with multi-layer cache
- `src/core/winenum_lite.ahk` — full window enumeration (startup, snapshot)
- `src/shared/blacklist.ahk` — `Blacklist_IsWindowEligible()` — called per-window, per-event
- `src/shared/window_list.ahk` — store internals, upsert, dirty tracking, display list
- `src/core/mru_lite.ahk` — fallback MRU (if WinEventHook fails)

Questions to ask:
- How much work does each producer callback do? Is any of it deferrable?
- Are eligibility checks doing redundant work (re-checking things that haven't changed)?
- Is the store upsert doing unnecessary copies or recomputations?
- Are caches (komorebi state cache, blacklist compiled patterns, etc.) actually effective? Any cache misses on the hot path?
- Is dirty tracking granular enough, or does a single-window change trigger broader recomputation?

### Path 2: User Action → Pixels

The user presses Alt → Tab and must see the overlay with correct data as fast as possible. Then each subsequent Tab press must update the selection and repaint instantly.

This skill focuses on the **control flow and data preparation** — from keypress through state machine to the point where rendering begins, and from rendering completion to overlay visibility. The rendering pipeline itself (D2D draw calls, effects, compositing) is covered by `/review-paint`.

```
Alt down ──► Pre-warm (refresh data early)
Tab down ──► Freeze list ──► Build display items ──► [Paint — see /review-paint] ──► Show overlay
Tab again ──► Move selection ──► [Repaint]
Alt up   ──► Activate window ──► Hide overlay
Escape   ──► Cancel ──► Hide overlay
```

Key files:
- `src/gui/gui_interceptor.ahk` — keyboard hook callbacks, event dispatch
- `src/gui/gui_state.ahk` — state machine transitions
- `src/gui/gui_input.ahk` — input handling, selection movement
- `src/gui/gui_data.ahk` — live data layer, refresh, pre-cache, display eviction
- `src/gui/gui_overlay.ahk` — show/hide mechanics (DWM cloaking, anti-flash)
- `src/shared/gui_antiflash.ahk` — DWM cloaking / alpha sequencing
- `src/gui/gui_monitor.ahk` — monitor detection, DPI
- `src/gui/gui_workspace.ahk` — workspace label building
- `src/gui/gui_pump.ahk` — enrichment pump integration

**Out of scope** (covered by dedicated skills):
- `src/gui/gui_paint.ahk` — per-frame rendering internals (`/review-paint`)
- `src/gui/gui_effects.ahk` — 8-layer compositor internals (`/review-paint`)
- `src/gui/gui_gdip.ahk` — D2D resource management (`/review-paint`)
- `src/gui/gui_math.ahk` — layout calculations (`/review-paint`)
- `src/gui/gui_bgimage.ahk` — background image layer (`/review-paint`)
- `src/gui/d2d_shader.ahk` — D3D11 interop (`/review-d3d`)
- `src/shaders/*.hlsl` — pixel shaders (`/review-shaders`)

**In scope from gui_animation.ahk** (the frame pacing / latency boundary):
- `_Anim_FrameLoop` — three-tier pacing: compositor clock wait vs waitable swap chain vs QPC spin-wait
- Frame skip logic for explicit FPS caps (different behavior per pacing tier)
- `DCompositionBoostCompositorClock` — DRR boost on show/hide
- `Anim_EnsureTimer` deferred start guard (STA pump safety — indirectly affects first-frame latency)

Questions to ask:
- What work happens between Tab press and the call to `GUI_Repaint()`? Is any of it unnecessary or reorderable?
- Is display list construction doing work that could be pre-computed during pre-warm?
- How long does overlay show take after paint completes? Is DWM cloaking/uncloaking adding delay?
- Does the state machine transition path have unnecessary intermediate states or checks?
- What happens on subsequent Tab presses — does data preparation repeat unnecessarily?
- Is window activation (Alt-up) blocking on komorebic or Win32 calls?

### Cross-Cutting: Main Thread Blocking

The keyboard hooks run on the main thread. **Anything that blocks the main thread delays hook processing.** This includes:

- Timer callbacks that do heavy work (check with `query_timers.ps1`)
- Producer callbacks that take too long inside `Critical "On"` sections
- Synchronous file I/O (config reads, stats writes, log writes)
- D2D operations outside the paint path (e.g., resource creation triggered by config change)
- Any `DllCall` that might block (synchronous Win32 calls)

This is separate from the two paths above — even if Path 1 and Path 2 are individually fast, a long-running timer callback between Alt-down and Tab-down steals time from hook processing.

## Explore Strategy

Split by hot path (run in parallel):

- **Path 1 agent**: All producers in `src/core/`, eligibility in `blacklist.ahk`, store internals in `window_list.ahk`. Focus on per-event callback cost.
- **Path 2 agent**: `gui_interceptor.ahk`, `gui_state.ahk`, `gui_input.ahk`, `gui_data.ahk`, `gui_overlay.ahk`, `src/shared/gui_antiflash.ahk`, `gui_workspace.ahk`. Focus on keypress-to-paint-call and paint-done-to-visible sequences. Do NOT audit the rendering pipeline itself.
- **Cross-cutting agent**: `query_timers.ps1` output, Critical section durations, any synchronous I/O on the main thread. Scan all `src/gui/` and `src/core/` files for blocking operations.

### Tools

- `query_timers.ps1` — inventory all timers, find heavy callbacks
- `query_state.ps1` — trace state machine transitions for the Alt-Tab flow
- `query_interface.ps1 <file>` — public API surface of hot path files
- `query_function.ps1 <func>` — extract function bodies without loading full files
- `query_callchain.ps1 <func>` — trace call depth from hot path entry points

## Assessment Format

Surface **everything** — do not auto-exclude findings based on estimated size. Micro-optimizations on high-frequency paths are the point of this review.

For each finding, provide an honest assessment:

| Finding | File:Lines | Current Cost | Frequency | Compound Cost | Complexity | Fix |
|---------|-----------|-------------|-----------|---------------|------------|-----|
| Eligibility re-checks cloaked state on every focus event | `blacklist.ahk:142` | ~30μs | 50×/focus burst | ~1.5ms | One-line cache | Cache cloaked state, invalidate on EVENT_OBJECT_CLOAKED |
| Display list rebuilds workspace labels every paint | `gui_data.ahk:88` | ~200μs | Every Tab press | ~200μs | Medium — need invalidation signal | Pre-compute during pre-warm, cache until workspace change |

**Columns explained:**
- **Current Cost**: Estimated per-invocation cost (use flight recorder / paint timing data if available, otherwise estimate from code complexity)
- **Frequency**: How often this runs in the critical path (1× per Alt-Tab? 50× per focus burst? Per-pixel? Per-window?)
- **Compound Cost**: Current Cost × Frequency — the actual user-felt impact
- **Complexity**: How hard is the fix? One-line change, medium refactor, architectural change?

**Do not filter.** A 10μs saving that runs 100× per paint (1ms compound) is worth knowing about even if the fix is complex. The user decides the tradeoff.

## Validation

After explore agents report back, **validate every finding yourself**. This codebase has extensive caching and optimization already — what looks like a miss may be handled elsewhere.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted. Trace the full execution path, not just one function.
2. **Trace the frequency**: Don't guess — trace when and how often this code actually runs. A function called once at startup is not a hot path finding.
3. **Check for existing optimization**: This codebase has been through multiple optimization passes. Before flagging something, check if there's already a cache, early-exit, or pre-computation handling it.
4. **Counter-argument**: "What would make this optimization unnecessary or counterproductive?" — Does it add complexity that makes the next optimization harder? Does it break an invariant?
5. **Observed vs inferred**: Did you trace the execution path through all branches, or infer the cost from reading one function in isolation?

## Plan Format

**Section 1 — Path 1 findings (Window Change → Store):**

| Finding | File:Lines | Current Cost | Frequency | Compound Cost | Complexity | Fix |
|---------|-----------|-------------|-----------|---------------|------------|-----|

**Section 2 — Path 2 findings (User Action → Pixels):**

| Finding | File:Lines | Current Cost | Frequency | Compound Cost | Complexity | Fix |
|---------|-----------|-------------|-----------|---------------|------------|-----|

**Section 3 — Cross-cutting (Main Thread Blocking):**

| Finding | File:Lines | Block Duration | When It Fires | Impact on Hooks | Complexity | Fix |
|---------|-----------|---------------|--------------|----------------|------------|-----|

Order within each section by compound cost (highest first). Do not omit low-compound-cost findings — list them at the bottom.

Ignore any existing plans — create a fresh one.
