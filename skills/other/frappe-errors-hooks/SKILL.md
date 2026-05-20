---
name: frappe-errors-hooks
description: >
  Use when debugging hooks.py errors in Frappe/ERPNext. Covers hook not firing
  (typo, wrong dict structure), circular imports, app_include_js path errors,
  scheduler_events not running, doc_events on wrong DocType,
  permission_query_conditions SQL errors, override_doctype_class import
  failures, extend_doctype_class [v16+] conflicts, fixtures not loading.
  Error diagnosis by hook type for v14/v15/v16.
  Keywords: hooks.py error, hook not firing, scheduler not running,
  doc_events error, circular import, fixtures error, override class error.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Hooks Error Diagnosis & Resolution

Cross-ref: `frappe-syntax-hooks` (syntax), `frappe-impl-hooks` (workflows), `frappe-errors-controllers` (controller errors).

---

## Error-to-Fix Mapping Table

| Error / Symptom | Cause | Fix |
|-----------------|-------|-----|
| Hook not firing at all | Typo in dotted path | Verify module path matches actual file location |
| `ImportError` on bench start | Wrong module path or circular import | Fix import path; break circular dependency |
| `AttributeError: module has no attribute` | Function name typo in hooks.py | Match function name exactly to Python definition |
| `app_include_js` not loading | Path missing `assets/` prefix or wrong extension | Use `"assets/myapp/js/file.js"` format |
| scheduler_events not running | Scheduler disabled or workers down | `bench scheduler enable`, check `bench doctor` |
| doc_events handler never called | DocType name misspelled in dict key | Use exact DocType name with spaces: `"Sales Invoice"` |
| `permission_query_conditions` breaks list view | SQL syntax error or frappe.throw() in handler | Return valid SQL string; NEVER throw |
| `override_doctype_class` import failure | Parent class import path changed between versions | Pin import to correct module path for target version |
| `extend_doctype_class` [v16+] method conflict | Two extensions define same method name | Rename conflicting methods; check hook resolution order |
| Fixtures not loading on install | Wrong `dt` key or DocType doesn't exist on target | Verify DocType exists before export; check filter syntax |
| `extend_bootinfo` breaks login | Unhandled exception in boot handler | Wrap ALL bootinfo code in try/except |
| Wildcard `"*"` handler breaks all saves | Unhandled exception in wildcard doc_events | ALWAYS wrap wildcard handlers in try/except |
| Hook fires but changes lost | Missing `frappe.db.commit()` in scheduler | Add explicit commit in scheduler/background tasks |
| Multiple handler chain broken | First handler throws, others never run | Isolate non-critical ops in try/except |

---

## Hook Registration Errors

### Hook Not Firing — Diagnosis Checklist

```
IS YOUR HOOK NOT FIRING?
│
├─► Check 1: Is the dotted path correct?
│   hooks.py: "myapp.events.sales.validate"
│   File:     myapp/events/sales.py → def validate(doc, method=None):
│   COMMON MISTAKE: "myapp.events.sales_invoice.validate" when file is sales.py
│
├─► Check 2: Is the dict structure correct?
│   doc_events uses NESTED dict: {"Sales Invoice": {"validate": "path"}}
│   scheduler_events uses LIST: {"daily": ["path1", "path2"]}
│   permission_query uses FLAT dict: {"Sales Invoice": "path"}
│
├─► Check 3: Is bench restarted after hooks.py change?
│   ALWAYS run: bench restart (or bench clear-cache for dev)
│
├─► Check 4: Is the DocType name exact?
│   "Sales Invoice" NOT "SalesInvoice" NOT "sales_invoice"
│   Use exact DocType name as shown in Frappe UI
│
└─► Check 5: Is the app installed on the site?
    bench --site mysite list-apps
```

### Circular Import Errors

```python
# ❌ CAUSES ImportError — circular dependency
# myapp/hooks.py imports from myapp.events
# myapp/events/sales.py imports from myapp.hooks

# ✅ CORRECT — break the cycle
# Move shared constants to myapp/constants.py
# Import from constants in both hooks.py and events/
```

**Rule**: NEVER import from hooks.py in your event handlers. hooks.py is read by the framework, not imported by your code.

### Wrong Dict Structure by Hook Type

```python
# ❌ WRONG — doc_events needs nested dict, not flat
doc_events = {
    "Sales Invoice": "myapp.events.validate"  # WRONG: string, not dict
}

# ✅ CORRECT
doc_events = {
    "Sales Invoice": {
        "validate": "myapp.events.sales.validate"
    }
}

# ❌ WRONG — scheduler_events daily needs list
scheduler_events = {
    "daily": "myapp.tasks.daily_sync"  # WRONG: string, not list
}

# ✅ CORRECT
scheduler_events = {
    "daily": ["myapp.tasks.daily_sync"]
}

# ❌ WRONG — cron needs nested dict with list values
scheduler_events = {
    "cron": ["0 9 * * *", "myapp.tasks.morning"]  # WRONG structure
}

# ✅ CORRECT
scheduler_events = {
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.morning_report"]
    }
}
```

