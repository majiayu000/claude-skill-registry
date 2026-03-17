---
name: execute-tasks
description: Execute pending Claude Code Tasks in dependency order with wave-based concurrent execution and adaptive verification. Supports task group filtering and configurable parallelism. Use when user says "execute tasks", "run tasks", "start execution", "work on tasks", or wants to execute generated tasks autonomously.
argument-hint: "[task-id] [--task-group <group>] [--retries <n>] [--max-parallel <n>]"
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Task
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - TaskList
  - TaskGet
  - TaskUpdate
arguments:
  - name: task-id
    description: Optional specific task ID to execute. If omitted, executes all unblocked tasks in dependency order.
    required: false
  - name: task-group
    description: Optional task group name to filter tasks. Only tasks with matching metadata.task_group will be executed.
    required: false
  - name: retries
    description: Number of retry attempts for failed/partial tasks before moving on. Default is 3.
    required: false
  - name: max-parallel
    description: Maximum number of tasks to execute simultaneously per wave. Default is 5. Overrides settings file value.
    required: false
---

# Execute Tasks Skill

This skill orchestrates autonomous task execution for Claude Code Tasks. It builds a dependency-aware execution plan, launches a dedicated agent for each task through a 4-phase workflow (Understand, Implement, Verify, Complete), handles retries with failure context, and shares learnings across tasks through a shared execution context file.

## Core Principles

### 1. Understand Before Implementing

Never write code without first understanding:
- What the task requires (acceptance criteria or inferred requirements)
- What code already exists (read before modify)
- What conventions the project follows (CLAUDE.md, existing patterns)
- What earlier tasks discovered (shared execution context)

### 2. Follow Existing Patterns

Match the codebase's established patterns:
- Coding style, naming conventions, file organization
- Error handling approach, logging patterns
- Test framework, test structure, assertion style
- Import ordering, module organization

### 3. Verify Against Criteria

Do not assume implementation is correct. Verify by:
- Walking through each acceptance criterion for spec-generated tasks
- Running tests and linters for all tasks
- Confirming the core change works as intended
- Checking for regressions in existing functionality

### 4. Report Honestly

Produce accurate verification results:
- PASS only when all Functional criteria pass and tests pass
- PARTIAL when non-critical criteria fail but core works
- FAIL when Functional criteria or tests fail
- Never mark a task complete if verification fails

## Orchestration Workflow

This skill orchestrates task execution through a 10-step loop. See `references/orchestration.md` for the full detailed procedure.

### Step 1: Load Task List
Retrieve all tasks via `TaskList`. If a `--task-group` argument was provided, filter tasks to only those with matching `metadata.task_group`. If a specific `task-id` argument was provided, validate it exists.

### Step 2: Validate State
Handle edge cases: empty list, all completed, specific task blocked, no unblocked tasks, circular dependencies.

### Step 3: Build Execution Plan
Resolve `max_parallel` setting using precedence: `--max-parallel` CLI arg > `.claude/claude-alchemy.local.md` setting > default 5. Build a dependency graph from pending tasks. Assign tasks to waves using topological levels: Wave 1 = no dependencies, Wave 2 = depends on Wave 1 tasks, etc. Sort within waves by priority (critical > high > medium > low > unprioritized), break ties by "unblocks most others." Cap each wave at `max_parallel` tasks.

### Step 4: Check Settings
Read `.claude/claude-alchemy.local.md` if it exists for execution preferences, including `max_parallel` setting. CLI `--max-parallel` argument takes precedence over the settings file value.

### Step 5: Initialize Execution Directory
Generate a `task_execution_id` using three-tier resolution: (1) if `--task-group` provided → `{task_group}-{YYYYMMDD}-{HHMMSS}`, (2) else if all open tasks share the same `metadata.task_group` → `{task_group}-{YYYYMMDD}-{HHMMSS}`, (3) else → `exec-session-{YYYYMMDD}-{HHMMSS}`. Clean any stale `__live_session__/` files by archiving them to `.claude/sessions/interrupted-{YYYYMMDD}-{HHMMSS}/`, resetting any `in_progress` tasks from the interrupted session back to `pending`. Check for and enforce the concurrency guard via `.lock` file. Create `.claude/sessions/__live_session__/` directory containing:
- `execution_plan.md` — saved execution plan from Step 5
- `execution_context.md` — initialized with standard template
- `task_log.md` — initialized with table headers (Task ID, Subject, Status, Attempts, Duration, Token Usage)
- `tasks/` — subdirectory for archiving completed task files
- `progress.md` — initialized with status template for real-time progress tracking
- `execution_pointer.md` at `~/.claude/tasks/{CLAUDE_CODE_TASK_LIST_ID}/` — created immediately with absolute path to `.claude/sessions/__live_session__/`

