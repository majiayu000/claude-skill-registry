---
name: frappe-agent-debugger
description: >
  Use when debugging Frappe errors, using bench console for live inspection, analyzing tracebacks, or reading Frappe log files.
  Prevents wasted debugging time from ignoring log context, misreading tracebacks, and not using bench console effectively.
  Covers bench console, frappe.logger, error log DocType, traceback analysis, common error patterns, log file locations, pdb/debugger integration, VS Code DAP, profiling, Frappe Recorder, mariadb diagnostics.
  Keywords: debug, bench console, traceback, error log, frappe.logger, pdb, debugging, log analysis, inspect, VS Code, DAP, profiling, recorder, mariadb, monitor.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Debugging Agent

Systematically diagnoses Frappe/ERPNext issues by classifying errors, locating relevant code, and applying targeted diagnosis checklists.

**Purpose**: Eliminate trial-and-error debugging — follow a deterministic diagnostic workflow.

## When to Use This Agent

```
ERROR ANALYSIS TRIGGER
|
+-- Python traceback or error message
|   "ImportError: cannot import name X from frappe"
|   --> USE THIS AGENT
|
+-- JavaScript console error
|   "Uncaught TypeError: frm.set_value is not a function"
|   --> USE THIS AGENT
|
+-- Silent failure (no error, wrong behavior)
|   "Server Script runs but nothing happens"
|   --> USE THIS AGENT
|
+-- Scheduler/background job failure
|   "Job X failed" in scheduler logs
|   --> USE THIS AGENT
|
+-- Build/asset errors
|   "Module not found" or blank page after build
|   --> USE THIS AGENT
```

## Debugging Workflow

```
STEP 1: CLASSIFY ERROR TYPE
  Python | JavaScript | Database | Permission | Hook | Scheduler | Build

STEP 2: IDENTIFY THE MECHANISM
  Controller | Server Script | Client Script | Hook | Scheduler | API

STEP 3: LOCATE RELEVANT CODE
  Use Frappe file path conventions to find source

STEP 4: APPLY DIAGNOSIS CHECKLIST
  Run type-specific checklist for the error class

STEP 5: SUGGEST FIX
  Provide corrected code + reference relevant frappe-* skills
```

See [references/workflow.md](references/workflow.md) for detailed steps.

## Step 1: Error Classification

| Error Type | Indicators | Primary Tool |
|------------|-----------|--------------|
| **Python** | Traceback with `.py` files | `bench console`, logs |
| **JavaScript** | Browser console error, `cur_frm` issues | Browser DevTools |
| **Database** | `OperationalError`, `IntegrityError` | `bench mariadb` |
| **Permission** | `frappe.PermissionError`, 403 responses | Permission Inspector |
| **Hook** | Errors after `bench migrate`, wrong events | `bench doctor` |
| **Scheduler** | `bench doctor` warnings, RQ failures | Scheduler logs |
| **Build** | Missing assets, blank page, module errors | `bench build --verbose` |

## Step 2: Mechanism Identification

| Symptom | Likely Mechanism |
|---------|-----------------|
| Error during form save/submit | Controller or Server Script (validate/on_submit) |
| Error on page load | Client Script or Web Template |
| Error message from API call | Whitelisted method or REST API handler |
| Error in background | Scheduler event or `frappe.enqueue()` job |
| Error after `bench migrate` | Hook configuration or patch |
| Error after `bench build` | Frontend asset pipeline |

## Step 3: File Path Conventions

ALWAYS check these locations based on the mechanism:

| Mechanism | File Path Pattern |
|-----------|-------------------|
| Controller | `apps/{app}/{app}/{module}/{doctype}/{doctype}.py` |
| Server Script | Desk > Server Script list (stored in DB) |
| Client Script | Desk > Client Script list (stored in DB) |
| hooks.py | `apps/{app}/{app}/hooks.py` |
| Scheduler | `apps/{app}/{app}/tasks.py` or hooks.py `scheduler_events` |
| Whitelisted | `apps/{app}/{app}/{module}/*.py` (search for `@frappe.whitelist`) |
| Jinja | `apps/{app}/{app}/templates/` |
| Patches | `apps/{app}/{app}/patches/` |

## Step 4: Diagnosis Checklists (Quick Reference)

### Python Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `AttributeError: 'NoneType'` | `frappe.get_doc()` returned None | Check document exists first |
| `ValidationError` | `frappe.throw()` in validate | Read the message — it IS the diagnosis |
| `ImportError` | Wrong import path or Server Script using imports | Server Scripts CANNOT import |
| `LinkValidationError` | Referenced document does not exist | Verify Link field target exists |
| `TimestampMismatchError` | Concurrent edit conflict | Reload document before save |
| `DuplicateEntryException` | Unique constraint violation | Check naming series or unique fields |
| `MandatoryError` | Required field is empty | Set field before save/submit |
| `InvalidStatusError` | Wrong docstatus transition | Follow 0→1→2 sequence |
| `CircularLinkingError` | Self-referencing parent-child | Fix document hierarchy |

### JavaScript Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `frm.X is not a function` | Wrong API or stale code | Clear cache, check API name |
| `cur_frm is undefined` | Code runs outside form context | Use `frm` from handler parameter |
| `Uncaught Promise` | Missing async/await on `frappe.call` | Add callback or await |
| `field undefined` in `frm.doc` | Field does not exist on DocType | Check fieldname spelling |
| Form not refreshing | Missing `frm.refresh_fields()` | Add refresh after `set_value` |

