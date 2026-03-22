---
name: frappe-syntax-hooks-events
description: >
  Use when implementing document lifecycle hooks via doc_events in hooks.py, understanding event execution order, or extending/overriding document behavior from another app.
  Prevents silent hook failures from wrong event names, incorrect execution order assumptions, and broken override chains.
  Covers doc_events hook syntax, all document events (before_insert, validate, on_submit, etc.), event execution order, extend vs override behavior, cross-app doc_events.
  Keywords: doc_events, hooks.py, before_insert, validate, on_submit, on_cancel, lifecycle, document events, override, extend.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Document Lifecycle Hooks (doc_events)

## Quick Reference — Event Execution Order

### Insert (new document)

| Order | Event               | Purpose                              | Can Raise? |
|-------|---------------------|--------------------------------------|------------|
| 1     | `before_insert`     | Set defaults before naming           | YES        |
| 2     | `before_naming`     | Modify naming logic                  | YES        |
| 3     | `autoname`          | Set the `name` property              | YES        |
| 4     | `before_validate`   | Auto-set missing values              | YES        |
| 5     | `validate`          | Validation logic — throw to abort    | YES        |
| 6     | `before_save`       | Final mutations before DB write      | YES        |
| 7     | `db_insert`         | *Internal* — writes row to DB        | —          |
| 8     | `after_insert`      | Post-insert logic (runs once ever)   | YES        |
| 9     | `on_update`         | Post-save logic (runs on every save) | YES        |
| 10    | `on_change`         | Fires if any field value changed     | YES        |

### Save (existing document)

| Order | Event             | Purpose                           |
|-------|-------------------|-----------------------------------|
| 1     | `before_validate` | Auto-set missing values           |
| 2     | `validate`        | Validation logic — throw to abort |
| 3     | `before_save`     | Final mutations before DB write   |
| 4     | `db_update`       | *Internal* — updates row in DB    |
| 5     | `on_update`       | Post-save logic                   |
| 6     | `on_change`       | Fires if any field value changed  |

### Submit

| Order | Event             | Purpose                            |
|-------|-------------------|------------------------------------|
| 1     | `before_validate` | Auto-set missing values            |
| 2     | `validate`        | Validation logic                   |
| 3     | `before_save`     | Final mutations before DB write    |
| 4     | `before_submit`   | Pre-submit logic — throw to abort  |
| 5     | `db_update`       | *Internal* — updates row in DB     |
| 6     | `on_submit`       | Post-submit logic (GL entries etc) |
| 7     | `on_update`       | Post-save logic                    |
| 8     | `on_change`       | Fires if any field value changed   |

### Cancel

| Order | Event             | Purpose                             |
|-------|-------------------|-------------------------------------|
| 1     | `before_cancel`   | Pre-cancel validation               |
| 2     | `db_update`       | *Internal* — updates row in DB      |
| 3     | `on_cancel`       | Post-cancel logic (reverse GL etc)  |
| 4     | `on_change`       | Fires if any field value changed    |

### Delete

| Order | Event          | Purpose                        |
|-------|----------------|--------------------------------|
| 1     | `on_trash`     | Pre-delete cleanup             |
| 2     | `after_delete` | Post-delete logic              |

### Other Operations

| Operation              | Events (in order)                                        |
|------------------------|----------------------------------------------------------|
| Rename                 | `before_rename` → `after_rename`                         |
| Amend                  | `before_insert` chain runs on the new amended doc        |
| Update After Submit    | `before_update_after_submit` → `db_update` → `on_update_after_submit` → `on_change` |

---

## doc_events in hooks.py — Syntax

### Basic Structure

```python
# hooks.py
doc_events = {
    "Sales Invoice": {
        "on_submit": "myapp.events.sales_invoice.on_submit",
        "on_cancel": "myapp.events.sales_invoice.on_cancel",
    },
    "Purchase Order": {
        "validate": "myapp.events.purchase_order.validate",
    }
}
```

### Wildcard — Apply to ALL DocTypes

```python
doc_events = {
    "*": {
        "after_insert": "myapp.events.global_handler.after_insert_all",
        "on_update": "myapp.events.global_handler.track_changes",
    }
}
```

ALWAYS use `"*"` (string with asterisk) as the key. This fires the handler for every DocType.

### Multiple Handlers per Event

```python
doc_events = {
    "Sales Invoice": {
        "on_submit": [
            "myapp.events.accounting.create_gl_entries",
            "myapp.events.notifications.send_invoice_email",
        ]
    }
}
```

### Handler Function Signature

```python
# myapp/events/sales_invoice.py
def on_submit(doc, method=None):
    """
    doc    — the Document instance (e.g., Sales Invoice)
    method — string name of the event (e.g., "on_submit"), or None
    """
    if doc.grand_total > 10000:
        frappe.sendmail(...)
```

ALWAYS accept `method` as the second parameter (with default `None`). Frappe passes it automatically.

---

## Decision Tree — Which Event to Use

### "I need to validate data before saving"
→ Use `validate`. ALWAYS raise `frappe.throw()` here to block invalid saves.

### "I need to set default values automatically"
→ Use `before_validate`. This runs before `validate`, so your defaults are set before validation checks.

### "I need to run logic only on first creation"
→ Use `after_insert`. This fires ONLY on insert, NEVER on subsequent saves.

### "I need to run logic on every save (insert + update)"
→ Use `on_update`. This fires on both insert and save operations.

### "I need to create linked documents after submit"
→ Use `on_submit`. NEVER create linked docs in `validate` — the document is not yet committed.

