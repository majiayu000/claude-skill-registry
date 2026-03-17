---
name: ralph-loop
description: |
  Start a Ralph Wiggum autonomous task loop that keeps Claude working until a task
  is complete. Uses the Stop hook pattern to re-inject prompts when Claude tries
  to exit before finishing. Supports two completion strategies: promise-based
  (Claude outputs a completion token) and file-movement-based (task file moves to /Done).
  Use when a multi-step task requires Claude to iterate until completion, such as
  processing all items in /Needs_Action or generating a complete audit.
---

# Ralph Wiggum Autonomous Task Loop

Keep Claude working on a task autonomously until it reaches a defined completion state.

## How It Works

1. **Start**: Create a loop state file with the task prompt and completion criteria
2. **Iterate**: Claude works on the task
3. **Check**: At exit, the Stop hook checks if the task is complete
4. **Continue**: If not complete, the prompt is re-injected (up to max iterations)
5. **Done**: When complete (or max iterations hit), Claude is allowed to exit

## Two Completion Strategies

### Strategy 1: Promise-Based (Simple)
Claude outputs `<promise>TASK_COMPLETE</promise>` in its response to signal completion.

```
Example task prompt:
"Process all files in /Needs_Action.
When all items are processed and moved to /Done, output: <promise>TASK_COMPLETE</promise>"
```

### Strategy 2: File-Movement-Based (Gold Tier)
The Stop hook watches for a specific task file to move to `/Done`.
More reliable because completion is a natural part of the workflow.

```
Example: Start a loop watching for "TASK_20260223_inbox_sweep" in /Done
When the file appears in /Done, the loop exits naturally.
```

## Usage

### Start a Ralph Loop (Promise Strategy)
```python
from ralph_loop import RalphLoop

loop = RalphLoop(vault_path="./vault")
state = loop.start(
    prompt="Process all pending items in /Needs_Action. "
           "For each item, create a plan and move to /Done. "
           "When ALL items are processed, output: <promise>TASK_COMPLETE</promise>",
    completion_promise="TASK_COMPLETE",
    max_iterations=10,
)
print(f"Loop started: {state.task_id}")
```

### Start a Ralph Loop (File Movement Strategy)
```python
from ralph_loop import RalphLoop

loop = RalphLoop(vault_path="./vault")
state = loop.start(
    prompt="Generate this week's CEO briefing and save to vault/Briefings/. "
           "Move the trigger file to /Done when complete.",
    completion_file="TASK_briefing_trigger.md",
    max_iterations=5,
)
```

### Check Active Loops
```python
from ralph_loop import RalphLoop

loop = RalphLoop(vault_path="./vault")
active = loop.get_active_loops()
for state in active:
    print(f"Loop {state.task_id}: iteration {state.current_iteration}/{state.max_iterations}")
```

## Stop Hook Configuration

To use the Ralph Wiggum loop, configure the Stop hook in Claude Code settings.
The stop hook script at `src/ralph_loop.py` is called when Claude attempts to exit:

```bash
# In Claude Code settings (settings.json or CLAUDE.md):
# Add stop hook:
# python src/ralph_loop.py ./vault
```

The hook:
- Reads Claude's output from stdin
- Checks for completion promise OR looks for completion file in /Done
- Returns exit code 0 (allow exit) or 1 (block and re-inject prompt)

## Security Notes
- Max iterations prevent infinite loops (default: 10)
- All loop state stored in `vault/Logs/ralph_*.json` — visible audit trail
- Loop state files are deleted when loops complete
- Never loops on destructive operations without human approval first

## Example: Complete Inbox Processing Loop
```
/ralph-loop "Process all items in vault/Needs_Action in priority order (high → medium → low).
For each item:
1. Read the item's frontmatter
2. Create a Plan.md in vault/Plans/
3. If approval needed, create approval request in vault/Pending_Approval/
4. Otherwise, process and move to vault/Done/
When ALL items in vault/Needs_Action have been moved to vault/Done,
output: <promise>TASK_COMPLETE</promise>"
--max-iterations 15
```
