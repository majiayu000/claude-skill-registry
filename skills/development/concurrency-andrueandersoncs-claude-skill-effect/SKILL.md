---
name: Concurrency
description: This skill should be used when the user asks about "Effect concurrency", "fibers", "Fiber", "forking", "Effect.fork", "Effect.forkDaemon", "parallel execution", "Effect.all concurrency", "Deferred", "Queue", "PubSub", "Semaphore", "Latch", "fiber interruption", "Effect.race", "Effect.raceAll", "concurrent effects", or needs to understand how Effect handles parallel and concurrent execution.
version: 1.0.0
---

# Concurrency in Effect

## Overview

Effect provides lightweight fiber-based concurrency:

- **Fibers** - Lightweight threads managed by Effect runtime
- **Structured concurrency** - Parent fibers supervise children
- **Safe interruption** - Clean cancellation with resource cleanup
- **Concurrent primitives** - Queue, Deferred, Semaphore, PubSub

## Basic Parallel Execution

### Effect.all with Concurrency

```typescript
import { Effect } from "effect"

const results = yield* Effect.all(
  [fetchUser(1), fetchUser(2), fetchUser(3)],
  { concurrency: "unbounded" }
)

const results = yield* Effect.all(tasks, { concurrency: 5 })

const results = yield* Effect.all(tasks)
```

### Effect.forEach with Concurrency

```typescript
const users = yield* Effect.forEach(
  userIds,
  (id) => fetchUser(id),
  { concurrency: 10 }
)
```

## Fibers

### Creating Fibers with fork

```typescript
const program = Effect.gen(function* () {
  const fiber = yield* Effect.fork(longRunningTask)

  yield* doOtherWork()

  const result = yield* Fiber.join(fiber)
})
```

### Fork Variants

```typescript
const fiber = yield* Effect.fork(task)

const fiber = yield* Effect.forkDaemon(task)

const fiber = yield* Effect.forkIn(scope)(task)

const fiber = yield* Effect.forkWithErrorHandler(task, onError)
```

### Fiber Operations

```typescript
import { Fiber } from "effect"

const result = yield* Fiber.join(fiber)

const exit = yield* Fiber.await(fiber)

yield* Fiber.interrupt(fiber)

const maybeResult = yield* Fiber.poll(fiber)
```

## Racing

### Effect.race - First to Complete

```typescript
const fastest = yield* Effect.race(
  fetchFromServer1(),
  fetchFromServer2()
)
```

### Effect.raceAll - Race Many

```typescript
const fastest = yield* Effect.raceAll([
  fetchFromCDN1(),
  fetchFromCDN2(),
  fetchFromCDN3()
])
```

### Effect.raceFirst - Include Failures

```typescript
const first = yield* Effect.raceFirst(task1, task2)
```

## Deferred - One-Time Promise

```typescript
import { Deferred } from "effect"

const program = Effect.gen(function* () {
  const deferred = yield* Deferred.make<string, never>()

  const fiber = yield* Effect.fork(
    Effect.gen(function* () {
      const value = yield* Deferred.await(deferred)
      yield* Effect.log(`Got: ${value}`)
    })
  )

  yield* Deferred.succeed(deferred, "Hello!")

  yield* Fiber.join(fiber)
})
```

## Queue - Concurrent Queue

```typescript
import { Queue } from "effect"

const program = Effect.gen(function* () {
  const queue = yield* Queue.bounded<number>(100)

  yield* Effect.fork(
    Effect.forEach(
      [1, 2, 3, 4, 5],
      (n) => Queue.offer(queue, n)
    )
  )

  const items = yield* Effect.forEach(
    Array.from({ length: 5 }),
    () => Queue.take(queue)
  )
})
```

### Queue Variants

```typescript
const bounded = yield* Queue.bounded<number>(100)

const unbounded = yield* Queue.unbounded<number>()

const dropping = yield* Queue.dropping<number>(100)

const sliding = yield* Queue.sliding<number>(100)
```

## PubSub - Publish/Subscribe

```typescript
import { PubSub } from "effect"

const program = Effect.gen(function* () {
  const pubsub = yield* PubSub.bounded<string>(100)

  const sub1 = yield* PubSub.subscribe(pubsub)
  const sub2 = yield* PubSub.subscribe(pubsub)

  yield* PubSub.publish(pubsub, "Hello!")

  const msg1 = yield* Queue.take(sub1)
  const msg2 = yield* Queue.take(sub2)
})
```

## Semaphore - Limit Concurrency

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const semaphore = yield* Effect.makeSemaphore(3)

  yield* Effect.forEach(
    tasks,
    (task) => semaphore.withPermits(1)(task),
    { concurrency: "unbounded" }
  )
})
```

## Latch - Coordination Point

```typescript
import { Latch } from "effect"

const program = Effect.gen(function* () {
  const latch = yield* Latch.make(false)

  yield* Effect.fork(
    Effect.forEach(
      workers,
      (worker) =>
        Effect.gen(function* () {
          yield* Latch.await(latch)
          yield* worker.start()
        }),
      { concurrency: "unbounded" }
    )
  )

  yield* Latch.open(latch)
})
```

## Interruption

### Interrupting Fibers

```typescript
const fiber = yield* Effect.fork(longTask)

yield* Fiber.interrupt(fiber)
```

### Uninterruptible Regions

```typescript
const critical = Effect.uninterruptible(
  Effect.gen(function* () {
    yield* beginTransaction()
    yield* performOperations()
    yield* commitTransaction()
  })
)
```

### Interruptible Within Uninterruptible

```typescript
const program = Effect.uninterruptible(
  Effect.gen(function* () {
    yield* criticalSetup()

    // This part can be interrupted
    yield* Effect.interruptible(longOperation)

    yield* criticalTeardown()
  })
)
```

## Supervision

Structured concurrency ensures child fibers are managed:

```typescript
const parent = Effect.gen(function* () {
  const child1 = yield* Effect.fork(task1)
  const child2 = yield* Effect.fork(task2)

  // If parent fails/interrupts, children are interrupted
  yield* failingOperation()
})
// child1 and child2 automatically interrupted
```

### Daemon Fibers

Escape supervision with daemon:

```typescript
const daemon = yield* Effect.forkDaemon(backgroundTask)
```

## Common Patterns

### Timeout with Fallback

```typescript
const withTimeout = task.pipe(
  Effect.timeout("5 seconds"),
  Effect.map(Option.getOrElse(() => defaultValue))
)
```

### Worker Pool

```typescript
const workerPool = Effect.gen(function* () {
  const semaphore = yield* Effect.makeSemaphore(numWorkers)

  return (task: Effect.Effect<A>) =>
    semaphore.withPermits(1)(task)
})
```

### Parallel with Error Collection

```typescript
const results = yield* Effect.all(
  tasks,
  {
    concurrency: "unbounded",
    mode: "either" // Collect all results
  }
)
```

## Best Practices

1. **Use Effect.all concurrency** for simple parallelism
2. **Use Semaphore** to limit concurrent operations
3. **Prefer structured concurrency** over daemon fibers
4. **Handle interruption** in long-running effects
5. **Use Queue for producer/consumer** patterns
6. **Use Deferred for one-time coordination**

## Additional Resources

For comprehensive concurrency documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Fibers" for fiber management
- "Basic Concurrency" for parallel execution
- "Deferred" for synchronization primitives
- "Queue" for concurrent queues
- "PubSub" for publish/subscribe
- "Semaphore" for concurrency limiting
