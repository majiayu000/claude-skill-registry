---
name: erpnext-errors-database
description: "Error handling patterns for ERPNext/Frappe database operations. Use when handling DoesNotExistError, DuplicateEntryError, transaction failures, and query errors. Covers retry patterns and data integrity. V14/V15/V16 compatible. Triggers: database error, DoesNotExistError, DuplicateEntryError, transaction failed, query error."
---

# ERPNext Database - Error Handling

This skill covers error handling patterns for database operations. For syntax, see `erpnext-database`.

**Version**: v14/v15/v16 compatible

---

## Database Exception Types

```
┌─────────────────────────────────────────────────────────────────────┐
│ FRAPPE DATABASE EXCEPTIONS                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ frappe.DoesNotExistError                                            │
│   └─► Document not found (get_doc, get_value with strict)           │
│                                                                     │
│ frappe.DuplicateEntryError                                          │
│   └─► Unique constraint violation (insert, rename)                  │
│                                                                     │
│ frappe.LinkExistsError                                              │
│   └─► Cannot delete - linked documents exist                        │
│                                                                     │
│ frappe.ValidationError                                              │
│   └─► General validation failure                                    │
│                                                                     │
│ frappe.TimestampMismatchError                                       │
│   └─► Concurrent edit detected (modified since load)                │
│                                                                     │
│ frappe.db.InternalError                                             │
│   └─► Database-level error (deadlock, connection lost)              │
│                                                                     │
│ frappe.QueryTimeoutError (v15+)                                     │
│   └─► Query exceeded timeout limit                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Main Decision: Error Handling by Operation

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT DATABASE OPERATION?                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► frappe.get_doc() / frappe.get_cached_doc()                            │
│   └─► Can raise DoesNotExistError                                       │
│   └─► Check with frappe.db.exists() first OR catch exception            │
│                                                                         │
│ ► doc.insert() / frappe.new_doc().insert()                              │
│   └─► Can raise DuplicateEntryError (unique constraints)                │
│   └─► Can raise ValidationError (mandatory fields, custom validation)   │
│                                                                         │
│ ► doc.save()                                                            │
│   └─► Can raise ValidationError                                         │
│   └─► Can raise TimestampMismatchError (concurrent edit)                │
│                                                                         │
│ ► doc.delete() / frappe.delete_doc()                                    │
│   └─► Can raise LinkExistsError (linked documents)                      │
│   └─► Use force=True to ignore links (careful!)                         │
│                                                                         │
│ ► frappe.db.sql() / frappe.qb                                           │
│   └─► Can raise InternalError (syntax, deadlock, connection)            │
│   └─► Always use parameterized queries                                  │
│                                                                         │
│ ► frappe.db.set_value() / doc.db_set()                                  │
│   └─► Silently fails if record doesn't exist                            │
│   └─► No validation triggered                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling Patterns

### Pattern 1: Safe Document Fetch

```python
# Option A: Check first (preferred for expected missing docs)
if frappe.db.exists("Customer", customer_name):
    customer = frappe.get_doc("Customer", customer_name)
else:
    frappe.throw(_("Customer '{0}' not found").format(customer_name))

# Option B: Try/except (preferred when doc usually exists)
try:
    customer = frappe.get_doc("Customer", customer_name)
except frappe.DoesNotExistError:
    frappe.throw(_("Customer '{0}' not found").format(customer_name))

# Option C: Get with default (for optional lookups)
customer = frappe.db.get_value("Customer", customer_name, "*", as_dict=True)
if not customer:
    # Handle missing - no error raised
    customer = {"customer_name": "Unknown", "credit_limit": 0}
```

### Pattern 2: Safe Document Insert

```python
def create_customer(data):
    """Create customer with duplicate handling."""
    try:
        doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": data.get("name"),
            "customer_type": data.get("type", "Company")
        })
        doc.insert()
        return {"success": True, "name": doc.name}
        
    except frappe.DuplicateEntryError:
        # Already exists - return existing
        existing = frappe.db.get_value("Customer", {"customer_name": data.get("name")})
        return {"success": True, "name": existing, "existing": True}
        
    except frappe.ValidationError as e:
        return {"success": False, "error": str(e)}
```

### Pattern 3: Safe Document Delete

```python
def delete_customer(customer_name):
    """Delete customer with link handling."""
    if not frappe.db.exists("Customer", customer_name):
        frappe.throw(_("Customer '{0}' not found").format(customer_name))
    
    try:
        frappe.delete_doc("Customer", customer_name)
        return {"success": True}
        
    except frappe.LinkExistsError as e:
        # Get linked documents for user info
        linked = get_linked_documents("Customer", customer_name)
        frappe.throw(
            _("Cannot delete customer. Linked documents exist:<br>{0}").format(
                "<br>".join([f"• {l['doctype']}: {l['name']}" for l in linked[:10]])
            )
        )
