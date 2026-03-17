---
name: operability
description: Operations - deployment, rollback, feature flags. Use for ops tooling.
---

# Operability Guideline

## Tech Stack

* **Workflows**: Upstash Workflows + QStash
* **Cache**: Upstash Redis
* **Platform**: Vercel

## Non-Negotiables

* Dead-letter handling must exist and be operable (visible, replayable)
* Side-effects (email, billing, ledger) must be idempotent or safely re-entrant
* Drift alerts must have remediation playbooks

## Context

Operability is about running the system in production — not just building it. Systems fail. Jobs get stuck. State drifts. The question is: when something goes wrong, can an operator fix it without deploying code?

Consider the operator experience during an incident. What tools do they have? What runbooks exist? Can they safely retry failed jobs? Can they detect and fix drift?

## Driving Questions

* What happens when a job fails permanently?
* How would an operator know something is stuck?
* Can failed workflows be safely replayed without duplicating side-effects?
* What drift can occur between systems, and how would we detect it?
* What's the rollback plan if a deploy breaks something critical?
* What runbooks exist, and what runbooks should exist but don't?
