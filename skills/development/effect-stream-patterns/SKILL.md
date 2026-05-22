---
name: effect-stream-patterns
description: Stream creation, consumption, transformation. Stream.async, Stream.fromSchedule, Stream.runForEach. Progressive data patterns for Effect-TS streams.
model_invoked: true
triggers:
  - "Stream"
  - "progressive"
  - "Stream.async"
  - "Stream.runForEach"
  - "streaming"
---

# Effect Stream Patterns

## Overview

**Effect Streams** are pull-based, lazy sequences of values. Unlike Observables (push-based), Streams are consumed on-demand and provide powerful composition primitives.

Key characteristics:
- **Pull-based** — Consumer drives execution
- **Lazy** — Only computes what's needed
- **Chunked** — Emits `Chunk<A>` for efficiency
- **Effectful** — Each element can be an `Effect`
- **Composable** — Rich operators for transformation

Use streams for:
- **Progressive data loading** — Display results as they arrive
- **Infinite sequences** — Tickers, pollers, event sources
- **Resource-efficient processing** — Process large datasets without loading all into memory
- **Async iteration** — Cleaner than manual async loops

## Canonical Sources

### Effect Stream Core
- **Submodule**: `../../submodules/effect/packages/effect/src/`
  - `Stream.ts:52-70` — Stream constructors
  - `Stream.ts:316-362` — Stream.async
  - `Stream.ts` (various) — Operators and consumers

### Effect Website Documentation
- **Submodule**: `../../submodules/website/content/src/content/docs/docs/stream/`
  - `creating.mdx` — Stream constructors
  - `consuming-streams.mdx` — Running streams
  - `operations.mdx` — Transformations
  - `error-handling.mdx` — Failure management
  - `resourceful-streams.mdx` — Resource-managed streams

### TMNL Battle-tested Implementations
- **Progressive search** — `src/lib/data-manager/v1/atoms/index.ts:206` (Stream with atom updates)
- **Stream-to-Atom** — `src/lib/streams/atoms/streamToAtom.ts` (Reactive integration)
- **Mock streams** — `src/lib/data-grid/mocking/stream.ts` (Test utilities)

## Patterns

### Decision Tree: Which Stream Pattern?

```
Need a stream?
│
├─ From existing data (array, iterable)?
│  └─ Use: Stream.fromIterable(data)
│
├─ From async callback (WebSocket, EventSource)?
│  └─ Use: Stream.async((emit) => { ... })
│
├─ Ticking/polling at intervals?
│  └─ Use: Stream.fromSchedule(Schedule.spaced(...))
│
├─ Single effectful value?
│  └─ Use: Stream.fromEffect(effect)
│
├─ Range of numbers?
│  └─ Use: Stream.range(start, end)
│
├─ Infinite sequence?
│  └─ Use: Stream.iterate(initial, fn)
│
└─ From another stream with transformation?
   └─ Use: stream.pipe(Stream.map(...))
```

---

### Pattern 1: Stream.fromIterable — FROM ARRAYS

**When to use:**
- Have existing array/iterable data
- Want to process data lazily
- Need to chunk large datasets

**Signature:**
```typescript
Stream.fromIterable<A>(iterable: Iterable<A>): Stream.Stream<A>
```

**Full Example:**
```typescript
import { Stream, Effect } from 'effect'

// From array
const numbers = Stream.fromIterable([1, 2, 3, 4, 5])

// Lazy processing (only computes when consumed)
const doubled = numbers.pipe(
  Stream.map((n) => n * 2)
)

// Consume
const result = await Stream.runCollect(doubled).pipe(Effect.runPromise)
console.log(result)  // Chunk([2, 4, 6, 8, 10])

// From generator
function* fibonacci() {
  let a = 0, b = 1
  while (true) {
    yield a
    ;[a, b] = [b, a + b]
  }
}

const fibs = Stream.fromIterable(fibonacci()).pipe(
  Stream.take(10)
)
```

**Key Features:**
- **Lazy evaluation** — Doesn't process until consumed
- **Automatic chunking** — Emits `Chunk<A>` for efficiency
- **Supports generators** — Works with any `Iterable`

---

### Pattern 2: Stream.async — FROM ASYNC CALLBACKS

