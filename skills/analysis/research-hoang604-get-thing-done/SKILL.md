---
name: research
description: Trace execution paths and document how code actually behaves. Use when you need to understand how features work, walk through code flows, explain component behavior, trace where data comes from, understand relationships between components, or audit for orphaned events and dead code.
---

<principles>

## Zero Assumption

Never guess from names. `saveUser()` might delete records. READ THE CODE.

## Trust Threshold

Skip deep dive the implementation ONLY if docstring documents:

- What it does
- What it returns
- Side effects
- Exceptions

"Handles user data" → NOT trustworthy. Read it.

## Boundary

Stop at:

- Third-party libraries (assume documented behavior)
- Unrelated subsystems
- Full behavioral understanding

## Completeness

Investigation answers:

1. What does this do, step by step?
2. What dependencies does it interact with?
3. What are inputs, outputs, side effects?
4. What errors can occur?

## No Teleportation

Data doesn't appear out of nowhere. Every piece of data must have a traceable path:

- **Origin:** Where was it created?
- **Path:** What components touch it?
- **Destination:** Where is it consumed?

If data appears in component B but you can't trace it from A → investigation is **INCOMPLETE**.

Corollaries:

- Every WRITE needs a READER
- Every READ traces back to a WRITE
- Every EMIT needs a HANDLER

</principles>

<techniques>

## Dependency Classification

| Type           | Action                      |
| -------------- | --------------------------- |
| Core Logic     | MUST read fully             |
| Infrastructure | Read integration patterns   |
| Utilities      | Read if behavior unclear    |
| Third-Party    | Assume standard, don't read |

## Data Lineage

For every data artifact:

- **Origin:** Where created?
- **Path:** What components touch it?
- **Destination:** Where consumed?
- **Orphan check:** Every event has handler? Every write has reader?

</techniques>

<checklists>

## Before Finishing

- [ ] All entry points traced
- [ ] No "probably" or "likely" in findings
- [ ] Completeness questions answered
- [ ] No orphaned events/writes

</checklists>

<prohibitions>

- NEVER assume behavior — read it
- NEVER be vague — "Handles data" forbidden
- NEVER leave unknowns — resolve or ask

</prohibitions>
