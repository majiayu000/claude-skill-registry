---
name: af-pr-preparation
description: Prepare a pull request for review including required checks, documentation updates, and proper formatting. Use when ready to submit code for review, creating a PR, or checking exit criteria before merge.

# AgentFlow documentation fields
title: PR Preparation (Entry Point)
created: 2026-02-06
updated: 2026-02-06
last_checked: 2026-02-06
tags: [skill, entry-point, delivery, pull-request, review]
parent: ../README.md
related:
  - ../../docs/guides/delivery-guide.md
  - ../../docs/guides/work-management.md
  - ../af-delivery-process/SKILL.md
---

# PR Preparation

## Mandatory rules

**Read and follow the Pull Request Rules in CLAUDE-agentflow.md** — tests, lint, build must pass before PR; wait for CI and Claude Code Review after; own all failures.

## What to read

**PR rules (test, lint, build, CI, review, ownership):**
→ [CLAUDE-agentflow.md#pull-request-rules](../../CLAUDE-agentflow.md#pull-request-rules)

**PR output requirements:**
→ [delivery-guide.md#output-artifacts](../../docs/guides/delivery-guide.md#output-artifacts)

**Exit criteria (all tests pass, docs updated, coverage met):**
→ [delivery-guide.md#exit-criteria](../../docs/guides/delivery-guide.md#exit-criteria)

**Branch and merge pattern (push branch, merge via PR on GitHub):**
→ [work-management.md#branch-and-merge-pattern](../../docs/guides/work-management.md#branch-and-merge-pattern)

**Handoff to CI/CD:**
→ [delivery-guide.md#handoff-to-cicd](../../docs/guides/delivery-guide.md#handoff-to-cicd)

**For the full delivery workflow:**
→ [af-delivery-process/SKILL.md](../af-delivery-process/SKILL.md)
