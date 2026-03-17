---
name: referral
description: Referral systems - referral programs, viral loops. Use for referrals.
---

# Referral Guideline

## Tech Stack

* **Analytics**: PostHog
* **Database**: Neon (Postgres)

## Non-Negotiables

* Referral rewards must have clawback capability for fraud
* Attribution must be auditable (who referred whom, when, reward status)
* Velocity controls must exist to prevent abuse

## Context

Referral programs can drive explosive growth — or become fraud magnets. The best referral programs make sharing natural and rewarding. The worst become liability when abusers exploit them.

Consider both sides: what makes users want to share? And what prevents bad actors from gaming the system? A referral program that's easy to abuse is worse than no referral program.

## Driving Questions

* Why would a user share this product with someone they know?
* How easy is it for a bad actor to generate fake referrals?
* What fraud patterns exist that we haven't addressed?
* What is the actual ROI of the referral program?
* Where do users drop off in the referral/share flow?
* If we redesigned referrals from scratch, what would be different?
