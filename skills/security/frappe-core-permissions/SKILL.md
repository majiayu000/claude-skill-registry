---
name: frappe-core-permissions
description: >
  Use when implementing the Frappe/ERPNext permission system. Covers roles,
  user permissions, perm levels, data masking, and permission hooks for
  v14/v15/v16. Prevents common access control mistakes and security issues.
  Keywords: permissions, roles, user permissions, perm levels, data masking,
  access control, security, has_permission.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Permissions

> Deterministic patterns for the five-layer Frappe permission system.

---

## Permission Layers

| Layer | Controls | Configured Via | Version |
|-------|----------|----------------|---------|
| **Role Permissions** | What users CAN do | DocType permissions table | All |
| **User Permissions** | WHICH records users see | User Permission DocType | All |
| **Perm Levels** | WHICH fields users see/edit | Field `permlevel` property | All |
| **Permission Hooks** | Custom deny logic | `hooks.py` | All |
| **Data Masking** | Masked field values | Field `mask` property | [v16+] |

---

## Decision Tree

```
Need to control access?
├── Who can Create/Read/Write/Delete a DocType? → Role Permissions
├── Which specific records can a user see? → User Permissions
├── Which fields should be hidden? → Perm Levels (permlevel 1+)
├── Which fields show masked values? → Data Masking [v16+]
├── Custom runtime deny logic? → has_permission hook
├── Filter list queries dynamically? → permission_query_conditions hook
└── Share one document with one user? → frappe.share

Checking permissions in code?
├── Before action → frappe.has_permission() or doc.has_permission()
├── Raise on denial → doc.check_permission() or throw=True
├── System bypass → doc.flags.ignore_permissions = True (ALWAYS document why)
└── List query → ALWAYS use frappe.get_list() for user-facing data
```

---

## Permission Types

| Type | API Check | Applies To |
|------|-----------|------------|
| `read` | `frappe.has_permission(dt, "read")` | All DocTypes |
| `write` | `frappe.has_permission(dt, "write")` | All DocTypes |
| `create` | `frappe.has_permission(dt, "create")` | All DocTypes |
| `delete` | `frappe.has_permission(dt, "delete")` | All DocTypes |
| `submit` | `frappe.has_permission(dt, "submit")` | Submittable only |
| `cancel` | `frappe.has_permission(dt, "cancel")` | Submittable only |
| `amend` | `frappe.has_permission(dt, "amend")` | Submittable only |
| `select` | `frappe.has_permission(dt, "select")` | Link fields [v14+] |
| `report` | N/A | Report Builder access |
| `export` | N/A | Excel/CSV export |
| `import` | N/A | Data Import Tool |
| `share` | N/A | Share with other users |
| `print` | N/A | Print/PDF generation |
| `email` | N/A | Send email |
| `mask` | Role permission for unmasked view | Data Masking [v16+] |

---

## Automatic Roles

| Role | Assigned To | Notes |
|------|-------------|-------|
| `Guest` | Everyone (including anonymous) | Public pages |
| `All` | All registered users | Basic authenticated access |
| `Administrator` | Only the Administrator user | ALWAYS has all permissions |
| `Desk User` | System Users only | [v15+] |

---

## Essential API

### Check Permission

```python
# DocType-level
frappe.has_permission("Sales Order", "write")

# Document-level (by name or object)
frappe.has_permission("Sales Order", "write", "SO-00001")
frappe.has_permission("Sales Order", "write", doc=doc)

# For specific user
frappe.has_permission("Sales Order", "read", user="john@example.com")

# Throw on denial
frappe.has_permission("Sales Order", "delete", throw=True)

# Debug mode — prints evaluation steps
frappe.has_permission("Sales Order", "read", debug=True)
print(frappe.local.permission_debug_log)
```

### Document Instance Methods

