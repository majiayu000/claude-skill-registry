---
name: commerce-receiving
description: Manage inbound goods receiving, inspection, and put-away. Use when processing purchase order arrivals, transfers, or return receipts into warehouse locations.
---

# Commerce Receiving

Process inbound goods from purchase orders, transfers, and returns through receiving, inspection, and put-away.

## How It Works

1. Create a receipt linked to a purchase order, transfer, or return.
2. Record received quantities against expected line items.
3. Route items for quality inspection if required.
4. Create put-away tasks to move received goods into warehouse locations.
5. Complete put-away to finalize inventory placement.

## Usage

- MCP tools: `create_receipt`, `list_receipts`, `get_receipt`, `receive_items`, `create_put_away`, `complete_put_away`.
- Writes require `--apply`.

## Receipt Types

- PurchaseOrder (default): goods from supplier PO
- Transfer: inter-warehouse transfer
- Return: customer return receiving
- Adjustment: inventory adjustment receipt
- Production: finished goods from manufacturing
- Other: miscellaneous receipts

## Status Flows

**Receipt:** Expected -> InProgress -> Received -> Inspecting -> PuttingAway -> Completed (or Cancelled)

**Receipt Item:** Pending -> PartiallyReceived -> Received -> Inspecting -> Rejected -> PutAway

**Put-Away:** Pending -> Assigned -> InProgress -> Completed (or Cancelled)

## Output

```json
{"status":"completed","receipt_number":"RCV-2025-0042","items_received":3,"total_quantity":150,"put_away_location":"LOC-A1-05"}
```

## Present Results to User

- Receipt number and linked PO or reference.
- Quantities expected vs received vs rejected.
- Items pending inspection.
- Put-away locations and completion status.

## Troubleshooting

- Quantity mismatch: record actual received; flag discrepancy for supplier follow-up.
- Items pending inspection: quality hold blocks put-away until inspection passes.
- Unknown SKU on receipt: verify PO line items match product catalog.

## References
- references/receiving-flow.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/receiving.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/receiving.rs
