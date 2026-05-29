---
name: reactive-frp-frame-semantics
description: |
  Understanding frame nesting behavior in the Reactive FRP library. Use when:
  (1) triggers inside callbacks don't seem to propagate, (2) sample returns
  initial values instead of accumulated values, (3) foldDyn doesn't update
  as expected inside runWithReplaceM or event subscription callbacks,
  (4) code works at top level but not inside replacement computations.
  Covers withFrame, drainQueue, and glitch-free propagation semantics.
author: Claude Code
version: 1.0.0
date: 2025-01-22
---

# Reactive FRP Frame Semantics

## Problem

When using `foldDyn`, `trigger`, and `sample` inside `runWithReplaceM` replacement
computations or event subscription callbacks, `sample` returns initial values
instead of accumulated values, even though triggers were called.

## Context / Trigger Conditions

- Using `runWithReplaceM` or `runWithReplaceRequester` from Reactive.Host.Spider
- Calling `trigger` inside a replacement computation or subscription callback
- Expecting to `sample` a dynamic that should have been updated by those triggers
- Code works when run at top level but fails inside callbacks
- Test expects accumulated value but gets initial value (e.g., expects `[15, 30]`, gets `[15, 0]`)

## Root Cause

The Reactive library uses **frame-based propagation** for glitch-freedom:

1. **Triggers are framed**: `newTriggerEvent` returns a trigger wrapped with `env.withFrame`

2. **Frame behavior**:
   - If NOT in a frame: starts new frame, runs action, drains queue, ends frame
   - If ALREADY in a frame: just runs the action (no new drain cycle)

3. **Queue processing**: Events fired during a frame are enqueued and processed
   in height order after current callbacks complete

4. **Initial vs replacement context**:
   - Initial computations run OUTSIDE any frame (each trigger gets its own frame)
   - Replacement computations run INSIDE the triggering event's frame

## Solution

**Option 1: Return values that don't depend on synchronous propagation**

```lean
let computeWithState : Nat → SpiderM Nat := fun multiplier => do
  let (evt, trigger) ← newTriggerEvent (t := Spider) (a := Nat)
  let dyn ← foldDyn (fun x acc => acc + x) 0 evt
  trigger (multiplier * 1)
  trigger (multiplier * 2)
  -- Return multiplier directly, NOT sample dyn.current
  pure multiplier
```

**Option 2: Use initial values from holdDyn**

```lean
let computeWithState : Nat → SpiderM Nat := fun multiplier => do
  let (evt, _) ← newTriggerEvent (t := Spider) (a := Nat)
  let dyn ← holdDyn (multiplier * 3) evt  -- Initial value is computed
  sample dyn.current  -- Returns the initial value (multiplier * 3)
```

**Option 3: Observe dynamics after frame completes**

Subscribe to external events and verify dynamics work after the replacement frame ends.

## Key Code Locations

- `Reactive/Host/Spider/Core.lean:140` - `withFrame` implementation
- `Reactive/Host/Spider/Core.lean:108` - `drainQueue` implementation
- `Reactive/Host/Spider/Core.lean:302` - `TriggerEvent` instance wraps trigger
- `Reactive/Core/Event.lean:94` - `fire` checks frame status and enqueues

## Trace: Why Initial Works But Replacement Doesn't

**Initial computation** (runs outside frame):
```
trigger 5 → withFrame: NOT in frame
  → starts NEW frame
  → rawTrigger 5 → enqueues
  → drainQueue → foldDyn updates valueRef to 5
  → frame ends

trigger 10 → withFrame: NOT in frame (previous ended!)
  → starts NEW frame, drains, valueRef = 15
  → frame ends

sample → reads 15 ✓
```

**Replacement computation** (runs inside triggerReplace's frame):
```
triggerReplace(...) → withFrame starts frame
  → subscription callback runs (STILL IN FRAME!)
    → trigger 10 → withFrame: ALREADY in frame
      → just runs rawTrigger (no drain!)
      → enqueues to same queue
    → trigger 20 → enqueues
    → sample → reads 0 (queue not drained yet!)
    → returns 0
  → drainQueue continues, fires 10 and 20 (too late!)
→ frame ends
```

## Verification

Test that your code handles frame semantics correctly:
- Run `lake test` in the reactive project
- Check `ReactiveTests/AdjustableTests.lean` for examples

## Notes

- This is **correct glitch-free FRP behavior**, not a bug
- Within a frame, all events logically occur "at the same instant"
- You cannot observe intermediate propagation states during a frame
- FRP infrastructure created inside replacements DOES work—just not synchronously
- The dynamics will update correctly after the frame completes
