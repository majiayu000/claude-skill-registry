---
name: account-security
description: Account security - MFA, sessions, recovery. Use when protecting user accounts.
---

# Account Security Guideline

## Tech Stack

* **Auth**: Better Auth
* **Framework**: Next.js (with Turbopack)
* **Database**: Neon (Postgres)

## Non-Negotiables

* MFA required for admin/super_admin roles
* Sensitive actions require step-up re-authentication (password or email OTP)
* Verified session state must be scoped, time-bound, never implicitly reused
* Session/device visibility and revocation must exist
* All security-sensitive actions must be server-enforced and auditable
* Account recovery must require step-up verification

## Context

Account security handles how users manage sessions — visibility, revocation, step-up verification, MFA. Sign-in and SSO live in `auth`.

This is the SSOT for MFA policy. Admin and other privileged roles reference this.

## Driving Questions

* Can users see all active sessions and revoke them?
* Is re-authentication required for all sensitive actions?
* What happens when an account is compromised?
* How does the recovery flow prevent social engineering?
* What security events trigger user notification?
