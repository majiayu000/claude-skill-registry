---
name: whatsapp-automation
description: >
  Monitor WhatsApp Web via Playwright browser automation, detect important messages using
  keyword matching, generate AI-powered draft replies, and send approved messages with
  human-in-the-loop approval. Includes QR code authentication, session persistence,
  message polling, and Playwright-based send automation via MCP server. Use when:
  (1) building WhatsApp automation for business messaging, (2) implementing keyword-based
  message priority detection, (3) creating browser automation with Playwright for messaging
  apps, (4) setting up session management for WhatsApp Web, (5) building MCP servers for
  Playwright-based automation.
---

# WhatsApp Automation

## Architecture Overview

```
WhatsApp Web → Playwright Watcher (whatsapp_watcher.py) → Keyword Detection
                                                               ↓
                                                     vault/Inbox/WHATSAPP_*.md
                                                               ↓
                                              AI Draft Generator (draft_generator.py)
                                                               ↓
                                                  vault/Pending_Approval/WhatsApp/
                                                               ↓
                                                  [Human moves file to Approved/]
                                                               ↓
                                              Approval Watcher (approval_watcher.py)
                                                               ↓
                                              WhatsApp MCP (Playwright send)
                                                               ↓
                                                          Sent + Logged ✓
```

---

## Quick Start

### 1. Install Playwright

```bash
# Install Playwright with Chromium
pip install playwright==1.40.0
playwright install chromium

# Configure .env
WHATSAPP_SESSION_PATH=/home/user/.whatsapp_session
WHATSAPP_POLL_INTERVAL=30
WHATSAPP_KEYWORDS=urgent,meeting,payment,deadline,invoice,asap,help,client,contract
```

### 2. Setup WhatsApp Web Authentication

```python
# scripts/whatsapp_qr_setup.py
from playwright.sync_api import sync_playwright
import os

def setup_whatsapp_qr():
    """Display QR code for WhatsApp Web authentication"""
    session_path = os.getenv('WHATSAPP_SESSION_PATH')

    with sync_playwright() as p:
        # Launch browser in headed mode
        browser = p.chromium.launch(
            headless=False,
            user_data_dir=session_path
        )

        page = browser.new_page()
        page.goto('https://web.whatsapp.com')

        print("📱 Scan the QR code with your phone...")
        print("Waiting for authentication...")

        # Wait for successful login (chat list appears)
        page.wait_for_selector('div[data-testid="chat-list"]', timeout=120000)

        print("✅ Authentication successful!")
        print(f"Session saved to: {session_path}")

        # Keep browser open for 5 seconds to confirm
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    setup_whatsapp_qr()
```

Run QR setup:
```bash
python scripts/whatsapp_qr_setup.py
# → Browser opens with QR code
# → Scan with phone
# → Session persisted to WHATSAPP_SESSION_PATH
```

### 3. WhatsApp Watcher with Keyword Detection

```python
# scripts/whatsapp_watcher.py
from playwright.sync_api import sync_playwright
import os
import time

# WhatsApp Web selectors (Feb 2026)
SELECTORS = {
    'chat_list': 'div[data-testid="chat-list"]',
    'chat_item': 'div[data-testid="cell-frame-container"]',
    'unread_badge': 'span[data-testid="icon-unread"]',
    'chat_name': 'span[title]',
    'last_message': 'span.selectable-text',
    'qr_code': 'canvas[aria-label="Scan this QR code to link a device!"]'
}

def watch_whatsapp_messages():
    """Monitor WhatsApp Web for new messages and detect keywords"""
    session_path = os.getenv('WHATSAPP_SESSION_PATH')
    poll_interval = int(os.getenv('WHATSAPP_POLL_INTERVAL', 30))
    keywords = os.getenv('WHATSAPP_KEYWORDS', '').split(',')

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            user_data_dir=session_path
        )

        page = browser.new_page()
        page.goto('https://web.whatsapp.com')

        # Check if session expired (QR code present)
        if page.is_visible(SELECTORS['qr_code']):
            print("❌ WhatsApp session expired!")
            create_session_expired_alert()
            browser.close()
            return

        # Wait for chat list
        page.wait_for_selector(SELECTORS['chat_list'], timeout=30000)

        print("✅ WhatsApp watcher active")

        # Poll for new messages
        while True:
            # Find chats with unread badges
            chats = page.query_selector_all(SELECTORS['chat_item'])

            for chat in chats:
                # Check if chat has unread badge
                if not chat.query_selector(SELECTORS['unread_badge']):
                    continue

                # Extract chat info
                chat_name = chat.query_selector(SELECTORS['chat_name']).inner_text()
                last_msg = chat.query_selector(SELECTORS['last_message']).inner_text()

                # Keyword matching
                priority = 'Medium'
                matched_keywords = []
                for keyword in keywords:
                    if keyword.lower() in last_msg.lower():
                        priority = 'High'
                        matched_keywords.append(keyword)

                # Create task file
                create_whatsapp_task(
                    chat_name=chat_name,
                    message_preview=last_msg[:200],
                    priority=priority,
                    keywords_matched=matched_keywords
                )

                print(f"📩 New WhatsApp from {chat_name} - Priority: {priority}")

            time.sleep(poll_interval)

def create_session_expired_alert():
    """Create alert file for session expiry"""
    alert = """
---
type: alert
severity: high
action_required: true
---

# WhatsApp Session Expired

Your WhatsApp Web session has expired. Re-authenticate to continue monitoring.

**Steps to fix:**
1. Run: `python scripts/whatsapp_qr_setup.py`
2. Scan QR code with your phone
3. Restart watcher: `python scripts/whatsapp_watcher.py`
"""
    with open('vault/Needs_Action/whatsapp_session_expired.md', 'w') as f:
        f.write(alert)
```

