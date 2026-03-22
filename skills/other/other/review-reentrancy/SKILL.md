---
name: review-reentrancy
description: Audit the paint and frame loop paths for STA message pump reentrancy — COM calls that can dispatch timer/hotkey callbacks mid-execution
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit every COM/DWM/Win32 call in the paint and frame loop paths for STA message pump reentrancy hazards. This is the highest-consequence review — reentrancy bugs cause impossible symptoms (partial renders, frozen paints, corrupted state) that are extremely difficult to diagnose after the fact.

## The Mechanism

AHK v2 runs on a single-threaded apartment (STA) COM thread. When AHK makes a blocking or semi-blocking COM call (D2D BeginDraw, EndDraw, DXGI Present, DWM SetWindowPos, etc.), the COM runtime pumps the Windows message loop while waiting. This message pumping dispatches AHK timer callbacks and keyboard hook handlers **even when `Critical "On"` is active** — because COM's STA message pump operates at the Win32 level, below AHK's Critical mechanism.

This means:

```
Critical "On"
  gFlag := true
  ComCall(BeginDraw, ...)      ; <-- STA pump happens HERE
                                ;     Timer callback fires
                                ;     Callback reads gFlag (true, partially set state)
                                ;     Callback modifies gOtherState
                                ;     Callback returns
  ; Outer code resumes, gOtherState silently changed
  gFlag := false
Critical "Off"
```

`Critical "On"` prevents AHK-level thread interruption (timers preempting normal execution). It does NOT prevent COM STA message pumping from dispatching those same callbacks during a blocking COM call. This is the fundamental trap — developers assume Critical provides mutual exclusion, but COM calls inside Critical create reentrancy windows.

### Affected Call Types

Any COM method call (`ComCall`, vtable dispatch) on D2D, DXGI, DWM, or DComp interfaces is a potential STA pump point. The highest-risk calls are those that synchronize with the GPU or compositor:

**Known heavy pump points** (block waiting for GPU/compositor, pump aggressively):
- `IDXGISurface::Map` / `Unmap` (GPU readback stall)
- `IDXGISwapChain::Present` (VSync wait — non-blocking with waitable swap chain, but still a COM call)
- `ID2D1RenderTarget::BeginDraw` / `EndDraw` (D2D batch flush)
- `ID2D1Bitmap1::CopyFromMemory` (pixel transfer)
- `DwmSetWindowAttribute` / `SetWindowPos` / `ShowWindow` (DWM compositor sync)
- `CreateBitmapFromDxgiSurface` (D2D/DXGI interop)

**Known lightweight pump points** (usually return immediately, but still COM calls):
- `IDCompositionVisual::SetClip`, `SetTransform`, `SetOpacity`
- `IDCompositionDevice::Commit`
- `ID3D11DeviceContext` state setup (PSSetShader, VSSetShader, IASetPrimitiveTopology, etc.)
- `ID3D11DeviceContext::Draw`, `Dispatch` (GPU command submission, non-blocking)
- `IDCompositionScaleTransform::SetScaleX/Y`, `IDCompositionTranslateTransform::SetOffsetX/Y`

Even lightweight calls are technically pump points. The risk is proportional to how long the call blocks — but a "lightweight" call that takes 1ms on a loaded GPU is still pumping.

### What Reentrancy Breaks

1. **Partial state visibility**: Code between two assignments gets interrupted — the callback sees half-updated state
2. **Guard bypass**: A reentrancy guard (`if (gPainting) return`) is set, COM call pumps, a timer callback tries to paint, sees the guard, returns — but the guard is never cleared if the outer paint throws (need try/finally)
3. **Nested frame loops**: `Anim_EnsureTimer` starts the frame loop. If called from within a paint's STA pump, the frame loop starts inside the paint — the paint quasi-thread is suspended forever because the frame loop never yields back to it
4. **Collection mutation during iteration**: A timer callback modifies a Map/Array that the outer paint is iterating
5. **Double resource use**: Outer code acquires a D2D render target, STA pump fires a callback that also tries to acquire it

## The Five Invariants

