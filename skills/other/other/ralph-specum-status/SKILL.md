---
name: ralph-specum-status
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-status`, or explicitly asks Ralph Specum in Codex for status or active spec progress.
metadata:
  surface: helper
  action: status
---

# Ralph Specum Status

Use this to report Ralph state across configured spec roots.

## Contract

- Read `.claude/ralph-specum.local.md` when present
- Default specs root is `./specs`
- `.current-spec` lives in the default specs root
- Hidden directories do not count as specs

## Action

1. Resolve configured roots.
2. Read `.current-spec` to identify the active spec.
   - If `.current-spec` is missing or empty, report that there is no active spec and continue listing specs across roots.
3. Read `specs/.current-epic` when present and summarize epic status.
4. For each spec directory, inspect:
   - `.ralph-state.json`
   - `research.md`
   - `requirements.md`
   - `design.md`
   - `tasks.md`
5. If `tasks.md` exists, count completed and incomplete tasks.
6. Group results by spec root.
7. Show the active spec, current phase, backlog state, approval state, granularity when present, and which artifacts exist.

## Output

- Specs in the default root can be shown by name.
- Specs in other roots should include the root suffix for disambiguation.
- Include the next likely command when it is obvious.
- If an epic is active, include the next unblocked spec.
- If approval is pending, explicitly tell the user to approve the current artifact, request changes, or continue to the named next step.
