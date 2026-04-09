---
name: ralph-specum
description: Use only when the user explicitly invokes `$ralph-specum`, requests Ralph Specum in Codex, asks Ralph Specum to handle a named phase, or explicitly requests autonomous or quick mode or continuation without pauses.
metadata:
  surface: primary
---

# Ralph Specum

Use this as the primary Codex surface for Ralph Specum. It carries the full reusable workflow and can handle the entire command surface directly when helper skills are not installed.

## Read These References

- `references/workflow.md` for the phase flow, branch and worktree behavior, quick mode, and command routing
- `references/state-contract.md` for `.ralph-state.json`, `.progress.md`, commit rules, and resume semantics
- `references/path-resolution.md` for `specs_dirs`, `.current-spec`, ambiguity handling, and default directory behavior
- `references/parity-matrix.md` for Claude-to-Codex feature translation and command mapping

## Use These Helpers

- `scripts/resolve_spec_paths.py` for spec roots, current spec, and unique or ambiguous name resolution
- `scripts/merge_state.py` for safe top-level state merges
- `scripts/count_tasks.py` for task counts and next incomplete task
- `assets/templates/` for the canonical Ralph markdown file shapes
- `assets/bootstrap/` when the user wants optional project-local Codex guidance

## Primary Routing

Handle these intents directly:

| Intent | Action |
|--------|--------|
| Start, new, resume, quick mode | Follow the start flow in `references/workflow.md` |
| Triage | Delegate to `triage-analyst` sub-agent to decompose into epic and specs |
| Research | Delegate to `research-analyst` sub-agent to write `research.md` |
| Requirements | Delegate to `product-manager` sub-agent to write `requirements.md` |
| Design | Delegate to `architect-reviewer` sub-agent to write `design.md` |
| Tasks | Delegate to `task-planner` sub-agent to write `tasks.md` |
| Implement | Delegate each task to `spec-executor` sub-agent until complete or blocked |
| Status | Show active spec, backlog state, and per-root listing |
| Switch | Update `.current-spec` only |
| Cancel | Stop execution and clean up state, confirm before destructive delete |
| Index | Generate `specs/.index/` component and external specs |
| Refactor | Delegate to `refactor-specialist` sub-agent to update spec files |
| Feedback | Open or draft GitHub feedback |
| Help | Summarize the surface and next commands |

If the corresponding helper skill is installed and the user invoked it explicitly, keep behavior aligned with that helper. If not, perform the action here.

## Core Rules

0. **You are a coordinator, not a doer.** For every phase (research, requirements, design, tasks, implement, triage, refactor), delegate the actual generation work to the appropriate sub-agent. Never write spec artifacts (research.md, requirements.md, design.md, tasks.md) yourself. Your job is to gather context, run the interview, delegate, validate the output, and present results for approval.
1. Keep the Ralph disk contract stable.
2. Treat `.claude/ralph-specum.local.md` as the settings source when present.
3. Default to `./specs` when no valid config exists.
4. Keep `.current-spec` in the default specs root.
5. Merge state fields. Do not replace the whole state object.
6. Preserve `source`, `name`, `basePath`, `phase`, `taskIndex`, `totalTasks`, `taskIteration`, `maxTaskIterations`, `globalIteration`, `maxGlobalIterations`, `commitSpec`, and `relatedSpecs`.
7. Also preserve newer state fields when present, especially `awaitingApproval`, `quickMode`, `granularity`, `epicName`, `discoveredSkills`, and native task sync metadata.
8. Write `.progress.md` after every phase and after every implementation attempt.
9. Honor approval checkpoints between phases unless quick mode is active.
10. Honor the `Commit` line in tasks during implementation unless the user explicitly disables task commits.
11. Use branch creation or worktree creation when the user asks for branch isolation or the repo policy requires it.
12. Enter quick mode only when the user explicitly asks Ralph to be autonomous, do it quickly, or continue without pauses.
13. In quick mode, generate missing artifacts, default task granularity to `fine` when unset, and continue into implementation in the same session.

## Stop Enforcement

After completing any phase artifact (research, requirements, design, tasks), you MUST:

1. Display the walkthrough summary
2. Present the approval prompt (approve / request changes / continue to next)
3. **STOP and wait for user response**

The ONLY exception is `--quick` mode. Without `--quick`, you MUST NOT auto-continue to the next phase. This is non-negotiable.

## Response Handoff

- After writing `research.md`, `requirements.md`, `design.md`, `tasks.md`, or refactored spec files outside quick mode:
  - name the file or files that changed
  - give a short summary
  - end with exactly one explicit choice prompt:
    - `approve current artifact`
    - `request changes`
    - `continue to <named next step>`
- Treat `continue to <named next step>` as approval of the current artifact and permission to proceed.
- After `start` or `new`, summarize the resolved spec and stop unless the user explicitly asked for quick or autonomous flow. The next choice should point to `continue to research`.

## Current Workflow Expectations

- Use brainstorming-style interviews for research, requirements, design, and tasks when quick mode is not active.
- Route obviously large or cross-cutting efforts to triage before normal spec generation.
- Support active epic state via `specs/.current-epic` and per-epic state in `specs/_epics/<epic-name>/`.
- Treat task planning as POC-first with `[P]` markers for safe parallel work and `[VERIFY]` checkpoints for explicit quality validation.
- Support VE tasks when the plan needs autonomous end-to-end verification.
- During implementation, recompute task counts from disk, resume from the first incomplete task, and prefer task file truth over stale state.
- Native task sync is part of the current Ralph execution model. Keep Codex wording aligned with that behavior without promising Claude-only hook mechanics.

## Bootstrap

Bootstrap project-local files only when the user wants them.

Suggested bootstrap files:

- `assets/bootstrap/AGENTS.md` to give a consumer repo local Ralph guidance
- `assets/bootstrap/ralph-specum.local.md` to seed local settings

Do not bootstrap by default. Installation into `$CODEX_HOME/skills` is enough.
