---
name: playwright
description: "Playwright E2E testing patterns and best practices. Cross-browser automation, selectors, fixtures, and CI integration. Trigger: When writing or running end-to-end tests with Playwright."
skills:
  - conventions
  - typescript
  - javascript
dependencies:
  playwright: ">=1.40.0 <2.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Playwright Skill

## When to Use

- End-to-end browser testing
- Cross-browser automation
- CI/CD integration

## Critical Patterns

- Use fixtures for setup
- Prefer role-based selectors
- Parallelize tests for speed

## Decision Tree

- UI or API E2E? → Use browser/page or request
- Need screenshots? → Use page.screenshot
- CI integration? → Use playwright/test

## Edge Cases

- Flaky network tests
- Browser compatibility
- Headless vs headed mode
