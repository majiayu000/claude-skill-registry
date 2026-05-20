---
name: add-httparchive-metric-report
description: Add new metrics to HTTPArchive reports config. USE FOR adding performance metrics, adoption/percentage metrics, or custom metric analysis from crawl data. Chooses timeseries vs histogram based on data type.
---

# Adding Metrics to HTTPArchive Reports

## Documentation

**See [reports.md](../../../reports.md)** for complete guide including:

- Architecture and processing details
- Quick Decision Guide table
- Required SQL patterns checklist
- SQL pattern reference (adoption, percentiles, binning)
- Complete examples
- Troubleshooting

## Quick Start

1. Open `includes/reports.js`, find `config._metrics` (line ~42)
2. Choose type: **Timeseries** (adoption/percentiles) or **Histogram** (distributions)
3. Add metric with required patterns: `date`, `is_root_page`, `${params.lens.sql}`, `${params.devRankFilter}`, `${ctx.ref('crawl', 'pages')}`, `GROUP BY client`
4. Run `get_errors` to verify

## Key Rules

- **Boolean/adoption metrics**: Timeseries ONLY (histogram meaningless for 2 states)
- **Continuous metrics**: Both histogram + timeseries
- **Use safe functions**: `SAFE_DIVIDE()`, `SAFE.BOOL()` for custom metrics
- **Filter zeros**: Add `AND metric > 0` before percentile calculations

## Minimal Example

```javascript
metricName: {
  SQL: [
    {
      type: "timeseries", // or 'histogram'
      query: DataformTemplateBuilder.create(
        (ctx, params) => `
        SELECT client, /* your calculations */
        FROM ${ctx.ref("crawl", "pages")}
        WHERE date = '${params.date}' AND is_root_page
          ${params.lens.sql} ${params.devRankFilter}
        GROUP BY client ORDER BY client
      `,
      ),
    },
  ];
}
```

See [reports.md](../../../reports.md) for complete patterns and examples.
