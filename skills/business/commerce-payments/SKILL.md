---
name: commerce-payments
description: Manage payments, captures, refunds, and payment methods. Use when running `stateset-payments`, `stateset-pay`, or handling payment intents.
---

# Commerce Payments

Create, complete, and refund payments for orders.

## How It Works

1. Create a payment record tied to an order.
2. Complete or fail the payment based on gateway results.
3. Issue refunds (full or partial) when needed.
4. Record transaction references and update order status.

## Usage

- CLI: `stateset-payments ...` and `stateset-pay ...` for stablecoin operations.
- Writes require `--apply`.
- MCP tools: `list_payments`, `get_payment`, `create_payment`, `complete_payment`, `create_refund`.

## Output

```json
{"status":"completed","payment_id":"pay_123","amount":129.99}
```

## Present Results to User

- Payment or refund IDs and amounts.
- Method used and transaction references.
- Order status updates if applicable.

## Troubleshooting

- Payment already captured: avoid duplicate completion.
- Refund exceeds paid amount: validate remaining balance.

## References
- references/payments-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/payments.md
- /home/dom/stateset-icommerce/cli/bin/stateset-pay.js
