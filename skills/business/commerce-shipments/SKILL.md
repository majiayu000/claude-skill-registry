---
name: commerce-shipments
description: Manage shipments, tracking, and delivery updates. Use when running `stateset-shipments` or updating shipment status.
---

# Commerce Shipments

Track shipment creation and delivery events.

## How It Works

1. Validate the order is ready to ship.
2. Create a shipment with carrier and tracking details.
3. Update order status to shipped and track delivery.
4. Mark delivery or exceptions as they occur.

## Usage

- CLI: `stateset-shipments ...` and `stateset-orders ...` for status updates.
- Writes require `--apply`.
- MCP tools: `list_shipments`, `create_shipment`, `deliver_shipment`, `ship_order`.

## Output

```json
{"status":"shipped","shipment_id":"ship_123","tracking":"TRACK123"}
```

## Present Results to User

- Shipment IDs, carrier, and tracking numbers.
- Order status and delivery timestamps.
- Any delivery exceptions.

## Troubleshooting

- Invalid tracking format: verify carrier requirements.
- Order already shipped: reuse existing shipment record.

## References
- references/shipments-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/shipments.md
