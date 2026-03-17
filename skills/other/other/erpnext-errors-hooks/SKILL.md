---
name: erpnext-errors-hooks
description: "Error handling patterns for ERPNext hooks.py configurations. Use when debugging doc_events errors, scheduler failures, boot session issues, and app initialization problems. V14/V15/V16 compatible. Triggers: hooks.py error, doc_events error, scheduler error, boot session error, app initialization error."
---

# ERPNext Hooks - Error Handling

This skill covers error handling patterns for hooks.py configurations. For syntax, see `erpnext-syntax-hooks`. For implementation workflows, see `erpnext-impl-hooks`.

**Version**: v14/v15/v16 compatible

---

## Hooks Error Handling Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ HOOKS HAVE UNIQUE ERROR HANDLING CHARACTERISTICS                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ✅ Full Python power (try/except, raise)                            │
│ ⚠️ Multiple handlers in chain - one failure affects others         │
│ ⚠️ Some hooks are silent (scheduler, permission_query)             │
│ ⚠️ Transaction behavior varies by hook type                        │
│                                                                     │
│ Key differences from controllers:                                   │
│ • doc_events runs AFTER controller methods                          │
│ • Multiple apps can register handlers (order matters!)              │
│ • Scheduler has NO user feedback - logging is critical              │
│ • Permission hooks should NEVER throw errors                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Main Decision: Error Handling by Hook Type

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHICH HOOK TYPE ARE YOU USING?                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► doc_events (validate, on_update, on_submit, etc.)                     │
│   └─► Same as controllers: frappe.throw() rolls back in validate        │
│   └─► Multiple handlers: first error stops chain                        │
│   └─► Isolate non-critical operations in try/except                     │
│                                                                         │
│ ► scheduler_events (daily, hourly, cron)                                │
│   └─► NO user feedback - frappe.log_error() is essential                │
│   └─► ALWAYS use try/except around operations                           │
│   └─► MUST call frappe.db.commit() manually                             │
│                                                                         │
│ ► permission_query_conditions                                           │
│   └─► NEVER throw errors - return empty string on error                 │
│   └─► Silent failures break list views                                  │
│   └─► Log errors but return safe fallback                               │
│                                                                         │
│ ► has_permission                                                        │
│   └─► NEVER throw errors - return False on error                        │
│   └─► Return None to defer to default permission                        │
│                                                                         │
│ ► override_doctype_class / extend_doctype_class                         │
│   └─► ALWAYS call super() in try/except                                 │
│   └─► Parent errors should usually propagate                            │
│                                                                         │
│ ► extend_bootinfo                                                       │
│   └─► Errors break page load entirely!                                  │
│   └─► ALWAYS wrap in try/except with fallback                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## doc_events Error Handling

### Transaction Behavior (Same as Controllers)

| Event | frappe.throw() Effect |
|-------|----------------------|
| `validate` | ✅ Full rollback - document NOT saved |
| `before_save` | ✅ Full rollback - document NOT saved |
| `on_update` | ⚠️ Document IS saved, error shown |
| `after_insert` | ⚠️ Document IS saved, error shown |
| `on_submit` | ⚠️ docstatus=1, error shown |
| `on_cancel` | ⚠️ docstatus=2, error shown |

### Multiple Handler Chain

```python
# hooks.py - Multiple apps can register handlers
# App A
doc_events = {
    "Sales Invoice": {
        "validate": "app_a.events.validate_si"  # Runs first
    }
}

# App B  
doc_events = {
    "Sales Invoice": {
        "validate": "app_b.events.validate_si"  # Runs second
    }
}

# If App A throws error, App B's handler NEVER runs!
```

### Pattern: Validate Handler

```python
# myapp/events/sales_invoice.py
import frappe
from frappe import _

def validate(doc, method=None):
    """Validate handler with proper error handling."""
    errors = []
    
    # Collect validation errors
    if doc.grand_total < 0:
        errors.append(_("Total cannot be negative"))
    
    if doc.custom_field and not doc.customer:
        errors.append(_("Customer required when custom field is set"))
    
    # Throw all at once
    if errors:
        frappe.throw("<br>".join(errors))
```

