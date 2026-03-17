---
name: using-ccxt-adapter
description: How to use the CCXT adapter as a multi-exchange factory for CEX trading (Binance, Hyperliquid, Aster, etc.) — setup, credentials, and common operations.
metadata:
  tags: wayfinder, ccxt, binance, hyperliquid, aster, cex, trading, exchange
---

## When to use

Use this skill when you are:
- Trading on centralized exchanges (Binance, Hyperliquid, Aster, Bybit, dYdX, etc.)
- Fetching tickers, orderbooks, or balances from CEXes
- Placing market/limit orders via CCXT
- Writing scripts that interact with multiple exchanges simultaneously

## How to use

- [rules/setup-and-config.md](rules/setup-and-config.md) - Adapter init, config format, credentials per exchange
- [rules/examples.md](rules/examples.md) - Common operations (tickers, orders, balances, multi-exchange)
- [rules/gotchas.md](rules/gotchas.md) - Async lifecycle, credential formats, rate limits
