---
name: erpnext-permissions
description: Complete guide for Frappe/ERPNext permission system - roles, user permissions, perm levels, data masking, and permission hooks
version: 1.1.0
author: OpenAEC Foundation
tags: [erpnext, frappe, permissions, security, roles, access-control, data-masking]
frameworks: [frappe-14, frappe-15, frappe-16]
---

# ERPNext Permissions Skill

> Deterministic patterns for implementing robust permission systems in Frappe/ERPNext applications.

---

## Overview

Frappe's permission system has five layers:

| Layer | Controls | Configured Via | Version |
|-------|----------|----------------|---------|
| **Role Permissions** | What users CAN do | DocType permissions table | All |
| **User Permissions** | WHICH documents users see | User Permission records | All |
| **Perm Levels** | WHICH fields users see | Field permlevel property | All |
| **Permission Hooks** | Custom logic | hooks.py | All |
| **Data Masking** | MASKED field values | Field mask property | v16+ |

---

## Quick Reference

### Permission Types

| Type | Check | For |
|------|-------|-----|
| `read` | `frappe.has_permission(dt, "read")` | View document |
| `write` | `frappe.has_permission(dt, "write")` | Edit document |
| `create` | `frappe.has_permission(dt, "create")` | Create new |
| `delete` | `frappe.has_permission(dt, "delete")` | Delete |
| `submit` | `frappe.has_permission(dt, "submit")` | Submit (submittable only) |
| `cancel` | `frappe.has_permission(dt, "cancel")` | Cancel |
| `select` | `frappe.has_permission(dt, "select")` | Select in Link (v14+) |
| `mask` | Role permission for unmasked view | View unmasked data (v16+) |

### Automatic Roles

| Role | Assigned To |
|------|-------------|
| `Guest` | Everyone (including anonymous) |
| `All` | All registered users |
| `Administrator` | Only Administrator user |
| `Desk User` | System Users (v15+) |

---

## Essential API

### Check Permission

```python
# DocType level
frappe.has_permission("Sales Order", "write")

# Document level
frappe.has_permission("Sales Order", "write", "SO-00001")
frappe.has_permission("Sales Order", "write", doc=doc)

# For specific user
frappe.has_permission("Sales Order", "read", user="john@example.com")

# Throw on denial
frappe.has_permission("Sales Order", "delete", throw=True)

# On document instance
doc = frappe.get_doc("Sales Order", "SO-00001")
if doc.has_permission("write"):
    doc.status = "Approved"
    doc.save()

# Raise error if no permission
doc.check_permission("write")
```

### Get Permissions

```python
from frappe.permissions import get_doc_permissions

# Get all permissions for document
perms = get_doc_permissions(doc)
# {'read': 1, 'write': 1, 'create': 0, 'delete': 0, ...}
```

### User Permissions

```python
from frappe.permissions import add_user_permission, remove_user_permission

# Restrict user to specific company
add_user_permission(
    doctype="Company",
    name="My Company",
    user="john@example.com",
    is_default=1
)

# Remove restriction
remove_user_permission("Company", "My Company", "john@example.com")

# Get user's permissions
from frappe.permissions import get_user_permissions
perms = get_user_permissions("john@example.com")
```

### Sharing

```python
from frappe.share import add as add_share

# Share document with user
add_share(
    doctype="Sales Order",
    name="SO-00001",
    user="jane@example.com",
    read=1,
    write=1
)
```

---

## Data Masking (v16+)

Data Masking protects sensitive field values while keeping fields visible. Users without `mask` permission see masked values (e.g., `****`, `+91-811XXXXXXX`).

### Use Cases

- HR: Show employee details but mask salary amounts
- Support: Show phone numbers partially masked
- Finance: Show bank account fields without full numbers

### Enable Data Masking

**Via DocType (Developer Mode) or Customize Form:**

```json
{
  "fieldname": "phone_number",
  "fieldtype": "Data",
  "options": "Phone",
  "mask": 1
}
```

**Supported Field Types:**
- Data, Date, Datetime
- Currency, Float, Int, Percent
- Phone, Password
- Link, Dynamic Link
- Select, Read Only, Duration

### Configure Permission

Add `mask` permission to roles that should see unmasked data:

```json
{
  "permissions": [
    {"role": "Employee", "permlevel": 0, "read": 1},
    {"role": "HR Manager", "permlevel": 0, "read": 1, "mask": 1}
  ]
}
```

### How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│ DATA MASKING FLOW                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Field has mask=1 in DocField configuration                      │
│                                                                     │
│  2. System checks: meta.has_permlevel_access_to(                    │
│        fieldname=df.fieldname,                                      │
│        df=df,                                                       │
│        permission_type="mask"                                       │
│     )                                                               │
│                                                                     │
│  3. If user LACKS mask permission:                                  │
│     └─► Value automatically masked in:                              │
│         • Form views                                                │
│         • List views                                                │
│         • Report views                                              │
│         • API responses (/api/resource/, /api/method/)              │
│                                                                     │
│  4. If user HAS mask permission:                                    │
│     └─► Full value displayed                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Critical: Custom SQL Queries

**Data Masking does NOT apply to:**
- Custom SQL queries
- Query Reports using raw SQL
- Direct `frappe.db.sql()` calls

**You must implement masking manually:**

```python
def get_customer_report(filters):
    data = frappe.db.sql("""
        SELECT name, phone, email FROM tabCustomer
    """, as_dict=True)
    
    # Manual masking for users without permission
    if not frappe.has_permission("Customer", "mask"):
        for row in data:
            if row.phone:
                row.phone = mask_phone(row.phone)
    
    return data

def mask_phone(phone):
    """Mask phone number: +91-81123XXXXX"""
    if len(phone) > 5:
        return phone[:6] + "X" * (len(phone) - 6)
    return "****"
```

