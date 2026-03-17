---
name: using-polymarket-adapter
description: How to use the Polymarket adapter in Wayfinder Paths for market discovery (Gamma), orderbooks/prices/history (CLOB), user positions/activity (Data API), and execution (buy/sell + redeem) using USDC.e collateral on Polygon (incl bridge conversion).
metadata:
  tags: wayfinder, polymarket, predictions, gamma, clob, data-api, usdc.e, polygon, orderbook, timeseries, execution, redemption
---

## When to use

Use this skill when you are:
- Discovering Polymarket markets/events, or doing fuzzy search by text
- Pulling orderbooks/prices and historic time series for analysis
- Computing “movers” (dark-horse → trending) across a set of markets
- Placing predictions (buy), cashing out (sell), or redeeming resolved positions
- Converting collateral: native Polygon USDC ↔ **USDC.e** (required for trading)

## How to use

- `wayfinder_paths/adapters/polymarket_adapter/README.md` - Adapter overview + end-to-end cycle
- [rules/high-value-reads.md](rules/high-value-reads.md) - Market discovery, IDs, time series, analysis patterns
- [rules/deposits-withdrawals.md](rules/deposits-withdrawals.md) - Getting **USDC.e** and bridging back to USDC
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Approvals + trading flows (buy/sell/cancel/orders)
- [rules/gotchas.md](rules/gotchas.md) - Common pitfalls (USDC vs USDC.e, outcomes, tradability filters, rate limits)

