---
name: task-loop-verify
description: Verify the current task and output a completion marker. Use this to check if a task is complete and signal the stop hook to allow session exit.
version: 0.1.0
allowed-tools: Read, Glob, Grep, Bash(rm:*), Bash(jq:*), Task
---

# Task Loop Verification

Verify the current task in the loop and output a completion marker if successful. This skill wraps task-verifier and outputs the marker that the stop hook looks for.

## When to Use

Use this skill when:
- You've finished implementing a task and want to verify it
- The stop hook has triggered another loop iteration
- You want to exit the task loop cleanly

## Process

### Step 1: Read Loop State

First, check for the pointer file and get the state path:

```bash
if [[ -f .shipspec/active-loop.local.json ]]; then
  LOOP_TYPE=$(jq -r '.loop_type // empty' .shipspec/active-loop.local.json)
  if [[ "$LOOP_TYPE" == "task-loop" ]]; then
    jq -r '.state_path // empty' .shipspec/active-loop.local.json
  else
    echo "WRONG_LOOP_TYPE"
  fi
else
  echo "NO_POINTER"
fi
```

**If NO_POINTER or WRONG_LOOP_TYPE:**
> "No active task loop. Run `/implement-task <feature> <task-id>` to start a task."
> Stop here.

**If state_path found:**
Check the state file exists:
```bash
test -f [state_path] && echo "EXISTS" || echo "NO_STATE_FILE"
```

**If NO_STATE_FILE:**
Clean up stale pointer and report:
```bash
rm -f .shipspec/active-loop.local.json
```
> "No active task loop (stale pointer cleaned up). Run `/implement-task <feature> <task-id>` to start a task."
> Stop here.

**If found:**
Parse the JSON state file to extract:
```bash
jq -r '.feature // empty' [state_path]
jq -r '.task_id // empty' [state_path]
jq -r '.iteration // 0' [state_path]
jq -r '.max_iterations // 5' [state_path]
```

- `feature`: The feature directory name
- `task_id`: The task being implemented
- `iteration`: Current attempt number
- `max_iterations`: Maximum allowed attempts

**Store the state_path for cleanup later.**

### Step 2: Load Task Prompt

The task prompt is stored in TASKS.json, not in the state file.

Read the prompt from TASKS.json:
```bash
jq -r --arg id "[task_id]" '.tasks[$id].prompt // empty' .shipspec/planning/[feature]/TASKS.json
```

### Step 3: Run Verification

Delegate to the `task-verifier` agent with:
- The full task prompt (including acceptance criteria)
- The feature name
- The task ID

### Step 4: Handle Result

Based on task-verifier result:

#### VERIFIED

All acceptance criteria passed.

1. Clean up state file:
   ```bash
   rm -f [state_path] .shipspec/active-loop.local.json
   ```

2. Update TASKS.json: Use task-manager agent with `update_status` operation to set status to `completed`

3. Log completion to `.claude/shipspec-debug.log`:
   ```
   $(date -u +%Y-%m-%dT%H:%M:%SZ) | [task_id] | LOOP_END | VERIFIED after [iteration] attempts
   ```

4. **Output the completion marker:**
   `<task-loop-complete>VERIFIED</task-loop-complete>`

5. Tell user: "Task [task_id] verified! All acceptance criteria passed."

#### INCOMPLETE

Some criteria failed. Manual intervention required.

1. Clean up state file:
   ```bash
   rm -f [state_path] .shipspec/active-loop.local.json
   ```

2. Log the failure to `.claude/shipspec-debug.log`:
   ```
   $(date -u +%Y-%m-%dT%H:%M:%SZ) | [task_id] | LOOP_END | INCOMPLETE | [brief failure reason]
   ```

3. **Output the incomplete marker:**
   `<task-loop-complete>INCOMPLETE</task-loop-complete>`

4. Show the user what failed:
   > "## Verification Failed
   >
   > The following criteria are not met:
   > - [List failed criteria]
   >
   > Please fix these issues and run `/implement-task [feature]` again."

#### BLOCKED

Cannot verify due to infrastructure issues.

1. Clean up state file:
   ```bash
   rm -f [state_path] .shipspec/active-loop.local.json
   ```

2. Log to `.claude/shipspec-debug.log`:
   ```
   $(date -u +%Y-%m-%dT%H:%M:%SZ) | [task_id] | LOOP_END | BLOCKED | [reason]
   ```

3. **Output the blocked marker:**
   `<task-loop-complete>BLOCKED</task-loop-complete>`

4. Tell user: "Task verification is blocked: [reason]. Manual intervention required."

## Important Notes

1. **Completion markers are critical** - the stop hook looks for these to decide whether to allow session exit
2. **All results output markers** - VERIFIED, INCOMPLETE, and BLOCKED all output completion markers to exit the loop
3. **INCOMPLETE requires manual fix** - user must address issues and re-run `/implement-task`
4. **BLOCKED needs investigation** - tasks that can't be verified need manual attention
5. **State file cleanup** - always remove on any completion (VERIFIED, INCOMPLETE, or BLOCKED) to prevent stale loops
6. **Prompts in TASKS.json** - the task prompt is read from TASKS.json, not stored in the state file
