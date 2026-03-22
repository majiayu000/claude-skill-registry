---
name: frappe-core-workflow
description: >
  Use when creating or modifying Frappe Workflows, defining states and transitions, adding action conditions, or troubleshooting workflow permission errors.
  Prevents stuck documents from misconfigured transitions, missing state permissions, and circular workflow paths.
  Covers Workflow DocType, workflow states, transitions, actions, conditions (Python expressions), workflow permissions, workflow_state field, Workflow Action DocType.
  Keywords: workflow, states, transitions, actions, conditions, workflow_state, Workflow Action, approval, document workflow.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Workflow Engine

The Frappe Workflow engine is a state machine that controls document lifecycle through configurable states, transitions, and role-based permissions. It governs when and how documents change status, who can perform actions, and what side effects occur on each transition.

## Quick Reference

```
Workflow DocType            → Defines the state machine for a specific DocType
├── states (child table)    → Workflow Document State rows
│   ├── state               → Link to Workflow State
│   ├── doc_status          → 0 (Draft), 1 (Submitted), 2 (Cancelled)
│   ├── allow_edit          → Role that can edit in this state
│   ├── update_field        → Field to update when entering state
│   ├── update_value        → Value to set (literal or expression)
│   └── next_action_email_template → Email Template link
└── transitions (child table) → Workflow Transition rows
    ├── state               → Source state (Link to Workflow State)
    ├── action              → Link to Workflow Action Master
    ├── next_state          → Target state (Link to Workflow State)
    ├── allowed             → Role that can perform this action
    ├── allow_self_approval → Check (default: 1)
    ├── condition           → Python expression (optional)
    └── transition_tasks    → Link to Workflow Transition Tasks
```

### Key Fields on Workflow DocType

| Field | Type | Purpose |
|-------|------|---------|
| `workflow_name` | Data | Unique identifier |
| `document_type` | Link → DocType | Target DocType |
| `is_active` | Check | Only ONE workflow per DocType can be active |
| `workflow_state_field` | Data | Default: `workflow_state` |
| `override_status` | Check | Prevent workflow from overriding list view status |
| `send_email_alert` | Check | Email notifications with next possible actions |

## How the Engine Works

### 1. Activation and Field Creation

When a Workflow is saved with `is_active = 1`:
- All other workflows for the same DocType are deactivated automatically
- A hidden Custom Field (`workflow_state_field`, default `workflow_state`) is created on the target DocType if it does not exist
- The field is type `Link` to `Workflow State`, with `hidden=1`, `allow_on_submit=1`, `no_copy=1`
- Existing documents with empty workflow state get their state set based on their current `docstatus`

### 2. State Resolution

Every document under a workflow has a `workflow_state` field. The engine resolves available transitions by:

1. Reading current `workflow_state` from the document
2. Filtering `workflow.transitions` where `transition.state == current_state`
3. Filtering by user roles: `transition.allowed in frappe.get_roles()`
4. Evaluating `transition.condition` via `frappe.safe_eval()` (if set)
5. Returning matching transitions as available actions

### 3. Applying a Transition

When `apply_workflow(doc, action)` is called:

1. Load document from DB (fresh read)
2. Get available transitions for current user
3. Find transition matching the requested `action`
4. Check self-approval: blocked if `allow_self_approval=0` AND user is document owner
5. Set `workflow_state_field` to `transition.next_state`
6. If `update_field` is set on the target state, update that field
7. Execute transition tasks (sync first, then async via `frappe.enqueue`)
8. Handle docstatus change based on source/target state `doc_status` values
9. Save/Submit/Cancel document accordingly
10. Add workflow comment

## Workflow and DocStatus Interaction

**CRITICAL**: The workflow engine controls docstatus transitions. You NEVER call `doc.submit()` or `doc.cancel()` directly on a workflow-controlled document. The workflow does it.

### DocStatus Transition Rules

| Source doc_status | Target doc_status | Engine Action | Valid? |
|:-:|:-:|---|:-:|
| 0 (Draft) | 0 (Draft) | `doc.save()` | YES |
| 0 (Draft) | 1 (Submitted) | `doc.submit()` | YES |
| 1 (Submitted) | 1 (Submitted) | `doc.save()` | YES |
| 1 (Submitted) | 2 (Cancelled) | `doc.cancel()` | YES |
| 2 (Cancelled) | ANY | BLOCKED | NO |
| 1 (Submitted) | 0 (Draft) | BLOCKED | NO |
| 0 (Draft) | 2 (Cancelled) | BLOCKED | NO |

**ALWAYS** define your states so that docstatus only moves forward: 0→0, 0→1, 1→1, 1→2.
**NEVER** create a transition from a cancelled state or from submitted back to draft.

### Non-Submittable DocTypes

If the target DocType is NOT submittable, ALL states MUST have `doc_status = 0`. The engine validates this and throws an error if any state has `doc_status = 1` or `2` on a non-submittable DocType.

