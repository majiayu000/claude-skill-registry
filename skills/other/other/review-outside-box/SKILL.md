---
name: review-outside-box
description: Zoom out and find whole classes of performance, bug, or anti-pattern issues hiding in plain sight
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Think outside the box. Use maximum parallelism and processing — don't worry about tokens.

## What This Is

The other review skills look at specific domains: race conditions, resource leaks, dead code, etc. This review is different. It **zooms out** to find systemic patterns that cut across the entire codebase — whole classes of issues that are invisible when you're focused on individual functions or files.

Past runs of this review have found massive wins that targeted reviews missed (e.g., discovering that the entire codebase was using regex parsing where JSON parsing would be orders of magnitude faster). These are the "in retrospect, obvious" patterns that hide because everyone is looking at the trees, not the forest.

## How to Think

Do NOT start by reading individual functions. Start by asking architectural questions:

### Data flow
- What data format is used for IPC? Is it the right one? Is it parsed efficiently?
- How many times is the same data transformed, serialized, or copied between formats?
- Are there data structures being rebuilt from scratch when they could be incrementally updated?
- Is data being stored in one format but always consumed in another (requiring constant conversion)?

### Call patterns
- Are there O(n²) patterns hiding in nested loops over window lists, maps, or arrays?
- Are expensive operations (DllCall, file I/O, regex) inside hot loops when they could be hoisted?
- Are there functions called frequently that do redundant work because they don't know what changed?
- Is the same computation done independently by multiple callers when it could be done once and shared?

### Architecture
- Are there whole subsystems that exist for historical reasons but whose job could be done more simply now?
- Are there abstraction layers that add overhead without adding value?
- Is IPC being used where in-process data sharing would work?
- Are there synchronous operations blocking the hot path that could be async?

### Resource patterns
- Is the same file/registry/config being read repeatedly instead of cached?
- Are there per-item allocations (strings, buffers, objects) inside loops that process lists?
- Is GDI+/Win32 API usage following the optimal pattern, or a "works but slow" pattern?

### AHK-specific
- Are there places using AHK built-in commands where a DllCall would be dramatically faster?
- Conversely, are there DllCall chains where an AHK built-in does the same thing more simply?
- Are timer frequencies appropriate, or are some polling faster than needed?
- Are there string operations (concatenation in loops, regex where InStr suffices) that dominate hot paths?

## Explore Strategy

This review benefits from **diverse perspectives**. Spawn explore agents with different lenses:

- **Data flow agent** — trace data from producers → store → GUI. How many format conversions? How many copies?
- **Hot path agent** — identify the 5 most frequently executed code paths (keyboard input, paint, timer ticks, WinEvent callbacks) and profile their patterns
- **Architecture agent** — map the high-level module interactions. Any unnecessary indirection?
- **Resource agent** — trace file handles, DllCalls, GDI objects through their lifecycle. Any systemic waste pattern?
- **History agent** — skim git log for patterns of fixes. Do the same kinds of bugs keep happening in the same subsystem? That's a design smell.

Each agent should think at the **system level**, not the function level. The question is "is this the right approach?" not "is this function correct?"

## Validation

After explore agents report back, **validate every finding yourself**. Systemic findings need extra scrutiny because they often suggest large refactors — make sure the payoff justifies the cost.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" — quote the actual pattern across multiple files to show it's systemic, not isolated.
2. **Quantify the impact**: How many files/functions exhibit this pattern? What's the estimated cost (CPU time, memory, latency, code complexity)?
3. **Counter-argument**: "What would make this change counterproductive?" — Would the fix add complexity that outweighs the gain? Is the current approach "good enough" given actual usage patterns? Would the migration risk outweigh the benefit?
4. **Observed vs inferred**: Did you measure or count the pattern directly, or infer it from a few examples?
5. **Scope the fix**: Is this a "change 3 lines in 20 files" fix or a "redesign the subsystem" fix? Both can be valuable, but the plan should be honest about scope.

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
