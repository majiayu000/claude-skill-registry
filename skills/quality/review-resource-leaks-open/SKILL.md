---
name: review-resource-leaks-open
description: Open Audit for memory leaks, handle leaks, GDI leaks, and CPU churn
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Systematically audit the codebase for resource/memory leaks and unnecessary CPU churn. Use maximum parallelism — spawn explore agents for independent areas.

## Known Safe Patterns (Do NOT Flag)

- `gD2D_Res` brush/font cache — intentional lifetime cache, cleaned up on exit
- `static` buffers in hot-path functions — intentional reuse per `ahk-patterns.md`
- Flight recorder ring buffer — pre-allocated, fixed size, overwrites oldest entries
- Stats `.bak` sentinel files — intentional crash-safety pattern

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
