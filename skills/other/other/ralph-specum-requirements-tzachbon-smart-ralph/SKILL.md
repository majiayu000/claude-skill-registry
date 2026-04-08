---
name: ralph-specum-requirements
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-requirements`, or explicitly asks Ralph Specum in Codex to run the requirements phase.
metadata:
  surface: helper
  action: requirements
---

# Ralph Specum Requirements

Use this for the requirements phase.

## Contract

- Resolve the active spec by explicit path, exact name, or `.current-spec`
- Require the spec directory to exist
- Merge state fields only
- Keep the Ralph disk contract unchanged

## Action

1. Resolve the active spec. If none exists, stop.
2. Read `research.md` when present, `.progress.md`, and the current state.
3. Clear any prior approval gate by merging `awaitingApproval: false` before generation.
4. Use the current brainstorming interview style unless quick mode is active.
5. Write or rewrite `requirements.md`.
6. Merge state with `phase: "requirements"` and `awaitingApproval: true`.
7. Update `.progress.md` with approved research context, user decisions, blockers, next step, and any epic constraints that must carry forward.
8. If spec commits are enabled, commit only the spec artifacts.
9. In quick mode, continue directly into design.

## Output Shape

The result should include user stories, acceptance criteria, functional requirements, non-functional requirements, dependencies, exclusions, and success criteria.

## Response Handoff

- After writing `requirements.md`, name `requirements.md` and summarize the requirements briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to design`
- Treat `continue to design` as approval of `requirements.md`.
