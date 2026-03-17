---
name: erpnext-syntax-whitelisted
description: "Deterministic syntax for Frappe Whitelisted Methods (Python API endpoints) for v14/v15/v16. Use when Claude needs to generate code for API functions, REST endpoints, @frappe.whitelist() decorator, frappe.call() or frm.call() invocations, permission checks in APIs, error handling patterns, or when questions concern API structure, response formats, or client-server communication. Triggers: whitelisted, API endpoint, frappe.call, frm.call, REST API, @frappe.whitelist, allow_guest, API method."
---
# ERPNext Syntax: Whitelisted Methods

Whitelisted Methods expose Python functions as REST API endpoints.

## Quick Reference

### Basic Whitelisted Method

```python
import frappe

@frappe.whitelist()
def get_customer_summary(customer):
    """Basic API endpoint - authenticated users only."""
    if not frappe.has_permission("Customer", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    
    return frappe.get_doc("Customer", customer).as_dict()
```

### Endpoint URL

`/api/method/myapp.api.get_customer_summary`

---

## Decorator Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `allow_guest` | `False` | `True` = accessible without login |
| `methods` | All | `["GET"]`, `["POST"]`, or combination |
| `xss_safe` | `False` | `True` = don't escape HTML |

```python
# Public endpoint, POST only
@frappe.whitelist(allow_guest=True, methods=["POST"])
def submit_contact_form(name, email, message):
    # Validate input carefully with guest access!
    if not name or not email:
        frappe.throw(_("Name and email required"))
    return {"success": True}

# Read-only endpoint
@frappe.whitelist(methods=["GET"])
def get_status(order_id):
    return frappe.db.get_value("Sales Order", order_id, "status")
```

**Full options**: See [decorator-options.md](references/decorator-options.md)

---

## Permission Patterns

### ALWAYS Check Permissions

```python
@frappe.whitelist()
def get_data(doctype, name):
    # Check BEFORE fetching data
    if not frappe.has_permission(doctype, "read", name):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    return frappe.get_doc(doctype, name).as_dict()
```

### Role-Based Access

```python
@frappe.whitelist()
def admin_function():
    frappe.only_for("System Manager")  # Throws if user lacks role
    return {"admin_data": "sensitive"}

@frappe.whitelist()
def multi_role_function():
    frappe.only_for(["System Manager", "HR Manager"])
    return {"data": "value"}
```

**Security patterns**: See [permission-patterns.md](references/permission-patterns.md)

---

## Error Handling

### frappe.throw() for User-Facing Errors

```python
@frappe.whitelist()
def process_order(order_id, amount):
    # Validation error
    if not order_id:
        frappe.throw(_("Order ID required"), title=_("Missing Data"))
    
    # Permission error
    if not frappe.has_permission("Sales Order", "write"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    
    # Business logic error
    if amount < 0:
        frappe.throw(
            _("Amount cannot be negative: {0}").format(amount),
            frappe.ValidationError
        )
```

### Exception Types and HTTP Codes

| Exception | HTTP Code | When |
|-----------|-----------|------|
| `frappe.ValidationError` | 417 | Validation errors |
| `frappe.PermissionError` | 403 | Access denied |
| `frappe.DoesNotExistError` | 404 | Not found |
| `frappe.DuplicateEntryError` | 409 | Duplicate |
| `frappe.AuthenticationError` | 401 | Not logged in |

### Robust Error Pattern

```python
@frappe.whitelist()
def robust_api(param):
    try:
        result = process_data(param)
        return {"success": True, "data": result}
    except frappe.DoesNotExistError:
        frappe.local.response["http_status_code"] = 404
        return {"success": False, "error": "Not found"}
    except frappe.PermissionError:
        frappe.local.response["http_status_code"] = 403
        return {"success": False, "error": "Access denied"}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "API Error")
        frappe.local.response["http_status_code"] = 500
        return {"success": False, "error": "Internal error"}
```

**Full error patterns**: See [error-handling.md](references/error-handling.md)

---

## Response Patterns

### Return Value (Recommended)

```python
@frappe.whitelist()
def get_summary(customer):
    return {
        "customer": customer,
        "total": 15000
    }
# Response: {"message": {"customer": "...", "total": 15000}}
```

### Custom HTTP Status

```python
@frappe.whitelist()
def create_item(data):
    if not data:
        frappe.local.response["http_status_code"] = 400
        return {"error": "Data required"}
    # ... create item
    frappe.local.response["http_status_code"] = 201
    return {"created": True}
```

