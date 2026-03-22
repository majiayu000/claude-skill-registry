---
name: frappe-syntax-controllers
description: >
  Use when writing Python Document Controllers for ERPNext/Frappe DocTypes.
  Covers lifecycle hooks (validate, on_update, on_submit), controller
  override, submittable documents, autoname patterns, UUID naming (v16),
  and the flags system. Keywords: document controller, lifecycle hook,
  validate, on_update, on_submit, autoname, naming series, flags, v14-v16.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Syntax: Document Controllers

Document Controllers are Python classes that define all server-side logic for a DocType.
EVERY DocType has exactly one controller file. The controller class extends `frappe.model.document.Document`.

## Quick Reference

```python
import frappe
from frappe import _
from frappe.model.document import Document

class SalesOrder(Document):
    def autoname(self):
        """Custom naming logic. Sets self.name."""
        self.name = f"SO-{self.customer_code}-{frappe.utils.now_datetime().year}"

    def validate(self):
        """MAIN validation — runs on EVERY save (insert and update).
        Changes to self ARE saved to database."""
        if not self.items:
            frappe.throw(_("Items are required"))
        self.total = sum(item.amount for item in self.items)

    def on_update(self):
        """After save — changes to self are NOT saved.
        Use frappe.db.set_value() for post-save field changes."""
        self.notify_linked_docs()

    def on_submit(self):
        """After submit (docstatus 0 -> 1). Create ledger entries here."""
        self.create_gl_entries()

    def on_cancel(self):
        """After cancel (docstatus 1 -> 2). Reverse ledger entries here."""
        self.reverse_gl_entries()

    @frappe.whitelist()
    def recalculate(self):
        """Exposed to client JS via frm.call('recalculate')."""
        self.total = sum(item.amount for item in self.items)
        return {"total": self.total}
```

### File Location and Naming

| DocType Name | Class Name | File Path |
|---|---|---|
| Sales Order | `SalesOrder` | `selling/doctype/sales_order/sales_order.py` |
| My Custom Doc | `MyCustomDoc` | `module/doctype/my_custom_doc/my_custom_doc.py` |

**Rule**: DocType name -> PascalCase class -> snake_case filename. ALWAYS match exactly.

---

## Lifecycle Hook Execution Order

### INSERT (new document)

```
before_insert -> before_naming -> autoname -> before_validate -> validate
-> before_save -> [db_insert] -> after_insert -> on_update -> on_change
```

### SAVE (existing document)

```
before_validate -> validate -> before_save -> [db_update]
-> on_update -> on_change
```

### SUBMIT (docstatus 0 -> 1)

```
before_validate -> validate -> before_submit -> [db_update]
-> on_submit -> on_update -> on_change
```

### CANCEL (docstatus 1 -> 2)

```
before_cancel -> [db_update] -> on_cancel -> on_change
```

### UPDATE AFTER SUBMIT

```
before_update_after_submit -> [db_update]
-> on_update_after_submit -> on_change
```

### DELETE

```
on_trash -> [db_delete] -> after_delete
```

### DISCARD [v15+]

```
before_discard -> [db_set docstatus=2] -> on_discard
```

**Complete hook reference with parameters**: See [lifecycle-methods.md](references/lifecycle-methods.md)

---

## Hook Selection Decision Tree

```
What do you need to do?
|
+-- Validate data or calculate fields?
|   +-- validate (changes to self ARE saved)
|
+-- Action AFTER save (emails, sync, linked docs)?
|   +-- on_update (changes to self are NOT saved)
|
+-- Only for NEW documents?
|   +-- after_insert (runs once on first save only)
|
+-- Custom document name?
|   +-- autoname (set self.name)
|
+-- Before/after SUBMIT?
|   +-- Validate before submit? -> before_submit
|   +-- Create entries after submit? -> on_submit
|
+-- Before/after CANCEL?
|   +-- Check linked docs? -> before_cancel
|   +-- Reverse entries? -> on_cancel
|
+-- Cleanup before delete?
|   +-- on_trash
|
+-- React to ANY value change (including db_set)?
|   +-- on_change (MUST be idempotent)
```

---

## Critical Rules

### 1. Changes after on_update are NOT saved

