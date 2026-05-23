---
name: commerce-tax
description: Calculate taxes and manage tax rates. Use when running `stateset-tax`, calculating cart tax, or validating tax settings.
---

# Commerce Tax

Calculate taxes and manage tax jurisdiction settings.

## How It Works

1. Identify jurisdiction from shipping address.
2. Calculate tax for items or carts.
3. Apply exemptions when valid.
4. Report tax breakdown and totals.

## Usage

- CLI: `stateset-tax ...` or `stateset "calculate tax for cart ..."`
- MCP tools: `calculate_tax`, `calculate_cart_tax`, `get_tax_rate`, `list_tax_rates`, `create_tax_exemption`.

## Output

```json
{"tax_total":7.25,"jurisdiction":"US-CA"}
```

## Present Results to User

- Tax rates used and jurisdiction.
- Exemptions applied, if any.
- Final tax totals and rounding.

## Troubleshooting

- Missing address fields: collect postal code and region.
- Invalid exemption: verify certificate and expiry.

## References
- references/tax-commands.md
- /home/dom/stateset-icommerce/cli/.claude/agents/tax.md
