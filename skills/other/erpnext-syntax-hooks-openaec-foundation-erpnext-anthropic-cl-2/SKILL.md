---
name: erpnext-syntax-hooks
description: "Deterministic syntax for Frappe hooks.py configuration. Use when Claude needs to configure app events, scheduler tasks, document events, fixtures, boot session, jenv customization, or website routing. Covers v14/v15/v16 including extend_doctype_class. Triggers: hooks.py, doc_events, scheduler_events, fixtures, app_include_js, override_whitelisted_methods."
---

# ERPNext Syntax: Hooks (hooks.py)

Hooks in hooks.py enable custom apps to extend Frappe/ERPNext functionality.

## Quick Reference

### doc_events - Document Lifecycle

```python
# In hooks.py
doc_events = {
    "*": {
        "after_insert": "myapp.events.log_all_inserts"
    },
    "Sales Invoice": {
        "validate": "myapp.events.si_validate",
        "on_submit": "myapp.events.si_on_submit"
    }
}
```

```python
# In myapp/events.py
import frappe

def si_validate(doc, method=None):
    """doc = document object, method = event name"""
    if doc.grand_total < 0:
        frappe.throw("Total cannot be negative")
```

### scheduler_events - Periodic Tasks

```python
# In hooks.py
scheduler_events = {
    "daily": ["myapp.tasks.daily_cleanup"],
    "hourly_long": ["myapp.tasks.heavy_sync"],
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.weekday_morning"]
    }
}
```

```python
# In myapp/tasks.py
def daily_cleanup():
    """No arguments - called automatically"""
    frappe.db.delete("Log", {"creation": ["<", one_month_ago()]})
```

### extend_bootinfo - Client Data Injection

```python
# In hooks.py
extend_bootinfo = "myapp.boot.extend_boot"
```

```python
# In myapp/boot.py
def extend_boot(bootinfo):
    """bootinfo = dict that goes to frappe.boot"""
    bootinfo.my_setting = frappe.get_single("My Settings").value
```

```javascript
// Client-side
console.log(frappe.boot.my_setting);
```

---

## Most Used doc_events

| Event | When | Use Case |
|-------|------|----------|
| `validate` | Before every save | Validation, calculations |
| `on_update` | After every save | Notifications, sync |
| `after_insert` | After new doc | Creation-only actions |
| `on_submit` | After submit | Ledger entries |
| `on_cancel` | After cancel | Reverse entries |
| `on_trash` | Before delete | Cleanup |

**Complete list**: See [doc-events.md](references/doc-events.md)

---

## Scheduler Event Types

| Event | Frequency | Queue/Timeout |
|-------|-----------|---------------|
| `hourly` | Every hour | default / 5 min |
| `daily` | Every day | default / 5 min |
| `weekly` | Every week | default / 5 min |
| `monthly` | Every month | default / 5 min |
| `hourly_long` | Every hour | long / 25 min |
| `daily_long` | Every day | long / 25 min |
| `cron` | Custom timing | default / 5 min |

**Cron syntax and examples**: See [scheduler-events.md](references/scheduler-events.md)

---

## Critical Rules

### 1. bench migrate after scheduler changes

```bash
# REQUIRED - otherwise changes won't be picked up
bench --site sitename migrate
```

### 2. No commits in doc_events

```python
# ❌ WRONG
def on_update(doc, method=None):
    frappe.db.commit()  # Breaks transaction

# ✅ CORRECT - Frappe commits automatically
def on_update(doc, method=None):
    update_related_docs(doc)
```

### 3. Changes after on_update via db_set

```python
# ❌ WRONG - change is lost
def on_update(doc, method=None):
    doc.status = "Processed"

# ✅ CORRECT
def on_update(doc, method=None):
    frappe.db.set_value(doc.doctype, doc.name, "status", "Processed")
```

### 4. Heavy tasks to _long queue

```python
# ❌ WRONG - timeout after 5 min
scheduler_events = {
    "daily": ["myapp.tasks.process_all_records"]  # May take 20 min
}

# ✅ CORRECT - 25 min timeout
scheduler_events = {
    "daily_long": ["myapp.tasks.process_all_records"]
}
```

### 5. Tasks receive no arguments

```python
# ❌ WRONG
def my_task(some_arg):
    pass

# ✅ CORRECT
def my_task():
    # Fetch data inside the function
    pass
```

---

## Cron Syntax Cheatsheet

```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-6, Sun=0)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

| Pattern | Meaning |
|---------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 9 * * *` | Daily at 09:00 |
| `0 9 * * 1-5` | Weekdays at 09:00 |
| `0 0 1 * *` | First day of month |
| `0 17 * * 5` | Friday at 17:00 |

---

## doc_events vs Controller Hooks

| Aspect | doc_events (hooks.py) | Controller Methods |
|--------|----------------------|-------------------|
| Location | `hooks.py` | `doctype/xxx/xxx.py` |
| Scope | Hook OTHER doctypes | Only OWN doctype |
| Multiple handlers | ✅ Yes (list) | ❌ No |
| Priority | After controller | First |
| Wildcard (`*`) | ✅ Yes | ❌ No |

**Use doc_events when**:
- Hooking other apps' DocTypes from your custom app
- Reacting to ALL DocTypes (wildcard)
- Registering multiple handlers

**Use controller methods when**:
- Working on your own DocType
- You want full lifecycle control

