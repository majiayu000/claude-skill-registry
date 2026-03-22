---
name: frappe-impl-serverscripts
description: >
  Use when implementing server-side features via Setup > Server Script:
  document validation, auto-fill, API endpoints, scheduled tasks,
  permission queries. Covers sandbox-safe coding, script type selection,
  testing, migration to controllers. Keywords: how to implement server
  script, which script type, sandbox limitation, Document Event, API
  script, Scheduler Event, Permission Query, migrate to controller.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Server Scripts — Implementation Workflows

Step-by-step workflows for building server-side features without a custom app. For exact syntax, see `frappe-syntax-serverscripts`.

**Version**: v14/v15/v16 | **v15+ Note**: Server Scripts disabled by default — enable with `bench set-config server_script_enabled true`

## CRITICAL: Sandbox Limitations

```
ALL IMPORTS BLOCKED — RestrictedPython sandbox
  import json          → ImportError: __import__ not found
  from frappe.utils    → ImportError
  import requests      → ImportError

SOLUTION: Use pre-loaded namespace:
  frappe.utils.nowdate()        frappe.utils.flt()
  frappe.parse_json(data)       json.loads() (json IS available)
  frappe.as_json(obj)           json.dumps()
  frappe.make_get_request(url)  (replaces requests.get)
```

**Rule**: If you need `import` statements beyond `json`, ALWAYS use a Controller instead.

## Workflow 1: Create a Server Script

1. Enable server scripts: `bench set-config server_script_enabled true`
2. Navigate to **Setup > Server Script** (or awesomebar: "New Server Script")
3. Select **Script Type** (see decision tree below)
4. Configure type-specific settings (DocType, event, API method, cron)
5. Write script in the editor
6. Save — script is active immediately
7. Test by triggering the configured event
8. Use "Compare Versions" button to diff changes

## Workflow 2: Choose the Script Type

```
WHAT DO YOU NEED?
│
├── React to document save/submit/cancel?
│   └── Document Event
│       └── Select DocType + Event (Before Save, After Save, etc.)
│
├── Create a REST API endpoint?
│   └── API
│       └── Set method name + guest access setting
│       └── Endpoint: /api/method/{method_name}
│
├── Run task on schedule (daily/hourly/cron)?
│   └── Scheduler Event
│       └── Set cron pattern or frequency
│
└── Filter list views per user/role?
    └── Permission Query
        └── Select DocType — set `conditions` variable
```

> See [references/decision-tree.md](references/decision-tree.md) for complete decision tree.

## Workflow 3: Document Event — Validation

**Goal**: Validate Sales Order before save.

**Step 1**: Choose event — "Before Save" maps to `validate` hook.

**Step 2**: Write sandbox-safe script:

```python
# Type: Document Event | Event: Before Save | DocType: Sales Order

errors = []

if not doc.customer:
    errors.append("Customer is required")

if doc.delivery_date and doc.delivery_date < frappe.utils.today():
    errors.append("Delivery date cannot be in the past")

for item in doc.items:
    if item.qty <= 0:
        errors.append(f"Row {item.idx}: Quantity must be positive")

if errors:
    frappe.throw("<br>".join(errors), title="Validation Error")
```

**Rules**:
- ALWAYS collect errors and throw once (better UX than multiple throws)
- NEVER call `doc.save()` in Before Save — framework handles it
- ALWAYS use `frappe.throw()` — `msgprint` does NOT stop save

## Workflow 4: Document Event — Auto-Calculate

**Goal**: Auto-calculate totals and set derived fields.

```python
# Type: Document Event | Event: Before Save | DocType: Purchase Order

doc.total_qty = sum(item.qty or 0 for item in doc.items)
doc.total_amount = sum((item.qty or 0) * (item.rate or 0) for item in doc.items)

if doc.total_amount > 50000:
    doc.requires_approval = 1
    doc.approval_status = "Pending"

if doc.supplier and not doc.supplier_name:
    doc.supplier_name = frappe.db.get_value("Supplier", doc.supplier, "supplier_name")
```

**Rule**: ALWAYS modify `doc` fields directly in Before Save — they are automatically persisted.

## Workflow 5: Document Event — Create Related Document

**Goal**: Create a ToDo when a new Lead is inserted.

```python
# Type: Document Event | Event: After Insert | DocType: Lead

frappe.get_doc({
    "doctype": "ToDo",
    "allocated_to": doc.lead_owner or doc.owner,
    "reference_type": "Lead",
    "reference_name": doc.name,
    "description": f"Follow up with new lead: {doc.lead_name}",
    "date": frappe.utils.add_days(frappe.utils.today(), 1),
    "priority": "High" if doc.status == "Hot" else "Medium"
}).insert(ignore_permissions=True)
```

**Rules**:
- ALWAYS use After Insert or After Save for creating related docs
- NEVER create documents in Before Save — `doc.name` may not exist yet
- ALWAYS use `ignore_permissions=True` for system-generated documents

## Workflow 6: API Endpoint

**Goal**: Create authenticated REST API returning customer data.

