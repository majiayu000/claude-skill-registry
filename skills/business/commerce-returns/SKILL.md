---
name: commerce-returns
description: Handle returns, refunds, and exchanges. Use when running `stateset-returns`, `stateset-direct returns`, or creating return flows.
---

# Commerce Returns

Process returns from request through approval and refund.

## How It Works

1. Locate the order and create a return request.
2. Approve or reject the return based on policy.
3. Receive items and trigger refund or exchange.
4. Update inventory as needed.

## Usage

- CLI: `stateset-returns ...` or `stateset-direct returns <action>`
- Writes require `--apply`.
- MCP tools: `list_returns`, `get_return`, `create_return`, `approve_return`, `reject_return`.

## Output

```json
{"status":"approved","return_id":"rma_123","refund_amount":79.99}
```

## Present Results to User

- Return status, reasons, and refund/exchange details.
- Inventory adjustments made.
- Any customer-facing next steps.

## Troubleshooting

- Return not eligible: verify policy window and status.
- Refund mismatch: confirm totals and fees.

## References
- references/returns-flow.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-returns/SKILL.md
- /home/dom/stateset-icommerce/examples/workflows.md
