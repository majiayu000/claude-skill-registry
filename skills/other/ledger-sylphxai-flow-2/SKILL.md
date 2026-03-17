---
name: ledger
description: Financial ledger - transactions, audit trails. Use when tracking money.
---

# Ledger Guideline

## Tech Stack

* **Payments**: Stripe
* **Database**: Neon (Postgres)
* **ORM**: Drizzle

## Non-Negotiables

* Balances must be immutable ledger (append-only), not mutable fields
* No floating-point for money (use deterministic precision)
* All financial mutations must be idempotent
* Monetary flows must be reconcilable with Stripe

## Context

Financial systems are unforgiving. A bug that creates or destroys money — even briefly — is a serious incident. Users trust us with their money; that trust is easily lost and hard to regain.

If balance/credits/wallet exists, it must be bulletproof. If it doesn't exist yet, consider whether the current design would support adding it correctly. Retrofitting financial integrity is painful.

## Driving Questions

* Does a balance/credits system exist, and is it implemented correctly?
* Where could money be created or destroyed by a bug?
* What happens during concurrent transactions?
* How would we detect if balances drifted from reality?
* Can we prove every balance by replaying the ledger?
* What financial edge cases (refunds, disputes, chargebacks) aren't handled?