---

## Permission Hooks

### has_permission Hook

Add custom permission logic. Can only **deny**, not grant.

```python
# hooks.py
has_permission = {
    "Sales Order": "myapp.permissions.check_order_permission"
}
```

```python
# myapp/permissions.py
def check_order_permission(doc, ptype, user):
    """
    Returns:
        None: Continue standard checks
        False: Deny permission
    """
    # Deny editing cancelled orders for non-managers
    if ptype == "write" and doc.docstatus == 2:
        if "Sales Manager" not in frappe.get_roles(user):
            return False
    
    return None  # ALWAYS return None by default
```

### permission_query_conditions Hook

Filter list queries. Only affects `get_list()`, NOT `get_all()`.

```python
# hooks.py
permission_query_conditions = {
    "Customer": "myapp.permissions.customer_query"
}
```

```python
# myapp/permissions.py
def customer_query(user):
    """Return SQL WHERE clause fragment."""
    if not user:
        user = frappe.session.user
    
    # Managers see all
    if "Sales Manager" in frappe.get_roles(user):
        return ""
    
    # Others see only their customers
    return f"`tabCustomer`.owner = {frappe.db.escape(user)}"
```

**CRITICAL**: Always use `frappe.db.escape()` - never string concatenation!

---

## get_list vs get_all

| Method | User Permissions | Query Hook |
|--------|------------------|------------|
| `frappe.get_list()` | ✅ Applied | ✅ Applied |
| `frappe.get_all()` | ❌ Ignored | ❌ Ignored |

```python
# User-facing query - respects permissions
docs = frappe.get_list("Sales Order", filters={"status": "Open"})

# System query - bypasses permissions
docs = frappe.get_all("Sales Order", filters={"status": "Open"})
```

---

## Field-Level Permissions (Perm Levels)

### Configure Field

```json
{
  "fieldname": "salary",
  "fieldtype": "Currency",
  "permlevel": 1
}
```

### Configure Role Access

```json
{
  "permissions": [
    {"role": "Employee", "permlevel": 0, "read": 1},
    {"role": "HR Manager", "permlevel": 0, "read": 1, "write": 1},
    {"role": "HR Manager", "permlevel": 1, "read": 1, "write": 1}
  ]
}
```

**Rule**: Level 0 MUST be granted before higher levels.

---

## Decision Tree

```
Need to control access?
├── To entire DocType → Role Permissions
├── To specific documents → User Permissions
├── To specific fields (hide completely) → Perm Levels
├── To specific fields (show masked) → Data Masking (v16+)
├── With custom logic → has_permission hook
└── For list queries → permission_query_conditions hook

Checking permissions in code?
├── Before action → frappe.has_permission() or doc.has_permission()
├── Raise error → doc.check_permission() or throw=True
└── Bypass needed → doc.flags.ignore_permissions = True (document why!)
```

---

## Common Patterns

### Owner-Only Edit

```json
{
  "role": "Sales User",
  "read": 1, "write": 1, "create": 1,
  "if_owner": 1
}
```

### Check Before Action

```python
@frappe.whitelist()
def approve_order(order_name):
    doc = frappe.get_doc("Sales Order", order_name)
    
    if not doc.has_permission("write"):
        frappe.throw(_("No permission"), frappe.PermissionError)
    
    doc.status = "Approved"
    doc.save()
```

### Role-Restricted Endpoint

```python
@frappe.whitelist()
def sensitive_action():
    frappe.only_for(["Manager", "Administrator"])
    # Only reaches here if user has role
```

---

## Critical Rules

1. **ALWAYS use permission API** - Not role checks
2. **ALWAYS escape SQL** - `frappe.db.escape(user)`
3. **ALWAYS use get_list** - For user-facing queries
4. **ALWAYS return None** - In has_permission hooks (not True)
5. **ALWAYS document** - When using ignore_permissions
6. **ALWAYS clear cache** - After permission changes: `frappe.clear_cache()`
7. **ALWAYS mask manually** - In custom SQL queries (v16+)

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `if "Role" in frappe.get_roles()` | `frappe.has_permission(dt, ptype)` |
| `frappe.get_all()` for user queries | `frappe.get_list()` |
| `return True` in has_permission | `return None` |
| `f"owner = '{user}'"` | `f"owner = {frappe.db.escape(user)}"` |
| `frappe.throw()` in hooks | `return False` |
| Assume masking in custom SQL | Implement masking manually |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| `select` permission | ✅ | ✅ | ✅ |
| `Desk User` role | ❌ | ✅ | ✅ |
| Custom Permission Types | ❌ | ❌ | ✅ (experimental) |
| **Data Masking** | ❌ | ❌ | ✅ |
| `mask` permission type | ❌ | ❌ | ✅ |

---

## Debugging

```python
# Enable debug output
frappe.has_permission("Sales Order", "read", doc, debug=True)

# View logs
print(frappe.local.permission_debug_log)

# Check user's effective permissions
from frappe.permissions import get_doc_permissions
perms = get_doc_permissions(doc, user="john@example.com")
```

---

## Reference Files

See `references/` folder for:
- `permission-types-reference.md` - All permission types
- `permission-api-reference.md` - Complete API reference
- `permission-hooks-reference.md` - Hook patterns
- `examples.md` - Working examples
- `anti-patterns.md` - Common mistakes

---

## Related Skills

- `erpnext-database` - Database operations that respect permissions
- `erpnext-syntax-controllers` - Controller permission checks
- `erpnext-syntax-hooks` - Hook configuration

---

*Last updated: 2026-01-18 | Frappe v14/v15/v16*
