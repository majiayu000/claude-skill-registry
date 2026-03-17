---
name: execute
description: EXECUTION PHASE - Run tasks via isolated subagents. Requires completed task DAG from plan phase.
tools:
  - agent
  - bash
  - file_read
  - file_write
---

# Execute Workflow

**CRITICAL: This is the EXECUTE skill. Only use this after /plan has completed and task files exist in .tasker/tasks/. If no tasks exist, tell the user to run /tasker:plan first.**

**IMPORTANT: All tasker working files are in `$TARGET_DIR/.tasker/`. Do NOT create or use any other directories like `project-planning/`, `planning/`, or `schemas/` at the target project root. The `.tasker/` directory is the ONLY location for tasker artifacts (including `.tasker/schemas/` for JSON schemas).**

Execute a task DAG via isolated subagents. This is Phase 3 of the tasker workflow:

```
/specify → /plan → /execute
```

## Input Requirements

- **Task DAG** from `/plan`: `.tasker/tasks/T001.json`, `T002.json`, etc.
- **State file**: `.tasker/state.json` with phase = "ready" or "executing"

## Output

- **Working implementation** in target directory
- **Task results**: `.tasker/bundles/T001-result.json`, etc.
- **Evaluation report**: `.tasker/reports/evaluation-report.txt`

---

## MANDATORY FIRST STEP: Ask for Target Project Directory

**ALWAYS ask for target_dir FIRST before anything else.** No guessing, no inference from CWD.

Use AskUserQuestion to ask:
```
What is the target project directory?
```
Free-form text input. User must provide an absolute or relative path.

After target_dir is confirmed:
```bash
TARGET_DIR="<user-provided-path>"
# Convert to absolute path
TARGET_DIR=$(cd "$TARGET_DIR" 2>/dev/null && pwd)

TASKER_DIR="$TARGET_DIR/.tasker"

# Verify .tasker/ exists and has state
if [ ! -f "$TASKER_DIR/state.json" ]; then
    echo "Error: No tasker session found at $TASKER_DIR"
    echo "Run /plan first to create a task plan."
    exit 1
fi
```

---

## Execute Prerequisites

```bash
# Verify planning is complete
tasker state status
# Phase must be: ready, executing, or have tasks
```

---

## Git Repository Initialization (MANDATORY)

**Before any implementation begins**, check if the target repository has git initialized. If not, initialize it:

```bash
./scripts/ensure-git.sh "$TARGET_DIR"
```

**Why this is required:**
- Enables automatic commit hooks to track changes per task
- Provides audit trail of all implementation changes
- Required for the post-task-commit hook to function

---

## Recovery on Start (CRITICAL)

**Before starting the execute loop**, always check for and recover from a previous crash:

```bash
# Check for existing checkpoint from previous run
tasker state checkpoint status

# If checkpoint exists and is active, recover
tasker state checkpoint recover

# This will:
# 1. Find tasks that completed (have result files) but weren't acknowledged
# 2. Identify orphaned tasks (still "running" with no result file)
# 3. Update checkpoint state accordingly
```

If orphaned tasks are found, ask user:
```markdown
Found 3 orphaned tasks from previous run:
- T019, T011, T006

Options:
1. Retry orphaned tasks (reset to pending)
2. Skip orphaned tasks (mark failed)
3. Abort and investigate
```

To retry orphaned tasks:
```bash
tasker state task retry T019
tasker state task retry T011
tasker state task retry T006
tasker state checkpoint clear
```

---

## Execute Loop

**CRITICAL CONSTRAINTS:**
- **Max 3 parallel executors** - More causes orchestrator context exhaustion
- **Task-executors are self-completing** - They update state and write results directly
- **Checkpoint before spawning** - Track batch for crash recovery
- **Minimal returns** - Executors return only `T001: SUCCESS` or `T001: FAILED - reason`

### Loop Steps

Repeat until no more tasks or halt requested:

**Step 0: Check for Halt**
- Use Bash: `tasker state check-halt`
- If exit code is non-zero, halt was requested:
  - Run `tasker state checkpoint complete`
  - Generate and display evaluation report (see "Evaluation Report" section)
  - Run `tasker state confirm-halt`
  - Exit loop

**Step 1: Get Ready Tasks**
- Use Bash: `tasker state ready`
- If no ready tasks:
  - Run `tasker state advance`
  - If successful: all tasks complete! Clear checkpoint, generate and display evaluation report, exit loop
  - If no progress: check for blockers with `tasker state status`, exit loop

**Step 2: Select Batch**
- Take up to 3 task IDs from ready tasks

**Step 3: Generate and Validate Bundles**
For each task in batch:
- Use Bash: `tasker bundle generate {TASK_ID}`
- Use Bash: `tasker bundle validate-integrity {TASK_ID}`
- If integrity fails (exit code 1): fail the task with `tasker state task fail {TASK_ID} "Bundle integrity validation failed" --category dependency`
- If integrity warns (exit code 2): regenerate bundle

