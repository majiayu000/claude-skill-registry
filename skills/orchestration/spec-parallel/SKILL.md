---
name: spec-parallel
description: Auto-detect and parallelize Spec Kit tasks
triggers:
  - /tasks completes
  - tasks.md updated
  - "parallelize spec"
  - "spawn spec tasks"
---

# Spec Kit Parallel Executor

I automatically detect when Spec Kit tasks have parallel-eligible items and offer to spawn agents.

## Activation

I activate when:
- `/tasks` command completes
- User explicitly requests spec parallelization
- `.spec/tasks.md` is updated with new tasks

## Detection Logic

```python
def should_parallelize(tasks_file):
    tasks = parse_tasks(tasks_file)
    parallel_tasks = [t for t in tasks if "[P]" in t or "(P)" in t]
    return len(parallel_tasks) >= 3
```

## Spec Context

I include all Spec Kit artifacts in each agent's context:

| File | Purpose | Required |
|------|---------|----------|
| `.spec/spec.md` | Feature specification | Yes |
| `.spec/plan.md` | Implementation plan | Recommended |
| `.spec/design.md` | Design decisions | Optional |
| `.spec/tasks.md` | Task breakdown | Yes |

## Agent Prompt Template

```
You are a Spec Kit implementation agent.

## Your Task
{task_description}

## Feature Specification
{spec_content}

## Implementation Plan
{plan_content}

## Design Decisions
{design_content}

## Instructions
1. Implement ONLY the assigned task
2. Follow the specification exactly
3. Adhere to the implementation plan
4. Write tests for new functionality
5. Commit with message: "feat(spec): {task_name}"
6. Output TASK_COMPLETE when done

Begin implementation.
```

## Files

- `spawn-tasks.sh` - Parse tasks and spawn agents

## Integration with Base

This skill extends the base `parallel-executor` skill:
- Uses same worktree pattern
- Same monitoring commands
- Same merge workflow

## Spec Validation

After tasks complete, I can validate against spec:
```bash
# Check each worktree's implementation
for wt in ../project-*; do
    claude -p "Validate implementation in $wt against .spec/spec.md" --print
done
```
