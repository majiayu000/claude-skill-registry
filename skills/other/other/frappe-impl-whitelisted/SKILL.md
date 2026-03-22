---
name: frappe-impl-whitelisted
description: >
  Use when building API endpoints with @frappe.whitelist() in Frappe.
  Covers endpoint design, permission patterns, error handling, client
  integration, file uploads, background jobs, rate limiting, REST API
  testing, and migration from Server Scripts to whitelisted methods.
  Prevents permission bypasses, SQL injection, and data exposure.
  Keywords: how to create API, build REST endpoint, frappe.call,
  frappe.whitelist, API permission, guest API, secure endpoint,
  rate limiting, curl testing, frm.call.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Whitelisted Methods Implementation Workflow

Step-by-step workflows for building API endpoints. For decorator syntax, see `frappe-syntax-whitelisted`.

**Version**: v14/v15/v16 (version-specific features noted)

---

## Master Decision: What Type of Endpoint?

```
WHAT ARE YOU BUILDING?
│
├─► Public API (no login required)?
│   └─► allow_guest=True + STRICT input validation + rate limiting
│
├─► Authenticated API for logged-in users?
│   └─► Default @frappe.whitelist() + document permission checks
│
├─► Admin-only API?
│   └─► frappe.only_for("System Manager")
│
├─► Document-specific method (called from form)?
│   └─► Controller method + frm.call() from JS
│
├─► Standalone utility API?
│   └─► Separate api.py + frappe.call() from JS
│
├─► External webhook receiver?
│   └─► allow_guest=True + signature verification
│
└─► Background job trigger?
    └─► Authenticated API that calls frappe.enqueue()
```

---

## Workflow 1: Design the Endpoint

### Step 1: Choose Location

```
WHERE SHOULD THE CODE LIVE?
│
├─► Related to a DocType, called from its form?
│   └─► doctype/xxx/xxx.py (controller method)
│       Client: frm.call('method_name', args)
│
├─► Related to a DocType, standalone?
│   └─► doctype/xxx/xxx_api.py or myapp/api/module.py
│       Client: frappe.call('myapp.api.module.method')
│
├─► General app utility?
│   └─► myapp/api.py (small app) or myapp/api/module.py (large app)
│
└─► External integration?
    └─► myapp/integrations/service_name.py
```

### Step 2: Choose Permission Model

```
WHO CAN CALL THIS API?
│
├─► Anyone (public) → allow_guest=True
│   ⚠️ MUST validate ALL input, sanitize for XSS, rate limit
│
├─► Any logged-in user → Default (no allow_guest)
│   Still check document permissions per record!
│
├─► Specific role(s) → frappe.only_for("Role")
│
└─► Document-level → frappe.has_permission(doctype, ptype, doc)
```

### Step 3: Choose HTTP Method

```
WHAT DOES THE API DO?
│
├─► Read-only → methods=["GET"]
├─► Creates/modifies data → methods=["POST"]
└─► Both or default → omit methods parameter (all allowed)
```

---

## Workflow 2: Implement an Authenticated API

### Step-by-Step

**Step 1: Create the function**

```python
# myapp/api.py
import frappe
from frappe import _

@frappe.whitelist()
def get_customer_balance(customer):
    """Get outstanding balance for a customer."""
    # 1. Permission check
    if not frappe.has_permission("Customer", "read", customer):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # 2. Validate input
    if not customer or not frappe.db.exists("Customer", customer):
        frappe.throw(_("Customer not found"), frappe.DoesNotExistError)

    # 3. Fetch and return
    balance = frappe.db.sql("""
        SELECT COALESCE(SUM(outstanding_amount), 0)
        FROM `tabSales Invoice`
        WHERE customer = %s AND docstatus = 1
    """, customer)[0][0]

    return {"customer": customer, "balance": balance}
```

**Step 2: Call from Client Script**

```javascript
frappe.call({
    method: 'myapp.api.get_customer_balance',
    args: { customer: 'CUST-00001' },
    callback(r) {
        if (r.message) console.log(r.message.balance);
    }
});
```

