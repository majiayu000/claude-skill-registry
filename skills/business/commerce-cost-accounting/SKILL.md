---
name: commerce-cost-accounting
description: Manage item costs, cost layers, variances, and inventory valuation. Use when setting standard costs, tracking FIFO/LIFO cost layers, analyzing variances, or rolling up BOM costs.
---

# Commerce Cost Accounting

Track item costs using multiple costing methods, manage cost layers, analyze variances, and value inventory.

## How It Works

1. Set item costs with material, labor, and overhead components.
2. Choose costing method: Average, FIFO, LIFO, Standard, or Specific.
3. Create cost layers as inventory is received.
4. Issue from cost layers when inventory is consumed (FIFO/LIFO order).
5. Track cost variances (purchase, material, labor, overhead).
6. Roll up BOM costs for manufactured items.
7. Generate inventory valuation reports.

## Usage

- MCP tools: `set_item_cost`, `get_item_cost`, `list_item_costs`, `create_cost_layer`, `issue_from_cost_layer`, `record_cost_variance`, `create_cost_adjustment`, `approve_cost_adjustment`, `rollup_bom_cost`, `get_inventory_valuation`, `get_sku_cost_summary`.
- Writes require `--apply`.

## Costing Methods

- **Average**: Weighted average of all receipts
- **FIFO**: First In, First Out (consume oldest first)
- **LIFO**: Last In, First Out (consume newest first)
- **Standard**: Predetermined cost with variance tracking
- **Specific**: Individual unit cost identification

## Variance Types

- Purchase: actual vs standard purchase price
- Material: actual vs standard material usage
- Labor: actual vs standard labor cost
- Overhead: actual vs standard overhead
- Efficiency: actual vs standard quantity
- Volume: over/under absorption of fixed costs

## Cost Adjustment Statuses

- Pending -> Approved -> Applied (or Rejected)

## Output

```json
{"status":"cost_set","sku":"WIDGET-001","cost_method":"standard","unit_cost":12.50,"material":8.00,"labor":3.00,"overhead":1.50}
```

## Present Results to User

- SKU and current unit cost with breakdown.
- Costing method and active cost layers.
- Variance amounts and types.
- BOM rollup total with component costs.
- Inventory valuation totals.

## Troubleshooting

- Variance too high: review standard cost vs actual receipts.
- Cost adjustment rejected: provide justification and re-submit.
- BOM rollup incomplete: ensure all component costs are set.
- FIFO/LIFO mismatch: verify cost layers are properly ordered by receipt date.

## References
- references/costing-methods.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/cost_accounting.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/cost_accounting.rs
