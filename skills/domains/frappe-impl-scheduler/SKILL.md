---
name: frappe-impl-scheduler
description: >
  Use when implementing scheduled tasks and background jobs in Frappe
  v14/v15/v16. Covers hooks.py scheduler_events, frappe.enqueue, queue
  selection, job deduplication, testing with bench execute/scheduler,
  monitoring via Scheduled Job Log and RQ Dashboard, error handling,
  long-running job patterns, email digest, data cleanup, and report
  generation. Keywords: schedule task, background job, cron job, async
  processing, queue selection, job deduplication, scheduler implementation.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Scheduler & Background Jobs - Implementation

Workflow for implementing scheduled tasks and background jobs. For exact syntax, see `frappe-syntax-scheduler`.

**Version**: v14/v15/v16 compatible

---

## Main Decision: scheduler_events vs frappe.enqueue

```
WHAT ARE YOU BUILDING?
|
+-- Runs at fixed intervals/times?
|   +-- YES --> scheduler_events (hooks.py)
|   |           Task receives NO arguments
|   |           See: Workflow 1-2
|   |
|   +-- NO --> Triggered by user action or code?
|              +-- YES --> frappe.enqueue()
|              |           Pass any serializable data
|              |           See: Workflow 3-4
|              |
|              +-- NO --> Reconsider requirements
```

| Aspect | scheduler_events | frappe.enqueue |
|--------|------------------|----------------|
| Triggered by | Time/interval | Code execution |
| Defined in | hooks.py | Python code |
| Arguments | NONE (must be parameterless) | Any serializable data |
| Use case | Daily cleanup, hourly sync | User-triggered long task |
| Queue control | Event suffix (_long) | queue= parameter |
| Restart behavior | Runs on schedule | Lost if worker restarts |

---

## Which Scheduler Event Type?

| Need | Event Key | Queue |
|------|-----------|-------|
| Every scheduler tick | `all` | short (NEVER >60s) |
| Hourly (<5 min) | `hourly` | short |
| Hourly (5-25 min) | `hourly_long` | long |
| Daily (<5 min) | `daily` | short |
| Daily (5-25 min) | `daily_long` | long |
| Weekly (<5 min) | `weekly` | short |
| Weekly (5-25 min) | `weekly_long` | long |
| Monthly (<5 min) | `monthly` | short |
| Monthly (5-25 min) | `monthly_long` | long |
| Custom schedule | `cron["expr"]` | short |

**Rule**: ALWAYS use `*_long` suffix for tasks exceeding 5 minutes.

---

## Which Queue for frappe.enqueue?

| Queue | Default Timeout | Use For |
|-------|-----------------|---------|
| `short` | 300s (5 min) | Quick operations (<1 min) |
| `default` | 300s (5 min) | Standard tasks (1-5 min) |
| `long` | 1500s (25 min) | Heavy processing (>5 min) |

**Rule**: ALWAYS specify `queue=` explicitly. NEVER rely on the default.

---

## Implementation Step 1: Scheduler Event

```python
# myapp/tasks.py
import frappe

def daily_cleanup():
    """Daily cleanup - NO parameters allowed."""
    cutoff = frappe.utils.add_days(frappe.utils.nowdate(), -30)
    frappe.db.delete("Error Log", {"creation": ("<", cutoff)})
    frappe.db.commit()
```

```python
# hooks.py
scheduler_events = {
    "daily": ["myapp.tasks.daily_cleanup"]
}
```

**After editing hooks.py**: ALWAYS run `bench migrate`.

---

## Implementation Step 2: Background Job (frappe.enqueue)

```python
# myapp/api.py
import frappe
from frappe.utils.background_jobs import is_job_enqueued

@frappe.whitelist()
def process_documents(doctype, filters):
    job_id = f"process_{doctype}_{frappe.session.user}"

    if is_job_enqueued(job_id):
        return {"message": "Already in progress"}

    frappe.enqueue(
        "myapp.tasks.process_batch",
        queue="long",
        timeout=1800,
        job_id=job_id,
        enqueue_after_commit=True,
        doctype=doctype,
        filters=filters
    )
    return {"status": "queued"}
```

---

## Testing Scheduled Tasks

### Method 1: bench execute (direct)
```bash
# Run the function directly (no queue involved)
bench --site mysite execute myapp.tasks.daily_cleanup
```

### Method 2: bench scheduler (full scheduler test)
```bash
# Check scheduler status
bench --site mysite scheduler status

# Enable scheduler
bench --site mysite scheduler enable

# Trigger all pending scheduler events NOW
bench --site mysite scheduler trigger

# Run specific event type
bench --site mysite execute frappe.utils.scheduler.trigger --args "['daily']"
```

### Method 3: bench console (interactive)
```python
bench --site mysite console
>>> frappe.enqueue("myapp.tasks.my_task", queue="short", now=True)
# now=True executes synchronously for testing
```