**When to use:**
- Integrate push-based sources (WebSocket, EventSource, DOM events)
- Wrap callbacks into pull-based stream
- Need cleanup logic

**Signature:**
```typescript
Stream.async<A, E>(
  register: (emit: Emit<A, E>) => Effect.Effect<void> | void,
  bufferSize?: number
): Stream.Stream<A, E>
```

**Full Example:**
```typescript
import { Stream, Effect } from 'effect'

// WebSocket stream
const wsStream = Stream.async<string, Error>((emit) => {
  const ws = new WebSocket('wss://example.com/stream')

  ws.onmessage = (event) => {
    emit.single(event.data)  // Emit single value
  }

  ws.onerror = (error) => {
    emit.fail(new Error('WebSocket error'))  // Emit error
  }

  ws.onclose = () => {
    emit.end()  // End stream
  }

  // Cleanup function
  return Effect.sync(() => {
    ws.close()
  })
})

// EventSource stream
const sseStream = Stream.async<MessageEvent>((emit) => {
  const source = new EventSource('/api/events')

  source.onmessage = (event) => {
    emit.single(event)
  }

  source.onerror = () => {
    emit.fail(new Error('SSE error'))
  }

  return Effect.sync(() => {
    source.close()
  })
})

// DOM event stream
const clickStream = Stream.async<MouseEvent>((emit) => {
  const handler = (event: MouseEvent) => {
    emit.single(event)
  }

  document.addEventListener('click', handler)

  return Effect.sync(() => {
    document.removeEventListener('click', handler)
  })
})
```

**Emit API:**
- `emit.single(value)` — Emit one value
- `emit.chunk(chunk)` — Emit multiple values at once
- `emit.fail(error)` — Emit error and end stream
- `emit.end()` — End stream successfully
- `emit.fromEffect(effect)` — Emit from Effect
- `emit.fromEffectChunk(effect)` — Emit chunk from Effect

**Key Features:**
- **Cleanup support** — Return Effect for cleanup logic
- **Buffer size** — Control backpressure (default: 16)
- **Error handling** — Emit failures via `emit.fail`

---

### Pattern 3: Stream.fromSchedule — TICKING STREAMS

**When to use:**
- Poll at regular intervals
- Emit values on a schedule
- Implement retry logic with backoff

**Signature:**
```typescript
Stream.fromSchedule<A>(schedule: Schedule.Schedule<A>): Stream.Stream<A>
```

**Full Example:**
```typescript
import { Stream, Schedule, Effect } from 'effect'

// Tick every second
const ticker = Stream.fromSchedule(Schedule.spaced('1 second'))

// Emit current time every second
const clock = ticker.pipe(
  Stream.map(() => new Date())
)

// Exponential backoff ticker
const backoff = Stream.fromSchedule(
  Schedule.exponential('100 millis').pipe(
    Schedule.compose(Schedule.recurs(5))  // Max 5 retries
  )
)

// Poll API every 5 seconds
const pollApi = Stream.fromSchedule(Schedule.spaced('5 seconds')).pipe(
  Stream.mapEffect(() =>
    Effect.tryPromise(() => fetch('/api/status').then(r => r.json()))
  )
)

// Consume with counter
const counted = ticker.pipe(
  Stream.scan(0, (count) => count + 1),
  Stream.take(10)
)
```

**Common Schedules:**
- `Schedule.spaced('1 second')` — Fixed interval
- `Schedule.exponential('100 millis')` — Exponential backoff
- `Schedule.fibonacci('1 second')` — Fibonacci backoff
- `Schedule.recurs(n)` — Limit number of emissions

**Key Features:**
- **Schedule composition** — Combine schedules with `.pipe`
- **Automatic timing** — No manual `setTimeout`
- **Configurable** — Durations, retry logic, jitter

---

### Pattern 4: Stream.fromEffect — SINGLE EFFECTFUL VALUE

**When to use:**
- Stream from a single Effect
- Lift async operation into stream
- Compose with other streams

**Signature:**
```typescript
Stream.fromEffect<A, E>(effect: Effect.Effect<A, E>): Stream.Stream<A, E>
```

