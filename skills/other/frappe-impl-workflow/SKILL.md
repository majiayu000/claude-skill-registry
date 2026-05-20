---
name: frappe-impl-workflow
description: >
  Use when implementing document Workflows, approval chains, or state-based transitions in Frappe.
  Prevents stuck documents from missing transitions, broken approval chains, and permission errors on workflow actions.
  Covers Workflow DocType, Workflow State, Workflow Action, transition rules, allowed roles, conditions, workflow_state field, apply_workflow.
  Keywords: workflow, approval, transition, Workflow State, Workflow Action, state machine, approval chain, workflow_state.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Workflow Implementation

Step-by-step guide for implementing document workflows in Frappe. Covers design, setup, testing, and common approval chain patterns.

## Quick Reference — Implementation Checklist

```
1. □ Design states and transitions on paper/diagram first
2. □ Create Workflow State records (master list)
3. □ Create Workflow Action Master records (Approve, Reject, etc.)
4. □ Create the Workflow DocType record
5. □ Add states with correct doc_status values
6. □ Add transitions with roles, actions, and conditions
7. □ Set allow_edit roles per state
8. □ Configure email notifications (optional)
9. □ Test every transition path with test users
10. □ Verify self-approval blocking works as expected
```

## Step 1: Design Your Workflow

Before touching the UI, map out your workflow on paper.

### Identify States

**ALWAYS** start by listing every distinct document stage:

```
Example — Purchase Order Approval:
  Draft → Pending Review → Pending Approval → Approved → Submitted → Cancelled
```

### Map DocStatus to States

For submittable DocTypes, ALWAYS assign `doc_status` correctly:

| Stage | doc_status | Meaning |
|-------|:-:|---------|
| All "in-progress" states | 0 | Document is Draft, editable |
| Final approved/active state | 1 | Document is Submitted, locked |
| Cancelled state | 2 | Document is Cancelled |

**NEVER** assign `doc_status = 1` to intermediate approval states. A submitted document cannot return to draft. Once submitted, the only forward path is another submitted state or cancellation.

### Map Transitions

For each state, define: What actions are possible? Who can perform them? Any conditions?

```
Draft         →[Submit for Review / Creator]→     Pending Review
Pending Review →[Approve / Reviewer]→              Pending Approval
Pending Review →[Reject / Reviewer]→               Draft
Pending Approval →[Approve / Manager]→             Approved
Pending Approval →[Reject / Manager]→              Draft
Approved      →[Submit / Manager]→                 Submitted (doc_status=1)
Submitted     →[Cancel / Manager]→                 Cancelled (doc_status=2)
```

## Step 2: Create Prerequisite Records

### 2a. Create Workflow States

Navigate to **Workflow State** list or create via API:

```python
# Create states with appropriate styles
states = [
    {"workflow_state_name": "Draft", "style": ""},
    {"workflow_state_name": "Pending Review", "style": "Primary"},
    {"workflow_state_name": "Pending Approval", "style": "Warning"},
    {"workflow_state_name": "Approved", "style": "Success"},
    {"workflow_state_name": "Submitted", "style": "Info"},
    {"workflow_state_name": "Rejected", "style": "Danger"},
    {"workflow_state_name": "Cancelled", "style": "Inverse"},
]
for s in states:
    if not frappe.db.exists("Workflow State", s["workflow_state_name"]):
        frappe.get_doc({"doctype": "Workflow State", **s}).insert()
```

Available styles: `Primary`, `Success`, `Warning`, `Danger`, `Info`, `Inverse` (or empty for default).

### 2b. Create Workflow Action Masters

```python
actions = ["Submit for Review", "Approve", "Reject", "Send Back", "Cancel"]
for action in actions:
    if not frappe.db.exists("Workflow Action Master", action):
        frappe.get_doc({
            "doctype": "Workflow Action Master",
            "workflow_action_name": action
        }).insert()
```

## Step 3: Create the Workflow

### Via UI

Navigate to **Setup > Workflow > New Workflow**:

