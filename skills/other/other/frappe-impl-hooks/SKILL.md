---
name: frappe-impl-hooks
description: >
  Use when implementing hooks.py configurations in a Frappe custom app.
  Covers step-by-step workflows for doc_events, scheduler_events,
  override/extend_doctype_class, permission hooks, extend_bootinfo,
  fixtures, asset injection, website hooks, and doctype_js.
  Prevents broken transactions, missed migrations, and multi-app conflicts.
  Keywords: hooks.py, doc_events, scheduler_events, override doctype,
  extend doctype class, permission hook, scheduler job, fixtures,
  doctype_js, extend_bootinfo, website hooks.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Hooks Implementation Workflow

Step-by-step workflows for implementing hooks.py configurations. For API syntax reference, see `frappe-syntax-hooks`.

**Version**: v14/v15/v16 (V16-specific features noted)

---

## Master Decision: What Are You Implementing?

```
WHAT DO YOU WANT TO ACHIEVE?
│
├─► React to document lifecycle events?
│   ├─► On OTHER app's DocTypes → doc_events in hooks.py
│   ├─► On YOUR OWN DocTypes → controller methods (preferred)
│   └─► On ALL DocTypes → doc_events with "*" wildcard
│
├─► Run code on a schedule?
│   └─► scheduler_events (daily, hourly, cron, etc.)
│
├─► Modify an existing DocType's behavior?
│   ├─► V16+: extend_doctype_class (RECOMMENDED)
│   └─► V14/V15: override_doctype_class (last app wins!)
│
├─► Override an existing API endpoint?
│   └─► override_whitelisted_methods
│
├─► Add custom permission logic?
│   ├─► List filtering → permission_query_conditions
│   └─► Document-level → has_permission
│
├─► Send config data to client on page load?
│   └─► extend_bootinfo
│
├─► Export/import configuration?
│   └─► fixtures
│
├─► Add JS/CSS to desk or portal?
│   ├─► Desk-wide → app_include_js / app_include_css
│   ├─► Portal-wide → web_include_js / web_include_css
│   └─► Specific form → doctype_js
│
├─► Customize website/portal behavior?
│   └─► website_context, portal_menu_items, website_route_rules
│
└─► Hook into session/auth lifecycle?
    └─► on_login, on_session_creation, on_logout
```

---

## Workflow 1: Implementing doc_events

### When to Use

Use doc_events when you need to react to document lifecycle events on DocTypes owned by OTHER apps (ERPNext, Frappe core). For YOUR OWN DocTypes, ALWAYS prefer controller methods.

### Step-by-Step

**Step 1: Choose the right event** (see `references/decision-tree.md`)

```
BEFORE save: validate (every save), before_insert (new only)
AFTER save:  after_insert (new only), on_update (every save), on_change (any change)
SUBMIT flow: before_submit → on_submit → on_change
CANCEL flow: before_cancel → on_cancel → on_change
DELETE:      on_trash (before), after_delete (after)
RENAME:      before_rename, after_rename
```

**Step 2: Add to hooks.py**

```python
# myapp/hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "myapp.events.sales_invoice.validate",
        "on_submit": "myapp.events.sales_invoice.on_submit"
    }
}
```

**Step 3: Create handler module**

```python
# myapp/events/sales_invoice.py
import frappe

def validate(doc, method=None):
    """Changes to doc ARE saved (before-save event)."""
    if doc.grand_total < 0:
        frappe.throw("Total cannot be negative")

def on_submit(doc, method=None):
    """Document already saved. Use db_set_value for changes."""
    frappe.db.set_value("Sales Invoice", doc.name,
                        "custom_external_id", create_external(doc))
```

**Step 4: Deploy**

```bash
bench --site sitename migrate
```

**Step 5: Test**

```bash
bench --site sitename execute myapp.events.sales_invoice.validate --kwargs '{"doc_name": "INV-001"}'
# Or in bench console:
# doc = frappe.get_doc("Sales Invoice", "INV-001"); doc.save()
```

