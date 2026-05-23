---
name: commerce-customer-service
description: Handle customer service operations for iCommerce. Use when managing tickets, order issues, returns, refunds, or support playbooks.
---

# Commerce Customer Service

Coordinate cross-domain customer support workflows.

## How It Works

1. Identify the customer and related orders or carts.
2. Resolve the request using orders, returns, inventory, or checkout tools.
3. Confirm outcomes and provide next steps.
4. Document any exceptions or manual follow-up.

## Usage

- CLI: use `stateset` in natural language with `--apply` for writes.
- MCP tools span customers, orders, products, inventory, returns, and carts.

## Output

```json
{"status":"resolved","customer_id":"cust_123","order_id":"ord_123"}
```

## Present Results to User

- Actions taken across domains.
- Key identifiers (customer, order, return, cart).
- Any remaining follow-up required.

## Troubleshooting

- Missing identifiers: ask for email, order number, or cart ID.
- Conflicting statuses: verify latest order or return state before acting.

## References
- references/customer-service-playbooks.md
- /home/dom/stateset-icommerce/cli/.claude/agents/customer-service.md
