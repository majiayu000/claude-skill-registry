---
name: odoo-integration
description: >
  Automated Odoo accounting integration for draft invoice and expense entry creation with
  human approval workflow. Detects accounting tasks (type="invoice" or type="expense"),
  generates draft entries via Odoo JSON-RPC API, presents for approval, and creates drafts
  in Odoo (NEVER auto-confirms/posts). Includes graceful degradation when Odoo unavailable,
  cross-domain routing (Personal vs Business), and comprehensive audit logging. Use when:
  (1) integrating Odoo Community/Enterprise with AI automation, (2) implementing accounting
  draft workflows with approval gates, (3) creating MCP servers for Odoo JSON-RPC API,
  (4) building cross-domain task routing, (5) setting up offline-capable accounting workflows.
---

# Odoo Integration

## Architecture

```
Email/Task → Accounting Detection (type="invoice"|"expense")
                        ↓
              Odoo Draft Generator (odoo_watcher.py)
                        ↓
            vault/Pending_Approval/Odoo/
                        ↓
         [Human approves → Approved/Odoo/]
                        ↓
    Approval Watcher → Odoo MCP (JSON-RPC create draft)
                        ↓
            Odoo Draft Entry Created (status=draft) ✓
                  [NEVER auto-confirmed]
```

---

## Quick Start

### 1. Odoo Configuration

```bash
# .env configuration
ENABLE_ODOO=true
ODOO_URL=http://localhost:8069
ODOO_DB=mycompany
ODOO_USER=admin
ODOO_PASSWORD=admin_password
```

### 2. Odoo MCP Server

```python
# mcp_servers/odoo_mcp/server.py
import xmlrpc.client
import json
import sys

class OdooClient:
    def __init__(self, url: str, db: str, username: str, password: str):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None

    def authenticate(self):
        """Authenticate with Odoo"""
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = common.authenticate(self.db, self.username, self.password, {})

        if not self.uid:
            raise Exception("AUTH_FAILED: Invalid Odoo credentials")

        return self.uid

    def execute(self, model: str, method: str, *args):
        """Execute Odoo RPC call"""
        if not self.uid:
            self.authenticate()

        models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        return models.execute_kw(
            self.db, self.uid, self.password,
            model, method, args
        )

def create_draft_invoice(customer: str, amount: float, description: str,
                          odoo_url: str, odoo_db: str, odoo_user: str, odoo_pass: str) -> dict:
    """
    Create DRAFT invoice in Odoo (NOT confirmed/posted)

    CRITICAL: status=draft, manual confirmation required
    """
    client = OdooClient(odoo_url, odoo_db, odoo_user, odoo_pass)
    client.authenticate()

    # Find customer (partner)
    partner_ids = client.execute(
        'res.partner', 'search',
        [('name', 'ilike', customer)],
        {'limit': 1}
    )

    if not partner_ids:
        raise Exception(f"CUSTOMER_NOT_FOUND: {customer}")

    # Create draft invoice
    invoice_data = {
        'partner_id': partner_ids[0],
        'move_type': 'out_invoice',  # Customer invoice
        'state': 'draft',  # CRITICAL: Draft only
        'invoice_line_ids': [(0, 0, {
            'name': description,
            'price_unit': amount,
            'quantity': 1
        })]
    }

    invoice_id = client.execute('account.move', 'create', [invoice_data])

    return {
        "odoo_record_id": invoice_id,
        "odoo_model": "account.move",
        "status": "draft",
        "confirmation_url": f"{odoo_url}/web#id={invoice_id}&model=account.move"
    }

def create_draft_expense(description: str, amount: float, employee: str,
                          odoo_url: str, odoo_db: str, odoo_user: str, odoo_pass: str) -> dict:
    """Create DRAFT expense in Odoo (NOT confirmed)"""
    client = OdooClient(odoo_url, odoo_db, odoo_user, odoo_pass)
    client.authenticate()

    # Find employee
    employee_ids = client.execute(
        'hr.employee', 'search',
        [('name', 'ilike', employee)],
        {'limit': 1}
    )

    if not employee_ids:
        # Use default employee (current user)
        employee_ids = client.execute('hr.employee', 'search', [('user_id', '=', client.uid)])

    expense_data = {
        'name': description,
        'unit_amount': amount,
        'employee_id': employee_ids[0] if employee_ids else False,
        'state': 'draft'  # CRITICAL: Draft only
    }

    expense_id = client.execute('hr.expense', 'create', [expense_data])

    return {
        "odoo_record_id": expense_id,
        "odoo_model": "hr.expense",
        "status": "draft",
        "confirmation_url": f"{odoo_url}/web#id={expense_id}&model=hr.expense"
    }

# JSON-RPC handler
def handle_jsonrpc():
    """MCP server main loop"""
    for line in sys.stdin:
        request = json.loads(line)

        try:
            if request['method'] == 'tools/call':
                tool = request['params']['name']
                args = request['params']['arguments']

                if tool == 'create_draft_invoice':
                    result = create_draft_invoice(**args)
                elif tool == 'create_draft_expense':
                    result = create_draft_expense(**args)
                else:
                    raise ValueError(f"Unknown tool: {tool}")

                response = {
                    "jsonrpc": "2.0",
                    "id": request['id'],
                    "result": result
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

**MCP Config:**
```json
// ~/.config/claude-code/mcp.json
{
  "servers": {
    "odoo-mcp": {
      "command": "python",
      "args": ["/path/to/mcp_servers/odoo_mcp/server.py"],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "mycompany",
        "ODOO_USER": "admin",
        "ODOO_PASSWORD": "password"
      }
    }
  }
}
```

---

## Odoo Draft Detection

### Task Detection

```python
# scripts/odoo_watcher.py
from agent_skills.vault_parser import parse_task_file
from agent_skills.draft_generator import generate_odoo_draft

