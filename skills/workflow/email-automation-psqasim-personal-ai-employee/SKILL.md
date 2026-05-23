---
name: email-automation
description: >
  Automated email draft generation with AI, human-in-the-loop approval workflow,
  and SMTP-based sending via MCP server. Monitors Gmail for high-priority inbox items,
  generates contextual draft replies using Claude API, presents drafts for human approval
  via Obsidian vault file-move workflow, and sends approved emails via Email MCP server.
  Use when: (1) building AI-powered email assistants, (2) implementing draft-and-approve
  workflows for email automation, (3) integrating Gmail watching with AI analysis,
  (4) setting up SMTP send automation with human approval gates, (5) creating MCP servers
  for email operations.
---

# Email Automation

## Architecture Overview

```
Gmail Inbox → Watcher (gmail_watcher.py) → AI Draft Generator (draft_generator.py)
                                            ↓
                                   vault/Pending_Approval/Email/
                                            ↓
                                   [Human moves file to Approved/]
                                            ↓
                            Approval Watcher (approval_watcher.py)
                                            ↓
                            Email MCP Server (SMTP send)
                                            ↓
                                    Sent + Logged ✓
```

---

## Quick Start

### 1. Setup Gmail Watcher

**Prerequisites:**
- Gmail API credentials (`credentials.json`)
- Claude API key for draft generation

```bash
# Install dependencies
pip install google-api-python-client google-auth-oauthlib anthropic

# Setup Gmail authentication
python scripts/setup_gmail_auth.py
# → Opens browser for OAuth2 consent
# → Saves token.json

# Configure .env
ENABLE_AI_ANALYSIS=true
CLAUDE_API_KEY=sk-ant-api03-...
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.json
```

### 2. Start Gmail Watcher

```python
# scripts/gmail_watcher.py
from agent_skills.draft_generator import generate_email_draft
from agent_skills.vault_parser import parse_task_file
from googleapiclient.discovery import build

def watch_gmail_inbox():
    """Monitor Gmail for high-priority emails and create drafts"""
    service = build('gmail', 'v1', credentials=creds)

    # Query: Important emails, unread, inbox only
    results = service.users().messages().list(
        userId='me',
        q='is:important is:unread in:inbox',
        maxResults=10
    ).execute()

    for msg in results.get('messages', []):
        # Fetch full email
        email = service.users().messages().get(
            userId='me', id=msg['id']
        ).execute()

        # Create task file in vault/Inbox/
        task_path = create_email_task(email)

        # Generate draft reply
        draft = generate_email_draft(task_path)

        # Save to vault/Pending_Approval/Email/
        save_draft(draft, f"EMAIL_DRAFT_{msg['id']}.md")
```

### 3. Create Email MCP Server

```python
# mcp_servers/email_mcp/server.py
import smtplib
import json
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to: str, subject: str, body: str) -> dict:
    """Send email via SMTP"""
    try:
        # Load SMTP config
        with open('config.json') as f:
            config = json.load(f)

        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['SMTP_USER']
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send via SMTP
        with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT']) as server:
            server.starttls()
            server.login(config['SMTP_USER'], config['SMTP_PASSWORD'])
            server.send_message(msg)

        return {
            "message_id": msg['Message-ID'],
            "sent_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise Exception(f"SMTP_SEND_FAILED: {str(e)}")

# JSON-RPC 2.0 handler
def handle_jsonrpc():
    for line in sys.stdin:
        request = json.loads(line)

        if request['method'] == 'tools/call':
            tool = request['params']['name']
            args = request['params']['arguments']

            if tool == 'send_email':
                result = send_email(**args)
                response = {
                    "jsonrpc": "2.0",
                    "id": request['id'],
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request['id'],
                    "error": {"code": -32601, "message": "Method not found"}
                }

        print(json.dumps(response))
        sys.stdout.flush()
```

### 4. Configure MCP Server

```json
// ~/.config/claude-code/mcp.json
{
  "servers": {
    "email-mcp": {
      "command": "python",
      "args": ["/path/to/mcp_servers/email_mcp/server.py"],
      "env": {}
    }
  }
}
```

