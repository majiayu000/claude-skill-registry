---
name: effect-match-patterns
description: Effect.Match for discriminated unions, Queue/PubSub for concurrency, Fiber lifecycle, and HashMap for registries. Covers patterns missing from effect-patterns skill.
model_invoked: true
triggers:
  - "Match"
  - "Match.tag"
  - "Match.tagsExhaustive"
  - "Queue"
  - "PubSub"
  - "Fiber"
  - "HashMap"
  - "pattern matching"
---

# Effect Match, Queue, PubSub, Fiber, HashMap Patterns

## Overview

This skill covers advanced Effect-TS patterns not in the core `effect-patterns` skill:

1. **Match** — Type-safe pattern matching with exhaustiveness checking
2. **Queue** — Bounded/unbounded async queues for producer-consumer patterns
3. **PubSub** — One-to-many event broadcasting
4. **Fiber** — Lightweight concurrency (fork, join, interrupt)
5. **HashMap** — Immutable hash maps for registries

## Canonical Sources

### Effect-TS Core
- **Submodule**: `../../submodules/effect/packages/effect/src/`
- **Tests**: `../../submodules/effect/packages/effect/test/`
- **DeepWiki**: Query `Effect-TS/effect` for verification

### TMNL Implementations
- **ChannelService** — `src/lib/streams/constructs/ChannelService.ts` (Queue, PubSub, Fiber, HashMap)
- **Feed** — `src/lib/streams/constructs/Feed.ts` (Fiber lifecycle)
- **TokenRegistry** — `src/lib/primitives/TokenRegistry/TokenRegistry.ts` (HashMap)

---

## Pattern 1: Match — TYPE-SAFE PATTERN MATCHING

**When:** Pattern matching on discriminated unions with exhaustiveness checking.

### Basic Match with Tags

```typescript
import { Match } from 'effect'

type Event =
  | { readonly _tag: 'Fetch' }
  | { readonly _tag: 'Success'; readonly data: string }
  | { readonly _tag: 'Error'; readonly error: Error }
  | { readonly _tag: 'Cancel' }

const handleEvent = Match.type<Event>().pipe(
  Match.tag('Fetch', () => 'Fetching...'),
  Match.tag('Success', (e) => `Got: ${e.data}`),
  Match.tag('Error', (e) => `Error: ${e.error.message}`),
  Match.tag('Cancel', () => 'Cancelled'),
  Match.exhaustive  // Compile error if case missing
)

// Usage
const result = handleEvent({ _tag: 'Success', data: 'Hello' })  // 'Got: Hello'
```

### Match.tagsExhaustive — OBJECT SYNTAX

**When:** Prefer object syntax for all cases at once.

```typescript
import { Match, pipe } from 'effect'

type Shape =
  | { _tag: 'Circle'; radius: number }
  | { _tag: 'Square'; side: number }
  | { _tag: 'Rectangle'; width: number; height: number }

const area = pipe(
  Match.type<Shape>(),
  Match.tagsExhaustive({
    Circle: (s) => Math.PI * s.radius ** 2,
    Square: (s) => s.side ** 2,
    Rectangle: (s) => s.width * s.height,
  })
)

area({ _tag: 'Circle', radius: 5 })  // ~78.54
```

### Match with Schema.TaggedStruct

**When:** Pattern matching on Effect Schema types.

```typescript
import { Schema } from 'effect'
import { Match, pipe } from 'effect'

// Schema definitions
const PointerDown = Schema.TaggedStruct('PointerDown', {
  x: Schema.Number,
  y: Schema.Number,
})

const PointerUp = Schema.TaggedStruct('PointerUp', {
  x: Schema.Number,
  y: Schema.Number,
})

const PointerEvent = Schema.Union(PointerDown, PointerUp)
type PointerEvent = typeof PointerEvent.Type

// Pattern matching
const describe = pipe(
  Match.type<PointerEvent>(),
  Match.tagsExhaustive({
    PointerDown: (e) => `Down at (${e.x}, ${e.y})`,
    PointerUp: (e) => `Up at (${e.x}, ${e.y})`,
  })
)
```

### Match.discriminator — CUSTOM DISCRIMINANT

