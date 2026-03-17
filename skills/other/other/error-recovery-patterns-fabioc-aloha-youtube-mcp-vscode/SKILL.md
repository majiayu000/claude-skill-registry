---
name: "Error Recovery Patterns Skill"
description: "What to do when things break."
applyTo: "**/*error*,**/*exception*,**/*retry*,**/*fallback*,**/*recovery*"
---

# Error Recovery Patterns Skill

> What to do when things break.

## Recovery Hierarchy

Prevent → Detect → Contain → Recover → Learn

## Retry Rules

| Retry | Don't Retry |
| ----- | ----------- |
| Network timeouts | Validation errors (400) |
| Rate limits (429) | Auth failures (401, 403) |
| Server errors (5xx) | Not found (404) |
| Connection refused | Business logic errors |

## Retry with Backoff

```typescript
const delay = baseDelay * Math.pow(2, attempt - 1);
const jitter = Math.random() * 0.3 * delay;
await sleep(delay + jitter);
```

## Circuit Breaker States

CLOSED → (failures > threshold) → OPEN → (timeout) → HALF-OPEN → (success) → CLOSED

## Fallback Patterns

| Pattern | Use Case |
| ------- | -------- |
| Default value | Config loading |
| Cached value | Data fetch failure |
| Degraded service | Non-critical features |

```typescript
const result = await primary().catch(() => fallback());
```

## Rollback Patterns

| Pattern | Use Case |
| ------- | -------- |
| DB transaction | Atomic operations |
| Saga (compensate) | Distributed transactions |
| Feature flag | Instant rollback |

## Error Boundaries

Contain failures to prevent cascade. Catch at component boundaries, log, show fallback UI.

## Synapses

See [synapses.json](synapses.json) for connections.
