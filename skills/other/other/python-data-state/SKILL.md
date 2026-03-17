---
name: python-data-state
description: Use when designing data ownership, validation boundaries, consistency models, or configuration strategy in Python. Also use when encountering unclear ownership across modules, shared mutable state leaking between layers, validation gaps at ingress, cross-module transactional coupling, or config drift between environments.
---

# Python Data and State

## Overview

Every data bug traces back to an unclear answer to three questions: who owns this data, where is it validated, and how far does it travel?
This skill encodes boundary-first thinking — make ownership explicit, validate at the edge, and minimize what crosses a boundary.

Treat these defaults as starting points.
When project constraints demand deviation, call out tradeoffs and compensating controls (tests, observability, rollback).

## When to Use

- Data ownership is ambiguous or split across modules.
- Validation logic is scattered or duplicated instead of concentrated at ingress.
- Mutable state is shared across module or layer boundaries.
- Multiple modules participate in a single transaction.
- Configuration is stringly-typed, read lazily, or inconsistent across environments.
- Lifecycle of a data object (creation, transformation, persistence) spans unclear boundaries.

### When NOT to Use

- Pure algorithmic or computational logic with no shared state.
- Prototypes or throwaway scripts where boundary discipline adds no value.
- UI/presentation-layer styling decisions with no data modeling impact.

## Quick Reference

- Make module ownership and invariants explicit.
- Validate at ingress and normalize before domain decisions.
- Share minimal data across boundaries — prefer narrow, typed interfaces.
- Avoid cross-module transactions by default; if unavoidable, isolate coordination logic.
- Keep configuration typed, environment-driven, and startup-validated.

## Common Mistakes

- **Validating deep inside the call stack** — pushing checks into domain logic instead of catching bad data at the boundary where it enters.
- **Exposing internal models across module boundaries** — sharing ORM objects or rich domain models instead of narrow DTOs or typed dicts.
- **Relying on implicit ownership** — assuming "whoever wrote it last" owns the data, leading to conflicting mutations and no single source of truth.
- **Lazy, untyped config reads** — calling `os.getenv()` at point-of-use with string defaults, so missing or malformed config surfaces as a runtime surprise instead of a startup failure.
- **Wrapping unrelated modules in a shared transaction** — coupling independent data stores for perceived consistency, creating hidden rollback complexity and contention.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-data-state`.

## References

- `references/data-lifecycle.md`
- `references/consistency-boundaries.md`
- `references/configuration.md`
