---
name: vitest-best-practices
description: Comprehensive vitest testing patterns covering test structure, AAA pattern, parameterized tests, assertions, mocking, test doubles, error handling, async testing, and performance optimization. Use when writing, reviewing, or refactoring vitest tests, or when user mentions vitest, testing, TDD, test coverage, mocking, assertions, or test files (*.test.ts, *.spec.ts).
compatibility: Requires vitest testing framework
metadata:
  author: gohypergiant
  version: "1.0"
---

# Vitest Best Practices

## When to Apply This Skill

Use this skill when you encounter any of these scenarios:

### File Patterns
- Working with `*.test.ts`, `*.spec.ts`, or similar test files
- Creating new test files for TypeScript/JavaScript modules
- Reviewing existing vitest test suites

### User Intent Keywords
- User mentions: vitest, testing, TDD, BDD, unit tests, integration tests
- User asks to: write tests, add test coverage, fix failing tests, refactor tests
- User discusses: mocking, stubbing, assertions, test performance, test organization

### Code Context
- Files importing from `vitest` (`describe`, `it`, `expect`, `vi`)
- Test setup/teardown code (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`)
- Mock/spy implementations using `vi.mock()`, `vi.spyOn()`, `vi.fn()`
- Assertion chains (`expect(...).toEqual()`, `.toBe()`, `.toThrow()`, etc.)

### Common Tasks
- Writing new test cases for existing functionality
- Refactoring tests for better clarity or performance
- Debugging flaky or failing tests
- Improving test coverage or maintainability
- Reviewing test code for best practices compliance

## Do NOT Use This Skill When

- Working with Jest (not vitest) - different API and conventions
- Working with other testing frameworks (Mocha, Jasmine, etc.)
- Writing end-to-end tests with Playwright/Cypress (different scope)
- The task is purely about implementation code, not tests

## What This Skill Covers

This skill provides comprehensive guidance on:

1. **Test Organization**: File placement, naming conventions, grouping strategies
2. **AAA Pattern**: Arrange, Act, Assert structure for clarity
3. **Parameterized Tests**: Using `it.each()` for testing variations
4. **Error Handling**: Testing exceptions, edge cases, and fault injection
5. **Assertions**: Choosing strict assertions (`toEqual`, `toStrictEqual`, `toThrow`)
6. **Test Doubles**: Fakes, stubs, mocks, spies - when to use each
7. **Async Testing**: Promises, async/await, timers, and concurrent tests
8. **Performance**: Fast tests, avoiding expensive operations, cleanup patterns
9. **Vitest-Specific Features**: Coverage, watch mode, benchmarking, type testing, setup files
10. **Snapshot Testing**: When and how to use snapshots effectively

## How to Use

This skill uses a **progressive disclosure** structure to minimize context usage:

### 1. Start with the Overview (AGENTS.md)
Read [AGENTS.md](AGENTS.md) for a concise overview of all rules with one-line summaries.

### 2. Load Specific Rules as Needed
When you identify a relevant optimization, load the corresponding reference file for detailed implementation guidance:

**Core Patterns:**
- [organization.md](references/organization.md)
- [aaa-pattern.md](references/aaa-pattern.md)
- [parameterized-tests.md](references/parameterized-tests.md)
- [error-handling.md](references/error-handling.md)
- [assertions.md](references/assertions.md)
- [test-doubles.md](references/test-doubles.md)

**Advanced Topics:**
- [async-testing.md](references/async-testing.md)
- [performance.md](references/performance.md)
- [vitest-features.md](references/vitest-features.md)
- [snapshot-testing.md](references/snapshot-testing.md)

### 3. Apply the Pattern
Each reference file contains:
- ❌ Incorrect examples showing the anti-pattern
- ✅ Correct examples showing the optimal implementation
- Explanations of why the pattern matters

## Quick Example

This skill helps you transform unclear tests into clear, maintainable ones:

**Before (unclear):**
```ts
test('product test', () => {
  const p = new ProductService().add({name: 'Widget'});
  expect(p.status).toBe('pendingApproval');
});
```

**After (optimized with this skill):**
```ts
describe('ProductService', () => {
  describe('Add new product', () => {
    it('should have status "pending approval" when no price is specified', () => {
      // Arrange
      const productService = new ProductService();

      // Act
      const newProduct = productService.add({name: 'Widget'});

      // Assert
      expect(newProduct.status).toEqual('pendingApproval');
    });
  });
});
```

## Key Principles

- **Clarity over cleverness**: Tests should be instantly understandable
- **Flat structure**: Avoid deep nesting in describe blocks
- **One assertion per concept**: Focus tests on single behaviors
- **Strict assertions**: Prefer `toEqual` over `toBe`, `toStrictEqual` when needed
- **Minimal mocking**: Use real implementations when practical
- **Fast execution**: Keep tests quick through efficient setup/teardown