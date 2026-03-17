---
name: erpnext-errors-controllers
description: "Error handling patterns for ERPNext Document Controllers. Use when implementing try/except, validation errors, permission errors, and transaction management. Covers rollback patterns, error logging, and user feedback. V14/V15/V16 compatible. Triggers: controller error, try except catch, ValidationError, PermissionError, rollback, error handling."
---

# ERPNext Controllers - Error Handling

This skill covers error handling patterns for Document Controllers. For syntax, see `erpnext-syntax-controllers`. For implementation workflows, see `erpnext-impl-controllers`.

**Version**: v14/v15/v16 compatible

---

## Controllers vs Server Scripts: Error Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│ CONTROLLERS HAVE FULL PYTHON POWER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ✅ try/except blocks - Full exception handling                      │
│ ✅ raise statements - Custom exceptions                             │
│ ✅ Multiple except clauses - Handle specific errors                 │
│ ✅ finally blocks - Cleanup operations                              │
│ ✅ frappe.throw() - Stop with user message                          │
│ ✅ frappe.log_error() - Silent error logging                        │
│                                                                     │
│ ⚠️ Transaction behavior varies by hook:                            │
│    • validate: throw rolls back entire save                         │
│    • on_update: document already saved!                             │
│    • on_submit: partial rollback possible                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Main Decision: Error Handling by Hook

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHICH LIFECYCLE HOOK ARE YOU IN?                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► validate / before_save                                                │
│   └─► frappe.throw() → Rolls back, document NOT saved                   │
│   └─► try/except → Catch and re-throw or handle gracefully              │
│                                                                         │
│ ► on_update / after_insert                                              │
│   └─► Document already saved! frappe.throw() shows error but saved      │
│   └─► Use try/except + log_error for non-critical operations            │
│   └─► Critical failures: frappe.throw() (shows error, doc is saved)     │
│                                                                         │
│ ► before_submit                                                         │
│   └─► frappe.throw() → Prevents submit, stays draft                     │
│   └─► Last chance for validation before docstatus=1                     │
│                                                                         │
│ ► on_submit                                                             │
│   └─► Document is submitted! throw shows error but docstatus=1          │
│   └─► Critical: throw causes partial state (submitted but failed)       │
│   └─► Better: validate everything in before_submit                      │
│                                                                         │
│ ► on_cancel                                                             │
│   └─► Reverse operations - use try/except for each reversal             │
│   └─► Log errors but try to continue cleanup                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Error Methods Reference

### Quick Reference

| Method | Stops Execution? | Rolls Back? | User Sees? | Use For |
|--------|:----------------:|:-----------:|:----------:|---------|
| `frappe.throw()` | ✅ YES | Depends on hook | Dialog | Validation errors |
| `raise Exception` | ✅ YES | Depends on hook | Error page | Internal errors |
| `frappe.msgprint()` | ❌ NO | ❌ NO | Dialog | Warnings |
| `frappe.log_error()` | ❌ NO | ❌ NO | Error Log | Debug/audit |

### Transaction Rollback by Hook

| Hook | frappe.throw() Effect |
|------|----------------------|
| `validate` | ✅ Full rollback - document NOT saved |
| `before_save` | ✅ Full rollback - document NOT saved |
| `on_update` | ⚠️ Document IS saved, error shown |
| `after_insert` | ⚠️ Document IS saved, error shown |
| `before_submit` | ✅ Full rollback - stays Draft |
| `on_submit` | ⚠️ docstatus=1, error shown |
| `before_cancel` | ✅ Full rollback - stays Submitted |
| `on_cancel` | ⚠️ docstatus=2, error shown |

---

## Error Handling Patterns

### Pattern 1: Validation with Error Collection

```python
def validate(self):
    """Collect all errors before throwing."""
    errors = []
    
    # Required fields
    if not self.customer:
        errors.append(_("Customer is required"))
    
    if not self.items:
        errors.append(_("At least one item is required"))
    
    # Business rules
    if self.discount_percent > 50:
        errors.append(_("Discount cannot exceed 50%"))
    
    # Child table validation
    for idx, item in enumerate(self.items, 1):
        if not item.item_code:
            errors.append(_("Row {0}: Item Code is required").format(idx))
        if (item.qty or 0) <= 0:
            errors.append(_("Row {0}: Quantity must be positive").format(idx))
    
    # Throw all errors at once
    if errors:
        frappe.throw("<br>".join(errors), title=_("Validation Error"))
```