### Step 6: Present Execution Plan and Confirm
Display the plan showing tasks to execute, blocked tasks, and completed count. Also display the details of step 5 which includes the session directory path (`.claude/sessions/__live_session__/`) and files created, including the execution pointer file location.

Then ask the user to confirm before proceeding with execution. If the user cancels, stop without modifying any tasks.

### Step 7: Initialize Execution Context
Read `.claude/sessions/__live_session__/execution_context.md` (created in Step 5). If a prior execution context exists, look in `.claude/sessions/` for the most recent timestamped subfolder and merge relevant learnings into the new one.

### Step 8: Execute Loop
Execute tasks in waves. For each wave: snapshot `execution_context.md`, mark wave tasks `in_progress`, update `progress.md` with all active tasks, launch up to `max_parallel` agents simultaneously via **parallel Task tool calls in a single turn**. Each agent writes to `context-task-{id}.md` instead of the shared context file. As agents return: calculate duration, capture token usage, log to `task_log.md`, update `progress.md`. Failed tasks with retries remaining are re-launched immediately within the wave. After all wave agents complete: merge per-task context files into `execution_context.md`, delete per-task files, archive completed task JSONs, refresh TaskList for newly unblocked tasks, form next wave, repeat.

### Step 9: Session Summary
Display execution results with pass/fail counts, total execution time, failed task list, newly unblocked tasks, and token usage summary (captured from Task tool responses if available). Save `session_summary.md` to `.claude/sessions/__live_session__/`. Archive the session by moving all contents from `__live_session__/` to `.claude/sessions/{task_execution_id}/`, leaving `__live_session__/` as an empty directory. `execution_pointer.md` stays pointing to `__live_session__/`.

### Step 10: Update CLAUDE.md
Review execution context for project-wide changes (new patterns, dependencies, commands, structure changes, design decisions). Make targeted edits to CLAUDE.md if meaningful changes occurred. Skip if only task-specific or internal implementation details.

## Task Classification

Determine whether a task is spec-generated or general to select the right verification approach.

### Detection Algorithm

1. **Check description format**: Look for `**Acceptance Criteria:**` with categorized criteria (`_Functional:_`, `_Edge Cases:_`, etc.)
2. **Check metadata**: Look for `metadata.spec_path` field
3. **Check source reference**: Look for `Source: {path} Section {number}` in the description

If any check matches -> **spec-generated task** (use criterion-based verification)

If none match -> **General task** (use inferred verification)

## 4-Phase Workflow

Each task is executed by the `claude-alchemy-sdd:task-executor` agent through these phases:

### Phase 1: Understand

Load context and understand scope before writing code.

- Read the execute-tasks skill and references
- Read `.claude/sessions/__live_session__/execution_context.md` for learnings from prior tasks
- Load task details via `TaskGet`
- Classify the task (spec-generated vs general)
- Parse acceptance criteria or infer requirements from description
- Explore affected files via Glob/Grep
- Read `CLAUDE.md` for project conventions

### Phase 2: Implement

Execute the code changes following project patterns.

- Read all target files before modifying them
- Follow the project's implementation order (data -> service -> interface -> tests)
- Match existing coding patterns and conventions
- Write tests if specified in testing requirements
- Run mid-implementation checks (linter, existing tests) to catch issues early

### Phase 3: Verify

Verify implementation against task requirements using the adaptive approach.

- **spec-generated tasks**: Walk each acceptance criteria category (Functional, Edge Cases, Error Handling, Performance), check testing requirements, run tests
- **General tasks**: Infer "done" from description, run existing tests, run linter, verify core change is implemented

### Phase 4: Complete

Report results and share learnings.

- Determine status (PASS/PARTIAL/FAIL) based on verification results
- If PASS: mark task as `completed` via `TaskUpdate`
- If PARTIAL or FAIL: leave as `in_progress` for the orchestrator to decide on retry
- Append learnings to `.claude/sessions/__live_session__/execution_context.md` (files discovered, patterns learned, issues encountered)
- Return structured report with verification results

## Adaptive Verification Overview

Verification adapts based on task type:

