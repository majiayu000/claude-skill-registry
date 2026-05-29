---
name: parallel-processing
description: Run multiple tasks in parallel using tmux windows
triggers: background tasks, parallel execution, concurrent work, multi-task, batch processing, async operations, running multiple commands
---

# Parallel Processing

Use tmux for background tasks and parallel work.

## Recommended: Use Subagents for Context Efficiency

**For simple parallel commands**, launch multiple `tmux-runner` subagents in parallel:

```python
# Launch all three in parallel (single message with multiple Task calls)
Task(subagent_type="tmux-runner", description="Run tests",
     prompt="Run 'npm test' and return results", model="haiku")
Task(subagent_type="tmux-runner", description="Run lint",
     prompt="Run 'npm run lint' and return results", model="haiku")
Task(subagent_type="tmux-runner", description="Run build",
     prompt="Run 'npm run build' and return results", model="haiku")
```

This saves context in the main conversation - you only see the results, not all the intermediate tmux operations.

## Pattern: Background Task (Direct)

For long-running servers you need to monitor:

```python
# Start background task
window_id = tmux_new_window(command="npm run dev", name="dev-server")

# Continue working...

# Check later
output = tmux_capture(target=window_id, lines=50)

# Clean up
tmux_kill(target=window_id)
```

## Pattern: With Notification

```python
window_id = tmux_new_window(command="npm run build", name="build")
status = tmux_wait_idle(target=window_id, timeout=300)
notify(title="Build Complete", message=f"Status: {status}")
```

## Pattern: Multiple Parallel (Direct)

When you need to manage windows yourself:

```python
test_win = tmux_new_window(command="npm test", name="tests")
lint_win = tmux_new_window(command="npm run lint", name="lint")
build_win = tmux_new_window(command="npm run build", name="build")

for w in [test_win, lint_win, build_win]:
    tmux_wait_idle(target=w, timeout=120)
```
