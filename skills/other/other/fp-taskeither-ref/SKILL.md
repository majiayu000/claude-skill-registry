---
name: fp-taskeither-ref
description: Quick reference for TaskEither. Use when user needs async error handling, API calls, or Promise-based operations that can fail.
version: 1.0.0
tags: [fp-ts, taskeither, async, promise, error-handling, quick-reference]
---

# TaskEither Quick Reference

TaskEither = async operation that can fail. Like `Promise<Either<E, A>>`.

## Create

```typescript
import * as TE from 'fp-ts/TaskEither'

TE.right(value)          // Async success
TE.left(error)           // Async failure
TE.tryCatch(asyncFn, toError)  // Promise → TaskEither
TE.fromEither(either)    // Either → TaskEither
```

## Transform

```typescript
TE.map(fn)               // Transform success value
TE.mapLeft(fn)           // Transform error
TE.flatMap(fn)           // Chain (fn returns TaskEither)
TE.orElse(fn)            // Recover from error
```

## Execute

```typescript
// TaskEither is lazy - must call () to run
const result = await myTaskEither()  // Either<E, A>

// Or pattern match
await pipe(
  myTaskEither,
  TE.match(
    (err) => console.error(err),
    (val) => console.log(val)
  )
)()
```

## Common Patterns

```typescript
import { pipe } from 'fp-ts/function'
import * as TE from 'fp-ts/TaskEither'

// Wrap fetch
const fetchUser = (id: string) => TE.tryCatch(
  () => fetch(`/api/users/${id}`).then(r => r.json()),
  (e) => ({ type: 'NETWORK_ERROR', message: String(e) })
)

// Chain async calls
pipe(
  fetchUser('123'),
  TE.flatMap(user => fetchPosts(user.id)),
  TE.map(posts => posts.length)
)

// Parallel calls
import { sequenceT } from 'fp-ts/Apply'
sequenceT(TE.ApplyPar)(
  fetchUser('1'),
  fetchPosts('1'),
  fetchComments('1')
)

// With recovery
pipe(
  fetchUser('123'),
  TE.orElse(() => TE.right(defaultUser)),
  TE.getOrElse(() => defaultUser)
)
```

## vs async/await

```typescript
// ❌ async/await - errors hidden
async function getUser(id: string) {
  try {
    const res = await fetch(`/api/users/${id}`)
    return await res.json()
  } catch (e) {
    return null  // Error info lost
  }
}

// ✅ TaskEither - errors typed and composable
const getUser = (id: string) => pipe(
  TE.tryCatch(() => fetch(`/api/users/${id}`), toNetworkError),
  TE.flatMap(res => TE.tryCatch(() => res.json(), toParseError))
)
```

Use TaskEither when you need **typed errors** for async operations.
