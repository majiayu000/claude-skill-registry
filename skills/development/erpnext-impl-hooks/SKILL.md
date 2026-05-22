---
name: erpnext-impl-hooks
description: "Implementation workflows and decision trees for Frappe hooks.py configuration. Use when determining HOW to implement doc_events, scheduler_events, override hooks, permission hooks, extend_bootinfo, fixtures, and asset includes. Covers V16 extend_doctype_class. Triggers: how do I hook, which hook to use, doc_events vs controller, override doctype, extend doctype class, permission hook, scheduler job, cron task, fixtures export."
---

# ERPNext Hooks - Implementation

This skill helps you determine HOW to implement hooks.py configurations. For exact syntax, see `erpnext-syntax-hooks`.

**Version**: v14/v15/v16 compatible (with V16-specific features noted)

## Main Decision: What Are You Trying to Do?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT DO YOU WANT TO ACHIEVE?                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► React to document events on OTHER apps' DocTypes?                     │
│   └── doc_events in hooks.py                                            │
│                                                                         │
│ ► Run code periodically (hourly, daily, custom schedule)?               │
│   └── scheduler_events                                                  │
│                                                                         │
│ ► Modify behavior of existing DocType controller?                       │
│   ├── V16+: extend_doctype_class (RECOMMENDED - multiple apps work)     │
│   └── V14/V15: override_doctype_class (last app wins)                   │
│                                                                         │
│ ► Modify existing API endpoint behavior?                                │
│   └── override_whitelisted_methods                                      │
│                                                                         │
│ ► Add custom permission logic?                                          │
│   ├── List filtering: permission_query_conditions                       │
│   └── Document-level: has_permission                                    │
│                                                                         │
│ ► Send data to client on page load?                                     │
│   └── extend_bootinfo                                                   │
│                                                                         │
│ ► Export/import configuration between sites?                            │
│   └── fixtures                                                          │
│                                                                         │
│ ► Add JS/CSS to desk or portal?                                         │
│   ├── Desk: app_include_js/css                                          │
│   ├── Portal: web_include_js/css                                        │
│   └── Specific form: doctype_js                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree: doc_events vs Controller Methods

```
WHERE IS THE DOCTYPE?
│
├─► DocType is in YOUR custom app?
│   └─► Use controller methods (doctype/xxx/xxx.py)
│       - Direct control over lifecycle
│       - Cleaner code organization
│
├─► DocType is in ANOTHER app (ERPNext, Frappe)?
│   └─► Use doc_events in hooks.py
│       - Only way to hook external DocTypes
│       - Can register multiple handlers
│
└─► Need to hook ALL DocTypes (logging, audit)?
    └─► Use doc_events with wildcard "*"
```

**Rule**: Controller methods for YOUR DocTypes, doc_events for OTHER apps' DocTypes.

---

## Decision Tree: Which doc_event?

```
WHAT DO YOU NEED TO DO?
│
├─► Validate data or calculate fields?
│   ├─► Before any save → validate
│   └─► Only on new documents → before_insert
│
├─► React after document is saved?
│   ├─► Only first save → after_insert
│   ├─► Every save → on_update
│   └─► ANY change (including db_set) → on_change
│
├─► Handle submittable documents?
│   ├─► Before submit → before_submit
│   ├─► After submit → on_submit (ledger entries here)
│   ├─► Before cancel → before_cancel
│   └─► After cancel → on_cancel (reverse entries here)
│
├─► Handle document deletion?
│   ├─► Before delete (can prevent) → on_trash
│   └─► After delete (cleanup) → after_delete
│
└─► Handle document rename?
    ├─► Before rename → before_rename
    └─► After rename → after_rename
```

---

## Decision Tree: Scheduler Event Type

```
HOW LONG DOES YOUR TASK RUN?
│
├─► < 5 minutes
│   │
│   │ HOW OFTEN?
│   ├─► Every ~60 seconds → all
│   ├─► Every hour → hourly
│   ├─► Every day → daily
│   ├─► Every week → weekly
│   ├─► Every month → monthly
│   └─► Specific time → cron
│
└─► > 5 minutes (up to 25 minutes)
    │
    │ HOW OFTEN?
    ├─► Every hour → hourly_long
    ├─► Every day → daily_long
    ├─► Every week → weekly_long
    └─► Every month → monthly_long

⚠️ Tasks > 25 minutes: Split into chunks or use background jobs
```

---

## Decision Tree: Override vs Extend (V16)

```
FRAPPE VERSION?
│
├─► V16+
│   │
│   │ WHAT DO YOU NEED?
│   ├─► Add methods/properties to DocType?
│   │   └─► extend_doctype_class (RECOMMENDED)
│   │       - Multiple apps can extend same DocType
│   │       - Safer, less breakage on updates
│   │
│   └─► Completely replace controller logic?
│       └─► override_doctype_class (use sparingly)
│
└─► V14/V15
    └─► override_doctype_class (only option)
        ⚠️ Last installed app wins!
        ⚠️ Always call super() in methods!
```

---

## Implementation Workflow: doc_events

### Step 1: Add to hooks.py

```python
# myapp/hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "myapp.events.sales_invoice.validate",
        "on_submit": "myapp.events.sales_invoice.on_submit"
    }
}
```

### Step 2: Create handler module

```python
# myapp/events/sales_invoice.py
import frappe

def validate(doc, method=None):
    """
    Args:
        doc: The document object
        method: Event name ("validate")
    
    Changes to doc ARE saved (before save event)
    """
    if doc.grand_total < 0:
        frappe.throw("Total cannot be negative")
    
    # Calculate custom field
    doc.custom_margin = doc.grand_total - doc.total_cost

def on_submit(doc, method=None):
    """
    After submit - document already saved
    Use frappe.db.set_value for additional changes
    """
    create_external_record(doc)
```

