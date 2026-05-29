---
name: using-boros-adapter
description: How to use the Boros adapter for fixed-rate market data, margin flows, and vault execution in Wayfinder Paths (market discovery, vault screening, quoting, and transaction gotchas).
metadata:
  tags: wayfinder, boros, fixed-rate, orderbook, execution, margin, vaults
---

## When to use

Use this skill when you are:
- Discovering Boros markets and quoting APRs
- Screening Boros vaults by APY, tenor, capacity, and collateral type
- Building fixed-rate strategies (tenor curves, orderbook-driven pricing)
- Executing Boros actions (deposit/withdraw, vault deposit, place/cancel, close positions)

## How to use

- [rules/what-is-boros.md](rules/what-is-boros.md) - Mental model: what Boros is, what “fixed rate” means, and how markets settle
- [rules/high-value-reads.md](rules/high-value-reads.md) - Market data, vault discovery, and account state reads
- [rules/rate-locking.md](rules/rate-locking.md) - How to lock funding for delta-neutral (and how to read “the rate now”)
- [rules/execution-opportunities.md](rules/execution-opportunities.md) - Margin funding, vault deposits, withdrawals, orders, and what can be broadcast
- [rules/gotchas.md](rules/gotchas.md) - Units, isolated vs cross, tick math, and calldata sequencing
