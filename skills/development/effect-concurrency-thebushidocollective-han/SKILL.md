---
name: effect-concurrency
description: Use when Effect concurrency patterns including fibers, fork, join, parallel execution, and race conditions. Use for concurrent operations in Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Concurrency

Master concurrent execution in Effect using fibers. This skill covers forking,
joining, interruption, parallel execution, and advanced concurrency patterns for
building high-performance Effect applications.

## Fibers Fundamentals

### What are Fibers?

Fibers are lightweight virtual threads that execute effects concurrently:

```typescript
import { Effect, Fiber } from "effect"

// Every effect runs on a fiber
const effect = Effect.succeed(42)
// When run, this executes on a fiber

// Effects are descriptions - fibers are executions
// Effect: lazy, immutable description
// Fiber: running execution with state
```

### Forking Effects

Create independent concurrent fibers:

```typescript
import { Effect, Fiber } from "effect"

const task = Effect.gen(function* () {
  yield* Effect.sleep("1 second")
  yield* Effect.log("Task completed")
  return 42
})

const program = Effect.gen(function* () {
  // Fork creates a new fiber
  const fiber = yield* Effect.fork(task)
  // fiber: RuntimeFiber<number, never>

  yield* Effect.log("Main fiber continues")

  // Join waits for fiber to complete
  const result = yield* Fiber.join(fiber)
  yield* Effect.log(`Result: ${result}`)

  return result
})
```

### Fiber Operations

```typescript
import { Effect, Fiber } from "effect"

const program = Effect.gen(function* () {
  const fiber = yield* Effect.fork(longRunningTask)

  // Join - wait for result
  const result = yield* Fiber.join(fiber)

  // Await - get Exit value (success/failure/interruption)
  const exit = yield* Fiber.await(fiber)

  // Interrupt - cancel execution
  yield* Fiber.interrupt(fiber)

  // Poll - check if complete (non-blocking)
  const status = yield* Fiber.poll(fiber)
})
```

## Parallel Execution

### Effect.all - Run Multiple Effects

```typescript
import { Effect } from "effect"

// Parallel execution (default)
const program = Effect.gen(function* () {
  const results = yield* Effect.all([
    fetchUser("1"),
    fetchUser("2"),
    fetchUser("3")
  ])
  // All requests run concurrently
  return results
})

// Sequential execution
const sequential = Effect.gen(function* () {
  const results = yield* Effect.all([
    fetchUser("1"),
    fetchUser("2"),
    fetchUser("3")
  ], { concurrency: 1 })
  return results
})

// Limited concurrency
const limited = Effect.gen(function* () {
  const results = yield* Effect.all(
    Array.from({ length: 100 }, (_, i) => fetchUser(`${i}`)),
    { concurrency: 10 } // Max 10 concurrent
  )
  return results
})
```

### Effect.all with Batching

```typescript
import { Effect } from "effect"

// Batching for efficiency
const batchFetch = Effect.gen(function* () {
  const userIds = Array.from({ length: 1000 }, (_, i) => `${i}`)

  const results = yield* Effect.all(
    userIds.map(id => fetchUser(id)),
    {
      concurrency: 50, // 50 concurrent requests
      batching: true   // Enable batching optimization
    }
  )

  return results
})
```

### Effect.forEach - Concurrent Iteration

```typescript
import { Effect } from "effect"

const processUsers = (userIds: string[]) =>
  Effect.forEach(
    userIds,
    (id) => Effect.gen(function* () {
      const user = yield* fetchUser(id)
      const processed = yield* processUser(user)
      return processed
    }),
    { concurrency: "unbounded" } // No limit
  )

// With concurrency limit
const processUsersLimited = (userIds: string[]) =>
  Effect.forEach(
    userIds,
    (id) => processUser(id),
    { concurrency: 10 }
  )
```

## Racing Effects

### Effect.race - First to Complete

```typescript
import { Effect } from "effect"

const fetchWithFallback = (id: string) =>
  Effect.race(
    fetchFromPrimaryDb(id),
    fetchFromSecondaryDb(id)
  )
// Returns whichever completes first

// Racing multiple effects
const fastestSource = Effect.race(
  fetchFromSource1(),
  fetchFromSource2(),
  fetchFromSource3()
)
```

