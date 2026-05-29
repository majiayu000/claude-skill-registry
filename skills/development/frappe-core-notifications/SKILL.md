---
name: frappe-core-notifications
description: >
  Use when implementing email notifications, system alerts, Assignment Rules, Auto Repeat, or ToDo items.
  Prevents misconfigured Email Accounts, broken notification templates, and silent delivery failures.
  Covers frappe.sendmail, Notification DocType, Email Account setup, Jinja email templates, Assignment Rules, Auto Repeat scheduling, ToDo API.
  Keywords: notification, email, sendmail, Email Account, Assignment Rule, Auto Repeat, ToDo, alert, template.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Notification System

## Quick Reference

| Channel | Method | Use Case |
|---------|--------|----------|
| Email | `frappe.sendmail()` | Programmatic email with full control |
| Email | Notification DocType (Email) | No-code email on document events |
| System | `frappe.publish_realtime()` | In-app real-time alerts via socket.io |
| System | Notification DocType (System) | No-code in-app alerts |
| SMS | Notification DocType (SMS) | No-code SMS on document events |
| Slack | Notification DocType (Slack) | No-code Slack webhook messages |
| Assignment | `frappe.desk.form.assign_to.add()` | Assign document to user (creates ToDo) |
| ToDo | `frappe.get_doc({"doctype": "ToDo", ...})` | Direct task creation |
| Comment | `doc.add_comment("Comment", text)` | Timeline comment on document |
| Tag | `doc.add_tag("tag_name")` | Document tagging for filtering |

---

## Decision Tree

```
What notification mechanism do you need?
│
├─ Email on document event (no code)?
│  └─ Notification DocType → Channel: Email
│
├─ Programmatic email with custom logic?
│  └─ frappe.sendmail() in server script or hook
│
├─ Real-time in-app notification?
│  ├─ No-code → Notification DocType → Channel: System Notification
│  └─ Programmatic → frappe.publish_realtime()
│
├─ SMS on document event?
│  └─ Notification DocType → Channel: SMS (requires SMS Settings)
│
├─ Assign document to user?
│  ├─ No-code → Assignment Rule DocType
│  └─ Programmatic → frappe.desk.form.assign_to.add()
│
├─ Recurring document creation?
│  └─ Auto Repeat DocType
│
└─ Add comment or tag?
   ├─ Comment → doc.add_comment("Comment", text="...")
   └─ Tag → doc.add_tag("tag_name")
```

---

## Notification DocType

The Notification DocType enables no-code alerts across four channels.

### Event Triggers

| Event | Fires When |
|-------|------------|
| New | Document is created |
| Save | Document is saved |
| Submit | Document is submitted |
| Cancel | Document is cancelled |
| Value Change | Specific field value changes |
| Days Before | N days before a date field value |
| Days After | N days after a date field value |
| Method | Custom Python method is called |

### Condition Syntax

ALWAYS use Python expressions in the Condition field:

```python
# Status-based
doc.status == "Open"

# Date-based
doc.due_date == nowdate()

# Threshold-based
doc.grand_total > 40000

# Combined
doc.status == "Overdue" and doc.grand_total > 10000
```

Available context: `doc`, `nowdate()`, `frappe.utils.*`.

### Recipient Configuration

| Source | Description |
|--------|-------------|
| Document Field | Email/phone field on the document |
| Role | All users with specified role |
| Custom | Hard-coded email address |
| All Assignees | All users assigned to the document |
| Condition | Jinja expression to filter recipients |

### Jinja Message Template

```html
<h3>Order Overdue</h3>
<p>Transaction {{ doc.name }} has exceeded its due date.</p>

{% if comments %}
Last comment: {{ comments[-1].comment }} by {{ comments[-1].by }}
{% endif %}

<ul>
  <li>Customer: {{ doc.customer }}</li>
  <li>Amount: {{ doc.grand_total }}</li>
</ul>
```

Template variables: `{{ doc }}`, `{{ doc.fieldname }}`, `{{ comments }}`, `{{ nowdate() }}`.

### Attach Print

Set **Attach Print** to include a PDF of the document. Select a **Print Format** for custom layout.

---

## frappe.sendmail() — Programmatic Email

```python
frappe.sendmail(
    recipients=["user@example.com"],       # list of email addresses
    subject="Invoice Due",                  # email subject
    message="<p>Your invoice is due.</p>",  # HTML body
    template="invoice_reminder",            # Jinja template name (optional)
    args={"customer": "ACME"},              # template context variables
    attachments=[{"fname": "inv.pdf", "fcontent": pdf_bytes}],
    reference_doctype="Sales Invoice",      # links email to document
    reference_name="SINV-00001",
    delayed=True,                           # queue via Email Queue (default)
    now=False,                              # True = send immediately, skip queue
    sender="noreply@example.com",           # override sender
    cc=["manager@example.com"],
    bcc=["audit@example.com"],
    reply_to="support@example.com",
    expose_recipients="header",             # show recipients in email header
)
```

