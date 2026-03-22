---
name: frappe-errors-serverscripts
description: >
  Use when debugging or preventing errors in Frappe Server Scripts.
  Prevents ImportError (the #1 error), NameError for restricted builtins,
  sandbox violations, doc_events not firing, wrong script type selection,
  SQL injection, permission denied in scheduled scripts, infinite loops,
  and API scripts not returning JSON. Covers error message mapping table.
  Keywords: server script error, ImportError, NameError, sandbox,
  restricted, frappe.throw, doc_events, scheduler, API script, SQL injection.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Server Script Errors — Diagnosis and Resolution

Cross-refs: `frappe-syntax-serverscripts` (syntax), `frappe-impl-serverscripts` (workflows), `frappe-errors-clientscripts` (client-side).

---

## CRITICAL: Server Scripts Disabled by Default [v15+]

Starting from Frappe v15, Server Scripts are **disabled by default**. You MUST enable them:

```python
# In site_config.json
{ "server_script_enabled": 1 }
```

On Frappe Cloud: Server Scripts are ONLY available on **private benches**, NOT on shared benches.

---

## Error Diagnosis Flowchart

```
ERROR IN SERVER SCRIPT
│
├─► ImportError / NameError
│   ├─► "import json" → BLOCKED. Use frappe.parse_json()
│   ├─► "import datetime" → BLOCKED. Use frappe.utils
│   ├─► "import os/sys/subprocess" → BLOCKED. Security restriction
│   └─► "NameError: name 'dict' is not defined" → Some builtins restricted
│
├─► SyntaxError: not allowed
│   ├─► "try/except" → BLOCKED by RestrictedPython [v14-v15]
│   ├─► "raise ValueError" → BLOCKED. Use frappe.throw()
│   └─► "exec/eval" → BLOCKED. Security restriction
│
├─► Script runs but nothing happens
│   ├─► Wrong Script Type selected → Check Document Event vs API vs Scheduler
│   ├─► Wrong DocType selected → Verify exact DocType name
│   ├─► Wrong Event selected → Before Save ≠ After Save
│   └─► Script disabled → Check "Enabled" checkbox
│
├─► 403 Permission Denied
│   ├─► Scheduler script → Runs as Administrator, check role permissions
│   ├─► API script → Check Allow Guest setting
│   └─► doc_event → User lacks DocType permission
│
├─► Data not saved in Scheduler
│   └─► Missing frappe.db.commit() → REQUIRED in scheduler scripts
│
└─► API script returns empty/wrong response
    └─► Not setting frappe.response["message"] → ALWAYS set response
```

---

## Error Message → Cause → Fix Table

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `ImportError: import not allowed` | Any `import` statement in sandbox | Use `frappe.utils`, `frappe.parse_json()`, etc. |
| `NameError: name 'dict' is not defined` | Some Python builtins blocked by RestrictedPython | Use `frappe._dict()` or literal `{}` |
| `SyntaxError: try/except not allowed` | RestrictedPython blocks exception handling [v14-v15] | Use conditional checks (`if/else`) instead |
| `SyntaxError: raise not allowed` | RestrictedPython blocks `raise` | Use `frappe.throw()` |
| `Script not executing` | Wrong Script Type or Event selected | Verify type matches: Document Event, API, or Scheduler |
| `doc is not defined` | Using `doc` in API or Scheduler script (no document context) | `doc` is only available in Document Event scripts |
| `PermissionError` in Scheduler | Scheduler runs as Administrator but script accesses restricted resource | Use `ignore_permissions=True` where appropriate |
| `Changes not saved` in Scheduler | Missing `frappe.db.commit()` | ALWAYS call `frappe.db.commit()` in Scheduler scripts |
| `API returns empty response` | Forgot to set `frappe.response["message"]` | ALWAYS set `frappe.response["message"] = result` |
| `Timeout / killed` | Infinite loop or processing too many records | ALWAYS add `limit` to queries, ALWAYS use batch processing |
| `ValidationError: qty is required` | `doc.save()` called in Before Save (recursion) | NEVER call `doc.save()` in Before Save; just set values |
| `SQL injection via string format` | User input in SQL without escaping | ALWAYS use `frappe.db.escape()` or parameterized queries |

---

## The #1 Error: ImportError

**Every beginner hits this.** The Server Script sandbox blocks ALL imports except `json`.

```python
# ❌ BLOCKED — These ALL fail with ImportError
import json                    # Use frappe.parse_json() / frappe.as_json()
from datetime import datetime  # Use frappe.utils.now(), frappe.utils.today()
import re                      # Not available in sandbox
import os                      # Security: blocked
import requests                # Use frappe.make_get_request(), frappe.make_post_request()

# ✅ CORRECT — Sandbox equivalents
data = frappe.parse_json(doc.json_field)         # Instead of json.loads()
today = frappe.utils.today()                      # Instead of datetime.date.today()
now = frappe.utils.now()                          # Instead of datetime.now()
diff = frappe.utils.date_diff(date1, date2)       # Instead of timedelta
resp = frappe.make_get_request("https://api.com") # Instead of requests.get()
resp = frappe.make_post_request("https://api.com", data=payload)
```

### Available Sandbox API (Complete Reference)

| Category | Available Methods |
|----------|-------------------|
| **Document** | `frappe.get_doc()`, `frappe.new_doc()`, `frappe.get_last_doc()`, `frappe.get_cached_doc()`, `frappe.get_mapped_doc()`, `frappe.rename_doc()`, `frappe.delete_doc()` |
| **Database** | `frappe.db.get_list()`, `frappe.db.get_all()`, `frappe.db.get_value()`, `frappe.db.get_single_value()`, `frappe.db.set_value()`, `frappe.db.exists()`, `frappe.db.sql()`, `frappe.db.commit()`, `frappe.db.rollback()`, `frappe.db.escape()` |
| **Query Builder** | `frappe.qb` (full query builder) |
| **HTTP** | `frappe.make_get_request()`, `frappe.make_post_request()`, `frappe.make_put_request()` |
| **Utility** | `frappe.utils.*` (all utility functions), `frappe.parse_json()`, `frappe.as_json()` |
| **User/Session** | `frappe.session.user`, `frappe.get_roles()`, `frappe.has_permission()` |
| **Messages** | `frappe.throw()`, `frappe.msgprint()`, `frappe.log_error()`, `frappe.sendmail()` |
| **Module** | `json` (the ONLY importable module) |

---

## Script Type Selection Errors

ALWAYS verify you selected the correct Script Type:

| Script Type | Trigger | Has `doc`? | Has `frappe.form_dict`? | Auto-commit? |
|-------------|---------|:----------:|:-----------------------:|:------------:|
| Document Event | DocType lifecycle (Before Save, After Save, etc.) | YES | NO | YES |
| API | HTTP request to `/api/method/{method_name}` | NO | YES | YES |
| Scheduler Event | Cron schedule | NO | NO | NO — MUST call `frappe.db.commit()` |
| Permission Query | Every list query on the DocType | NO | NO (has `user`) | N/A |

### Common Mistake: Wrong Event

```python
# ❌ WRONG — "After Save" cannot prevent save
# Script Type: Document Event, Event: After Save
if not doc.customer:
    frappe.throw("Customer is required")  # Document already saved!

# ✅ CORRECT — Use "Before Save" or "Before Validate"
# Script Type: Document Event, Event: Before Save
if not doc.customer:
    frappe.throw("Customer is required")  # Prevents save
```

---

## Sandbox Workarounds

### try/except Is Blocked — Use Conditional Checks

```python
# ❌ BLOCKED in sandbox
try:
    customer = frappe.get_doc("Customer", doc.customer)
except Exception:
    frappe.throw("Customer not found")

# ✅ CORRECT — Check first, then access
if not frappe.db.exists("Customer", doc.customer):
    frappe.throw(f"Customer '{doc.customer}' not found")
customer = frappe.get_doc("Customer", doc.customer)
```

### raise Is Blocked — Use frappe.throw()

```python
# ❌ BLOCKED
if amount < 0:
    raise ValueError("Amount cannot be negative")

# ✅ CORRECT
if amount < 0:
    frappe.throw("Amount cannot be negative")
```

### frappe.throw() Exception Types for API Scripts

| Exception | HTTP Code | Use When |
|-----------|:---------:|----------|
| `frappe.ValidationError` | 417 | Input validation failure |
| `frappe.PermissionError` | 403 | Access denied |
| `frappe.DoesNotExistError` | 404 | Record not found |
| `frappe.AuthenticationError` | 401 | Not logged in |
| (default, no exc) | 417 | General validation error |

```python
# API Script — Correct exception types
if not customer:
    frappe.throw("Customer param required", exc=frappe.ValidationError)  # 417
if not frappe.db.exists("Customer", customer):
    frappe.throw("Customer not found", exc=frappe.DoesNotExistError)    # 404
if not frappe.has_permission("Customer", "read", customer):
    frappe.throw("Access denied", exc=frappe.PermissionError)           # 403
```

---

## Scheduler Script — Critical Mistakes

```python
# ❌ WRONG — No limit, no commit, no error logging
invoices = frappe.get_all("Sales Invoice", filters={"status": "Unpaid"})
for inv in invoices:
    frappe.db.set_value("Sales Invoice", inv.name, "reminder_sent", 1)

# ✅ CORRECT — Limit, batch commit, error logging
BATCH_SIZE = 50
invoices = frappe.get_all(
    "Sales Invoice",
    filters={"status": "Unpaid", "docstatus": 1},
    fields=["name", "customer"],
    limit=500  # ALWAYS limit
)

errors = []
for i in range(0, len(invoices), BATCH_SIZE):
    batch = invoices[i:i + BATCH_SIZE]
    for inv in batch:
        if not frappe.db.exists("Customer", inv.customer):
            errors.append(f"{inv.name}: Customer not found")
            continue
        frappe.db.set_value("Sales Invoice", inv.name, "reminder_sent", 1)
    frappe.db.commit()  # REQUIRED

if errors:
    frappe.log_error("\n".join(errors), "Reminder Errors")
frappe.db.commit()
```

---

## SQL Injection Prevention

```python
# ❌ VULNERABLE — String interpolation with user input
territory = frappe.form_dict.get("territory")
conditions = f"`tabCustomer`.territory = '{territory}'"  # SQL INJECTION!

# ✅ SAFE — Use frappe.db.escape()
territory = frappe.form_dict.get("territory")
conditions = f"`tabCustomer`.territory = {frappe.db.escape(territory)}"

# ✅ SAFEST — Use parameterized query or Query Builder
results = frappe.db.get_all("Customer", filters={"territory": territory})
```

---

## ALWAYS / NEVER Rules

### ALWAYS

1. **Use `frappe.utils.*` instead of Python imports** — Only `json` module is importable
2. **Use `frappe.throw()` instead of `raise`** — `raise` is blocked by sandbox
3. **Use conditional checks instead of `try/except`** — Exception handling is blocked [v14-v15]
4. **Call `frappe.db.commit()` in Scheduler scripts** — Changes are NOT auto-committed
5. **Add `limit` to ALL queries in Scheduler scripts** — Prevent memory exhaustion
6. **Set `frappe.response["message"]` in API scripts** — Otherwise response is empty
7. **Use `frappe.db.escape()` for user input in SQL** — Prevent SQL injection
8. **Log errors in Scheduler scripts** with `frappe.log_error()` — No user to see errors
9. **Verify Script Type matches your intent** — Document Event vs API vs Scheduler

### NEVER

1. **NEVER use `import` statements** (except `json`) — Blocked by RestrictedPython
2. **NEVER use `try/except` or `raise`** — Blocked by sandbox [v14-v15]
3. **NEVER call `doc.save()` in Before Save** — Causes infinite recursion
4. **NEVER use string formatting for SQL with user input** — SQL injection risk
5. **NEVER process unlimited records in Scheduler** — Always use `limit`
6. **NEVER assume `doc` exists in API/Scheduler scripts** — Only available in Document Events
7. **NEVER forget `frappe.db.commit()` in Scheduler** — All changes will be lost

---

## Reference Files

| File | Contents |
|------|----------|
| `references/examples.md` | Real error scenarios with diagnosis |
| `references/anti-patterns.md` | Common sandbox mistakes with fixes |
| `references/patterns.md` | Defensive error handling patterns by script type |