### Critical Rules for doc_events

- **NEVER** call `frappe.db.commit()` inside a doc_event handler — Frappe manages the transaction
- **NEVER** modify `doc` fields in `on_update` — changes are lost; use `frappe.db.set_value()` instead
- **ALWAYS** accept `method=None` as second parameter in handler signature
- **ALWAYS** use rename signature: `def handler(doc, method, old, new, merge)`
- **ALWAYS** run `bench --site sitename migrate` after changing hooks.py

---

## Workflow 2: Implementing scheduler_events

### Step-by-Step

**Step 1: Choose frequency**

| Frequency | Short (< 5 min) | Long (5-25 min) |
|-----------|-----------------|------------------|
| Every tick | `all` | — |
| Hourly | `hourly` | `hourly_long` |
| Daily | `daily` | `daily_long` |
| Weekly | `weekly` | `weekly_long` |
| Monthly | `monthly` | `monthly_long` |
| Custom | `cron` | `cron` (use long queue manually) |

**Step 2: Add to hooks.py**

```python
scheduler_events = {
    "daily": ["myapp.tasks.daily_cleanup"],
    "daily_long": ["myapp.tasks.heavy_sync"],
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.weekday_report"]
    }
}
```

**Step 3: Implement task (NO arguments)**

```python
# myapp/tasks.py
import frappe

def daily_cleanup():
    """Scheduler calls with NO arguments."""
    frappe.db.delete("Error Log", {
        "creation": ["<", frappe.utils.add_days(None, -30)]
    })
    frappe.db.commit()

def heavy_sync():
    """Long task — commit periodically."""
    records = get_records_to_sync()
    for i, record in enumerate(records):
        process(record)
        if i % 100 == 0:
            frappe.db.commit()
    frappe.db.commit()
```

**Step 4: Deploy and verify**

```bash
bench --site sitename migrate
bench --site sitename scheduler enable
bench --site sitename scheduler status
# Test manually:
bench --site sitename execute myapp.tasks.daily_cleanup
```

### Critical Rules for Scheduler

- **NEVER** add parameters to scheduler task functions — the scheduler passes none
- **ALWAYS** use `_long` variants for tasks exceeding 5 minutes (default queue timeout is 5 min)
- **ALWAYS** commit periodically in long tasks to save progress
- Tasks > 25 minutes: split into chunks or use `frappe.enqueue()`

---

## Workflow 3: Implementing extend_doctype_class (V16+)

### Step-by-Step

**Step 1: Add to hooks.py**

```python
extend_doctype_class = {
    "Sales Invoice": ["myapp.extensions.sales_invoice.SalesInvoiceMixin"]
}
```

**Step 2: Create mixin class**

```python
# myapp/extensions/sales_invoice.py
import frappe
from frappe.model.document import Document

class SalesInvoiceMixin(Document):
    def validate(self):
        super().validate()  # ALWAYS call super() FIRST
        self.custom_validation()

    def custom_validation(self):
        if self.grand_total > 1000000:
            frappe.msgprint("High-value invoice", indicator="orange")
```

**Step 3: Deploy** — `bench --site sitename migrate`

### When to Use extend vs override

- **ALWAYS** prefer `extend_doctype_class` on V16+ — multiple apps can extend safely
- **ONLY** use `override_doctype_class` when you must completely replace controller logic
- On V14/V15, `override_doctype_class` is the only option — last installed app wins

---

## Workflow 4: Implementing Permission Hooks

### Step-by-Step

**Step 1: Add to hooks.py**

```python
permission_query_conditions = {
    "Sales Invoice": "myapp.permissions.si_query"
}
has_permission = {
    "Sales Invoice": "myapp.permissions.si_permission"
}
```

**Step 2: Implement handlers**

