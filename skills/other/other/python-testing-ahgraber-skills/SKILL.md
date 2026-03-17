---
name: python-testing
description: Use when writing or reviewing tests for Python behavior, contracts, async lifecycles, or reliability paths. Also use when tests are flaky, coupled to implementation details, missing regression coverage, slow to run, or when unclear what tests a change needs.
---

# Python Testing

## Overview

Test observable behavior and contracts, not internal implementation.
Keep unit tests fast, deterministic, and patched at module boundaries.

These are preferred defaults for common cases.
When a default conflicts with project constraints, suggest a better-fit alternative, call out tradeoffs, and note compensating controls.

## When to Use

- Writing or reviewing unit, integration, or reliability-sensitive tests.
- Tests are flaky, slow, or coupled to implementation details.
- Adding regression tests after a bugfix.
- Testing async lifecycles, cancellation, or cleanup paths.
- Unsure what test coverage a change needs.

**When NOT to use:**

- Pure data-shape or schema validation (see `python-types-contracts`).
- Production observability or monitoring concerns (see `python-runtime-operations`).
- Concurrency design decisions outside of test harnesses (see `python-concurrency-performance`).

## Quick Reference

- Test observable behavior, not internals.
- Keep unit tests fast and deterministic.
- Patch at module boundaries and import locations used by the unit under test.
- Add regression tests for bugfixes.
- Include timeout/retry/cancellation/cleanup coverage where relevant.

## Change-Specific Diagnostics

- Dependency updates: run `uv run pytest scripts/test_pypi_security_audit.py -v`
- Async-heavy lifecycle changes: run `pyleak` diagnostics.

## Common Mistakes

- **Mocking too deep** — patching internals instead of module-boundary seams makes tests brittle and coupled to implementation.
- **Testing the mock** — verifying mock call counts without asserting on observable output proves nothing about behavior.
- **Missing regression test** — fixing a bug without a test that reproduces it first; the bug will recur.
- **Non-deterministic time/order** — relying on wall-clock time or dict/set ordering instead of injecting clocks and sorting explicitly.
- **Skipping cleanup assertions** — verifying the happy path but never asserting that resources are released on failure or cancellation.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/testing-strategy.md`
- `references/pytest-practices.md`
- `references/async-and-concurrency-testing.md`
- `references/reliability-lifecycle-testing.md`
