---
name: ship-feature
description: Implement a feature safely end-to-end in this repository. Use when adding or changing functionality across backend, frontend, or MCP with required verification and documentation updates.
---

# Ship Feature

Use this workflow for medium or large implementation tasks.

## Steps
- Explore impacted modules first.
- Write a short implementation plan before editing.
- Implement smallest coherent diff that satisfies requirements.
- Run relevant verification commands.
- Update docs when commands, paths, architecture, or behavior changed.

## Required quality checks
- Keep API and websocket contracts stable unless intentionally changed.
- Keep destructive operations behind explicit guardrails.
- Avoid broad refactors in feature tickets unless requested.

## Finish checklist
- Tests/build/typecheck completed or explicitly reported as not run.
- Changed file set is scoped and intentional.
- User-facing docs updated if behavior changed.

## References
- Checklist template: `references/feature-checklist.md`
