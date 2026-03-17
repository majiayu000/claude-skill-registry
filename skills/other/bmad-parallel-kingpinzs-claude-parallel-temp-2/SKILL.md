---
name: bmad-parallel
description: Auto-detect and parallelize BMAD story tasks
triggers:
  - /dev-story completes
  - story file updated
  - "parallelize story"
  - "spawn story tasks"
---

# BMAD Parallel Executor

I automatically detect when a BMAD story has parallel-eligible tasks and offer to spawn agents.

## Activation

I activate when:
- `/dev-story` command completes
- User explicitly requests story parallelization
- A story file is updated with new tasks

## Detection Logic

```python
def should_parallelize(story_file):
    tasks = parse_tasks(story_file)
    parallel_tasks = [t for t in tasks if is_parallel(t)]
    return len(parallel_tasks) >= 3
```

## BMAD Context

I include BMAD artifacts in each agent's context:

| File | Purpose |
|------|---------|
| `.bmad/prd.md` | Product requirements |
| `.bmad/architecture.md` | System design |
| `.bmad/tech-spec.md` | Technical specifications |
| Story file | Task context |

## Agent Prompt Template

```
You are a BMAD implementation agent.

## Your Task
{task_description}

## Story Context
{story_content}

## Project Artifacts
- PRD: {prd_summary}
- Architecture: {arch_summary}
- Tech Spec: {spec_summary}

## Instructions
1. Implement ONLY the assigned task
2. Follow existing code patterns
3. Write tests for new functionality
4. Commit with message: "feat(story): {task_name}"
5. Output TASK_COMPLETE when done

Begin implementation.
```

## Files

- `spawn-story.sh` - Parse story tasks and spawn agents

## Integration with Base

This skill extends the base `parallel-executor` skill:
- Uses same worktree pattern
- Same monitoring commands
- Same merge workflow
