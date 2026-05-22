---
name: effect-queues-background
description: Queue and PubSub patterns, background fibers, and graceful shutdown. Use for decoupling producers/consumers.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Queues, PubSub & Background

## When to use
- Decoupling producers/consumers with backpressure
- Broadcasting events to multiple subscribers
- Running background loops with graceful shutdown

## Queue (bounded)
```ts
import { Queue } from "effect"
const q = yield* Queue.bounded<string>(32)
yield* Queue.offer(q, "job")
const job = yield* Queue.take(q)
```

## PubSub (broadcast)
```ts
import { PubSub } from "effect"
const ps = yield* PubSub.bounded<string>(32)
yield* PubSub.publish(ps, "evt")
```

## Background Fiber
```ts
const fiber = yield* Effect.fork(loop)
yield* Fiber.interrupt(fiber)
```

## Guidance
- Prefer bounded queues to apply natural backpressure
- Use multiple workers by forking consumers
- Ensure background fibers are interrupted during shutdown

## Pitfalls
- Unbounded queues lead to memory growth
- Silent background failures → add logging/metrics

## Cross-links
- Concurrency for pools and interruption
- Time/Logging for observability of background tasks

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Queue: `docs/effect-source/effect/src/Queue.ts`
- PubSub: `docs/effect-source/effect/src/PubSub.ts`
- Fiber: `docs/effect-source/effect/src/Fiber.ts`

### Example Searches
```bash
# Find Queue patterns
grep -F "bounded" docs/effect-source/effect/src/Queue.ts
grep -F "offer" docs/effect-source/effect/src/Queue.ts
grep -F "take" docs/effect-source/effect/src/Queue.ts

# Study PubSub operations
grep -F "publish" docs/effect-source/effect/src/PubSub.ts
grep -F "subscribe" docs/effect-source/effect/src/PubSub.ts

# Find background fiber patterns
grep -F "fork" docs/effect-source/effect/src/Fiber.ts
grep -F "interrupt" docs/effect-source/effect/src/Fiber.ts

# Look at Queue test examples
grep -F "Queue." docs/effect-source/effect/test/Queue.test.ts
```

### Workflow
1. Identify the Queue or PubSub API you need
2. Search `docs/effect-source/effect/src/Queue.ts` or `PubSub.ts` for the implementation
3. Study the types and backpressure patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