### Pattern: on_update Handler (Isolated Operations)

```python
def on_update(doc, method=None):
    """Post-save handler with isolated operations."""
    # Critical operation - let errors propagate
    update_linked_records(doc)
    
    # Non-critical operations - isolate errors
    try:
        send_notification(doc)
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Notification failed for {doc.name}"
        )
    
    try:
        sync_to_external(doc)
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"External sync failed for {doc.name}"
        )
```

---

## scheduler_events Error Handling

### Critical: No User Feedback!

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  SCHEDULER TASKS HAVE NO USER - LOGGING IS ESSENTIAL             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ • No one sees frappe.throw() - task just fails silently             │
│ • No automatic email on failure (unless configured)                 │
│ • frappe.log_error() is your ONLY debugging tool                    │
│ • Always commit changes manually                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Pattern: Scheduler Task with Error Handling

```python
# myapp/tasks.py
import frappe

def daily_sync():
    """Daily sync task with comprehensive error handling."""
    results = {
        "processed": 0,
        "errors": []
    }
    
    try:
        # Get records to process (ALWAYS with limit!)
        records = frappe.get_all(
            "Sales Invoice",
            filters={"sync_status": "Pending"},
            limit=500
        )
        
        for record in records:
            try:
                process_record(record.name)
                results["processed"] += 1
            except Exception as e:
                results["errors"].append(f"{record.name}: {str(e)}")
                frappe.log_error(
                    frappe.get_traceback(),
                    f"Sync error: {record.name}"
                )
        
        # REQUIRED: Commit changes
        frappe.db.commit()
        
    except Exception as e:
        # Log fatal errors
        frappe.log_error(
            frappe.get_traceback(),
            "Daily Sync Fatal Error"
        )
        return
    
    # Log summary
    if results["errors"]:
        summary = f"Processed: {results['processed']}, Errors: {len(results['errors'])}"
        frappe.log_error(
            summary + "\n\n" + "\n".join(results["errors"][:50]),
            "Daily Sync Summary"
        )
```

### Pattern: Scheduler with Batch Commits

```python
def process_large_dataset():
    """Process large dataset with periodic commits."""
    BATCH_SIZE = 100
    
    try:
        records = frappe.get_all("Item", limit=5000)
        total = len(records)
        
        for i in range(0, total, BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            
            for record in batch:
                try:
                    update_item(record.name)
                except Exception:
                    frappe.log_error(
                        frappe.get_traceback(),
                        f"Item update error: {record.name}"
                    )
            
            # Commit after each batch
            frappe.db.commit()
            
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Batch Processing Error")
```

---

## Permission Hooks Error Handling

### permission_query_conditions - NEVER Throw!

```python
# ❌ WRONG - Breaks list view entirely!
def query_conditions(user):
    if not user:
        frappe.throw("User required")  # DON'T DO THIS!
    return f"owner = '{user}'"

# ✅ CORRECT - Return safe fallback
def query_conditions(user):
    """Permission query with error handling."""
    try:
        if not user:
            user = frappe.session.user
        
        if "System Manager" in frappe.get_roles(user):
            return ""  # No restrictions
        
        return f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"
        
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Permission Query Error"
        )
        # Safe fallback - restrict to own records
        return f"`tabSales Invoice`.owner = {frappe.db.escape(frappe.session.user)}"
```

### has_permission - NEVER Throw!

```python
# ❌ WRONG - Breaks document access!
def has_permission(doc, user=None, permission_type=None):
    if doc.status == "Locked":
        frappe.throw("Document is locked")  # DON'T DO THIS!

# ✅ CORRECT - Return boolean or None
def has_permission(doc, user=None, permission_type=None):
    """Document permission check with error handling."""
    try:
        user = user or frappe.session.user
        
        # Deny access to locked documents
        if doc.status == "Locked" and permission_type == "write":
            return False
        
        # Custom logic
        if permission_type == "delete":
            if doc.has_linked_records():
                return False
        
        # Return None to defer to default permission system
        return None
        
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Permission check error: {doc.name}"
        )
        # Safe fallback - defer to default
        return None
```

