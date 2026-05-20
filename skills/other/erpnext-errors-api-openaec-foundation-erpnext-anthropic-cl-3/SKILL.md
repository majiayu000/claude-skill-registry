---
name: erpnext-errors-api
description: "Error handling patterns for ERPNext/Frappe API development (v14/v15/v16). Covers whitelisted method errors, REST API errors, client-side handling, external integrations, and webhooks. Triggers: API error, whitelisted method error, frappe.call error, REST API error, webhook error, external API error, HTTP status codes."
---

# ERPNext API Error Handling

Patterns for handling errors in API development. For syntax details, see `erpnext-api-patterns`.

**Version**: v14/v15/v16 compatible

## API Error Handling Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ API ERROR HANDLING DECISION                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Where is the error occurring?                                      │
│                                                                     │
│ Server-side (Python)?                                              │
│ ├── Validation error → frappe.throw() with clear message          │
│ ├── Permission error → frappe.throw() + PermissionError           │
│ ├── Not found        → frappe.throw() + DoesNotExistError         │
│ └── Unexpected       → Log + generic error to client              │
│                                                                     │
│ Client-side (JavaScript)?                                          │
│ ├── frappe.call      → Use error callback or .catch()             │
│ └── frappe.xcall     → Use try/catch with async/await             │
│                                                                     │
│ External integration?                                              │
│ └── requests library → try/except with specific exceptions         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## HTTP Status Codes Reference

| Code | Meaning | When Frappe Uses |
|------|---------|------------------|
| 200 | Success | Normal response |
| 400 | Bad Request | Validation error |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Document doesn't exist |
| 417 | Expectation Failed | frappe.throw() called |
| 500 | Server Error | Unhandled exception |

## Server-Side Patterns

### Basic Whitelisted Method

```python
@frappe.whitelist()
def update_status(docname, status):
    # Validate input
    if not docname:
        frappe.throw(_("Document name is required"), frappe.ValidationError)
    
    if status not in ["Draft", "Submitted", "Cancelled"]:
        frappe.throw(_("Invalid status: {0}").format(status))
    
    try:
        doc = frappe.get_doc("My DocType", docname)
        doc.status = status
        doc.save()
        return {"success": True, "name": doc.name}
    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} not found").format(docname))
    except frappe.PermissionError:
        frappe.throw(_("Permission denied"), frappe.PermissionError)
```

### Bulk Operation with Partial Failure

```python
@frappe.whitelist()
def bulk_update(items):
    items = frappe.parse_json(items)
    results = {"success": [], "failed": []}
    
    for item in items:
        try:
            doc = frappe.get_doc("Item", item["name"])
            doc.update(item)
            doc.save()
            results["success"].append(item["name"])
        except Exception as e:
            results["failed"].append({
                "name": item["name"],
                "error": str(e)
            })
    
    frappe.db.commit()
    return results
```

## Client-Side Patterns

### frappe.call Error Handling

```javascript
frappe.call({
    method: "myapp.api.update_status",
    args: { docname: "DOC-001", status: "Submitted" },
    callback: function(r) {
        if (r.message && r.message.success) {
            frappe.show_alert({message: __("Updated"), indicator: "green"});
        }
    },
    error: function(r) {
        // Called on HTTP error or frappe.throw
        frappe.msgprint({
            title: __("Error"),
            message: r.message || __("Operation failed"),
            indicator: "red"
        });
    }
});
```

### async/await Pattern

```javascript
async function updateDocument(docname, status) {
    try {
        const result = await frappe.xcall("myapp.api.update_status", {
            docname: docname,
            status: status
        });
        return result;
    } catch (error) {
        console.error("API Error:", error);
        frappe.throw(__("Failed to update document"));
    }
}
```

## External API Pattern

```python
import requests

def call_external_api(endpoint, data):
    try:
        response = requests.post(
            endpoint,
            json=data,
            timeout=30,
            headers={"Authorization": f"Bearer {get_api_key()}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        frappe.log_error("External API timeout", "API Integration")
        frappe.throw(_("External service timeout. Please try again."))
    except requests.HTTPError as e:
        frappe.log_error(f"HTTP {e.response.status_code}", "API Integration")
        frappe.throw(_("External service error"))
    except requests.RequestException as e:
        frappe.log_error(str(e), "API Integration")
        frappe.throw(_("Connection failed"))
```

## Critical Rules

### ✅ ALWAYS
- Validate input before processing
- Use `frappe.throw()` for user-facing errors
- Log unexpected errors with `frappe.log_error()`
- Return structured responses from APIs
- Handle both success and error in callbacks

### ❌ NEVER
- Expose internal error details to users
- Catch exceptions without logging
- Return raw exception messages
- Assume API calls will succeed
- Skip input validation

## Quick Reference: Error Responses

```python
# User-facing error (shows alert)
frappe.throw(_("Clear error message"))

# Permission error (403)
frappe.throw(_("Not allowed"), frappe.PermissionError)

# Validation error (400)
frappe.throw(_("Invalid input"), frappe.ValidationError)

# Log error (no user message)
frappe.log_error(frappe.get_traceback(), "Error Title")
```

---

## Reference Files

| File | Contents |
|------|----------|
| [patterns.md](references/patterns.md) | Detailed error handling patterns |
| [examples.md](references/examples.md) | Complete working examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes to avoid |

---

## See Also

- `erpnext-api-patterns` - API implementation patterns
- `erpnext-syntax-whitelisted` - Whitelisted method syntax
- `erpnext-errors-serverscripts` - Server Script error handling