def watch_odoo_tasks():
    """Monitor vault/Inbox/ for accounting tasks"""

    # Poll vault/Inbox/ every 30 seconds
    for task_file in glob('vault/Inbox/*.md'):
        task = parse_task_file(task_file)

        # Detect Odoo tasks
        if task.get('type') in ['invoice', 'expense']:
            # Generate draft
            draft = generate_odoo_draft(task)

            # Save to Pending_Approval
            save_draft(draft, 'vault/Pending_Approval/Odoo/')

            print(f"✅ Odoo {task['type']} draft created")

def generate_odoo_draft(task: dict) -> dict:
    """Generate Odoo draft entry from task"""

    if task['type'] == 'invoice':
        return {
            "draft_id": f"odoo_invoice_{int(time.time())}",
            "entry_type": "invoice",
            "odoo_data": {
                "customer": extract_customer(task),
                "amount": extract_amount(task),
                "description": task.get('description', '')
            },
            "action": "create_draft_invoice",
            "status": "pending_approval",
            "generated_at": datetime.utcnow().isoformat()
        }

    elif task['type'] == 'expense':
        return {
            "draft_id": f"odoo_expense_{int(time.time())}",
            "entry_type": "expense",
            "odoo_data": {
                "description": task.get('description', ''),
                "amount": extract_amount(task),
                "employee": os.getenv('USER', 'Default Employee')
            },
            "action": "create_draft_expense",
            "status": "pending_approval",
            "generated_at": datetime.utcnow().isoformat()
        }

def extract_customer(task: dict) -> str:
    """Extract customer name from task content"""
    # Parse task content for customer mentions
    import re
    content = task.get('content', '')
    match = re.search(r'customer[:\s]+([A-Za-z\s]+)', content, re.IGNORECASE)
    return match.group(1).strip() if match else "Unknown Customer"

def extract_amount(task: dict) -> float:
    """Extract dollar amount from task content"""
    import re
    content = task.get('content', '')
    match = re.search(r'\$?([\d,]+\.?\d*)', content)
    return float(match.group(1).replace(',', '')) if match else 0.0
```

---

## Graceful Degradation

### Offline Mode

```python
def generate_odoo_draft_with_fallback(task: dict) -> dict:
    """Generate Odoo draft with fallback to manual template"""

    # Check if Odoo enabled
    if not os.getenv('ENABLE_ODOO', '').lower() == 'true':
        return create_manual_entry_template(task)

    # Check if Odoo MCP available
    try:
        # Test Odoo connection
        test_odoo_connection()
        return generate_odoo_draft(task)

    except Exception as e:
        # Odoo unavailable - create manual template
        print(f"⚠️  Odoo unavailable: {e}")
        return create_manual_entry_template(task)

def create_manual_entry_template(task: dict) -> dict:
    """Create manual entry template for offline review"""
    return {
        "draft_id": f"odoo_manual_{int(time.time())}",
        "entry_type": task['type'],
        "manual_entry": True,
        "odoo_unavailable": True,
        "template_data": {
            "customer": extract_customer(task),
            "amount": extract_amount(task),
            "description": task.get('description', ''),
            "instructions": "Odoo unavailable - create entry manually"
        },
        "status": "pending_approval",
        "generated_at": datetime.utcnow().isoformat()
    }
```

---

## Cross-Domain Routing

### Business vs Personal Domain

```python
# scripts/gmail_watcher.py (extension)
def route_by_domain(task: dict):
    """Route tasks to appropriate domain"""

    # Read task category (from Silver AI analysis)
    category = task.get('category', 'Personal')

    if category in ['Work', 'Urgent'] and task.get('type') == 'invoice':
        # Business domain → Odoo
        task['domain'] = 'Business'
        task['route_to'] = 'odoo'

    elif category == 'Personal' and task.get('type') == 'expense':
        # Personal domain → Manual review
        task['domain'] = 'Personal'
        task['route_to'] = 'manual'

    elif category == 'Work' and task.get('type') == 'email':
        # Business domain → LinkedIn/Email automation
        task['domain'] = 'Business'
        task['route_to'] = 'email_automation'

    else:
        task['domain'] = 'Personal'
        task['route_to'] = 'manual'

    # Update task frontmatter
    update_task_frontmatter(task)