```python
doc = frappe.get_doc("Sales Order", "SO-00001")

# Returns bool
if doc.has_permission("write"):
    doc.status = "Approved"
    doc.save()

# Raises frappe.PermissionError if denied
doc.check_permission("write")
```

### Get Effective Permissions

```python
from frappe.permissions import get_doc_permissions

perms = get_doc_permissions(doc)
# {'read': 1, 'write': 1, 'create': 0, 'delete': 0, ...}

perms = get_doc_permissions(doc, user="john@example.com")
```

---

## User Permissions (Record-Level)

Restrict users to specific Link field values (e.g., specific Company, Territory).

```python
from frappe.permissions import add_user_permission, remove_user_permission

# Restrict user to one company
add_user_permission(
    doctype="Company",
    name="My Company",
    user="john@example.com",
    is_default=1,            # auto-fill in new documents
    applicable_for="Sales Order"  # only for this DocType (optional)
)

# Remove restriction
remove_user_permission("Company", "My Company", "john@example.com")

# Query current restrictions
from frappe.permissions import get_user_permissions
perms = get_user_permissions("john@example.com")
# {"Company": [{"doc": "My Company", "is_default": 1}], ...}
```

---

## Sharing (Document-Level)

Grant access to a single document for a specific user.

```python
from frappe.share import add as add_share, remove as remove_share

add_share("Sales Order", "SO-00001", "jane@example.com",
          read=1, write=1, share=0, notify=1)

remove_share("Sales Order", "SO-00001", "jane@example.com")

# Share with everyone
add_share("Sales Order", "SO-00001", everyone=1, read=1)
```

---

## Field-Level Permissions (Perm Levels)

Group fields by `permlevel` (0-9). Level 0 MUST be granted before higher levels.

```json
{
  "fields": [
    {"fieldname": "employee_name", "permlevel": 0},
    {"fieldname": "salary",        "permlevel": 1}
  ],
  "permissions": [
    {"role": "Employee",   "permlevel": 0, "read": 1},
    {"role": "HR Manager", "permlevel": 0, "read": 1, "write": 1},
    {"role": "HR Manager", "permlevel": 1, "read": 1, "write": 1}
  ]
}
```

**Rule**: Levels do NOT imply hierarchy. Level 2 is not "higher" than level 1. They are independent field groups.

---

## Data Masking [v16+]

Fields with `mask=1` show masked values (e.g., `****`, `+91-811XXXXXXX`) to users without `mask` permission.

```json
{
  "fieldname": "phone_number", "fieldtype": "Data", "mask": 1
}
```

Grant `mask` permission to roles that MUST see unmasked values:

```json
{"role": "HR Manager", "permlevel": 0, "read": 1, "mask": 1}
```

**CRITICAL**: Data masking does NOT apply to `frappe.db.sql()` or Query Reports with raw SQL. You MUST mask manually in custom SQL queries.

---

## Permission Hooks

### has_permission — Custom Deny Logic

Can only **deny** access. NEVER returns `True` to grant. ALWAYS returns `None` to continue standard checks.

```python
# hooks.py
has_permission = {
    "Sales Order": "myapp.permissions.check_order_permission"
}
```

```python
# myapp/permissions.py
def check_order_permission(doc, ptype, user):
    if ptype == "write" and doc.docstatus == 2:
        if "Sales Manager" not in frappe.get_roles(user):
            return False
    return None  # ALWAYS return None by default
```

### permission_query_conditions — Filter List Queries

Returns SQL WHERE clause fragment. Only affects `get_list()`, NOT `get_all()`.

```python
# hooks.py
permission_query_conditions = {
    "Customer": "myapp.permissions.customer_query"
}
```

```python
def customer_query(user):
    if not user:
        user = frappe.session.user
    if "Sales Manager" in frappe.get_roles(user):
        return ""
    return f"`tabCustomer`.owner = {frappe.db.escape(user)}"
```

**ALWAYS** use `frappe.db.escape()` — NEVER use string concatenation with raw user input.