### "I need to reverse linked documents on cancel"
→ Use `on_cancel`. ALWAYS clean up GL entries, stock ledger entries, and linked docs here.

### "I need to modify the document name"
→ Use `autoname` in the controller, or `before_naming` for conditional logic.

### "I need to prevent deletion under certain conditions"
→ Use `on_trash`. Raise `frappe.throw()` to block deletion.

### "I need to update a submitted document's fields"
→ Use `before_update_after_submit` for validation and `on_update_after_submit` for side effects.

### "I need logic that runs only when values actually changed"
→ Use `on_change`. This fires only when at least one field value differs from the DB state.

---

## doc_events vs Controller Events

Both mechanisms trigger the SAME events. The difference is WHERE you register them.

| Aspect              | Controller (class method)            | doc_events (hooks.py)                    |
|---------------------|--------------------------------------|------------------------------------------|
| **Location**        | `{doctype}.py` controller file       | `hooks.py` in your app                   |
| **Use when**        | You OWN the DocType                  | You are EXTENDING another app's DocType  |
| **Execution**       | Runs first (controller)              | Runs after controller method             |
| **Multiple apps**   | Only one controller per DocType      | Multiple apps can register handlers      |

ALWAYS use `doc_events` when hooking into a DocType you do NOT own. NEVER modify another app's controller file directly.

### Execution Order Within a Single Event

For a given event (e.g., `validate`):
1. Controller method runs first (`def validate(self)`)
2. `doc_events` handlers run in app installation order
3. Wildcard `"*"` handlers run after specific DocType handlers

---

## extend_doctype_class [v16+]

In Frappe v16+, `extend_doctype_class` provides a cleaner alternative to `doc_events` for adding methods to existing DocTypes.

### hooks.py

```python
extend_doctype_class = {
    "Sales Invoice": [
        "myapp.overrides.sales_invoice.SalesInvoiceExtension"
    ]
}
```

### Extension Class (Mixin)

```python
# myapp/overrides/sales_invoice.py
import frappe

class SalesInvoiceExtension:
    def validate(self):
        """This is called as part of the controller chain."""
        if self.grand_total < 0:
            frappe.throw("Grand total cannot be negative")

    def custom_method(self):
        """Custom methods are also available on the doc instance."""
        return self.items
```

### Key Rules

- ALWAYS use `extend_doctype_class` over `override_doctype_class` in v16+ when multiple apps may extend the same DocType.
- Multiple apps can extend the same DocType — extensions stack via MRO.
- Class resolution order follows hooks priority: `class Final(App2Mixin, App1Mixin, Original)`.
- Extension methods (like `validate`) run as part of the controller, NOT as separate doc_events handlers.

---

## override_doctype_class [v14+]

Completely replaces the controller class. Use with extreme caution.

```python
# hooks.py
override_doctype_class = {
    "ToDo": "myapp.overrides.todo.CustomToDo"
}
```

```python
# myapp/overrides/todo.py
from frappe.desk.doctype.todo.todo import ToDo

class CustomToDo(ToDo):
    def validate(self):
        super().validate()  # ALWAYS call super() to preserve original logic
        # Your additions here
```

NEVER use `override_doctype_class` if `extend_doctype_class` is available (v16+). Only ONE app can override a DocType — last-installed app wins, silently breaking other apps.

---

## Multi-App Event Ordering

When multiple apps register `doc_events` for the same DocType and event:

1. Handlers execute in **app installation order** (as listed in `sites/{site}/site_config.json` → `installed_apps`).
2. The order can be changed via **Setup > Installed Applications > Update Hooks Resolution Order**.
3. For `override_doctype_class`, the **last-installed app wins** (only one override applies).
4. For `extend_doctype_class` (v16+), all extensions stack cumulatively.

---

## Transaction Behavior

All document events from `before_validate` through `on_change` run inside a single database transaction.

- If ANY event raises an exception, the ENTIRE operation rolls back (including `db_insert`/`db_update`).
- `after_insert`, `on_update`, `on_submit`, `on_cancel` — all run BEFORE the transaction commits.
- The transaction commits only AFTER all events complete successfully.
- `after_delete` runs after the DELETE statement but still within the request transaction.

NEVER assume data is committed to DB inside any event handler. Other concurrent requests will NOT see your changes until the full request completes.

---

## Critical Rules

1. ALWAYS use `frappe.throw()` to abort operations — NEVER use `raise Exception`.
2. NEVER modify `doc.name` outside of `autoname` or `before_naming`.
3. ALWAYS call `super().{event}()` when overriding controller methods in subclasses.
4. NEVER use `doc.save()` inside `validate` or `before_save` — this causes infinite recursion.
5. ALWAYS use `doc.flags.ignore_permissions = True` explicitly if your hook needs to bypass permissions — NEVER assume hooks run as Administrator.
6. NEVER put slow operations (API calls, file I/O) in `validate` — use `after_insert` or `on_update` with `frappe.enqueue()` instead.
7. ALWAYS use `doc.flags` to communicate between events in the same request (e.g., `doc.flags.skip_notification = True`).
8. NEVER rely on `on_change` for critical logic — it only fires when values actually differ from the database state.

---

## See Also

- [Event Execution Order — Detailed Diagrams](references/event-order.md)
- [Working Examples for Common Patterns](references/examples.md)
- [Anti-Patterns and Common Mistakes](references/anti-patterns.md)
- `frappe-syntax-hooks-config` — App-level hooks (scheduler, fixtures, permissions)
- Official docs: https://docs.frappe.io/framework/user/en/basics/doctypes/controllers
