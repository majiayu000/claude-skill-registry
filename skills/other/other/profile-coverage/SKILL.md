---
name: profile-coverage
description: Review profiler instrumentation coverage and recommend new instrumentation points
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Review which functions are instrumented for profiling and identify gaps. This is a review/discussion step — do not implement instrumentation changes without approval.

## Background

Alt-Tabby has a build-time strip profiler (`src/shared/profiler.ahk`). Functions are instrumented with `Profiler.Enter("FuncName") ; @profile` / `Profiler.Leave() ; @profile` pairs. In release builds, `tools/compile.ps1` strips all `; @profile` lines — true zero cost. In `--profile` builds, the profiler records QPC-timestamped events to a ring buffer and exports speedscope flame graphs.

The static analysis check validates balanced Enter/Leave per function (sub-check `profile_markers` in `tests/check_batch_directives.ps1`) — catches the early-return problem.

## Step 1 — Generate the instrumentation map

Run:
```
powershell -File tools/query_instrumentation.ps1 -Save
```

This writes `temp/INSTRUMENTATION_MAP.md` with every function in `src/gui/`, `src/core/`, `src/shared/` and whether it's currently instrumented.

Read it and summarize: how many functions total, how many instrumented, coverage %.

## Step 2 — Classify uninstrumented functions

For every uninstrumented function, research it and classify:

- **YES** — Recommend instrumenting. In hot path or can block/delay it.
- **MAYBE** — Useful for specific investigations but not essential.
- **NO** — Trivial, one-shot, or never delays user interaction.

Use `query_function.ps1 <name>` to read function bodies. Use `query_interface.ps1 <filename>` to see a file's public API.

### What counts as "hot path relevant"

The hot path is: Alt down → Tab → show overlay → paint → Alt up → activate window. But "hot path relevant" is BROADER than "directly in the hot path." It includes:

1. **Directly in the path**: interceptor callbacks, state machine, paint, activation
2. **Can BLOCK the path**: Any function that holds `Critical "On"` and runs on a timer or Windows callback. If it's executing when the user presses Alt, the Critical section blocks the hotkey callback until it finishes.
3. **Can DELAY the path**: Functions that produce data the hot path consumes. If they're slow, the hot path waits on stale/missing data or cache misses.

A function running on a 5-second background timer that holds Critical for 50ms IS hot-path-relevant because there's a 1% chance per Alt-Tab that it's mid-execution.

### Parent/child discrimination

Before classifying any MAYBE, check: **is its parent already instrumented? Are its children?**

**When the parent IS instrumented:**
- Child is always <1ms → **NO.** Parent captures the aggregate.
- Child is variable and you can't tell which child is slow → **YES.** Need per-child spans.

**When the children ARE instrumented:**
- Parent is just a dispatcher with <10μs own work → **NO.** Children already show the time.
- Parent is called at high frequency (100+/sec) → **NO, strongly.** Buffer pollution.

**When siblings ARE instrumented but there's a gap:**
- Unexplained time between instrumented phases → **YES.** Subtraction-based inference is exactly what profilers eliminate.

**When instrumenting a proposed-YES parent:**
- Contains a variable-cost sub-call (COM, subprocess, DllCall that can block) → instrument BOTH. Parent gives total, child gives breakdown.

### Known instrumentation gap: D3D11 / compositor pipeline

Post-#177, the rendering pipeline has extensive uninstrumented hot paths. The profiler currently covers `GUI_Repaint` (total paint time) but not the breakdown within:

- **Shader pre-render** (`Shader_PreRender` in `d2d_shader.ahk`): 40+ COM calls per shader per frame (cbuffer map, compute dispatch, D3D11 state setup, Draw, GPU→CPU readback). Runs N times per frame (once per active shader layer + mouse + selection + hover). Zero instrumentation currently.
- **Effect compositing** (`FX_DrawShaderLayers`, `FX_DrawMouseEffect`, `FX_DrawSelectionEffect`, `FX_DrawHoverEffect` in `gui_effects.ahk`): DrawImage calls for intermediate texture compositing. Only mouse effect has QPC measurement (for adaptive FPS skip).
- **DComp operations** (`D2D_SetClipRect`, `D2D_Commit` in `gui_overlay.ahk`): Clip update + commit on resize. No timing.
- **Frame pacing** (`_Anim_FrameLoop` in `gui_animation.ahk`): Compositor clock wait / waitable signal / spin-wait. Frame delta computed (`gAnim_FrameDt`) but not profiler-instrumented.

When classifying functions, pay special attention to these areas — they represent the majority of per-frame GPU-side cost but are invisible to the profiler.

### What does NOT need instrumentation

- Property accessors, flag checks, arithmetic (<1μs)
- One-shot init/teardown (startup, shutdown, config reload)
- Per-element inner loops (instrument the parent loop instead — avoids buffer flooding)
- Recursive sort internals (instrument top-level call, not inner recursion)
- Dispatcher/wrapper functions whose children are already instrumented
- High-frequency callbacks (100+/sec) where own work is <10μs
- User-initiated deliberate actions (blacklist add, config save) — not latency-sensitive

## Step 3 — Summary table

Produce a summary of all YES recommendations:

| File | Function | Why (one line) |
|------|----------|----------------|
| `gui_paint.ahk` | `_GUI_PaintOverlay` | Variable cost per-item, parent `GUI_Repaint` can't show which item is slow |

And a count: "X new functions recommended, bringing total from Y to Z (N% coverage)."

## Step 4 — Report and discuss

Present the summary table and ask if the user wants to discuss any items before implementation. Do NOT implement instrumentation changes in this skill — it is review only.