```python
# WRONG - change is lost after on_update
def on_update(self):
    self.status = "Completed"  # NOT saved to database

# CORRECT - use db_set or frappe.db.set_value
def on_update(self):
    self.db_set("status", "Completed")
```

### 2. NEVER call frappe.db.commit() in controllers

```python
# WRONG - breaks Frappe transaction management
def validate(self):
    frappe.db.commit()  # Can cause partial updates on error

# CORRECT - Frappe commits automatically at end of request
def validate(self):
    self.update_related()  # No commit needed
```

### 3. ALWAYS call super() when overriding

```python
# WRONG - parent validation is skipped entirely
def validate(self):
    self.custom_check()

# CORRECT - parent logic preserved
def validate(self):
    super().validate()
    self.custom_check()
```

### 4. Use flags for recursion prevention

```python
def on_update(self):
    if self.flags.get("from_linked_doc"):
        return
    linked = frappe.get_doc("Linked Doc", self.linked_doc)
    linked.flags.from_linked_doc = True
    linked.save()
```

### 5. NEVER put validation logic in on_update

```python
# WRONG - document is already saved when this throws
def on_update(self):
    if self.total < 0:
        frappe.throw("Invalid total")  # Too late!

# CORRECT - validate BEFORE save
def validate(self):
    if self.total < 0:
        frappe.throw("Invalid total")  # Blocks save
```

---

## Document Naming (autoname)

| Method | Example | Result | Version |
|---|---|---|---|
| `field:fieldname` | `field:customer_name` | `ABC Company` | All |
| `naming_series:` | `naming_series:` | `SO-2024-00001` | All |
| Expression | `PRE-.#####` | `PRE-00001` | All |
| Old-style format | `INV-{YYYY}-{####}` | `INV-2024-0001` | Deprecated v16 |
| `hash` / `random` | `hash` | `a1b2c3d4e5` | All |
| `Prompt` | `Prompt` | User enters name | All |
| `autoincrement` | `autoincrement` | `1`, `2`, `3` | All |
| **`UUID`** | `UUID` | `550e8400-e29b-...` | **v16+** |
| Custom method | `autoname()` in controller | Any pattern | All |

### Custom autoname Method

```python
from frappe.model.naming import getseries

class Project(Document):
    def autoname(self):
        prefix = f"P-{self.customer[:3].upper()}-"
        self.name = getseries(prefix, 3)
        # Result: P-ACM-001, P-ACM-002, etc.
```

### UUID Naming [v16+]

Set `autoname = "UUID"` in DocType definition. Frappe generates UUID v4.

```
When to use UUID:              When to use traditional naming:
- Cross-system sync            - User-facing references (SO-00001)
- Bulk record creation         - Sequential numbering required
- Global uniqueness needed     - Auditing requires readable names
```

---

## Controller Extension Mechanisms

### 1. override_doctype_class (full replacement) [All versions]

```python
# hooks.py
override_doctype_class = {
    "Sales Order": "custom_app.overrides.CustomSalesOrder"
}

# custom_app/overrides.py
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomSalesOrder(SalesOrder):
    def validate(self):
        super().validate()  # ALWAYS call super()
        self.custom_validation()
```

**WARNING**: Only ONE app can override a DocType class. Multiple overrides conflict.

### 2. extend_doctype_class (mixin, non-destructive) [v16+]

```python
# hooks.py
extend_doctype_class = {
    "Address": ["custom_app.extensions.address.GeocodingMixin"],
    "Contact": [
        "custom_app.extensions.common.ValidationMixin",
        "custom_app.extensions.contact.PhoneMixin"
    ]
}

# custom_app/extensions/address.py
from frappe.model.document import Document

class GeocodingMixin(Document):
    @property
    def full_address(self):
        return f"{self.address_line1}, {self.city}, {self.country}"

    def validate(self):
        super().validate()
        self.geocode_address()
```

**ALWAYS prefer `extend_doctype_class` over `override_doctype_class` in v16+.**
Multiple apps can safely extend the same DocType.

### 3. doc_events (hook individual events) [All versions]

