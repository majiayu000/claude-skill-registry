---
name: frappe-errors-permissions
description: >
  Use when debugging or handling permission errors in Frappe/ERPNext.
  Prevents broken document access from throwing in permission hooks.
  Covers PermissionError (403), has_permission hook failures, User Permission
  restricting too much or too little, perm_level blocking field access,
  System Manager bypass not working, Guest access denied, sharing permissions
  not applying, permission_query_conditions breaking get_list, owner-based
  permissions confusion, Apply User Permission checkbox behavior, and the
  permission debug workflow using frappe.permissions.get_doc_permissions.
  Keywords: PermissionError, has_permission, permission_query_conditions,
  User Permission, perm_level, sharing, guest access, owner permission.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Permission Error Handling

For permission system overview see `frappe-core-permissions`. For hook syntax see `frappe-syntax-hooks`.

---

## Quick Diagnostic: Error Message -> Cause -> Fix

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `frappe.exceptions.PermissionError` | User lacks role or doc-level access | Add role in Role Permissions Manager or grant User Permission |
| "Not permitted" on document open | `has_permission` hook returns False or role missing read | Check `frappe.permissions.get_doc_permissions(doc, user)` output |
| List view shows 0 records | `permission_query_conditions` returns overly restrictive SQL | Debug the SQL condition; check User Permissions for the Link field |
| "Not allowed to access ... for Guest" | Endpoint missing `allow_guest=True` or DocType lacks Guest read | Add `allow_guest=True` to `@frappe.whitelist()` |
| Field invisible despite role having read | `perm_level` > 0 on field and role lacks that level | Add role permission row for the specific `perm_level` |
| "User Permission restriction" blocking | User Permission on a Link field auto-filters documents | Uncheck "Apply User Permissions" on that role row or add matching User Permission |
| Sharing not granting access | Sharing adds access but never overrides role absence | User MUST have base role permission; sharing only adds doc-level grants |
| `ignore_permissions` has no effect | Flag set after `get_doc` already checked permissions | Set `flags.ignore_permissions = True` BEFORE calling `save()` or `insert()` |
| System Manager cannot access | Custom `has_permission` hook denies without checking role | ALWAYS check for System Manager / Administrator in hook |

---

## Decision Tree: Where Is the Error?

```
Permission error occurred
├── Document-level (single doc access)?
│   ├── has_permission hook returning False?
│   │   └── Debug: frappe.permissions.get_doc_permissions(doc, user)
│   ├── User Permission restricting Link field?
│   │   └── Check: frappe.get_all("User Permission", filters={"user": user})
│   ├── perm_level blocking field?
│   │   └── Check: role has permission row for that perm_level
│   └── Sharing not applying?
│       └── Check: user has base role + sharing record exists
├── List-level (0 records in list view)?
│   ├── permission_query_conditions returning bad SQL?
│   │   └── Debug: run condition manually in MariaDB console
│   ├── User Permission auto-filtering?
│   │   └── Check "Apply User Permissions" checkbox on role row
│   └── get_all vs get_list confusion?
│       └── ALWAYS use get_list for user-facing queries
├── API endpoint (403 response)?
│   ├── Missing @frappe.whitelist()?
│   │   └── Add decorator to Python method
│   ├── Missing allow_guest=True?
│   │   └── Add allow_guest parameter for public endpoints
│   └── frappe.only_for() blocking?
│       └── Check user has required role
└── System Manager bypass failing?
    └── Custom hook does not check for System Manager role
```

---

## Permission Hook Errors

### has_permission Hook — NEVER Throw

```python
# hooks.py
has_permission = {
    "Sales Order": "myapp.permissions.sales_order_has_permission",
}
```

