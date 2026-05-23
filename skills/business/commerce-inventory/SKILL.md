---
name: commerce-inventory
description: Manage inventory counts, adjustments, and stock health. Use when running `stateset-inventory`, `stateset-direct inventory`, or checking low-stock and adjustments.
---

# Commerce Inventory

Track stock levels, reservations, and adjustments across locations.

## How It Works

1. Check stock and availability for SKUs.
2. Adjust inventory with a reason code.
3. Reserve, confirm, or release stock for orders.
4. Report new availability and low-stock signals.

## Usage

- CLI: `stateset-inventory ...` or `stateset-direct inventory <action>`
- Writes require `--apply`.
- MCP tools: `get_stock`, `create_inventory_item`, `adjust_inventory`, `reserve_inventory`, `confirm_reservation`, `release_reservation`.

## Output

```json
{"status":"adjusted","sku":"WIDGET-001","available":75}
```

## Present Results to User

- Updated stock levels and reservation status.
- Any low-stock or reorder warnings.
- Reason notes used for adjustments.

## Troubleshooting

- Insufficient stock: check reservations and on-hand counts.
- Unknown SKU: ensure the product and inventory item exist.

## References
- references/inventory-commands.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-inventory/SKILL.md
- /home/dom/stateset-icommerce/examples/workflows.md
