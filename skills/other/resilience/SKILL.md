---
name: resilience
description: "Apply fault-tolerance patterns to outbound calls and async consumers (timeouts, retries with backoff+jitter, circuit breakers, bulkheads, idempotency keys, graceful degradation). Use when a service calls external dependencies, processes queues/events, or needs hardening against partial failures and flaky upstreams. NOT for diagnosing existing failures (use debug); NOT for multi-service architecture decisions (use architecture)."
metadata: {"stage":"Harden","tags":["fault-tolerance","timeouts","retries","idempotency","circuit-breaker","backoff","jitter","graceful-degradation","load-shedding"],"aliases":["fault-tolerance","retry","timeout","circuit-breaker","bulkhead","backoff","idempotent"]}
---

# Resilience

## Overview

Make I/O failures boring: set explicit timeouts, retry safely, keep operations idempotent, and prevent cascades with circuit breakers and bulkheads.

Enterprise systems fail partially (timeouts, 5xx, queue lag). Resilience patterns make those failures bounded and observable.

## Workflow

1. Identify the I/O boundary: HTTP, gRPC, DB, cache, queue/stream, third-party API.
2. Define the failure model:
   - which failures are expected/transient vs permanent
   - what “success” means under degradation (fallback? partial data? fail fast?)
3. Apply patterns in this order:
   1. **Timeouts + cancellation**
   2. **Idempotency** (especially if retries exist)
   3. **Retries with backoff + jitter** (bounded)
   4. **Circuit breaker** (when a dependency is unhealthy)
   5. **Bulkheads / concurrency limits** (to protect your own resources)
4. Add observability (retry counts, breaker state, queue lag, error codes).
5. Add consumer-visible tests for semantics; add a local smoke test for failure modes.

## Chooser (What To Use Where)

- **Inbound HTTP/gRPC**: timeouts for downstream calls; guardrails; load shedding; return stable error codes.
- **Outbound HTTP/gRPC clients**: timeouts + bounded retries + (optional) circuit breaker + concurrency limit.
- **DB/Redis**: short timeouts; limited retries (often none); concurrency limits/pools; backpressure.
- **Message consumers**: idempotency + dedupe; retry with backoff; dead-letter strategy; track lag.

## Clarifying Questions

- What I/O boundary is involved (HTTP client, gRPC client, DB, cache, queue/stream, third-party API)?
- What failures are expected/transient vs permanent for this dependency?
- Is the operation idempotent? If not, can you add an idempotency key?
- What is the time budget for this operation (how long can the caller wait)?
- What should happen under degradation (fail fast, return stale/cached data, partial results, fallback)?
- Are there existing resilience patterns in the codebase (retry helpers, circuit breaker, timeout wrappers)?

## Core Patterns (Opinionated Defaults)

### Timeouts + cancellation (mandatory)

- Every outbound call has a timeout and participates in cancellation.
- Use a single “time budget” per request; don’t let retries exceed it.

### Retries (bounded, only when safe)

- Retry only for **transient** failures (timeouts, connection resets, 429/503 depending on semantics).
- Use exponential backoff + jitter to avoid synchronized retry storms.
- Cap attempts and cap total delay; consider a retry budget per request.

### Idempotency (required when retries exist)

- Never retry a non-idempotent operation unless the server-side operation is idempotent (idempotency key / dedupe).
- For message consumers, assume at-least-once delivery: handle duplicates safely.

### Circuit breaker (for flakey/unhealthy dependencies)

- Open the breaker when failure rate exceeds a threshold; fail fast for a cooldown period.
- Half-open to probe recovery; close after successful probes.
- Expose breaker state as metrics and log transitions.

### Bulkheads / concurrency limits (protect yourself)

- Limit concurrent work per dependency to avoid saturating your process.
- Prefer per-dependency limits (bulkheads) over one global limit.

## Minimal TypeScript Snippets

Backoff with jitter:

```ts
export function backoffDelayMs(
  attempt: number,
  baseMs = 100,
  maxMs = 2_000,
): number {
  const exp = Math.min(maxMs, baseMs * 2 ** attempt);
  const jitter = 0.5 + Math.random(); // [0.5, 1.5)
  return Math.round(exp * jitter);
}
```

## Testing / Verification

- Timeouts: request returns a stable timeout error within the budget.
- Retries: attempts are bounded; retryable vs non-retryable errors are classified correctly.
- Idempotency: duplicate request/message does not double-apply side effects.
- Bulkheads: dependency overload doesn’t starve unrelated work.
- Breaker: opens under repeated failures and closes after recovery.

## References

- Deeper checklists: [`references/checklists.md`](references/checklists.md)
- TypeScript snippets: [`references/snippets/typescript.md`](references/snippets/typescript.md)
- Related patterns: [`Circuit Breaker`](../architecture/references/circuit-breaker.md), [`Idempotent Consumer`](../architecture/references/idempotent-consumer.md), [`Transactional outbox`](../architecture/references/transactional-outbox.md)
- Instrumentation guidance: [`observability`](../observability/SKILL.md)
- Typed error semantics and explicit lifetimes: [`typescript`](../typescript/SKILL.md)
- Wrapping clients: [`patterns-structural`](../patterns-structural/SKILL.md) (Proxy/Decorator)

## Output Template

When applying this skill, return:

- The failure model assumptions (retryable errors, idempotency strategy, time budget).
- The minimal code changes (timeouts, retry loop, breaker/bulkhead wrapper).
- The verification steps (tests + how to simulate failure locally).