**Step 4: Create Checkpoint**
- Use Bash: `tasker state checkpoint create {TASK_IDs...}`

**Step 5: Mark Tasks Started**
For each valid task:
- Use Bash: `tasker state task start {TASK_ID}`

**Step 6: Spawn Executors in Parallel**
Use the Task tool to spawn `task-executor` subagents for ALL valid tasks in a SINGLE message (parallel execution):

```
Execute task {TASK_ID}

TASKER_DIR: {absolute path to .tasker directory}
Bundle: {TASKER_DIR}/bundles/{TASK_ID}-bundle.json
```

Wait for all executors to return. Each returns only: `{TASK_ID}: SUCCESS` or `{TASK_ID}: FAILED - reason`

**Step 7: Update Checkpoint**
For each task in batch:
- Use Bash: `tasker state checkpoint update {TASK_ID} {status}`

**Step 8: Complete Checkpoint**
- Use Bash: `tasker state checkpoint complete`

**Step 9: Check for Halt After Batch**
- Use Bash: `tasker state check-halt`
- If halted: generate and display evaluation report, confirm halt, exit loop

**Step 10: Continue to Next Batch**

---

## Post-Execution Commit (Defense in Depth)

Task file commits are handled **automatically** by a Claude Code hook, ensuring commits happen regardless of executor behavior.

### Hook Configuration

Configured in `.claude/settings.local.json`:
```json
"PostToolUse": [
  {
    "matcher": "Task",
    "hooks": [
      {
        "type": "command",
        "command": ".claude/hooks/post-task-commit.sh",
        "timeout": 30
      }
    ]
  }
]
```

---

## Subagent Spawn Template

Spawn task-executor with self-contained bundle. **Executors are self-completing** - they update state and write results directly, returning only a minimal status line.

```
Execute task [TASK_ID]

## Logging (MANDATORY)

```bash
./scripts/log-activity.sh INFO task-executor start "Executing task [TASK_ID]"
./scripts/log-activity.sh INFO task-executor decision "What decision and why"
./scripts/log-activity.sh INFO task-executor complete "Outcome description"
```

TASKER_DIR: {absolute path to .tasker directory}
Bundle: {TASKER_DIR}/bundles/[TASK_ID]-bundle.json

The bundle contains everything you need:
- Task definition and acceptance criteria
- Expanded behavior details (what to implement)
- File paths and purposes
- Target directory
- Constraints and patterns to follow
- Dependencies (files from prior tasks)

## Self-Completion Protocol (CRITICAL)

You are responsible for updating state and persisting results. Do NOT rely on the orchestrator.

### On Success:
1. Track all files you created/modified
2. Call: `tasker state task complete [TASK_ID] --created file1 file2 --modified file3`
3. Write result file: `{TASKER_DIR}/bundles/[TASK_ID]-result.json`
4. Return ONLY this line: `[TASK_ID]: SUCCESS`

### On Failure:
1. Call: `tasker state task fail [TASK_ID] "error message" --category <cat> --retryable`
2. Write result file with error details
3. Return ONLY this line: `[TASK_ID]: FAILED - <one-line reason>`

### Result File Schema
Write to `{TASKER_DIR}/bundles/[TASK_ID]-result.json`:
```json
{
  "version": "1.0",
  "task_id": "[TASK_ID]",
  "name": "Task name from bundle",
  "status": "success|failed",
  "started_at": "ISO timestamp",
  "completed_at": "ISO timestamp",
  "files": {
    "created": ["path1", "path2"],
    "modified": ["path3"]
  },
  "verification": {
    "verdict": "PASS|FAIL",
    "criteria": [
      {"name": "criterion", "status": "PASS|FAIL", "evidence": "..."}
    ]
  },
  "error": {
    "category": "dependency|compilation|test|validation|runtime",
    "message": "...",
    "retryable": true
  },
  "notes": "Any decisions or observations"
}
```

## Workflow Summary
1. Read the bundle file - it has ALL context
2. Implement behaviors in specified files
3. Run acceptance criteria verification
4. Call tasker state to update task status
5. Write detailed result to bundles/[TASK_ID]-result.json
6. Return ONE LINE status to orchestrator

IMPORTANT: Use the TASKER_DIR absolute path provided. Do NOT use relative paths.
```

---

## Bundle Contents

The bundle (`{TASKER_DIR}/bundles/T001-bundle.json`) includes:

| Field | Purpose |
|-------|---------|
| `task_id`, `name` | Task identification |
| `target_dir` | Where to write code |
| `behaviors` | Expanded behavior details (not just IDs) |
| `files` | Paths, actions, purposes, layers |
| `acceptance_criteria` | Verification commands |
| `constraints` | Tech stack, patterns, testing |
| `dependencies.files` | Files from prior tasks to read |
| `context` | Domain, capability, spec reference |
| `state_machine` | FSM context for adherence verification (if present) |