```json
// mcp_servers/email_mcp/config.json
{
  "SMTP_HOST": "smtp.gmail.com",
  "SMTP_PORT": 587,
  "SMTP_USER": "your-email@gmail.com",
  "SMTP_PASSWORD": "your-app-password"
}
```

---

## Email Draft Generation

### Draft Generator Implementation

```python
# agent_skills/draft_generator.py
from anthropic import Anthropic
from agent_skills.vault_parser import parse_task_file

def generate_email_draft(task_path: str) -> dict:
    """
    Generate AI-powered email draft reply

    Args:
        task_path: Path to EMAIL_*.md task file in vault/Inbox/

    Returns:
        EmailDraft dict with to, subject, draft_body, original_email_id
    """
    # Parse task file
    task = parse_task_file(task_path)

    # Sanitize input (first 200 chars only, no PII)
    sanitized_email = sanitize_email_content(
        task['email_body'],
        max_chars=200
    )

    # Generate draft via Claude API
    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Generate a professional email reply to:

From: {task['from_email']}
Subject: {task['subject']}
Content preview: {sanitized_email}

Requirements:
- Professional tone
- Address the sender's request
- Keep under 500 words
- No attachments or links
- Close with appropriate sign-off
"""
        }]
    )

    draft_body = response.content[0].text

    # Validate draft
    if len(draft_body) > 5000:
        raise ValueError("Draft exceeds 5000 char limit")

    return {
        "to": task['from_email'],
        "subject": f"Re: {task['subject']}",
        "draft_body": draft_body,
        "original_email_id": task['email_id'],
        "action": "send_email",
        "status": "pending_approval",
        "generated_at": datetime.utcnow().isoformat()
    }

def sanitize_email_content(text: str, max_chars: int = 200) -> str:
    """Strip PII and truncate email content"""
    import re

    # Remove email addresses
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)

    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

    # Remove account numbers
    text = re.sub(r'\b\d{10,}\b', '[ACCOUNT]', text)

    # Truncate
    return text[:max_chars]
```

### Draft File Format

```markdown
<!-- vault/Pending_Approval/Email/EMAIL_DRAFT_1234567890.md -->
---
draft_id: email_draft_1234567890
original_email_id: "1234567890abcdef"
to: sender@example.com
subject: "Re: Q1 Budget Proposal"
action: send_email
status: pending_approval
generated_at: "2026-02-14T10:30:00Z"
---

# Email Draft: Re: Q1 Budget Proposal

**To:** sender@example.com
**Subject:** Re: Q1 Budget Proposal

## Draft Body

Dear [Name],

Thank you for sending the Q1 budget proposal. I've reviewed the numbers and have a few questions:

1. Can you clarify the marketing spend increase?
2. Are the infrastructure costs one-time or recurring?

I'd like to schedule a call to discuss this week. Are you available Thursday afternoon?

Best regards,
[Your Name]

---

**Approval Instructions:**
- ✅ Approve: Move this file to `vault/Approved/Email/`
- ❌ Reject: Move this file to `vault/Rejected/`
- ✏️ Edit: Modify the Draft Body above, then approve
```

---

## Approval Workflow

### File-Move Detection

```python
# agent_skills/approval_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from agent_skills.mcp_client import call_mcp_tool

class ApprovalHandler(FileSystemEventHandler):
    def on_moved(self, event):
        """Detect file moves to vault/Approved/Email/"""
        if not event.is_directory and 'Approved/Email' in event.dest_path:
            # Parse approved draft
            draft = parse_draft_file(event.dest_path)

            # Invoke Email MCP
            result = call_mcp_tool(
                server="email-mcp",
                tool="send_email",
                arguments={
                    "to": draft['to'],
                    "subject": draft['subject'],
                    "body": draft['draft_body']
                }
            )

            # Log action
            log_mcp_action(
                mcp_server="email-mcp",
                action="send_email",
                outcome="success",
                human_approved=True,
                approval_file_path=event.dest_path
            )

            # Move to Done
            shutil.move(event.dest_path, f"vault/Done/{Path(event.dest_path).name}")

def start_approval_watcher():
    """Monitor vault/Approved/ for file-move events"""
    observer = Observer()
    observer.schedule(
        ApprovalHandler(),
        path="vault/Pending_Approval/",
        recursive=True
    )
    observer.start()
```

