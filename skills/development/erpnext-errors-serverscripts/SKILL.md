---
name: erpnext-errors-serverscripts
description: "Error handling patterns for ERPNext Server Scripts. Use when handling sandbox errors, frappe.throw usage, validation in server scripts, and debugging. V14/V15/V16 compatible. Triggers: server script error, frappe.throw, sandbox error, validation error, debugging server script."
---

# ERPNext Server Scripts - Error Handling

This skill covers error handling patterns for Server Scripts. For syntax, see `erpnext-syntax-serverscripts`. For implementation workflows, see `erpnext-impl-serverscripts`.

**Version**: v14/v15/v16 compatible

---

## CRITICAL: Sandbox Limitations for Error Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  SANDBOX RESTRICTIONS AFFECT ERROR HANDLING                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ❌ NO try/except blocks (blocked in RestrictedPython)               │
│ ❌ NO raise statements (use frappe.throw instead)                   │
│ ❌ NO import traceback                                              │
│                                                                     │
│ ✅ frappe.throw() - Stop execution, show error                      │
│ ✅ frappe.log_error() - Log to Error Log doctype                    │
│ ✅ frappe.msgprint() - Show message, continue execution             │
│ ✅ Conditional checks before operations                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Main Decision: How to Handle the Error?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT TYPE OF ERROR ARE YOU HANDLING?                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► Validation error (must stop save/submit)?                             │
│   └─► frappe.throw() with clear message                                 │
│                                                                         │
│ ► Warning (inform user, allow continue)?                                │
│   └─► frappe.msgprint() with indicator                                  │
│                                                                         │
│ ► Log error for debugging (no user impact)?                             │
│   └─► frappe.log_error()                                                │
│                                                                         │
│ ► API error response (HTTP error)?                                      │
│   └─► frappe.throw() with exc parameter OR set response                 │
│                                                                         │
│ ► Scheduler task error?                                                 │
│   └─► frappe.log_error() + continue processing other items              │
│                                                                         │
│ ► Prevent operation but not with error dialog?                          │
│   └─► Return early + frappe.msgprint()                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Error Methods Reference

### Quick Reference

| Method | Stops Execution? | User Sees? | Logged? | Use For |
|--------|:----------------:|:----------:|:-------:|---------|
| `frappe.throw()` | ✅ YES | Dialog | Error Log | Validation errors |
| `frappe.msgprint()` | ❌ NO | Dialog | No | Warnings |
| `frappe.log_error()` | ❌ NO | No | Error Log | Debug/audit |
| `frappe.publish_realtime()` | ❌ NO | Toast | No | Background updates |

### frappe.throw() - Stop Execution

```python
# Basic throw - stops execution, rolls back transaction
frappe.throw("Customer is required")

# With title
frappe.throw("Amount cannot be negative", title="Validation Error")

# With exception type (for API scripts)
frappe.throw("Not authorized", exc=frappe.PermissionError)
frappe.throw("Record not found", exc=frappe.DoesNotExistError)

# With formatted message
frappe.throw(
    f"Credit limit exceeded. Limit: {credit_limit}, Requested: {amount}",
    title="Credit Check Failed"
)
```

**Exception Types for API Scripts:**

| Exception | HTTP Code | Use For |
|-----------|:---------:|---------|
| `frappe.ValidationError` | 417 | Validation failures |
| `frappe.PermissionError` | 403 | Access denied |
| `frappe.DoesNotExistError` | 404 | Record not found |
| `frappe.AuthenticationError` | 401 | Not logged in |
| `frappe.OutgoingEmailError` | 500 | Email send failed |

### frappe.log_error() - Silent Logging

```python
# Basic error log
frappe.log_error("Something went wrong", "My Script Error")

# With context data
frappe.log_error(
    f"Failed to process invoice {doc.name}: {error_detail}",
    "Invoice Processing Error"
)

# Log current exception (in controllers, not sandbox)
frappe.log_error(frappe.get_traceback(), "Unexpected Error")
```

