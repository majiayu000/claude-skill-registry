---
name: review-resource-leaks
description: Audit for memory leaks, handle leaks, GDI leaks, and CPU churn
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Systematically audit the codebase for resource leaks and unnecessary CPU churn. Use maximum parallelism — spawn explore agents for independent areas.

## Resource Categories

### 1. GDI+ object leaks

GDI+ objects (brushes, pens, fonts, bitmaps, graphics) that are created but never deleted. Each leaked object consumes a GDI handle — Windows limits these per-process (~10,000). Over time, leaks cause rendering failures or crashes.

**Known safe pattern**: `D2D_GetCachedBrush` and `gD2D_Res` cache objects intentionally — these are NOT leaks. The rendering pipeline uses D2D now — look for D2D resource create/release patterns and any remaining GDI+ usage in `src/lib/`.

Look for:
- Create without matching delete in the same scope or cleanup path
- Creates inside loops or per-paint callbacks (should use `static` cached objects per `ahk-patterns.md`)
- Error/early-return paths that skip cleanup

### 2. Win32 handle leaks

Handles from `DllCall` that require explicit cleanup:
- `CreateFile` / `CloseHandle` — named pipe handles, file handles
- `OpenProcess` / `CloseHandle` — process handles for icon/info extraction
- `DllCall("SetWinEventHook")` / `DllCall("UnhookWinEvent")` — event hooks
- `LoadImage` / `DestroyIcon` — icon handles (HICON)
- `CreateCompatibleDC` / `DeleteDC` — device contexts

Look for handles stored in variables that go out of scope without cleanup, and error paths that skip `CloseHandle`.

### 3. File handle leaks

`FileOpen()` calls where the file object is never closed, or where an error path skips `.Close()`. Also check for `FileAppend` in tight loops (each call opens+closes — not a leak, but a performance concern that could be replaced with a single `FileOpen` + `.Write()`).

### 4. Named pipe leaks

The IPC system uses named pipes (`ipc_pipe.ahk`). Check that:
- Server pipe handles are closed when clients disconnect
- Client pipes are closed on process exit or reconnect
- Pipe handles in error paths are cleaned up

### 5. Timer leaks

`SetTimer` calls without corresponding `SetTimer(callback, 0)` to disable. A timer that fires after its context is gone can cause errors or unnecessary CPU work. Also check for one-shot timers (`SetTimer(cb, -period)`) that should be negative but aren't.

### 6. CPU churn

Unnecessary polling or computation when idle:
- Timers that fire frequently but do no useful work most of the time (should be adaptive or event-driven)
- Polling loops that should be event-driven
- Redundant recomputation in paint callbacks (should be cached and invalidated)
- String concatenation for logging evaluated when logging is disabled (see `ahk-patterns.md` caller-side log guards)

### 7. Unbounded growth

Data structures that grow over time without pruning:
- Maps/Arrays that accumulate entries for windows that no longer exist
- Caches without eviction (icon cache, process name cache)
- Log buffers or event buffers without size limits

## Known Safe Patterns (Do NOT Flag)

- `gD2D_Res` brush/font cache — intentional lifetime cache, cleaned up on exit
- `static` buffers in hot-path functions — intentional reuse per `ahk-patterns.md`
- Flight recorder ring buffer — pre-allocated, fixed size, overwrites oldest entries
- Stats `.bak` sentinel files — intentional crash-safety pattern

## Explore Strategy

Split by resource type for independent parallel exploration:

- **D2D / GDI+** — `src/gui/gui_paint.ahk`, `src/gui/gui_overlay.ahk`, `src/gui/gui_gdip.ahk`, any file using `D2D_*` functions. Some `Gdip_*` may remain in `src/lib/` but the paint pipeline is D2D now
- **Win32 handles** — `src/core/` producers, `src/shared/ipc_pipe.ahk`, DllCall-heavy files. Use `query_function_visibility.ps1` to trace cleanup call chains and `query_callchain.ps1 -Reverse` to find all callers that should reach cleanup — verify every Create/Open has a corresponding Close/Delete reachable from all callers. Use `query_global_ownership.ps1 <resource>` to determine who declares and writes resource handles (responsible for cleanup). Use `query_impact.ps1 <cleanup_func>` to assess the blast radius if a cleanup function is missing or broken.
- **Timers** — use `query_timers.ps1` to inventory all timers, then check each for proper cleanup
- **Pipe IPC** — `src/shared/ipc_pipe.ahk`, `src/pump/` files
- **Data growth** — `src/shared/window_list.ahk` (window store), icon/process caches
- **CPU churn** — timer callbacks, paint functions, producer polling loops

## Validation

After explore agents report back, **validate every finding yourself**. Resource "leaks" are frequently false positives where cleanup happens in a different function, on a timer, or at process exit.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted.
2. **Trace the lifecycle**: Where is the resource created? Where is it supposed to be freed? Is there a cleanup function called on exit/disconnect/error?
3. **Counter-argument**: "What would make this fix unnecessary?" — Is the resource freed at process exit anyway? Is the "leak" actually a cache with bounded size? Does AHK's garbage collector handle this?
4. **Observed vs inferred**: State whether you saw a missing cleanup directly, or inferred it from the absence of a delete call (absence of evidence is not evidence — the cleanup may be elsewhere).
5. **Impact assessment**: Is this a per-paint leak (catastrophic), per-window leak (slow burn), or per-session leak (negligible)?

## Plan Format

Group by severity (per-paint > per-event > per-session > theoretical):

| File | Lines | Resource Type | Leak Description | Impact | Fix |
|------|-------|--------------|-----------------|--------|-----|
| `file.ahk` | 42–58 | D2D Brush | D2D brush created in paint loop, never released | ~60 handles/sec | Use `D2D_GetCachedBrush` or `static` |

For CPU churn findings, use a separate table:

| File | Lines | Pattern | Frequency | Fix |
|------|-------|---------|-----------|-----|
| `file.ahk` | 100–120 | Timer polls every 100ms, no-ops 99% of the time | 10/sec idle | Adaptive interval or event-driven |

Ignore any existing plans — create a fresh one.
