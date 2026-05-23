---
# VERSION: 2.43.0
name: parallel
description: "Run multiple Ralph loops concurrently for independent tasks. Manages parallel agent execution with proper isolation and result aggregation. Use when: (1) multiple independent fixes needed, (2) parallel reviews required, (3) batch processing tasks. Triggers: /parallel, 'parallel loops', 'concurrent execution', 'run in parallel', 'batch'."
context: fork
user-invocable: true
---

# Parallel - Concurrent Execution

Run multiple Ralph loops concurrently for independent tasks.

## Quick Start

```bash
/parallel "fix auth errors" "fix api errors" "fix ui errors"
ralph parallel task1 task2 task3
```

## When to Use

### Good for Parallel
- Independent file changes
- Multiple module fixes
- Batch reviews
- Different analysis types

### Must Be Sequential
- Dependent changes
- Same file modifications
- Order-dependent operations
- Shared state changes

## Workflow

### 1. Spawn Parallel Agents

```yaml
# Launch multiple background agents
Task:
  subagent_type: "code-reviewer"
  model: "sonnet"
  run_in_background: true
  prompt: "Review auth module"

Task:
  subagent_type: "code-reviewer"
  model: "sonnet"
  run_in_background: true
  prompt: "Review api module"

Task:
  subagent_type: "code-reviewer"
  model: "sonnet"
  run_in_background: true
  prompt: "Review ui module"
```

### 2. Monitor Progress

```yaml
# Check each task
TaskOutput:
  task_id: "<auth-task>"
  block: false

TaskOutput:
  task_id: "<api-task>"
  block: false
```

### 3. Aggregate Results

```yaml
# Wait for all to complete
TaskOutput:
  task_id: "<auth-task>"
  block: true

TaskOutput:
  task_id: "<api-task>"
  block: true
```

## Parallel Patterns

### Review Pattern
```bash
# Parallel reviews with different focus
/parallel "security review src/" "performance review src/" "quality review src/"
```

### Fix Pattern
```bash
# Parallel fixes for different modules
/parallel "fix auth errors" "fix api errors" "fix db errors"
```

### Analysis Pattern
```bash
# Parallel analysis tasks
/parallel "analyze complexity" "analyze coverage" "analyze dependencies"
```

## Isolation

Each parallel task runs with:
- Separate context (`context: fork`)
- Independent iteration counter
- Own quality gates
- Isolated file access

## Result Aggregation

### All Succeed
- Aggregate changes
- Run global gates
- VERIFIED_DONE

### Partial Success
- Report failures
- Keep successful changes
- Retry failed tasks

### All Fail
- Report all errors
- Analyze patterns
- Sequential retry

## Integration

- Used for independent sub-tasks
- Each parallel task follows Ralph Loop
- Results feed back to orchestrator

## Anti-Patterns

- Never run parallel on same files
- Never exceed 5 concurrent agents
- Never ignore partial failures
- Never skip aggregation step
