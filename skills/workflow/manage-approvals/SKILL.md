---
name: manage-approvals
description: |
  Manage the human-in-the-loop approval workflow. Check for pending approval requests,
  review approved/rejected items, process decisions, and check for expired requests.
  Use when managing sensitive actions that require human sign-off before execution.
---

# Manage Approvals

Handle the human-in-the-loop approval workflow for sensitive actions.

## When to Create Approval Requests

Always create approval requests for:
- **Payments**: Any financial transaction
- **Email sends**: Especially to new contacts or bulk sends
- **LinkedIn posts**: Any social media content before publishing
- **File deletions**: Any destructive file operations
- **External API calls**: Actions that interact with external services

## Workflow

### 1. Check Pending Approvals
```
List all .md files in vault/Pending_Approval/ (ignore .gitkeep)
For each file, report: action type, priority, creation date, expiry
```

### 2. Review Approved Items
```
List all .md files in vault/Approved/
These have been approved by the human and are ready for execution
For each: read the action details and execute the approved action
After execution, move the file to vault/Done/
```

### 3. Review Rejected Items
```
List all .md files in vault/Rejected/
Log the rejection and move to vault/Done/
```

### 4. Check for Expired Requests
```
For each file in vault/Pending_Approval/:
  Parse the "expires" field from YAML frontmatter
  If expired, flag it and log the expiration
```

### 5. Create New Approval Request
When a sensitive action is needed, create a file in vault/Pending_Approval/:
```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_action_type"
action: action_type
priority: high|medium|low
created: ISO-8601
expires: ISO-8601
status: pending
details:
  key: "value"
---

# Approval Required: Action Title

Description of what will happen if approved.

## How to Respond
- **To Approve**: Move this file to the `/Approved` folder
- **To Reject**: Move this file to the `/Rejected` folder
```

## Important Rules

- Never auto-execute actions that require approval
- Always log approval decisions to vault/Logs/
- Expired requests should be flagged but not auto-rejected
- Include clear descriptions so humans can make informed decisions
