---
name: concurrent-observable-state-updates
description: |
  Pattern for updating observable state from multiple concurrent threads while preserving
  event delivery. Use when: (1) multiple threads update shared state and publish to
  observables/dynamics, (2) events tied to state changes are being dropped, (3) stale
  state overwrites newer state due to thread interleaving, (4) lock ordering causes
  deadlocks between frame/transaction locks and other mutexes. Covers monotonic version
  numbers, atomic CAS for state, and separating event firing from state version checks.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# Concurrent Observable State Updates

## Problem

When multiple threads update shared state and publish to observables (reactive values,
UI state, etc.), several concurrency bugs can occur:

1. **Stale overwrites**: Thread A reads state, Thread B updates and publishes newer state,
   then Thread A publishes its stale snapshot, overwriting B's correct state
2. **Event drops**: Using version numbers to skip stale state updates also skips the
   associated events, losing notifications of things that actually happened
3. **Lock order inversion**: Taking a version/state mutex before a frame/transaction lock
   creates deadlock risk with code paths that hold frame lock first
4. **Frame incoherence**: Events and state updates in separate frames cause subscribers
   to see inconsistent snapshots

## Context / Trigger Conditions

- Multiple worker threads completing tasks and updating shared state
- FRP/reactive systems where state changes trigger observable updates
- Worker pools, task queues, or concurrent job processors
- Symptoms: missing events, state showing older values, occasional deadlocks

## Solution

### 1. Use Monotonic Version Numbers

Add a version counter to your state that increments on every mutation:

```
structure State where
  data : ...
  version : Nat := 0  -- Monotonically increasing
```

Every atomic state mutation must increment the version:
```
atomically do
  let newVersion := state.version + 1
  let newState := { state with ..., version := newVersion }
  set newState
  return (newState, newVersion)
```

### 2. Separate Event Firing from State Version Checks

**Critical insight**: Events represent things that happened and must NEVER be dropped.
Version checks should only gate observable/state updates, not events.

```
let updateWithEvent := fun (state, version, fireEvent) =>
  withFrame do
    -- ALWAYS fire events first - they happened, notify subscribers
    fireEvent

    -- THEN check version for state updates only
    let shouldUpdateState ← versionMutex.atomically do
      if version > lastPublishedVersion then
        set version
        return true
      else
        return false

    if shouldUpdateState then
      updateObservables state
```

### 3. Consistent Lock Ordering

**Always acquire frame/transaction lock BEFORE any other mutexes**:

```
-- CORRECT: Frame lock first, then version mutex inside
withFrame do
  fireEvent
  versionMutex.atomically do ...  -- Brief, inside frame

-- WRONG: Version mutex first creates lock inversion risk
versionMutex.atomically do ...
withFrame do ...  -- Can deadlock with code already in frame
```

### 4. Atomic State Modifications Return New State

Don't read state separately from modifying it - return the new state from the atomic block:

```
-- CORRECT: Modification returns the state to publish
let (newState, version) ← stateMutex.atomically do
  let modified := { currentState with ... }
  set modified
  return (modified, modified.version)
publishState newState version

-- WRONG: Separate read can see other threads' changes
stateMutex.atomically do modify ...
let state ← stateMutex.atomically do get  -- May include other changes!
publishState state
```

## Verification

1. **No event drops**: Every completed operation fires its event, even if state update is skipped
2. **Monotonic state**: Observable state version never decreases
3. **No deadlocks**: All code paths acquire locks in same order (frame → version)
4. **Eventually consistent**: Final observable state matches final mutex state

## Example

Worker pool with concurrent job completions:

```lean
-- Worker completes job
let (newState, version) ← stateMutex.atomically do
  if generation == expectedGeneration then
    let state' := { state with
      running := state.running.erase jobId,
      statuses := state.statuses.insert jobId .completed,
      version := state.version + 1
    }
    set state'
    return some (state', state'.version)
  else
    return none

match result with
| some (state, ver) =>
    -- Frame first, then version check inside
    withFrame do
      -- Always fire completion event
      fireCompleted (jobId, result)

      -- Only update observables if latest version
      let shouldUpdate ← versionMutex.atomically do
        if ver > lastPublished then
          set ver; return true
        else return false

      if shouldUpdate then
        updateJobStates state.statuses
        updateCounts state.pending.size state.running.size
| none => pure ()
```

## Notes

- **Trade-off**: When an event fires, observable state might not yet reflect that event
  if a newer version was already published. But events carry complete data, so subscribers
  have what they need.
- **State is eventually consistent**: The latest state will be published; only intermediate
  stale states are skipped.
- **Events are point-in-time**: They represent discrete occurrences, so they must always fire.
- **Observables are latest-value**: They represent current state, so stale values should be skipped.

## Anti-patterns

1. **Skipping events with state**: `if versionOk then { updateState; fireEvent }` loses events
2. **Lock inversion**: Taking state/version mutex before frame lock
3. **Separate state reads**: Reading state in one atomic block, publishing in another
4. **Blocking in frame**: Holding frame lock while doing slow operations
