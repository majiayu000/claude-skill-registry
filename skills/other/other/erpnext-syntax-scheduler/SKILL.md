---
name: erpnext-syntax-scheduler
description: Scheduler and background jobs syntax for Frappe/ERPNext v14/v15/v16. Use for scheduler_events in hooks.py, frappe.enqueue() for async jobs, queue configuration, job deduplication, error handling, and monitoring. Triggers on questions about scheduled tasks, background processing, cron jobs, RQ workers, job queues, async tasks.
---

# ERPNext Syntax: Scheduler & Background Jobs

Deterministic syntax reference for Frappe scheduler events and background job processing.

## Quick Reference

### Scheduler Events (hooks.py)

```python
# hooks.py
scheduler_events = {
    "all": ["myapp.tasks.every_tick"],
    "hourly": ["myapp.tasks.hourly_task"],
    "daily": ["myapp.tasks.daily_task"],
    "weekly": ["myapp.tasks.weekly_task"],
    "monthly": ["myapp.tasks.monthly_task"],
    "daily_long": ["myapp.tasks.heavy_daily"],  # Long queue
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.weekday_9am"],
        "*/15 * * * *": ["myapp.tasks.every_15_min"]
    }
}
```

**CRITICAL**: After EVERY change to scheduler_events: `bench migrate`

### frappe.enqueue Basics

```python
# Simple
frappe.enqueue("myapp.tasks.process", customer="CUST-001")

# With queue and timeout
frappe.enqueue(
    "myapp.tasks.heavy_task",
    queue="long",
    timeout=3600,
    param="value"
)

# With deduplication (v15)
from frappe.utils.background_jobs import is_job_enqueued

job_id = f"import::{doc.name}"
if not is_job_enqueued(job_id):
    frappe.enqueue("myapp.tasks.import_data", job_id=job_id, doc=doc.name)
```

## Scheduler Event Types

| Event | Frequency | Queue |
|-------|-----------|-------|
| `all` | Every tick (v14: 4min, v15: 60s) | default |
| `hourly` | Per hour | default |
| `daily` | Per day | default |
| `weekly` | Per week | default |
| `monthly` | Per month | default |
| `hourly_long` | Per hour | **long** |
| `daily_long` | Per day | **long** |
| `weekly_long` | Per week | **long** |
| `monthly_long` | Per month | **long** |
| `cron` | Custom schedule | configurable |

**Version difference scheduler tick**:
- v14: ~240 seconds (4 min)
- v15: ~60 seconds

## Queue Types

| Queue | Timeout | Usage |
|-------|---------|-------|
| `short` | 300s (5 min) | Quick tasks, UI responses |
| `default` | 300s (5 min) | Standard tasks |
| `long` | 1500s (25 min) | Heavy processing, imports |

## frappe.enqueue Parameters

```python
frappe.enqueue(
    method,                      # REQUIRED: function or module path
    queue="default",             # Queue name
    timeout=None,                # Override timeout (seconds)
    is_async=True,               # False = execute directly
    now=False,                   # True = via frappe.call()
    job_id=None,                 # v15: unique ID for deduplication
    enqueue_after_commit=False,  # Wait for DB commit
    at_front=False,              # Place at front of queue
    on_success=None,             # Success callback
    on_failure=None,             # Failure callback
    **kwargs                     # Arguments for method
)
```

## Job Deduplication

### v15+ (Recommended)

```python
from frappe.utils.background_jobs import is_job_enqueued

job_id = f"process::{doc.name}"
if not is_job_enqueued(job_id):
    frappe.enqueue(
        "myapp.tasks.process",
        job_id=job_id,
        doc_name=doc.name
    )
```

### v14 (Deprecated)

```python
# DO NOT USE - only for legacy code
from frappe.core.page.background_jobs.background_jobs import get_info
enqueued = [d.get("job_name") for d in get_info()]
if name not in enqueued:
    frappe.enqueue(..., job_name=name)
```

## Error Handling Pattern

```python
def process_records(records):
    for record in records:
        try:
            process_single(record)
            frappe.db.commit()  # Commit per success
        except Exception:
            frappe.db.rollback()  # Rollback on error
            frappe.log_error(
                frappe.get_traceback(),
                f"Process Error: {record}"
            )
```

## Callbacks

```python
def on_success_handler(job, connection, result, *args, **kwargs):
    frappe.publish_realtime("show_alert", {"message": "Done!"})

def on_failure_handler(job, connection, type, value, traceback):
    frappe.log_error(f"Job {job.id} failed: {value}")

frappe.enqueue(
    "myapp.tasks.risky_task",
    on_success=on_success_handler,
    on_failure=on_failure_handler
)
```

## User Context

**IMPORTANT**: Scheduler jobs run as **Administrator**!

```python
def scheduled_task():
    # frappe.session.user = "Administrator"
    
    # Set explicit owner:
    doc = frappe.new_doc("ToDo")
    doc.owner = "user@example.com"
    doc.insert(ignore_permissions=True)
```

## Monitoring

| Tool | Description |
|------|-------------|
| RQ Worker (DocType) | Worker status, busy/idle |
| RQ Job (DocType) | Job status, queue filter |
| `bench doctor` | Scheduler status overview |
| Scheduled Job Log | Execution history |

## Version Differences v14 vs v15

| Feature | v14 | v15 |
|---------|-----|-----|
| Tick interval | 4 min | 60 sec |
| Config key | `scheduler_interval` | `scheduler_tick_interval` |
| Deduplication | `job_name` | `job_id` + `is_job_enqueued()` |

## Reference Files

- **[scheduler-events.md](references/scheduler-events.md)**: All event types, cron syntax, configuration
- **[enqueue-api.md](references/enqueue-api.md)**: Complete frappe.enqueue/enqueue_doc API
- **[queues.md](references/queues.md)**: Queue types, timeouts, custom queues, workers
- **[examples.md](references/examples.md)**: Complete working examples
- **[anti-patterns.md](references/anti-patterns.md)**: Common mistakes and corrections

## Critical Rules

1. **ALWAYS** `bench migrate` after hooks.py scheduler_events changes
2. **USE** `job_id` + `is_job_enqueued()` for deduplication (v15)
3. **CHOOSE** correct queue: short/default/long based on duration
4. **COMMIT** per successful record, rollback on error
5. **REMEMBER** that jobs run as Administrator
6. **ENQUEUE** heavy tasks from scheduler events, don't execute directly
