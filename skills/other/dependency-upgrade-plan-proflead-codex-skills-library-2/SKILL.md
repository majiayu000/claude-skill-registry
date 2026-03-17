---
name: dependency-upgrade-plan
description: Plan safe dependency upgrades with risk notes. Use when a mid-level developer is tasked with upgrading libraries.
---

# Dependency Upgrade Plan

## Purpose
Plan safe dependency upgrades with risk notes.

## Inputs to request
- Current and target versions.
- Release notes and breaking changes.
- Test coverage and release cadence.

## Workflow
1. Identify version gaps and breaking change notes.
2. Propose upgrade order and testing focus.
3. List rollback steps if regressions appear.

## Output
- Upgrade plan with risks and tests.

## Quality bar
- Upgrade the smallest risky dependency first.
- Note any migration tooling available.
