---
name: delivery
description: Delivery - CI/CD, testing, releases. Use when improving pipelines.
---

# Delivery Guideline

## Tech Stack

* **CI**: GitHub Actions
* **Testing**: Bun test
* **Linting**: Biome
* **Platform**: Vercel

## Non-Negotiables

* All release gates must be automated (manual verification doesn't count)
* Build must fail-fast on missing required configuration
* CI must block on: lint, typecheck, tests, build
* `/en/*` must redirect (no duplicate content)
* Security headers must be verified by tests
* Consent gating must be verified by tests

## Context

Delivery handles pre-production — CI/CD pipeline, release gates, quality checks. Post-deployment operations (rollback, feature flags, runbooks) live in `deployments`.

The question isn't "what tests do we have?" but "what could go wrong that we wouldn't catch?"

## Driving Questions

* What could ship to production that shouldn't?
* Where does manual verification substitute for automation?
* What flaky tests are training people to ignore failures?
* How fast is the feedback loop, and what slows it down?
* What's the worst thing that shipped recently that tests should have caught?