**Full Example:**
```typescript
import { Stream, Effect } from 'effect'

// From Effect
const userStream = Stream.fromEffect(
  Effect.tryPromise(() =>
    fetch('/api/user').then(r => r.json())
  )
)

// Compose multiple
const combined = Stream.mergeAll(
  Stream.fromEffect(fetchUsers),
  Stream.fromEffect(fetchPosts),
  Stream.fromEffect(fetchComments)
)

// Chain effectful streams
const users = Stream.fromEffect(fetchUserIds).pipe(
  Stream.flatMap((id) =>
    Stream.fromEffect(fetchUser(id))
  )
)
```

---

### Pattern 5: Stream Transformations

**map** — Transform each element:
```typescript
const doubled = stream.pipe(
  Stream.map((n) => n * 2)
)
```

**mapEffect** — Transform with Effect:
```typescript
const validated = stream.pipe(
  Stream.mapEffect((item) =>
    Effect.tryPromise(() => validateItem(item))
  )
)
```

**filter** — Keep matching elements:
```typescript
const evens = stream.pipe(
  Stream.filter((n) => n % 2 === 0)
)
```

**flatMap** — Transform to stream and flatten:
```typescript
const expanded = stream.pipe(
  Stream.flatMap((item) =>
    Stream.fromIterable(item.children)
  )
)
```

**take** — Limit number of elements:
```typescript
const first10 = stream.pipe(
  Stream.take(10)
)
```

**drop** — Skip first N elements:
```typescript
const afterFirst5 = stream.pipe(
  Stream.drop(5)
)
```

**scan** — Accumulate state:
```typescript
const cumulative = stream.pipe(
  Stream.scan(0, (sum, n) => sum + n)
)
```

**rechunk** — Change chunk size:
```typescript
const batched = stream.pipe(
  Stream.rechunk(50)  // Emit in chunks of 50
)
```

**debounce** — Emit only after quiet period:
```typescript
const debounced = stream.pipe(
  Stream.debounce('500 millis')
)
```

**throttle** — Limit emission rate:
```typescript
const throttled = stream.pipe(
  Stream.throttle({
    cost: () => 1,
    units: 10,
    duration: '1 second'
  })
)
```

---

### Pattern 6: Stream Consumers

**Stream.runCollect** — Collect all elements:
```typescript
const result = await Stream.runCollect(stream).pipe(Effect.runPromise)
console.log(result)  // Chunk([...])
```

**Stream.runForEach** — Side effect per element:
```typescript
await Stream.runForEach(stream, (item) =>
  Effect.sync(() => console.log(item))
).pipe(Effect.runPromise)
```

**Stream.runFold** — Reduce to single value:
```typescript
const sum = await Stream.runFold(stream, 0, (acc, n) => acc + n)
  .pipe(Effect.runPromise)
```

**Stream.runDrain** — Run and discard results:
```typescript
await Stream.runDrain(stream).pipe(Effect.runPromise)
```

**Stream.runIntoQueue** — Push to Queue:
```typescript
import { Queue } from 'effect'

const queue = await Queue.unbounded<number>().pipe(Effect.runPromise)
await Stream.runIntoQueue(stream, queue).pipe(Effect.runPromise)
```

---

### Pattern 7: Progressive Accumulation (TMNL Pattern)

**When to use:**
- Display search results as they arrive
- Progressive UI updates
- Combine Stream with effect-atom

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Stream, Effect } from 'effect'

// State atoms
const resultsAtom = Atom.make<SearchResult[]>([])
const statusAtom = Atom.make<'idle' | 'streaming' | 'complete'>('idle')

// Operation atom with progressive stream
const searchOp = runtimeAtom.fn<string>()((query, ctx) =>
  Effect.gen(function* () {
    // Create stream
    const stream = yield* SearchKernel.pipe(
      Effect.flatMap((k) => k.searchStream(query))
    )

    // Initialize state
    ctx.set(statusAtom, 'streaming')
    ctx.set(resultsAtom, [])

    // Consume stream progressively
    yield* Stream.runForEach(stream, (item) =>
      Effect.sync(() => {
        const prev = ctx.get(resultsAtom)
        ctx.set(resultsAtom, [...prev, item])
      })
    )

    // Finalize
    ctx.set(statusAtom, 'complete')
  })
)

