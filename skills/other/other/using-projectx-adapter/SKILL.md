---
name: using-projectx-adapter
description: How to use the ProjectX (HyperEVM Uniswap V3 fork) adapter in Wayfinder Paths for pool reads, position management, swaps, points, and subgraph swap history (pool_address config + common gotchas).
metadata:
  tags: wayfinder, projectx, prjx, hyperevm, uniswap, v3, liquidity, lp, swaps, points, subgraph
---

## When to use

Use this skill when you are:
- Working with ProjectX concentrated liquidity on HyperEVM (chain 999)
- Reading pool state, positions, balances, fees, or swap history
- Minting/increasing/removing/burning positions via the NPM
- Swapping via the PRJX router (`swap_exact_in`)
- Fetching ProjectX points (`fetch_prjx_points`) or subgraph swap data (`fetch_swaps`)

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Pool/positions/swaps/points reads (data in/out)
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Mint/increase/remove/collect/burn/swap scripts
- [rules/gotchas.md](rules/gotchas.md) - `pool_address` requirement, tuple returns, RPC/subgraph availability, units/ticks

