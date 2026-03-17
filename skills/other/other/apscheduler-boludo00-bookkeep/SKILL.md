---
name: apscheduler
description: |
  Configures background job scheduling and task execution with APScheduler 3.x in FastAPI.
  Use when: adding new background jobs, modifying job intervals, implementing job state persistence, handling job events, or debugging scheduler issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# APScheduler Skill

Bookkeep uses APScheduler 3.x with `AsyncIOScheduler` for background job execution. Jobs are registered at startup via `initialize_jobs()`, persisted to `JobSchedule` table, and exposed through `/api/jobs/` endpoints for runtime control.

## Quick Start

### Define a New Job

```python
# backend/app/scheduler.py - Add to JOB_DEFINITIONS
JOB_DEFINITIONS = {
    "my_new_job": {
        "default_interval": 60 * 60,  # 1 hour
        "description": "Description for UI/logs",
        "type": "PROCESS",
    },
    # ... existing jobs
}
```

### Implement the Job Function

```python
# backend/app/tasks.py
async def my_new_job():
    """Background task description"""
    db: Session = SessionLocal()
    try:
        # Do work
        logger.info("my_new_job_complete", processed=count)
    except Exception as e:
        logger.error("my_new_job_error", error=str(e))
        db.rollback()
    finally:
        db.close()
```

### Register in initialize_jobs()

```python
# backend/app/scheduler.py - Add to job_functions dict
from app.tasks import my_new_job

job_functions = {
    "my_new_job": my_new_job,
    # ... existing mappings
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `AsyncIOScheduler` | Main scheduler for async jobs | `scheduler = AsyncIOScheduler()` |
| `IntervalTrigger` | Time-based job execution | `IntervalTrigger(seconds=300)` |
| `MemoryJobStore` | In-memory job storage | `jobstores={'default': MemoryJobStore()}` |
| `JobSchedule` model | Persist intervals/state to DB | See the **sqlalchemy** skill |
| `coalesce=True` | Combine missed executions | Prevents job pileup after downtime |
| `max_instances=1` | Single concurrent execution | Prevents overlapping job runs |

## Common Patterns

### Trigger Job Immediately

```python
from app.scheduler import run_job_now
run_job_now("sync_from_booklore")  # Modifies next_run_time to now
```

### Reschedule with New Interval

```python
from app.scheduler import reschedule_job
reschedule_job("refresh_seed_data", 12 * 60 * 60)  # 12 hours
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **python** skill for async patterns and error handling
- See the **sqlalchemy** skill for `JobSchedule` model and database sessions
- See the **fastapi** skill for router endpoints in `routers/jobs.py`