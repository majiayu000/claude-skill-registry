---
name: erpnext-syntax-serverscripts
description: Complete syntax reference for Frappe Server Scripts. Use this skill when Claude needs to write Python code for Server Scripts in ERPNext/Frappe, including Document Events, API endpoints, Scheduler Events, and Permission Queries. Covers sandbox limitations, available frappe.* methods, event name mapping, and correct syntax for v14/v15/v16.
---

# ERPNext Server Scripts Syntax

Server Scripts are Python scripts that run within Frappe's secure sandbox environment. They are managed via **Setup → Server Script** in the ERPNext UI.

## CRITICAL: Sandbox Limitations

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  NO IMPORTS ALLOWED                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ The sandbox blocks ALL import statements:                          │
│   import json        → ImportError: __import__ not found           │
│   from datetime import date  → ImportError                         │
│                                                                     │
│ SOLUTION: Use Frappe's pre-loaded namespace:                       │
│   frappe.utils.nowdate()     not: from frappe.utils import nowdate │
│   frappe.parse_json(data)    not: import json; json.loads(data)    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Server Script Types

| Type | Usage | Trigger |
|------|-------|---------|
| **Document Event** | React to document lifecycle | Save, Submit, Cancel, etc. |
| **API** | Custom REST endpoint | HTTP request to `/api/method/{name}` |
| **Scheduler Event** | Scheduled tasks | Cron schedule |
| **Permission Query** | Dynamic list filtering | Document list view |

## Event Name Mapping (Document Event)

**IMPORTANT**: The UI event names differ from the internal hook names:

| UI Name (Server Script) | Internal Hook | When |
|-------------------------|---------------|------|
| Before Insert | `before_insert` | Before new doc to DB |
| After Insert | `after_insert` | After new doc saved |
| Before Validate | `before_validate` | Before validation |
| **Before Save** | **`validate`** | Before save (new or update) |
| After Save | `on_update` | After successful save |
| Before Submit | `before_submit` | Before submit |
| After Submit | `on_submit` | After submit |
| Before Cancel | `before_cancel` | Before cancel |
| After Cancel | `on_cancel` | After cancel |
| Before Delete | `on_trash` | Before delete |
| After Delete | `after_delete` | After delete |

## Quick Reference: Available API

### Always available in sandbox

```python
# Document object (in Document Event scripts)
doc                      # Current document
doc.name                 # Document name
doc.doctype              # DocType name
doc.fieldname            # Field value
doc.get("fieldname")     # Safe field access
doc.items                # Child table (list)

# Frappe namespace
frappe.db                # Database operations
frappe.get_doc()         # Fetch document
frappe.get_all()         # Multiple documents
frappe.throw()           # Validation error
frappe.msgprint()        # User message
frappe.log_error()       # Error logging
frappe.utils.*           # Utility functions
frappe.session.user      # Current user
frappe.form_dict         # Request parameters (API)
frappe.response          # Response object (API)
```

## Decision Tree: Which Script Type?

```
What do you want to achieve?
│
├─► React to document save/submit/cancel?
│   └─► Document Event script
│
├─► Create REST API endpoint?
│   └─► API script
│
├─► Run task on schedule?
│   └─► Scheduler Event script
│
└─► Filter document list view per user/role?
    └─► Permission Query script
```

## Basic Syntax per Type

### Document Event

```python
# Configuration:
#   Reference DocType: Sales Invoice
#   DocType Event: Before Save (= validate)

if doc.grand_total < 0:
    frappe.throw("Total cannot be negative")

if doc.grand_total > 10000:
    doc.requires_approval = 1
```

### API

```python
# Configuration:
#   API Method: get_customer_info
#   Allow Guest: No
# Endpoint: /api/method/get_customer_info

customer = frappe.form_dict.get("customer")
if not customer:
    frappe.throw("Customer parameter required")

data = frappe.get_all(
    "Sales Order",
    filters={"customer": customer, "docstatus": 1},
    fields=["name", "grand_total"],
    limit=10
)
frappe.response["message"] = data
```

### Scheduler Event

```python
# Configuration:
#   Event Frequency: Cron
#   Cron Format: 0 9 * * * (daily at 9:00)

overdue = frappe.get_all(
    "Sales Invoice",
    filters={"status": "Unpaid", "due_date": ["<", frappe.utils.today()]},
    fields=["name", "customer"]
)

for inv in overdue:
    frappe.log_error(f"Overdue: {inv.name}", "Invoice Reminder")

frappe.db.commit()
```

### Permission Query

```python
# Configuration:
#   Reference DocType: Sales Invoice
# Output: conditions string for WHERE clause

user_roles = frappe.get_roles(user)

if "System Manager" in user_roles:
    conditions = ""  # Full access
elif "Sales User" in user_roles:
    conditions = f"`tabSales Invoice`.owner = {frappe.db.escape(user)}"
else:
    conditions = "1=0"  # No access
```

## References

- **[references/events.md](references/events.md)** - Complete event mapping and execution order
- **[references/methods.md](references/methods.md)** - All available frappe.* methods in sandbox
- **[references/examples.md](references/examples.md)** - 10+ working examples per script type
- **[references/anti-patterns.md](references/anti-patterns.md)** - Sandbox limitations and common mistakes

## Version Information

- **Frappe v14+**: Server Scripts fully supported
- **Activation required**: `bench --site [site] set-config server_script_enabled true`
- **Frappe v15**: No significant syntax changes for Server Scripts
