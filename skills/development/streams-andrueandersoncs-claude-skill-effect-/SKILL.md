---
name: Streams
description: This skill should be used when the user asks about "Effect Stream", "Stream.from", "Stream.map", "Stream.filter", "Stream.run", "streaming data", "async iteration", "Sink", "Channel", "Stream.concat", "Stream.merge", "backpressure", "Stream.fromIterable", "chunked processing", "real-time data", or needs to understand how Effect handles streaming data processing.
version: 1.0.0
---

# Streams in Effect

## Overview

Effect Streams provide:

- **Lazy evaluation** - Elements produced on demand
- **Resource safety** - Automatic cleanup
- **Backpressure** - Producer/consumer coordination
- **Composition** - Transform, filter, merge streams
- **Error handling** - Typed errors in stream pipeline

```typescript
Stream<A, E, R>
// Produces values of type A
// May fail with error E
// Requires environment R
```

## Creating Streams

### From Values

```typescript
import { Stream } from "effect"

const numbers = Stream.make(1, 2, 3, 4, 5)

const fromArray = Stream.fromIterable([1, 2, 3])

const empty = Stream.empty

const single = Stream.succeed(42)

const infinite = Stream.iterate(1, (n) => n + 1)
```

### From Effects

```typescript
const fromEffect = Stream.fromEffect(fetchData())

const polling = Stream.repeatEffect(checkStatus())

const scheduled = Stream.repeatEffectWithSchedule(
  checkStatus(),
  Schedule.spaced("5 seconds")
)
```

### From Async Sources

```typescript
// From async iterable
const fromAsyncIterable = Stream.fromAsyncIterable(
  asyncGenerator(),
  (error) => new StreamError({ cause: error })
)

// From callback/event emitter
const fromCallback = Stream.async<number, never>((emit) => {
  const handler = (value: number) => emit.single(value)
  eventEmitter.on("data", handler)
  return Effect.sync(() => eventEmitter.off("data", handler))
})

// From queue
const fromQueue = Stream.fromQueue(queue)
```

### Generating Streams

```typescript
const naturals = Stream.unfold(1, (n) => Option.some([n, n + 1]))

const range = Stream.range(1, 100)

const repeated = Stream.repeat(Stream.succeed("ping")).pipe(
  Stream.take(5)
)
```

## Transforming Streams

### map - Transform Elements

```typescript
const doubled = numbers.pipe(
  Stream.map((n) => n * 2)
)

const enriched = users.pipe(
  Stream.mapEffect((user) => fetchProfile(user.id))
)

const parallel = items.pipe(
  Stream.mapEffect(process, { concurrency: 10 })
)
```

### filter - Select Elements

```typescript
const evens = numbers.pipe(
  Stream.filter((n) => n % 2 === 0)
)

const valid = items.pipe(
  Stream.filterEffect((item) => validate(item))
)
```

### flatMap - Nested Streams

```typescript
const expanded = numbers.pipe(
  Stream.flatMap((n) => Stream.make(n, n * 10, n * 100))
)
// 1, 10, 100, 2, 20, 200, ...
```

### take/drop

```typescript
const first5 = numbers.pipe(Stream.take(5))
const skip5 = numbers.pipe(Stream.drop(5))
const firstWhile = numbers.pipe(Stream.takeWhile((n) => n < 10))
const dropWhile = numbers.pipe(Stream.dropWhile((n) => n < 10))
```

## Combining Streams

### concat - Sequential

```typescript
const combined = Stream.concat(stream1, stream2)
// or
const combined = stream1.pipe(Stream.concat(stream2))
```

### merge - Interleaved

```typescript
// Interleave elements from both
const merged = Stream.merge(stream1, stream2)

// Merge multiple
const allMerged = Stream.mergeAll([s1, s2, s3], { concurrency: 3 })
```

### zip - Pair Elements

```typescript
const zipped = Stream.zip(names, ages)
// Stream<[string, number]>

// With function
const combined = Stream.zipWith(
  names,
  ages,
  (name, age) => ({ name, age })
)
```

