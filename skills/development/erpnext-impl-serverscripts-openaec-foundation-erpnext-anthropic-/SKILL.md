---
name: erpnext-impl-serverscripts
description: "Implementation workflows and decision trees for ERPNext Server Scripts. Use when determining HOW to implement server-side features: document validation, automated calculations, API endpoints, scheduled tasks, permission filtering. Triggers: how do I implement server-side, when to use server script vs controller, which script type, build custom API, automate validation, schedule task, filter documents per user."
---

# ERPNext Server Scripts - Implementation

This skill helps you determine HOW to implement server-side features. For exact syntax, see `erpnext-syntax-serverscripts`.

**Version**: v14/v15/v16 compatible

## CRITICAL: Sandbox Limitation

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  ALL IMPORTS BLOCKED IN SERVER SCRIPTS                          │
├─────────────────────────────────────────────────────────────────────┤
│ import json              → ImportError: __import__ not found       │
│ from frappe.utils import → ImportError                             │
│                                                                     │
│ SOLUTION: Use pre-loaded namespace directly:                       │
│   frappe.utils.nowdate()      frappe.parse_json(data)              │
└─────────────────────────────────────────────────────────────────────┘
```

## Main Decision: Server Script vs Controller?

```
┌───────────────────────────────────────────────────────────────────┐
│ WHAT DO YOU NEED?                                                 │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ► No custom app / Quick prototyping                               │
│   └── Server Script ✓                                             │
│                                                                   │
│ ► Import external libraries (requests, pandas, etc.)              │
│   └── Controller (in custom app)                                  │
│                                                                   │
│ ► Complex multi-document transactions                             │
│   └── Controller (full Python, try/except/rollback)               │
│                                                                   │
│ ► Simple validation / auto-fill / notifications                   │
│   └── Server Script ✓                                             │
│                                                                   │
│ ► Create REST API without custom app                              │
│   └── Server Script API type ✓                                    │
│                                                                   │
│ ► Scheduled background job                                        │
│   └── Server Script Scheduler type ✓ (simple)                     │
│   └── hooks.py scheduler_events (complex)                         │
│                                                                   │
│ ► Dynamic list filtering per user                                 │
│   └── Server Script Permission Query type ✓                       │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

**Rule of thumb**: Server Scripts for no-code/low-code solutions within Frappe's sandbox. Controllers for full Python power.

## Decision Tree: Which Script Type?

```
WHAT DO YOU WANT TO ACHIEVE?
│
├─► React to document lifecycle (save/submit/cancel)?
│   └── Document Event
│       └── Which event? See event mapping below
│
├─► Create REST API endpoint?
│   └── API
│       ├── Public endpoint? → Allow Guest: Yes
│       └── Authenticated? → Allow Guest: No
│
├─► Run task on schedule (daily/hourly)?
│   └── Scheduler Event
│       └── Define cron pattern
│
└─► Filter list view per user/role/territory?
    └── Permission Query
        └── Return conditions string for WHERE clause
```

→ See [references/decision-tree.md](references/decision-tree.md) for complete decision tree.

## Event Name Mapping (Document Event)

| UI Name | Internal Hook | Best For |
|---------|---------------|----------|
| Before Validate | `before_validate` | Pre-validation setup |
| **Before Save** | **`validate`** | All validation + auto-calc |
| After Save | `on_update` | Notifications, audit logs |
| Before Submit | `before_submit` | Submit-time validation |
| After Submit | `on_submit` | Post-submit automation |
| Before Cancel | `before_cancel` | Cancel prevention |
| After Cancel | `on_cancel` | Cleanup after cancel |
| After Insert | `after_insert` | Create related docs |
| Before Delete | `on_trash` | Delete prevention |

## Implementation Workflows

### Workflow 1: Validation with Conditional Logic

**Scenario**: Validate sales order based on customer credit limit.

```python
# Configuration:
#   Type: Document Event
#   DocType Event: Before Save
#   Reference DocType: Sales Order

# Get customer's credit limit
credit_limit = frappe.db.get_value("Customer", doc.customer, "credit_limit") or 0

# Check outstanding
outstanding = frappe.db.get_value(
    "Sales Invoice",
    filters={"customer": doc.customer, "docstatus": 1, "status": "Unpaid"},
    fieldname="sum(outstanding_amount)"
) or 0

# Validate
total_exposure = outstanding + doc.grand_total
if credit_limit > 0 and total_exposure > credit_limit:
    frappe.throw(
        f"Credit limit exceeded. Limit: {credit_limit}, Exposure: {total_exposure}",
        title="Credit Limit Error"
    )
```

### Workflow 2: Auto-Calculate and Auto-Fill

**Scenario**: Auto-calculate totals and set derived fields.

```python
# Configuration:
#   Type: Document Event
#   DocType Event: Before Save
#   Reference DocType: Purchase Order

# Calculate from child table
doc.total_qty = sum(item.qty or 0 for item in doc.items)
doc.total_amount = sum(item.amount or 0 for item in doc.items)

# Set derived fields
if doc.total_amount > 50000:
    doc.requires_approval = 1
    doc.approval_status = "Pending"

# Auto-fill from linked document
if doc.supplier and not doc.supplier_name:
    doc.supplier_name = frappe.db.get_value("Supplier", doc.supplier, "supplier_name")
```

### Workflow 3: Create Related Document

**Scenario**: Create ToDo when document is inserted.