### Pattern 2: External API Call with Fallback

```python
def validate(self):
    """Call external API with error handling."""
    if self.requires_credit_check:
        try:
            result = self.check_credit_external()
            self.credit_score = result.get("score", 0)
        except requests.Timeout:
            # Timeout - use cached value
            frappe.msgprint(
                _("Credit check timed out. Using cached value."),
                indicator="orange"
            )
            self.credit_score = self.get_cached_credit_score()
        except requests.RequestException as e:
            # API error - log and continue with warning
            frappe.log_error(
                f"Credit check failed: {str(e)}",
                "External API Error"
            )
            frappe.msgprint(
                _("Credit check unavailable. Please verify manually."),
                indicator="orange"
            )
            self.credit_check_pending = 1
        except Exception as e:
            # Unexpected error - log and re-raise
            frappe.log_error(frappe.get_traceback(), "Credit Check Error")
            frappe.throw(_("Credit check failed. Please try again."))
```

### Pattern 3: Safe Post-Save Operations

```python
def on_update(self):
    """Handle post-save operations safely."""
    # Critical operation - throw on failure
    self.update_linked_documents()
    
    # Non-critical operations - log errors, don't throw
    try:
        self.send_notification()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Notification failed for {self.name}"
        )
    
    try:
        self.sync_to_external_system()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"External sync failed for {self.name}"
        )
        # Queue for retry
        frappe.enqueue(
            "myapp.tasks.retry_sync",
            doctype=self.doctype,
            name=self.name,
            queue="short"
        )
```

### Pattern 4: Submittable Document Error Handling

```python
def before_submit(self):
    """All validations that must pass before submit."""
    # Validate everything here - last chance to abort cleanly
    if not self.items:
        frappe.throw(_("Cannot submit without items"))
    
    if self.grand_total <= 0:
        frappe.throw(_("Total must be greater than zero"))
    
    # Check stock availability
    for item in self.items:
        available = get_stock_balance(item.item_code, item.warehouse)
        if available < item.qty:
            frappe.throw(
                _("Row {0}: Insufficient stock for {1}. Available: {2}").format(
                    item.idx, item.item_code, available
                )
            )

def on_submit(self):
    """Post-submit actions - document is already submitted!"""
    # These operations should not fail if before_submit passed
    try:
        self.create_stock_ledger_entries()
    except Exception as e:
        # CRITICAL: Document is submitted but entries failed!
        frappe.log_error(frappe.get_traceback(), "Stock Ledger Error")
        frappe.throw(
            _("Stock entries failed. Please cancel and retry. Error: {0}").format(str(e))
        )
    
    try:
        self.create_gl_entries()
    except Exception as e:
        # Rollback stock entries if GL fails
        self.reverse_stock_ledger_entries()
        frappe.log_error(frappe.get_traceback(), "GL Entry Error")
        frappe.throw(_("Accounting entries failed. Stock entries reversed."))
```

### Pattern 5: Cancel with Cleanup

```python
def before_cancel(self):
    """Validate cancel is allowed."""
    # Check for linked documents
    linked_invoices = frappe.get_all(
        "Sales Invoice Item",
        filters={"sales_order": self.name, "docstatus": 1},
        pluck="parent"
    )
    
    if linked_invoices:
        frappe.throw(
            _("Cannot cancel. Linked invoices exist: {0}").format(
                ", ".join(linked_invoices)
            )
        )

def on_cancel(self):
    """Reverse operations - try to complete all cleanup."""
    errors = []
    
    # Reverse stock
    try:
        self.reverse_stock_ledger_entries()
    except Exception as e:
        errors.append(f"Stock reversal: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Stock Reversal Error")
    
    # Reverse GL
    try:
        self.reverse_gl_entries()
    except Exception as e:
        errors.append(f"GL reversal: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "GL Reversal Error")
    
    # Update linked docs
    try:
        self.update_linked_on_cancel()
    except Exception as e:
        errors.append(f"Linked docs: {str(e)}")
        frappe.log_error(frappe.get_traceback(), "Linked Doc Update Error")
    
    # Report any errors but don't prevent cancel
    if errors:
        frappe.msgprint(
            _("Cancel completed with errors:<br>{0}").format("<br>".join(errors)),
            title=_("Warning"),
            indicator="orange"
        )
```

