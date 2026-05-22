---
name: backtest-strategy
description: Guide agents through backtesting strategy ideas with automatic data fetching and performance analysis
metadata:
  tags: backtesting, strategy, performance, sharpe, drawdown, funding, simulation, yield, lending, carry, delta-neutral
---

## When to use

Use this skill when you are:
- Backtesting an existing strategy from `wayfinder_paths/strategies/`
- Validating a new trading strategy idea before production deployment
- Analyzing historical performance (Sharpe, drawdown, CAGR, funding PnL)
- Testing any strategy type: momentum, delta-neutral, yield rotation, carry trade
- Testing different leverage levels or parameter combinations

## How to use

**First, determine if you're backtesting an existing strategy or a new idea:**

### Backtesting an existing strategy (from `wayfinder_paths/strategies/`)

Load these rules:

1. **[rules/backtesting.md](rules/backtesting.md)** — **Always load first.** Config reference, stats format, gotchas.
2. **[rules/existing-strategies.md](rules/existing-strategies.md)** — **REQUIRED for existing strategies.** Workflow for reading strategy source code, extracting parameters, fetching real Delta Lab data, and faithfully reproducing signal logic. Never use generic helpers with default parameters for existing strategies.
3. Load the strategy-type-specific rule if applicable (yield-strategies.md).

### Backtesting a new strategy idea

Load these rules in order (most to least specific for your strategy type):

1. **[rules/backtesting.md](rules/backtesting.md)** — Strategy type → helper mapping, quick start examples, config reference, stats format, gotchas, production path. **Always load this first.**

2. **[rules/yield-strategies.md](rules/yield-strategies.md)** — Detailed patterns for lending/yield strategies: supply rate rotation, leveraged yield loops, carry trade, multi-venue benchmark. Load when the user's strategy involves lending protocols, supply APRs, or borrow rates.

## Examples

- [examples/basic_momentum.py](examples/basic_momentum.py) — Cross-sectional momentum using `quick_backtest`
- [examples/delta_neutral.py](examples/delta_neutral.py) — Delta-neutral basis carry using `backtest_delta_neutral`
- [examples/yield_rotation.py](examples/yield_rotation.py) — USDC rotation across lending venues using `backtest_yield_rotation`
- [examples/carry_trade.py](examples/carry_trade.py) — Borrow cheap / supply expensive using `backtest_carry_trade`

## Strategy type → helper cheat sheet

| Strategy | One-liner |
|---|---|
| Momentum/trend (perp) | `quick_backtest(strategy_fn, symbols, start, end)` |
| Delta-neutral basis carry | `backtest_delta_neutral(symbols, start, end)` |
| Yield rotation (lending) | `backtest_yield_rotation(symbol, venues, start, end)` |
| Carry trade (borrow/supply spread) | `backtest_carry_trade(symbol, start, end)` |
| Full control | `run_backtest(prices, target_positions, config)` |

All helpers are in `wayfinder_paths.core.backtesting`.