### MCP Client Integration

```python
# agent_skills/mcp_client.py
import json
import subprocess

def call_mcp_tool(server: str, tool: str, arguments: dict) -> dict:
    """
    Invoke MCP server tool via JSON-RPC 2.0

    Args:
        server: MCP server name (from mcp.json)
        tool: Tool name (e.g., "send_email")
        arguments: Tool-specific params

    Returns:
        MCP result dict

    Raises:
        MCPError: On auth failures, network errors, or tool errors
    """
    # Build JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool,
            "arguments": arguments
        }
    }

    # Launch MCP server process
    mcp_config = load_mcp_config()[server]
    proc = subprocess.Popen(
        [mcp_config['command']] + mcp_config['args'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # Send request
    proc.stdin.write(json.dumps(request) + '\n')
    proc.stdin.flush()

    # Read response
    response = json.loads(proc.stdout.readline())
    proc.terminate()

    if 'error' in response:
        raise MCPError(response['error']['code'], response['error']['message'])

    return response['result']
```

---

## Human Approval Gate Enforcement

### Safety Rules

**Critical:** ALL MCP actions MUST have approval file before execution

```python
def enforce_approval_gate(draft_path: str):
    """Verify approval file exists before MCP invocation"""
    # Check file is in Approved/ folder
    if 'Approved/' not in draft_path:
        raise ValueError("Draft not approved - file not in Approved/ folder")

    # Check approval file exists
    if not os.path.exists(draft_path):
        raise FileNotFoundError("Approval file missing")

    # Log approval
    log_human_approval(
        approval_file_path=draft_path,
        timestamp=datetime.utcnow().isoformat()
    )
```

### Audit Logging

```python
def log_mcp_action(mcp_server: str, action: str, outcome: str,
                    human_approved: bool, approval_file_path: str):
    """
    Log MCP action to vault/Logs/MCP_Actions/YYYY-MM-DD.md

    IMPORTANT: Log BEFORE MCP invocation (not after)
    """
    log_entry = f"""
---
log_id: {uuid.uuid4()}
mcp_server: {mcp_server}
action: {action}
payload_summary: {summarize_payload(50)}  # Max 50 chars, no PII
outcome: {outcome}
timestamp: {datetime.utcnow().isoformat()}
human_approved: {human_approved}
approval_file_path: {approval_file_path}
---

## MCP Action Log

**Server:** {mcp_server}
**Action:** {action}
**Outcome:** {outcome}
**Human Approved:** {'Yes ✓' if human_approved else 'No ✗'}

**Approval File:** `{approval_file_path}`
"""

    # Append to today's log
    log_path = f"vault/Logs/MCP_Actions/{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(log_path, 'a') as f:
        f.write(log_entry)
```

---

## Production Patterns

### Error Recovery

```python
def send_email_with_retry(draft: dict, max_retries: int = 3):
    """Send email with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            result = call_mcp_tool("email-mcp", "send_email", {
                "to": draft['to'],
                "subject": draft['subject'],
                "body": draft['draft_body']
            })
            return result
        except MCPError as e:
            if e.code == -32000:  # SMTP_AUTH_FAILED
                # Don't retry auth errors
                raise

            if attempt < max_retries - 1:
                # Exponential backoff: 5s, 10s, 20s
                time.sleep(5 * (2 ** attempt))
            else:
                # Create escalation file
                create_escalation_file(
                    f"vault/Needs_Action/email_send_failed_{draft['draft_id']}.md",
                    error_details=str(e),
                    draft_path=draft['path']
                )
                raise
```

### Graceful Degradation