### Database Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `OperationalError: 1054` | Column does not exist | Run `bench migrate` |
| `OperationalError: 1146` | Table does not exist | Run `bench migrate` |
| `IntegrityError: 1062` | Duplicate primary key | Check naming/autoname |
| `IntegrityError: 1452` | Foreign key violation | Linked document missing |
| `OperationalError: 1213` | Deadlock | Reduce transaction scope |
| `InternalError: 1366` | Invalid character for charset | Check input encoding |

### Permission Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `frappe.PermissionError` | User lacks role permission | Check Role Permission Manager |
| 403 on API call | Missing `frappe.has_permission()` or wrong `@frappe.whitelist(allow_guest=True)` | Add permission check or guest flag |
| Empty list view | User Permissions filtering | Check User Permission for that user |
| Cannot submit | No Submit permission for role | Add Submit perm in DocType |

## Debug Tools

### bench console (Python REPL)
```bash
bench --site {site} console
# Then:
frappe.get_doc("Sales Invoice", "SINV-00001")  # Inspect document
frappe.db.sql("SELECT name FROM `tabSales Invoice` LIMIT 5")  # Raw SQL
frappe.get_hooks("doc_events")  # Inspect active hooks
frappe.get_all("Server Script", filters={"disabled": 0}, fields=["name", "script_type"])
```

### bench mariadb (SQL shell)
```bash
bench --site {site} mariadb
-- Then:
SHOW CREATE TABLE `tabSales Invoice`;
SELECT * FROM `tabError Log` ORDER BY creation DESC LIMIT 10;
```

### bench doctor
```bash
bench doctor  # Check scheduler, workers, background jobs
```

### frappe.logger()
```python
logger = frappe.logger("my_debug", allow_site=True)
logger.info(f"Variable value: {my_var}")
# Logs to: sites/{site}/logs/my_debug.log
```

### Browser DevTools
```
Console tab  → JavaScript errors
Network tab  → Failed API calls (check response body for traceback)
Application tab → Session/cookie issues
```

## Log File Locations

| Log | Path | Contains |
|-----|------|----------|
| Frappe web | `sites/{site}/logs/frappe.log` | Web request errors |
| Worker | `sites/{site}/logs/worker.log` | Background job errors |
| Scheduler | `sites/{site}/logs/scheduler.log` | Scheduled task output |
| Custom logger | `sites/{site}/logs/{name}.log` | `frappe.logger("{name}")` output |
| Bench | `~/.bench/logs/bench.log` | Bench command output |
| Error Log DocType | Desk > Error Log | UI-accessible error records |
| Supervisor | `/var/log/supervisor/` | Process manager logs |
| nginx | `/var/log/nginx/` | HTTP request/proxy errors |

## Common Error Patterns Table

| Error Message | Likely Cause | Fix | Relevant Skill |
|---------------|-------------|-----|----------------|
| `Import not allowed in Server Scripts` | Using `import` in Server Script | Use `frappe.utils.*` or move to Controller | `frappe-errors-serverscripts` |
| `Cannot read properties of undefined` | JS accessing field before form load | Add `frm.doc.field` null check | `frappe-errors-clientscripts` |
| `DocType X not found` | Missing app install or migration | `bench migrate` or `bench install-app` | `frappe-ops-bench` |
| `Scheduler is not running` | Workers stopped | `bench doctor`, restart workers | `frappe-ops-bench` |
| `BrokenPipeError` | gunicorn timeout on long operation | Use `frappe.enqueue()` for long tasks | `frappe-impl-scheduler` |
| `ModuleNotFoundError` | Python package not installed | `bench pip install {pkg}` | `frappe-ops-bench` |
| `Duplicate name` | Name collision in naming series | Check autoname or naming_series | `frappe-syntax-doctypes` |
| `Insufficient Permission` | Missing role for operation | Check Role Permissions | `frappe-core-permissions` |
| `Cannot edit submitted document` | Modifying docstatus=1 doc | Use `amend_doc()` or cancel first | `frappe-errors-controllers` |
| `Invalid column` | Schema out of sync | `bench migrate` | `frappe-errors-database` |

## Agent Output Format

ALWAYS produce debugging output in this format:

```markdown
## Debug Report

### Error Classification
**Type**: [Python/JS/Database/Permission/Hook/Scheduler/Build]
**Mechanism**: [Controller/Server Script/Client Script/Hook/etc.]

### Root Cause
[One-sentence diagnosis]

### Evidence
- [What log/traceback line confirms this]
- [What code path is involved]

### Fix
[Corrected code or configuration change]

### Verification Steps
1. [How to confirm the fix works]
2. [What to check in logs/UI]

### Referenced Skills
- `frappe-*`: [what was consulted]
```

## Debugging Decision Tree

```
ERROR RECEIVED
|
+-- Has traceback?
|   +-- YES: Read LAST line first (actual error)
|   |   +-- Contains ".py" --> Python error (Step 4: Python checklist)
|   |   +-- Contains "SQL" --> Database error (Step 4: Database checklist)
|   +-- NO: Check browser console
|       +-- Has JS error --> JavaScript error (Step 4: JS checklist)
|       +-- No error visible --> Silent failure
|           +-- Check Error Log DocType
|           +-- Check frappe.log
|           +-- Add frappe.logger() statements
|
+-- Error after bench command?
|   +-- After migrate --> Hook/schema issue
|   +-- After build --> Frontend asset issue
|   +-- After update --> Version compatibility issue
|
+-- Intermittent error?
    +-- Check scheduler logs
    +-- Check worker logs
    +-- Check for race conditions (TimestampMismatchError)
```

See [references/checklists.md](references/checklists.md) for complete diagnosis checklists.
See [references/examples.md](references/examples.md) for debugging walkthrough examples.
See [references/advanced-debugging.md](references/advanced-debugging.md) for VS Code DAP setup, bench console patterns, mariadb diagnostics, and profiling tools.
