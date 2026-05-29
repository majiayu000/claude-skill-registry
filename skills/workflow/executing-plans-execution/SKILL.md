---
name: executing-plans-execution
description: Detailed execution logic for the executing-plans skill
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
  - Write
  - Task
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Execution Phase Details

This document contains detailed execution logic for the executing-plans skill.

## Step 2: Execute Batch

**Default: First 3 tasks** (or use dependency graph for collab workflow)

### Standard Execution (No Dependency Graph)

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 2.1: Per-Task Execution with Item Type Routing

Before executing each task, determine its item type and follow the appropriate execution path.

**Determine Item Type:**
1. Read design doc
2. Find the work item that this task belongs to
3. Check the `Type:` field from the work item
4. Map to execution flow

**Routing Logic:**

```
FUNCTION executeTask(task, itemType):
  IF itemType == "task":
    # Skip TDD for operational tasks
    EXECUTE task steps directly (from task-planning Prerequisites/Steps/Verification)
    RUN verification checks
    MARK task as complete if verification passes
  ELSE IF itemType IN ["code", "bugfix"]:
    # Normal TDD flow
    INVOKE test-driven-development skill
    WRITE failing test
    IMPLEMENT code per design spec
    VERIFY test passes
    MARK task as complete
  ELSE:
    STOP - unknown item type, ask user
```

**For Task Type Items:**
1. Execute prerequisites validation (verify all prerequisites exist)
2. Execute each step in order (run commands/actions)
3. Run verification checks (confirm success)
4. Mark task as complete

**For Code/Bugfix Type Items:**
1. Invoke test-driven-development skill
2. Work through red-green-refactor cycle
3. Mark task as complete

### Dependency-Aware Execution (Collab Workflow)

When a task dependency graph is present, use intelligent parallel dispatch:

**Find Ready Tasks:**
```
ready_tasks = tasks where:
  - status is "pending"
  - all depends-on tasks are in "completed"
```

**Parallel Dispatch Logic:**
1. From ready tasks, identify parallel-safe group:
   - Tasks explicitly marked `parallel: true`
   - OR tasks with no file overlap and no shared dependencies
2. If multiple parallel-safe tasks exist:
   - Update task diagram: set all parallel tasks to "executing"
   - **REQUIRED:** Spawn Task agents in parallel (single message, multiple tool calls)
   - Each Task agent MUST invoke `mermaid-collab:subagent-driven-development:implementer-prompt` skill
   - Task prompt includes: task ID, files, description, relevant pseudocode
   - Wait for all agents to complete
   - Update task diagram: completed → "completed", failed → "failed"
3. If only sequential tasks remain:
   - Execute one at a time in topological order
   - Update diagram before/after each task

**RED FLAG - INLINE IMPLEMENTATION:**
If you find yourself using Edit/Write tools directly on source files instead of spawning Task agents, you are violating the subagent requirement. STOP and use Task tool instead.

### Task Agent Prompt Template (Collab Workflow)

```
You are implementing a task from the collab workflow.

## Design Document Location
Collab Session: .collab/<session-name>

**Per-item documents (read these for your task's context):**
- Interface: .collab/<session-name>/documents/interface-item-<N>.md
- Pseudocode: .collab/<session-name>/documents/pseudocode-item-<N>.md
- Skeleton: .collab/<session-name>/documents/skeleton-item-<N>.md

## REQUIRED: Read Per-Item Documents First
Before implementing, read the per-item documents for your work item:
1. Read interface-item-<N>.md → function signatures, types, file paths
2. Read pseudocode-item-<N>.md → step-by-step logic for your task
3. Read skeleton-item-<N>.md → task graph and planned files

These documents are the SOURCE OF TRUTH. Follow them exactly.

## Task Details
Task ID: <task-id>
Item Number: <item-number>
Files: <task-files>
Description: <task-description>

## Your Task's Design Spec
Interface:
<paste from interface-item-<N>.md>

Pseudocode:
<paste from pseudocode-item-<N>.md>

## Instructions
1. Read the per-item documents above
2. Implement EXACTLY as specified - no interpretation
3. Write tests
4. Report what you implemented
```

### Task Prompt with Test Patterns

When dispatching tasks, include the `tests` field in the prompt:

```
## Targeted Tests

During TDD (RED-GREEN-REFACTOR), run ONLY these tests:
{task.tests}

Command: npm run test:ci -- {tests joined by space}

Do NOT run the full test suite during TDD cycles.
```

### Task Completion Handling

When a task completes:
1. Move task from `in_progress` to `completed`
2. Check what tasks are now unblocked (their `depends-on` all satisfied)
3. Add newly unblocked tasks to the ready queue
4. Repeat until all tasks done

### Wave Completion Checkpoint

After all tasks in a wave complete:

1. Run full test suite:
   ```bash
   npm run test:ci
   ```

2. If tests fail:
   ```
   Full test suite failed after wave completion.
   Investigate failures before proceeding to next wave.
   ```
   STOP and report.

3. If tests pass:
   ```
   Full test suite passed. Proceeding to next wave.
   ```

**Example Execution Flow:**
```
Wave 1: [auth-types, utils] (parallel: true) → dispatch together
  ↓ both complete
Wave 2: [auth-service] (depends-on: auth-types) → dispatch
  ↓ complete
Wave 3: [auth-middleware] (depends-on: auth-service) → dispatch
```
