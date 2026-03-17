---
name: using-pool-token-balance-data
description: How to fetch and interpret pool/token/balance data in Wayfinder Paths (PoolClient/TokenClient + adapters + MCP balance tools), including common query patterns and I/O shapes.
metadata:
  tags: wayfinder, defi, pools, tokens, balances, data
---

## When to use

Use this skill when you are:
- Building a strategy that screens pools/vault-like opportunities (APY/TVL)
- Resolving token identifiers/decimals/chain for correct unit handling
- Fetching wallet balances (API or on-chain) and recording results to the local ledger

## How to use

- [rules/pools.md](rules/pools.md) - Pool discovery, APY/TVL, DefiLlama merges
- [rules/tokens.md](rules/tokens.md) - Token metadata, decimals, gas token lookup
- [rules/balances-and-ledger.md](rules/balances-and-ledger.md) - Balance reads and local ledger bookkeeping

