---
name: aads-architect
description: Design architecture and contract changes for AADS-ULoRA with explicit module boundaries, compatibility strategy, and testable acceptance criteria. Use for interface, config-schema, data-flow, and cross-module redesign decisions before implementation.
---

# AADS Architect

## Workflow

1. Baseline current architecture.
- Inspect current modules and contract surfaces.
- Read `references/architecture-checklist.md`.

2. Define target architecture.
- Assign module responsibilities.
- Define interfaces, config keys, and data flow boundaries.

3. Analyze compatibility and migration.
- Identify backward-incompatible changes.
- Provide migration path and rollback direction.

4. Define acceptance criteria.
- Map each criterion to concrete tests/scripts.
- Include failure-mode checks.

5. Emit decision-complete design note.
- Provide chosen option, rejected alternatives, and risk posture.

## Output Contract

Return sections in this order:
1. Current architecture snapshot
2. Proposed design
3. Interface and contract deltas
4. Compatibility and migration plan
5. Acceptance criteria and validation map
6. Risks and rollback strategy
7. Implementation handoff notes

## References

- Use `references/architecture-checklist.md` for boundaries, contracts, and migration planning.