**When:** Discriminated union uses field other than `_tag`.

```typescript
type Message =
  | { kind: 'text'; content: string }
  | { kind: 'image'; url: string }
  | { kind: 'video'; url: string; duration: number }

const handle = pipe(
  Match.type<Message>(),
  Match.discriminator('kind')('text', (m) => m.content),
  Match.discriminator('kind')('image', (m) => `Image: ${m.url}`),
  Match.discriminator('kind')('video', (m) => `Video: ${m.url} (${m.duration}s)`),
  Match.exhaustive
)
```

---

## Pattern 2: Queue — ASYNC PRODUCER-CONSUMER

**When:** Async communication between producers and consumers.

### Bounded Queue

```typescript
import { Effect, Queue } from 'effect'

const program = Effect.gen(function* () {
  // Create bounded queue (capacity 10)
  const queue = yield* Queue.bounded<string>(10)

  // Producer
  yield* Queue.offer(queue, 'message-1')
  yield* Queue.offer(queue, 'message-2')

  // Consumer
  const msg1 = yield* Queue.take(queue)  // 'message-1'
  const msg2 = yield* Queue.take(queue)  // 'message-2'

  return [msg1, msg2]
})
```

### Queue Strategies

| Strategy | Behavior when full |
|----------|-------------------|
| `Queue.bounded(n)` | `offer` suspends until space |
| `Queue.dropping(n)` | Drops new elements |
| `Queue.sliding(n)` | Drops oldest elements |
| `Queue.unbounded()` | Never full (grows indefinitely) |

### Queue in Service Pattern

**TMNL Example** — ChannelService (`src/lib/streams/constructs/ChannelService.ts:72-73`):
```typescript
export interface ChannelInstance {
  readonly state: ChannelState
  readonly fibers: HashMap.HashMap<string, Fiber.RuntimeFiber<void, unknown>>
  readonly subscriptions: HashMap.HashMap<string, Queue.Dequeue<unknown>>
}
```

---

## Pattern 3: PubSub — ONE-TO-MANY BROADCASTING

**When:** Single publisher, multiple subscribers each receive all messages.

### Basic PubSub

```typescript
import { Effect, PubSub, Queue } from 'effect'

const program = Effect.gen(function* () {
  // Create PubSub
  const pubsub = yield* PubSub.bounded<string>(100)

  // Subscribe (each subscriber gets own Queue)
  const sub1 = yield* PubSub.subscribe(pubsub)
  const sub2 = yield* PubSub.subscribe(pubsub)

  // Publish
  yield* PubSub.publish(pubsub, 'hello')

  // Both subscribers receive
  const msg1 = yield* Queue.take(sub1)  // 'hello'
  const msg2 = yield* Queue.take(sub2)  // 'hello'
})
```

### PubSub for Event Dispatch

**TMNL Pattern** — Command/Event channels:
```typescript
// From ChannelService concept
interface ChannelServiceShape {
  readonly commandPubSub: PubSub.PubSub<ChannelCommand>
  readonly eventPubSub: PubSub.PubSub<ChannelEvent>

  // Send command to all listeners
  readonly dispatch: (cmd: ChannelCommand) => Effect.Effect<void>

  // Subscribe to events
  readonly onEvent: <T extends ChannelEvent['_tag']>(
    tag: T,
    handler: (event: Extract<ChannelEvent, { _tag: T }>) => Effect.Effect<void>
  ) => Effect.Effect<void, never, Scope.Scope>
}
```

### PubSub Strategies

| Strategy | Behavior |
|----------|----------|
| `PubSub.bounded(n)` | Backpressure on publishers |
| `PubSub.dropping(n)` | Drops new messages if full |
| `PubSub.sliding(n)` | Drops old messages |
| `PubSub.unbounded()` | Never full |

---

## Pattern 4: Fiber — LIGHTWEIGHT CONCURRENCY

**When:** Run Effects concurrently, manage lifecycle (cancel, await).

### Fork and Join

```typescript
import { Effect, Fiber } from 'effect'

const program = Effect.gen(function* () {
  // Fork runs Effect concurrently, returns immediately
  const fiber = yield* Effect.fork(
    Effect.delay(Effect.succeed('result'), '1 second')
  )

  // Do other work...
  yield* Effect.log('Doing other work')

  // Wait for fiber to complete
  const result = yield* Fiber.join(fiber)  // 'result'
})
```