1. Set **Workflow Name** (e.g., "Purchase Order Approval")
2. Set **Document Type** (e.g., "Purchase Order")
3. Check **Is Active**
4. Add states in the **States** table
5. Add transitions in the **Transitions** table

### Via Python

```python
workflow = frappe.get_doc({
    "doctype": "Workflow",
    "workflow_name": "Purchase Order Approval",
    "document_type": "Purchase Order",
    "is_active": 1,
    "send_email_alert": 1,
    "states": [
        {"state": "Draft", "doc_status": "0", "allow_edit": "Purchase User"},
        {"state": "Pending Approval", "doc_status": "0", "allow_edit": "Purchase Manager"},
        {"state": "Approved", "doc_status": "1", "allow_edit": "Purchase Manager"},
        {"state": "Rejected", "doc_status": "0", "allow_edit": "Purchase User"},
        {"state": "Cancelled", "doc_status": "2"},
    ],
    "transitions": [
        {
            "state": "Draft",
            "action": "Submit for Review",
            "next_state": "Pending Approval",
            "allowed": "Purchase User",
            "allow_self_approval": 1,
        },
        {
            "state": "Pending Approval",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "Purchase Manager",
            "allow_self_approval": 0,
        },
        {
            "state": "Pending Approval",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "Purchase Manager",
        },
        {
            "state": "Rejected",
            "action": "Submit for Review",
            "next_state": "Pending Approval",
            "allowed": "Purchase User",
        },
        {
            "state": "Approved",
            "action": "Cancel",
            "next_state": "Cancelled",
            "allowed": "Purchase Manager",
        },
    ],
})
workflow.insert()
```

## Step 4: Configure Advanced Features

### Conditional Transitions

Add Python conditions to show transitions only when criteria are met:

```python
# Only allow approval for orders above 50000 by Senior Manager
{
    "state": "Pending Approval",
    "action": "Approve",
    "next_state": "Approved",
    "allowed": "Senior Manager",
    "condition": "doc.grand_total > 50000",
}

# Standard approval for orders up to 50000
{
    "state": "Pending Approval",
    "action": "Approve",
    "next_state": "Approved",
    "allowed": "Purchase Manager",
    "condition": "doc.grand_total <= 50000",
}
```

**ALWAYS** use `doc.fieldname` syntax in conditions (the document is exposed as a dict).

Available in conditions: `frappe.db.get_value()`, `frappe.db.get_list()`, `frappe.session.user`, `frappe.utils.now_datetime()`, `frappe.utils.add_to_date()`, `frappe.utils.get_datetime()`.

### Self-Approval Blocking

Set `allow_self_approval = 0` on approval transitions. This means:
- The document **owner** (creator) CANNOT perform this action
- Administrator is ALWAYS exempt from this restriction
- Other users with the required role CAN perform the action

### Email Notifications

1. Set `send_email_alert = 1` on the Workflow
2. On each state row, set `send_email = 1` (default)
3. Optionally link an `Email Template` via `next_action_email_template`
4. Add a custom `message` on the state row for inline notification text

### Update Fields on State Change

Use `update_field` and `update_value` on state rows to automatically set document fields:

```python
# Set approval_status when entering "Approved" state
{"state": "Approved", "doc_status": "1",
 "update_field": "approval_status", "update_value": "Approved"}

# Use expression to set approval date dynamically
{"state": "Approved", "doc_status": "1",
 "update_field": "custom_approved_on", "update_value": "frappe.utils.now()",
 "evaluate_as_expression": 1}
```

## Step 5: Test Your Workflow

### Manual Testing Checklist

1. **Create a test document** — verify it starts in the first state (Draft)
2. **Check available actions** — only roles with transitions from Draft should see buttons
3. **Perform each transition** — verify state changes correctly
4. **Test rejection paths** — verify documents return to correct state
5. **Test self-approval** — log in as document owner, verify blocked transitions
6. **Test conditions** — create documents that meet/fail conditions, verify button visibility
7. **Test email notifications** — verify emails sent on state changes
8. **Test with non-submittable DocType** — verify all doc_status = 0

### Programmatic Testing

