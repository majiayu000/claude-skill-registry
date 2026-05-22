---
name: ralph-specum-implement
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-implement`, or explicitly asks Ralph Specum in Codex to run implementation for approved tasks, quick mode, or an explicit continue request.
metadata:
  surface: helper
  action: implement
---

# Ralph Specum Implement

You are a **coordinator, not an executor** -- delegate each task to a `spec-executor` sub-agent.

## Contract

- Resolve the active spec by explicit path, exact name, or `.current-spec`
- Require `tasks.md`
- Recompute task counts from disk before execution
- Merge state fields only
- Remove `.ralph-state.json` only when all tasks are complete and verified

## Action

1. Resolve the active spec. If none exists, stop.
2. Require `tasks.md`. Read `.progress.md`, current state, and current task markers.
3. Recompute task counters from disk: `total`, `completed`, and `next_index`.
4. Merge state for execution:
   - `phase: "execution"`
   - `awaitingApproval: false`
   - `totalTasks: total`
   - `taskIndex: next_index`
   - preserve `taskIteration`, `maxTaskIterations`, `globalIteration`, `maxGlobalIterations`, `commitSpec`, and `relatedSpecs`
5. **Delegate** each task to a `spec-executor` sub-agent. Pass the task description, file targets, success criteria, and context from `.progress.md`. The sub-agent implements the task and outputs `TASK_COMPLETE`. Do NOT implement tasks yourself. Execute tasks in order until complete or blocked.
6. `[P]` tasks may batch only when file sets do not overlap and verification is independent.
7. `[VERIFY]` tasks stay in the same run and must produce explicit verification evidence.
8. Marker syntax must be explicitly present in `tasks.md`. If markers are absent, treat tasks as non-batchable by default.
9. VE tasks are valid quality tasks when the spec includes autonomous end-to-end verification.
10. Native task sync metadata should be preserved when present.
11. After each task or safe batch:
   - mark the checkbox
   - update `.progress.md`
   - merge the state update
   - use the task `Commit` line unless commits were explicitly disabled
12. On failure or interruption, persist the current state and stop with a resumable summary.
13. On full completion, remove `.ralph-state.json` and report completion.

## Resume Rules

- Resume from the persisted task state when execution was already in progress.
- If disk state and task checkboxes disagree, prefer `tasks.md` for completion and repair state to match.
- If approval is still pending for tasks, stop and get approval unless quick mode or explicit user direction says to continue.
