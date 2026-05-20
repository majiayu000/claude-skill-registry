---
name: using-etherfi-adapter
description: How to use the ether.fi adapter for ETH liquid restaking on Ethereum mainnet (stake ETH→eETH, wrap/unwrap weETH, async withdraw requests, and position reads).
metadata:
  tags: wayfinder, etherfi, eeth, weeth, liquid-restaking, withdrawals, permit, ethereum
---

## When to use

Use this skill when you are:
- Staking ETH into ether.fi (ETH -> eETH)
- Wrapping/unwrapping eETH <-> weETH
- Requesting and claiming async withdrawals via WithdrawRequest NFTs
- Reading eETH/weETH balances, weETH rate, and withdraw request status/claimable amounts

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Positions + withdrawal status reads
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Stake, wrap/unwrap, request withdraw, claim withdraw
- [rules/gotchas.md](rules/gotchas.md) - Mainnet-only scope, rounding, approvals/permits, and request-id handling
