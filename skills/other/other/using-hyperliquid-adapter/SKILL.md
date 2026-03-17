---
name: using-hyperliquid-adapter
description: How to use Hyperliquid adapter data (meta, funding, candles, orderbooks) and execution surfaces (orders/transfers) in Wayfinder Paths, including required executor wiring.
metadata:
  tags: wayfinder, hyperliquid, perps, spot, funding, candles, execution
---

## When to use

Use this skill when you are:
- Pulling Hyperliquid market data (perp + spot)
- Using time series (funding history, OHLCV candles)
- Planning order execution (market/limit/stop), transfers, or withdrawals

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Data sources + I/O shapes for market data and time series
- [rules/deposits-withdrawals.md](rules/deposits-withdrawals.md) - Bridge2 deposit/withdraw mechanics (chain, minimums, timing, monitoring)
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Order/transfer/withdraw flows and required executor injection
- [rules/gotchas.md](rules/gotchas.md) - Asset IDs, spot naming, and common integration pitfalls
