---
name: odoo-accounting
description: |
  Manage Odoo Community accounting: view invoices, payments, and journal entries.
  Generate financial summaries and accounting reports for the vault. Supports
  both direct Odoo JSON-RPC integration and the mcp-odoo-adv MCP server.
  All write operations (posting invoices, recording payments) require human
  approval through the HITL workflow. Read-only operations are auto-approved.
  Use when financial data is needed for the CEO Briefing, when invoices arrive,
  or when accounting records need to be reviewed.
---

# Odoo Accounting Integration

Manage Odoo Community accounting and generate financial reports.

## Setup Requirements

1. **Odoo Community 19+** installed locally (default: http://localhost:8069)
2. Configure in `.env`:
   ```
   ODOO_URL=http://localhost:8069
   ODOO_DB=odoo
   ODOO_USER=admin
   ODOO_PASSWORD=your_odoo_password
   ```
3. In DEV_MODE=true, Odoo operations are simulated with mock data.

## Workflow A: Generate Accounting Summary

```python
from odoo_connector import OdooConnector

# Initialize connector
odoo = OdooConnector(vault_path="./vault")
odoo.authenticate()

# Generate and write summary to vault/Accounting/
summary_path = odoo.write_accounting_summary()
print(f"Summary written: {summary_path}")
```

This creates `vault/Accounting/Summary_YYYY_MM.md` with:
- Total invoiced and received revenue
- Total outgoing payments
- Net revenue calculation
- Detected subscription services

## Workflow B: Review Invoices

Read invoices from Odoo and create action files for outstanding ones:

1. Fetch invoices: `odoo.get_invoices(state='posted')`
2. For unpaid invoices, create `vault/Needs_Action/ODOO_INVOICE_*.md`
3. Planner creates a `PLAN_*.md` with follow-up steps
4. For payment execution, create an approval request in `vault/Pending_Approval/`

## Workflow C: Process Payment (Requires Approval)

Payment processing always requires human approval:

1. Create approval request in `vault/Pending_Approval/`:
```markdown
---
type: approval_request
action: odoo_payment
priority: high
details:
  invoice: "INV/2026/0001"
  amount: "2500.00"
  payee: "Client A"
---

# Approval Required: Process Invoice Payment

## Payment Details
- **Invoice**: INV/2026/0001
- **Amount**: $2,500.00
- **Payee**: Client A

## How to Respond
- **To Approve**: Move this file to `/Approved` folder
- **To Reject**: Move this file to `/Rejected` folder
```

2. After approval, execute via Odoo JSON-RPC:
   - POST to `/jsonrpc` with `account.payment.register` method

## Workflow D: Subscription Audit

Analyze payments for subscription patterns:

```python
# Analyze all payments for subscription patterns
payments = odoo.get_payments()
for payment in payments:
    sub = odoo.analyze_transaction({
        "description": payment["name"],
        "amount": payment["amount"],
        "date": str(payment["date"]),
    })
    if sub:
        print(f"Subscription found: {sub['name']} - ${sub['amount']}/month")
```

Flag subscriptions unused > 30 days for review and create approval requests
to cancel them.

## Log Format
```json
{
  "timestamp": "ISO-8601",
  "action_type": "accounting_summary_generated",
  "actor": "odoo_connector",
  "total_invoiced": 4300.00,
  "total_received": 2500.00,
  "net_revenue": 2500.00,
  "result": "success"
}
```

## Security Notes
- Odoo credentials stored in `.env` (never in vault)
- All payment operations require human approval
- DEV_MODE uses mock data only, no real Odoo calls
- Credentials rotated monthly per security policy