// React component
function SearchResults() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)

  return (
    <div>
      {status === 'streaming' && <Spinner />}
      <List items={results} />
    </div>
  )
}
```

**Key Pattern:**
1. Create state atoms at module level
2. Stream emits chunks progressively
3. `Stream.runForEach` updates atoms via `ctx.set`
4. React re-renders on each atom update
5. UI shows progressive results

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:206`):
```typescript
export const doSearch = runtimeAtom.fn<{ query: string; limit: number }>()(
  ({ query, limit }, ctx) =>
    Effect.gen(function* () {
      const dm = yield* DataManager
      const stream = yield* dm.searchStream(query, limit)

      ctx.set(statusAtom, 'streaming')
      ctx.set(resultsAtom, [])

      yield* Stream.runForEach(stream, (result) =>
        Effect.sync(() => {
          const prev = ctx.get(resultsAtom)
          ctx.set(resultsAtom, [...prev, result])
        })
      )

      ctx.set(statusAtom, 'complete')
    })
)
```

---

### Pattern 8: Error Handling

**catchAll** — Recover from errors:
```typescript
const recovered = stream.pipe(
  Stream.catchAll((error) =>
    Stream.succeed({ error: error.message })
  )
)
```

**retry** — Retry on failure:
```typescript
const retried = stream.pipe(
  Stream.retry(Schedule.exponential('100 millis').pipe(
    Schedule.compose(Schedule.recurs(3))
  ))
)
```

**orElse** — Fallback stream:
```typescript
const withFallback = primaryStream.pipe(
  Stream.orElse(() => fallbackStream)
)
```

---

### Pattern 9: Stream Merging & Combining

**mergeAll** — Merge multiple streams:
```typescript
const merged = Stream.mergeAll(
  stream1,
  stream2,
  stream3
)
```

**concat** — Concatenate streams:
```typescript
const concatenated = stream1.pipe(
  Stream.concat(stream2)
)
```

**zip** — Combine elements pairwise:
```typescript
const zipped = stream1.pipe(
  Stream.zip(stream2)
)
// Emits: [a1, b1], [a2, b2], ...
```

**interleave** — Alternate between streams:
```typescript
const interleaved = stream1.pipe(
  Stream.interleave(stream2)
)
// Emits: a1, b1, a2, b2, a3, b3, ...
```

---

### Pattern 10: Resource-Managed Streams

**Stream.acquireRelease** — Managed resources:
```typescript
const fileStream = Stream.acquireRelease(
  Effect.tryPromise(() => fs.open('file.txt')),
  (handle) => Effect.sync(() => handle.close())
).pipe(
  Stream.flatMap((handle) =>
    Stream.fromIterable(handle.readLines())
  )
)
```

**Stream.ensuring** — Run effect on completion:
```typescript
const logged = stream.pipe(
  Stream.ensuring(
    Effect.sync(() => console.log('Stream completed'))
  )
)
```

## Examples

### Example 1: Infinite Ticker with Scan

```typescript
import { Stream, Schedule, Effect } from 'effect'

const counter = Stream.fromSchedule(Schedule.spaced('1 second')).pipe(
  Stream.scan(0, (count) => count + 1),
  Stream.take(10)
)

await Stream.runForEach(counter, (n) =>
  Effect.sync(() => console.log(`Tick ${n}`))
).pipe(Effect.runPromise)
```

### Example 2: WebSocket with Error Handling

```typescript
import { Stream, Effect } from 'effect'

const wsStream = Stream.async<string, Error>((emit) => {
  const ws = new WebSocket('wss://example.com')

  ws.onmessage = (event) => emit.single(event.data)
  ws.onerror = () => emit.fail(new Error('Connection failed'))
  ws.onclose = () => emit.end()

  return Effect.sync(() => ws.close())
}).pipe(
  Stream.retry(Schedule.exponential('1 second').pipe(
    Schedule.compose(Schedule.recurs(3))
  )),
  Stream.catchAll((error) =>
    Stream.succeed(`Error: ${error.message}`)
  )
)
```

### Example 3: Batched API Polling

