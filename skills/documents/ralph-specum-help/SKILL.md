---
name: ralph-specum-help
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-help`, or explicitly asks Ralph Specum in Codex for help or command guidance.
metadata:
  surface: helper
  action: help
---

# Ralph Specum Help

Use this to explain the Ralph Specum surface in Codex.

## Cover

- Primary skill: `$ralph-specum`
- Helper skills: `$ralph-specum-start`, `$ralph-specum-triage`, `$ralph-specum-research`, `$ralph-specum-requirements`, `$ralph-specum-design`, `$ralph-specum-tasks`, `$ralph-specum-implement`, `$ralph-specum-status`, `$ralph-specum-switch`, `$ralph-specum-cancel`, `$ralph-specum-index`, `$ralph-specum-refactor`, `$ralph-specum-feedback`, `$ralph-specum-help`
- Normal flow: start, stop, research, approval, requirements, approval, design, approval, tasks, approval, implement
- Large effort flow: triage, then start each unblocked spec
- Quick mode: generate missing artifacts and continue into implementation in one run only when the user explicitly asks for quick or autonomous flow
- Disk contract: `./specs` or configured roots, `.current-spec`, optional `.current-epic`, per-spec markdown files, `.ralph-state.json`

## Guidance

- Recommend `$ralph-specum` as the default entrypoint.
- Recommend `$ralph-specum-triage` when the user describes a large, multi-part, or dependency-heavy effort.
- Mention helper skills when the user wants explicit phase control.
- Explain that Ralph does not self-advance by default. The user must approve the current artifact, request changes, or explicitly continue to the next step.
- Mention optional bootstrap assets only when the user wants repo-local guidance.
