---
name: frontend-dev
description: "Front-end development workflow and best practices. Componentization, state management, testing, and deployment. Trigger: When building, refactoring, or scaling front-end applications."
skills:
  - conventions
  - typescript
  - react
  - architecture-patterns
  - a11y
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# Frontend Development Skill

## Overview

This skill provides universal patterns for front-end development workflow, focusing on componentization, state management, testing, and deployment. It is technology-agnostic and emphasizes maintainability, scalability, and quality.

## When to Use

- Building, refactoring, or scaling front-end applications
- Managing state, side effects, or data flow
- Preparing for deployment or CI/CD
- Reviewing or improving code quality and structure

## Critical Patterns

### Componentization

- Build small, reusable components with clear responsibilities
- Use composition over inheritance
- Separate UI, logic, and data concerns

### State Management

- Use local state for isolated logic, global state for shared data
- Avoid prop drilling by using context or stores
- Keep state immutable and predictable

### Testing

- Write unit and integration tests for components and logic
- Use user-centric testing (simulate real interactions)
- Automate tests in CI pipelines

### Deployment

- Automate build, test, and deploy steps
- Use environment variables for config
- Monitor deployments for errors and rollbacks

## Decision Tree

- New feature? → Create isolated, testable component
- State needed? → Use local or global store
- Deployment? → Automate with CI/CD
- Bug found? → Add/expand test coverage

## Edge Cases

- State sync bugs (race conditions, stale data)
- Build pipeline failures (misconfig, env issues)
- Cross-browser or device-specific issues

## Practical Examples

### Before (monolithic component)

> Large component with mixed UI, logic, and data fetching.

### After (modularized)

> Split into small components: UI, logic, and data separated, easier to test and maintain.

### Before (no tests)

> Features shipped without automated tests, leading to regressions.

### After (tested)

> Each component and logic path has unit/integration tests, CI runs on every PR.

## References

- Use with conventions, architecture-patterns, and a11y for best results.
