---
name: using-sparklend-adapter
description: How to use the SparkLend adapter for the functionality implemented in this repo (market reads, user state, supply/withdraw, borrow/repay, collateral, rewards, and native-token flows).
metadata:
  tags: wayfinder, sparklend, spark, lending, borrowing, collateral, rewards
---

## When to use

Use this skill when you are:
- Reading SparkLend markets on supported chains
- Reading a user's SparkLend reserve position or single-chain account state
- Writing scripts that supply, withdraw, borrow, repay, manage collateral, claim rewards, or handle native-token borrow/repay on SparkLend

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Markets, reserve positions, and single-chain user state
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Supply/withdraw/borrow/repay/collateral/rewards/native flows
- [rules/gotchas.md](rules/gotchas.md) - Single-chain behavior, method signatures, units, and native-token handling