### Step 3: Deploy

```bash
bench --site sitename migrate
```

---

## Implementation Workflow: scheduler_events

### Step 1: Add to hooks.py

```python
# myapp/hooks.py
scheduler_events = {
    "daily": ["myapp.tasks.daily_cleanup"],
    "daily_long": ["myapp.tasks.heavy_processing"],
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.weekday_report"]
    }
}
```

### Step 2: Create task module

```python
# myapp/tasks.py
import frappe

def daily_cleanup():
    """NO arguments - scheduler calls with no args"""
    old_logs = frappe.get_all(
        "Error Log",
        filters={"creation": ["<", frappe.utils.add_days(None, -30)]},
        pluck="name"
    )
    for name in old_logs:
        frappe.delete_doc("Error Log", name)

def heavy_processing():
    """Long task - use _long variant in hooks"""
    for batch in get_batches():
        process_batch(batch)
        frappe.db.commit()  # Commit per batch for long tasks
```

### Step 3: Deploy and verify

```bash
bench --site sitename migrate
bench --site sitename scheduler enable
bench --site sitename scheduler status
```

---

## Implementation Workflow: extend_doctype_class (V16+)

### Step 1: Add to hooks.py

```python
# myapp/hooks.py
extend_doctype_class = {
    "Sales Invoice": ["myapp.extensions.SalesInvoiceMixin"]
}
```

### Step 2: Create mixin class

```python
# myapp/extensions.py
import frappe
from frappe.model.document import Document

class SalesInvoiceMixin(Document):
    """Mixin that extends Sales Invoice"""
    
    @property
    def profit_margin(self):
        """Add computed property"""
        if self.grand_total:
            return ((self.grand_total - self.total_cost) / self.grand_total) * 100
        return 0
    
    def validate(self):
        """Extend validation - ALWAYS call super()"""
        super().validate()
        self.validate_margin()
    
    def validate_margin(self):
        """Custom validation logic"""
        if self.profit_margin < 10:
            frappe.msgprint("Warning: Low margin invoice")
```

### Step 3: Deploy

```bash
bench --site sitename migrate
```

---

## Implementation Workflow: Permission Hooks

### Step 1: Add to hooks.py

```python
# myapp/hooks.py
permission_query_conditions = {
    "Sales Invoice": "myapp.permissions.si_query"
}
has_permission = {
    "Sales Invoice": "myapp.permissions.si_permission"
}
```

### Step 2: Create permission handlers

```python
# myapp/permissions.py
import frappe

def si_query(user):
    """
    Returns SQL WHERE clause for list filtering.
    ONLY works with get_list, NOT get_all!
    """
    if not user:
        user = frappe.session.user
    
    if "Sales Manager" in frappe.get_roles(user):
        return ""  # No filter - see all
    
    # Regular users see only their own
    return f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"

def si_permission(doc, user=None, permission_type=None):
    """
    Document-level permission check.
    Return: True (allow), False (deny), None (use default)
    
    NOTE: Can only DENY, not grant additional permissions!
    """
    if permission_type == "write" and doc.status == "Closed":
        return False  # Deny write on closed invoices
    
    return None  # Use default permission system
```

---

## Quick Reference: Handler Signatures

| Hook | Signature |
|------|-----------|
| doc_events | `def handler(doc, method=None):` |
| rename events | `def handler(doc, method, old, new, merge):` |
| scheduler_events | `def handler():` (no args) |
| extend_bootinfo | `def handler(bootinfo):` |
| permission_query | `def handler(user):` → returns SQL string |
| has_permission | `def handler(doc, user=None, permission_type=None):` → True/False/None |
| override methods | Must match original signature exactly |

---

## Critical Rules

### 1. Never commit in doc_events

```python
# ❌ WRONG - breaks transaction
def on_update(doc, method=None):
    frappe.db.commit()

# ✅ CORRECT - Frappe commits automatically
def on_update(doc, method=None):
    update_related(doc)
```

### 2. Use db_set_value after on_update

```python
# ❌ WRONG - change is lost
def on_update(doc, method=None):
    doc.status = "Processed"

# ✅ CORRECT
def on_update(doc, method=None):
    frappe.db.set_value(doc.doctype, doc.name, "status", "Processed")
```

### 3. Always call super() in overrides

```python
# ❌ WRONG - breaks core functionality
class CustomInvoice(SalesInvoice):
    def validate(self):
        self.my_validation()

# ✅ CORRECT
class CustomInvoice(SalesInvoice):
    def validate(self):
        super().validate()  # FIRST!
        self.my_validation()
```

### 4. Always migrate after hooks changes

```bash
# Required after ANY hooks.py change
bench --site sitename migrate
```

### 5. permission_query only works with get_list

```python
# ❌ NOT filtered by permission_query_conditions
frappe.db.get_all("Sales Invoice", filters={})

# ✅ Filtered by permission_query_conditions
frappe.db.get_list("Sales Invoice", filters={})
```

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| doc_events | ✅ | ✅ | ✅ |
| scheduler_events | ✅ | ✅ | ✅ |
| override_doctype_class | ✅ | ✅ | ✅ |
| **extend_doctype_class** | ❌ | ❌ | ✅ |
| permission hooks | ✅ | ✅ | ✅ |
| Scheduler tick | 4 min | 4 min | 60 sec |

---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete hook selection flowcharts |
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns |
| [examples.md](references/examples.md) | Working code examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes and solutions |