```python
# Get available transitions for a document
from frappe.model.workflow import get_transitions, apply_workflow

doc = frappe.get_doc("Purchase Order", "PO-00001")
transitions = get_transitions(doc)
# Returns list of dicts with action, next_state, allowed, etc.

# Apply a workflow action
updated_doc = apply_workflow(doc, "Approve")
# Returns the updated document after state change
```

## Common Workflow Patterns

### Pattern 1: Sequential Approval Chain

```
Draft → Level 1 Review → Level 2 Review → Approved → Submitted
```

Each level has its own role. Document moves linearly through approvals.

### Pattern 2: Conditional Routing by Amount

```
Draft → Pending Approval
  ├─[amount <= 10000 / Team Lead]─→ Approved
  ├─[amount <= 50000 / Manager]──→ Approved
  └─[amount > 50000 / Director]──→ Approved
```

Use `condition` on each transition to route based on document values.

### Pattern 3: Review with Rejection Loop

```
Draft ←──[Reject]── Pending Review ──[Approve]──→ Approved
  └──[Submit for Review]──→ Pending Review
```

Rejected documents return to Draft for revision. Creator resubmits. This is the most common approval pattern.

### Pattern 4: Leave Approval

```
Applied (doc_status=0, allow_edit=Employee)
  └─[Approve / Leave Approver]─→ Approved (doc_status=1)
  └─[Reject / Leave Approver]─→ Rejected (doc_status=0)
Approved
  └─[Cancel / HR Manager]─→ Cancelled (doc_status=2)
```

### Pattern 5: Document Review (Non-Submittable)

For non-submittable DocTypes, ALL states MUST have `doc_status = 0`:

```
Draft → Under Review → Reviewed → Published
(all doc_status = 0)
```

## Migrating from Manual DocStatus to Workflow

If your DocType currently uses manual Submit/Cancel buttons and you want to add a workflow:

1. **Map existing documents** — The workflow engine auto-maps existing documents to states based on their `docstatus` when the workflow is created
2. **Define a state for each docstatus** — ALWAYS have at least one state per docstatus value your documents currently use
3. **Test with existing data** — Verify that existing submitted documents show the correct workflow state
4. **Update list views** — If using `override_status`, the workflow state replaces the Status column

**NEVER** activate a workflow without a state for docstatus=0. New documents would have no valid initial state.

## Decision Tree

```
Starting a new workflow implementation?
│
├── What type of DocType?
│   ├── Submittable → can use doc_status 0, 1, 2
│   └── Non-submittable → ALL states must be doc_status = 0
│
├── How many approval levels?
│   ├── Single → Two-state: Draft → Approved
│   ├── Sequential → Chain: Draft → L1 → L2 → Approved
│   └── Conditional → Route by field values using conditions
│
├── Need self-approval blocking?
│   └── Set allow_self_approval = 0 on approval transitions
│
├── Need rejection/revision loop?
│   └── Add Reject transition back to Draft or previous state
│
├── Need email notifications?
│   ├── Enable send_email_alert on Workflow
│   └── Link Email Template on each state
│
└── Need automated field updates?
    └── Use update_field + update_value on target state
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No action buttons visible | User lacks required role | Add role to user OR add transition for user's role |
| "Self approval is not allowed" | User is doc owner + `allow_self_approval=0` | Have different user approve, or set flag to 1 |
| "Workflow State not set" | Document created before workflow activation | Run `update_default_workflow_status` or manually set state |
| Document stuck in state | No outgoing transition defined for current state + user role | Add missing transition |
| "Cannot cancel before submitting" | Transition goes from doc_status=0 to doc_status=2 | Add intermediate submitted state |
| Actions show for wrong users | Role assignment too broad | Use more specific roles or add conditions |

## See Also

- [Workflow Patterns](references/workflows.md) — Detailed step-by-step workflow examples
- [Decision Tree](references/decision-tree.md) — Extended decision tree for workflow design
- [Examples](references/examples.md) — Code examples for common scenarios
- [Anti-Patterns](references/anti-patterns.md) — Mistakes to avoid
- `frappe-core-workflow` — Workflow engine internals and API reference
