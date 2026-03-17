---
name: account-security
description: Account security - MFA, sessions, recovery. Use when protecting user accounts.
---

# Account Security Guideline

## Tech Stack

* **Auth**: better-auth
* **Framework**: Next.js

## Non-Negotiables

* Session/device visibility and revocation must exist
* All security-sensitive actions must be server-enforced and auditable
* Account recovery must require step-up verification

## Context

Account security is about giving users control over their own safety. Users should be able to see what's accessing their account, remove suspicious sessions, and understand when something unusual happens.

But it's also about protecting users from threats they don't know about. Compromised credentials, session hijacking, social engineering attacks on support — these require proactive detection, not just user vigilance.

## Driving Questions

* Can a user tell if someone else has access to their account?
* What happens when an account is compromised — how fast can we detect and respond?
* How does the recovery flow prevent social engineering attacks?
* What security events should trigger user notification?
* Where are we relying on user vigilance when we should be detecting threats?
* What would a truly paranoid user want that we don't offer?