| Task Type | Verification Method | Pass Threshold |
|-----------|-------------------|----------------|
| spec-generated | Criterion-by-criterion evaluation | All Functional + Tests must pass |
| General | Inferred checklist from description | Core change works + Tests pass |

**Critical rule**: All Functional criteria must pass for a PASS result. Edge Cases, Error Handling, and Performance failures result in PARTIAL but do not block completion.

## Shared Execution Context

Tasks within an execution session share learnings through `.claude/sessions/__live_session__/execution_context.md`:

- **Snapshot before wave**: The orchestrator snapshots `execution_context.md` before launching each wave — all agents in a wave read the same baseline
- **Per-task writes**: During concurrent execution, each agent writes to `context-task-{id}.md` instead of the shared file to avoid write contention
- **Merge after wave**: After all agents in a wave complete, the orchestrator merges all `context-task-{id}.md` files into `execution_context.md` and deletes the per-task files
- **Sequential fallback**: When `max_parallel` is 1, agents write directly to `execution_context.md` as before (no per-task files)
- **Sections**: Project Patterns, Key Decisions, Known Issues, File Map, Task History

This enables later tasks to benefit from earlier discoveries and retry attempts to learn from previous failures.

## Key Behaviors

- **Autonomous execution loop**: After the user confirms the execution plan, no further prompts occur between tasks. The loop runs without interruption once started.
- **Wave-based parallelism**: Tasks at the same dependency level run simultaneously, up to `max_parallel` concurrent agents per wave. Tasks in later waves wait until their dependencies in earlier waves complete.
- **One agent per task, multiple per wave**: Each task gets a fresh agent invocation with isolated context, but multiple agents run concurrently within a wave.
- **Per-task context isolation**: During concurrent execution, each agent writes to `context-task-{id}.md`. The orchestrator merges these after each wave to prevent write contention.
- **Within-wave retry**: Failed tasks with retries remaining are re-launched immediately as agent slots free up within the current wave, maximizing throughput.
- **Configurable parallelism**: Default 5 concurrent tasks, configurable via `--max-parallel` argument or `.claude/claude-alchemy.local.md` settings. Set to 1 for sequential execution.
- **Configurable retries**: Default 3 attempts per task, configurable via `retries` argument.
- **Retry with context**: Each retry includes the previous attempt's failure details so the agent can try a different approach.
- **Dynamic unblocking**: After each wave completes, the dependency graph is refreshed and newly unblocked tasks are added to the next wave.
- **Honest failure handling**: After retries exhausted, tasks stay `in_progress` (not completed), and execution continues.
- **Circular dependency detection**: If all remaining tasks are blocked by each other, break at the weakest link (task with fewest blockers) and log a warning.
- **Shared context**: Agents read the snapshot of `execution_context.md` and write learnings to per-task files that get merged between waves.
- **Resilient context sharing**: If a task-executor fails to append to its context file, learnings are captured in the verification report as a fallback.
- **Single-session invariant**: Only one execution session can run at a time per project. A `.lock` file in `__live_session__/` prevents concurrent invocations.
- **Interrupted session recovery**: Stale sessions are detected and archived; tasks left `in_progress` are automatically reset to `pending`.

## Example Usage

### Execute all unblocked tasks
```
/claude-alchemy-sdd:execute-tasks
```

### Execute a specific task
```
/claude-alchemy-sdd:execute-tasks 5
```

### Execute with custom retry limit
```
/claude-alchemy-sdd:execute-tasks --retries 1
```

### Execute specific task with retries
```
/claude-alchemy-sdd:execute-tasks 5 --retries 5
```

### Execute tasks for a specific group
```
/claude-alchemy-sdd:execute-tasks --task-group user-authentication
```

### Execute specific group with custom retries
```
/claude-alchemy-sdd:execute-tasks --task-group payments --retries 1
```

### Execute with limited parallelism
```
/claude-alchemy-sdd:execute-tasks --max-parallel 2
```

### Execute sequentially (no concurrency)
```
/claude-alchemy-sdd:execute-tasks --max-parallel 1
```

### Execute group with custom parallelism and retries
```
/claude-alchemy-sdd:execute-tasks --task-group payments --max-parallel 3 --retries 1
```

## Reference Files

- `references/orchestration.md` - 10-step orchestration loop with execution plan, retry handling, and session summary
- `references/execution-workflow.md` - Detailed phase-by-phase procedures for the 4-phase workflow
- `references/verification-patterns.md` - Task classification, criterion verification, pass/fail rules, and failure reporting format