**Step 3: Test with curl**

```bash
# Authenticate first
curl -X POST https://site.com/api/method/login \
  -d 'usr=admin&pwd=password'

# Call the API
curl -X POST https://site.com/api/method/myapp.api.get_customer_balance \
  -H "Content-Type: application/json" \
  -d '{"customer": "CUST-00001"}' \
  --cookie cookies.txt

# Or use token auth
curl -X POST https://site.com/api/method/myapp.api.get_customer_balance \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"customer": "CUST-00001"}'
```

---

## Workflow 3: Implement a Public (Guest) API

### Step-by-Step

**Step 1: Create with strict validation**

```python
@frappe.whitelist(allow_guest=True, methods=["POST"])
def submit_inquiry(name, email, phone=None, message=None):
    """Public contact form — strict validation required."""
    # 1. Validate required fields
    if not all([name, email]):
        frappe.throw(_("Name and email are required"))

    # 2. Validate email format
    if not frappe.utils.validate_email_address(email):
        frappe.throw(_("Invalid email address"))

    # 3. Sanitize ALL input
    name = frappe.utils.strip_html(name)[:100]
    email = email.strip().lower()[:200]
    phone = frappe.utils.strip_html(phone)[:20] if phone else None
    message = frappe.utils.strip_html(message)[:2000] if message else None

    # 4. Create record with ignore_permissions
    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": name, "email_id": email,
        "phone": phone, "notes": message, "source": "Website"
    })
    lead.insert(ignore_permissions=True)

    return {"success": True, "message": _("Thank you")}
```

**Step 2: Add rate limiting (v15+)**

```python
from frappe.rate_limiter import rate_limit

@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=5, seconds=60)  # 5 calls per minute
def submit_inquiry(name, email, phone=None, message=None):
    ...
```

### Critical Rules for Guest APIs

- **ALWAYS** validate and sanitize every input parameter
- **ALWAYS** use `methods=["POST"]` for data-writing endpoints
- **ALWAYS** add rate limiting (v15+ decorator or manual cache-based throttle on v14)
- **NEVER** expose internal error details — log with `frappe.log_error()`, show generic message
- **NEVER** return sensitive data (internal IDs, file paths, stack traces)
- **NEVER** pass raw user input to `frappe.get_doc()` — use explicit field mapping

---

## Workflow 4: Implement a Controller Method

### Step-by-Step

**Step 1: Add method to DocType controller**

```python
# myapp/doctype/sales_order/sales_order.py
class SalesOrder(Document):
    @frappe.whitelist()
    def calculate_shipping(self, carrier):
        """Called from form via frm.call()."""
        if not self.shipping_address:
            frappe.throw(_("Shipping address required"))
        rate = get_shipping_rate(self.shipping_address, carrier)
        return {"carrier": carrier, "rate": rate}
```

**Step 2: Call from form JS**

```javascript
frm.call('calculate_shipping', {
    carrier: 'FedEx'
}).then(r => {
    frm.set_value('shipping_amount', r.message.rate);
});
```

**Key difference**: Frappe automatically checks document permissions for controller methods called via `frm.call()`. No manual permission check needed for the document itself.

---

## Workflow 5: Implement Error Handling

### Standard Pattern

```python
@frappe.whitelist()
def process_payment(invoice, amount):
    try:
        # Validate
        if not invoice:
            frappe.throw(_("Invoice required"), frappe.ValidationError)
        if not frappe.has_permission("Sales Invoice", "write", invoice):
            frappe.throw(_("Not permitted"), frappe.PermissionError)

        # Process
        result = do_payment(invoice, float(amount))
        return {"success": True, "data": result}

    except (frappe.ValidationError, frappe.PermissionError):
        raise  # Let Frappe handle (417 / 403)
    except frappe.DoesNotExistError:
        frappe.throw(_("Not found"), frappe.DoesNotExistError)  # 404
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Payment Error")
        frappe.local.response["http_status_code"] = 500
        return {"success": False, "error": _("Internal error")}
```

