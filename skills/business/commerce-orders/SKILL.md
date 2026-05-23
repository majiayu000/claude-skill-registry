---
name: commerce-orders
description: Manage order lifecycles, fulfillment, shipping, and cancellations. Use when running `stateset-orders`, `stateset-direct orders`, or updating order status.
---

# Commerce Orders

Handle order creation, status transitions, and fulfillment updates.

## How It Works

1. Fetch the order and validate current status.
2. Apply allowed status transitions.
3. Ship, cancel, or update fulfillment details.
4. Report final status and tracking info.

## Usage

- CLI: `stateset-orders ...` or `stateset-direct orders <action>`
- Writes require `--apply`.
- MCP tools: `list_orders`, `get_order`, `create_order`, `update_order_status`, `ship_order`, `cancel_order`.

## Output

```json
{"status":"updated","order_id":"ord_123","order_status":"shipped"}
```

## Present Results to User

- Status transition applied and any tracking numbers.
- Items or totals affected.
- Follow-up actions required (refunds, returns).

## Troubleshooting

- Invalid transition: confirm the current status before updating.
- Already shipped: create a return flow instead of cancelling.

## References
- references/order-status.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-orders/SKILL.md
- /home/dom/stateset-icommerce/examples/workflows.md