```

### Pattern 4: Concurrent Edit Handling

```python
def update_document(doctype, name, updates):
    """Update with concurrent edit detection."""
    try:
        doc = frappe.get_doc(doctype, name)
        doc.update(updates)
        doc.save()
        return {"success": True}
        
    except frappe.TimestampMismatchError:
        # Document was modified by another user
        frappe.throw(
            _("This document was modified by another user. Please refresh and try again."),
            title=_("Concurrent Edit Detected")
        )
    except frappe.DoesNotExistError:
        frappe.throw(_("Document not found"))
```

### Pattern 5: Batch Operations with Error Isolation

```python
def bulk_update_items(items_data):
    """Bulk update with per-item error handling."""
    results = {"success": [], "failed": []}
    
    for item_data in items_data:
        item_code = item_data.get("item_code")
        
        try:
            if not frappe.db.exists("Item", item_code):
                results["failed"].append({
                    "item": item_code,
                    "error": "Item not found"
                })
                continue
            
            doc = frappe.get_doc("Item", item_code)
            doc.update(item_data)
            doc.save()
            results["success"].append(item_code)
            
        except frappe.ValidationError as e:
            results["failed"].append({
                "item": item_code,
                "error": str(e)
            })
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Bulk update error: {item_code}")
            results["failed"].append({
                "item": item_code,
                "error": "Unexpected error"
            })
    
    return results
```

### Pattern 6: Safe SQL Query

```python
def get_sales_report(customer, from_date, to_date):
    """Safe SQL query with error handling."""
    try:
        # ALWAYS use parameterized queries
        result = frappe.db.sql("""
            SELECT 
                customer,
                SUM(grand_total) as total,
                COUNT(*) as count
            FROM `tabSales Invoice`
            WHERE customer = %(customer)s
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND docstatus = 1
            GROUP BY customer
        """, {
            "customer": customer,
            "from_date": from_date,
            "to_date": to_date
        }, as_dict=True)
        
        return result[0] if result else {"total": 0, "count": 0}
        
    except frappe.db.InternalError as e:
        frappe.log_error(frappe.get_traceback(), "Sales Report Query Error")
        frappe.throw(_("Database error. Please try again or contact support."))
```

> **See**: `references/patterns.md` for more error handling patterns.

---

## Transaction Handling

### Automatic Transaction Management

```python
# Frappe wraps each request in a transaction
# On success: auto-commit
# On exception: auto-rollback

def validate(self):
    # All changes are in ONE transaction
    self.calculate_totals()
    frappe.db.set_value("Counter", "main", "count", 100)
    
    if error_condition:
        frappe.throw("Error")  # EVERYTHING rolls back
```

### Manual Savepoints (Advanced)

```python
def complex_operation():
    """Use savepoints for partial rollback."""
    # Create savepoint
    frappe.db.savepoint("before_risky_op")
    
    try:
        risky_database_operation()
    except Exception:
        # Rollback only to savepoint
        frappe.db.rollback(save_point="before_risky_op")
        frappe.log_error(frappe.get_traceback(), "Risky Op Failed")
        # Continue with alternative approach
        safe_alternative_operation()
```

### Scheduler/Background Jobs

```python
def background_task():
    """Background jobs need explicit commit."""
    try:
        for record in records:
            process_record(record)
        
        # REQUIRED in background jobs
        frappe.db.commit()
        
    except Exception:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Background Task Error")
```

---

## Critical Rules

### ✅ ALWAYS

1. **Check existence before get_doc** - Or catch DoesNotExistError
2. **Use parameterized SQL queries** - Never string formatting
3. **Handle DuplicateEntryError on insert** - Unique constraints
4. **Commit in scheduler/background jobs** - No auto-commit
5. **Log database errors with context** - Include query/doc info
6. **Use db.exists() for existence checks** - Not try/except get_doc

### ❌ NEVER

1. **Don't use string formatting in SQL** - SQL injection risk
2. **Don't commit in controller hooks** - Breaks transaction
3. **Don't ignore DoesNotExistError silently** - Handle or log
4. **Don't assume db.set_value() succeeded** - No error on missing doc
5. **Don't catch generic Exception for database ops** - Catch specific types

---

## Quick Reference: Exception Handling

```python
# DoesNotExistError - Document not found
try:
    doc = frappe.get_doc("Customer", name)
except frappe.DoesNotExistError:
    frappe.throw(_("Customer not found"))

# DuplicateEntryError - Unique constraint violation
try:
    doc.insert()
except frappe.DuplicateEntryError:
    # Handle duplicate

# LinkExistsError - Cannot delete linked document
try:
    frappe.delete_doc("Customer", name)
except frappe.LinkExistsError:
    frappe.throw(_("Cannot delete - linked documents exist"))

# TimestampMismatchError - Concurrent edit
try:
    doc.save()
except frappe.TimestampMismatchError:
    frappe.throw(_("Document was modified. Please refresh."))

# InternalError - Database-level error
try:
    frappe.db.sql(query)
except frappe.db.InternalError:
    frappe.log_error(frappe.get_traceback(), "Database Error")
    frappe.throw(_("Database error occurred"))
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

- `erpnext-database` - Database operations syntax
- `erpnext-errors-controllers` - Controller error handling
- `erpnext-errors-serverscripts` - Server Script error handling
- `erpnext-permissions` - Permission patterns