### HTTP Status Code Reference

| Code | Frappe Exception | When |
|------|-----------------|------|
| 200 | — | Success |
| 403 | PermissionError | Access denied |
| 404 | DoesNotExistError | Not found |
| 409 | DuplicateEntryError | Duplicate |
| 417 | ValidationError | Validation failed |
| 429 | — | Rate limit exceeded (v15+) |
| 500 | Exception | Server error |

---

## Workflow 6: File Upload Endpoint

```python
@frappe.whitelist()
def upload_attachment(doctype, docname):
    """Handle file upload attached to a document."""
    if not frappe.has_permission(doctype, "write", docname):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    file = frappe.request.files.get('file')
    if not file:
        frappe.throw(_("No file provided"))

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file.filename,
        "attached_to_doctype": doctype,
        "attached_to_name": docname,
        "content": file.read(),
        "is_private": 1
    })
    file_doc.insert(ignore_permissions=True)
    return {"file_url": file_doc.file_url}
```

---

## Workflow 7: Background Job Endpoint

```python
@frappe.whitelist()
def start_heavy_export(doctype, filters=None):
    """Trigger a background job — returns immediately."""
    frappe.only_for("System Manager")

    frappe.enqueue(
        "myapp.tasks.export_data",
        queue="long",
        timeout=1500,
        doctype=doctype,
        filters=filters,
        user=frappe.session.user
    )
    return {"status": "queued", "message": _("Export started")}
```

---

## Client Integration Patterns

### frappe.call() with Options

```javascript
frappe.call({
    method: 'myapp.api.my_method',
    args: { param: 'value' },
    freeze: true,
    freeze_message: __('Processing...'),
    callback(r) { console.log(r.message); },
    error(r) { frappe.msgprint(__('Error')); }
});
```

### Async/Await Pattern

```javascript
const r = await frappe.call({
    method: 'myapp.api.get_data',
    args: { id: 123 }
});
console.log(r.message);
```

### REST API from External System

```bash
# Token auth (recommended for integrations)
curl -H "Authorization: token api_key:api_secret" \
  https://site.com/api/method/myapp.api.method

# Bearer auth (OAuth)
curl -H "Authorization: Bearer access_token" \
  https://site.com/api/method/myapp.api.method
```

---

## Security Rules (ALWAYS/NEVER)

1. **ALWAYS** check permissions before accessing any document
2. **ALWAYS** use parameterized queries — **NEVER** use f-strings in SQL
3. **ALWAYS** validate and sanitize input for guest APIs
4. **ALWAYS** check role with `frappe.only_for()` before using `ignore_permissions=True`
5. **NEVER** expose internal errors — log details, return generic message
6. **NEVER** use `methods=["GET"]` for endpoints that modify data
7. **NEVER** trust `data` dicts from guest APIs — use explicit parameter names
8. **ALWAYS** include `X-Frappe-CSRF-Token` header in fetch() calls from browser

---

## Migration: Server Script API to Whitelisted Method

| Step | Action |
|------|--------|
| 1 | Copy Server Script logic to `myapp/api/module.py` |
| 2 | Add `@frappe.whitelist()` decorator with same permission model |
| 3 | Update all `frappe.call()` references to new dotted path |
| 4 | Disable or delete the Server Script |
| 5 | Run `bench --site sitename migrate` |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|:---:|:---:|:---:|
| @frappe.whitelist() | Yes | Yes | Yes |
| allow_guest | Yes | Yes | Yes |
| methods parameter | Yes | Yes | Yes |
| Type annotation validation | No | **Yes** | Yes |
| @rate_limit decorator | No | **Yes** | Yes |
| API v2 endpoints | No | **Yes** | Yes |

### v15+ Type Validation

```python
@frappe.whitelist()
def typed_api(customer: str, limit: int = 10) -> dict:
    """v15+ validates types from annotations automatically."""
    return {"customer": customer, "limit": limit}
```

---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete API type and permission selection guide |
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns (10+ workflows) |
| [examples.md](references/examples.md) | Production-ready code examples |