---

## app_include_js / app_include_css Errors

```python
# ❌ WRONG — missing assets/ prefix
app_include_js = "js/myapp.js"

# ❌ WRONG — using Python module path instead of file path
app_include_js = "myapp.public.js.myapp"

# ✅ CORRECT — full asset path
app_include_js = "assets/myapp/js/myapp.js"

# ✅ CORRECT — multiple files as list
app_include_js = ["assets/myapp/js/app.js", "assets/myapp/js/utils.js"]
app_include_css = "assets/myapp/css/myapp.css"
```

**Diagnosis**: If JS/CSS not loading, check browser DevTools Network tab for 404. Run `bench build` after adding new files. ALWAYS verify the file exists at `myapp/public/js/myapp.js`.

---

## scheduler_events Not Running

### Diagnosis Steps

```bash
# Step 1: Is scheduler enabled?
bench scheduler status
# If disabled: bench scheduler enable

# Step 2: Are workers running?
bench doctor
# Look for: "Workers online: X"
# If 0: bench start (dev) or supervisorctl restart all (prod)

# Step 3: Check Scheduled Job Log
# In Frappe UI: /api/method/frappe.client.get_list?doctype=Scheduled Job Log&limit=5

# Step 4: Check Error Log for task failures
# In Frappe UI: /app/error-log

# Step 5: Is the task registered?
bench execute frappe.utils.scheduler.get_all_tasks
```

### Common Scheduler Failures

```python
# ❌ PROBLEM: Task runs but changes not persisted
def daily_sync():
    for item in frappe.get_all("Item", limit=100):
        frappe.db.set_value("Item", item.name, "synced", 1)
    # MISSING: frappe.db.commit() — ALL changes lost!

# ✅ FIX: ALWAYS commit in scheduler tasks
def daily_sync():
    for item in frappe.get_all("Item", limit=100):
        frappe.db.set_value("Item", item.name, "synced", 1)
    frappe.db.commit()

# ❌ PROBLEM: Task fails silently — no debugging possible
def daily_task():
    try:
        process_records()
    except Exception:
        pass  # Silent death

# ✅ FIX: ALWAYS log errors in scheduler
def daily_task():
    try:
        process_records()
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Daily Task Error")
```

---

## doc_events Errors

### Error Handling by Event Phase

| Event | Throw Effect | Transaction | Pattern |
|-------|-------------|-------------|---------|
| `validate` | Prevents save, full rollback | Pre-write | Collect errors, throw once |
| `before_save` | Prevents save, full rollback | Pre-write | Same as validate |
| `on_update` | Doc already saved, error shown | Post-write | Isolate non-critical ops |
| `after_insert` | Doc already saved, error shown | Post-write | Isolate non-critical ops |
| `on_submit` | Doc already submitted | Post-write | Isolate non-critical ops |
| `on_cancel` | Doc already cancelled | Post-write | Isolate non-critical ops |

### Multiple Handler Chain Problem

```python
# If App A and App B both register validate for Sales Invoice:
# App A's handler throws → App B's handler NEVER runs

# ✅ ALWAYS be aware: your handler is not alone
def validate(doc, method=None):
    """Collect errors, throw once at end."""
    errors = []
    if doc.grand_total < 0:
        errors.append(_("Total cannot be negative"))
    if errors:
        frappe.throw("<br>".join(errors))

# ✅ For on_update: isolate independent operations
def on_update(doc, method=None):
    try:
        send_notification(doc)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Notify error: {doc.name}")
    try:
        sync_external(doc)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Sync error: {doc.name}")
```

### NEVER Commit in doc_events

```python
# ❌ BREAKS transaction management
def on_update(doc, method=None):
    frappe.db.set_value("Counter", "main", "count", 100)
    frappe.db.commit()  # Partial commit — dangerous!

# ✅ Framework handles commits automatically
def on_update(doc, method=None):
    frappe.db.set_value("Counter", "main", "count", 100)
```

---

## Permission Hook Errors

### permission_query_conditions — NEVER Throw

```python
# ❌ BREAKS list view entirely
def query_conditions(user):
    if "Sales User" not in frappe.get_roles(user):
        frappe.throw("Access denied")  # LIST VIEW CRASHES
    return f"owner = '{user}'"  # Also: SQL injection!

# ✅ CORRECT — safe fallback, escaped values
def query_conditions(user):
    try:
        user = user or frappe.session.user
        if "System Manager" in frappe.get_roles(user):
            return ""
        return f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Query Conditions Error")
        return f"`tabSales Invoice`.owner = {frappe.db.escape(frappe.session.user)}"
```

**Note**: permission_query_conditions only affects `frappe.db.get_list()`, NOT `frappe.db.get_all()`.

### has_permission — NEVER Throw

```python
# ❌ BREAKS document access
def has_permission(doc, user=None, permission_type=None):
    if doc.status == "Locked":
        frappe.throw("Locked")  # DOCUMENT INACCESSIBLE

# ✅ Return False to deny, None to defer
def has_permission(doc, user=None, permission_type=None):
    try:
        user = user or frappe.session.user
        if doc.status == "Locked" and permission_type == "write":
            return False
        return None  # Defer to default permission system
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Permission Error")
        return None
```

