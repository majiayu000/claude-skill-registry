---
name: effect-resources-scope
description: Resource safety with acquireRelease, Effect.scoped, and finalizers. Use when opening files, sockets, servers, or external handles.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Resource Management (Scope)

## Acquire/Release
```ts
const withConn = Effect.acquireRelease(
  Effect.sync(() => open()),
  (conn) => Effect.sync(() => close(conn))
).pipe(Effect.flatMap(use))
```

## Scoped
```ts
yield* Effect.scoped(
  Effect.gen(function* () {
    const h = yield* Effect.acquireRelease(acquire(), release)
    return yield* use(h)
  })
)
```

## Finalizers
```ts
yield* Effect.addFinalizer(() => cleanup)
```

## Ensuring
```ts
operation.pipe(Effect.ensuring(cleanup))
```

## Real-world snippet: wrap Promise APIs with typed errors and spans
```ts
const wrapS3Promise = <T>(promise: Promise<T> | Effect.Effect<Promise<T>>) =>
  Effect.gen(function* () {
    if (promise instanceof Promise) {
      return yield* Effect.tryPromise({ try: () => promise, catch: (cause) => new S3Error({ cause }) })
    }
    return yield* promise.pipe(
      Effect.flatMap((cb) =>
        Effect.tryPromise({ try: () => cb, catch: (cause) => new S3Error({ cause }) })
      )
    )
  }).pipe(Effect.catchTag("UnknownException", (cause) => new S3Error({ cause })))

// Usage with spans
const put = wrapS3Promise(client.send(new S3.PutObjectCommand(args))).pipe(
  Effect.withSpan("S3.putObject", { attributes: { key: args.Key } })
)
```

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Effect: `docs/effect-source/effect/src/Effect.ts`
- Scope: `docs/effect-source/effect/src/Scope.ts`

### Example Searches
```bash
# Find acquireRelease patterns
grep -F "acquireRelease" docs/effect-source/effect/src/Effect.ts

# Study scoped operations
grep -F "scoped" docs/effect-source/effect/src/Effect.ts
grep -F "addFinalizer" docs/effect-source/effect/src/Effect.ts

# Find ensuring patterns
grep -F "ensuring" docs/effect-source/effect/src/Effect.ts

# Look at Scope implementation
grep -F "export" docs/effect-source/effect/src/Scope.ts | grep -F "function"
```

### Workflow
1. Identify the resource management API you need (e.g., acquireRelease)
2. Search `docs/effect-source/effect/src/Effect.ts` for the implementation
3. Study the types and resource patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

