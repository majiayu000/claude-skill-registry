---
name: effect-streams-pipelines
description: Stream creation, transformation, sinks, batching, and resilience. Use when building data pipelines with concurrency and backpressure.
allowed-tools: Read, Grep, Glob, Edit, Write, mcp__effect-docs__effect_docs_search
---

# Streams & Pipelines

## When to use
- You’re building data pipelines with batching/backpressure
- You need controlled concurrency per element
- You must process large inputs with constant memory

## Create
```ts
const s = Stream.fromIterable(items)
```

## Transform
```ts
const out = s.pipe(
  Stream.mapEffect(processItem, { concurrency: 4 }),
  Stream.filter((a) => a.valid),
  Stream.grouped(100)
)
```

## Consume
```ts
yield* Stream.runDrain(out)
// or
const all = yield* Stream.runCollect(out)
```

## Resource-Safe
```ts
const fileLines = Stream.acquireRelease(open(), close).pipe(
  Stream.flatMap(readLines)
)
```

## Resilience
```ts
const resilient = s.pipe(
  Stream.mapEffect((x) => op(x).pipe(Effect.retry(retry)))
)
```

## Real-world snippet: Stream to S3 with progress and scoped background ticker
```ts
let downloadedBytes = 0

yield* Effect.gen(function* () {
  // background progress ticker
  yield* Effect.repeat(
    Effect.gen(function* () {
      const bytes = yield* Effect.succeed(downloadedBytes)
      yield* Effect.log(`Downloaded ${bytes}/${contentLength} bytes`)
    }),
    Schedule.forever.pipe(Schedule.delayed(() => "2 seconds"))
  ).pipe(Effect.delay("100 millis"), Effect.forkScoped)

  yield* s3.putObject(key,
    resp.stream.pipe(
      Stream.tap((chunk) => { downloadedBytes += chunk.length; return Effect.void })
    ),
    { contentLength }
  )
}).pipe(Effect.scoped)
```

## Guidance
- Prefer `Stream.mapEffect` with `concurrency` to control parallel work
- Use `grouped(n)` for batching network/DB operations
- Always model resource acquisition with `acquireRelease`

## Pitfalls
- Collecting massive streams into memory → prefer `runDrain` or chunked writes
- Doing blocking IO in transformations → keep operations effectful and non-blocking

## Cross-links
- Concurrency: pools and timeouts for per-item work
- Resources: scope/finalizers for pipeline resources
- EffectPatterns inspiration: https://github.com/PaulJPhilp/EffectPatterns

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Stream: `docs/effect-source/effect/src/Stream.ts`
- Sink: `docs/effect-source/effect/src/Sink.ts`
- Channel: `docs/effect-source/effect/src/Channel.ts`

### Example Searches
```bash
# Find Stream creation patterns
grep -F "fromIterable" docs/effect-source/effect/src/Stream.ts
grep -F "make" docs/effect-source/effect/src/Stream.ts
grep -F "fromEffect" docs/effect-source/effect/src/Stream.ts

# Study Stream transformations
grep -F "mapEffect" docs/effect-source/effect/src/Stream.ts
grep -F "filter" docs/effect-source/effect/src/Stream.ts
grep -F "grouped" docs/effect-source/effect/src/Stream.ts

# Find Stream consumption
grep -F "runDrain" docs/effect-source/effect/src/Stream.ts
grep -F "runCollect" docs/effect-source/effect/src/Stream.ts

# Look at Stream test examples
grep -F "Stream." docs/effect-source/effect/test/Stream.test.ts
```

### Workflow
1. Identify the Stream API you need (e.g., mapEffect, grouped)
2. Search `docs/effect-source/effect/src/Stream.ts` for the implementation
3. Study the types and pipeline patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

