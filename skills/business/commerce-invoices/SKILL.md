---
name: commerce-invoices
description: Manage invoices and overdue billing. Use when running `stateset-invoices` or reconciling invoice status.
---

# Commerce Invoices

Create invoices, send to customers, and record payments.

## How It Works

1. Create an invoice with line items and terms.
2. Send the invoice and track status.
3. Record payments or partial payments.
4. Report overdue invoices and aging.

## Usage

- CLI: `stateset-invoices ...`
- Writes require `--apply`.
- MCP tools: `list_invoices`, `create_invoice`, `send_invoice`, `record_invoice_payment`, `get_overdue_invoices`.

## Output

```json
{"status":"sent","invoice_id":"inv_123","total":5000}
```

## Present Results to User

- Invoice status, terms, and totals.
- Payment records or overdue flags.
- Next actions (reminders, collections).

## Troubleshooting

- Invoice already paid: show payment history.
- Missing customer: create or link a customer record.

## References
- references/invoices-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/invoices.md
