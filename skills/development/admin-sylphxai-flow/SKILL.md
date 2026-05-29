---
name: admin
description: Admin panel - RBAC, config, admin tools. Use when building admin UI.
---

# Admin Guideline

## Tech Stack

* **Framework**: Next.js (with Turbopack)
* **API**: tRPC
* **Database**: Neon (Postgres)
* **ORM**: Drizzle
* **Components**: Radix UI
* **Styling**: Tailwind CSS

## Non-Negotiables

* Admin bootstrap via INITIAL_SUPERADMIN_EMAIL only (one-time, non-reentrant)
* All privilege grants must be audited (who/when/why)
* Actions affecting money/access/security require step-up verification
* Secrets must never be exposed through admin UI
* Only super_admin can promote to admin or access system config

## Context

The admin platform is where operational power lives — and where operational mistakes happen. A well-designed admin reduces human error while giving operators tools to resolve issues quickly.

MFA requirements for admin roles are enforced via `account-security`.

## Driving Questions

* Is bootstrap using INITIAL_SUPERADMIN_EMAIL correctly?
* Can an admin accidentally cause serious damage?
* How would we detect admin access misuse?
* What repetitive admin tasks should be automated?
* Where is audit logging missing?