**Rules**:
- ALWAYS set `reference_doctype` and `reference_name` when the email relates to a document — this links the email in the document timeline.
- NEVER set `now=True` in production — it blocks the request. Use `delayed=True` (default) to queue via Email Queue.
- ALWAYS ensure an Email Account with "Enable Outgoing" is configured before calling `frappe.sendmail`.

### Email Queue

Emails are queued in the **Email Queue** DocType and sent by the scheduler. Check queue status:

```python
# Check pending emails
pending = frappe.get_all("Email Queue", filters={"status": "Not Sent"}, limit=10)
```

---

## frappe.publish_realtime() — System Notifications

```python
frappe.publish_realtime(
    event="msgprint",                      # event name
    message={"msg": "Task completed!"},    # dict payload
    user="user@example.com",               # target specific user
    doctype="Sales Invoice",               # broadcast to doctype room
    docname="SINV-00001",                  # broadcast to document room
    after_commit=True,                     # emit after transaction commits
)
```

### Room Types

| Room | Audience |
|------|----------|
| `user:{email}` | Single user (set `user=`) |
| `doctype:{dt}` | All users viewing that list |
| `doc:{dt}/{dn}` | All users viewing that document |
| `all` | All Desk users site-wide |
| `task_progress:{id}` | Background task progress |

### Built-in Events

| Event | Purpose |
|-------|---------|
| `msgprint` | Show message dialog to user |
| `list_update` | Refresh document list view |
| `docinfo_update` | Refresh document info sidebar |
| `progress` | Show progress bar |

ALWAYS set `after_commit=True` when publishing from within a database transaction — otherwise the event fires before data is committed and the client may read stale data.

---

## Assignment Rules

Auto-assign documents to users based on conditions (no code).

### Configuration Fields

| Field | Purpose |
|-------|---------|
| Document Type | Which DocType triggers the rule |
| Assign Condition | Python expression (same as Notification) |
| Assignment Days | Limit to specific weekdays |
| Users | List of users to assign to |
| Assignment Rule | Round Robin, Load Balancing, or Based on Field |

### Programmatic Assignment

```python
from frappe.desk.form.assign_to import add, remove, close, clear

# Assign
add({
    "assign_to": ["user@example.com"],
    "doctype": "Task",
    "name": "TASK-00001",
    "description": "Please review this task",
    "priority": "High",
    "date": "2025-12-31",
})

# Remove assignment (cancels ToDo)
remove("Task", "TASK-00001", "user@example.com")

# Close assignment (only assignee can close)
close("Task", "TASK-00001", "user@example.com")

# Clear all assignments
clear("Task", "TASK-00001")
```

NEVER call `close()` as a different user than the assignee — it raises a permission error.

---

## Auto Repeat

Creates recurring copies of documents on a schedule.

| Field | Purpose |
|-------|---------|
| Reference DocType | Which DocType to repeat |
| Reference Document | Source document to copy |
| Frequency | Daily, Weekly, Monthly, Quarterly, Half-yearly, Yearly |
| Start Date / End Date | Schedule window |
| Notify By Email | Send notification on creation |

ALWAYS set an **End Date** on Auto Repeat — open-ended schedules create documents indefinitely and are difficult to debug.

---

## ToDo API

```python
# Create ToDo directly
todo = frappe.get_doc({
    "doctype": "ToDo",
    "allocated_to": "user@example.com",
    "assigned_by": frappe.session.user,
    "description": "Review the quarterly report",
    "priority": "Medium",
    "date": "2025-12-31",
    "status": "Open",
    "reference_type": "Task",
    "reference_name": "TASK-00001",
}).insert(ignore_permissions=True)
```

ToDo statuses: `Open`, `Closed`, `Cancelled`.

---

## Comments and Tags

```python
# Add comment (appears in document timeline)
doc.add_comment("Comment", text="Reviewed and approved")
doc.add_comment("Edit", "Values changed")

# Add/get tags
doc.add_tag("urgent")
tags = doc.get_tags()  # returns list of tag strings
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Notification DocType | All 4 channels | All 4 channels | All 4 channels |
| Minutes Before/After | Not available | Available | Available |
| `frappe.publish_realtime` | Available | Available | Available |
| Assignment Rules | Available | Available | Available |

---

## See Also

- [references/email-system.md](references/email-system.md) — Email Account, Email Queue, Communication linking, Newsletter, Notification Log
- [references/examples.md](references/examples.md) — Full notification workflow examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common mistakes and fixes
- [references/api-reference.md](references/api-reference.md) — Complete API signatures
- `frappe-core-database` — Database operations referenced in notifications
- `frappe-core-permissions` — Permission model for notification access
