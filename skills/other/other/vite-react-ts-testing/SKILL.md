---
name: vite-react-ts-testing
description: Add a testing setup to a Vite React-TS project (Vitest + Testing Library) following best practices, with minimal configuration and fast feedback.
argument-hint: "[goal: unit/component] [jsdom] [coverage]"
allowed-tools: Read, Grep, Glob
---

# Vite React-TS Testing (Vitest) Skill

Add fast unit/component tests suitable for Vite + React + TS.

## Rules / best practices

1) Prefer Vitest for unit tests in Vite projects.
2) Prefer @testing-library/react for UI tests.
3) Use jsdom environment for React component tests.
4) Keep configuration minimal.

## Deliverables

- Install commands
- vitest config (inline in vite.config.ts or separate vitest config)
- setupTests file if needed
- one example test

Use template.md as the default structure.