```python
# hooks.py
doc_events = {
    "Sales Order": {
        "validate": "custom_app.events.validate_sales_order",
        "on_submit": "custom_app.events.on_submit_sales_order"
    },
    "*": {  # ALL DocTypes
        "after_insert": "custom_app.events.log_creation"
    }
}

# custom_app/events.py
def validate_sales_order(doc, method=None):
    if doc.total > 100000:
        doc.requires_approval = 1
```

### When to Use Which

```
Need full class replacement?     -> override_doctype_class [all versions]
Need to add methods/properties?  -> extend_doctype_class [v16+]
Need to hook one or two events?  -> doc_events [all versions]
Need to extend in v14/v15?       -> override_doctype_class or doc_events
```

---

## Whitelisted Methods

Expose controller methods to client-side JavaScript with `@frappe.whitelist()`:

```python
class SalesOrder(Document):
    @frappe.whitelist()
    def send_email(self, recipient):
        """Callable from JS: frm.call('send_email', {recipient: '...'})"""
        frappe.sendmail(recipients=[recipient], message="Order confirmed")
        return {"status": "sent"}
```

```javascript
// Client-side call
frm.call('send_email', { recipient: 'customer@example.com' })
    .then(r => frappe.msgprint(r.message.status));
```

**Rules**:
- ALWAYS add `@frappe.whitelist()` decorator — without it, the method is NOT callable from client
- The method MUST be defined on the controller class (not standalone)
- Permission checks happen automatically (user must have read access to the document)

---

## Submittable Documents

Documents with `is_submittable = 1` follow the docstatus lifecycle:

| docstatus | State | Editable | Transitions |
|---|---|---|---|
| 0 | Draft | Yes | -> 1 (Submit) |
| 1 | Submitted | Only "Allow on Submit" fields | -> 2 (Cancel) |
| 2 | Cancelled | No | None (amend creates new Draft) |

ALWAYS implement both `on_submit` and `on_cancel` as a pair.
ALWAYS reverse in `on_cancel` what `on_submit` created.

---

## Inheritance Patterns

```python
# Standard controller
from frappe.model.document import Document
class MyDoc(Document): pass

# Tree DocType (hierarchical)
from frappe.utils.nestedset import NestedSet
class Department(NestedSet):
    nsm_parent_field = "parent_department"

# Virtual DocType (no database table)
class ExternalData(Document):
    def load_from_db(self): ...
    def db_insert(self, *args, **kwargs): ...
    def db_update(self, *args, **kwargs): ...
    @staticmethod
    def get_list(args): ...
    @staticmethod
    def get_count(args): ...
```

---

## Type Annotations [v15+]

```python
class Person(Document):
    if TYPE_CHECKING:
        from frappe.types import DF
        first_name: DF.Data
        last_name: DF.Data
        birth_date: DF.Date
        company: DF.Link
```

Enable auto-generation in `hooks.py`: `export_python_type_annotations = True`

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---|---|---|---|
| Type annotations | No | Auto-generated | Yes |
| `before_discard` / `on_discard` | No | Yes | Yes |
| `flags.notify_update` | No | Yes | Yes |
| `extend_doctype_class` | No | No | **Yes** |
| UUID autoname | No | No | **Yes** |
| Old-style format naming | Yes | Yes | Deprecated |

---

## Reference Files

| File | Contents |
|---|---|
| [lifecycle-methods.md](references/lifecycle-methods.md) | All hooks with execution order diagrams |
| [document-api-complete.md](references/document-api-complete.md) | **Complete Document API**: all methods by category (CRUD, fields, DB, permissions, flags, child tables, naming) |
| [methods.md](references/methods.md) | Document class method signatures |
| [events.md](references/events.md) | All document events in order |
| [examples.md](references/examples.md) | Complete working controller examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes and corrections |
| [flags.md](references/flags.md) | Flags system (doc.flags, frappe.flags) |
| [hooks.md](references/hooks.md) | Controller interaction with hooks.py |
| [patterns.md](references/patterns.md) | Common controller patterns |
| [syntax.md](references/syntax.md) | Controller class syntax reference |

## Related Skills

- `frappe-syntax-serverscripts` -- Server Scripts (sandbox alternative)
- `frappe-syntax-hooks` -- hooks.py configuration
- `frappe-impl-controllers` -- Implementation workflows
- `frappe-core-permissions` -- Permission system
