---
name: phase-5-execute
description: Execute phase skill for plan management. DUMB TASK RUNNER that executes tasks from TASK-*.toon files sequentially.
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Skill, Task, AskUserQuestion
---

# Phase Execute Skill

**Role**: DUMB TASK RUNNER that executes tasks from TASK-*.toon files sequentially.

**Execution Pattern**: Locate current task → Execute steps → Mark progress → Next task

**Phase Handled**: execute

**CRITICAL**: Use manage-* scripts via Bash for plan file updates (Edit/Write tools trigger permission prompts on `.plan/` directories).

---

## Standards (Load On-Demand)

### Workflow
```
Read standards/workflow.md
```
Contains: Task execution pattern, phase transition, auto-continue behavior

### Operations
```
Read standards/operations.md
```
Contains: Delegation patterns for builds, quality checks, PR creation

---

## Execution Loop

### Step 0: Get Routing Context (Once at start)

Get current phase, skill routing, and progress in a single call:

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle get-routing-context \
  --plan-id {plan_id}
```

Returns:
```toon
status: success
plan_id: {plan_id}
current_phase: 5-execute
skill: pm-workflow:phase-5-execute
skill_description: Execute phase skill for task implementation
total_phases: 4
completed_phases: 2
phases:
- init: complete
- refine: complete
- execute: in_progress
- finalize: pending
```

Use `current_phase` for logging, `skill` for dynamic routing, and `completed_phases/total_phases` for progress display.

### Step 0.1: Read Commit Strategy (Once at start)

Cache the commit strategy for the entire execute loop:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-5-execute get --trace-plan-id {plan_id}
```

Extract `commit_strategy` from output. Valid values: `per_deliverable`, `per_plan`, `none`.

### Step 0.5: Log Phase Start (Once per phase)

At the start of execute or finalize phase:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-5-execute) Starting {phase} phase"
```

For each task in current phase:

### Step 1: Locate Task with Context

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks next \
  --plan-id {plan_id} \
  --include-context
```

Returns next task with status `pending` or `in_progress`, including embedded goal context (title, body) for immediate use without additional script calls.

### Step 2: Execute Steps

For each step in task's `steps[]` array:
1. Parse the step text
2. Execute the action (delegate if specified)
3. Mark step complete via `manage-tasks:step-done`

### Step 3: Mark Step Complete

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks step-done \
  --plan-id {plan_id} \
  --task {task_number} \
  --step {step_number}
```

### Step 3.5: Log Task Completion

After each task completes:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[OUTCOME] (pm-workflow:phase-5-execute) Completed {task_id}: {task_title} ({steps_completed} steps)"
```

### Step 3.6: Conditional Per-Deliverable Commit

If `commit_strategy == per_deliverable` (cached from Step 0.1):

1. **Check dependency chain**: Does any other pending/in-progress task have `depends_on` pointing to the just-completed task?
   - **YES** → Skip commit (a downstream task still needs to run)
   - **NO** → This is the chain tail (all tasks for this deliverable are done) → Commit

2. **Commit** (only when chain tail):
   ```
   Skill: pm-workflow:workflow-integration-git
   Parameters:
     - message: conventional commit derived from task title
     - push: false
     - create-pr: false
   ```

3. **Log commit outcome**:
   ```bash
   python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
     work {plan_id} INFO "[OUTCOME] (pm-workflow:phase-5-execute) Per-deliverable commit: {task_id} ({commit_hash})"
   ```

If `commit_strategy` is `per_plan` or `none` → Skip this step entirely.

### Step 4: Next Task or Phase

- If more tasks in phase → Continue to next task
- If phase complete → Log phase outcome and auto-transition to next phase
- If all phases complete → Mark plan complete

### Step 5: Log Phase Completion (When phase completes)

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-5-execute) Completed {phase} phase: {tasks_completed} tasks"
```

---

## Delegation

When checklist items specify delegation, invoke the appropriate agent/skill:

| Checklist Pattern | Delegation |
|-------------------|------------|
| "Run build" / "maven" / "npm" | See `standards/operations.md` |
| "Delegate to {agent}" | `Task: {agent}` |
| "Load skill: {skill}" | `Skill: {skill}` |
| "Run /command" | `SlashCommand: /command` |

---

## Auto-Continue Behavior

Execute continuously without user prompts except:
- Error blocks progress
- Decision genuinely required
- User explicitly requested confirmation

**Do NOT prompt for**:
- Phase transitions
- Task transitions
- Routine confirmations

---

## Phase Transition

When transitioning from execute phase to verify:

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle transition \
  --plan-id {plan_id} \
  --completed 5-execute
```

This automatically updates status.toon and moves to the next phase.

---

## Error Handling

On any error, **first log the error** to work-log:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} ERROR "[ERROR] (pm-workflow:phase-5-execute) {task_id} failed - {error_type}: {error_context}"
```

### Script Failure (Lessons-Learned Capture)

**ON SCRIPT FAILURE**: When any script execution fails (exit != 0):
1. Log error to work-log (see above)
2. Capture error context (script path, exit code, stderr)
3. Continue with normal error recovery (retry, fail task, etc.)

### Other Errors

| Error | Options |
|-------|---------|
| Build failure | Fix and retry / View log / Skip task |
| Test failure | Fix tests / View details / Skip task |
| Dependency not met | Complete dependency / Skip check |

---

## Integration

### Command Integration
- **/plan-marshall action=execute** - Primary entry point invoking this skill

### Related Skills
- **phase-4-plan** - Creates tasks from deliverables (previous phase)
- **phase-6-verify** - Quality verification (next phase)
- **phase-7-finalize** - Shipping workflow (commit, PR)