---

## WhatsApp MCP Server

### Server Implementation

```python
# mcp_servers/whatsapp_mcp/server.py
from playwright.sync_api import sync_playwright
import json
import sys
import os

# WhatsApp Web selectors
SELECTORS = {
    'search_box': 'div[contenteditable="true"][data-tab="3"]',
    'message_input': 'div[contenteditable="true"][data-tab="10"]',
    'send_button': 'button[data-tab="11"]',
    'message_in_history': 'div.message-out span.selectable-text'
}

def authenticate_qr() -> dict:
    """Display QR code for authentication"""
    session_path = os.getenv('WHATSAPP_SESSION_PATH')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, user_data_dir=session_path)
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')

        # Check if QR code present
        qr_selector = 'canvas[aria-label="Scan this QR code to link a device!"]'
        if page.is_visible(qr_selector):
            # QR code displayed - save as base64
            qr_element = page.query_selector(qr_selector)
            qr_screenshot = qr_element.screenshot()
            import base64
            qr_base64 = base64.b64encode(qr_screenshot).decode()

            browser.close()
            return {
                "status": "waiting",
                "qr_code_base64": qr_base64
            }
        else:
            # Already authenticated
            browser.close()
            return {
                "status": "authenticated"
            }

def send_message(chat_id: str, message: str) -> dict:
    """Send WhatsApp message via Playwright automation"""
    session_path = os.getenv('WHATSAPP_SESSION_PATH')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, user_data_dir=session_path)
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')

        # Wait for chat list
        page.wait_for_selector('div[data-testid="chat-list"]', timeout=30000)

        # Search for chat
        search_box = page.query_selector(SELECTORS['search_box'])
        search_box.click()
        search_box.fill(chat_id)
        page.wait_for_timeout(1000)

        # Click first result
        page.query_selector('div[data-testid="cell-frame-container"]').click()
        page.wait_for_timeout(1000)

        # Type message
        msg_input = page.query_selector(SELECTORS['message_input'])
        msg_input.click()
        msg_input.fill(message)
        page.wait_for_timeout(500)

        # Click send button
        page.query_selector(SELECTORS['send_button']).click()

        # Confirm message in history
        page.wait_for_selector(SELECTORS['message_in_history'], timeout=5000)

        browser.close()

        return {
            "message_id": f"whatsapp_{chat_id}_{int(time.time())}",
            "sent_at": datetime.utcnow().isoformat()
        }

# JSON-RPC 2.0 handler
def handle_jsonrpc():
    """MCP server main loop"""
    for line in sys.stdin:
        request = json.loads(line)

        try:
            if request['method'] == 'tools/call':
                tool = request['params']['name']
                args = request['params']['arguments']

                if tool == 'authenticate_qr':
                    result = authenticate_qr()
                elif tool == 'send_message':
                    result = send_message(**args)
                else:
                    raise ValueError(f"Unknown tool: {tool}")

                response = {
                    "jsonrpc": "2.0",
                    "id": request['id'],
                    "result": result
                }
            elif request['method'] == 'tools/list':
                response = {
                    "jsonrpc": "2.0",
                    "id": request['id'],
                    "result": {
                        "tools": [
                            {
                                "name": "authenticate_qr",
                                "description": "Display QR code for WhatsApp Web authentication",
                                "inputSchema": {"type": "object", "properties": {}}
                            },
                            {
                                "name": "send_message",
                                "description": "Send WhatsApp message via Playwright",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "chat_id": {"type": "string"},
                                        "message": {"type": "string"}
                                    },
                                    "required": ["chat_id", "message"]
                                }
                            }
                        ]
                    }
                }
            else:
                raise ValueError(f"Unknown method: {request['method']}")

        except Exception as e:
            response = {
                "jsonrpc": "2.0",
                "id": request['id'],
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }

        print(json.dumps(response))
        sys.stdout.flush()

if __name__ == "__main__":
    handle_jsonrpc()
```

