---
name: ln-400-story-executor
description: "Executes Story tasks in priority order (To Review, To Rework, Todo). Use when Story has planned tasks ready for implementation."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L2 Coordinator
**Category:** 4XX Execution

# Story Execution Orchestrator

Runtime-backed coordinator for Story execution. Owns task ordering, worktree lifecycle, task/group checkpoints, and the final Story transition to `To Review`.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.  
**Status filter:** Todo, In Progress, To Rework, To Review

## Purpose & Scope

- Load Story and task metadata once per loop
- Execute in order: `To Review -> To Rework -> Todo`
- Launch `Todo` parallel groups only when explicitly marked
- Force immediate review after every executor/rework step
- Persist resumable runtime state in `.hex-skills/story-execution/runtime/`
- Move Story only to `To Review`; never to `Done`

## Runtime Contract

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`
**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/story_execution_runtime_contract.md`, `shared/references/coordinator_summary_contract.md`
**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use the Story execution row

Runtime CLI:

```bash
node shared/scripts/story-execution-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-execution/manifest.json
node shared/scripts/story-execution-runtime/cli.mjs status
node shared/scripts/story-execution-runtime/cli.mjs checkpoint --phase PHASE_3_SELECT_WORK --payload '{...}'
node shared/scripts/story-execution-runtime/cli.mjs record-task --task-id {taskId} --payload '{...}'
node shared/scripts/story-execution-runtime/cli.mjs record-group --group-id {groupId} --payload '{...}'
node shared/scripts/story-execution-runtime/cli.mjs advance --to PHASE_4_TASK_EXECUTION
```

## Workflow

### Phase 0: Config

1. Resolve `storyId`.
2. Detect `task_provider` from task-management config.
3. Build execution manifest:
   - `story_id`
   - `task_provider`
   - `project_root`
   - planned `worktree_dir`
   - branch name
   - `parallel_group_policy`
   - `status_transition_policy`
4. Start runtime and checkpoint `PHASE_0_CONFIG`.

### Phase 1: Discovery

1. Resolve Story title and current Story status.
2. Load child task metadata only:
   - Linear: `list_issues(parentId=storyId)`
   - File mode: parse task files and `**Status:**`
3. Build `processable_counts` for:
   - `to_review`
   - `to_rework`
   - `todo`
4. Checkpoint `PHASE_1_DISCOVERY`.

### Phase 2: Worktree Setup

1. Detect current branch.
2. If already inside `feature/*`, treat current directory as active worktree.
3. Otherwise create `.hex-skills/worktrees/story-{identifier}` and branch `feature/{identifier}-{slug}` per worktree fallback guide.
4. Checkpoint `PHASE_2_WORKTREE_SETUP` with:
   - `worktree_ready`
   - `worktree_dir`
   - `branch`
5. Advance only after `worktree_ready=true`.

### Phase 3: Select Work

Selection order is deterministic:

1. Any `To Review` task first, sequentially
2. Then any `To Rework` task, sequentially
3. Then `Todo` tasks:
   - tasks with `**Parallel Group:** {N}` may run as one group
   - tasks without a group are single-task sequential units

Checkpoint `PHASE_3_SELECT_WORK` with:
- `current_task_id` or `current_group_id`
- fresh `processable_counts`

If all processable counts are zero, skip execution and advance to `PHASE_7_STORY_TO_REVIEW`.

### Phase 4: Task Execution

Used for:
- `To Review` -> `ln-402`
- `To Rework` -> `ln-403`, then immediate `ln-402`
- single `Todo` test task -> `ln-404`, then immediate `ln-402`
- single `Todo` impl/refactor task -> `ln-401`, then immediate `ln-402`

Flow:

1. Execute the worker.
2. Read the worker summary artifact from `.hex-skills/runtime-artifacts/runs/{run_id}/task-status/{task_id}.json`.
3. Run immediate review when required.
4. Read the latest review summary artifact for the same task.
5. Record runtime task result with `record-task`.
6. Checkpoint `PHASE_4_TASK_EXECUTION`.
7. Advance to `PHASE_6_VERIFY_STATUSES`.

### Phase 5: Group Execution

Used only for `Todo` groups with more than one task.

