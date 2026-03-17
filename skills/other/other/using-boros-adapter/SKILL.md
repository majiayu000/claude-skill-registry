---
name: using-boros-adapter
description: How to use the Boros adapter for fixed-rate market data and execution in Wayfinder Paths (market discovery, quoting, tick math, and transaction gotchas).
metadata:
  tags: wayfinder, boros, fixed-rate, orderbook, execution
---

## When to use

Use this skill when you are:
- Discovering Boros markets and quoting APRs
- Building fixed-rate strategies (tenor curves, orderbook-driven pricing)
- Executing Boros actions (deposit/withdraw, place/cancel, close positions)

## How to use

- [rules/what-is-boros.md](rules/what-is-boros.md) - Mental model: what Boros is, what “fixed rate” means, and how markets settle
- [rules/high-value-reads.md](rules/high-value-reads.md) - Market data + quote outputs
- [rules/rate-locking.md](rules/rate-locking.md) - How to lock funding for delta-neutral (and how to read “the rate now”)
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Deposits, withdrawals, orders, and what can be broadcast
- [rules/gotchas.md](rules/gotchas.md) - Units, tick math, and calldata sequencing