```typescript
import { Stream, Schedule, Effect } from 'effect'

const pollUsers = Stream.fromSchedule(Schedule.spaced('5 seconds')).pipe(
  Stream.mapEffect(() =>
    Effect.tryPromise(() =>
      fetch('/api/users').then(r => r.json())
    )
  ),
  Stream.take(10),
  Stream.rechunk(3)  // Batch 3 responses together
)

await Stream.runForEach(pollUsers, (batch) =>
  Effect.sync(() => console.log(`Batch:`, batch))
).pipe(Effect.runPromise)
```

### Example 4: Stream-to-Atom (TMNL Testbed)

```typescript
import { Atom } from '@effect-atom/atom-react'
import { Stream, Schedule, Effect } from 'effect'

// Create stream atom
const tickerAtom = Atom.make(
  Stream.fromSchedule(Schedule.spaced('1 second')).pipe(
    Stream.scan(0, (n) => n + 1),
    Stream.take(10)
  )
)

// React component
function Ticker() {
  const result = useAtomValue(tickerAtom)

  if (Result.isInitial(result)) return <div>Starting...</div>
  if (Result.isSuccess(result)) return <div>Count: {result.value}</div>
  return <div>Error: {result.error.message}</div>
}
```

## Anti-Patterns

### 1. Not Consuming Streams

```typescript
// WRONG — Stream is lazy, nothing happens
const stream = Stream.fromIterable([1, 2, 3]).pipe(
  Stream.map((n) => n * 2)
)

// CORRECT — Must consume
const result = await Stream.runCollect(stream).pipe(Effect.runPromise)
```

### 2. Ignoring Errors

```typescript
// WRONG — Errors crash stream
const stream = Stream.fromIterable(urls).pipe(
  Stream.mapEffect((url) => Effect.tryPromise(() => fetch(url)))
)

// CORRECT — Handle errors
const stream = Stream.fromIterable(urls).pipe(
  Stream.mapEffect((url) =>
    Effect.tryPromise(() => fetch(url))
  ),
  Stream.catchAll((error) =>
    Stream.succeed({ error: error.message })
  )
)
```

### 3. Blocking Operations in map

```typescript
// WRONG — Blocking sync operation
const stream = Stream.fromIterable(items).pipe(
  Stream.map((item) => {
    const result = await fetchData(item)  // ❌ Can't await in map
    return result
  })
)

// CORRECT — Use mapEffect
const stream = Stream.fromIterable(items).pipe(
  Stream.mapEffect((item) =>
    Effect.tryPromise(() => fetchData(item))
  )
)
```

### 4. Not Cleaning Up Resources

```typescript
// WRONG — No cleanup
Stream.async((emit) => {
  const ws = new WebSocket('wss://example.com')
  ws.onmessage = (e) => emit.single(e.data)
  // No cleanup!
})

// CORRECT — Return cleanup Effect
Stream.async((emit) => {
  const ws = new WebSocket('wss://example.com')
  ws.onmessage = (e) => emit.single(e.data)
  return Effect.sync(() => ws.close())
})
```

## Quick Reference

| Need | Constructor | Example |
|------|-------------|---------|
| From array | `Stream.fromIterable` | `Stream.fromIterable([1, 2, 3])` |
| From async callback | `Stream.async` | `Stream.async((emit) => { ... })` |
| Ticker | `Stream.fromSchedule` | `Stream.fromSchedule(Schedule.spaced('1 second'))` |
| Single Effect | `Stream.fromEffect` | `Stream.fromEffect(fetchUser)` |
| Transform | `Stream.map` | `stream.pipe(Stream.map((n) => n * 2))` |
| Filter | `Stream.filter` | `stream.pipe(Stream.filter((n) => n > 0))` |
| Limit | `Stream.take` | `stream.pipe(Stream.take(10))` |
| Accumulate | `Stream.scan` | `stream.pipe(Stream.scan(0, (s, n) => s + n))` |
| Collect all | `Stream.runCollect` | `Stream.runCollect(stream)` |
| Side effects | `Stream.runForEach` | `Stream.runForEach(stream, (x) => Effect.log(x))` |
| Fold | `Stream.runFold` | `Stream.runFold(stream, 0, (s, n) => s + n)` |

## Related Skills

- **effect-atom-integration** — Integrate streams with React atoms
- **effect-service-authoring** — Use streams in service methods
- **effect-testing-patterns** — Test stream-based code
