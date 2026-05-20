---
name: using-euler-v2-adapter
description: How to use the Euler v2 (EVK / eVault) adapter for vault market discovery, APYs, positions, and EVC-batched lend/borrow flows.
metadata:
  tags: wayfinder, euler, euler-v2, evk, evault, evc, erc-4626, lending, borrowing
---

## When to use

Use this skill when you are:
- Discovering Euler v2 markets (vaults) on a given chain
- Fetching point-in-time supply/borrow APYs and vault metadata
- Reading a user’s enabled vaults / positions (assets, shares, borrowed, collateral/controller flags)
- Writing scripts that deposit/withdraw/borrow/repay using EVC batching

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Verified vaults, markets, and user snapshots
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Deposit/withdraw/borrow/repay + collateral/controller flows
- [rules/gotchas.md](rules/gotchas.md) - Terminology, units, perspectives, and adapter wiring gotchas

