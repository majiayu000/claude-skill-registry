---
name: parallel-session-orchestration
description: Run multiple agent tasks in parallel cloud sandboxes with real-time progress monitoring, achieving 2x throughput vs sequential execution. Use for multi-repo tasks, independent bug fixes, concurrent feature development, or team workflows requiring parallel workstreams. Supports session management, result aggregation, and local teleport. Triggers on "parallel tasks", "multiple repos", "concurrent work", "parallel sessions", "multi-repo".
---

# Parallel Session Orchestration

## Purpose

Execute multiple agent tasks in parallel cloud sandboxes with real-time progress monitoring, achieving 2x throughput vs sequential execution.

## When to Use

- Multiple repository tasks
- Team workflows with parallel streams
- Independent bug fixes across projects
- Concurrent feature development
- Batch operations on multiple codebases

## Core Instructions

### Orchestration Pattern

```python
import asyncio

async def orchestrate_parallel(tasks):
    """
    Run multiple tasks in parallel sandboxes
    """
    sessions = []

    # Create sandbox session for each task
    for task in tasks:
        session = await create_sandbox_session(task)
        sessions.append(session)

    # Execute all in parallel
    results = await asyncio.gather(*[
        session.execute() for session in sessions
    ])

    # Aggregate results
    return merge_results(results)


async def create_sandbox_session(task):
    """
    Create isolated sandbox for task
    """
    return {
        'task': task,
        'sandbox_id': generate_sandbox_id(),
        'repo': clone_repo(task.repo_url),
        'execute': lambda: run_in_sandbox(task)
    }
```

### Progress Monitoring

```python
async def monitor_parallel_execution(sessions):
    """
    Monitor all sessions in real-time
    """
    while any(s.status == 'running' for s in sessions):
        for session in sessions:
            progress = await session.get_progress()
            print(f"{session.task.name}: {progress}%")

        await asyncio.sleep(1)

    return [s.result for s in sessions]
```

### Example Workflow

```python
tasks = [
    {
        'name': 'fix-auth-bug',
        'repo': 'https://github.com/org/repo-a',
        'instructions': 'Fix authentication timeout'
    },
    {
        'name': 'update-deps',
        'repo': 'https://github.com/org/repo-b',
        'instructions': 'Update dependencies to latest'
    },
    {
        'name': 'add-tests',
        'repo': 'https://github.com/org/repo-c',
        'instructions': 'Add unit tests for API'
    }
]

# Run all in parallel
results = await orchestrate_parallel(tasks)

# Results available simultaneously
# Time: max(task_times) instead of sum(task_times)
```

## Performance

- **2x throughput** vs sequential execution
- Real-time progress monitoring
- Isolated sandboxes prevent conflicts
- Results can be teleported to local

## Version

v1.0.0 (2025-10-23)