Generate bundles with:
```bash
tasker bundle generate T001       # Single task
tasker bundle generate-ready      # All ready tasks
```

---

## Execute Options

| Command | Behavior |
|---------|----------|
| `/execute` | Interactive, one task at a time |
| `/execute T005` | Execute specific task only |
| `/execute --batch` | All ready tasks, no prompts |
| `/execute --parallel 3` | Up to 3 tasks simultaneously |

---

## Graceful Halt and Resume

The executor supports graceful halt via two mechanisms:

### 1. STOP File (Recommended for External Control)

Create a `STOP` file in the `.tasker/` directory:

```bash
touch .tasker/STOP
```

The executor checks for this file before starting each new task and after completing each task. When detected:
1. Current task (if running) completes normally
2. No new tasks are started
3. State is saved with halt information
4. Clean exit with instructions to resume

### 2. User Message (For Interactive Sessions)

If a user sends "STOP" during an interactive `/execute` session, the orchestrator should:
1. Call `tasker state halt user_message`
2. Allow current task to complete
3. Exit gracefully

### Resuming Execution

To resume after a halt:

```bash
# Check current halt status
tasker state halt-status

# Clear halt and resume
tasker state resume

# Then run /execute again
```

---

## FSM Coverage Report (After Execution Completes)

After all tasks complete, generate the execution coverage report:

```bash
tasker fsm validate execute-coverage-report \
    {TASKER_DIR}/artifacts/fsm/index.json \
    {TASKER_DIR}/bundles \
    --output {TASKER_DIR}/artifacts/fsm-coverage.execute.json
```

This report includes:
- Which transitions were verified during execution
- Evidence type for each transition (test, runtime_assertion, manual)
- Which invariants were enforced
- Pointers to tasks and acceptance criteria that provide evidence

---

## Evaluation Report (After Completion)

**MANDATORY**: After all tasks complete (or execution halts), generate AND DISPLAY the evaluation report.

### Step 1: Generate the report

Use Bash tool:
- `tasker evaluate --output {TASKER_DIR}/reports/evaluation-report.txt`
- `tasker evaluate --format json --output {TASKER_DIR}/reports/evaluation-report.json`

### Step 2: Read and display the report

**CRITICAL:** Use the Read tool to read `{TASKER_DIR}/reports/evaluation-report.txt` and display its full contents to the user. Do NOT just say "report generated" - show the actual report.

The report includes:
- **Planning Quality** - plan verdict and issues at planning time
- **Execution Summary** - completed/failed/blocked/skipped counts
- **First-Attempt Success Rate** - measures spec quality
- **Verification Breakdown** - criteria pass/partial/fail, code quality scores
- **Cost Analysis** - total tokens, total cost, per-task cost
- **Failure Analysis** - which tasks failed and why (if any)
- **Improvement Patterns** - common issues for process improvement

### Step 3: Summarize key outcomes

After displaying the report, provide a brief summary:
- Total tasks completed vs failed
- Any notable failures or issues requiring attention
- Suggested next steps (e.g., "run tests", "review changes", "check logs")

---

## Archive Execution Artifacts (After Completion)

After execution completes (all tasks done or halted), archive execution artifacts:

```bash
tasker archive execution {project_name}
```

This creates:
```
archive/{project_name}/execution/{timestamp}/
├── bundles/        # Task bundles and result files
├── logs/           # Activity logs
├── state.json      # State snapshot
└── archive-manifest.json
```

---

## State Commands Reference

```bash
# Execution
tasker state ready               # List ready tasks
tasker state task start <id>     # Mark running
tasker state task complete <id>  # Mark done
tasker state task fail <id> <e>  # Mark failed
tasker state load-tasks          # Reload from files

# Halt / Resume
tasker state halt [reason]       # Request graceful halt
tasker state check-halt          # Check if halted (exit 1 = halted)
tasker state confirm-halt        # Confirm halt completed
tasker state halt-status         # Show halt status
tasker state resume              # Clear halt, resume execution

# Checkpoint (Crash Recovery)
tasker state checkpoint create <t1> [t2 ...]  # Create batch checkpoint
tasker state checkpoint update <id> <status>  # Update task
tasker state checkpoint complete              # Mark batch done
tasker state checkpoint status                # Show current checkpoint
tasker state checkpoint recover               # Recover orphaned tasks
tasker state checkpoint clear                 # Remove checkpoint

# Bundles
tasker bundle generate <id>      # Generate bundle for task
tasker bundle generate-ready     # Generate all ready bundles
tasker bundle validate <id>      # Validate bundle against schema
tasker bundle validate-integrity <id>  # Check deps + checksums
tasker bundle list               # List existing bundles
tasker bundle clean              # Remove all bundles
```

---

## Error Recovery

If task fails:
1. `tasker state task fail` marks it failed
2. Rollback triggered (created files deleted, modified files restored)
3. Dependent tasks auto-blocked
4. Other ready tasks can continue
5. User can retry later: fix issue, then `tasker state task retry` again