These are the defenses against STA reentrancy. Each addresses a specific failure mode. The audit verifies all five hold for every COM call site in the paint and frame loop paths.

### Invariant 1: try/finally on reentrancy guards

**What it protects**: Reentrancy guard (`gPaint_RepaintInProgress`) is always cleared, even if a COM call throws or a callback causes an early exit.

**How to verify**: Every function that sets a reentrancy guard before making COM calls must use `try/finally`:
```ahk
gPaint_RepaintInProgress := true
try {
    ; ... COM calls that may pump STA ...
} finally {
    gPaint_RepaintInProgress := false
}
```

**Failure mode if violated**: Guard gets stuck `true` after an error — all future paint attempts are blocked permanently.

### Invariant 2: Deferred timer start (Anim_EnsureTimer)

**What it protects**: The frame loop (`_Anim_FrameLoop`) never launches from inside a paint's STA pump.

**How to verify**: `Anim_EnsureTimer()` checks `gPaint_RepaintInProgress`. If true, it sets a deferred flag instead of starting the timer immediately. The timer is started after the paint completes.

**Failure mode if violated**: Frame loop starts inside paint → frame loop calls paint → paint is already in progress → the original paint quasi-thread is suspended by the STA pump forever. The overlay freezes.

### Invariant 3: Critical "On" scope covers entire paint

**What it protects**: No AHK-level timer/hotkey interruption between data preparation and render completion. (Note: COM STA pumping can still reenter — this invariant works in concert with the others.)

**How to verify**: `Critical "On"` is set before any data read and not released until after `EndDraw`. No `Critical "Off"` between data snapshot and render completion.

**Failure mode if violated**: A timer callback modifies `gGUI_DisplayItems` or `gGUI_LiveItems` between the data snapshot and the D2D draw calls — corrupted render (wrong items, stale positions, partial list).

### Invariant 4: Paint-before-tween ordering

**What it protects**: The first visible frame is fully rendered before animation tweens begin. The user never sees a stale or blank frame as the first frame of an overlay show.

**How to verify**: The show sequence is: set opacity to 0 → paint first frame → start entrance tweens (opacity 0→1). The paint happens before any tween modifies visual state.

**Failure mode if violated**: Tweens start before paint completes → first frame shows at partial opacity with stale/blank content → visible flash.

### Invariant 5: ForceCompleteHide at FREEZE boundary

**What it protects**: Clean state transition when the state machine leaves ACTIVE. No stale overlay, no lingering animation state, no transform residue.

**How to verify**: `Anim_ForceCompleteHide()` completes all active tweens, clears transforms, resets opacity, and hides the overlay before any new show sequence begins.

**Failure mode if violated**: Stale animation state leaks into the next overlay appearance — wrong scale, wrong opacity, wrong position. Or the overlay stays visible when it should be hidden.

### Invariant 6: No shared mutable buffers across STA pump points

**What it protects**: Static buffers, static locals, and global state used by a function are not corrupted by a reentrant call to the same (or a related) function during an STA pump.

**How to verify**: For any function reachable from the paint/frame loop path that uses `static` buffers or writes to globals, check: if a COM call within (or after) the buffer write pumps STA and re-enters this function, does the reentrant call overwrite the buffer before the outer call reads it? Key patterns:
- `static buf := Buffer(N)` → `NumPut(...)` → `ComCall(...)` → `NumGet(buf, ...)` — UNSAFE if the ComCall can pump STA and re-enter
- `static buf := Buffer(N)` → `NumPut(...)` → `NumGet(...)` into locals → `ComCall(...)` — SAFE (buffer consumed before pump point)
- `QPC()` using a static buffer instead of a local `"int64*", &c := 0` — UNSAFE (called from everywhere)

Also check `Float()` wrappers on `NumPut("float", ...)` for D2D/D3D buffers — these ensure IEEE 754 bit patterns and are not redundant.

**Failure mode if violated**: GPU receives wrong geometry, timestamps, or viewport data. Symptoms are cyclic (corrupt on hitch frames, recover between hitches) because the reentrancy is intermittent. Extremely difficult to diagnose — presents as shader artifacts, not code bugs.