### frappe.msgprint() - Warning Without Stopping

```python
# Simple warning
frappe.msgprint("Stock is running low", indicator="orange")

# With title
frappe.msgprint(
    "This customer has pending payments",
    title="Warning",
    indicator="yellow"
)

# Alert style (top of page)
frappe.msgprint(
    "Document will be processed in background",
    alert=True
)
```

---

## Error Handling Patterns by Script Type

### Pattern 1: Document Event - Validation

```python
# Type: Document Event
# Event: Before Save

# Collect all errors, show together
errors = []

if not doc.customer:
    errors.append("Customer is required")

if doc.grand_total <= 0:
    errors.append("Total must be greater than zero")

if not doc.items:
    errors.append("At least one item is required")
else:
    for idx, item in enumerate(doc.items, 1):
        if not item.item_code:
            errors.append(f"Row {idx}: Item Code is required")
        if (item.qty or 0) <= 0:
            errors.append(f"Row {idx}: Quantity must be positive")

# Throw all errors at once
if errors:
    frappe.throw("<br>".join(errors), title="Validation Errors")
```

### Pattern 2: Document Event - Conditional Warning

```python
# Type: Document Event
# Event: Before Save

# Warning: doesn't stop save
credit_limit = frappe.db.get_value("Customer", doc.customer, "credit_limit") or 0

if credit_limit > 0 and doc.grand_total > credit_limit:
    frappe.msgprint(
        f"Order total ({doc.grand_total}) exceeds credit limit ({credit_limit})",
        title="Credit Warning",
        indicator="orange"
    )
```

### Pattern 3: Document Event - Safe Database Lookup

```python
# Type: Document Event
# Event: Before Save

# Always validate before database lookup
if doc.customer:
    customer_data = frappe.db.get_value(
        "Customer", 
        doc.customer, 
        ["credit_limit", "disabled", "territory"],
        as_dict=True
    )
    
    # Check if customer exists
    if not customer_data:
        frappe.throw(f"Customer {doc.customer} not found")
    
    # Check if disabled
    if customer_data.disabled:
        frappe.throw(f"Customer {doc.customer} is disabled")
    
    # Use the data
    doc.territory = customer_data.territory
```

### Pattern 4: API Script - Error Responses

```python
# Type: API
# Method: get_customer_info

customer = frappe.form_dict.get("customer")

# Validate required parameter
if not customer:
    frappe.throw("Parameter 'customer' is required", exc=frappe.ValidationError)

# Check existence
if not frappe.db.exists("Customer", customer):
    frappe.throw(f"Customer '{customer}' not found", exc=frappe.DoesNotExistError)

# Check permission
if not frappe.has_permission("Customer", "read", customer):
    frappe.throw("You don't have permission to view this customer", exc=frappe.PermissionError)

# Success response
frappe.response["message"] = {
    "customer": customer,
    "credit_limit": frappe.db.get_value("Customer", customer, "credit_limit")
}
```

### Pattern 5: Scheduler - Batch Processing with Error Isolation

```python
# Type: Scheduler Event
# Cron: 0 9 * * * (daily at 9:00)

processed = 0
errors = []

invoices = frappe.get_all(
    "Sales Invoice",
    filters={"status": "Unpaid", "docstatus": 1},
    fields=["name", "customer"],
    limit=100  # ALWAYS limit in scheduler
)

for inv in invoices:
    # Isolate errors per item - don't let one failure stop all
    if not frappe.db.exists("Customer", inv.customer):
        errors.append(f"{inv.name}: Customer not found")
        continue
    
    # Safe processing
    result = process_invoice(inv.name)
    if result.get("success"):
        processed += 1
    else:
        errors.append(f"{inv.name}: {result.get('error', 'Unknown error')}")

# Log summary
if errors:
    frappe.log_error(
        f"Processed: {processed}, Errors: {len(errors)}\n\n" + "\n".join(errors),
        "Invoice Processing Summary"
    )

# REQUIRED: commit in scheduler
frappe.db.commit()


def process_invoice(invoice_name):
    """Helper function with error handling"""
    # Validate invoice exists
    if not frappe.db.exists("Sales Invoice", invoice_name):
        return {"success": False, "error": "Invoice not found"}
    
    # Process logic here
    return {"success": True}
```

