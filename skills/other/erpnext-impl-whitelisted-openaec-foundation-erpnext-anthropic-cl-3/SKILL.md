---
name: erpnext-impl-whitelisted
description: "Implementation workflows and decision trees for Frappe Whitelisted Methods (REST APIs). Use when determining HOW to implement API endpoints: public vs authenticated, permission patterns, error handling, response formats, client integration. Triggers: how do I create API, build REST endpoint, frappe.call pattern, API permission check, guest API, secure endpoint."
---

# ERPNext Whitelisted Methods - Implementation

This skill helps you determine HOW to implement REST API endpoints. For exact syntax, see `erpnext-syntax-whitelisted`.

**Version**: v14/v15/v16 compatible

## Main Decision: What Type of API?

```
┌───────────────────────────────────────────────────────────────────┐
│ WHAT ARE YOU BUILDING?                                            │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ► Public API (contact forms, status checks)?                      │
│   └── allow_guest=True + strict input validation                  │
│                                                                   │
│ ► Internal API for logged-in users?                               │
│   └── Default (no allow_guest) + permission checks                │
│                                                                   │
│ ► Admin-only API?                                                 │
│   └── frappe.only_for("System Manager")                           │
│                                                                   │
│ ► Document-specific method (on a form)?                           │
│   └── Controller method + frm.call()                              │
│                                                                   │
│ ► Standalone utility API?                                         │
│   └── Separate api.py + frappe.call()                             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

→ See [references/decision-tree.md](references/decision-tree.md) for complete guide.

---

## Decision: Where to Put API Code?

```
WHERE SHOULD YOUR API LIVE?
│
├─► Related to a specific DocType?
│   │
│   ├─► Called from that DocType's form?
│   │   └─► Controller method (doctype/xxx/xxx.py)
│   │       Client: frm.call('method_name', args)
│   │
│   └─► Standalone but DocType-related?
│       └─► Same file or doctype/xxx/xxx_api.py
│           Client: frappe.call('path.to.method', args)
│
├─► General utility API?
│   └─► myapp/api.py or myapp/api/module.py
│       Client: frappe.call('myapp.api.method', args)
│
└─► External integration?
    └─► myapp/integrations/service_name.py
        Often combined with webhooks
```

---

## Decision: Permission Model

```
WHO CAN ACCESS THIS API?
│
├─► Anyone (public)?
│   └─► allow_guest=True
│       ⚠️ MUST validate all input
│       ⚠️ MUST rate limit if possible
│       ⚠️ NEVER expose sensitive data
│
├─► Any logged-in user?
│   └─► Default (no allow_guest)
│       Still check document permissions!
│
├─► Specific role(s)?
│   └─► frappe.only_for("Role") or frappe.only_for(["Role1", "Role2"])
│       Throws PermissionError if user lacks role
│
├─► Document-level permission?
│   └─► frappe.has_permission(doctype, ptype, doc)
│       Check before accessing each document
│
└─► Custom permission logic?
    └─► Implement your own checks
        Always deny by default
```

---

## Quick Implementation Patterns

### Pattern 1: Simple Authenticated API

```python
# myapp/api.py
import frappe
from frappe import _

@frappe.whitelist()
def get_customer_balance(customer):
    """Get customer's outstanding balance."""
    # Permission check
    if not frappe.has_permission("Customer", "read", customer):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    
    # Fetch data
    balance = frappe.db.get_value("Customer", customer, "outstanding_amount")
    
    return {"customer": customer, "balance": balance or 0}
```

```javascript
// Client call
frappe.call({
    method: 'myapp.api.get_customer_balance',
    args: { customer: 'CUST-00001' }
}).then(r => {
    console.log(r.message.balance);
});
```

### Pattern 2: Public API with Validation

```python
@frappe.whitelist(allow_guest=True, methods=["POST"])
def submit_inquiry(name, email, message):
    """Public contact form - strict validation required."""
    # Validate required fields
    if not all([name, email, message]):
        frappe.throw(_("All fields are required"))
    
    # Validate email format
    if not frappe.utils.validate_email_address(email):
        frappe.throw(_("Invalid email address"))
    
    # Sanitize input
    name = frappe.utils.strip_html(name)[:100]
    message = frappe.utils.strip_html(message)[:2000]
    
    # Create record
    doc = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": name,
        "email_id": email,
        "notes": message,
        "source": "Website"
    })
    doc.insert(ignore_permissions=True)
    
    return {"success": True, "id": doc.name}
```

### Pattern 3: Role-Restricted API

```python
@frappe.whitelist()
def get_salary_data(employee):
    """HR-only endpoint."""
    # Role check - throws if not HR
    frappe.only_for(["HR Manager", "HR User"])
    
    return frappe.get_doc("Employee", employee).as_dict()
```

### Pattern 4: Document Controller Method

```python
# In doctype/sales_order/sales_order.py
class SalesOrder(Document):
    @frappe.whitelist()
    def calculate_shipping(self, carrier):
        """Called via frm.call() from form."""
        # Permission already checked by Frappe for doc access
        rate = get_shipping_rate(self.shipping_address, carrier)
        return {"carrier": carrier, "rate": rate}
```

```javascript
// Client (in sales_order.js)
frm.call('calculate_shipping', {
    carrier: 'FedEx'
}).then(r => {
    frm.set_value('shipping_amount', r.message.rate);
});
```

→ See [references/workflows.md](references/workflows.md) for 10+ complete workflows.

---

## Critical Security Rules

### 1. ALWAYS Check Permissions

```python
# ❌ WRONG - exposes all data
@frappe.whitelist()
def get_document(doctype, name):
    return frappe.get_doc(doctype, name).as_dict()

# ✅ CORRECT
@frappe.whitelist()
def get_document(doctype, name):
    if not frappe.has_permission(doctype, "read", name):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    return frappe.get_doc(doctype, name).as_dict()