## Audit Procedure

### Step 1 — Enumerate all COM call sites in the paint and frame loop paths

Scan these files for `ComCall(`, `ComObj`, vtable dispatch patterns, and `DllCall` to DWM/D2D/DXGI/DComp APIs:

**Primary (per-frame hot path):**
- `src/gui/gui_paint.ahk` — `GUI_Repaint`, `_GUI_PaintOverlay`
- `src/gui/gui_effects.ahk` — all `FX_PreRender*` and `FX_Draw*` functions
- `src/gui/d2d_shader.ahk` — `Shader_PreRender` (40+ ComCalls per invocation, runs up to 7x/frame)
- `src/gui/gui_overlay.ahk` — `D2D_AcquireBackBuffer`, `D2D_ReleaseBackBuffer`, `D2D_Present`, `D2D_SetClipRect`, `D2D_Commit`
- `src/gui/gui_animation.ahk` — `_Anim_FrameLoop` (frame pacing + tween sync + DComp operations)
- `src/gui/gui_gdip.ahk` — D2D resource calls (CreateBrush, DrawText, DrawImage, etc.)

**Secondary (show/hide transitions):**
- `src/shared/gui_antiflash.ahk` — DWM cloaking, SetWindowPos, ShowWindow
- `src/gui/gui_state.ahk` — state transitions that trigger show/hide
- `src/gui/gui_overlay.ahk` — `D2D_HandleDeviceLoss` (full pipeline recreation)

For each COM call site, record:

| Call | File:Line | Context | Inside Critical? | Inside try/finally? | Can start timer? | Pump Risk |
|------|-----------|---------|-----------------|--------------------|-----------------|-----------|
| `BeginDraw` | `gui_paint.ahk:182` | Paint body | Yes | Yes (gPaint_RepaintInProgress) | No | High |

### Step 2 — Verify the five invariants

For each COM call site from Step 1:

1. **Is it inside a try/finally reentrancy guard?** If it's in the paint path, `gPaint_RepaintInProgress` must be set with try/finally around it. If it's in the frame loop, check for equivalent guards.

2. **Can it transitively trigger `Anim_EnsureTimer`?** Trace the STA pump scenario: if a timer callback fires during this COM call, could any code path reach `Anim_EnsureTimer`? If yes, verify the deferred-start guard checks `gPaint_RepaintInProgress`.

3. **Is Critical "On" active?** All paint-path COM calls should be inside Critical. Frame loop COM calls should be inside the frame loop's Critical section.

4. **Does it affect the show sequence?** If this COM call is in the show path (first paint, overlay reveal), verify paint completes before tweens start.

5. **Is ForceCompleteHide aware of this state?** If this COM call sets visual state (transforms, opacity, DComp properties), verify `Anim_ForceCompleteHide` clears it.

6. **Are any static buffers live across this COM call?** Check: does the enclosing function (or its callers) have `static` Buffer/variable state that was written before this COM call and read after it? If yes, a reentrant call during the STA pump corrupts that state. Also check functions this COM call reaches transitively — utility functions with `static` buffers (like QPC, monitor info helpers) are especially dangerous.

### Step 3 — Identify new/changed COM call sites since last audit

Use `git log --all -p --diff-filter=AM -- src/gui/ src/gui/d2d_shader.ahk` and search for new `ComCall` additions. Any new COM call in the paint or frame loop path needs all 5 invariants verified. Pay special attention to:

- New DComp calls (transforms, opacity, Commit) — added for animation effects
- New D3D11 calls — added for compute shaders, new shader layers
- New D2D calls — added for selection/hover effects
- Any COM call added to a function that didn't previously make COM calls (new STA pump point in a previously-safe function)

## Explore Strategy

Split by path (run in parallel):

- **Paint path agent**: `gui_paint.ahk`, `gui_effects.ahk`, `gui_gdip.ahk` — enumerate every COM call in the paint body. For each, verify invariants 1-3. Check: is any COM call outside the try/finally guard? Is any COM call between data snapshot and render completion where a callback could corrupt state?