### Interrupt

```typescript
const program = Effect.gen(function* () {
  const fiber = yield* Effect.fork(
    Effect.forever(Effect.log('Running...'))
  )

  // Let it run briefly
  yield* Effect.sleep('100 millis')

  // Interrupt (cancel)
  yield* Fiber.interrupt(fiber)
})
```

### Fiber Registry Pattern

**TMNL Example** — Feed lifecycle (`src/lib/streams/constructs/Feed.ts`):
```typescript
interface FeedInstance {
  readonly state: FeedState
  readonly fiber: Fiber.RuntimeFiber<void, unknown> | null
}

// Start feed (fork emission fiber)
const start = (feedId: FeedId): Effect.Effect<void> =>
  Effect.gen(function* () {
    const feed = yield* getFeed(feedId)
    const emissionFiber = yield* Effect.fork(runEmission(feed))

    // Store fiber reference for later interrupt
    yield* updateFeed(feedId, {
      ...feed,
      fiber: emissionFiber,
    })
  })

// Stop feed (interrupt fiber)
const stop = (feedId: FeedId): Effect.Effect<void> =>
  Effect.gen(function* () {
    const feed = yield* getFeed(feedId)
    if (feed.fiber) {
      yield* Fiber.interrupt(feed.fiber)
    }
  })
```

### Scoped Fiber (Auto-Cleanup)

**When:** Fiber should be interrupted when scope closes.

```typescript
import { Effect, Scope } from 'effect'

const program = Effect.gen(function* () {
  yield* Effect.scoped(
    Effect.gen(function* () {
      // Fiber auto-interrupted when scope closes
      yield* Effect.forkScoped(
        Effect.forever(Effect.log('Running...'))
      )

      yield* Effect.sleep('100 millis')
    })
  )
  // Fiber automatically interrupted here
})
```

---

## Pattern 5: HashMap — IMMUTABLE REGISTRIES

**When:** Need immutable map for service state (registries, caches).

### Basic HashMap

```typescript
import { HashMap } from 'effect'

// Create
let map = HashMap.empty<string, number>()

// Set (returns new map)
map = HashMap.set(map, 'a', 1)
map = HashMap.set(map, 'b', 2)

// Get
const a = HashMap.get(map, 'a')  // Option.some(1)
const c = HashMap.get(map, 'c')  // Option.none()

// Size
HashMap.size(map)  // 2
```

### HashMap in Ref (Mutable Registry)

**TMNL Pattern** — ChannelService registry:
```typescript
import { Effect, Ref, HashMap, Option } from 'effect'

interface RegistryService<K, V> {
  readonly get: (key: K) => Effect.Effect<Option.Option<V>>
  readonly set: (key: K, value: V) => Effect.Effect<void>
  readonly remove: (key: K) => Effect.Effect<void>
  readonly entries: Effect.Effect<ReadonlyArray<readonly [K, V]>>
}

const makeRegistry = <K, V>(): Effect.Effect<RegistryService<K, V>> =>
  Effect.gen(function* () {
    const ref = yield* Ref.make(HashMap.empty<K, V>())

    return {
      get: (key) => Ref.get(ref).pipe(Effect.map((m) => HashMap.get(m, key))),

      set: (key, value) =>
        Ref.update(ref, (m) => HashMap.set(m, key, value)),

      remove: (key) =>
        Ref.update(ref, (m) => HashMap.remove(m, key)),

      entries: Ref.get(ref).pipe(Effect.map(HashMap.toEntries)),
    }
  })
```

### HashMap with Fiber References

**TMNL Example** — ChannelInstance (`src/lib/streams/constructs/ChannelService.ts:69-73`):
```typescript
export interface ChannelInstance {
  readonly state: ChannelState
  readonly fibers: HashMap.HashMap<string, Fiber.RuntimeFiber<void, unknown>>
  readonly subscriptions: HashMap.HashMap<string, Queue.Dequeue<unknown>>
}

const makeInstance = (state: ChannelState): ChannelInstance => ({
  state,
  fibers: HashMap.empty(),
  subscriptions: HashMap.empty(),
})
```

