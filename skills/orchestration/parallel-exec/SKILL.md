---
name: parallel-exec
description: Automatic task decomposition with parallel agent execution. Use when: breaking down complex tasks, parallel agent work, multi-file changes, optimizing execution time, task decomposition, understanding parallel execution phases.
---

# Parallel Exec

Automatically decomposes tasks and executes with parallel agents.

## Usage

```
Skill(skill="parallel-exec", args="Implement login feature with UI, backend, and tests")
```

## What It Does

1. **Analyzes** the task description for parallelizable work items
2. **Decomposes** into independent subtasks
3. **Builds** a dependency graph
4. **Identifies** parallelizable groups
5. **Executes** with optimal parallelism
6. **Aggregates** results with timing/metrics

## Options

Pass options as a JSON string or comma-separated:

```
Skill(skill="parallel-exec", args='{"task": "Implement X", "parallel": true, "dry_run": false}')
```

Or simple form:
```
Skill(skill="parallel-exec", args="Implement login feature")
```

## Output

```
## Decomposition Result

Original Task: [task description]

### Subtasks (N)
1. [EXPLORE] Explore codebase patterns
2. [ARCHITECT] Design architecture
3. [BUILDER] Implement backend logic
4. [UI] Design login dialog
5. [QUALITY] Write tests
6. [REVIEWER] Code review

### Execution Plan
- Phase 1 (Parallel): subtask_1, subtask_2, subtask_3
- Phase 2 (Sequential): subtask_4
- Phase 3 (Parallel): subtask_5, subtask_6

### Results
- Status: completed/partial/failed
- Total time: X ms
- Parallel groups: N
- Estimated savings: X ms
```

## Parallel Opportunities

| Task Pattern | Detected Work | Parallel Phases |
|--------------|---------------|-----------------|
| "Implement X with Y and Z" | 3 components | Explore (×3) → Architect → Implement (×3) → Tests + Review |
| "Add feature for layer A and B" | 2 layers | Explore A + B → Implement A + B |
| "Fix bug in X and add tests" | Bug + Tests | Explore → Fix → Tests (sequential) |

## Integration

Uses the unified ChainExecutor with parallel mode:

```python
from casare_rpa.domain.services import ChainExecutor

executor = ChainExecutor(orchestrator, enable_parallel=True)
result = await executor.execute("Implement login feature", parallel=True)
```
