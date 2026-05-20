---
name: frappe-impl-controllers
description: >
  Use when building Document Controllers in a custom Frappe app:
  file creation, lifecycle hooks, validation, autoname, submittable
  workflows, controller override, child table controllers, flags system,
  migration from hooks.py and Server Scripts. Keywords: how to implement
  controller, which hook to use, validate vs on_update, override controller,
  submittable document, autoname, flags, extend_doctype_class, controller
  testing, child table controller.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Document Controllers — Implementation Workflows

Step-by-step workflows for building server-side DocType logic with full Python power. For exact syntax, see `frappe-syntax-controllers`.

**Version**: v14/v15/v16 | **v15+**: Supports auto-generated type annotations

## Quick Decision: Controller vs Server Script?

```
NEED full Python (imports, classes, generators)?     → Controller
NEED external libraries (requests, pandas)?          → Controller
NEED try/except with rollback?                       → Controller
NEED frappe.enqueue() for background jobs?           → Controller
NEED to extend standard ERPNext DocType?             → Controller
Quick validation without custom app?                 → Server Script
Simple auto-fill or notification?                    → Server Script
```

**Rule**: ALWAYS use Controllers when you need a custom app. ALWAYS use Server Scripts for no-code prototyping.

## Workflow 1: Create a New Controller

**Step 1**: Create DocType via Frappe UI or `bench new-doctype`

**Step 2**: File is auto-generated at:
```
apps/myapp/myapp/{module}/doctype/{doctype_name}/{doctype_name}.py
```

**Step 3**: Implement the controller class:

```python
import frappe
from frappe import _
from frappe.model.document import Document

class MyDocType(Document):
    def validate(self):
        self.validate_dates()
        self.calculate_totals()

    def validate_dates(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw(_("From Date cannot be after To Date"))

    def calculate_totals(self):
        self.total = sum(item.amount for item in self.items)
```

**Step 4**: Run `bench restart` (or `bench watch` for hot-reload in dev)

**Naming convention**: DocType "Sales Order" → class `SalesOrder`, file `sales_order.py`

## Workflow 2: Choose the Right Hook

```
WHAT DO YOU WANT?
├── Validate data / calculate fields before save?
│   └── validate — changes to self ARE saved
│
├── Action AFTER save (emails, linked docs, logs)?
│   └── on_update — changes to self NOT saved (use db_set)
│
├── Only for NEW documents?
│   └── after_insert
│
├── Before/after SUBMIT?
│   ├── Check before submit → before_submit
│   └── Ledger entries after → on_submit
│
├── Before/after CANCEL?
│   ├── Prevent cancel → before_cancel
│   └── Reverse entries → on_cancel
│
├── Before DELETE?
│   └── on_trash (throw to prevent)
│
├── Custom document naming?
│   └── autoname
│
└── Detect ANY change (including db_set)?
    └── on_change
```

> See [references/decision-tree.md](references/decision-tree.md) for all hooks with execution order.

## CRITICAL: validate vs on_update

| Aspect | `validate` | `on_update` |
|--------|-----------|-------------|
| When | Before DB write | After DB write |
| `self.x = y` saved? | YES | **NO** — use `db_set` |
| Can abort with throw? | YES | Already saved |
| `get_doc_before_save()` | Available | Available |
| Use for | Validation, calculations | Notifications, linked docs |

```python
# WRONG — changes in on_update are NOT saved
def on_update(self):
    self.status = "Completed"  # LOST!

# CORRECT — use db_set
def on_update(self):
    frappe.db.set_value(self.doctype, self.name, "status", "Completed")
```

## Workflow 3: Validation with Error Collection

```python
def validate(self):
    errors = []
    if not self.items:
        errors.append(_("At least one item is required"))
    for item in self.items:
        if item.qty <= 0:
            errors.append(_("Row {0}: Qty must be positive").format(item.idx))
    if self.from_date > self.to_date:
        errors.append(_("From Date cannot be after To Date"))
    if errors:
        frappe.throw("<br>".join(errors))
```

## Workflow 4: Detect Field Changes

```python
def validate(self):
    old = self.get_doc_before_save()
    if old and old.status != self.status:
        self.flags.status_changed = True
        self.status_changed_on = frappe.utils.now()

def on_update(self):
    if self.flags.get('status_changed'):
        self.notify_status_change()
```

**Rule**: ALWAYS use `self.flags` to pass data between hooks. NEVER rely on external state.

## Workflow 5: Custom Naming (autoname)

```python
from frappe.model.naming import getseries

def autoname(self):
    # Format: PRJ-CUST-2025-001
    code = (self.customer or "GEN")[:4].upper()
    year = frappe.utils.getdate(self.start_date or frappe.utils.today()).year
    prefix = f"PRJ-{code}-{year}-"
    self.name = getseries(prefix, 3)
```

**Alternative — before_naming**:
```python
def before_naming(self):
    if self.is_priority:
        self.naming_series = "PRIORITY-.#####"
    else:
        self.naming_series = "STD-.#####"
```

## Workflow 6: Submittable Document

