---
name: billing
description: Billing - Stripe, webhooks, subscriptions. Use when implementing payments.
---

# Billing Guideline

## Tech Stack

* **Payments**: Stripe
* **Workflows**: Upstash Workflows + QStash

## Non-Negotiables

* Webhook signature must be verified (reject unverifiable events)
* Stripe event ID must be used for idempotency
* Webhooks must handle out-of-order delivery
* No dual-write: billing truth comes from Stripe events only
* UI must only display states derivable from server-truth

## Context

Billing is where trust meets money. A bug here isn't just annoying — it's a financial and legal issue. Users must always see accurate state, and the system must never lose or duplicate charges.

Beyond correctness, consider the user experience of billing. Is the upgrade path frictionless? Are failed payments handled gracefully? Does the dunning process recover revenue or just annoy users?

## Driving Questions

* What happens when webhooks arrive out of order?
* Where could revenue leak (failed renewals, unhandled states)?
* What billing states are confusing to users?
* How are disputes and chargebacks handled end-to-end?
* If Stripe is temporarily unavailable, what breaks?
* What would make the billing experience genuinely excellent?