1. Spawn all group executors in parallel via Agent tool.
2. Wait for all executors to finish.
3. Read each task summary artifact.
4. Review each task sequentially via `ln-402`.
5. Record group summary with `record-group`.
6. Checkpoint `PHASE_5_GROUP_EXECUTION`.
7. Advance to `PHASE_6_VERIFY_STATUSES`.

### Phase 6: Verify Statuses

1. Re-read task metadata from source of truth.
2. Refresh `processable_counts`.
3. Validate that every task touched in this run has a machine-readable latest summary.
4. If any worker leaves an unexpected transition, pause runtime.
5. If any task hits `To Rework` for the third consecutive time, pause runtime with escalation reason.
6. Checkpoint `PHASE_6_VERIFY_STATUSES`.
7. If processable work remains -> advance back to `PHASE_3_SELECT_WORK`.
8. If no processable work remains -> advance to `PHASE_7_STORY_TO_REVIEW`.

### Phase 7: Story To Review

1. Verify no tasks remain in `Todo`, `To Review`, or `To Rework`.
2. Update Story status to `To Review`.
3. Update kanban to `To Review`.
4. Checkpoint `PHASE_7_STORY_TO_REVIEW` with:
   - `story_transition_done=true`
   - `story_final_status="To Review"`
   - `final_result="READY_FOR_GATE"`

### Phase 8: Self-Check

Build final checklist from runtime state, not memory:

- [ ] Config checkpoint exists
- [ ] Discovery checkpoint exists
- [ ] Worktree checkpoint exists and `worktree_ready=true`
- [ ] Every executed task has a summary artifact
- [ ] Every processed group has a recorded runtime result
- [ ] Rework loop guard did not trip
- [ ] Story moved to `To Review`

Checkpoint `PHASE_8_SELF_CHECK` with `pass=true|false`.
Complete runtime only after `pass=true`.

## Worker Invocation (MANDATORY)

| Status | Worker | Invocation |
|--------|--------|------------|
| `To Review` | `ln-402-task-reviewer` | Inline via `Skill()` |
| `To Rework` | `ln-403-task-rework` | Agent, then immediate `ln-402` |
| `Todo` tests | `ln-404-test-executor` | Agent, then immediate `ln-402` |
| `Todo` impl/refactor | `ln-401-task-executor` | Agent, then immediate `ln-402` |

Executors and reworkers run isolated:

```javascript
Agent(
  description: "Execute task {taskId}",
  prompt: "Execute task worker.\n\nStep 1: Invoke worker:\n  Skill(skill: \"{worker}\")\n\nCONTEXT:\nTask ID: {taskId}",
  subagent_type: "general-purpose"
)
```

Reviewer runs inline:

```javascript
Skill(skill: "ln-402-task-reviewer", args: "{taskId}")
```

## TodoWrite format (mandatory)

```
- Start ln-400 runtime (pending)
- Load Story/task metadata (pending)
- Setup or detect worktree (pending)
- Select next task/group (pending)
- Execute task/group (pending)
- Review task results immediately (pending)
- Re-read statuses and record checkpoint (pending)
- Move Story to To Review (pending)
- Run runtime self-check and complete (pending)
```

## Critical Rules

- Runtime state is the orchestration SSOT; kanban is the task-status SSOT.
- Never batch reviews.
- Never move Story to `Done`.
- Every worker outcome must be read from summary JSON, not from prose-only chat.
- Reviews remain sequential even when execution groups are parallel.
- `ln-402` remains the only worker that can accept a task as `Done`.

## Definition of Done

- [ ] Runtime started and `PHASE_0_CONFIG` checkpointed
- [ ] Discovery and worktree setup checkpointed
- [ ] Every executed task/group recorded in runtime
- [ ] Rework-loop escalation handled deterministically (`PAUSED`) when needed
- [ ] Final status verification checkpointed
- [ ] Story moved to `To Review`, not `Done`
- [ ] Self-check passed and runtime completed

## Phase 9: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Run after phases complete. Output to chat using the `execution-orchestrator` format.

## Reference Files

- `shared/references/coordinator_runtime_contract.md`
- `shared/references/story_execution_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/git_worktree_fallback.md`
- `../ln-401-task-executor/SKILL.md`
- `../ln-402-task-reviewer/SKILL.md`
- `../ln-403-task-rework/SKILL.md`
- `../ln-404-test-executor/SKILL.md`

---
**Version:** 4.0.0
**Last Updated:** 2026-01-29
