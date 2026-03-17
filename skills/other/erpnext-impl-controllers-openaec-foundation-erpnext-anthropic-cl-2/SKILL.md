---
name: erpnext-impl-controllers
description: "Implementation workflows and decision trees for Frappe Document Controllers. Use when determining HOW to implement server-side DocType logic: lifecycle hooks, validation patterns, autoname, submittable workflows, controller override. Triggers: how do I implement controller, which hook to use, validate vs on_update, override controller, submittable document, autoname pattern, flags system."
---

# ERPNext Controllers - Implementation

This skill helps you determine HOW to implement server-side DocType logic. For exact syntax, see `erpnext-syntax-controllers`.

**Version**: v14/v15/v16 compatible

## Main Decision: Controller vs Server Script?

```
┌───────────────────────────────────────────────────────────────────┐
│ WHAT DO YOU NEED?                                                 │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ► Import external libraries (requests, pandas, numpy)             │
│   └── Controller ✓                                                │
│                                                                   │
│ ► Complex multi-document transactions with rollback               │
│   └── Controller ✓                                                │
│                                                                   │
│ ► Full Python power (try/except, classes, generators)             │
│   └── Controller ✓                                                │
│                                                                   │
│ ► Extend/override standard ERPNext DocType                        │
│   └── Controller (override_doctype_class in hooks.py)             │
│                                                                   │
│ ► Quick validation without custom app                             │
│   └── Server Script                                               │
│                                                                   │
│ ► Simple auto-fill or calculation                                 │
│   └── Server Script                                               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

**Rule**: Controllers for custom apps with full Python power. Server Scripts for quick no-code solutions.

## Decision Tree: Which Hook?

```
WHAT DO YOU WANT TO DO?
│
├─► Validate data or calculate fields before save?
│   └─► validate
│       NOTE: Changes to self ARE saved
│
├─► Action AFTER save (emails, linked docs, logs)?
│   └─► on_update
│       ⚠️ Changes to self are NOT saved! Use db_set instead
│
├─► Only for NEW documents?
│   └─► after_insert
│
├─► Only for SUBMIT (docstatus 0→1)?
│   ├─► Check before submit? → before_submit
│   └─► Action after submit? → on_submit
│
├─► Only for CANCEL (docstatus 1→2)?
│   ├─► Prevent cancel? → before_cancel
│   └─► Cleanup after cancel? → on_cancel
│
├─► Before DELETE?
│   └─► on_trash
│
├─► Custom document naming?
│   └─► autoname
│
└─► Detect any change (including db_set)?
    └─► on_change
```

→ See [references/decision-tree.md](references/decision-tree.md) for complete decision tree with all hooks.

## CRITICAL: Changes After on_update

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  CHANGES TO self AFTER on_update ARE NOT SAVED                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ❌ WRONG - This does NOTHING:                                       │
│    def on_update(self):                                             │
│        self.status = "Completed"  # NOT SAVED!                      │
│                                                                     │
│ ✅ CORRECT - Use db_set:                                            │
│    def on_update(self):                                             │
│        frappe.db.set_value(self.doctype, self.name,                 │
│                           "status", "Completed")                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Hook Comparison: validate vs on_update

| Aspect | validate | on_update |
|--------|----------|-----------|
| When | Before DB write | After DB write |
| Changes to self | ✅ Saved | ❌ NOT saved |
| Can throw error | ✅ Aborts save | ⚠️ Already saved |
| Use for | Validation, calculations | Notifications, linked docs |
| get_doc_before_save() | ✅ Available | ✅ Available |

## Common Implementation Patterns

### Pattern 1: Validation with Error

```python
def validate(self):
    if not self.items:
        frappe.throw(_("At least one item is required"))
    
    if self.from_date > self.to_date:
        frappe.throw(_("From Date cannot be after To Date"))
```

### Pattern 2: Auto-Calculate Fields

```python
def validate(self):
    self.total = sum(item.amount for item in self.items)
    self.tax_amount = self.total * 0.1
    self.grand_total = self.total + self.tax_amount
```

### Pattern 3: Detect Field Changes

```python
def validate(self):
    old_doc = self.get_doc_before_save()
    if old_doc and old_doc.status != self.status:
        self.flags.status_changed = True
        
def on_update(self):
    if self.flags.get('status_changed'):
        self.notify_status_change()