### Method 4: Check Scheduled Job Type
```
1. Go to: Setup > Scheduled Job Type
2. Find: myapp.tasks.daily_cleanup
3. Verify: Frequency correct, Stopped = No
4. Click "Run Now" to trigger manually
```

---

## Monitoring

### Scheduled Job Log (UI)
```
Setup > Scheduled Job Log
- Shows every scheduler run with status
- Filter by: status (Success/Failed), creation date
- Check execution time to detect slow tasks
```

### RQ Dashboard
```bash
# Start RQ monitor (development)
bench --site mysite rq-dashboard
# Opens at http://localhost:9181

# Show background job status
bench --site mysite show-pending-jobs
bench --site mysite show-failed-jobs
```

### Programmatic Health Check
```python
def scheduler_health_check():
    failed = frappe.db.count("Scheduled Job Log", {
        "status": "Failed",
        "creation": [">=", frappe.utils.add_to_date(None, hours=-1)]
    })
    if failed > 5:
        frappe.sendmail(
            recipients=["admin@example.com"],
            subject="Scheduler Alert: Many failures",
            message=f"{failed} scheduler jobs failed in last hour"
        )
```

---

## Error Handling in Scheduled Tasks

### Per-Record Error Isolation
```python
def sync_all_orders():
    orders = get_pending_orders()
    success, errors = 0, 0

    for order in orders:
        try:
            sync_to_external(order)
            success += 1
        except Exception as e:
            errors += 1
            frappe.db.rollback()
            frappe.log_error(
                f"Sync failed for {order}: {e}",
                "Order Sync Error"
            )
    frappe.db.commit()
    frappe.logger("sync").info(f"{success} ok, {errors} errors")
```

**Rule**: ALWAYS wrap per-record processing in try-except. NEVER let one failure stop the entire batch.

---

## Long-Running Job Patterns

### Self-Chaining Pattern (>25 min tasks)
```python
def process_batch(offset=0, batch_size=500, total=None):
    if total is None:
        total = frappe.db.count("Sales Invoice", {"custom_processed": 0})

    records = frappe.get_all("Sales Invoice",
        filters={"custom_processed": 0},
        pluck="name", limit=batch_size)

    if not records:
        return  # Done

    for name in records:
        process_single(name)
    frappe.db.commit()

    remaining = frappe.db.count("Sales Invoice", {"custom_processed": 0})
    if remaining > 0:
        frappe.enqueue(
            "myapp.tasks.process_batch",
            queue="long",
            offset=offset + batch_size,
            batch_size=batch_size,
            total=total
        )
```

**Rule**: ALWAYS split tasks >25 min into self-chaining batches.

---

## Common Implementation Patterns

### Email Digest (weekly summary)
```python
# hooks.py
scheduler_events = {
    "cron": {
        "0 8 * * 1": ["myapp.newsletter.send_weekly_digest"]
    }
}
```
See `references/examples.md` Example 4 for complete implementation.

### Data Cleanup (daily maintenance)
```python
scheduler_events = {
    "daily_long": ["myapp.maintenance.daily_database_maintenance"]
}
```
See `references/examples.md` Example 1 for batch deletion pattern.

### Report Generation (user-triggered)
```python
frappe.enqueue(
    "myapp.tasks.generate_report",
    queue="long",
    timeout=3600,
    job_id=f"report::{frappe.session.user}",
    user=frappe.session.user
)
```
See `references/workflows.md` Workflow 6 for progress reporting.

---

## Critical Rules

1. **Scheduler tasks receive NO arguments** - Use settings or hardcoded values
2. **ALWAYS `bench migrate` after hooks.py changes** - Required to register events
3. **Jobs run as Administrator** - ALWAYS commit explicitly
4. **Commit in batches** - NEVER per-record (every 100-500 records)
5. **ALWAYS use `job_id` for user-triggered jobs** - Prevents duplicates
6. **Use `enqueue_after_commit=True`** from document events - Ensures data exists
7. **Scheduler events should be thin** - Enqueue heavy work to background

## Version Differences

| Aspect | v14 | v15 | v16 |
|--------|-----|-----|-----|
| Tick interval | 240s | 60s | 60s |
| Job dedup param | `job_name` | `job_id` | `job_id` |
| `enqueue_doc()` | Yes | Yes | Yes |
| Custom queues | No | Yes | Yes |

---

## Reference Files

| File | Contents |
|------|----------|
| [workflows.md](references/workflows.md) | 8 step-by-step implementation patterns |
| [decision-tree.md](references/decision-tree.md) | Detailed decision flowcharts |
| [examples.md](references/examples.md) | 5 complete working examples |
| [anti-patterns.md](references/anti-patterns.md) | 14 common mistakes to avoid |

## See Also

- `frappe-syntax-scheduler` - Exact syntax reference for hooks and enqueue
- `frappe-errors-serverscripts` - Error handling patterns
- `frappe-impl-hooks` - Hook configuration patterns
- `frappe-ops-bench` - Bench commands for scheduler management
- `frappe-ops-performance` - Performance tuning for background jobs
- `frappe-testing-unit` - Testing scheduled task logic