---

## Anti-Patterns

### 1. Missing Exhaustiveness Check

```typescript
// WRONG — No compile error if case missing
const handle = Match.type<Event>().pipe(
  Match.tag('Fetch', () => 'Fetching'),
  Match.orElse(() => 'Unknown'),  // Catches all — hides missing cases
)

// CORRECT — Compile error if case missing
const handle = Match.type<Event>().pipe(
  Match.tag('Fetch', () => 'Fetching'),
  Match.tag('Success', (e) => e.data),
  Match.tag('Error', (e) => e.error.message),
  Match.tag('Cancel', () => 'Cancelled'),
  Match.exhaustive,  // Enforces all cases
)
```

### 2. Unbounded Queue Memory Leak

```typescript
// WRONG — Queue grows forever if consumer is slow
const queue = yield* Queue.unbounded<Event>()

// CORRECT — Bounded with backpressure or sliding
const queue = yield* Queue.bounded<Event>(1000)
// or
const queue = yield* Queue.sliding<Event>(1000)  // Drop old if full
```

### 3. Fiber Leak (No Interrupt)

```typescript
// WRONG — Fiber runs forever, never cleaned up
const fiber = yield* Effect.fork(Effect.forever(...))
// Fiber keeps running even after parent exits

// CORRECT — Use forkScoped or manual interrupt
yield* Effect.scoped(
  Effect.forkScoped(Effect.forever(...))
)  // Auto-interrupted on scope close

// OR
const fiber = yield* Effect.fork(...)
yield* Effect.ensuring(
  doWork,
  Fiber.interrupt(fiber)  // Always interrupt on exit
)
```

### 4. HashMap Mutation (Wrong Mental Model)

```typescript
// WRONG — HashMap is immutable, this doesn't work
const map = HashMap.empty<string, number>()
HashMap.set(map, 'a', 1)  // Returns NEW map, original unchanged
console.log(HashMap.get(map, 'a'))  // None!

// CORRECT — Capture returned map
let map = HashMap.empty<string, number>()
map = HashMap.set(map, 'a', 1)
console.log(HashMap.get(map, 'a'))  // Some(1)
```

---

## Decision Tree: When to Use Each

```
Need async communication?
│
├─ One producer, one consumer?
│  └─ Use: Queue.bounded() or Queue.unbounded()
│
├─ One producer, many consumers (each gets ALL messages)?
│  └─ Use: PubSub (each subscriber gets own Queue)
│
├─ Pattern matching on discriminated union?
│  ├─ Want exhaustiveness check?
│  │  └─ Use: Match.exhaustive or Match.tagsExhaustive
│  └─ OK with fallback?
│     └─ Use: Match.orElse
│
├─ Need concurrent execution?
│  ├─ Fire and forget?
│  │  └─ Use: Effect.fork (but manage lifecycle!)
│  ├─ Need result later?
│  │  └─ Use: Effect.fork + Fiber.join
│  └─ Auto-cleanup on scope exit?
│     └─ Use: Effect.forkScoped
│
└─ Need registry/map state?
   └─ Use: Ref.make(HashMap.empty<K, V>())
      with HashMap.set/get/remove
```

---

## File Locations Summary

| Pattern | File | Lines | Usage |
|---------|------|-------|-------|
| **Queue + PubSub** | `src/lib/streams/constructs/ChannelService.ts` | 16-54 | Event dispatch |
| **Fiber registry** | `src/lib/streams/constructs/ChannelService.ts` | 69-79 | Lifecycle management |
| **HashMap registry** | `src/lib/primitives/TokenRegistry/TokenRegistry.ts` | — | Token storage |
| **Fiber lifecycle** | `src/lib/streams/constructs/Feed.ts` | — | Emission control |

---

## Integration Points

- **effect-patterns** — Service/Layer patterns that use these primitives
- **effect-stream-patterns** — Streams that produce to Queues/PubSub
- **effect-atom-integration** — Atoms that wrap Queue/PubSub state
- **xstate-integration** — Machine transitions that dispatch via PubSub
