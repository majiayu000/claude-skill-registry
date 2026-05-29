---
name: frappe-syntax-scheduler
description: >
  Use when configuring scheduler events and background jobs in Frappe/ERPNext
  v14/v15/v16. Covers scheduler_events in hooks.py, frappe.enqueue() for
  async jobs, queue configuration, job deduplication, error handling, and
  monitoring. Keywords: scheduler, background job, cron, RQ worker, job
  queue, async task, frappe.enqueue, scheduled task.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Scheduler & Background Jobs

Deterministic syntax reference for Frappe scheduler events and background job processing via Redis Queue (RQ).

## Decision Tree

```
Need periodic execution?
├─ Fixed interval (hourly/daily/weekly/monthly) → scheduler_events in hooks.py
├─ Custom cron schedule → scheduler_events.cron in hooks.py
├─ User-configurable interval → Scheduled Job Type DocType
└─ No, triggered by user/event
   ├─ Run method on a specific document → frappe.enqueue_doc()
   ├─ Run standalone function async → frappe.enqueue()
   └─ Run from controller on self → self.queue_action()
```

## Quick Reference: Scheduler Events (hooks.py)

```python
# hooks.py — ALWAYS run bench migrate after changes
scheduler_events = {
    # Standard events (default queue)
    "all": ["myapp.tasks.every_tick"],           # Every tick [v14: 240s, v15+: 60s]
    "hourly": ["myapp.tasks.hourly_task"],
    "daily": ["myapp.tasks.daily_task"],
    "weekly": ["myapp.tasks.weekly_task"],
    "monthly": ["myapp.tasks.monthly_task"],

    # Long queue events (for heavy processing)
    "hourly_long": ["myapp.tasks.hourly_heavy"],
    "daily_long": ["myapp.tasks.daily_heavy"],
    "weekly_long": ["myapp.tasks.weekly_heavy"],
    "monthly_long": ["myapp.tasks.monthly_heavy"],

    # Cron events (croniter-compatible syntax)
    "cron": {
        "*/15 * * * *": ["myapp.tasks.every_15_min"],
        "0 9 * * 1-5": ["myapp.tasks.weekday_9am"],
        "0 0 1 * *": ["myapp.tasks.first_of_month"],
    }
}
```

**CRITICAL**: ALWAYS run `bench migrate` after ANY change to scheduler_events. Without it, changes are NOT applied.

## Scheduler Event Types

| Event | Frequency | Queue | Use Case |
|-------|-----------|-------|----------|
| `all` | Every tick [v14: 4min, v15+: 60s] | default | Frequent polling |
| `hourly` | Once per hour | default | Sync, cleanup |
| `daily` | Once per day | default | Reports, summaries |
| `weekly` | Once per week | default | Archival |
| `monthly` | Once per month | default | Billing, statements |
| `hourly_long` | Once per hour | **long** | Heavy sync |
| `daily_long` | Once per day | **long** | Large exports |
| `weekly_long` | Once per week | **long** | Data warehousing |
| `monthly_long` | Once per month | **long** | Annual reports |
| `cron` | Custom schedule | configurable | Any custom timing |

## Cron Syntax

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

| Symbol | Meaning | Example |
|--------|---------|---------|
| `*` | Any value | `* * * * *` = every minute |
| `,` | List | `1,15 * * * *` = minute 1 and 15 |
| `-` | Range | `0 9-17 * * *` = hours 9 through 17 |
| `/` | Interval | `*/10 * * * *` = every 10 minutes |

Common patterns:
- Every 5 min: `*/5 * * * *`
- Weekdays at 9:00: `0 9 * * 1-5`
- Monday at 8:00: `0 8 * * 1`
- Business hours hourly: `0 9-17 * * 1-5`

## Quick Reference: frappe.enqueue()

```python
frappe.enqueue(
    method,                      # REQUIRED: function or "dotted.module.path"
    queue="default",             # "short", "default", "long", or custom
    timeout=None,                # Override queue timeout (seconds)
    is_async=True,               # False = run synchronously (skip worker)
    now=False,                   # True = run via frappe.call() directly
    job_id=None,                 # [v15+] Unique ID for deduplication
    enqueue_after_commit=False,  # Wait for DB commit before enqueue
    at_front=False,              # Place at front of queue
    on_success=None,             # Success callback
    on_failure=None,             # Failure callback
    **kwargs                     # Arguments passed to method
)
```

## Queue Types

| Queue | Default Timeout | Use When |
|-------|-----------------|----------|
| `short` | 300s (5 min) | Task < 30 seconds |
| `default` | 300s (5 min) | Task 30s - 5 min |
| `long` | 1500s (25 min) | Task 5 - 25 min |
| `long` + custom timeout | user-defined | Task > 25 min |

```python
# Short queue — quick status update
frappe.enqueue("myapp.tasks.update_status", queue="short", doc=doc.name)

# Long queue — heavy report generation
frappe.enqueue("myapp.tasks.generate_report", queue="long", timeout=3600)
```

## frappe.enqueue_doc()

Enqueue a controller method on a specific document.

```python
frappe.enqueue_doc(
    "Sales Invoice",              # DocType
    "SINV-00001",                 # Document name
    "send_notification",          # Controller method name
    queue="long",
    timeout=600,
    recipient="user@example.com"  # kwargs passed to method
)
```

The controller method MUST be decorated with `@frappe.whitelist()`:

```python
class SalesInvoice(Document):
    @frappe.whitelist()
    def send_notification(self, recipient):
        # self is the loaded document
        pass
```

## self.queue_action()

Alternative from within a controller:

```python
class SalesOrder(Document):
    def on_submit(self):
        self.queue_action("send_emails", emails=email_list)

    def send_emails(self, emails):
        for email in emails:
            send_mail(email)
```

## Job Deduplication

### [v15+] Recommended Pattern

```python
from frappe.utils.background_jobs import is_job_enqueued

job_id = f"import::{doc.name}"
if not is_job_enqueued(job_id):
    frappe.enqueue(
        "myapp.tasks.import_data",
        job_id=job_id,
        doc_name=doc.name
    )
else:
    frappe.msgprint("Import already in progress")
```

### [v14] Legacy Pattern (NEVER use in new code)

```python
from frappe.core.page.background_jobs.background_jobs import get_info
enqueued = [d.get("job_name") for d in get_info()]
if name not in enqueued:
    frappe.enqueue(..., job_name=name)
```

## Error Handling Pattern

ALWAYS use try/except with commit/rollback per record in batch jobs:

```python
def process_records(records):
    success, errors = 0, 0
    for record in records:
        try:
            process_single(record)
            frappe.db.commit()
            success += 1
        except Exception:
            frappe.db.rollback()
            frappe.log_error(
                frappe.get_traceback(),
                f"Process Error: {record}"
            )
            errors += 1
    return {"success": success, "errors": errors}
```

## Retry Pattern

```python
def task_with_retry(data, retry_count=0, max_retries=3):
    try:
        external_api_call(data)
    except Exception:
        if retry_count < max_retries:
            frappe.enqueue(
                "myapp.tasks.task_with_retry",
                queue="default",
                data=data,
                retry_count=retry_count + 1,
                max_retries=max_retries,
                enqueue_after_commit=True
            )
            frappe.log_error(f"Retry {retry_count+1}/{max_retries}", "Task Retry")
        else:
            frappe.log_error(frappe.get_traceback(), f"Failed after {max_retries} retries")
            raise
```

## Callbacks

```python
def on_success_handler(job, connection, result, *args, **kwargs):
    frappe.publish_realtime("show_alert", {"message": "Done!"})

def on_failure_handler(job, connection, type, value, traceback):
    frappe.log_error(f"Job {job.id} failed: {value}", "Job Error")

frappe.enqueue(
    "myapp.tasks.risky_task",
    on_success=on_success_handler,
    on_failure=on_failure_handler,
)
```

## Progress Updates

```python
def long_task(items, user):
    total = len(items)
    for i, item in enumerate(items):
        process_item(item)
        frappe.publish_realtime(
            "task_progress",
            {"progress": (i + 1) / total * 100, "current": i + 1, "total": total},
            user=user,
        )
```

## User Context

**CRITICAL**: Scheduler jobs run as **Administrator**. ALWAYS set explicit ownership when creating documents:

```python
def scheduled_task():
    doc = frappe.new_doc("ToDo")
    doc.owner = "user@example.com"
    doc.insert(ignore_permissions=True)
```

## Monitoring

| Tool | Purpose |
|------|---------|
| `bench doctor` | Scheduler status, worker health |
| RQ Worker (DocType) | Worker status: busy/idle |
| RQ Job (DocType) | Job status, queue filtering |
| Scheduled Job Log (DocType) | Execution history, errors |
| `logs/worker.error.log` | Worker exceptions |
| `logs/scheduler.log` | Scheduler activity |

## Version Differences

| Feature | v14 | v15+ |
|---------|-----|------|
| Tick interval (`all` event) | ~240s (4 min) | ~60s |
| Config key for tick | `scheduler_interval` | `scheduler_tick_interval` |
| Deduplication | `job_name` (deprecated) | `job_id` + `is_job_enqueued()` |

Custom tick in `common_site_config.json`:

```json
{ "scheduler_tick_interval": 120 }
```

## Critical Rules

1. **ALWAYS** run `bench migrate` after any scheduler_events change in hooks.py
2. **ALWAYS** use `job_id` + `is_job_enqueued()` for deduplication [v15+]
3. **ALWAYS** choose the correct queue: short/default/long based on task duration
4. **ALWAYS** commit per record and rollback on error in batch jobs
5. **ALWAYS** remember that scheduler jobs run as Administrator
6. **NEVER** run heavy logic directly in a scheduler event — enqueue it instead
7. **NEVER** use `job_name` for deduplication in new code (v14 legacy)

## Reference Files

- **[scheduler-events.md](references/scheduler-events.md)**: All event types, cron syntax, configuration
- **[enqueue-api.md](references/enqueue-api.md)**: Complete frappe.enqueue / enqueue_doc API
- **[queues.md](references/queues.md)**: Queue types, timeouts, custom queues, workers
- **[monitoring.md](references/monitoring.md)**: RQ DocTypes, bench doctor, log files, alerts
- **[error-handling.md](references/error-handling.md)**: Error patterns, retry, batch processing
- **[examples.md](references/examples.md)**: Complete working examples
- **[anti-patterns.md](references/anti-patterns.md)**: Common mistakes and corrections

## See Also

- `frappe-syntax-hooks` — Full hooks.py reference
- `frappe-core-background` — Background job architecture
- `frappe-errors-jobs` — Job failure debugging