### Effect.raceAll - Race Multiple Effects

```typescript
import { Effect } from "effect"

const sources = [
  fetchFromSource1(),
  fetchFromSource2(),
  fetchFromSource3()
]

// First to succeed wins
const fastest = Effect.raceAll(sources)
```

### Timeout Racing

```typescript
import { Effect } from "effect"

const withTimeout = <A, E, R>(
  effect: Effect.Effect<A, E, R>,
  duration: Duration.Duration
) =>
  Effect.race(
    effect,
    Effect.sleep(duration).pipe(
      Effect.andThen(Effect.fail({ _tag: "Timeout" }))
    )
  )

const program = Effect.gen(function* () {
  const result = yield* withTimeout(
    slowOperation(),
    Duration.seconds(5)
  )
  return result
})
```

## Interruption

### Fiber Interruption

```typescript
import { Effect, Fiber } from "effect"

const program = Effect.gen(function* () {
  const fiber = yield* Effect.fork(longRunningTask)

  // Cancel after 1 second
  yield* Effect.sleep("1 second")
  yield* Fiber.interrupt(fiber)

  yield* Effect.log("Task cancelled")
})

// Automatic interruption on parent exit
const autoInterrupt = Effect.gen(function* () {
  const fiber = yield* Effect.fork(infiniteLoop)
  // fiber will be interrupted when this effect completes
})
```

### Uninterruptible Regions

```typescript
import { Effect } from "effect"

const criticalSection = Effect.gen(function* () {
  // This region cannot be interrupted
  yield* Effect.uninterruptible(
    Effect.gen(function* () {
      yield* beginTransaction()
      yield* updateDatabase()
      yield* commitTransaction()
    })
  )
})

// Interruptible regions within uninterruptible
const mixed = Effect.uninterruptible(
  Effect.gen(function* () {
    yield* criticalOperation1()

    // Allow interruption here
    yield* Effect.interruptible(
      nonCriticalOperation()
    )

    yield* criticalOperation2()
  })
)
```

## Daemon Fibers

### Fork Daemon - Independent Fibers

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  // Regular fork - interrupted when parent exits
  const regularFiber = yield* Effect.fork(task)

  // Daemon fork - survives parent exit
  const daemonFiber = yield* Effect.forkDaemon(backgroundTask)

  // Parent exits, regularFiber interrupted, daemonFiber continues
})

// Background worker example
const startBackgroundWorker = Effect.gen(function* () {
  yield* Effect.forkDaemon(
    Effect.gen(function* () {
      while (true) {
        yield* processQueue()
        yield* Effect.sleep("1 second")
      }
    })
  )
})
```

## Scoped Concurrency

### Effect.forkScoped - Fiber Cleanup

```typescript
import { Effect, Scope } from "effect"

const program = Effect.gen(function* () {
  yield* Effect.scoped(
    Effect.gen(function* () {
      // Fibers are tied to scope
      const fiber1 = yield* Effect.forkScoped(task1)
      const fiber2 = yield* Effect.forkScoped(task2)

      // Do work
      yield* doWork()

      // Scope exit automatically interrupts fibers
    })
  )
  // fiber1 and fiber2 are interrupted here
})
```

### Fork In Scope

```typescript
import { Effect } from "effect"

const managedConcurrency = Effect.gen(function* () {
  const scope = yield* Scope.make()

  // Fork in specific scope
  const fiber = yield* Effect.forkIn(task, scope)

  // Work continues
  yield* doWork()

  // Close scope, interrupt fiber
  yield* Scope.close(scope, Exit.succeed(undefined))
})
```

## Advanced Patterns

### Worker Pool

```typescript
import { Effect, Queue } from "effect"

interface Task {
  id: string
  data: unknown
}

const createWorkerPool = (workers: number) =>
  Effect.gen(function* () {
    const queue = yield* Queue.bounded<Task>(100)

    // Start workers
    const workerFibers = yield* Effect.all(
      Array.from({ length: workers }, () =>
        Effect.fork(
          Effect.forever(
            Effect.gen(function* () {
              const task = yield* Queue.take(queue)
              yield* processTask(task)
            })
          )
        )
      )
    )

    return {
      submit: (task: Task) => Queue.offer(queue, task),
      shutdown: () =>
        Effect.all(
          workerFibers.map(fiber => Fiber.interrupt(fiber))
        )
    }
  })
