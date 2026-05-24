---
name: billing
description: Billing - Stripe, webhooks, subscriptions. Use when implementing payments.
---

# Billing Guideline

## Tech Stack

* **Payments**: Stripe
* **Workflows**: Upstash Workflows + QStash
* **Database**: Neon (Postgres)
* **ORM**: Drizzle

## Non-Negotiables

* Webhook signature must be verified (reject unverifiable events)
* Stripe event ID must be used for idempotency
* Webhooks must handle out-of-order delivery
* Subscription state changes must be audit-logged
* Payment failures must trigger appropriate user communication

## Context

Billing handles the payment processing mechanics — webhooks, subscription lifecycle, payment methods. It's the plumbing that moves money. Pricing strategy and entitlements live in `pricing`.

The platform owns billing logic. Stripe is a payment processor. All billing configuration must be in code, not Stripe dashboard.

## Driving Questions

* Are webhooks handling all subscription lifecycle events?
* What happens when payment fails mid-cycle?
* How are disputes and chargebacks handled end-to-end?
* Can failed webhooks be safely replayed?
* Where could revenue leak (failed renewals, unhandled states)?
