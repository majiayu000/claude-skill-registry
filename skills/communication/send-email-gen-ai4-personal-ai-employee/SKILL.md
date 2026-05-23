---
name: send-email
description: |
  Send emails via Gmail API as an MCP-style external action. Drafts emails,
  creates approval requests for external communications, and sends after
  human approval. Use when an email needs to be sent as part of processing
  a task or responding to a communication.
---

# Send Email (Gmail MCP Action)

Send emails via the Gmail API with human-in-the-loop approval.

## Workflow

### 1. Draft the Email
Based on the task context, draft an email with:
- **To**: Recipient email address
- **Subject**: Clear, concise subject line
- **Body**: Professional email body

### 2. Check if Approval is Needed

**Always require approval for:**
- Emails to new/unknown contacts
- Bulk emails
- Emails containing financial information
- Emails with attachments

**Auto-approve for:**
- Replies to known contacts (if configured in Company_Handbook.md)

### 3. Create Approval Request
For emails requiring approval, create in `vault/Pending_Approval/`:

```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_email_send"
action: email_send
priority: medium
created: ISO-8601
expires: ISO-8601
status: pending
details:
  to: "recipient@example.com"
  subject: "Email Subject"
  has_attachment: false
---

# Approval Required: Send Email

## Email Details
- **To**: recipient@example.com
- **Subject**: Email Subject
- **Body Preview**: First 200 chars...

## Full Email Body
[Complete email text]

## How to Respond
- **To Approve**: Move this file to the `/Approved` folder
- **To Reject**: Move this file to the `/Rejected` folder
```

### 4. Send (After Approval)
Once approved, use the Gmail API to send:

```python
# Using gmail API (requires google-api-python-client)
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

message = MIMEText(body)
message['to'] = recipient
message['subject'] = subject
raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

service.users().messages().send(
    userId='me',
    body={'raw': raw}
).execute()
```

In DEV_MODE/DRY_RUN: Log the intended action instead of actually sending.

### 5. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "recipient@example.com",
  "parameters": {"subject": "Email Subject"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### 6. Update Dashboard
After sending, update the dashboard with the action.

## Important Rules
- **NEVER send emails without approval** unless auto-approve rules match
- Always use the Company_Handbook.md rules for tone and content
- Check DRY_RUN mode before actual sending
- Log every send attempt (success or failure)
- Never include credentials in log entries or vault files