```

### Parallel Map-Reduce

```typescript
import { Effect, Chunk } from "effect"

const parallelMapReduce = <A, B, E, R>(
  items: A[],
  map: (item: A) => Effect.Effect<B, E, R>,
  reduce: (acc: B, item: B) => B,
  initial: B,
  concurrency: number
) =>
  Effect.gen(function* () {
    const mapped = yield* Effect.forEach(
      items,
      map,
      { concurrency }
    )

    return mapped.reduce(reduce, initial)
  })
```

### Request Deduplication

```typescript
import { Effect, Request, RequestResolver } from "effect"

interface GetUser extends Request.Request<User, UserNotFound> {
  readonly _tag: "GetUser"
  readonly id: string
}

const GetUserResolver = RequestResolver.makeBatched(
  (requests: GetUser[]) =>
    Effect.gen(function* () {
      const ids = requests.map(r => r.id)
      const users = yield* fetchUsersBatch(ids)

      // Resolve all requests
      return Effect.forEach(requests, (request) => {
        const user = users.find(u => u.id === request.id)
        return user
          ? Request.complete(request, user)
          : Request.fail(request, { _tag: "UserNotFound", id: request.id })
      })
    })
)

// Multiple concurrent requests for same ID deduplicated
const program = Effect.gen(function* () {
  const results = yield* Effect.all([
    Effect.request(GetUser({ id: "1" }), GetUserResolver),
    Effect.request(GetUser({ id: "1" }), GetUserResolver),
    Effect.request(GetUser({ id: "1" }), GetUserResolver)
  ])
  // Only one actual fetch for ID "1"
})
```

## Best Practices

1. **Use Effect.all for Parallel Work**: Don't fork manually when Effect.all
   suffices.

2. **Limit Concurrency**: Set appropriate concurrency limits to avoid resource
   exhaustion.

3. **Handle Interruption**: Ensure cleanup code runs in uninterruptible regions.

4. **Use Scoped Forks**: Tie fiber lifetime to scopes for automatic cleanup.

5. **Avoid Infinite Loops**: Use Effect.forever with sleep for background tasks.

6. **Batch Requests**: Use request resolvers to batch and deduplicate.

7. **Timeout Long Operations**: Add timeouts to prevent hanging.

8. **Monitor Fiber Status**: Use Fiber.await and Fiber.poll for status checks.

9. **Use Daemon Sparingly**: Only fork daemons when truly independent.

10. **Test Concurrent Code**: Write tests for race conditions and interruption.

## Common Pitfalls

1. **Forgetting to Join**: Forking without joining loses results.

2. **No Concurrency Limits**: Unbounded concurrency can exhaust resources.

3. **Not Handling Interruption**: Missing cleanup in interruptible regions.

4. **Race Conditions**: Sharing mutable state between fibers.

5. **Deadlocks**: Circular dependencies between fibers.

6. **Ignoring Failures**: Not checking fiber exit status.

7. **Memory Leaks**: Daemon fibers that never terminate.

8. **Over-Forking**: Creating too many fibers unnecessarily.

9. **Missing Timeouts**: Long-running operations without limits.

10. **Wrong Execution Mode**: Using sequential when parallel is intended.

## When to Use This Skill

Use effect-concurrency when you need to:

- Execute multiple operations in parallel
- Build high-performance data pipelines
- Handle concurrent user requests
- Implement background workers
- Race multiple data sources
- Add timeouts to operations
- Build concurrent job processors
- Manage fiber lifecycles
- Implement request deduplication
- Optimize throughput with batching

## Resources

### Official Documentation

- [Concurrency](https://effect.website/docs/concurrency/)
- [Fibers](https://effect.website/docs/concurrency/fibers)
- [Concurrency Options](https://effect.website/docs/concurrency/concurrency-options)
- [Racing](https://effect.website/docs/concurrency/racing)
- [Interruption](https://effect.website/docs/concurrency/interruption)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-resource-management - Resource cleanup with scopes
