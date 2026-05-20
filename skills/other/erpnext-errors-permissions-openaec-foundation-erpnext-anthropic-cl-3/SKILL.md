---
name: erpnext-errors-permissions
description: "Error handling patterns for ERPNext/Frappe permissions and access control. Use when handling PermissionError, has_permission failures, role issues, and document access problems. V14/V15/V16 compatible. Triggers: permission error, access denied, PermissionError, role error, has_permission failed, document access error."
---

# ERPNext Permissions - Error Handling

This skill covers error handling patterns for the Frappe permission system. For permission syntax, see `erpnext-permissions`. For hooks, see `erpnext-syntax-hooks`.

**Version**: v14/v15/v16 compatible

---

## Permission Error Handling Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ PERMISSION ERRORS REQUIRE SPECIAL HANDLING                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Permission Hooks (has_permission, permission_query_conditions):     │
│ ⚠️ NEVER throw errors - return False or empty string                │
│ ⚠️ Errors break document access and list views                      │
│ ⚠️ Always provide safe fallbacks                                    │
│                                                                     │
│ Permission Checks in Code:                                          │
│ ✅ Use frappe.has_permission() before operations                    │
│ ✅ Use throw=True for automatic error handling                      │
│ ✅ Catch frappe.PermissionError for custom handling                 │
│                                                                     │
│ API Endpoints:                                                      │
│ ✅ frappe.only_for() for role-restricted endpoints                  │
│ ✅ doc.has_permission() before document operations                  │
│ ✅ Return proper HTTP 403 for access denied                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Main Decision: Where Is the Permission Check?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHERE ARE YOU HANDLING PERMISSIONS?                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► has_permission hook (hooks.py)                                        │
│   └─► NEVER throw - return False to deny, None to defer                 │
│   └─► Wrap in try/except, log errors, return None on failure            │
│                                                                         │
│ ► permission_query_conditions hook (hooks.py)                           │
│   └─► NEVER throw - return SQL condition or empty string                │
│   └─► Wrap in try/except, return restrictive fallback on failure        │
│                                                                         │
│ ► Whitelisted method / API endpoint                                     │
│   └─► Use frappe.has_permission() with throw=True                       │
│   └─► Or catch PermissionError for custom response                      │
│   └─► Use frappe.only_for() for role-restricted endpoints               │
│                                                                         │
│ ► Controller method                                                     │
│   └─► Use doc.has_permission() or doc.check_permission()                │
│   └─► Let PermissionError propagate for standard handling               │
│                                                                         │
│ ► Client Script                                                         │
│   └─► Handle in frappe.call error callback                              │
│   └─► Check exc type for PermissionError                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Permission Hook Error Handling

### has_permission - NEVER Throw!

```python
# ❌ WRONG - Breaks document access!
def has_permission(doc, ptype, user):
    if doc.status == "Locked":
        frappe.throw("Document is locked")  # DON'T DO THIS!

# ✅ CORRECT - Return False to deny, None to defer
def has_permission(doc, ptype, user):
    """
    Custom permission check.
    
    Returns:
        None: Defer to standard permission system
        False: Deny permission
        
    NEVER return True - hooks can only deny, not grant.
    """
    try:
        user = user or frappe.session.user
        
        # Deny editing locked documents
        if ptype == "write" and doc.get("status") == "Locked":
            if "System Manager" not in frappe.get_roles(user):
                return False
        
        # Deny access to confidential documents
        if doc.get("is_confidential"):
            allowed_users = get_allowed_users(doc.name)
            if user not in allowed_users:
                return False
        
        # ALWAYS return None to defer to standard checks
        return None
        
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Permission check error: {doc.name if hasattr(doc, 'name') else 'unknown'}"
        )
        # Safe fallback - defer to standard system
        return None
```

### permission_query_conditions - NEVER Throw!

```python
# ❌ WRONG - Breaks list views!
def query_conditions(user):
    if not user:
        frappe.throw("User required")
    return f"owner = '{user}'"  # Also SQL injection!

# ✅ CORRECT - Return safe SQL condition
def query_conditions(user):
    """
    Return SQL WHERE clause fragment for list filtering.
    
    Returns:
        str: SQL condition (empty string for no restriction)
        
    NEVER throw errors - return restrictive fallback.
    """
    try:
        if not user:
            user = frappe.session.user
        
        roles = frappe.get_roles(user)
        
        # Admins see all
        if "System Manager" in roles:
            return ""
        
        # Managers see team records
        if "Sales Manager" in roles:
            team_users = get_team_users(user)
            if team_users:
                escaped = ", ".join([frappe.db.escape(u) for u in team_users])
                return f"`tabSales Order`.owner IN ({escaped})"
        
        # Default: own records only
        return f"`tabSales Order`.owner = {frappe.db.escape(user)}"
        
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Permission query error for {user}"
        )
        # SAFE FALLBACK: Most restrictive - own records only
        return f"`tabSales Order`.owner = {frappe.db.escape(frappe.session.user)}"
```

---

## Permission Check Error Handling

### Pattern 1: Check Before Action (Recommended)

```python
@frappe.whitelist()
def update_order_status(order_name, new_status):
    """Update order status with permission check."""
    # Check document exists
    if not frappe.db.exists("Sales Order", order_name):
        frappe.throw(
            _("Sales Order {0} not found").format(order_name),
            exc=frappe.DoesNotExistError
        )
    
    # Check permission - throws automatically
    frappe.has_permission("Sales Order", "write", order_name, throw=True)
    
    # Now safe to proceed
    frappe.db.set_value("Sales Order", order_name, "status", new_status)
    
    return {"status": "success"}
```