```

### 2. NEVER Trust User Input in SQL

```python
# ❌ WRONG - SQL injection!
@frappe.whitelist()
def search(term):
    return frappe.db.sql(f"SELECT * FROM tabItem WHERE name LIKE '%{term}%'")

# ✅ CORRECT - parameterized
@frappe.whitelist()
def search(term):
    return frappe.db.sql("""
        SELECT name, item_name FROM tabItem 
        WHERE name LIKE %(term)s
        LIMIT 20
    """, {"term": f"%{term}%"}, as_dict=True)
```

### 3. VALIDATE All Input for Guest APIs

```python
@frappe.whitelist(allow_guest=True)
def public_api(data):
    # ❌ WRONG - trusts input
    doc = frappe.get_doc(data)
    doc.insert(ignore_permissions=True)
    
    # ✅ CORRECT - validate everything
    if not isinstance(data, dict):
        frappe.throw(_("Invalid data format"))
    
    allowed_fields = {"name", "email", "message"}
    clean_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    # Validate each field...
```

### 4. NEVER Expose Sensitive Data in Errors

```python
# ❌ WRONG - leaks internal info
except Exception as e:
    frappe.throw(str(e))

# ✅ CORRECT - generic message, log details
except Exception:
    frappe.log_error(frappe.get_traceback(), "API Error")
    frappe.throw(_("An error occurred. Please try again."))
```

### 5. Use ignore_permissions Sparingly

```python
# ❌ WRONG - bypasses all security
@frappe.whitelist()
def get_all_data():
    return frappe.get_all("Salary Slip", ignore_permissions=True)

# ✅ CORRECT - check role first
@frappe.whitelist()
def get_all_data():
    frappe.only_for("HR Manager")  # Verify role first!
    return frappe.get_all("Salary Slip", ignore_permissions=True)
```

---

## Error Handling Pattern

### Standard Error Response

```python
@frappe.whitelist()
def robust_api(param):
    """API with proper error handling."""
    try:
        # Validate input
        if not param:
            frappe.throw(_("Parameter required"), frappe.ValidationError)
        
        # Check permissions
        if not frappe.has_permission("MyDocType", "read"):
            frappe.throw(_("Not permitted"), frappe.PermissionError)
        
        # Process
        result = do_something(param)
        return {"success": True, "data": result}
        
    except frappe.ValidationError:
        raise  # Let Frappe handle (417)
    except frappe.PermissionError:
        raise  # Let Frappe handle (403)
    except frappe.DoesNotExistError:
        frappe.local.response["http_status_code"] = 404
        return {"success": False, "error": "Not found"}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "API Error")
        frappe.local.response["http_status_code"] = 500
        return {"success": False, "error": "Internal error"}
```

### HTTP Status Codes

| Code | Exception | When to Use |
|------|-----------|-------------|
| 200 | - | Success |
| 201 | - | Created (set manually) |
| 400 | - | Bad request (set manually) |
| 401 | AuthenticationError | Not logged in |
| 403 | PermissionError | Access denied |
| 404 | DoesNotExistError | Not found |
| 417 | ValidationError | Validation failed |
| 409 | DuplicateEntryError | Duplicate |
| 500 | Exception | Server error |

---

## Response Patterns

### Simple Return (Most Common)

```python
@frappe.whitelist()
def get_data():
    return {"key": "value"}
# Response: {"message": {"key": "value"}}
```

### List Response

```python
@frappe.whitelist()
def get_items():
    return frappe.get_all("Item", fields=["name", "item_name"], limit=10)
# Response: {"message": [{"name": "...", "item_name": "..."}, ...]}
```

### With Metadata

```python
@frappe.whitelist()
def get_paged_data(page=1, page_size=20):
    offset = (int(page) - 1) * int(page_size)
    total = frappe.db.count("Item")
    items = frappe.get_all("Item", limit=page_size, start=offset)
    
    return {
        "data": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }
```

---

## Client Integration

### frappe.call() Options

```javascript
frappe.call({
    method: 'myapp.api.my_method',
    args: { param1: 'value' },
    
    // UI Options
    freeze: true,                    // Show loading overlay
    freeze_message: __('Loading...'), // Custom message
    
    // Callbacks
    callback: function(r) {
        if (r.message) { /* success */ }
    },
    error: function(r) {
        // Handle error
    },
    always: function() {
        // Always runs (finally)
    },
    
    // Other
    async: true,                     // Default true
    type: 'POST'                     // Default POST
});
```

### Async/Await Pattern

```javascript
async function fetchData() {
    try {
        const r = await frappe.call({
            method: 'myapp.api.get_data',
            args: { id: 123 }
        });
        return r.message;
    } catch (e) {
        frappe.msgprint(__('Error loading data'));
        console.error(e);
    }
}
```

---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete API type selection guide |
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns |
| [examples.md](references/examples.md) | Complete working examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes to avoid |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|:---:|:---:|:---:|
| @frappe.whitelist() | ✅ | ✅ | ✅ |
| allow_guest | ✅ | ✅ | ✅ |
| methods parameter | ✅ | ✅ | ✅ |
| Type annotation validation | ❌ | ✅ | ✅ |
| Rate limiting decorator | ❌ | ✅ | ✅ |
| API v2 endpoints | ❌ | ✅ | ✅ |

### v15+ Type Validation

```python
# v15+ validates types automatically
@frappe.whitelist()
def typed_api(customer: str, limit: int = 10) -> dict:
    return {"customer": customer, "limit": limit}
```

### v15+ Rate Limiting

```python
from frappe.rate_limiter import rate_limit

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60)  # 5 calls per minute
def rate_limited_api():
    return {"status": "ok"}
```