---

## Override & Extend Errors

### override_doctype_class — Import Failures

```python
# ❌ COMMON: Import path changes between ERPNext versions
# v14 path:
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSI"
}
# myapp/overrides.py:
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
# This path may change in v15/v16!

# ✅ ALWAYS call super(), re-raise validation errors
class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        try:
            super().validate()
        except frappe.ValidationError:
            raise  # ALWAYS re-raise validation errors
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Parent validate error")
            raise
        self.custom_validation()
```

**Warning**: Only ONE app's override_doctype_class is active per DocType ("last writer wins"). Use extend_doctype_class [v16+] for multi-app compatibility.

### extend_doctype_class [v16+] — Conflicts

```python
# hooks.py
extend_doctype_class = {
    "Sales Invoice": ["myapp.extensions.si.SalesInvoiceMixin"]
}

# ❌ CONFLICT: Two extensions define same method
# App A: class Mixin: def custom_calc(self): ...
# App B: class Mixin: def custom_calc(self): ...
# Result: Last app's method wins silently

# ✅ ALWAYS prefix method names with app name
class SalesInvoiceMixin:
    def myapp_custom_calc(self):
        """Prefixed to avoid conflicts with other extensions."""
        pass
```

---

## extend_bootinfo Errors

```python
# ❌ BREAKS LOGIN — unhandled error prevents desk from loading
def extend_boot(bootinfo):
    settings = frappe.get_single("My Settings")  # DoesNotExistError!
    bootinfo.config = settings.config

# ✅ ALWAYS wrap in try/except with safe defaults
def extend_boot(bootinfo):
    bootinfo.myapp_config = {}
    try:
        if frappe.db.exists("My Settings", "My Settings"):
            settings = frappe.get_single("My Settings")
            bootinfo.myapp_config = {"feature": settings.feature or False}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Bootinfo Error")
```

---

## Fixtures Not Loading

```python
# ❌ WRONG — dt key misspelled
fixtures = [{"doctype": "Custom Field", "filters": [...]}]  # "doctype" not "dt"!

# ✅ CORRECT — use "dt" key
fixtures = [{"dt": "Custom Field", "filters": [["module", "=", "My App"]]}]

# ❌ PROBLEM: DocType doesn't exist on target site
fixtures = [{"dt": "My Custom DocType"}]  # If not created yet → install fails

# ✅ FIX: Ensure DocType is created before fixtures are imported
# Order: DocType JSON → fixtures JSON (install order matters)
```

**Export command**: `bench --site mysite export-fixtures`
**Import**: Automatic during `bench --site mysite install-app myapp`

---

## Critical Rules

### ALWAYS
1. Restart bench after changing hooks.py
2. Use try/except in scheduler tasks — no user sees errors
3. Call `frappe.db.commit()` in scheduler — no auto-commit
4. Return safe fallbacks in permission hooks — NEVER throw
5. Call `super()` in override classes — re-raise ValidationError
6. Wrap `extend_bootinfo` in try/except — errors break login
7. Wrap wildcard `"*"` doc_events in try/except — errors break ALL saves
8. Prefix extend_doctype_class [v16+] methods with app name

### NEVER
1. Throw in `permission_query_conditions` — breaks list views
2. Throw in `has_permission` — breaks document access
3. Commit in doc_events — breaks transaction management
4. Import from hooks.py in event handlers — causes circular imports
5. Assume single handler — multiple apps register doc_events
6. Use string formatting in permission SQL — SQL injection risk
7. Ignore scheduler errors — they fail completely silently

---

## Quick Reference: Error Handling by Hook Type

| Hook Type | Can Throw? | Commit? | Error Strategy |
|-----------|:----------:|:-------:|----------------|
| doc_events (validate) | YES | NEVER | Collect errors, throw once |
| doc_events (on_update+) | Careful | NEVER | Isolate non-critical ops |
| scheduler_events | Pointless | ALWAYS | try/except + log_error |
| permission_query_conditions | NEVER | NEVER | Return "" or owner filter |
| has_permission | NEVER | NEVER | Return None on error |
| extend_bootinfo | NEVER | NEVER | try/except + safe defaults |
| override_doctype_class | YES | NEVER | super() + re-raise |
| extend_doctype_class [v16+] | YES | NEVER | Prefix methods, avoid conflicts |
| fixtures | N/A | N/A | Verify dt key and DocType existence |
| app_include_js/css | N/A | N/A | Check assets/ prefix, run bench build |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns by hook type |
| `references/examples.md` | Full working examples with error handling |
| `references/anti-patterns.md` | Common mistakes with wrong/correct pairs |

---

## See Also

- `frappe-syntax-hooks` — Hook syntax and dict structures
- `frappe-impl-hooks` — Implementation workflows
- `frappe-errors-controllers` — Controller error handling
- `frappe-errors-database` — Database error handling
- `frappe-errors-serverscripts` — Server Script error handling