## Workflow States

Workflow State is a separate DocType used as a master list. Each state has:

| Field | Purpose |
|-------|---------|
| `state` | Display name of the state |
| `style` | CSS class for badge display (Primary, Success, Warning, Danger, Info, Inverse) |
| `icon` | Font Awesome icon class |

### State Row Fields (Workflow Document State)

| Field | Purpose |
|-------|---------|
| `state` | Link to Workflow State |
| `doc_status` | Select: 0, 1, or 2 |
| `allow_edit` | Link to Role — ONLY this role can edit the document in this state |
| `update_field` | Field to update when document enters this state |
| `update_value` | Value to set (string or Python expression if `evaluate_as_expression=1`) |
| `is_optional_state` | Check — optional states are skipped in `get_next_possible_transitions` |
| `send_email` | Check (default 1) — send email notification on entering this state |
| `next_action_email_template` | Link to Email Template |
| `message` | Text message for the email notification |

## Workflow Transitions

Each transition row defines one possible action:

| Field | Purpose |
|-------|---------|
| `state` | Source state (MUST exist in states table) |
| `action` | Link to Workflow Action Master (e.g., "Approve", "Reject", "Review") |
| `next_state` | Target state (MUST exist in states table) |
| `allowed` | Link to Role — ONLY users with this role see this action |
| `allow_self_approval` | Check (default 1) — if 0, document owner cannot perform this action |
| `condition` | Python expression evaluated with `frappe.safe_eval()` |
| `transition_tasks` | Link to Workflow Transition Tasks (v15+) |

### Condition Expressions

Conditions are Python expressions evaluated in a sandboxed environment. Available globals:

```python
# Available in condition expressions:
frappe.db.get_value(doctype, name, fieldname)
frappe.db.get_list(doctype, filters, fields)
frappe.session.user
frappe.session.roles  # NOT available — use frappe.get_roles() outside conditions
frappe.utils.now_datetime()
frappe.utils.add_to_date(date, **kwargs)
frappe.utils.get_datetime(datetime_str)
frappe.utils.now()
doc.fieldname  # Access any field on the document (as dict)
```

Example conditions:
```python
doc.grand_total > 50000
doc.department == "HR"
doc.grand_total > 50000 and doc.department != "Finance"
```

## Workflow Actions

### Workflow Action Master

Simple DocType with just a `workflow_action_name` field. Common actions: Approve, Reject, Review, Send Back, Cancel. Create these first before defining transitions.

### Workflow Action DocType

Tracks pending actions for users. Created automatically when a document enters a state with outgoing transitions.

| Field | Purpose |
|-------|---------|
| `status` | Open or Completed |
| `reference_doctype` | The DocType of the document |
| `reference_name` | The document name |
| `workflow_state` | Current workflow state |
| `user` | Assigned user |
| `permitted_roles` | Table MultiSelect of roles that can act |
| `completed_by` | User who completed the action |
| `completed_by_role` | Role used to complete |

Workflow Actions appear in the user's "Workflow Action" list and can be acted on via email links.

## Self-Approval Control

```python
def has_approval_access(user, doc, transition):
    return (user == "Administrator"
            or transition.get("allow_self_approval")
            or user != doc.get("owner"))
```

- **Administrator** ALWAYS has approval access regardless of settings
- If `allow_self_approval = 1` (default): document owner CAN approve
- If `allow_self_approval = 0`: document owner CANNOT approve their own document

## Decision Tree

```
Need workflow on a DocType?
├── Is DocType submittable?
│   ├── YES → States can use doc_status 0, 1, 2
│   └── NO  → ALL states MUST have doc_status = 0
├── Define states → Create Workflow State records first
├── Define transitions → Need Workflow Action Master records first
├── Who can edit in each state? → Set allow_edit per state
├── Need conditional transitions?
│   └── Use Python expressions with doc.field access
├── Need to block self-approval?
│   └── Set allow_self_approval = 0 on specific transitions
└── Need email notifications?
    └── Set send_email_alert on Workflow + email templates on states
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `WorkflowStateError` | Document has no workflow_state set | Ensure workflow sets initial state on creation |
| `WorkflowTransitionError` | Action not valid for current state/role | Verify transitions table covers all needed paths |
| `WorkflowPermissionError` | User lacks role for transition, or self-approval blocked | Check `allowed` role and `allow_self_approval` |
| "Illegal Document Status" | Invalid docstatus transition (e.g., 0→2) | Fix state `doc_status` values |
| "Cannot cancel before submitting" | Transition from draft (0) to cancelled (2) | Add intermediate submitted (1) state |

## See Also

- [API Reference](references/api-reference.md) — Complete workflow Python API
- [Examples](references/examples.md) — Workflow configuration examples
- [Anti-Patterns](references/anti-patterns.md) — Common mistakes and how to avoid them
- `frappe-impl-workflow` — Step-by-step implementation guide
