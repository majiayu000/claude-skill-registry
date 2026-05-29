---
name: using-brap-adapter
description: How to use the BRAP adapter/client in Wayfinder Paths for cross-chain quotes and swaps (data in/out, execution paths, approvals, and common gotchas).
metadata:
  tags: wayfinder, brap, swap, bridge, execution
---

## When to use

Use this skill when you are:
- Building strategies that need swap/bridge quotes (read-only)
- Executing swaps/bridges on EVM chains (write paths)
- Debugging approvals, calldata, slippage, and unit conversion

## How to use

- [rules/high-value-reads.md](rules/high-value-reads.md) - Quote endpoints + expected shapes
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Swap execution and what it can broadcast
- [rules/gotchas.md](rules/gotchas.md) - Units, approvals, and safety rails