```python
# myapp/permissions.py
import frappe

def si_query(user):
    """Returns SQL WHERE clause for list filtering."""
    if not user:
        user = frappe.session.user
    if "Sales Manager" in frappe.get_roles(user):
        return ""  # See all
    return f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"

def si_permission(doc, user=None, permission_type=None):
    """Returns True (allow), False (deny), or None (use default)."""
    if not user:
        user = frappe.session.user
    if permission_type == "write" and doc.status == "Closed":
        return False
    return None
```

### Critical Rules for Permission Hooks

- `permission_query_conditions` **ONLY** works with `get_list`, **NEVER** with `get_all`
- `has_permission` can **ONLY** deny access — returning True does NOT grant additional permissions
- **ALWAYS** handle `user=None` by defaulting to `frappe.session.user`

---

## Workflow 5: Asset Injection and doctype_js

### Adding Global JS/CSS

```python
# hooks.py
app_include_js = "/assets/myapp/js/myapp.min.js"       # Desk
app_include_css = "/assets/myapp/css/myapp.min.css"     # Desk
web_include_js = "/assets/myapp/js/portal.min.js"       # Portal
web_include_css = "/assets/myapp/css/portal.min.css"    # Portal
```

### Extending a Specific Form

```python
# hooks.py
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}
```

```javascript
// myapp/public/js/sales_invoice.js
frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Custom Action"), () => {
                frappe.call({
                    method: "myapp.api.custom_action",
                    args: { invoice: frm.doc.name },
                    freeze: true
                });
            }, __("Actions"));
        }
    }
});
```

**ALWAYS** run `bench build --app myapp` after changing JS/CSS files.

---

## Workflow 6: Fixtures, Boot Info, and Website Hooks

### Fixtures

```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My App"]]}
]
```

**NEVER** export fixtures without filters — it captures ALL apps' customizations.

### extend_bootinfo

```python
extend_bootinfo = "myapp.boot.extend_with_config"
```

```python
def extend_with_config(bootinfo):
    bootinfo.my_app = {"feature_enabled": True}
    # NEVER send secrets — bootinfo is visible in browser DevTools
```

### Website Hooks

```python
website_route_rules = [
    {"from_route": "/shop/<category>", "to_route": "shop"}
]
portal_menu_items = [
    {"title": "My Orders", "route": "/my-orders", "role": "Customer"}
]
on_login = "myapp.handlers.on_login"
on_logout = "myapp.handlers.on_logout"
```

---

## Migration: Moving Logic Between Hooks, Controllers, and Server Scripts

| From | To | Steps |
|------|----|-------|
| Server Script → hooks.py | 1. Create Python handler, 2. Add doc_events, 3. Disable Server Script, 4. Migrate |
| hooks.py → Controller | 1. Move logic to doctype .py, 2. Remove doc_events entry, 3. Migrate |
| Controller → hooks.py | 1. Create events module, 2. Add doc_events, 3. Remove from controller, 4. Migrate |

**ALWAYS** migrate after ANY hooks.py change: `bench --site sitename migrate`

---

## Handler Signatures Quick Reference

| Hook | Signature |
|------|-----------|
| doc_events | `def handler(doc, method=None):` |
| rename events | `def handler(doc, method, old, new, merge):` |
| scheduler_events | `def handler():` (no args) |
| extend_bootinfo | `def handler(bootinfo):` |
| permission_query | `def handler(user):` returns SQL string |
| has_permission | `def handler(doc, user=None, permission_type=None):` returns True/False/None |
| on_login | `def handler(login_manager):` |
| on_logout | `def handler():` |

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| doc_events | Yes | Yes | Yes |
| scheduler_events | Yes | Yes | Yes |
| override_doctype_class | Yes | Yes | Yes |
| **extend_doctype_class** | No | No | **Yes** |
| permission hooks | Yes | Yes | Yes |
| Scheduler tick interval | ~4 min | ~4 min | ~60 sec |
| auth_hooks | No | Yes | Yes |

---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete hook selection flowcharts |
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns |
| [examples.md](references/examples.md) | Working code examples for all hook types |
