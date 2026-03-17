---
name: python-types-contracts
description: Use when defining or evolving public interfaces, schema boundaries, or pydantic usage in Python. Also use when annotations are missing on public APIs, pydantic models appear everywhere instead of at trust boundaries, contract changes lack migration guidance, or Any/object types are overused across module boundaries.
---

# Python Types and Contracts

## Overview

Treat type hints as interface design, not decoration.
Focus on explicit contracts, stable public APIs, and boundary-safe modeling.

These are preferred defaults for common cases, not universal rules.
When a default conflicts with project constraints, suggest a better-fit alternative and explain tradeoffs and compensating controls.

## When to Use

- Public API signatures lack type annotations or use overly broad types.
- Pydantic models are scattered throughout internal logic instead of at trust boundaries.
- Contract changes risk breaking downstream consumers without migration paths.
- Interfaces accept `Any`, `object`, or untyped dicts where narrower types apply.
- Schema boundaries between layers (API, DB, domain) are implicit or inconsistent.
- Adding or evolving protocols, abstract base classes, or structural subtyping.

**When NOT to use:**

- Pure implementation-level code with no public interface.
- Throwaway scripts or one-off data munging where type rigor adds no value.
- Performance-critical inner loops where typing overhead matters more than safety.

## Quick Reference

- Type public APIs and keep contracts explicit.
- Prefer narrow interfaces and boundary protocols over broad parameter types.
- Use pydantic at trust boundaries by default, not everywhere.
- Make compatibility and migration impact explicit for any contract change.
- Favor `Protocol` for structural subtyping over deep inheritance hierarchies.
- Return concrete types from public functions; accept protocols or unions as inputs.

## Common Mistakes

- **Typing everything identically.**
  Internal helpers don't need the same rigor as public APIs.
  Over-annotating private code adds noise without safety.
- **Pydantic everywhere.**
  Using pydantic models for internal data flow instead of reserving them for validation at trust boundaries (API ingress, config loading, external data).
- **Broad return types.**
  Returning `Any` or `dict` from public functions forces callers to guess structure.
  Return concrete types or TypedDicts.
- **Breaking contracts silently.**
  Changing function signatures, removing fields, or narrowing accepted types without versioning, deprecation warnings, or migration notes.
- **Ignoring `None`.**
  Omitting `Optional` or union with `None` when a value can legitimately be absent, hiding null-safety bugs until runtime.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/typing-policy.md`
- `references/contract-evolution.md`
- `references/pydantic-boundaries.md`
