---
name: vitest
description: Vitest testing framework patterns for test setup, async testing, mocking with vi.*, snapshots, and test performance (formerly test-vitest). This skill should be used when writing or debugging Vitest tests. This skill does NOT cover TDD methodology (use test-tdd skill), API mocking with MSW (use test-msw skill), or Jest-specific APIs.
---

# Vitest Best Practices

Comprehensive performance optimization and best practices guide for Vitest testing framework. Contains 44 rules across 8 categories, prioritized by impact to guide test writing, refactoring, and code review.

## When to Apply

Reference these guidelines when:
- Writing new Vitest tests
- Debugging flaky or slow tests
- Setting up test configuration
- Reviewing test code in PRs
- Migrating from Jest to Vitest
- Optimizing CI/CD test performance

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Async Patterns | CRITICAL | `async-` |
| 2 | Test Setup & Isolation | CRITICAL | `setup-` |
| 3 | Mocking Patterns | HIGH | `mock-` |
| 4 | Performance | HIGH | `perf-` |
| 5 | Snapshot Testing | MEDIUM | `snap-` |
| 6 | Environment | MEDIUM | `env-` |
| 7 | Assertions | LOW-MEDIUM | `assert-` |
| 8 | Test Organization | LOW | `org-` |

## Quick Reference

### 1. Async Patterns (CRITICAL)

- `async-await-assertions` - Await async assertions to prevent false positives
- `async-return-promises` - Return promises from test functions
- `async-fake-timers` - Use fake timers for time-dependent code
- `async-waitfor-polling` - Use vi.waitFor for async conditions
- `async-concurrent-expect` - Use test context expect in concurrent tests
- `async-act-wrapper` - Await user events to avoid act warnings
- `async-error-handling` - Test async error handling properly

### 2. Test Setup & Isolation (CRITICAL)

- `setup-beforeeach-cleanup` - Clean up state in afterEach hooks
- `setup-restore-mocks` - Restore mocks after each test
- `setup-avoid-shared-state` - Avoid shared mutable state between tests
- `setup-beforeall-expensive` - Use beforeAll for expensive one-time setup
- `setup-reset-modules` - Reset modules when testing module state
- `setup-test-factories` - Use test factories for complex test data

### 3. Mocking Patterns (HIGH)

- `mock-vi-mock-hoisting` - Understand vi.mock hoisting behavior
- `mock-spyon-vs-mock` - Choose vi.spyOn vs vi.mock appropriately
- `mock-implementation-not-value` - Use mockImplementation for dynamic mocks
- `mock-msw-network` - Use MSW for network request mocking
- `mock-avoid-overmocking` - Avoid over-mocking
- `mock-type-safety` - Maintain type safety in mocks
- `mock-clear-between-tests` - Clear mock state between tests

### 4. Performance (HIGH)

- `perf-pool-selection` - Choose the right pool for performance
- `perf-disable-isolation` - Disable test isolation when safe
- `perf-happy-dom` - Use happy-dom over jsdom when possible
- `perf-sharding` - Use sharding for CI parallelization
- `perf-run-mode-ci` - Use run mode in CI environments
- `perf-bail-fast-fail` - Use bail for fast failure in CI

### 5. Snapshot Testing (MEDIUM)

- `snap-inline-over-file` - Prefer inline snapshots for small values
- `snap-avoid-large` - Avoid large snapshots
- `snap-stable-serialization` - Ensure stable snapshot serialization
- `snap-review-updates` - Review snapshot updates before committing
- `snap-describe-intent` - Name snapshot tests descriptively

### 6. Environment (MEDIUM)

- `env-per-file-override` - Override environment per file when needed
- `env-setup-files` - Use setup files for global configuration
- `env-globals-config` - Configure globals consistently
- `env-browser-api-mocking` - Mock browser APIs not available in test environment

### 7. Assertions (LOW-MEDIUM)

- `assert-specific-matchers` - Use specific matchers over generic ones
- `assert-edge-cases` - Test edge cases and boundaries
- `assert-one-assertion-concept` - Test one concept per test
- `assert-expect-assertions` - Use expect.assertions for async tests
- `assert-toequal-vs-tobe` - Choose toBe vs toEqual correctly

### 8. Test Organization (LOW)

- `org-file-colocation` - Colocate test files with source files
- `org-describe-nesting` - Use describe blocks for logical grouping
- `org-test-naming` - Write descriptive test names
- `org-test-skip-only` - Use skip and only appropriately

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- [async-await-assertions](references/async-await-assertions.md) - Example rule file
- [mock-vi-mock-hoisting](references/mock-vi-mock-hoisting.md) - Example rule file

## Related Skills

- For TDD methodology, see `test-tdd` skill
- For API mocking with MSW, see `test-msw` skill
- For TypeScript testing patterns, see `typescript` skill

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
