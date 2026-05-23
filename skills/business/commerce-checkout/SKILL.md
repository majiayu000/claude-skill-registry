---
name: commerce-checkout
description: Handle carts and checkout flows (rates, totals, and cart creation). Use when running `stateset-checkout` or working with cart/checkout MCP tools.
---

# Commerce Checkout

Run cart creation and checkout flows from start to finish.

## How It Works

1. Create or locate a cart for a customer.
2. Add or update cart items.
3. Set shipping address, rates, and payment details.
4. Apply discounts and complete checkout.

## Usage

- CLI: `stateset-checkout ...` or `stateset "create cart for customer@example.com"`
- Writes require `--apply`.
- MCP tools: `create_cart`, `add_cart_item`, `update_cart_item`, `set_cart_shipping_address`, `set_cart_payment`, `apply_cart_discount`, `get_shipping_rates`, `complete_checkout`.

## Output

```json
{"status":"completed","cart_id":"cart_123","order_number":"ORD-12345"}
```

## Present Results to User

- Cart and order identifiers.
- Totals (subtotal, tax, shipping, discounts).
- Any missing fields needed to finalize checkout.

## Troubleshooting

- Missing shipping/payment: collect required fields before completing.
- Coupon rejected: validate promotion rules and dates.

## References
- references/checkout-flow.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-checkout/SKILL.md
- /home/dom/stateset-icommerce/examples/workflows.md
