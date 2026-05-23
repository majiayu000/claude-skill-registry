---
name: State Management
description: This skill should be used when the user asks about "Effect Ref", "mutable state", "Ref.make", "Ref.get", "Ref.set", "Ref.update", "SubscriptionRef", "SynchronizedRef", "reactive state", "state updates", "concurrent state", "shared mutable state", or needs to understand how Effect handles mutable state in a functional way.
version: 1.0.0
---

# State Management in Effect

## Overview

Effect provides functional mutable state primitives:

- **Ref** - Basic mutable reference
- **SynchronizedRef** - Ref with effectful updates
- **SubscriptionRef** - Ref with change notifications

All are fiber-safe and work correctly with concurrent access.

## Ref - Basic Mutable Reference

### Creating and Using Refs

```typescript
import { Effect, Ref } from "effect"

const program = Effect.gen(function* () {
  const counter = yield* Ref.make(0)

  const current = yield* Ref.get(counter)

  yield* Ref.set(counter, 10)

  yield* Ref.update(counter, (n) => n + 1)

  const old = yield* Ref.getAndSet(counter, 0)

  const newValue = yield* Ref.updateAndGet(counter, (n) => n + 5)

  const [oldVal, result] = yield* Ref.modify(counter, (n) => [
    n,
    n * 2
  ])
})
```

### Atomic Operations

```typescript
const atomicIncrement = Effect.gen(function* () {
  const counter = yield* Ref.make(0)

  yield* Effect.all([
    Ref.update(counter, (n) => n + 1),
    Ref.update(counter, (n) => n + 1),
    Ref.update(counter, (n) => n + 1)
  ], { concurrency: "unbounded" })

  return yield* Ref.get(counter)
})
```

### Ref in Services

```typescript
const CounterService = Effect.gen(function* () {
  const ref = yield* Ref.make(0)

  return {
    increment: Ref.update(ref, (n) => n + 1),
    decrement: Ref.update(ref, (n) => n - 1),
    get: Ref.get(ref),
    reset: Ref.set(ref, 0)
  }
})

const CounterLive = Layer.effect(Counter, CounterService)
```

## SynchronizedRef - Effectful Updates

For updates that require running effects:

```typescript
import { Effect, SynchronizedRef } from "effect"

const program = Effect.gen(function* () {
  const ref = yield* SynchronizedRef.make({ count: 0, lastUpdated: Date.now() })

  yield* SynchronizedRef.updateEffect(ref, (state) =>
    Effect.gen(function* () {
      yield* Effect.log("Updating state")
      return {
        count: state.count + 1,
        lastUpdated: Date.now()
      }
    })
  )

  const result = yield* SynchronizedRef.modifyEffect(ref, (state) =>
    Effect.gen(function* () {
      const newCount = state.count + 1
      yield* sendMetric("counter", newCount)
      return [
        newCount,
        { ...state, count: newCount }
      ]
    })
  )
})
```

### When to Use SynchronizedRef

- Updates require API calls
- Updates require logging/metrics
- Updates depend on external state
- Updates need error handling

```typescript
// Cache with async refresh
const cache = yield* SynchronizedRef.make<Data | null>(null)

const refreshCache = SynchronizedRef.updateEffect(cache, () =>
  Effect.tryPromise(() => fetchLatestData())
)
```

## SubscriptionRef - Reactive State

For state that needs to notify subscribers:

```typescript
import { Effect, SubscriptionRef, Stream } from "effect"

const program = Effect.gen(function* () {
  const ref = yield* SubscriptionRef.make(0)

  const changes = yield* SubscriptionRef.changes(ref)

  yield* Effect.fork(
    Stream.runForEach(changes, (value) =>
      Effect.log(`Value changed to: ${value}`)
    )
  )

  yield* SubscriptionRef.set(ref, 1)
  yield* SubscriptionRef.update(ref, (n) => n + 1)
  yield* SubscriptionRef.set(ref, 10)
})
```

### Reactive Patterns

```typescript
const configRef = yield* SubscriptionRef.make(initialConfig)

const subscriber1 = Effect.fork(
  Stream.runForEach(
    SubscriptionRef.changes(configRef),
    (config) => updateService1(config)
  )
)

const subscriber2 = Effect.fork(
  Stream.runForEach(
    SubscriptionRef.changes(configRef),
    (config) => updateService2(config)
  )
)

yield* SubscriptionRef.set(configRef, newConfig)
```

## Comparison

| Feature | Ref | SynchronizedRef | SubscriptionRef |
|---------|-----|-----------------|-----------------|
| Basic get/set | ✅ | ✅ | ✅ |
| Atomic updates | ✅ | ✅ | ✅ |
| Effectful updates | ❌ | ✅ | ❌ |
| Change notifications | ❌ | ❌ | ✅ |
| Use case | Simple state | Async updates | Reactive state |

## Common Patterns

### Counter Service

```typescript
class Counter extends Context.Tag("Counter")<
  Counter,
  {
    readonly increment: Effect.Effect<number>
    readonly decrement: Effect.Effect<number>
    readonly get: Effect.Effect<number>
  }
>() {}

const CounterLive = Layer.effect(
  Counter,
  Effect.gen(function* () {
    const ref = yield* Ref.make(0)
    return {
      increment: Ref.updateAndGet(ref, (n) => n + 1),
      decrement: Ref.updateAndGet(ref, (n) => n - 1),
      get: Ref.get(ref)
    }
  })
)
```

### State Machine

```typescript
type State = "idle" | "loading" | "success" | "error"

const stateMachine = Effect.gen(function* () {
  const state = yield* Ref.make<State>("idle")

  const transition = (from: State, to: State) =>
    Ref.modify(state, (current) =>
      current === from
        ? [true, to]
        : [false, current]
    )

  return {
    state: Ref.get(state),
    startLoading: transition("idle", "loading"),
    succeed: transition("loading", "success"),
    fail: transition("loading", "error"),
    reset: Ref.set(state, "idle")
  }
})
```

### Accumulator

```typescript
const accumulator = Effect.gen(function* () {
  const items = yield* Ref.make<Array<Item>>([])

  return {
    add: (item: Item) => Ref.update(items, (arr) => [...arr, item]),
    getAll: Ref.get(items),
    clear: Ref.set(items, []),
    count: Effect.map(Ref.get(items), (arr) => arr.length)
  }
})
```

## Best Practices

1. **Use Ref for simple state** - Basic counters, flags, accumulators
2. **Use SynchronizedRef for async updates** - When updates need effects
3. **Use SubscriptionRef for reactive patterns** - When others need notifications
4. **Keep state minimal** - Don't store derived data
5. **Prefer immutable updates** - Return new objects, don't mutate

## Additional Resources

For comprehensive state management documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Ref" for basic mutable references
- "SynchronizedRef" for effectful updates
- "SubscriptionRef" for reactive state
