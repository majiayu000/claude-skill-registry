---
name: stagehand
description: "Stagehand automation patterns and best practices. Scripted browser flows, data seeding, and test orchestration. Trigger: When automating browser flows or test setup with Stagehand."
skills:
  - conventions
  - typescript
  - javascript
  - playwright
dependencies:
  stagehand: ">=1.0.0 <2.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Stagehand Skill

## When to Use

- Automating browser flows
- Data seeding for tests
- Orchestrating test environments

## Critical Patterns

- Use scripts for repeatable flows
- Integrate with Playwright for E2E
- Modularize setup/teardown

## Decision Tree

- Browser or API flows? → Use Playwright or fetch
- Data setup needed? → Use scripts
- Test orchestration? → Use Stagehand CLI

## Edge Cases

- Browser version drift
- Data race conditions
- Script idempotency
