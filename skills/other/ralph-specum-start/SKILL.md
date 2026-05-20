---
name: ralph-specum-start
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-start`, or explicitly asks Ralph Specum in Codex to start or resume a spec.
metadata:
  surface: helper
  action: start
---

# Ralph Specum Start

Use this for the `start` and `new` entrypoints.

## Contract

- Read `.claude/ralph-specum.local.md` when present
- Default specs root is `./specs`
- Keep `.current-spec` in the default specs root
- Keep the standard Ralph files stable
- Merge `.ralph-state.json`. Do not replace the full object

## Action

1. Parse explicit name, goal, `--quick`, commit flags, optional specs root, and optional `--tasks-size fine|coarse`.
2. Resolve the target by explicit path, exact name, or `.current-spec`.
3. If the same name exists in multiple configured roots, stop and require a full path.
4. Check active epic context from `specs/.current-epic` when no explicit spec was chosen.
5. For large or cross-cutting goals, route to triage instead of forcing a single spec.
6. `new` is an alias here. Create the spec directory if needed.
7. Initialize or merge state with:
   - `source: "spec"`
   - `name`
   - `basePath`
   - `phase: "research"`
   - `taskIndex: 0`
   - `totalTasks: 0`
   - `taskIteration: 1`
   - `maxTaskIterations: settings default or 5`
   - `globalIteration: 1`
   - `maxGlobalIterations: 100`
   - `commitSpec: settings auto_commit_spec or true`
   - `relatedSpecs: []`
   - `awaitingApproval: true` when the run will stop after setup and wait for explicit direction
   - `awaitingApproval: false` when quick mode or explicit autonomy will continue without pausing
   - preserve or set `quickMode`
   - preserve or set `granularity` when `--tasks-size` was supplied
   - preserve or set `epicName` when starting from an epic suggestion
8. Update `.current-spec`.
9. Write `.progress.md` with goal, current phase, next step, blockers, learnings, and skill discovery results when used.
10. On resume, prefer `tasks.md` and present files over stale state when they disagree.
11. In quick mode, generate missing artifacts in order, skip normal approval pauses, and continue into implementation in the same run.
12. Without quick mode or explicit autonomy, stop after setup and ask whether to continue to research.

## Branch Isolation

- If the user wants isolation, offer a feature branch in place or a worktree with a feature branch.
- If a worktree is created, stop after creation and ask the user to continue from that worktree.

## Response Handoff

- After creating or resuming the spec, name the resolved spec path and summarize the current state briefly.
- End with exactly one explicit choice prompt:
  - `request changes`
  - `continue to research`
- Do not run research until the user explicitly asks to continue or explicitly asked for quick or autonomous flow.
