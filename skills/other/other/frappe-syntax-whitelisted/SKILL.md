---
name: frappe-syntax-whitelisted
description: >
  Use when creating Frappe Whitelisted Methods (Python API endpoints) for
  v14/v15/v16. Covers @frappe.whitelist() decorator, frappe.call/frm.call
  invocations, permission checks, error handling, response formats, and
  client-server communication. Keywords: whitelisted, API endpoint,
  frappe.call, frm.call, REST API, @frappe.whitelist, allow_guest.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---
# Frappe Syntax: Whitelisted Methods

Whitelisted methods expose Python functions as HTTP API endpoints via `/api/method/`.

## Quick Reference

```python
import frappe
from frappe import _

# Authenticated endpoint (default)
@frappe.whitelist()
def get_customer_summary(customer):
    frappe.has_permission("Customer", "read", throw=True)
    return frappe.get_doc("Customer", customer).as_dict()

# Public endpoint — ALWAYS validate input thoroughly
@frappe.whitelist(allow_guest=True, methods=["POST"])
def submit_contact(name, email, message):
    if not name or not email:
        frappe.throw(_("Name and email required"), frappe.ValidationError)
    return {"success": True}

# Controller method — called via frm.call('method_name')
class SalesOrder(Document):
    @frappe.whitelist()
    def calculate_taxes(self, include_shipping=False):
        return {"tax": self.grand_total * 0.21}
```

**Endpoint URL**: `/api/method/myapp.module.function_name`

---

## Decorator Signature [v14+]

```python
@frappe.whitelist(
    allow_guest=False,   # True = accessible without login
    xss_safe=False,      # True = do NOT escape HTML in response
    methods=None,        # ["GET"], ["POST"], or ["GET","POST"] — default: all
    force_types=None     # True = require type annotations [v15+]
)
```

| Parameter | Default | Effect |
|-----------|---------|--------|
| `allow_guest` | `False` | `True` = Guest role can call; ALWAYS add extra input validation |
| `xss_safe` | `False` | `True` = HTML not escaped; NEVER use without sanitized output |
| `methods` | `None` (all) | Restrict allowed HTTP verbs |
| `force_types` | `None` | `True` = all params MUST have type annotations [v15+] |

Full details: [decorator-options.md](references/decorator-options.md)

---

## Decision Tree

```
What kind of endpoint?
|
+-- Standalone API (utility, integration, dashboard)?
|   --> @frappe.whitelist() on a module-level function
|   --> Call via: frappe.call('myapp.api.function')
|   --> URL: /api/method/myapp.api.function
|
+-- Document-specific action?
|   --> @frappe.whitelist() on a Document class method
|   --> Call via: frm.call('method_name')
|   --> URL: /api/method/run_doc_method (internal)
|
+-- Server Script (no-code)?
    --> Use Server Script DocType instead (no decorator needed)

Who may call the API?
|
+-- Anyone (including guests)?
|   --> allow_guest=True + thorough input validation + rate limiting
|
+-- Logged-in users only?
    +-- Specific role? --> frappe.only_for("RoleName")
    +-- DocType-level? --> frappe.has_permission(doctype, ptype, throw=True)
    +-- Document-level? --> frappe.has_permission(doctype, ptype, doc, throw=True)

Which HTTP methods?
|
+-- Read only? --> methods=["GET"]
+-- Write only? --> methods=["POST"]
+-- Both? --> methods=["GET","POST"] or default
```

---

## Permission Patterns

ALWAYS check permissions inside every whitelisted method. The `@frappe.whitelist()` decorator only verifies the user is logged in — it does NOT check DocType or document-level permissions.

```python
# DocType-level permission (throw=True raises PermissionError automatically)
@frappe.whitelist()
def get_orders():
    frappe.has_permission("Sales Order", "read", throw=True)
    return frappe.get_all("Sales Order", limit=20)

# Document-level permission
@frappe.whitelist()
def get_order(name):
    frappe.has_permission("Sales Order", "read", name, throw=True)
    return frappe.get_doc("Sales Order", name).as_dict()

# Role-based restriction
@frappe.whitelist()
def admin_action():
    frappe.only_for("System Manager")  # throws if user lacks role
    return {"secret": "data"}
```

Full patterns: [permission-patterns.md](references/permission-patterns.md)

---

## Parameter Handling

Parameters arrive as **strings** from HTTP requests. ALWAYS convert explicitly.

```python
@frappe.whitelist()
def calculate(amount, quantity, items=None):
    amount = float(amount)          # ALWAYS cast numeric params
    quantity = int(quantity)
    if isinstance(items, str):      # ALWAYS parse JSON strings
        items = frappe.parse_json(items)
    return amount * quantity
```

Access all request parameters via `frappe.form_dict`:
```python
@frappe.whitelist()
def dynamic_handler():
    all_params = frappe.form_dict
    customer = frappe.form_dict.get("customer")
```

### Type Annotations [v15+]

Frappe v15+ validates type annotations automatically at request time via Pydantic:

```python
@frappe.whitelist()
def get_orders(customer: str, limit: int = 10, active: bool = True) -> dict:
    # Frappe auto-validates: limit MUST be convertible to int
    return {"orders": frappe.get_all("Sales Order", limit=limit)}
```

### force_types and require_type_annotated_api_methods [v15+]

- `@frappe.whitelist(force_types=True)` — EVERY parameter MUST have a type annotation
- App-level enforcement via `hooks.py`: `require_type_annotated_api_methods = 1`
- Missing annotations raise `FrappeTypeError`

Full details: [parameter-handling.md](references/parameter-handling.md)

---

## Client Calls

### frappe.call() — Standalone APIs

