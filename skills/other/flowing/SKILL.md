---
name: flowing
description: Lightweight DAG workflow runner with checkpoint resume and detachable tasks. Use when orchestrating 3+ sequential or parallel tool calls into a single invocation, or when pipelines need resume-from-failure without re-running succeeded steps.
metadata:
  version: 1.0.0
---

# Flowing — DAG Workflow Runner

Batch independent operations into one `python3` invocation. Declare steps, wire dependencies, run once.

## Quick Start

```python
from flowing import task, Flow

@task
def fetch_data():
    return {"items": [1, 2, 3]}

@task(depends_on=[fetch_data])
def process(fetch_data):
    return sum(fetch_data["items"])

@task(depends_on=[process])
def store(process):
    print(f"Result: {process}")

Flow(store).run()
```

## Core API

### `@task` decorator

```python
@task(
    depends_on=[other_task],  # DAG edges
    retry=2,                  # retry count (0 = no retry)
    retry_backoff_base_ms=1000,
    retry_max_backoff_ms=30_000,
    timeout_s=60.0,
    detached=True,            # non-blocking side-effect
    name="custom_name",       # override function name
)
def my_step(other_task):      # param name = dependency task name
    return result
```

### `Flow` class

```python
flow = Flow(terminal_task, max_workers=5, fail_fast=True)
results = flow.run()          # execute full DAG
flow.summary()                # human-readable status
flow.value(some_task)         # get succeeded task's return value
```

### Resume from failure

When a step fails mid-pipeline, fix the issue and continue without re-running succeeded steps:

```python
flow = Flow(terminal)
results = flow.run()                    # step_3 fails
flow.override(step_3, corrected_value)  # inject fix
results = flow.resume()                 # step_1, step_2 cached; step_4+ runs
```

- `flow.resume()`: Resets FAILED/SKIPPED tasks, keeps SUCCEEDED results cached
- `flow.override(task_def, value)`: Manually inject a succeeded result

### Detached tasks (non-blocking side-effects)

```python
@task(depends_on=[create_issue], detached=True)
def store_memory(create_issue):
    remember(create_issue["url"], ...)
```

- Run in a final layer after the main DAG completes
- Failures collected in `flow.detached_failures`, never trigger `fail_fast`
- Dependencies must all be SUCCEEDED (same as normal tasks)

## When to use

- 3+ independent operations (recall, SQL, web search) that can parallelize
- Multi-step pipelines where late failures shouldn't waste early work
- Side-effects (memory storage, notifications) that shouldn't block the critical path

## When NOT to use

- Next step depends on *reasoning* about prior result (use a think loop)
- Single sequential operation
- Async/distributed workflows (this is single-container, ThreadPoolExecutor)