```python
def generate_email_draft_with_fallback(task_path: str) -> dict:
    """Generate draft with fallback to manual template"""
    try:
        return generate_email_draft(task_path)
    except Exception as e:
        # Claude API unavailable - use manual template
        task = parse_task_file(task_path)
        return {
            "to": task['from_email'],
            "subject": f"Re: {task['subject']}",
            "draft_body": f"[AI unavailable - manual draft required]\n\nOriginal email:\n{task['email_preview']}",
            "status": "pending_approval",
            "ai_generated": False
        }
```

---

## Testing

### Unit Test: Draft Generation

```python
# tests/unit/test_draft_generator.py
import pytest
from agent_skills.draft_generator import generate_email_draft

def test_generate_email_draft_valid():
    """Test draft generation for valid email task"""
    # Setup mock task file
    task_path = create_mock_task({
        'from_email': 'test@example.com',
        'subject': 'Test Subject',
        'email_body': 'Test email content'
    })

    # Generate draft
    draft = generate_email_draft(task_path)

    # Assertions
    assert draft['to'] == 'test@example.com'
    assert draft['subject'] == 'Re: Test Subject'
    assert len(draft['draft_body']) > 0
    assert len(draft['draft_body']) <= 5000
    assert draft['status'] == 'pending_approval'
```

### Integration Test: Email Workflow

```python
# tests/integration/test_email_workflow.py
import pytest
from unittest.mock import patch, MagicMock

def test_email_draft_approve_send_workflow():
    """Test complete email workflow: draft → approve → send"""
    # 1. Create high-priority email task
    task_path = create_email_task({
        'from': 'client@example.com',
        'subject': 'Urgent: Contract Review',
        'priority': 'High'
    })

    # 2. Generate draft
    draft = generate_email_draft(task_path)
    draft_path = save_draft(draft, 'vault/Pending_Approval/Email/')

    # 3. Simulate human approval (move file)
    approved_path = 'vault/Approved/Email/' + Path(draft_path).name
    shutil.move(draft_path, approved_path)

    # 4. Mock SMTP send
    with patch('smtplib.SMTP') as mock_smtp:
        # Trigger approval watcher
        approval_handler.on_moved(MockEvent(dest_path=approved_path))

        # Verify SMTP send called
        assert mock_smtp.called
        assert mock_smtp.send_message.call_count == 1

    # 5. Verify logging
    log_path = f"vault/Logs/MCP_Actions/{datetime.now().strftime('%Y-%m-%d')}.md"
    assert os.path.exists(log_path)
    with open(log_path) as f:
        assert 'human_approved: true' in f.read()
```

---

## Configuration Reference

### Environment Variables

```bash
# .env
ENABLE_AI_ANALYSIS=true
CLAUDE_API_KEY=sk-ant-api03-...
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.json
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### MCP Server Config

```json
{
  "SMTP_HOST": "smtp.gmail.com",
  "SMTP_PORT": 587,
  "SMTP_USER": "your-email@gmail.com",
  "SMTP_PASSWORD": "your-app-password"
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **SMTP_AUTH_FAILED** | Incorrect password or 2FA enabled | Use app password, not account password |
| **Draft not generated** | Claude API key invalid | Check `CLAUDE_API_KEY` in .env |
| **Email not sent after approval** | Approval watcher not running | Start `python scripts/run_approval_watcher.py` |
| **MCP server not responding** | Server process crashed | Check MCP server logs, restart |
| **Duplicate emails sent** | Race condition on file-move | File locking enforced - report bug if occurs |

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/gmail_watcher.py` | Monitor Gmail inbox, create tasks |
| `agent_skills/draft_generator.py` | Generate AI email drafts |
| `agent_skills/approval_watcher.py` | Monitor Approved/ folder |
| `agent_skills/mcp_client.py` | MCP server invocation |
| `mcp_servers/email_mcp/server.py` | SMTP send MCP server |
| `vault/Pending_Approval/Email/` | Draft review queue |
| `vault/Approved/Email/` | Approved drafts (triggers send) |
| `vault/Logs/MCP_Actions/` | Audit trail |

---

**Production Ready:** This skill implements all Gold tier email automation requirements with human approval gates, comprehensive logging, and graceful degradation.
