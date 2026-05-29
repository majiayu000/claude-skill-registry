---
name: Batching and Caching
description: This skill should be used when the user asks about "Effect batching", "request batching", "Effect caching", "Cache", "Request", "RequestResolver", "Effect.cached", "Effect.cachedWithTTL", "automatic batching", "N+1 problem", "data loader pattern", "deduplication", or needs to understand how Effect optimizes API calls through batching and caching.
version: 1.0.0
---

# Batching and Caching in Effect

## Overview

Effect provides automatic optimization for API calls:

- **Batching** - Combine multiple requests into single API calls
- **Caching** - Avoid redundant requests with smart caching
- **Deduplication** - Prevent duplicate concurrent requests

This solves the N+1 query problem automatically.

## The Problem: N+1 Queries

```typescript
const program = Effect.gen(function* () {
  const todos = yield* getTodos()

  const owners = yield* Effect.forEach(
    todos,
    (todo) => getUserById(todo.ownerId),
    { concurrency: "unbounded" }
  )
})
```

Effect's batching transforms this into optimized batch calls.

## Request-Based Batching

### Step 1: Define Request Types

```typescript
import { Request } from "effect"

// Define request shape
interface GetUserById extends Request.Request<User, UserNotFound> {
  readonly _tag: "GetUserById"
  readonly id: number
}

// Create tagged constructor
const GetUserById = Request.tagged<GetUserById>("GetUserById")
```

### Step 2: Create Resolver

```typescript
import { RequestResolver, Effect } from "effect"

// Batched resolver - handles multiple requests at once
const GetUserByIdResolver = RequestResolver.makeBatched(
  (requests: ReadonlyArray<GetUserById>) =>
    Effect.gen(function* () {
      // Single batch API call
      const users = yield* Effect.tryPromise(() =>
        fetch("/api/users/batch", {
          method: "POST",
          body: JSON.stringify({ ids: requests.map((r) => r.id) })
        }).then((res) => res.json())
      )

      // Complete each request with its result
      yield* Effect.forEach(requests, (request, index) =>
        Request.completeEffect(
          request,
          Effect.succeed(users[index])
        )
      )
    })
)
```

### Step 3: Define Query

```typescript
const getUserById = (id: number) =>
  Effect.request(GetUserById({ id }), GetUserByIdResolver)
```

### Step 4: Use with Automatic Batching

```typescript
const program = Effect.gen(function* () {
  const todos = yield* getTodos()

  const owners = yield* Effect.forEach(
    todos,
    (todo) => getUserById(todo.ownerId),
    { concurrency: "unbounded" }
  )
})
```

## Resolver Types

### Standard Resolver (No Batching)

```typescript
const SingleUserResolver = RequestResolver.fromEffect(
  (request: GetUserById) =>
    Effect.tryPromise(() =>
      fetch(`/api/users/${request.id}`).then((r) => r.json())
    )
)
```

### Batched Resolver

```typescript
const BatchedUserResolver = RequestResolver.makeBatched(
  (requests: ReadonlyArray<GetUserById>) =>
    // Handle all requests in one call
    batchFetch(requests)
)
```

### Resolver with Context

```typescript
const UserResolverWithContext = RequestResolver.makeBatched(
  (requests: ReadonlyArray<GetUserById>) =>
    Effect.gen(function* () {
      // Access services from context
      const httpClient = yield* HttpClient
      const logger = yield* Logger

      yield* logger.info(`Batching ${requests.length} user requests`)

      return yield* httpClient.post("/api/users/batch", {
        ids: requests.map((r) => r.id)
      })
    })
)

// Provide context to resolver
const ContextualResolver = UserResolverWithContext.pipe(
  RequestResolver.provideContext(context)
)
```

## Caching

### Effect.cached - Memoize Effect Result

```typescript
import { Effect } from "effect"

const fetchConfig = Effect.promise(() =>
  fetch("/api/config").then((r) => r.json())
)

const cachedConfig = yield* Effect.cached(fetchConfig)

const config1 = yield* cachedConfig
const config2 = yield* cachedConfig
```

