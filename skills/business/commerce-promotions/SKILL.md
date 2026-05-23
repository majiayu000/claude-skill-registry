---
name: commerce-promotions
description: Manage promotions, discounts, and coupons. Use when running `stateset-promotions`, validating coupons, or applying discounts.
---

# Commerce Promotions

Manage promotions, coupons, and cart discounts.

## How It Works

1. Create or update a promotion with rules and dates.
2. Activate or deactivate campaigns.
3. Create coupon codes and validate eligibility.
4. Apply promotions to carts and report savings.

## Usage

- CLI: `stateset-promotions ...` or `stateset "apply coupon CODE to cart"`
- Writes require `--apply`.
- MCP tools: `create_promotion`, `activate_promotion`, `create_coupon`, `validate_coupon`, `apply_cart_promotions`.

## Output

```json
{"status":"active","promotion_id":"promo_123","coupon":"SAVE10"}
```

## Present Results to User

- Promotion status, dates, and trigger rules.
- Coupon validation results and discount totals.
- Any conflicts with existing promotions.

## Troubleshooting

- Coupon invalid: verify dates, usage limits, and cart eligibility.
- Overlapping promotions: clarify precedence or deactivate one.

## References
- references/promotions-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/promotions.md