### Pattern 2: Custom Permission Error Response

```python
@frappe.whitelist()
def sensitive_operation(doc_name):
    """Operation with custom permission error handling."""
    try:
        doc = frappe.get_doc("Sensitive Doc", doc_name)
        doc.check_permission("write")
        
    except frappe.DoesNotExistError:
        frappe.throw(
            _("Document not found"),
            exc=frappe.DoesNotExistError
        )
        
    except frappe.PermissionError:
        # Log attempted access
        frappe.log_error(
            f"Unauthorized access attempt: {doc_name} by {frappe.session.user}",
            "Security Alert"
        )
        # Custom error message
        frappe.throw(
            _("You don't have permission to perform this action. This incident has been logged."),
            exc=frappe.PermissionError
        )
    
    # Proceed with operation
    return process_document(doc)
```

### Pattern 3: Role-Restricted Endpoint

```python
@frappe.whitelist()
def admin_dashboard_data():
    """Endpoint restricted to specific roles."""
    # This throws PermissionError if user lacks role
    frappe.only_for(["System Manager", "Dashboard Admin"])
    
    # Only reaches here if authorized
    return compile_dashboard_data()


@frappe.whitelist()
def manager_report():
    """Endpoint with graceful role check."""
    allowed_roles = ["Sales Manager", "General Manager", "System Manager"]
    user_roles = frappe.get_roles()
    
    if not any(role in user_roles for role in allowed_roles):
        frappe.throw(
            _("This report is only available to managers"),
            exc=frappe.PermissionError
        )
    
    return generate_report()
```

---

## Error Response Patterns

### Standard Permission Error

```python
# Uses frappe.PermissionError - returns HTTP 403
frappe.throw(
    _("You don't have permission to access this resource"),
    exc=frappe.PermissionError
)
```

### Permission Error with Context

```python
def check_access(doc):
    """Check access with helpful error message."""
    if not doc.has_permission("read"):
        owner_name = frappe.db.get_value("User", doc.owner, "full_name")
        frappe.throw(
            _("This document belongs to {0}. You can only view your own documents.").format(owner_name),
            exc=frappe.PermissionError
        )
```

### Soft Permission Denial (No Error)

```python
@frappe.whitelist()
def get_dashboard_widgets():
    """Return widgets based on user permissions."""
    widgets = []
    
    # Add widgets based on permissions
    if frappe.has_permission("Sales Order", "read"):
        widgets.append(get_sales_widget())
    
    if frappe.has_permission("Purchase Order", "read"):
        widgets.append(get_purchase_widget())
    
    if frappe.has_permission("Employee", "read"):
        widgets.append(get_hr_widget())
    
    # No error if no widgets - just return empty
    return widgets
```

---

## Client-Side Permission Error Handling

### JavaScript Error Handling

```javascript
// Handle permission errors in frappe.call
frappe.call({
    method: "myapp.api.sensitive_operation",
    args: { doc_name: "DOC-001" },
    callback: function(r) {
        if (r.message) {
            frappe.show_alert({
                message: __("Operation completed"),
                indicator: "green"
            });
        }
    },
    error: function(r) {
        // Check if it's a permission error
        if (r.exc_type === "PermissionError") {
            frappe.msgprint({
                title: __("Access Denied"),
                message: __("You don't have permission to perform this action."),
                indicator: "red"
            });
        } else {
            // Generic error handling
            frappe.msgprint({
                title: __("Error"),
                message: r.exc || __("An error occurred"),
                indicator: "red"
            });
        }
    }
});
```

### Permission Check Before Action

```javascript
// Check permission before showing button
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        // Only show button if user has write permission
        if (frm.doc.docstatus === 0 && frappe.perm.has_perm("Sales Order", 0, "write")) {
            frm.add_custom_button(__("Special Action"), function() {
                perform_special_action(frm);
            });
        }
    }
});

// Or use frappe.call to check server-side
frappe.call({
    method: "frappe.client.has_permission",
    args: {
        doctype: "Sales Order",
        docname: frm.doc.name,
        ptype: "write"
    },
    async: false,
    callback: function(r) {
        if (r.message) {
            // Has permission - show button
        }
    }
});
```

---

## Critical Rules

### ✅ ALWAYS

1. **Return None in has_permission hooks** - Never return True
2. **Use frappe.db.escape() in query conditions** - Prevent SQL injection
3. **Wrap hooks in try/except** - Errors break access entirely
4. **Log permission errors** - Security audit trail
5. **Use throw=True in permission checks** - Automatic error handling
6. **Provide helpful error messages** - Tell users what they can do

### ❌ NEVER

1. **Don't throw in permission hooks** - Return False instead
2. **Don't use string concatenation in SQL** - SQL injection risk
3. **Don't return True in has_permission** - Hooks can only deny
4. **Don't ignore permission errors** - Security risk
5. **Don't expose sensitive info in errors** - Security risk

---

## Quick Reference: Permission Error Handling

| Context | Error Method | Fallback |
|---------|--------------|----------|
| has_permission hook | Return False | Return None |
| permission_query_conditions | Return restrictive SQL | Own records filter |
| Whitelisted method | frappe.throw(exc=PermissionError) | N/A |
| Controller | doc.check_permission() | Let propagate |
| Client Script | error callback | Show user message |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns |
| `references/examples.md` | Full working examples |
| `references/anti-patterns.md` | Common mistakes to avoid |

---

## See Also

- `erpnext-permissions` - Permission system overview
- `erpnext-errors-hooks` - Hook error handling
- `erpnext-errors-api` - API error handling
- `erpnext-syntax-hooks` - Hook syntax
