---
name: ledger
description: Financial ledger - transactions, audit trails. Use when tracking money.
---

# Ledger Guideline

## Tech Stack

* **Database**: Neon (Postgres)
* **ORM**: Drizzle

## Non-Negotiables

* Balances must be immutable ledger (append-only), not mutable fields
* No floating-point for money (use deterministic precision)
* All financial mutations must be idempotent
* Every balance must be provable by replaying the ledger

## Context

Ledger handles financial integrity — transaction history, balance correctness, audit trail. Payment processing lives in `billing`, pricing strategy lives in `pricing`.

A bug that creates or destroys money is a serious incident. This must be bulletproof.

## Driving Questions

* Does a balance/credits system exist, and is it implemented correctly?
* Where could money be created or destroyed by a bug?
* What happens during concurrent transactions?
* How would we detect if balances drifted from reality?
* Can we prove every balance by replaying the ledger?
