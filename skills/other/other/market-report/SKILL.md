---
name: market-report
description: Create a structured market analysis report with regime, levels, catalysts, and risks.
metadata:
  {
    "marketbot": {
      "emoji": "chart"
    }
  }
---

# Market Report

Produce a concise, structured market analysis report for a single asset.

## When to use
- User asks for market analysis, outlook, or trade plan.
- User requests regime/trend/levels/catalysts/risk summary.

## Inputs to confirm (ask if missing)
- Asset (symbol + market: crypto/stocks/futures/forex)
- Timeframe(s) (e.g., 1h/4h/1d)
- Risk tolerance (low/medium/high)
- Style (scalp/intraday/swing/position)
- Data availability (quotes, indicators, news)

## Process
1. State data sources and whether any data is missing or stale.
2. Separate facts vs assumptions.
3. Provide a structured report with clear, labeled sections.
4. Include invalidation levels and a brief disclaimer.

## Output format (markdown)
```
# Market Analysis: <ASSET>

## Summary
- Direction/Bias:
- Confidence (0-100):
- Regime:

## Trend & Structure
- Trend (1h/4h/1d):
- Structure notes:

## Key Levels
- Support:
- Resistance:
- Invalidation:

## Catalysts
- Upcoming/Recent:

## Risks
- Primary risks:
- What would change the view:

## Plan (optional)
- Entry ideas:
- Stop:
- Targets:
- Position size guidance:

> Disclaimer: MarketBot provides research/analysis only. Not financial advice.
```

## Style rules
- Keep it concise and actionable.
- Call out missing data explicitly.
- Avoid execution claims without user confirmation.