```

### Pattern 4: Post-Save Actions

```python
def on_update(self):
    # Update linked document
    if self.linked_doc:
        frappe.db.set_value("Other DocType", self.linked_doc, 
                          "status", "Updated")
    
    # Send notification (never fails the save)
    try:
        self.send_notification()
    except Exception:
        frappe.log_error("Notification failed")
```

### Pattern 5: Custom Naming

```python
from frappe.model.naming import getseries

def autoname(self):
    # Format: CUST-ABC-001
    prefix = f"CUST-{self.customer[:3].upper()}-"
    self.name = getseries(prefix, 3)
```

→ See [references/workflows.md](references/workflows.md) for more implementation patterns.

## Submittable Documents Workflow

```
DRAFT (docstatus=0)
    │
    ├── save() → validate → on_update
    │
    └── submit()
         │
         ├── validate
         ├── before_submit  ← Last chance to abort
         ├── [DB: docstatus=1]
         ├── on_update
         └── on_submit      ← Post-submit actions

SUBMITTED (docstatus=1)
    │
    └── cancel()
         │
         ├── before_cancel  ← Last chance to abort
         ├── [DB: docstatus=2]
         ├── on_cancel      ← Reverse actions
         └── [check_no_back_links]
```

### Submittable Implementation

```python
def before_submit(self):
    # Validation that only applies on submit
    if self.total > 50000 and not self.manager_approval:
        frappe.throw(_("Manager approval required for orders over 50,000"))

def on_submit(self):
    # Actions after submit
    self.update_stock_ledger()
    self.make_gl_entries()

def before_cancel(self):
    # Prevent cancel if linked docs exist
    if self.has_linked_invoices():
        frappe.throw(_("Cannot cancel - linked invoices exist"))

def on_cancel(self):
    # Reverse submitted actions
    self.reverse_stock_ledger()
    self.reverse_gl_entries()
```

## Controller Override (hooks.py)

### Method 1: Full Override

```python
# hooks.py
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}

# myapp/overrides.py
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()  # ALWAYS call parent
        self.custom_validation()
```

### Method 2: Add Event Handler (Safer)

```python
# hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "myapp.events.validate_sales_invoice",
    }
}

# myapp/events.py
def validate_sales_invoice(doc, method=None):
    if doc.grand_total < 0:
        frappe.throw(_("Invalid total"))
```

### V16: extend_doctype_class (New)

```python
# hooks.py (v16+)
extend_doctype_class = {
    "Sales Invoice": "myapp.extends.SalesInvoiceExtend"
}

# myapp/extends.py - Only methods to add/override
class SalesInvoiceExtend:
    def custom_method(self):
        pass
```

## Flags System

```python
# Document-level flags
doc.flags.ignore_permissions = True   # Bypass permissions
doc.flags.ignore_validate = True      # Skip validate()
doc.flags.ignore_mandatory = True     # Skip required fields

# Custom flags for inter-hook communication
def validate(self):
    if self.is_urgent:
        self.flags.needs_notification = True
        
def on_update(self):
    if self.flags.get('needs_notification'):
        self.notify_team()

# Insert/save with flags
doc.insert(ignore_permissions=True, ignore_mandatory=True)
doc.save(ignore_permissions=True)
```

## Execution Order Reference

### INSERT (New Document)
```
before_insert → before_naming → autoname → before_validate →
validate → before_save → [DB INSERT] → after_insert → 
on_update → on_change
```

### SAVE (Existing Document)
```
before_validate → validate → before_save → [DB UPDATE] →
on_update → on_change
```

### SUBMIT
```
validate → before_submit → [DB: docstatus=1] → on_update →
on_submit → on_change
```

→ See [references/decision-tree.md](references/decision-tree.md) for all execution orders.

## Quick Anti-Pattern Check

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| `self.x = y` in on_update | `frappe.db.set_value(...)` |
| `frappe.db.commit()` in hooks | Let framework handle commits |
| Heavy operations in validate | Use `frappe.enqueue()` in on_update |
| `self.save()` in on_update | Causes infinite loop! |
| Assume hook order across docs | Each doc has its own cycle |

→ See [references/anti-patterns.md](references/anti-patterns.md) for complete list.

## References

- [decision-tree.md](references/decision-tree.md) - Complete hook selection with all execution orders
- [workflows.md](references/workflows.md) - Extended implementation patterns
- [examples.md](references/examples.md) - Complete working examples
- [anti-patterns.md](references/anti-patterns.md) - Common mistakes to avoid
