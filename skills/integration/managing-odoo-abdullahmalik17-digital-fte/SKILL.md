---
name: managing-odoo
description: |
  Manage business accounting via Odoo ERP using XML-RPC API.
  Use when creating invoices, recording expenses, querying financial data,
  or managing customers and products.
  NOT when using QuickBooks or Xero (different systems).
---

# Odoo Accounting MCP Skill

FastMCP server for Odoo ERP integration via XML-RPC API.

## Quick Start

```bash
# Start MCP server
python src/mcp_servers/odoo_server.py

# Check connection
python -c "from src.mcp_servers.odoo_server import check_connection; print(check_connection())"
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `create_customer_invoice` | Create customer invoice with line items |
| `record_expense` | Record vendor bill (expense) |
| `get_financial_summary` | Revenue, expenses, profit for date range |
| `list_recent_invoices` | List recent customer invoices |
| `list_recent_bills` | List recent vendor bills |
| `list_products` | Search/list products |
| `get_partner_details` | Get customer/vendor details |
| `check_connection` | Verify Odoo connectivity |

## Production Gotchas

### Invoice Line Format
Invoice lines require Odoo's special tuple format `(0, 0, {...})`:

```python
# ✓ CORRECT - Tuple format for new lines
invoice_line_values.append((0, 0, {
    'product_id': product_id,
    'name': description,
    'quantity': quantity,
    'price_unit': unit_price
}))

# ✗ WRONG - Plain dictionary
invoice_line_values.append({
    'product_id': product_id,
    ...
})
```

The `(0, 0, {...})` means: "Create new record with these values".

### Move Types
Odoo uses `move_type` to distinguish invoice types:

| Type | Move Type |
|------|-----------|
| Customer Invoice | `out_invoice` |
| Customer Refund | `out_refund` |
| Vendor Bill | `in_invoice` |
| Vendor Refund | `in_refund` |

### Partner Auto-Creation
When customer/vendor doesn't exist, system auto-creates:
- Customers: `customer_rank: 1`
- Vendors: `supplier_rank: 1`

### Product Auto-Creation
Missing products are auto-created as `type: 'service'`. For physical products, create manually in Odoo.

### Partner ID Returns Tuple
Partner fields return `[id, name]` tuple, not just ID:

```python
# partner_id = [42, "Acme Corp"]
customer_name = invoice['partner_id'][1]  # "Acme Corp"
customer_id = invoice['partner_id'][0]    # 42
```

### Financial Summary Only Counts Posted
Only invoices/bills with `state: 'posted'` are included in financial summaries. Draft invoices are excluded.

### Date Format Required
All dates must be ISO format `YYYY-MM-DD`:

```python
# ✓ CORRECT
create_customer_invoice(..., invoice_date="2026-01-30")

# ✗ WRONG
create_customer_invoice(..., invoice_date="01/30/2026")
```

### Circuit Breaker Pattern
API calls use circuit breaker for resilience. After 3 failures, circuit opens for 30 seconds.

## Configuration

Required in `.env`:

```bash
ODOO_URL=http://localhost:8069    # Odoo server URL
ODOO_DB=digital_fte               # Database name
ODOO_USERNAME=admin               # Odoo username
ODOO_PASSWORD=your_password       # Odoo password (KEEP SECRET)
```

## Setup

### 1. Odoo Installation

See `docs/setup/ODOO_SETUP.md` for full setup guide.

Quick local setup:
```bash
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:13
docker run -d -p 8069:8069 --link db:db -e HOST=db -e USER=odoo -e PASSWORD=odoo --name odoo odoo
```

### 2. Enable XML-RPC

Odoo 14+ has XML-RPC enabled by default. Verify at:
`http://localhost:8069/xmlrpc/2/common`

### 3. Create API User

For production, create a dedicated API user with appropriate permissions.

## Security Notes

- All financial operations are audit logged
- Business domain actions use `AuditDomain.BUSINESS`
- No approval workflow by default (add via orchestrator if needed)
- Keep `ODOO_PASSWORD` in `.env`, never commit

## Connection Caching

Connection is cached globally to avoid repeated authentication:

```python
_odoo_connection = None  # Module-level cache

def get_odoo() -> OdooConnection:
    global _odoo_connection
    if _odoo_connection is None:
        _odoo_connection = OdooConnection(...)
    return _odoo_connection
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `generating-ceo-briefing` - Uses financial data for reports
- `watching-gmail` - Detect invoice requests from emails
- `digital-fte-orchestrator` - Process accounting tasks