### MCP Configuration

```json
// ~/.config/claude-code/mcp.json
{
  "servers": {
    "whatsapp-mcp": {
      "command": "python",
      "args": ["/path/to/mcp_servers/whatsapp_mcp/server.py"],
      "env": {
        "WHATSAPP_SESSION_PATH": "/home/user/.whatsapp_session"
      }
    }
  }
}
```

---

## Draft Generation

### WhatsApp Draft Generator

```python
# agent_skills/draft_generator.py (extension)
def generate_whatsapp_draft(task_path: str) -> dict:
    """
    Generate context-aware WhatsApp reply

    Args:
        task_path: Path to WHATSAPP_*.md task file

    Returns:
        WhatsAppDraft dict with chat_id, draft_body, keywords_matched
    """
    task = parse_task_file(task_path)

    # Sanitize input (first 200 chars, remove phone numbers)
    sanitized_msg = sanitize_whatsapp_content(
        task['message_preview'],
        max_chars=200
    )

    # Generate draft via Claude API
    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Generate a professional WhatsApp reply to:

From: {task['from_contact']}
Message: {sanitized_msg}
Keywords matched: {', '.join(task.get('keywords_matched', []))}

Requirements:
- Professional but conversational tone
- Keep under 500 characters
- Address the urgency if keywords matched
- No emojis unless appropriate for business context
- Clear call-to-action if needed
"""
        }]
    )

    draft_body = response.content[0].text

    # Validate draft
    if len(draft_body) > 500:
        draft_body = draft_body[:497] + "..."

    return {
        "chat_id": task['from_contact'],
        "draft_body": draft_body,
        "original_message_id": task['message_id'],
        "keywords_matched": task.get('keywords_matched', []),
        "action": "send_message",
        "status": "pending_approval",
        "generated_at": datetime.utcnow().isoformat()
    }

def sanitize_whatsapp_content(text: str, max_chars: int = 200) -> str:
    """Strip PII and media from WhatsApp content"""
    import re

    # Remove phone numbers
    text = re.sub(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', '[PHONE]', text)

    # Remove media indicators
    text = text.replace('[Image]', '').replace('[Video]', '').replace('[Audio]', '')

    return text[:max_chars]
```

### Draft File Format

```markdown
<!-- vault/Pending_Approval/WhatsApp/WHATSAPP_DRAFT_client_abc_1234.md -->
---
draft_id: whatsapp_draft_client_abc_1234
original_message_id: "msg_1234567890"
chat_id: "Client ABC"
from_contact: "Client ABC"
action: send_message
status: pending_approval
keywords_matched: ["urgent", "payment"]
generated_at: "2026-02-14T15:30:00Z"
---

# WhatsApp Draft: Client ABC

**To:** Client ABC
**Keywords:** urgent, payment

## Draft Body

Hi! I received your message about the urgent payment. I'll process the invoice immediately and send you the payment confirmation by end of day today.

Is there anything specific you need in the payment receipt?

---

**Approval Instructions:**
- ✅ Approve: Move to `vault/Approved/WhatsApp/`
- ❌ Reject: Move to `vault/Rejected/`
- ✏️ Edit: Modify Draft Body above, then approve
```

---

## Production Patterns

### Session Management

```python
def check_whatsapp_session_valid() -> bool:
    """Verify WhatsApp Web session is still valid"""
    session_path = os.getenv('WHATSAPP_SESSION_PATH')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, user_data_dir=session_path)
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')

        # Check for QR code (session expired)
        qr_visible = page.is_visible('canvas[aria-label*="QR code"]', timeout=5000)

        browser.close()

        if qr_visible:
            create_session_expired_alert()
            return False

        return True
```