- **Shader pipeline agent**: `d2d_shader.ahk` — `Shader_PreRender` is the densest COM call site (40+ calls). It runs BEFORE `BeginDraw` (in the pre-render phase). Verify: is it inside the reentrancy guard? Could a callback during GPU readback (`Map`) modify shader state that the outer pre-render loop is iterating? Check the compute dispatch path separately — CS dispatch + UAV unbind + SRV rebind is a multi-step sequence where reentrancy between steps could corrupt D3D11 pipeline state.

- **Frame loop / transition agent**: `gui_animation.ahk`, `gui_overlay.ahk`, `gui_antiflash.ahk`, `gui_state.ahk` — enumerate COM calls in the frame loop (Present, DComp Commit, transform setters). Verify invariants 2, 4, 5. Check: could `Anim_EnsureTimer` be reached via STA pump during any of these calls? Is the show sequence ordered correctly (paint before tweens)? Does ForceCompleteHide clear all visual state set by these calls?

### Tools

- `query_function.ps1 <func>` — extract function bodies to inspect COM calls in context
- `query_callchain.ps1 <func>` — trace what a function calls (find transitive COM call sites)
- `query_callchain.ps1 <func> -Reverse` — find callers (verify a COM call is only reached from protected contexts)
- `query_global_ownership.ps1 gPaint_RepaintInProgress` — verify the reentrancy guard is set/cleared correctly
- `query_timers.ps1` — identify all timer callbacks that could fire during STA pump
- `query_state.ps1` — extract state machine branches to identify which state transitions could trigger COM calls or be interrupted by STA pump reentrancy

## Assessment Format

For each COM call site:

| Call | File:Line | Inv.1 (guard) | Inv.2 (timer) | Inv.3 (Crit) | Inv.4 (order) | Inv.5 (reset) | Inv.6 (buffers) | Status |
|------|-----------|--------------|--------------|-------------|-------------|-------------|----------------|--------|
| `BeginDraw` | `gui_paint.ahk:182` | Yes | N/A | Yes | N/A | N/A | Check | Safe |
| `SetOpacity` | `gui_animation.ahk:295` | No guard | N/A | Yes | Verify | Must clear | N/A | **AUDIT** |

**Status values:**
- **Safe** — All applicable invariants verified
- **AUDIT** — One or more invariants not verified or potentially violated
- **VIOLATION** — Invariant definitively broken — this is a bug

### Sections

**Section 1 — COM Call Inventory:**

Full table of every COM call in the paint and frame loop paths, with invariant status.

**Section 2 — Violations (if any):**

| Call | File:Line | Invariant Broken | Failure Scenario | Fix |
|------|-----------|-----------------|-----------------|-----|

Describe the specific reentrancy scenario: which callback fires, what state is corrupted, what the user sees.

**Section 3 — Near-Misses:**

COM calls that are currently safe but fragile — e.g., a function that makes COM calls and is currently only called from inside the reentrancy guard, but has no guard of its own (safe today, breaks if someone calls it from a new context).

**Section 4 — New COM Calls Since Last Audit:**

If using `git log` to diff, list all new COM call sites and their invariant status. This is the highest-value section for incremental audits after feature work.

## Validation

After agents report:

1. **Trace the actual reentrancy path**: For any AUDIT or VIOLATION finding, construct the specific scenario: "Timer X fires during COM call Y, callback Z runs, modifies state W, which outer code assumes is stable." If you can't construct the scenario, downgrade to near-miss.

2. **Verify guard coverage**: Read the actual try/finally blocks. A guard that's set 10 lines before the COM call but the try block starts 5 lines before the COM call means 5 lines of COM calls are OUTSIDE the guard.

3. **Check callback reachability**: Use `query_timers.ps1` to list all active timer callbacks. For each AUDIT finding, check: could this specific callback actually fire during this specific COM call? If the timer is disabled during paint (e.g., stopped before paint starts), the reentrancy window doesn't exist.

4. **Cross-reference with review-criticals**: If a Critical section was flagged as "narrowable" by review-criticals, check whether narrowing it would expose a COM call to unprotected reentrancy.

Ignore any existing plans — create a fresh one.