### Effect.cachedWithTTL - Time-Based Expiry

```typescript
const cachedUser = yield* Effect.cachedWithTTL(
  fetchCurrentUser,
  "5 minutes"
)

const user1 = yield* cachedUser
yield* Effect.sleep("6 minutes")
const user2 = yield* cachedUser
```

### Effect.cachedInvalidateWithTTL - Manual Invalidation

```typescript
const [cachedUser, invalidate] = yield* Effect.cachedInvalidateWithTTL(
  fetchCurrentUser,
  "5 minutes"
)

const user = yield* cachedUser
yield* invalidate
const freshUser = yield* cachedUser
```

## Cache Service

For more control, use the Cache service:

```typescript
import { Cache } from "effect"

const program = Effect.gen(function* () {
  const cache = yield* Cache.make({
    capacity: 100,
    timeToLive: "10 minutes",
    lookup: (userId: string) => fetchUser(userId)
  })

  const user1 = yield* cache.get("user-1")
  const user2 = yield* cache.get("user-1")

  const isCached = yield* cache.contains("user-1")

  yield* cache.invalidate("user-1")

  const stats = yield* cache.cacheStats
})
```

## Request Caching

Requests are automatically cached within a query context:

```typescript
const program = Effect.gen(function* () {
  const user1 = yield* getUserById(1)
  const user2 = yield* getUserById(1)

  const user3 = yield* getUserById(2)
})
```

### Disabling Request Caching

```typescript
const noCaching = getUserById(1).pipe(
  Effect.withRequestCaching(false)
)
```

### Custom Cache for Requests

```typescript
const customCache = yield* Request.makeCache({
  capacity: 1000,
  timeToLive: "30 minutes"
})

const program = getUserById(1).pipe(
  Effect.withRequestCache(customCache)
)
```

## Disabling Batching

```typescript
const noBatching = program.pipe(
  Effect.withRequestBatching(false)
)
```

## Complete Example

```typescript
import { Effect, Request, RequestResolver, Schema } from "effect"

// Error types
class UserNotFound extends Schema.TaggedError<UserNotFound>()(
  "UserNotFound",
  { id: Schema.Number }
) {}

// Request type
interface GetUserById extends Request.Request<User, UserNotFound> {
  readonly _tag: "GetUserById"
  readonly id: number
}
const GetUserById = Request.tagged<GetUserById>("GetUserById")

// Batched resolver
const UserResolver = RequestResolver.makeBatched(
  (requests: ReadonlyArray<GetUserById>) =>
    Effect.gen(function* () {
      const ids = requests.map((r) => r.id)

      const response = yield* Effect.tryPromise({
        try: () =>
          fetch("/api/users/batch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ids })
          }).then((r) => r.json() as Promise<User[]>),
        catch: () => new Error("Batch fetch failed")
      })

      yield* Effect.forEach(requests, (request, index) => {
        const user = response[index]
        return user
          ? Request.completeEffect(request, Effect.succeed(user))
          : Request.completeEffect(
              request,
              Effect.fail(new UserNotFound({ id: request.id }))
            )
      })
    })
)

// Query function
const getUserById = (id: number) =>
  Effect.request(GetUserById({ id }), UserResolver)

// Usage - automatically batched
const program = Effect.gen(function* () {
  const todos = yield* getTodos()

  const owners = yield* Effect.forEach(
    todos,
    (todo) => getUserById(todo.ownerId),
    { concurrency: "unbounded" }
  )

  return owners
})
```

## Best Practices

1. **Use batching for N+1 scenarios** - Especially with databases/APIs
2. **Cache expensive computations** - Use Effect.cached
3. **Set appropriate TTLs** - Balance freshness vs performance
4. **Use Request deduplication** - Automatic with Effect.request
5. **Batch at API boundaries** - Group related requests

## Additional Resources

For comprehensive batching and caching documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Batching" for complete batching guide
- "Caching" for caching patterns
- "Cache" for Cache service
- "Caching Effects" for Effect.cached patterns