**Full response patterns**: See [response-patterns.md](references/response-patterns.md)

---

## Client Calls

### frappe.call() - Standalone APIs

```javascript
// Promise-based (recommended)
frappe.call({
    method: 'myapp.api.get_customer_summary',
    args: { customer: 'CUST-00001' }
}).then(r => {
    console.log(r.message);
});

// With loading indicator
frappe.call({
    method: 'myapp.api.process_data',
    args: { data: myData },
    freeze: true,
    freeze_message: __('Processing...')
});
```

### frm.call() - Controller Methods

```javascript
frm.call('calculate_taxes', {
    include_shipping: true
}).then(r => {
    frm.set_value('tax_amount', r.message.tax_amount);
});
```

**Full client patterns**: See [client-calls.md](references/client-calls.md)

---

## Decision Tree: Which Options?

```
Who may call the API?
│
├─► Anyone (including guests)?
│   └─► allow_guest=True + extra input validation
│
└─► Logged-in users only?
    │
    └─► Specific role required?
        ├─► Yes → frappe.only_for("RoleName") in method
        └─► No → frappe.has_permission() check

Which HTTP methods?
│
├─► Read only?
│   └─► methods=["GET"]
│
├─► Write only?
│   └─► methods=["POST"]
│
└─► Both?
    └─► methods=["GET", "POST"] or default (all)
```

---

## Security Checklist

For EVERY whitelisted method:

- [ ] Permission check present (`frappe.has_permission()` or `frappe.only_for()`)
- [ ] Input validation (types, ranges, formats)
- [ ] No SQL injection (parameterized queries)
- [ ] No sensitive data in error messages
- [ ] `allow_guest=True` only with explicit reason
- [ ] `ignore_permissions=True` only with role check
- [ ] HTTP method restricted where possible

---

## Critical Rules

### 1. NEVER Skip Permission Check

```python
# ❌ WRONG - anyone can see all data
@frappe.whitelist()
def get_all_salaries():
    return frappe.get_all("Salary Slip", fields=["*"])

# ✅ CORRECT
@frappe.whitelist()
def get_salaries():
    frappe.only_for("HR Manager")
    return frappe.get_all("Salary Slip", fields=["*"])
```

### 2. NEVER Use User Input in SQL

```python
# ❌ WRONG - SQL injection!
@frappe.whitelist()
def search(term):
    return frappe.db.sql(f"SELECT * FROM tabCustomer WHERE name LIKE '%{term}%'")

# ✅ CORRECT - parameterized
@frappe.whitelist()
def search(term):
    return frappe.db.sql("""
        SELECT * FROM tabCustomer WHERE name LIKE %(term)s
    """, {"term": f"%{term}%"}, as_dict=True)
```

### 3. NEVER Leak Sensitive Data in Errors

```python
# ❌ WRONG - leaks internal information
except Exception as e:
    frappe.throw(str(e))  # May leak stack traces!

# ✅ CORRECT
except Exception:
    frappe.log_error(frappe.get_traceback(), "API Error")
    frappe.throw(_("An error occurred"))
```

**All anti-patterns**: See [anti-patterns.md](references/anti-patterns.md)

---

## Version Differences (v14 vs v15)

| Feature | v14 | v15 |
|---------|-----|-----|
| Type annotations validation | ❌ | ✅ |
| API v2 endpoints | ❌ | ✅ `/api/v2/` |
| Rate limiting decorators | ❌ | ✅ `@rate_limit()` |
| Document method endpoint | N/A | `/api/v2/document/{dt}/{name}/method/{m}` |

### v15 Type Validation

```python
@frappe.whitelist()
def get_orders(customer: str, limit: int = 10) -> dict:
    """v15 validates types automatically on request."""
    return {"orders": frappe.get_all("Sales Order", limit=limit)}
```

---

## Reference Files

| File | Content |
|------|---------|
| [decorator-options.md](references/decorator-options.md) | All @frappe.whitelist() parameters |
| [parameter-handling.md](references/parameter-handling.md) | Request parameters and type conversion |
| [response-patterns.md](references/response-patterns.md) | Response types and structures |
| [client-calls.md](references/client-calls.md) | frappe.call() and frm.call() patterns |
| [permission-patterns.md](references/permission-patterns.md) | Security best practices |
| [error-handling.md](references/error-handling.md) | Error patterns and exception types |
| [examples.md](references/examples.md) | Complete working API examples |
| [anti-patterns.md](references/anti-patterns.md) | What to avoid |
