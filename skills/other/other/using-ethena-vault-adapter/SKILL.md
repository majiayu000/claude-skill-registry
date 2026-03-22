---
name: using-ethena-vault-adapter
description: How to use the Ethena sUSDe vault adapter for spot APY, cooldown/position reads, and USDe→sUSDe stake/unstake flows (Ethereum mainnet vault).
metadata:
  tags: wayfinder, ethena, usde, susde, erc-4626, vault, staking, apy, cooldown
---

## When to use

Use this skill when you are:
- Fetching Ethena sUSDe spot APY (derived from the vault’s vesting model)
- Reading a user’s USDe/sUSDe balances and cooldown state (mainnet + OFT balances on other EVM chains)
- Writing scripts to stake USDe (deposit) or withdraw via the two-step cooldown + unstake flow

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - APY, cooldown, and user state
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Deposit + request-withdraw + claim-withdraw flows
- [rules/gotchas.md](rules/gotchas.md) - Mainnet-only vault, two-step withdrawals, and return formats