```javascript
// Promise-based (ALWAYS prefer this)
frappe.call({
    method: 'myapp.api.get_summary',
    args: { customer: 'CUST-001' },
    freeze: true,
    freeze_message: __('Loading...')
}).then(r => {
    console.log(r.message);  // return value is in r.message
}).catch(err => {
    frappe.show_alert({ message: __('Error'), indicator: 'red' });
});
```

### frm.call() — Controller Methods

```javascript
frm.call('calculate_taxes', { include_shipping: true })
    .then(r => frm.set_value('tax_amount', r.message.tax_amount));
```

### REST API (External Clients)

```bash
# Token auth (ALWAYS use for external integrations)
curl -H "Authorization: token api_key:api_secret" \
     -H "Content-Type: application/json" \
     -X POST https://site.com/api/method/myapp.api.create_order \
     -d '{"customer": "CUST-001"}'
```

Full patterns: [client-calls.md](references/client-calls.md)

---

## Error Handling

```python
@frappe.whitelist()
def process_order(order_id):
    if not order_id:
        frappe.throw(_("Order ID required"), frappe.ValidationError)

    if not frappe.has_permission("Sales Order", "write", order_id):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    try:
        result = heavy_operation(order_id)
        return {"success": True, "data": result}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "process_order")
        frappe.throw(_("Operation failed. Contact support."))
```

| Exception | HTTP Code | When to Use |
|-----------|-----------|-------------|
| `frappe.ValidationError` | 417 | Input validation failure |
| `frappe.PermissionError` | 403 | Access denied |
| `frappe.DoesNotExistError` | 404 | Document not found |
| `frappe.DuplicateEntryError` | 409 | Duplicate record |
| `frappe.AuthenticationError` | 401 | Not logged in |

Full patterns: [error-handling.md](references/error-handling.md)

---

## Response Patterns

```python
# Return value auto-wraps as {"message": <return_value>}
@frappe.whitelist()
def get_data():
    return {"key": "value"}   # Client receives: {"message": {"key": "value"}}

# Custom HTTP status
@frappe.whitelist()
def create_item(data):
    doc = frappe.get_doc(data).insert()
    frappe.local.response["http_status_code"] = 201
    return {"name": doc.name}

# File download
@frappe.whitelist()
def download_report(name):
    content = generate_pdf(name)
    frappe.response.filename = f"{name}.pdf"
    frappe.response.filecontent = content
    frappe.response.type = "download"
```

Full patterns: [response-patterns.md](references/response-patterns.md)

---

## Rate Limiting [v14+]

```python
from frappe.rate_limiter import rate_limit

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60)  # 5 requests per 60 seconds per IP
def public_endpoint():
    return {"status": "ok"}
```

`rate_limit` signature:
```python
rate_limit(key=None, limit=5, seconds=86400, methods="ALL", ip_based=True)
```

ALWAYS apply `@rate_limit` on `allow_guest=True` endpoints to prevent abuse.

---

## Version Differences

| Feature | v14 | v15+ | v16+ |
|---------|-----|------|------|
| `@frappe.whitelist()` | Yes | Yes | Yes |
| `allow_guest`, `xss_safe`, `methods` | Yes | Yes | Yes |
| Type annotation validation | No | Yes (auto via Pydantic) | Yes |
| `force_types` parameter | No | Yes | Yes |
| `require_type_annotated_api_methods` hook | No | Yes | Yes |
| `@rate_limit()` decorator | Yes | Yes | Yes |
| `FrappeTypeError` for missing annotations | No | Yes | Yes |

---

## Critical Rules

1. **NEVER skip permission checks** — `@frappe.whitelist()` only confirms login, not authorization
2. **NEVER use user input in raw SQL** — ALWAYS use parameterized queries or ORM
3. **NEVER leak stack traces** — log with `frappe.log_error()`, show generic messages
4. **ALWAYS validate input types** — parameters arrive as strings from HTTP
5. **ALWAYS apply `@rate_limit` on guest endpoints** — prevents abuse
6. **NEVER use `ignore_permissions=True` without a preceding role check**
7. **ALWAYS use `JSON.stringify()` for complex JS args** — arrays and objects

Full anti-patterns: [anti-patterns.md](references/anti-patterns.md)

---

## Security Checklist

For EVERY whitelisted method, verify:

- [ ] Permission check present (`frappe.has_permission()` or `frappe.only_for()`)
- [ ] Input validated (types, ranges, formats)
- [ ] SQL queries parameterized (NEVER string interpolation)
- [ ] Error messages contain no internal details
- [ ] `allow_guest=True` only with explicit reason + rate limiting
- [ ] `ignore_permissions=True` only with preceding role check
- [ ] HTTP methods restricted where possible
- [ ] Response contains only necessary fields (no sensitive data leaks)

---

## Reference Files

| File | Content |
|------|---------|
| [decorator-options.md](references/decorator-options.md) | All `@frappe.whitelist()` parameters and `force_types` |
| [parameter-handling.md](references/parameter-handling.md) | Request parameters, type coercion, `frappe.form_dict` |
| [response-patterns.md](references/response-patterns.md) | Return types, file downloads, streaming, HTTP status |
| [client-calls.md](references/client-calls.md) | `frappe.call()`, `frm.call()`, REST API, fetch patterns |
| [permission-patterns.md](references/permission-patterns.md) | Permission checks, role guards, custom logic |
| [error-handling.md](references/error-handling.md) | Exception types, `frappe.throw()`, logging |
| [examples.md](references/examples.md) | Complete working API examples |
| [anti-patterns.md](references/anti-patterns.md) | Security mistakes and performance pitfalls |
| [hooks.md](references/hooks.md) | Declaring whitelisted methods in `hooks.py` |
| [syntax.md](references/syntax.md) | Core decorator syntax and registration mechanics |