---

## Reference Files

| File | Contents |
|------|----------|
| [doc-events.md](references/doc-events.md) | All document events, signatures, execution order |
| [scheduler-events.md](references/scheduler-events.md) | Scheduler types, cron syntax, timeouts |
| [bootinfo.md](references/bootinfo.md) | extend_bootinfo, session hooks |
| [overrides.md](references/overrides.md) | Override and extend patterns |
| [permissions.md](references/permissions.md) | Permission hooks |
| [fixtures.md](references/fixtures.md) | Fixtures configuration |
| [examples.md](references/examples.md) | Complete hooks.py examples |
| [anti-patterns.md](references/anti-patterns.md) | Mistakes and corrections |

---

## Configuration Hooks

### Override DocType Controller

```python
# In hooks.py
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}
```

```python
# In myapp/overrides.py
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()  # CRITICAL: always call super()!
        self.custom_validation()
```

**Warning**: Last installed app wins when multiple apps override the same DocType.

### Override Whitelisted Methods

```python
# In hooks.py
override_whitelisted_methods = {
    "frappe.client.get_count": "myapp.overrides.custom_get_count"
}
```

```python
# Method signature MUST be identical to original!
def custom_get_count(doctype, filters=None, debug=False, cache=False):
    # Custom implementation
    return frappe.db.count(doctype, filters)
```

### Permission Hooks

```python
# In hooks.py
permission_query_conditions = {
    "Sales Invoice": "myapp.permissions.si_query_conditions"
}
has_permission = {
    "Sales Invoice": "myapp.permissions.si_has_permission"
}
```

```python
# In myapp/permissions.py
def si_query_conditions(user):
    """Returns SQL WHERE fragment for list filtering"""
    if not user:
        user = frappe.session.user
    
    if "Sales Manager" in frappe.get_roles(user):
        return ""  # No restrictions
    
    return f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"

def si_has_permission(doc, user=None, permission_type=None):
    """Document-level permission check"""
    if permission_type == "write" and doc.status == "Closed":
        return False
    return None  # Fallback to default
```

**Note**: `permission_query_conditions` only works with `get_list`, NOT with `get_all`!

### Fixtures

```python
# In hooks.py
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My App"]]},
    {"dt": "Role", "filters": [["name", "like", "MyApp%"]]}
]
```

```bash
# Export fixtures to JSON
bench --site sitename export-fixtures
```

### Asset Includes

```python
# In hooks.py

# Desk (backend) assets
app_include_js = "/assets/myapp/js/myapp.min.js"
app_include_css = "/assets/myapp/css/myapp.min.css"

# Website/Portal assets
web_include_js = "/assets/myapp/js/web.min.js"
web_include_css = "/assets/myapp/css/web.min.css"

# Form script extensions
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}
```

### Install/Migrate Hooks

```python
# In hooks.py
after_install = "myapp.setup.after_install"
after_migrate = "myapp.setup.after_migrate"
```

```python
# In myapp/setup.py
def after_install():
    create_default_roles()
    
def after_migrate():
    clear_custom_cache()
```

---

## Complete Decision Tree

```
What do you want to achieve?
│
├─► REACT to document events from OTHER apps?
│   └─► doc_events
│
├─► Run PERIODIC tasks?
│   └─► scheduler_events
│       ├─► < 5 min → hourly/daily/weekly/monthly
│       ├─► > 5 min → hourly_long/daily_long/etc.
│       └─► Specific time → cron
│
├─► Send DATA to CLIENT at page load?
│   └─► extend_bootinfo
│
├─► Modify CONTROLLER of existing DocType?
│   ├─► Frappe v16+ → extend_doctype_class (recommended)
│   └─► Frappe v14/v15 → override_doctype_class
│
├─► Modify API ENDPOINT?
│   └─► override_whitelisted_methods
│
├─► Customize PERMISSIONS?
│   ├─► List filtering → permission_query_conditions
│   └─► Document-level → has_permission
│
├─► EXPORT/IMPORT configuration?
│   └─► fixtures
│
├─► ADD JS/CSS to desk or portal?
│   ├─► Desk → app_include_js/css
│   ├─► Portal → web_include_js/css
│   └─► Form specific → doctype_js
│
└─► SETUP on install/migrate?
    └─► after_install, after_migrate
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| doc_events | ✅ | ✅ | ✅ |
| scheduler_events | ✅ | ✅ | ✅ |
| extend_bootinfo | ✅ | ✅ | ✅ |
| override_doctype_class | ✅ | ✅ | ✅ |
| extend_doctype_class | ❌ | ❌ | ✅ |
| permission_query_conditions | ✅ | ✅ | ✅ |
| has_permission | ✅ | ✅ | ✅ |
| fixtures | ✅ | ✅ | ✅ |

---

## Anti-Patterns Summary

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `frappe.db.commit()` in handler | Frappe commits automatically |
| `doc.field = x` in on_update | `frappe.db.set_value()` |
| Heavy task in `daily` | Use `daily_long` |
| Change scheduler without migrate | Always `bench migrate` |
| Sensitive data in bootinfo | Only public config |
| Override without `super()` | Always `super().method()` first |
| `get_all` with permission_query | Use `get_list` |
| Fixtures without filters | Filter by module/app |

**Full anti-patterns**: See [anti-patterns.md](references/anti-patterns.md)