```
DRAFT (docstatus=0) → submit() → SUBMITTED (docstatus=1) → cancel() → CANCELLED (docstatus=2)

submit():  validate → before_submit → [DB: docstatus=1] → on_update → on_submit
cancel():  before_cancel → [DB: docstatus=2] → on_cancel
```

```python
class PurchaseOrder(Document):
    def validate(self):
        self.validate_items()
        self.calculate_totals()

    def before_submit(self):
        # ONLY submit-specific checks here
        if self.total > 100000 and not self.manager_approval:
            frappe.throw(_("Manager approval required for POs over 100,000"))

    def on_submit(self):
        self.update_ordered_qty()
        self.create_purchase_receipt_draft()

    def before_cancel(self):
        if frappe.db.exists("Purchase Invoice",
                {"purchase_order": self.name, "docstatus": 1}):
            frappe.throw(_("Cancel linked invoices first"))

    def on_cancel(self):
        self.reverse_ordered_qty()
```

**Rule**: NEVER duplicate validation between `validate` and `before_submit`. `validate` ALWAYS runs before `before_submit`.

## Workflow 7: Override Standard ERPNext Controller

### Method A: Full Override (hooks.py)

```python
# hooks.py
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}

# myapp/overrides.py
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()  # ALWAYS call parent first
        self.custom_validation()
```

### Method B: Event Handler (Safer, no class override)

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

### Method C: extend_doctype_class (v16+)

```python
# hooks.py
extend_doctype_class = {
    "Sales Invoice": "myapp.extends.SalesInvoiceExtend"
}

# myapp/extends.py — Only methods to add/override
class SalesInvoiceExtend:
    def custom_method(self):
        pass
```

**Rule**: ALWAYS call `super().validate()` in override. NEVER skip parent methods — standard ERPNext logic depends on it.

## Workflow 8: Whitelisted Methods (Client-Callable)

```python
class Quotation(Document):
    @frappe.whitelist()
    def apply_discount(self, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            frappe.throw(_("Discount must be 0-100"))
        self.discount_amount = self.total * (discount_percent / 100)
        self.grand_total = self.total - self.discount_amount
        self.save()
        return {"grand_total": self.grand_total}
```

Client-side call:
```javascript
frm.call('apply_discount', { discount_percent: 10 }).then(r => {
    frm.reload_doc();
});
```

## Workflow 9: Flags System

```python
# Document-level flags (built-in)
doc.flags.ignore_permissions = True    # Bypass permission checks
doc.flags.ignore_validate = True       # Skip validate() hook
doc.flags.ignore_mandatory = True      # Skip required field check

# Custom flags for inter-hook communication
def validate(self):
    if self.is_urgent:
        self.flags.needs_notification = True

def on_update(self):
    if self.flags.get('needs_notification'):
        self.notify_team()
```

## Workflow 10: Testing Controllers

```python
# tests/test_my_doctype.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestMyDocType(FrappeTestCase):
    def test_validate_dates(self):
        doc = frappe.get_doc({
            "doctype": "My DocType",
            "from_date": "2025-01-10",
            "to_date": "2025-01-01"  # Before from_date
        })
        self.assertRaises(frappe.ValidationError, doc.insert)

    def test_calculate_totals(self):
        doc = frappe.get_doc({
            "doctype": "My DocType",
            "items": [
                {"item": "A", "qty": 2, "rate": 100},
                {"item": "B", "qty": 3, "rate": 50}
            ]
        })
        doc.insert()
        self.assertEqual(doc.total, 350)
```

Run: `bench run-tests --module myapp.module.doctype.my_doctype.test_my_doctype`

## Execution Order Reference

### INSERT
```
before_insert → before_naming → autoname → before_validate →
validate → before_save → [DB INSERT] → after_insert →
on_update → on_change
```

### SAVE (existing)
```
before_validate → validate → before_save → [DB UPDATE] →
on_update → on_change
```

### SUBMIT
```
validate → before_submit → [DB: docstatus=1] →
on_update → on_submit → on_change
```

## Anti-Pattern Quick Check

| Do NOT | Do Instead |
|--------|------------|
| `self.x = y` in on_update | `frappe.db.set_value(...)` |
| `self.save()` in on_update | Causes infinite loop |
| `frappe.db.commit()` in hooks | Let framework handle |
| Heavy ops in validate | Use `frappe.enqueue()` in on_update |
| Skip `super().validate()` | ALWAYS call parent first |
| `frappe.get_doc()` in loops | Use `frappe.get_cached_doc()` |
| Hardcoded thresholds | Use Settings DocType |

> See [references/anti-patterns.md](references/anti-patterns.md) for complete list.

## Related Skills

- `frappe-syntax-controllers` — Exact hook signatures and API
- `frappe-errors-controllers` — Error handling patterns
- `frappe-impl-serverscripts` — When Server Script suffices
- `frappe-syntax-hooks` — hooks.py configuration
- `frappe-core-database` — `frappe.db.*` operations

> See [references/decision-tree.md](references/decision-tree.md) for all hooks.
> See [references/workflows.md](references/workflows.md) for extended patterns.
> See [references/examples.md](references/examples.md) for complete working examples.