```python
# WRONG — Breaks ALL document access
def sales_order_has_permission(doc, user, permission_type):
    if doc.status == "Locked":
        frappe.throw("Locked")  # NEVER do this

# CORRECT — Return False to deny, None to defer
def sales_order_has_permission(doc, user, permission_type):
    """
    ALWAYS wrap in try/except. NEVER throw. NEVER return True.
    Returns: False (deny) or None (defer to standard system).
    """
    try:
        user = user or frappe.session.user
        if user == "Administrator":
            return None

        # ALWAYS check System Manager early
        if "System Manager" in frappe.get_roles(user):
            return None

        # Deny write on locked docs (but allow read)
        if permission_type in ("write", "delete", "cancel"):
            if doc.get("status") == "Locked":
                return False

        return None  # Defer to standard permission system

    except Exception:
        frappe.log_error(frappe.get_traceback(),
            f"has_permission error: {getattr(doc, 'name', 'unknown')}")
        return None  # Safe fallback — defer
```

**Critical rules for has_permission hooks:**
- ALWAYS return `None` to defer, `False` to deny. NEVER return `True` — hooks can only restrict, not grant.
- ALWAYS wrap the entire function in `try/except`. An unhandled exception breaks ALL access to that DocType.
- ALWAYS check for `Administrator` and `System Manager` at the top.
- NEVER call `frappe.throw()` inside this hook.

### permission_query_conditions — NEVER Throw

```python
# hooks.py
permission_query_conditions = {
    "Sales Order": "myapp.permissions.sales_order_query",
}
```

```python
# WRONG — Breaks list view for all users
def sales_order_query(user):
    if not user:
        frappe.throw("User required")  # NEVER do this
    return f"owner = '{user}'"  # SQL injection!

# CORRECT — Return SQL string or empty string
def sales_order_query(user):
    """
    ALWAYS return a string. Empty string = no restriction.
    ALWAYS use frappe.db.escape(). ALWAYS wrap in try/except.
    """
    try:
        user = user or frappe.session.user
        if user == "Administrator":
            return ""
        if "System Manager" in frappe.get_roles(user):
            return ""

        return f"`tabSales Order`.owner = {frappe.db.escape(user)}"

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Query conditions error")
        # SAFE FALLBACK: most restrictive
        return f"`tabSales Order`.owner = {frappe.db.escape(frappe.session.user)}"
```

**Critical rules for permission_query_conditions:**
- NEVER throw errors — return `"1=0"` to deny all or a restrictive SQL string.
- ALWAYS use `frappe.db.escape()` for every user-supplied value.
- This hook ONLY affects `frappe.get_list()` / `frappe.db.get_list()`. It does NOT affect `frappe.get_all()` / `frappe.db.get_all()`.

---

## User Permission Errors

### Too Restrictive — Records Disappear

```
Error: User can't see any Sales Orders despite having Sales User role.
Cause: A User Permission for "Company" exists, and "Apply User Permissions"
       is checked on the Sales Order role row. Sales Order has a Company
       Link field, so ALL Sales Orders are filtered by that Company value.
```

**Debug steps:**
```python
# Step 1: Check what User Permissions exist
frappe.get_all("User Permission",
    filters={"user": "john@example.com"},
    fields=["allow", "for_value", "applicable_for"])

# Step 2: Check if Apply User Permissions is checked
frappe.get_all("DocPerm",
    filters={"parent": "Sales Order", "role": "Sales User"},
    fields=["role", "permlevel", "apply_user_permissions"])  # [v14]

# Step 3: Check effective permissions on a specific doc
from frappe.permissions import get_doc_permissions
perms = get_doc_permissions(frappe.get_doc("Sales Order", "SO-001"), "john@example.com")
```

**Fix patterns:**
- Remove overly broad User Permissions that filter unintended DocTypes.
- Use the `applicable_for` field [v14+] to limit which DocType a User Permission applies to.
- Uncheck "Apply User Permissions" on the role permission row if blanket filtering is unwanted.

### Too Permissive — User Sees Everything

```
Error: User Permission set for Territory = "North" but user sees all territories.
Cause: "Apply User Permissions" is NOT checked on the role permission row,
       or the DocType has no Link field for Territory.
```

**Fix:** Ensure the role permission row has "Apply User Permissions" checked AND the DocType has a Link field to the restricted DocType.