### interleave

```typescript
const interleaved = Stream.interleave(stream1, stream2)
// a1, b1, a2, b2, ...
```

## Consuming Streams

### Running to Collection

```typescript
const array = yield* Stream.runCollect(numbers)

const first = yield* Stream.runHead(numbers)

const sum = yield* Stream.runFold(
  numbers,
  0,
  (acc, n) => acc + n
)
```

### Running for Effects

```typescript
yield* numbers.pipe(
  Stream.runForEach((n) => Effect.log(`Got: ${n}`))
)

yield* numbers.pipe(Stream.runDrain)
```

### Running to Sink

```typescript
import { Sink } from "effect"

const sum = yield* numbers.pipe(
  Stream.run(Sink.sum)
)

const array = yield* numbers.pipe(
  Stream.run(Sink.collectAll())
)
```

## Chunking

Streams process elements in chunks for efficiency:

```typescript
const chunked = numbers.pipe(
  Stream.grouped(10)
)

const processed = numbers.pipe(
  Stream.mapChunks((chunk) => Chunk.map(chunk, (n) => n * 2))
)

const rechunked = numbers.pipe(
  Stream.rechunk(100)
)
```

## Error Handling

```typescript
const safe = stream.pipe(
  Stream.catchAll((error) => Stream.succeed(fallbackValue))
)

const handled = stream.pipe(
  Stream.catchTag("NetworkError", (error) =>
    Stream.succeed(cachedValue)
  )
)

const resilient = stream.pipe(
  Stream.retry(Schedule.exponential("1 second"))
)

const withFallback = stream.pipe(
  Stream.orElse(() => fallbackStream)
)
```

## Resource Management

```typescript
// Stream with resource lifecycle
const fileStream = Stream.acquireRelease(
  Effect.sync(() => fs.openSync("data.txt", "r")),
  (fd) => Effect.sync(() => fs.closeSync(fd))
).pipe(
  Stream.flatMap((fd) =>
    Stream.repeatEffectOption(
      Effect.sync(() => {
        const buffer = Buffer.alloc(1024)
        const bytes = fs.readSync(fd, buffer)
        return bytes > 0 ? Option.some(buffer.slice(0, bytes)) : Option.none()
      })
    )
  )
)

// Scoped streams
const scoped = Stream.scoped(
  Effect.acquireRelease(openConnection, closeConnection)
)
```

## Sinks

Sinks consume stream elements:

```typescript
import { Sink } from "effect"

Sink.sum
Sink.count
Sink.head
Sink.last
Sink.collectAll()
Sink.forEach(f)

const maxSink = Sink.foldLeft(
  Number.NEGATIVE_INFINITY,
  (max, n: number) => Math.max(max, n)
)
```

## Common Patterns

### Batched Processing

```typescript
const batchProcess = stream.pipe(
  Stream.grouped(100),
  Stream.mapEffect((batch) =>
    Effect.tryPromise(() => api.processBatch(Chunk.toArray(batch)))
  )
)
```

### Rate Limiting

```typescript
const rateLimited = stream.pipe(
  Stream.throttle({
    units: 1,
    duration: "100 millis",
    strategy: "shape"
  })
)
```

### Debouncing

```typescript
const debounced = stream.pipe(
  Stream.debounce("500 millis")
)
```

### Windowing

```typescript
// Time-based windows
const windows = stream.pipe(
  Stream.groupedWithin(1000, "1 second")
)
```

## Best Practices

1. **Use chunking for efficiency** - Batch operations when possible
2. **Handle backpressure** - Use appropriate buffer strategies
3. **Clean up resources** - Use acquireRelease for external resources
4. **Process in parallel** - Use concurrency option in mapEffect
5. **Handle errors early** - Catch/retry before final consumption

## Additional Resources

For comprehensive stream documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Creating Streams" for stream construction
- "Consuming Streams" for running streams
- "Operations" for transformations
- "Error Handling in Streams" for error patterns
- "Resourceful Streams" for resource management
- "Sink" for custom sinks
