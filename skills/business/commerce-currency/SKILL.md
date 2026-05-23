---
name: commerce-currency
description: Manage currency settings and exchange rates. Use when running `stateset-currency` or converting amounts.
---

# Commerce Currency

Handle exchange rates and currency settings for global commerce.

## How It Works

1. Fetch current exchange rates.
2. Convert amounts between currencies.
3. Update rates or base currency as needed.
4. Format and report currency values.

## Usage

- CLI: `stateset-currency ...`
- MCP tools: `get_exchange_rate`, `list_exchange_rates`, `convert_currency`, `set_exchange_rate`, `set_base_currency`, `enable_currencies`, `format_currency`.

## Output

```json
{"amount":100,"from":"USD","to":"EUR","converted":92.0}
```

## Present Results to User

- Rate used and timestamp.
- Converted totals and formatting.
- Any base currency changes.

## Troubleshooting

- Rate missing: set a rate or enable the currency.
- Precision issues: use correct decimal places per currency.

## References
- references/currency-commands.md
- /home/dom/stateset-icommerce/cli/.claude/agents/currency.md
