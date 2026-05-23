---
name: commerce-manufacturing
description: Manage manufacturing BOMs and work orders. Use when running `stateset-manufacturing` or tracking production.
---

# Commerce Manufacturing

Create BOMs and run work orders for production.

## How It Works

1. Create and activate a BOM for a product.
2. Add components and quantities.
3. Create and start work orders.
4. Complete work orders and update inventory.

## Usage

- CLI: `stateset-manufacturing ...`
- Writes require `--apply`.
- MCP tools: `create_bom`, `add_bom_component`, `activate_bom`, `create_work_order`, `start_work_order`, `complete_work_order`.

## Output

```json
{"status":"completed","work_order_id":"wo_123","completed_quantity":98}
```

## Present Results to User

- BOM or work order identifiers.
- Production quantities and inventory updates.
- Any shortages or scrap notes.

## Troubleshooting

- Component missing: confirm SKU and inventory levels.
- BOM inactive: activate before creating work orders.

## References
- references/manufacturing-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/manufacturing.md
