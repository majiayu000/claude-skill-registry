---
name: unit-testing
description: "Unit testing patterns and best practices for frontend and backend. Test isolation, mocks, coverage, and structure. Trigger: When writing or reviewing unit tests for any layer."
skills:
  - conventions
  - jest
  - react-testing-library
  - react-native-testing-library
  - typescript
  - frontend-dev
  - backend-dev
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# Unit Testing Skill

## When to Use

- Writing unit tests for frontend or backend
- Reviewing test coverage and isolation
- Refactoring test structure

## Critical Patterns

### Frontend

- Use RTL for user-centric tests
- Mock dependencies and hooks
- Test UI logic in isolation

### Backend

- Use Jest for logic isolation
- Mock I/O and external services
- Test pure functions and modules

## Decision Tree

- UI or logic? → Use RTL or Jest
- Need mocks? → Use jest.mock or manual mocks
- Async code? → Use async/await in tests

## Edge Cases

- Flaky async tests
- Mocking native modules
- Coverage gaps