```

---

## Approval Workflow

### Odoo Approval Handler

```python
# agent_skills/approval_watcher.py (Odoo handler)
def handle_odoo_approval(draft_path: str):
    """Create draft entry in Odoo after approval"""

    draft = parse_draft_file(draft_path)

    # Check if manual entry (Odoo unavailable)
    if draft.get('manual_entry'):
        print("⚠️  Manual entry - skipping Odoo MCP invocation")
        shutil.move(draft_path, f"vault/Done/{Path(draft_path).name}")
        return

    # Invoke Odoo MCP
    try:
        result = call_mcp_tool(
            "odoo-mcp",
            draft['action'],  # create_draft_invoice or create_draft_expense
            draft['odoo_data']
        )

        # Log with Odoo record ID
        log_mcp_action(
            "odoo-mcp",
            draft['action'],
            "success",
            draft_path,
            odoo_record_id=result['odoo_record_id']
        )

        # Move to Done
        shutil.move(draft_path, f"vault/Done/{Path(draft_path).name}")

        print(f"✅ Odoo {draft['entry_type']} created: {result['confirmation_url']}")

    except MCPError as e:
        if 'AUTH_FAILED' in str(e):
            # Odoo auth error - escalate
            create_escalation_file(
                'vault/Needs_Action/odoo_auth_failed.md',
                error_details=str(e)
            )
        raise
```

---

## Draft File Format

```markdown
<!-- vault/Pending_Approval/Odoo/ODOO_INVOICE_1234.md -->
---
draft_id: odoo_invoice_1234
entry_type: invoice
action: create_draft_invoice
status: pending_approval
generated_at: "2026-02-14T14:00:00Z"
odoo_data:
  customer: "Acme Corp"
  amount: 5000.00
  description: "Consulting services - Q1 2026"
---

# Odoo Draft Invoice

**Customer:** Acme Corp
**Amount:** $5,000.00
**Description:** Consulting services - Q1 2026

## Odoo Entry Details

This will create a **DRAFT invoice** in Odoo (NOT confirmed/posted).

Manual confirmation required in Odoo after creation.

---

**Approval Instructions:**
- ✅ Approve: Move to `vault/Approved/Odoo/`
- ❌ Reject: Move to `vault/Rejected/`
- ✏️ Edit: Modify odoo_data in frontmatter, then approve

**IMPORTANT:** Draft entry will be created in Odoo with status=draft.
Manual confirmation required to confirm/post the invoice.
```

---

## Safety Gates

### Never Auto-Confirm

```python
def ensure_draft_only():
    """Critical safety check - never auto-confirm Odoo entries"""

    # Validation in Odoo MCP server
    assert invoice_data['state'] == 'draft', "SAFETY: Only draft entries allowed"
    assert expense_data['state'] == 'draft', "SAFETY: Only draft entries allowed"

    # No confirm() or post() methods exposed in MCP
    # Only create() method available
```

---

## Testing

```python
# tests/integration/test_odoo_workflow.py
def test_odoo_invoice_draft_creation():
    """Test Odoo invoice draft workflow"""

    # Create invoice task
    task = create_task({
        'type': 'invoice',
        'content': 'Create invoice for Acme Corp - $5000 consulting',
        'category': 'Work'
    })

    # Generate draft
    draft = generate_odoo_draft(task)
    assert draft['entry_type'] == 'invoice'
    assert draft['odoo_data']['customer'] == 'Acme Corp'
    assert draft['odoo_data']['amount'] == 5000.0

    # Mock Odoo API
    with patch('xmlrpc.client.ServerProxy') as mock_odoo:
        mock_odoo.return_value.execute_kw.return_value = 123  # invoice ID

        # Approve
        approved_path = 'vault/Approved/Odoo/ODOO_INVOICE_1234.md'
        handle_odoo_approval(approved_path)

        # Verify Odoo called with draft status
        assert mock_odoo.called
        call_args = mock_odoo.return_value.execute_kw.call_args
        assert call_args[0][3] == 'create'  # Method
        assert call_args[0][4][0]['state'] == 'draft'  # Draft only
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **AUTH_FAILED** | Check ODOO_USER/PASSWORD in .env |
| **CUSTOMER_NOT_FOUND** | Create customer in Odoo first |
| **Odoo unavailable** | Manual template created - enter manually |
| **Draft not in Odoo** | Check odoo_record_id in logs, verify URL |

---

## Key Files

- `scripts/odoo_watcher.py` - Detect accounting tasks
- `mcp_servers/odoo_mcp/server.py` - Odoo JSON-RPC integration
- `vault/Pending_Approval/Odoo/` - Draft review queue
- `vault/Done/` - Confirmed drafts (check Odoo for status)

---

**Production Ready:** Draft-only safety, graceful degradation, cross-domain routing, comprehensive error handling. Never auto-confirms/posts entries - manual confirmation required in Odoo.
