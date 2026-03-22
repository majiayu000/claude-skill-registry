---
name: edge
description: >
  Use when user asks about crypto tokens, trading, portfolios, or price alerts.
---

# Edge

Tools via `edge` MCP server:

- **search** — find tokens by name or address
- **inspect** — 9 views: token_overview, pair_metrics, token_holders, token_analytics,
  graduation, pair_overview, pair_candles, pair_swaps (token_holders includes sniper/insider flags)
- **screen** — filter by mcap, liquidity, sniper %, insider %, social presence
- **portfolio** — holdings, history, top traders, wallet scan, native balances
- **trade** — limit orders, entry/exit strategies, price impact
- **alerts** — subscribe/poll/unsubscribe; webhook delivery supported

## Patterns

1. **Price before order**: `inspect pair_metrics` → compute target → `trade place`
2. **Token → pair**: `inspect token_overview` returns `pairAddress`
3. **Chain IDs**: `"8453"` Base · `"1"` Ethereum · `"42161"` Arbitrum
4. **Alerts**: subscribe once, poll each turn, unsubscribe on cleanup

[Docs](https://docs.trade.edge/agents)
