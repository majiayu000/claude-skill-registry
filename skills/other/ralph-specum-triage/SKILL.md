---
name: ralph-specum-triage
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-triage`, or explicitly asks Ralph Specum in Codex to triage a large effort into multiple specs.
metadata:
  surface: helper
  action: triage
---

# Ralph Specum Triage

Use this for large goals that should be decomposed into multiple dependency-aware specs.

## Contract

- Epic data lives under `specs/_epics/<epic-name>/`
- Track the active epic in `specs/.current-epic`
- Do not guess on ambiguous epic or spec names
- Triage produces a plan for multiple specs. It does not implement them

## Action

1. Check `specs/.current-epic`. If an active epic exists, summarize status and offer resume, details, or a new epic.
2. Resolve or create the epic directory and initialize `research.md`, `epic.md`, `.progress.md`, and `.epic-state.json` as needed.
3. Run the current triage flow in four stages:
   - exploration research on seams, constraints, and existing boundaries
   - brainstorming and decomposition into specs
   - validation of dependencies, contracts, and scope
   - finalization of epic outputs
4. Build `epic.md` with:
   - vision and scope
   - spec list with goals and size
   - dependency graph
   - interface contracts and sequencing notes
5. Persist `.epic-state.json` with each spec, its status, and dependencies.
6. Set `specs/.current-epic` to the active epic name.
7. Show the next unblocked spec and route back to `$ralph-specum-start` for per-spec execution.

## Output Shape

The result should make it clear:
- what belongs in each spec
- which specs can start now
- which specs are blocked by dependencies
- what contracts must stay stable across specs

## Response Handoff

- After writing `epic.md`, name `epic.md` and summarize the epic plan briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to the next spec`
- Treat `continue to the next spec` as approval of `epic.md`.
