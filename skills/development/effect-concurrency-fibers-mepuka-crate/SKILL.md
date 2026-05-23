---
name: effect-concurrency-fibers
description: Concurrency with Effect.all, forEach concurrency, Fiber lifecycle, race and timeouts. Use for parallelizing tasks safely.
allowed-tools: Read, Grep, Glob, Edit, Write, mcp__effect-docs__effect_docs_search
---

# Concurrency & Fibers

## When to use
- Parallelizing independent work safely with limits
- Coordinating background tasks and lifecycle
- Racing operations for latency control

## Parallel Patterns
```ts
const results = yield* Effect.all(tasks, { concurrency: 10 })
```

```ts
const processed = yield* Effect.forEach(items, processItem, { concurrency: 5 })
```

## Fiber Lifecycle
```ts
const fiber = yield* Effect.fork(work)
const value = yield* Fiber.join(fiber)
yield* Fiber.interrupt(fiber)
```

## Racing / Timeouts
```ts
const fastest = yield* Effect.race(slow, fast)
const withTimeout = yield* Effect.timeout(operation, "5 seconds")
```

## Guidance
- Limit concurrency to protect resources
- Use `fork` for background loops; always manage interruption
- Prefer `Effect.all` for independent operations
 - Use `Effect.forEach` with `concurrency` for pools
 - Combine with retries and timeouts for resilient parallelism

## Pitfalls
- Unbounded concurrency can exhaust CPU/IO or hit rate limits
- Always interrupt background fibers on shutdown
- Don’t block inside fibers; keep work asynchronous/effectful

## Cross-links
- Errors & Retries: backoff + jitter for transient failures
- Streams & Pipelines: concurrent map over streams
- EffectPatterns inspiration: https://github.com/PaulJPhilp/EffectPatterns

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Effect: `docs/effect-source/effect/src/Effect.ts`
- Fiber: `docs/effect-source/effect/src/Fiber.ts`
- Duration: `docs/effect-source/effect/src/Duration.ts`

### Example Searches
```bash
# Find Effect.all and concurrency patterns
grep -F "Effect.all" docs/effect-source/effect/src/Effect.ts

# Find forEach with concurrency
grep -rF "forEach" docs/effect-source/effect/src/ | grep -F "concurrency"

# Study Fiber lifecycle operations
grep -F "export" docs/effect-source/effect/src/Fiber.ts | grep -E "fork|join|interrupt"

# Find race and timeout implementations
grep -F "race" docs/effect-source/effect/src/Effect.ts
grep -F "timeout" docs/effect-source/effect/src/Effect.ts
```

### Workflow
1. Identify the concurrency API you need (e.g., Effect.all, fork)
2. Search `docs/effect-source/effect/src/Effect.ts` for the implementation
3. Study the types and concurrency options
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