### Pattern 6: Permission Query - Safe Fallback

```python
# Type: Permission Query
# DocType: Sales Invoice

# Safe role check
user_roles = frappe.get_roles(user) or []

if "System Manager" in user_roles:
    conditions = ""  # Full access
elif "Sales Manager" in user_roles:
    # Manager sees team's invoices
    team = frappe.db.get_value("User", user, "department")
    if team:
        conditions = f"`tabSales Invoice`.department = {frappe.db.escape(team)}"
    else:
        conditions = f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"
elif "Sales User" in user_roles:
    # User sees only own invoices
    conditions = f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"
else:
    # No access - return impossible condition
    conditions = "1=0"
```

> **See**: `references/patterns.md` for more error handling patterns.

---

## Transaction Behavior

### Automatic Rollback on frappe.throw()

```python
# Type: Document Event - Before Save

# All changes roll back if throw is called
doc.status = "Processing"  # This change...
frappe.db.set_value("Counter", "main", "count", 100)  # ...and this...

if some_condition_fails:
    frappe.throw("Validation failed")  # ...are ALL rolled back
```

### Manual Commit in Scheduler

```python
# Type: Scheduler Event

# Changes are NOT auto-committed in scheduler
for item in items:
    frappe.db.set_value("Item", item.name, "last_sync", frappe.utils.now())

# REQUIRED: Explicit commit
frappe.db.commit()
```

### Partial Commit Pattern (Scheduler)

```python
# Type: Scheduler Event
# Process in batches with intermediate commits

BATCH_SIZE = 50
items = frappe.get_all("Item", filters={"sync_pending": 1}, limit=500)

for i in range(0, len(items), BATCH_SIZE):
    batch = items[i:i + BATCH_SIZE]
    
    for item in batch:
        frappe.db.set_value("Item", item.name, "sync_pending", 0)
    
    # Commit after each batch - partial progress saved
    frappe.db.commit()
```

---

## Critical Rules

### ✅ ALWAYS

1. **Validate inputs before database operations** - Check existence before get_doc
2. **Use `frappe.db.escape()` for user input in SQL** - Prevent SQL injection
3. **Add `limit` to queries in Scheduler scripts** - Prevent memory issues
4. **Call `frappe.db.commit()` in Scheduler scripts** - Changes aren't auto-saved
5. **Collect multiple errors before throwing** - Better user experience
6. **Log errors in Scheduler scripts** - No user to see the error

### ❌ NEVER

1. **Don't use try/except in Server Scripts** - Blocked by sandbox
2. **Don't use `raise` statement** - Use `frappe.throw()` instead
3. **Don't call `doc.save()` in Before Save event** - Framework handles it
4. **Don't assume database values exist** - Always check first
5. **Don't ignore empty results** - Handle gracefully

---

## Quick Reference: Error Message Quality

```python
# ❌ BAD - Technical, not actionable
frappe.throw("KeyError: customer")
frappe.throw("NoneType has no attribute 'name'")
frappe.throw("Query failed")

# ✅ GOOD - Clear, actionable
frappe.throw("Please select a customer before saving")
frappe.throw(f"Customer '{doc.customer}' not found. Please verify the customer exists.")
frappe.throw("Could not calculate totals. Please ensure all items have valid quantities.")
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

- `erpnext-syntax-serverscripts` - Server Script syntax
- `erpnext-impl-serverscripts` - Implementation workflows
- `erpnext-errors-clientscripts` - Client-side error handling
- `erpnext-database` - Database operations
