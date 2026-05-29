---
name: using-avantis-adapter
description: How to use the Avantis adapter for the avUSDC ERC-4626 vault on Base (market/manager reads, position snapshots, and deposit/redeem execution).
metadata:
  tags: wayfinder, avantis, avusdc, erc-4626, vault, base, usdc, lp
---

## When to use

Use this skill when you are:
- Reading Avantis avUSDC vault market stats (TVL, total supply, share price)
- Reading Avantis vault manager state (buffer ratio, rewards, balances)
- Reading a user’s avUSDC position (shares, assets, maxRedeem/maxWithdraw)
- Depositing USDC into the vault or redeeming avUSDC shares back to USDC

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Market, vault-manager, and position reads
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Deposit (assets) + redeem (shares) flows
- [rules/gotchas.md](rules/gotchas.md) - ERC-4626 units, Base-only scope, and unsupported borrow/repay

