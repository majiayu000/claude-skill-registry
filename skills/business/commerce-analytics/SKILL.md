---
name: commerce-analytics
description: Run commerce analytics, metrics, and forecasts. Use when running `stateset-analytics` or requesting sales, customer, inventory, or demand insights.
---

# Commerce Analytics

Generate revenue, customer, and inventory insights.

## How It Works

1. Select a time period or segment.
2. Fetch summary metrics and top entities.
3. Generate forecasts or breakdowns.
4. Report key trends and anomalies.

## Usage

- CLI: `stateset-analytics ...` or `stateset "show sales last 30 days"`
- MCP tools: `get_sales_summary`, `get_top_products`, `get_customer_metrics`, `get_inventory_health`, `get_demand_forecast`, `get_revenue_forecast`.

## Output

```json
{"revenue":45230,"orders":156,"aov":290}
```

## Present Results to User

- Metrics requested and time range.
- Notable trends or outliers.
- Follow-up actions (reorder, promo, retention).

## Troubleshooting

- Empty data: confirm date range or seed data.
- Forecast errors: verify historical data volume.

## References
- references/analytics-queries.md
- /home/dom/stateset-icommerce/cli/.claude/skills/commerce-analytics/SKILL.md
