---
name: reactive-same-frame-testing
description: |
  Test same-frame event behavior in the Reactive FRP library. Use when: (1) testing
  zipE, difference, or mergeList combinators that require simultaneous firing,
  (2) tests fail because events fire in separate frames when you need them in the
  same frame, (3) newTriggerEvent fires aren't combining as expected. Covers
  SpiderEnv.withFrame usage and raw trigger access for frame-controlled testing.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# Testing Same-Frame Event Behavior in Reactive FRP

## Problem

When testing Reactive FRP combinators like `zipE`, `difference`, or `mergeList` that
depend on events firing simultaneously in the same propagation frame, standard
`newTriggerEvent` triggers won't work because each trigger call starts its own frame.

## Context / Trigger Conditions

- Testing `Event.zipE` - should only fire when both events fire simultaneously
- Testing `Event.difference` - should suppress when both events fire in same frame
- Testing `Event.mergeList` - should collect simultaneous values into a single list
- Tests show events firing separately when you expected them to fire together
- Using `newTriggerEvent` and calling triggers sequentially

## Root Cause

In Reactive's Spider runtime, `newTriggerEvent` wraps each raw trigger with
`env.withFrame`:

```lean
instance : TriggerEvent Spider SpiderM where
  newTriggerEvent := ⟨fun env => do
    let (event, rawTrigger) ← Event.newTrigger env.timelineCtx
    -- Each trigger call starts a new frame if not already in one
    let framedTrigger := fun a => env.withFrame (rawTrigger a)
    pure (event, framedTrigger)⟩
```

When you call multiple framed triggers sequentially, each completes its own frame
before the next starts. For same-frame testing, you need raw triggers inside a
single `withFrame` call.

## Solution

### 1. Create a fireSimultaneous helper

```lean
/-- Fire multiple triggers simultaneously in the same propagation frame. -/
private def fireSimultaneous (fires : List (IO Unit)) : SpiderM Unit := do
  let env ← SpiderM.getEnv
  SpiderM.liftIO <| env.withFrame do
    for fire in fires do fire
```

### 2. Use raw triggers via Event.newTrigger

```lean
proptest "Event.zipE fires only when both fire simultaneously" :=
  forAllIO (Gen.pair (Gen.chooseInt 1 50) (Gen.chooseInt 1 50)) fun (a, b) =>
    runSpiderIO do
      let ctx ← SpiderM.getTimelineCtx
      -- Use raw triggers (not framed) so we can control frame boundaries
      let (e1, rawFire1) ← SpiderM.liftIO <| Event.newTrigger ctx
      let (e2, rawFire2) ← SpiderM.liftIO <| Event.newTrigger ctx
      let zipped ← SpiderM.liftIO <| Event.zipE ctx e1 e2

      let received ← SpiderM.liftIO <| IO.mkRef ([] : List (Int × Int))
      let _ ← zipped.subscribe fun v => received.modify (· ++ [v])

      -- Fire both in same frame
      fireSimultaneous [rawFire1 a, rawFire2 b]

      let actual ← SpiderM.liftIO received.get
      pure (actual == [(a, b)])
```

### 3. Key APIs

- `SpiderM.getEnv` - Access the SpiderEnv for frame control
- `env.withFrame` - Execute IO actions within a single propagation frame
- `Event.newTrigger ctx` - Get raw trigger (not frame-wrapped)

## Verification

After using `fireSimultaneous`:
- `zipE` should emit paired values when both fire
- `difference` should suppress output when both fire
- `mergeList` should collect all values into a single list emission

## Example: Testing Event.difference

```lean
proptest "Event.difference suppressed when both fire simultaneously" :=
  forAllIO (Gen.chooseInt 1 50) fun a =>
    runSpiderIO do
      let ctx ← SpiderM.getTimelineCtx
      let (e1, rawFire1) ← SpiderM.liftIO <| Event.newTrigger ctx
      let (e2, rawFire2) ← SpiderM.liftIO <| Event.newTrigger ctx
      let diff ← SpiderM.liftIO <| Event.difference ctx e1 e2

      let received ← SpiderM.liftIO <| IO.mkRef ([] : List Int)
      let _ ← diff.subscribe fun v => received.modify (· ++ [v])

      -- Fire both in same frame - diff should be suppressed
      fireSimultaneous [rawFire1 a, rawFire2 ()]

      let actual ← SpiderM.liftIO received.get
      pure actual.isEmpty  -- Should receive nothing
```

## Notes

- `withFrame` is idempotent: if already in a frame, it just runs the action
- The frame drains the propagation queue in height order after all fires complete
- This pattern is only needed for testing; normal application code uses framed triggers
- Raw triggers should not escape the test scope to avoid frame-boundary bugs

## References

- Reactive library source: `Reactive/Host/Spider/Core.lean` (SpiderEnv.withFrame)
- Reactive combinators: `Reactive/Combinators/Event.lean` (zipE, difference, mergeList)
