---
name: python-design-modularity
description: Use when designing module boundaries, planning refactors, or reviewing architecture in Python codebases. Also use when facing tangled dependencies, god classes, deep inheritance hierarchies, unclear ownership, or risky structural changes.
---

# Python Design and Modularity

## Overview

Readability-first design with explicit module contracts.
Keep control flow, data movement, and ownership boundaries visible so code stays maintainable and safe to change.

Treat these recommendations as preferred defaults.
When a default conflicts with project constraints, suggest a better-fit alternative and call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## When to Use

- Restructuring modules, packages, or ownership boundaries
- Breaking apart god classes or deeply nested hierarchies
- Choosing between composition and inheritance
- Applying Functional Core / Imperative Shell separation
- Planning a refactor that touches multiple modules
- Reviewing code for readability or architectural clarity

**When NOT to use:**

- Pure performance optimization — see `python-concurrency-performance`
- Error handling and resilience patterns — see `python-errors-reliability`
- Type contracts and protocol design — see `python-types-contracts`
- One-off script or throwaway code with no maintenance horizon

## Quick Reference

- Keep control flow and data movement explicit.
- Keep module ownership and invariants explicit.
- Prefer composition by default.
- Apply Functional Core / Imperative Shell where it improves testability and separation of concerns.
- Separate behavior changes from structural refactors — never mix in the same commit.

## Common Mistakes

- **Refactoring behavior and structure simultaneously** — conflates two kinds of risk, makes rollback harder, and obscures review.
  Do one, then the other.
- **Reaching for inheritance first** — deep hierarchies couple unrelated concerns and make reasoning non-local.
  Default to composition; inherit only when the "is-a" relationship is genuinely stable.
- **Hidden module coupling** — importing implementation details across boundaries creates invisible contracts.
  Expose explicit public APIs and keep internals private.
- **Premature abstraction** — extracting a shared interface before the second or third concrete use leads to wrong abstractions that are expensive to undo.
  Wait for duplication to reveal the real seam.
- **Ignoring the Functional Core / Imperative Shell split** — mixing I/O with business logic makes unit testing painful and increases the blast radius of changes.
  Push side effects to the edges.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/design-rules.md`
- `references/readability-and-complexity.md`
- `references/module-boundaries.md`
- `references/functional-core-shell.md`
- `references/refactor-guidelines.md`
