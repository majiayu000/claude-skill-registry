---
name: ralph-specum-requirements
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-requirements`, or explicitly asks Ralph Specum in Codex to run the requirements phase.
metadata:
  surface: helper
  action: requirements
---

# Ralph Specum Requirements

You are a **coordinator, not a product manager** -- delegate ALL work to a `product-manager` sub-agent.

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
5. **Delegate** requirements generation to a `product-manager` sub-agent. Pass research context, goal, and interview results. The sub-agent writes `requirements.md`. Do NOT write requirements.md yourself.
6. Read the sub-agent's output and validate it exists.
7. Merge state with `phase: "requirements"` and `awaitingApproval: true` (or `false` when `--quick` is active).
8. Update `.progress.md` with approved research context, user decisions, blockers, next step, and any epic constraints that must carry forward.
9. If spec commits are enabled, commit only the spec artifacts.

### Stop Behavior

- **Without `--quick`**: STOP HERE. Display the walkthrough summary and approval prompt. Do NOT continue to design. Wait for the user to explicitly approve and request the next phase.
- **With `--quick`**: Continue directly into design.

## Output Shape

The result should include user stories, acceptance criteria, functional requirements, non-functional requirements, dependencies, exclusions, and success criteria.

## Response Handoff

- After writing `requirements.md`, name `requirements.md` and summarize the requirements briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to design`
- Treat `continue to design` as approval of `requirements.md`.
