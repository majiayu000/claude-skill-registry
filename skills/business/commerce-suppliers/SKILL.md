---
name: commerce-suppliers
description: Manage suppliers and purchase orders. Use when running `stateset-suppliers` or handling procurement flows.
---

# Commerce Suppliers

Handle supplier records and purchase order workflows.

## How It Works

1. Create or update supplier records.
2. Create purchase orders for replenishment.
3. Approve and send POs to suppliers.
4. Track acknowledgements and receipt.

## Usage

- CLI: `stateset-suppliers ...`
- Writes require `--apply`.
- MCP tools: `list_suppliers`, `create_supplier`, `create_purchase_order`, `approve_purchase_order`, `send_purchase_order`.

## Output

```json
{"status":"approved","purchase_order_id":"po_123","supplier_id":"sup_123"}
```

## Present Results to User

- Supplier and PO identifiers.
- Approval and send status.
- Inventory impact or expected receipt date.

## Troubleshooting

- Supplier not found: create supplier first.
- PO already approved: avoid modifying line items.

## References
- references/suppliers-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/suppliers.md
