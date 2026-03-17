---
name: using-uniswap-adapter
description: How to use the Uniswap V3 adapter for concentrated liquidity on Base/Arbitrum/Ethereum (LP provisioning, position management, tick math, and common gotchas).
metadata:
  tags: wayfinder, uniswap, v3, liquidity, lp, base, arbitrum, tick, nft
---

## When to use

Use this skill when you are:
- Provisioning concentrated liquidity on Uniswap V3 (or V3 forks)
- Reading LP positions, pool state, or uncollected fees
- Writing scripts that add/remove liquidity or collect fees
- Working with tick math, price ranges, or sqrtPriceX96

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Pool state, positions, fees, tick/price conversions
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Add/remove liquidity, collect fees
- [rules/gotchas.md](rules/gotchas.md) - Tick math pitfalls, slippage, token ordering, ABIs