```python
# Configuration:
#   Type: Document Event
#   DocType Event: After Insert
#   Reference DocType: Lead

# Create follow-up task
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

### Workflow 4: Custom API Endpoint

**Scenario**: Create API to fetch customer dashboard data.

```python
# Configuration:
#   Type: API
#   API Method: get_customer_dashboard
#   Allow Guest: No
# Endpoint: /api/method/get_customer_dashboard

customer = frappe.form_dict.get("customer")
if not customer:
    frappe.throw("Parameter 'customer' is required")

# Permission check
if not frappe.has_permission("Customer", "read", customer):
    frappe.throw("Access denied", frappe.PermissionError)

# Aggregate data
orders = frappe.db.count("Sales Order", {"customer": customer, "docstatus": 1})
revenue = frappe.db.get_value(
    "Sales Invoice",
    filters={"customer": customer, "docstatus": 1},
    fieldname="sum(grand_total)"
) or 0

frappe.response["message"] = {
    "customer": customer,
    "total_orders": orders,
    "total_revenue": revenue
}
```

### Workflow 5: Scheduled Task

**Scenario**: Daily reminder for overdue invoices.

```python
# Configuration:
#   Type: Scheduler Event
#   Event Frequency: Cron
#   Cron Format: 0 9 * * *  (daily at 9:00)

today = frappe.utils.today()

overdue = frappe.get_all("Sales Invoice",
    filters={
        "status": "Unpaid",
        "due_date": ["<", today],
        "docstatus": 1
    },
    fields=["name", "customer", "owner", "due_date", "grand_total"],
    limit=100
)

for inv in overdue:
    days_overdue = frappe.utils.date_diff(today, inv.due_date)
    
    # Create ToDo if not exists
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
            "description": f"Invoice {inv.name} is {days_overdue} days overdue (${inv.grand_total})"
        }).insert(ignore_permissions=True)

frappe.db.commit()  # REQUIRED in scheduler scripts
```

### Workflow 6: Permission Query

**Scenario**: Filter documents by user's territory.

```python
# Configuration:
#   Type: Permission Query
#   Reference DocType: Customer

user_territory = frappe.db.get_value("User", user, "territory")
user_roles = frappe.get_roles(user)

if "System Manager" in user_roles:
    conditions = ""  # Full access
elif user_territory:
    conditions = f"`tabCustomer`.territory = {frappe.db.escape(user_territory)}"
else:
    conditions = f"`tabCustomer`.owner = {frappe.db.escape(user)}"
```

→ See [references/workflows.md](references/workflows.md) for more workflow patterns.

## Integration: Client Script + Server Script

| Client Script Calls | Server Script Provides |
|---------------------|------------------------|
| `frappe.call({method: 'api_name'})` | API type script |
| `frappe.db.get_value()` | Direct DB (no script needed) |
| `frm.call('method')` | Controller method (not Server Script) |

### Combined Pattern

```javascript
// CLIENT: Call server API
frappe.call({
    method: 'check_credit_limit',
    args: {
        customer: frm.doc.customer,
        amount: frm.doc.grand_total
    },
    callback: function(r) {
        if (!r.message.allowed) {
            frappe.throw(__('Credit limit exceeded'));
        }
    }
});
```

```python
# SERVER: API script 'check_credit_limit'
customer = frappe.form_dict.get("customer")
amount = frappe.utils.flt(frappe.form_dict.get("amount"))

credit_limit = frappe.db.get_value("Customer", customer, "credit_limit") or 0
outstanding = frappe.db.get_value(
    "Sales Invoice",
    {"customer": customer, "docstatus": 1, "status": "Unpaid"},
    "sum(outstanding_amount)"
) or 0

frappe.response["message"] = {
    "allowed": (outstanding + amount) <= credit_limit or credit_limit == 0,
    "available": max(0, credit_limit - outstanding)
}
```

## Checklist: Implementation Steps

### New Server Script Feature

1. **[ ] Determine script type**
   - Document lifecycle? → Document Event
   - Custom API? → API
   - Scheduled job? → Scheduler Event
   - List filtering? → Permission Query

2. **[ ] Check sandbox limitations**
   - No imports needed? → Proceed
   - Need imports? → Use Controller instead

3. **[ ] Implement core logic**
   - Use `frappe.utils.*` directly
   - Use `frappe.db.*` for database

4. **[ ] Add validation & error handling**
   - `frappe.throw()` for user errors
   - Input validation for API scripts

5. **[ ] Test edge cases**
   - Empty values (null checks)
   - Permission scenarios
   - Large data volumes (add limits)

6. **[ ] Scheduler-specific**
   - Add `frappe.db.commit()` at end
   - Add `limit` to queries
   - Batch process large datasets

## Critical Rules

| Rule | Why |
|------|-----|
| NO `import` statements | Sandbox blocks all imports |
| `frappe.db.commit()` in Scheduler | Changes not auto-committed |
| NO `doc.save()` in Before Save | Framework handles save |
| `frappe.throw()` for validation | Stops document operation |
| Always escape user input in SQL | Prevent SQL injection |
| Add `limit` to queries | Prevent memory issues |

## Related Skills

- `erpnext-syntax-serverscripts` — Exact syntax and method signatures
- `erpnext-errors-serverscripts` — Error handling patterns
- `erpnext-database` — frappe.db.* operations
- `erpnext-permissions` — Permission system details
- `erpnext-api-patterns` — API design patterns

→ See [references/examples.md](references/examples.md) for 10+ complete implementation examples.
