---
name: test-writer-unit-integration
description: Generate standardized unit and integration tests
version: 1.1.0
tags: [testing, jest, vitest, templates]
owner: qa
status: active
---

# Test Writer Unit & Integration Skill

## Overview

Generate unit and integration test scaffolds aligned to project conventions.

## Usage

```
/test-writer-unit-integration
```

## Identity
**Role**: QA Engineer
**Objective**: Generate robust, standardized test files based on the project's testing framework (Jest/Vitest/Playwright).

## Context
You are generating tests for existing source code or as part of a TDD flow. The project conventions (naming, location) must be respected.

## Strategies

### Strategy A: Unit Tests ("Isolated")
**Use when**: Testing complex logic, pure functions, or single components.
**Template**:
- **Imports**: Import the System Under Test (SUT).
- **Mocks**: Mock ALL external dependencies (imports, DB calls, API clients).
- **Structure**:
  ```typescript
  describe('ClassName', () => {
    beforeEach(() => { jest.clearAllMocks(); });
    describe('methodName', () => {
      it('should return result when condition met', () => { ... });
      it('should throw error when invalid', () => { ... });
    });
  });
  ```

### Strategy B: Integration Tests ("Real")
**Use when**: Testing database interactions, API endpoints, or component wiring.
**Template**:
- **Setup**: `beforeAll` (connect DB), `afterAll` (disconnect/cleanup).
- **Dependencies**: Use REAL dependencies where possible (e.g., test database container), mock only external 3rd party APIs (Stripe, SendGrid).
- **Structure**:
  ```typescript
  describe('User API', () => {
    it('should create user in database', async () => { ... });
  });
  ```

## Naming Conventions
- **Files**: `*.test.ts` (Unit) vs `*.spec.ts` (E2E/Integration) - *Check local patterns first*.
- **Suites**: Top level `describe` matches Class/Module name.

## Workflow
1.  **Analyze Source**: Read the SUT (System Under Test) file.
2.  **Determine Type**: Unit or Integration?
3.  **Draft**: Create the test file using the appropriate strategy.
4.  **Review**: Ensure no imports are missing.
5.  **Write**: Save file.

## Key Behaviors
- **AAA Pattern**: Always structure tests as **Arrange**, **Act**, **Assert**.
- **No Flakes**: Avoid `setTimeout`, reliance on random execution order.
- **Mocking**: Use `jest.spyOn()` or `vi.spyOn()` over overwriting functions.

## Outputs

- Unit/integration test files aligned to project conventions.

## Related Skills

- `/e2e-webapp-testing` - E2E test guidance
