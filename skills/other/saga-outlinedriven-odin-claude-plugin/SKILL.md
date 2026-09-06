---
name: saga
description: 'Use when a user runs saga or asks to autonomously build a sizable feature. Not for executing a given plan: use subagent-driven.'
---

# Saga

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User runs saga or asks to autonomously build a sizable feature. |
| Authority | Reversible local: writes specs and progress artifacts to the saga directory under `~/.sagas/` (rollback is deleting them) and worker artifacts in isolated git worktrees (rollback is version control). No remote mutation except a human-approved branch push or draft PR for remote-worker handoff. Validates each task to its criteria before integration; milestone-level validation gates progression; user acceptance is the terminal gate before integration to the target branch. |
| Side effect | Creates a saga directory outside the repo and spawns workers in isolated git worktrees. |
| Done | All tasks meet validation, milestones pass, user accepts. |

## Inputs

- Feature request (user-provided prompt or description).
- Target repository path.
- Saga directory is confirmed with user before creation.

## Procedure

### Phase 1: planning (orchestrator + user)

1. **Intake.** Restate the request as a one-paragraph problem statement and the rough shape of the feature. Identify major unknowns. Pick a saga directory name under `~/.sagas/` from a feature slug plus timestamp (e.g. `~/.sagas/dark-mode-20260609-0028/`). Confirm the path with the user before creating anything.

2. **Discover environment.** By inspecting the repo first, determine:
   - Program type (web app, native GUI, TUI, CLI/library, backend service).
   - Whether computer use is available (local, remote only, or not available).
   - Test runner, build, lint, and typecheck commands: confirm they run.
   - How the program is launched for manual or interactive verification.
   Record findings in `SAGA.md` under the environment section.

3. **Close ambiguity.** Iterate with the user via `ask_user_question` (with concrete options, recommended_option_index set) until behavior, scope boundaries, edge cases, data shapes, error handling, non-goals, and the acceptance bar are unambiguous. Batch up to 4 related questions per call.

4. **Write saga exit criteria.** Before decomposing, define the concrete, checkable conditions that mean the feature is complete and correct. These are the Phase 3 contract.

5. **Decompose into milestones and tasks.** Break work into milestones (ordered by dependency, independently meaningful) and tasks (scoped for one worker in one focused effort). For each task, specify its scope, owned files/surfaces, dependencies, validation criteria, and validation method. Write the spec tree: milestone index and exit criteria in `SAGA.md`, milestone detail in `MILESTONE.md`, task detail in each task spec.

6. **Get approval.** Present the full spec tree to the user via `ask_user_question`. Do not begin Phase 2 until approved.

### Phase 2: implementation (worker fleet)

1. **Launch workers.** Use `run_agents` to delegate tasks. The orchestrator never implements feature code. Immediately record each worker's agent/run ID, task, branch, and worktree in `PROGRESS.md`.

2. **Isolate local workers.** Give each worker its own git worktree and branch following the convention `saga/<saga-name>/m<M>t<T>-<task-slug>`. Create with:
   ```
   git worktree add ../saga-<saga-name>-m<M>t<T> -b saga/<saga-name>/m<M>t<T>-<task-slug> <base>
   ```
   Workers must never share a checkout.

3. **Per-worker contract.** Instruct each worker to: implement only its assigned task; self-validate against the task's criteria using the prescribed method (computer use, interactive CLI, or tests) in a fix→validate loop; create a durable handoff (commit to the task branch for local workers; for remote workers, obtain explicit human approval before pushing a branch, opening a draft PR, or sharing a patch); remove the worktree only after the durable handoff exists (`git worktree remove <path> --force`); report branch name, commit hash, changed files, validation evidence, and pass/blocked status.

4. **Collect and act on reports.** Update `PROGRESS.md` with per-task status and evidence. Handle blocked tasks: re-delegate with retained context, adjust the task spec, or escalate to the user via `ask_user_question` with options, only if the blocker is a genuine spec gap or external decision.

5. **Integrate each milestone.** Merge the milestone's branches into an integration branch, resolve conflicts, run milestone-level validation, and remove any worktrees left behind before proceeding.

6. **Maintain state.** Update `PROGRESS.md` continuously. Re-read specs and `PROGRESS.md` from disk rather than holding state in context.

### Phase 3: final validation

1. **Run exit criteria.** Execute all saga-level exit criteria using the strongest available method. Summarize evidence against each criterion.

2. **Present completion report.** What was built, how each exit criterion was validated, exact steps for manual verification.

3. **Loop user for acceptance.** Present via `ask_user_question` (accept or report specific issues). If issues are reported, capture them as new tasks, run a focused Phase 2 mini-loop, and re-present. Repeat until the user accepts. Only then is the saga complete.

### Continuing a saga

When asked to continue, resume, or pick up a saga:

1. **Locate.** Find the saga directory under `~/.sagas/`. If ambiguous, ask the user via `ask_user_question`.
2. **Rebuild orientation.** Read `SAGA.md` (problem, environment, exit criteria, phase, milestone index) and `PROGRESS.md` (phase, current milestone, task statuses, worker run IDs, open questions, recent log). Open only the spec for the milestone about to be acted on.
3. **Reconcile.** Verify git state for done/in-progress tasks: check whether branches and worktrees exist, whether they have been merged. Spot-check validation evidence for done tasks. Update `PROGRESS.md` to match reality.
4. **Resume.** From the reconciled state, resume Phase 2 at the current milestone or Phase 3 if all milestones are integrated. Follow the Phase 2/3 procedure above.
5. **Keep the contract.** Do not silently re-scope. If the spec is wrong, update the relevant spec file and note it in `PROGRESS.md` under Decisions & Deviations; escalate to the user if agreed behavior or exit criteria change.

## Failure and recovery
- Spec gap: ambiguity unresolved in Phase 1 blocks delegation. Escalate to user via `ask_user_question` with options; do not proceed until resolved.
- Worker blocked: collect the report, update `PROGRESS.md`, re-delegate with retained context or adjust the task spec; escalate to user if the blocker is not resolvable from the spec.
- Milestone validation failure: revert to pre-integration state (branches and commits are preserved in git history); re-delegate affected tasks.
- Phase 3 rejection: capture reported issues as new tasks; run a focused Phase 2 mini-loop; re-present.
- Unachievable validation: if a criterion cannot be checked with available tools, update the spec and note the finding; escalate to the user.
- Partial-result rule: never remove a worktree while validated or useful partial work is still inside it.
- Non-rollback rule: once a durable handoff exists (commit pushed, draft PR opened, patch returned), the work is preserved regardless of subsequent failures.
- Non-converged result: if a task cannot be completed despite re-delegation and spec adjustment, record the blocker in `PROGRESS.md` and escalate to the user. Do not silently declare done.

## Output
A completed feature meeting all saga exit criteria. A completion report listing what was built, how each criterion was validated, and exact steps for manual verification. Terminal state is user acceptance.
