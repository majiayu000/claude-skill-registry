---
name: release-prep
description: Use when preparing a production release or release candidate - provides a checklist-driven workflow for validation, versioning, build optimization, documentation updates, and deployment readiness.
---

# Release Prep

## Overview
Standardize release preparation with a safety-first checklist: validate quality and security, update versions and docs, build production artifacts, and prepare rollout/rollback plans.

## When to Use
- Preparing a release candidate or production deploy
- Coordinating pre-release validation and documentation
- Ensuring versioning, changelog, and build steps are consistent

Avoid when:
- You only need a quick version bump or doc update
- The release process is owned by a separate automation pipeline

## Quick Reference

| Task | Load reference |
| --- | --- |
| Release preparation | `skills/release-prep/references/prepare-release.md` |

## Workflow
1. Confirm release scope and version.
2. Load the release preparation reference.
3. Run pre-release validation (tests, security, performance).
4. Update versions, changelog, and docs.
5. Build production artifacts and validate.
6. Produce deployment checklist and rollback plan.

## Output
- Release readiness checklist
- Validation results and blockers
- Deployment plan with rollback steps

## Common Mistakes
- Skipping security or performance checks
- Shipping without updating changelog or docs
- Building artifacts without validating environment parity