---

## Override Hooks Error Handling

### override_doctype_class

```python
# myapp/overrides.py
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
import frappe
from frappe import _

class CustomSalesOrder(SalesOrder):
    def validate(self):
        """Override with proper error handling."""
        # ALWAYS call parent first in try/except
        try:
            super().validate()
        except frappe.ValidationError:
            # Re-raise validation errors
            raise
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Parent Validate Error")
            raise
        
        # Custom validation
        self.custom_validate()
    
    def custom_validate(self):
        if self.custom_approval_required and not self.custom_approved:
            frappe.throw(_("Approval required before saving"))
```

### extend_doctype_class (V16+)

```python
# myapp/extends.py
import frappe
from frappe import _

class SalesOrderExtend:
    """Extension class - only add new methods."""
    
    def custom_approval_check(self):
        """New method with error handling."""
        try:
            if not self.custom_approver:
                frappe.throw(_("Approver not set"))
            
            approver = frappe.get_doc("User", self.custom_approver)
            if not approver.enabled:
                frappe.throw(_("Approver is disabled"))
                
        except frappe.DoesNotExistError:
            frappe.throw(_("Approver not found"))
```

---

## extend_bootinfo Error Handling

### Critical: Errors Break Page Load!

```python
# ❌ WRONG - Unhandled error breaks desk entirely!
def extend_boot(bootinfo):
    settings = frappe.get_single("My Settings")  # What if it doesn't exist?
    bootinfo.my_config = settings.config

# ✅ CORRECT - Always handle errors
def extend_boot(bootinfo):
    """Extend bootinfo with error handling."""
    try:
        if frappe.db.exists("My Settings", "My Settings"):
            settings = frappe.get_single("My Settings")
            bootinfo.my_config = settings.config or {}
        else:
            bootinfo.my_config = {}
            
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Bootinfo Extension Error"
        )
        # Safe fallback
        bootinfo.my_config = {}
```

---

## Critical Rules

### ✅ ALWAYS

1. **Use try/except in scheduler tasks** - No user feedback otherwise
2. **Call frappe.db.commit() in scheduler** - Changes aren't auto-saved
3. **Return safe fallbacks in permission hooks** - Never throw
4. **Call super() in override classes** - Preserve parent behavior
5. **Log errors with context** - Include document name, operation
6. **Wrap extend_bootinfo in try/except** - Errors break page load

### ❌ NEVER

1. **Don't throw in permission_query_conditions** - Breaks list views
2. **Don't throw in has_permission** - Breaks document access
3. **Don't assume single handler** - Multiple apps can register
4. **Don't commit in doc_events** - Framework handles transactions
5. **Don't ignore scheduler errors** - They fail silently

---

## Quick Reference: Error Handling by Hook

| Hook Type | Can Throw? | Commit? | Key Pattern |
|-----------|:----------:|:-------:|-------------|
| doc_events (validate) | ✅ YES | ❌ NO | Collect errors, throw once |
| doc_events (on_update) | ⚠️ Careful | ❌ NO | Isolate non-critical ops |
| scheduler_events | ❌ Pointless | ✅ YES | Try/except + log_error |
| permission_query_conditions | ❌ NEVER | ❌ NO | Return "" on error |
| has_permission | ❌ NEVER | ❌ NO | Return None on error |
| extend_bootinfo | ❌ NEVER | ❌ NO | Try/except + fallback |
| override class | ✅ YES | ❌ NO | super() + re-raise |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns |
| `references/examples.md` | Full working examples |
| `references/anti-patterns.md` | Common mistakes to avoid |

---

## See Also

- `erpnext-syntax-hooks` - Hooks syntax
- `erpnext-impl-hooks` - Implementation workflows
- `erpnext-errors-controllers` - Controller error handling
- `erpnext-errors-serverscripts` - Server Script error handling
