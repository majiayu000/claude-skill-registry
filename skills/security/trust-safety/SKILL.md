---
name: trust-safety
description: Trust and safety - abuse prevention, rate limiting. Use when fighting bad actors.
---

# Trust Safety Guideline

## Tech Stack

* **Analytics**: PostHog
* **Database**: Neon (Postgres)
* **Workflows**: Upstash Workflows + QStash

## Non-Negotiables

* All enforcement actions must be auditable (who/when/why)
* Appeals process must exist for affected users
* Graduated response levels must be defined (warn → restrict → suspend → ban)

## Context

Trust & safety is about protecting users — from each other and from malicious actors. Every platform eventually attracts abuse. The question is whether you're prepared for it or scrambling to react.

Consider: what would a bad actor try to do? How would we detect it? How would we respond? What about the false positives — innocent users caught by automated systems? A good T&S system is effective against abuse AND fair to legitimate users.

## Driving Questions

* What would a motivated bad actor try to do on this platform?
* How would we detect coordinated abuse or bot networks?
* What happens when automated moderation gets it wrong?
* How do affected users appeal decisions, and is it fair?
* What abuse patterns exist that we haven't addressed?
* What would make users trust that we're protecting them?
