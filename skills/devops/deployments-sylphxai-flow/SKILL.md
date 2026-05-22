---
name: deployments
description: Deployments - rollback, feature flags, ops tooling. Use when shipping to production.
---

# Deployments Guideline

## Tech Stack

* **Workflows**: Upstash Workflows + QStash
* **Cache**: Upstash Redis
* **Platform**: Vercel

## Non-Negotiables

* Rollback plan must exist and be exercisable
* Dead-letter handling must exist and be operable (visible, replayable)
* Side-effects (email, billing, ledger) must be idempotent or safely re-entrant
* Drift alerts must have remediation playbooks

## Context

Deployments handles post-deployment operations — rollback, feature flags, runbooks, incident response. Pre-production CI/CD lives in `delivery`.

When something goes wrong, can an operator fix it without deploying code?

## Driving Questions

* What happens when a job fails permanently?
* How would an operator know something is stuck?
* Can failed workflows be safely replayed without duplicating side-effects?
* What's the rollback plan if a deploy breaks something critical?
* What runbooks exist, and what runbooks should exist but don't?