---

## perm_level Errors

```
Error: Field "cost_center" is invisible despite user having read permission.
Cause: Field has permlevel=1 but role only has permission for permlevel=0.
```

```python
# Check which perm_levels a role has access to
frappe.get_all("DocPerm",
    filters={"parent": "Sales Invoice", "role": "Accounts User"},
    fields=["permlevel", "read", "write"])
```

**Fix:** Add a new row in the DocType's Permission table for the role at the required `permlevel`.

---

## Sharing Permission Errors

```
Error: Document shared with user but user still gets PermissionError.
Cause: User has NO base role permission on the DocType. Sharing only
       supplements — it never replaces role-based permissions.
```

```python
# Share a document (user MUST already have a role with at least read)
frappe.share.add("Sales Order", "SO-001", "john@example.com",
    read=1, write=1, share=1)

# Check if sharing grants access
frappe.share.get_sharing_permissions("Sales Order", "SO-001", "john@example.com")
```

**Rules:**
- ALWAYS ensure the user has at least one role with read permission on the DocType before sharing.
- Sharing adds document-level grants on top of role permissions.
- [v15+] `frappe.share.add` accepts `notify=1` to send email notification.

---

## Guest Access Errors

```
Error: "Not permitted" for unauthenticated users.
Cause: DocType has no Guest read permission, or API missing allow_guest.
```

**Fix for web pages / portal:**
```python
# Add Guest read permission in DocType Permission table
# Role: Guest, Level: 0, Read: checked
```

**Fix for API endpoints:**
```python
@frappe.whitelist(allow_guest=True)
def public_endpoint():
    # ALWAYS validate input — guest endpoints are exposed to the internet
    pass
```

**NEVER grant Guest write/create/delete permissions** unless the DocType is specifically designed for public submission (e.g., Web Form backend).

---

## Debug Workflow: frappe.permissions

```python
import frappe
from frappe.permissions import get_doc_permissions

# Get all effective permissions for a user on a document
doc = frappe.get_doc("Sales Order", "SO-001")
perms = get_doc_permissions(doc, user="john@example.com")
# Returns dict: {"read": 1, "write": 0, "create": 0, ...}

# Check specific permission with full context
frappe.has_permission("Sales Order", ptype="write",
    doc="SO-001", user="john@example.com", throw=False)

# List all roles for a user
frappe.get_roles("john@example.com")

# Check User Permissions
frappe.get_all("User Permission",
    filters={"user": "john@example.com"},
    fields=["allow", "for_value", "applicable_for", "is_default"])
```

---

## Critical Rules

### ALWAYS
1. **Wrap permission hooks in try/except** — unhandled errors break all access
2. **Return None (not True) in has_permission** — hooks can only deny
3. **Use frappe.db.escape() in query conditions** — prevent SQL injection
4. **Check System Manager / Administrator first** in custom hooks
5. **Use frappe.has_permission(throw=True)** for endpoint permission checks
6. **Use get_list (not get_all)** for user-facing queries — get_all bypasses permissions
7. **Log permission denials** for security audit with `frappe.log_error()`

### NEVER
1. **Throw in has_permission or permission_query_conditions** — breaks access entirely
2. **Return True in has_permission** — has no effect, hooks can only restrict
3. **Use string formatting for SQL** — use `frappe.db.escape()` to prevent injection
4. **Grant Guest write/delete permissions** — security risk
5. **Use ignore_permissions without documenting why** — creates audit gaps
6. **Assume sharing replaces role permissions** — sharing only supplements

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete hook patterns, query conditions, API endpoints |
| `references/examples.md` | Full working examples with hooks.py configuration |
| `references/anti-patterns.md` | 15 common mistakes with wrong/correct comparisons |

---

## See Also

- `frappe-core-permissions` — Permission system architecture
- `frappe-errors-api` — API error handling (401/403/404)
- `frappe-errors-hooks` — Hook error handling patterns
- `frappe-syntax-hooks` — Hook registration syntax