```python
# Type: API | Method: get_customer_dashboard | Allow Guest: No
# Endpoint: /api/method/get_customer_dashboard

customer = frappe.form_dict.get("customer")
if not customer:
    frappe.throw("Parameter 'customer' is required")

# ALWAYS check permissions
if not frappe.has_permission("Customer", "read", customer):
    frappe.throw("Access denied", frappe.PermissionError)

orders = frappe.db.count("Sales Order", {"customer": customer, "docstatus": 1})
revenue = frappe.db.get_value("Sales Invoice",
    filters={"customer": customer, "docstatus": 1},
    fieldname="sum(grand_total)") or 0

frappe.response["message"] = {
    "customer": customer,
    "total_orders": orders,
    "total_revenue": revenue
}
```

**Rules**:
- ALWAYS validate input parameters
- ALWAYS check permissions (even with Allow Guest: No)
- ALWAYS cap query limits: `min(frappe.utils.cint(limit), 100)`
- NEVER expose full documents — return only needed fields

## Workflow 7: Scheduler Event

**Goal**: Daily reminder for overdue invoices.

```python
# Type: Scheduler Event | Cron: 0 9 * * * (daily at 9:00)

BATCH_SIZE = 50
today = frappe.utils.today()

overdue = frappe.get_all("Sales Invoice",
    filters={
        "status": "Unpaid",
        "due_date": ["<", today],
        "docstatus": 1
    },
    fields=["name", "customer", "owner", "due_date", "grand_total"],
    limit=BATCH_SIZE
)

for inv in overdue:
    days = frappe.utils.date_diff(today, inv.due_date)
    if not frappe.db.exists("ToDo", {
        "reference_type": "Sales Invoice",
        "reference_name": inv.name,
        "status": "Open"
    }):
        frappe.get_doc({
            "doctype": "ToDo",
            "allocated_to": inv.owner,
            "reference_type": "Sales Invoice",
            "reference_name": inv.name,
            "description": f"Invoice {inv.name} is {days} days overdue"
        }).insert(ignore_permissions=True)

frappe.db.commit()  # REQUIRED in scheduler scripts
```

**Rules**:
- ALWAYS add `frappe.db.commit()` at end of scheduler scripts
- ALWAYS add `limit` to queries — prevent memory exhaustion
- ALWAYS use `try/except` + `frappe.log_error()` in loops
- NEVER run scheduler scripts that process unlimited records

## Workflow 8: Permission Query

**Goal**: Users see only their territory's customers.

```python
# Type: Permission Query | DocType: Customer

user_territory = frappe.db.get_value("User", user, "territory")
user_roles = frappe.get_roles(user)

if "System Manager" in user_roles:
    conditions = ""  # Full access
elif user_territory:
    conditions = f"`tabCustomer`.territory = {frappe.db.escape(user_territory)}"
else:
    conditions = f"`tabCustomer`.owner = {frappe.db.escape(user)}"
```

**Rules**:
- ALWAYS give System Manager full access (`conditions = ""`)
- ALWAYS use `frappe.db.escape()` for user input in SQL
- ALWAYS set `conditions` variable — it is the output
- Permission Query only affects `frappe.db.get_list`, NOT `frappe.db.get_all`

## Event Name Mapping

| UI Name | Internal Hook | Best For |
|---------|---------------|----------|
| Before Validate | `before_validate` | Pre-validation defaults |
| **Before Save** | **`validate`** | Validation + calculations (MOST COMMON) |
| After Save | `on_update` | Notifications, audit logs |
| After Insert | `after_insert` | Create related docs (new only) |
| Before Submit | `before_submit` | Submit-time validation |
| After Submit | `on_submit` | Post-submit automation |
| Before Cancel | `before_cancel` | Cancel prevention |
| After Cancel | `on_cancel` | Cleanup after cancel |
| Before Delete | `on_trash` | Delete prevention |

## Sandbox-Safe API Quick Reference

| Need | Use (NOT import) |
|------|-------------------|
| Parse JSON | `frappe.parse_json()` or `json.loads()` |
| Serialize JSON | `frappe.as_json()` or `json.dumps()` |
| Today's date | `frappe.utils.today()` |
| Now (datetime) | `frappe.utils.now()` |
| Add days | `frappe.utils.add_days(date, n)` |
| Date diff | `frappe.utils.date_diff(d1, d2)` |
| Float conversion | `frappe.utils.flt(val)` |
| Int conversion | `frappe.utils.cint(val)` |
| HTTP GET | `frappe.make_get_request(url)` |
| HTTP POST | `frappe.make_post_request(url, data)` |
| Render template | `frappe.render_template(tmpl, ctx)` |
| Log error | `frappe.log_error(msg, title)` |
| Send email | `frappe.sendmail(recipients, subject, message)` |

## When to Migrate to Controller

ALWAYS migrate to a Document Controller when:
- You need `import` statements (beyond `json`)
- Script exceeds 100 lines
- You need try/except with rollback
- You need `frappe.enqueue()` for background jobs
- You need to extend an existing ERPNext DocType
- Multiple scripts on same DocType become hard to manage

**Migration path**: See `frappe-impl-controllers` for controller implementation.

## Related Skills

- `frappe-syntax-serverscripts` — Exact sandbox API reference
- `frappe-errors-serverscripts` — Error handling and anti-patterns
- `frappe-core-database` — `frappe.db.*` operations
- `frappe-core-permissions` — Permission system details
- `frappe-impl-controllers` — When to migrate from Server Script

> See [references/decision-tree.md](references/decision-tree.md) for complete decision trees.
> See [references/workflows.md](references/workflows.md) for extended patterns.
> See [references/examples.md](references/examples.md) for 10+ complete examples.
