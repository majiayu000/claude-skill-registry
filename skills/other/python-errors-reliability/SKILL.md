---
name: python-errors-reliability
description: Use when designing error handling, retry policies, timeout behavior, or failure classification in Python. Also use when code swallows exceptions, loses error context across boundaries, has unbounded retries, silent failures, or lacks idempotency guarantees on retried writes.
---

# Python Errors and Reliability

## Overview

Design errors so callers can act and operators can diagnose quickly.
Treat these recommendations as preferred defaults — when a default conflicts with project constraints, suggest a better-fit alternative and call out tradeoffs and compensating controls.

## When to Use

- Implementing or reviewing timeout, deadline, or retry logic.
- Translating exceptions across layer boundaries (e.g., infra → domain).
- Classifying failures as retryable vs. permanent.
- Adding idempotency guarantees to retried writes.
- Diagnosing swallowed exceptions or silent failures in existing code.

**When NOT to use:**

- Pure data-transformation code with no I/O or failure modes.
- Simple validation that raises immediately with no translation needed.
- Performance tuning unrelated to failure handling (see `python-concurrency-performance`).

## Quick Reference

- Preserve cause chains at translation boundaries.
- Catch only what can be handled.
- Keep timeout/deadline policy explicit.
- Keep retry policy explicit and bounded.
- Classify retryable vs. permanent failures with explicit policy data.
- Keep idempotency expectations explicit for retried writes.

## Common Mistakes

- **Swallowing exceptions** — bare `except: pass` or `except Exception` with no logging loses diagnostic context.
- **Unbounded retries** — retrying without a maximum count or total deadline leads to cascading failures and resource exhaustion.
- **Dropping the cause chain** — raising a new exception without `from original` discards the root cause operators need for diagnosis.
- **Treating all errors as retryable** — retrying a 400 Bad Request or a validation error wastes resources and delays the real fix.
- **Implicit timeouts** — relying on library defaults (or no timeout at all) produces unpredictable latency under failure conditions.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/error-strategy.md`
- `references/retryability-classification.md`
- `references/retries-timeouts.md`