### Error Recovery

```python
def send_whatsapp_with_retry(draft: dict, max_retries: int = 3):
    """Send WhatsApp message with retry logic"""
    for attempt in range(max_retries):
        try:
            result = call_mcp_tool("whatsapp-mcp", "send_message", {
                "chat_id": draft['chat_id'],
                "message": draft['draft_body']
            })
            return result

        except MCPError as e:
            if 'SESSION_EXPIRED' in str(e):
                # Don't retry session expiry
                create_session_expired_alert()
                raise

            if 'CHAT_NOT_FOUND' in str(e):
                # Don't retry invalid chat
                raise

            if attempt < max_retries - 1:
                # Exponential backoff
                time.sleep(5 * (2 ** attempt))
            else:
                # Create escalation
                create_escalation_file(
                    f"vault/Needs_Action/whatsapp_send_failed_{draft['draft_id']}.md",
                    error_details=str(e)
                )
                raise
```

### Selector Resilience

```python
# Store selectors in config for easy updates when WhatsApp changes UI
WHATSAPP_SELECTORS = {
    "v1": {  # Feb 2026
        "search_box": 'div[contenteditable="true"][data-tab="3"]',
        "message_input": 'div[contenteditable="true"][data-tab="10"]',
        "send_button": 'button[data-tab="11"]'
    },
    "v2": {  # Fallback selectors
        "search_box": 'div[title="Search input textbox"]',
        "message_input": 'div[title="Type a message"]',
        "send_button": 'span[data-icon="send"]'
    }
}

def get_selector(element_name: str) -> str:
    """Get WhatsApp selector with fallback"""
    for version in ['v1', 'v2']:
        selector = WHATSAPP_SELECTORS[version].get(element_name)
        if page.is_visible(selector, timeout=1000):
            return selector

    raise ValueError(f"WhatsApp UI changed - update selectors for {element_name}")
```

---

## Testing

### Integration Test

```python
# tests/integration/test_whatsapp_workflow.py
from unittest.mock import patch, MagicMock

def test_whatsapp_draft_approve_send():
    """Test WhatsApp workflow: keyword detection → draft → approve → send"""
    # 1. Create WhatsApp task with urgent keyword
    task = create_whatsapp_task({
        'from_contact': 'Test Client',
        'message_preview': 'Urgent: need invoice ASAP',
        'priority': 'High',
        'keywords_matched': ['urgent', 'invoice', 'asap']
    })

    # 2. Generate draft
    draft = generate_whatsapp_draft(task)
    assert 'urgent' in draft['draft_body'].lower()
    assert len(draft['draft_body']) <= 500

    # 3. Save to Pending_Approval
    draft_path = save_draft(draft, 'vault/Pending_Approval/WhatsApp/')

    # 4. Mock Playwright send
    with patch('playwright.sync_api.sync_playwright') as mock_pw:
        # Simulate approval
        approved_path = 'vault/Approved/WhatsApp/' + Path(draft_path).name
        shutil.move(draft_path, approved_path)

        # Trigger approval watcher
        approval_handler.on_moved(MockEvent(dest_path=approved_path))

        # Verify Playwright called
        assert mock_pw.called

    # 5. Verify logging
    log_path = f"vault/Logs/MCP_Actions/{datetime.now().strftime('%Y-%m-%d')}.md"
    assert os.path.exists(log_path)
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **Session expired** | WhatsApp logged out on phone | Run `whatsapp_qr_setup.py` to re-authenticate |
| **Selectors not found** | WhatsApp UI updated | Update `WHATSAPP_SELECTORS` in server.py |
| **Message not sent** | Chat name mismatch | Use exact chat name from WhatsApp Web |
| **Browser launch failed** | Chromium not installed | Run `playwright install chromium` |
| **Watcher not detecting** | Poll interval too high | Reduce `WHATSAPP_POLL_INTERVAL` in .env |

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/whatsapp_watcher.py` | Poll WhatsApp Web, detect keywords |
| `scripts/whatsapp_qr_setup.py` | QR authentication setup |
| `agent_skills/draft_generator.py` | Generate WhatsApp drafts |
| `mcp_servers/whatsapp_mcp/server.py` | Playwright send automation |
| `vault/Pending_Approval/WhatsApp/` | Draft review queue |
| `vault/Approved/WhatsApp/` | Approved drafts (triggers send) |

---

**Production Ready:** Includes session management, selector fallbacks, keyword detection, and comprehensive error handling for WhatsApp Web automation.
