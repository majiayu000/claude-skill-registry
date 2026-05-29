---
name: erpnext-impl-scheduler
description: "Implementation workflows for Frappe scheduled tasks and background jobs (v14/v15/v16). Covers hooks.py scheduler_events, frappe.enqueue, queue selection, job deduplication, and error handling. Triggers: how to schedule task, background job, cron job, async processing, queue selection, job deduplication, scheduler implementation."
---

# ERPNext Scheduler - Implementation

This skill helps you implement scheduled tasks and background jobs. For exact syntax, see `erpnext-syntax-scheduler`.

**Version**: v14/v15/v16 compatible

## Main Decision: What Are You Trying to Do?

```
┌─────────────────────────────────────────────────────────────────────┐
│ SCHEDULER DECISION                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Run at fixed intervals or times?                                   │
│ ├── YES → Scheduler Event (hooks.py)                               │
│ │         See: references/workflows.md §1-2                        │
│ │                                                                   │
│ └── NO → Run in response to user action?                           │
│          ├── YES → frappe.enqueue()                                │
│          │         See: references/workflows.md §3-4               │
│          │                                                          │
│          └── NO → Probably neither - reconsider requirements       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Scheduler Event vs frappe.enqueue

| Aspect | Scheduler Event | frappe.enqueue |
|--------|----------------|----------------|
| Triggered by | Time/interval | Code execution |
| Defined in | hooks.py | Python code |
| Arguments | None (must be parameterless) | Any serializable data |
| Use case | Daily cleanup, hourly sync | User-triggered long task |
| Restart behavior | Runs on schedule | Lost if worker restarts |

## Which Scheduler Event Type?

```
┌─────────────────────────────────────────────────────────────────────┐
│ SCHEDULER EVENT TYPE                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Simple recurring interval?                                         │
│ ├── Every minute    → scheduler_events.cron["* * * * *"]          │
│ ├── Hourly          → scheduler_events.hourly                      │
│ ├── Daily           → scheduler_events.daily                       │
│ ├── Weekly          → scheduler_events.weekly                      │
│ └── Monthly         → scheduler_events.monthly                     │
│                                                                     │
│ Complex schedule (e.g., "weekdays at 9am")?                        │
│ └── scheduler_events.cron["0 9 * * 1-5"]                          │
│                                                                     │
│ Run after every request?                                           │
│ └── scheduler_events.all (use sparingly!)                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Which Queue?

| Queue | Timeout | Use For |
|-------|---------|---------|
| `short` | 5 min | Quick operations (<1 min) |
| `default` | 5 min | Standard tasks (1-3 min) |
| `long` | 30 min | Heavy processing (>3 min) |

**Rule**: Always specify queue explicitly. Default is `short`.

## Quick Start: Basic Scheduled Task

```python
# myapp/tasks.py
import frappe

def daily_cleanup():
    """Daily cleanup task - no parameters allowed"""
    frappe.db.delete("Error Log", {"creation": ("<", frappe.utils.add_days(None, -30))})
    frappe.db.commit()
```

```python
# hooks.py
scheduler_events = {
    "daily": [
        "myapp.tasks.daily_cleanup"
    ]
}
```

After editing hooks.py: `bench migrate`

## Quick Start: Background Job

```python
# myapp/api.py
import frappe
from frappe import enqueue

@frappe.whitelist()
def process_documents(doctype, filters):
    enqueue(
        "myapp.tasks.process_batch",
        queue="long",
        timeout=1800,
        job_id=f"process_{doctype}_{frappe.session.user}",  # v15+ dedup
        doctype=doctype,
        filters=filters
    )
    return {"status": "queued"}
```

## Critical Rules

### 1. Scheduler tasks receive NO arguments
```python
# ❌ WRONG
def my_task(doctype):  # Arguments not supported
    pass

# ✅ CORRECT
def my_task():  # Parameterless
    doctype = "Sales Invoice"  # Hardcode or read from settings
```

### 2. ALWAYS migrate after hooks.py changes
```bash
bench migrate  # Required to register new scheduler events
```

### 3. Jobs run as Administrator
Scheduler and enqueued jobs run with Administrator permissions. Always commit explicitly.

### 4. Commit after batches, not per record
```python
# ❌ WRONG - Slow
for doc in docs:
    doc.save()
    frappe.db.commit()  # Commit per record

# ✅ CORRECT - Fast
for doc in docs:
    doc.save()
frappe.db.commit()  # Single commit after batch
```

### 5. Use job_id for deduplication (v15+)
```python
enqueue(..., job_id="unique_identifier")  # Prevents duplicate jobs
```

## Version Differences

| Aspect | v14 | v15 | v16 |
|--------|-----|-----|-----|
| Tick interval | 4 min | 60 sec | 60 sec |
| Job dedup | `job_name` | `job_id` | `job_id` |
| Cron support | ✅ | ✅ | ✅ |

**V14 deduplication** uses different parameter:
```python
# v14
enqueue(..., job_name="unique_id")
# v15+
enqueue(..., job_id="unique_id")
```

---

## Reference Files

| File | Contents |
|------|----------|
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns |
| [decision-tree.md](references/decision-tree.md) | Detailed decision flowcharts |
| [examples.md](references/examples.md) | Complete working examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes to avoid |

---

## See Also

- `erpnext-syntax-scheduler` - Exact syntax reference
- `erpnext-errors-serverscripts` - Error handling patterns
