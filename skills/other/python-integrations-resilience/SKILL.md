---
name: python-integrations-resilience
description: Use when building or reviewing external API integrations in Python — designing client boundaries, defining outbound reliability policy, or structuring contract tests. Also use when provider SDK details leak into domain logic, outbound calls lack timeout/retry policy, or failure paths are untested.
---

# Python Integrations and Resilience

## Overview

External integrations stay reliable when provider-specific details hide behind explicit client boundaries, and every outbound operation carries a defined reliability policy that is tested against both success and failure paths.

Treat these recommendations as preferred defaults.
When project constraints demand deviation, call out tradeoffs and compensating controls (tests, observability, rollback).

## When to Use

- Designing or reviewing client boundaries around external APIs or provider SDKs.
- Adding or auditing timeout, retry, or idempotency policy on outbound calls.
- Writing contract or resilience tests for provider integrations.
- Diagnosing contract drift between a client wrapper and the upstream provider.
- Refactoring domain logic that has coupled itself to a specific provider SDK.

### When NOT to Use

- Pure in-process library calls with no network or I/O boundary.
- Internal module interfaces that carry no external contract risk.
- Performance tuning of already-isolated integrations (see `python-concurrency-performance`).

## Quick Reference

- Hide provider-specific details behind explicit client boundaries.
- Keep domain logic isolated from provider SDK specifics.
- Require explicit timeout/retry/idempotency policy for every outbound operation.
- Test both contract mapping and failure behavior directly.

## Common Mistakes

- **Letting provider types cross the boundary** — returning raw SDK response objects into domain code couples the entire codebase to one provider.
- **Implicit or missing timeouts** — relying on library defaults (or no timeout at all) turns a slow upstream into a cascading failure.
- **Retrying non-idempotent calls** — retrying a POST without an idempotency key risks duplicate side effects.
- **Testing only the happy path** — skipping timeout, rate-limit, and malformed-response scenarios leaves the most likely production failures uncovered.
- **Hardcoding retry policy** — embedding backoff constants deep in client code prevents tuning without a redeploy.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/client-patterns.md`
- `references/request-reliability-policy.md`
- `references/resilience-and-contract-testing.md`