---

## get_list vs get_all

| Method | User Permissions | Query Hook | Use For |
|--------|------------------|------------|---------|
| `frappe.get_list()` | Applied | Applied | User-facing queries |
| `frappe.get_all()` | Ignored | Ignored | System/background queries |

**ALWAYS** use `get_list()` when returning data to users. `get_all()` bypasses ALL permission filtering.

---

## Common Patterns

### Owner-Only Edit

```json
{"role": "Sales User", "read": 1, "write": 1, "create": 1, "if_owner": 1}
```

### Role-Restricted Endpoint

```python
@frappe.whitelist()
def sensitive_action():
    frappe.only_for(["Manager", "Administrator"])
    # Only reaches here if user has one of these roles
```

### Bypass Permissions (Document Why!)

```python
# On document — ALWAYS add a comment explaining the reason
doc.flags.ignore_permissions = True
doc.save()

# On method call
doc.save(ignore_permissions=True)
doc.insert(ignore_permissions=True)
```

---

## Critical Rules

1. **ALWAYS** use `frappe.has_permission()` — NEVER check roles directly for access control
2. **ALWAYS** use `frappe.get_list()` for user-facing queries — NEVER `get_all()`
3. **ALWAYS** escape SQL in query hooks — `frappe.db.escape(user)`
4. **ALWAYS** prefix table names in query hooks — `` `tabDocType`.fieldname ``
5. **ALWAYS** return `None` in `has_permission` hooks by default — NEVER `True`
6. **ALWAYS** clear cache after permission changes — `frappe.clear_cache()`
7. **ALWAYS** document `ignore_permissions` usage with a comment
8. **NEVER** throw errors in `has_permission` hooks — return `False` to deny
9. **NEVER** grant permlevel 1+ without granting permlevel 0 first
10. **NEVER** assume data masking applies to custom SQL queries [v16+]

---

## Anti-Patterns

| Do NOT | Do Instead |
|--------|------------|
| `if "Role" in frappe.get_roles()` for access | `frappe.has_permission(dt, ptype)` |
| `frappe.get_all()` for user queries | `frappe.get_list()` |
| `return True` in has_permission hook | `return None` |
| `f"owner = '{user}'"` in SQL | `f"owner = {frappe.db.escape(user)}"` |
| `frappe.throw()` in permission hooks | `return False` |
| `frappe.db.set_value()` for user-facing updates | `doc.save()` with permission check |
| Sensitive data in error messages | Generic `frappe.PermissionError` |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| `select` permission | Yes | Yes | Yes |
| `Desk User` role | No | Yes | Yes |
| Data Masking (`mask` field) | No | No | Yes |
| `mask` permission type | No | No | Yes |
| Custom Permission Types | No | No | Experimental |

---

## Permission Precedence

1. **Administrator** — ALWAYS has all permissions (cannot be restricted)
2. **Role Permissions** — Based on assigned roles
3. **User Permissions** — Restricts to specific document values
4. **has_permission hook** — Can only deny (any `False` = denied)
5. **Sharing** — Grants access to shared documents
6. **if_owner** — Further restricts to owned documents

---

## Reference Files

| File | Contents |
|------|----------|
| [permission-types-reference.md](references/permission-types-reference.md) | All permission types with options |
| [permission-api-reference.md](references/permission-api-reference.md) | Complete API with all signatures |
| [permission-hooks-reference.md](references/permission-hooks-reference.md) | Hook patterns and examples |
| [examples.md](references/examples.md) | Working implementation examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes and fixes |

## Related Skills

- `frappe-core-database` — Database operations that respect permissions
- `frappe-core-api` — API endpoints with permission checks
- `frappe-syntax-controllers` — Controller permission validation
- `frappe-syntax-hooks` — Hook configuration patterns

---

*Verified against Frappe docs 2026-03-20 | Frappe v14/v15/v16*
