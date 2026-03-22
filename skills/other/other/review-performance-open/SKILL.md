---
name: review-performance-open
description: Open performance review
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Think outside the box. Use maximum parallelism and processing — don't worry about tokens.

## What This Is

This project has ballooned in complexity over time. This project uses many targeted reviews for performance issues. But targeted reviews only find what they are targeting. This is an open ended review to step back and look for any performance improvements without a contstrained review framework.

Reviewing the code, can you find any peformance opportunities? 

The window store and its producers are a main point of focus - any work they are doing can block the interceptor and GUI. Any optimizations to the window event -> updated window store path?

The GUI runs at high frame rates and responsiveness is the #1 pillar of this project. Any optimizations to the user action/window event -> pixel on screen path? 
 
But even micro optimizations are accepted and encouraged - they add up, especially with a UI running at 240fps. 

## Validation

After explore agents report back, **validate every finding yourself**. The explore agents sometimes identify errors, that in the larger context, are handled/captured elsewhere.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" — quote the actual pattern across multiple files to show it's systemic, not isolated.
2. **Quantify the impact**: How many files/functions exhibit this pattern? What's the estimated cost (CPU time, memory, latency, code complexity)?
3. **Counter-argument**: "What would make this change counterproductive?" — Would the fix add complexity that outweighs the gain? Is the current approach "good enough" given actual usage patterns? Would the migration risk outweigh the benefit?
4. **Observed vs inferred**: Did you measure or count the pattern directly, or infer it from a few examples?
5. **Scope the fix**: Is this a "change 3 lines in 20 files" fix or a "redesign the subsystem" fix? Both can be valuable, but the plan should be honest about scope.

## Safety Constraints

This project has a COM STA message pump that makes certain "obvious" optimizations unsafe:

- **Never make `Buffer()` static** in functions reachable from the paint/COM path. D2D/DXGI COM calls pump the STA message loop and can re-enter the same function, corrupting the shared buffer. `Critical "On"` does NOT prevent this. See `ahk-patterns.md` Hot Path Resource Rules.
- **Never remove `Float()` wrappers** from `NumPut("float", ...)` calls feeding D2D/D3D buffers. These ensure IEEE 754 bit patterns — not redundancy.
- **Never move per-invocation counters** (like frame counters) to batch/frame level without verifying all consumers expect the new semantics.

These constraints exist because a previous optimization pass introduced shader corruption, FPS drops, and visual hitching that took extensive bisection to diagnose. When in doubt, leave it alone.

## Plan Format

Group by class of issue, not by file:

### Issue Class: [descriptive name]

**Pattern**: What's happening systemically (1–2 sentences)

**Evidence**: Files and line ranges showing the pattern across the codebase

**Impact**: Estimated performance/reliability/maintainability cost

**Fix approach**: High-level — not line-by-line, but "change X to Y across the codebase"

**Scope**: How many files, estimated effort

**Counter-argument**: Why this might not be worth doing

---

Order by estimated impact (largest systemic wins first). A single architectural insight that affects 20 files is more valuable than 10 isolated micro-optimizations.

Ignore any existing plans — create a fresh one.
