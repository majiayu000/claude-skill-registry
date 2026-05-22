---
name: typescript-test
description: |
  Provides Jest-based TypeScript testing expertise and best practices. Ensures proper test structure, mocking strategies, async handling patterns, and coverage optimization. Specializes in unit testing, integration testing, test organization with describe/it blocks, jest.mock patterns, snapshot testing, and testing library integration for UI components.
  Use when: writing TypeScript test files (.spec.ts, .test.ts), structuring tests with describe/it/test blocks, implementing mocks with jest.mock/jest.spyOn, testing async code with async/await or promises, creating test fixtures and helpers, implementing snapshot tests, testing React components with Testing Library, measuring and improving code coverage, or configuring Jest for TypeScript projects.
---

# TypeScript Testing Code Guide

## Test File Structure

One-to-one matching with the file under test. Test files should be located in the same directory as the target file.

## File Naming

Format: `{target-file-name}.spec.ts`.

**Example:** `user.service.ts` → `user.service.spec.ts`

## Test Framework

Use Jest. Maintain consistency within the project.

## Test Hierarchy

Organize by method (function) unit as major sections, and by test case as minor sections. Complex methods can have intermediate sections by scenario.

## Test Coverage Selection

Omit obvious or overly simple logic (simple getters, constant returns). Prioritize testing business logic, conditional branches, and code with external dependencies.

## Test Case Composition

At least one basic success case is required. Focus primarily on failure cases, boundary values, edge cases, and exception scenarios.

## Test Independence

Each test should be executable independently. No test execution order dependencies. Initialize shared state for each test.

## Given-When-Then Pattern

Structure test code in three stages—Given (setup), When (execution), Then (assertion). Separate stages with comments or blank lines for complex tests.

## Test Data

Use hardcoded meaningful values. Avoid random data as it causes unreproducible failures. Fix seeds if necessary.

## Mocking Principles

Mock external dependencies (API, DB, file system). For modules within the same project, prefer actual usage; mock only when complexity is high.

## Test Reusability

Extract repeated mocking setups, fixtures, and helper functions into common utilities. Be careful not to harm test readability through excessive abstraction.

## Integration/E2E Testing

Unit tests are the priority. Write integration/E2E tests when complex flows or multi-module interactions are difficult to understand from code alone. Place in separate directories (`tests/integration`, `tests/e2e`).

## Test Naming

Test names should clearly express "what is being tested". Recommended format: "should do X when Y". Focus on behavior rather than implementation details.

## Assertion Count

Multiple related assertions in one test are acceptable, but separate tests when validating different concepts.

## Structure

Group methods/functionality with `describe`, write individual cases with `it`. Can classify scenarios with nested `describe`.

## Mocking

Utilize Jest's `jest.mock()`, `jest.spyOn()`. Mock external modules at the top level; change behavior per test with `mockReturnValue`, `mockImplementation`.

## Async Testing

Use `async/await`. Test Promise rejection with `await expect(fn()).rejects.toThrow()` form.

## Setup/Teardown

Use `beforeEach`, `afterEach` for common setup/cleanup. Use `beforeAll`, `afterAll` only for heavy initialization (DB connection, etc.).

## Type Safety

Type check test code too. Minimize `as any` or `@ts-ignore`. Use type guards or type assertions explicitly when needed.

## Test Utils Location

For single-file use, place at bottom of same file. For multi-file sharing, use `__tests__/utils` or `test-utils` directory.

## Coverage

Code coverage is a reference metric. Focus on meaningful test coverage rather than blindly pursuing 100%.