### Pattern 6: Database Operation Error Handling

```python
def validate(self):
    """Handle database errors gracefully."""
    try:
        # Check for duplicates
        existing = frappe.db.exists(
            "Customer Contract",
            {"customer": self.customer, "status": "Active", "name": ["!=", self.name]}
        )
        if existing:
            frappe.throw(_("Active contract already exists for this customer"))
            
    except frappe.db.InternalError as e:
        # Database error - log and show user-friendly message
        frappe.log_error(frappe.get_traceback(), "Database Error")
        frappe.throw(_("Database error. Please try again or contact support."))
```

> **See**: `references/patterns.md` for more error handling patterns.

---

## Transaction Management

### Understanding Transactions

```python
# Frappe wraps each request in a transaction
# - On success: auto-commit
# - On exception: auto-rollback

def validate(self):
    # All these changes are in ONE transaction
    self.calculate_totals()
    frappe.db.set_value("Counter", "main", "count", 100)
    
    if error_condition:
        frappe.throw("Error")  # EVERYTHING rolls back

def on_update(self):
    # Document save is already committed!
    # New changes here are in a NEW transaction
    frappe.db.set_value("Other", "doc", "field", "value")
    
    if error_condition:
        frappe.throw("Error")  # Only on_update changes roll back
        # The document itself is already saved!
```

### Manual Savepoints (Advanced)

```python
def on_submit(self):
    """Use savepoints for partial rollback."""
    # Create savepoint before risky operation
    frappe.db.savepoint("before_stock")
    
    try:
        self.create_stock_entries()
    except Exception:
        # Rollback only stock entries
        frappe.db.rollback(save_point="before_stock")
        frappe.log_error(frappe.get_traceback(), "Stock Entry Error")
        frappe.throw(_("Stock entries failed"))
    
    frappe.db.savepoint("before_gl")
    
    try:
        self.create_gl_entries()
    except Exception:
        frappe.db.rollback(save_point="before_gl")
        frappe.log_error(frappe.get_traceback(), "GL Entry Error")
        frappe.throw(_("GL entries failed"))
```

---

## Critical Rules

### ✅ ALWAYS

1. **Collect multiple validation errors** - Better UX than one at a time
2. **Use try/except around external calls** - APIs, file I/O, network
3. **Log unexpected errors** - `frappe.log_error(frappe.get_traceback())`
4. **Call super() in overridden methods** - Preserve parent behavior
5. **Validate in before_submit** - Last clean abort point for submittables
6. **Use _() for error messages** - Enable translation

### ❌ NEVER

1. **Don't call frappe.db.commit()** - Framework handles transactions
2. **Don't swallow errors silently** - Always log unexpected exceptions
3. **Don't assume on_update can rollback doc** - It's already saved
4. **Don't put critical logic in on_submit** - Validate in before_submit
5. **Don't ignore return values** - Check for None/empty results

---

## Quick Reference: Exception Handling

```python
# Catch specific exceptions first, general last
try:
    result = risky_operation()
except frappe.ValidationError:
    # Re-raise validation errors
    raise
except frappe.DoesNotExistError:
    # Handle missing document
    frappe.throw(_("Referenced document not found"))
except requests.Timeout:
    # Handle timeout specifically
    frappe.msgprint(_("Operation timed out"), indicator="orange")
except Exception as e:
    # Log and handle unexpected errors
    frappe.log_error(frappe.get_traceback(), "Unexpected Error")
    frappe.throw(_("An error occurred: {0}").format(str(e)))
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns |
| `references/examples.md` | Full working examples |
| `references/anti-patterns.md` | Common mistakes to avoid |

---

## See Also

- `erpnext-syntax-controllers` - Controller syntax
- `erpnext-impl-controllers` - Implementation workflows
- `erpnext-errors-serverscripts` - Server Script error handling (sandbox)
- `erpnext-errors-hooks` - Hook error handling
