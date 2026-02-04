---
name: react-testing-library-best-practices
description: React Testing Library best practices for writing maintainable, user-centric tests. Use when writing, reviewing, or refactoring RTL tests. Triggers on test files, testing patterns, getBy/queryBy queries, userEvent, waitFor, and component testing.
---

# React Testing Library Best Practices

Comprehensive testing guide for React components using Testing Library, designed for AI agents and LLMs. Contains 43 rules across 9 categories, prioritized by impact to guide test writing and code review.

## When to Apply

Reference these guidelines when:
- Writing new component tests with React Testing Library
- Selecting queries (getByRole, getByLabelText, etc.)
- Handling async operations in tests (findBy, waitFor)
- Simulating user interactions (userEvent)
- Reviewing tests for anti-patterns and implementation detail testing

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Selection | CRITICAL | `query-` |
| 2 | Async Handling | CRITICAL | `async-` |
| 3 | Common Anti-Patterns | CRITICAL | `anti-` |
| 4 | User Interaction | HIGH | `user-` |
| 5 | Assertions | HIGH | `assert-` |
| 6 | Component Setup | MEDIUM | `setup-` |
| 7 | Test Structure | MEDIUM | `struct-` |
| 8 | Debugging | LOW-MEDIUM | `debug-` |
| 9 | Accessibility Testing | LOW | `a11y-` |

## Quick Reference

### 1. Query Selection (CRITICAL)

- [`query-prefer-role`](references/query-prefer-role.md) - Prefer getByRole over other queries
- [`query-avoid-testid`](references/query-avoid-testid.md) - Avoid getByTestId as primary query
- [`query-use-screen`](references/query-use-screen.md) - Use screen for queries
- [`query-label-text-forms`](references/query-label-text-forms.md) - Use getByLabelText for form fields
- [`query-role-name-option`](references/query-role-name-option.md) - Use name option with getByRole
- [`query-get-vs-query`](references/query-get-vs-query.md) - Use getBy for present, queryBy for absent
- [`query-within-scope`](references/query-within-scope.md) - Use within() to scope queries

### 2. Async Handling (CRITICAL)

- [`async-findby-over-waitfor`](references/async-findby-over-waitfor.md) - Use findBy instead of waitFor + getBy
- [`async-await-findby`](references/async-await-findby.md) - Always await findBy queries
- [`async-single-assertion-waitfor`](references/async-single-assertion-waitfor.md) - Single assertion in waitFor
- [`async-no-side-effects-waitfor`](references/async-no-side-effects-waitfor.md) - Avoid side effects in waitFor
- [`async-waitfor-disappear`](references/async-waitfor-disappear.md) - Use waitForElementToBeRemoved

### 3. Common Anti-Patterns (CRITICAL)

- [`anti-unnecessary-act`](references/anti-unnecessary-act.md) - Avoid unnecessary act() wrapping
- [`anti-manual-cleanup`](references/anti-manual-cleanup.md) - Remove manual cleanup calls
- [`anti-implementation-details`](references/anti-implementation-details.md) - Avoid testing implementation details
- [`anti-empty-waitfor`](references/anti-empty-waitfor.md) - Avoid empty waitFor callbacks
- [`anti-container-queries`](references/anti-container-queries.md) - Avoid using container for queries
- [`anti-redundant-roles`](references/anti-redundant-roles.md) - Avoid adding redundant ARIA roles

### 4. User Interaction (HIGH)

- [`user-prefer-userevent`](references/user-prefer-userevent.md) - Use userEvent over fireEvent
- [`user-setup-before-render`](references/user-setup-before-render.md) - Setup userEvent before render
- [`user-await-interactions`](references/user-await-interactions.md) - Always await userEvent interactions
- [`user-keyboard-for-special-keys`](references/user-keyboard-for-special-keys.md) - Use keyboard() for special keys
- [`user-clear-before-type`](references/user-clear-before-type.md) - Use clear() before retyping

### 5. Assertions (HIGH)

- [`assert-jest-dom-matchers`](references/assert-jest-dom-matchers.md) - Use jest-dom matchers
- [`assert-visible-over-in-document`](references/assert-visible-over-in-document.md) - Use toBeVisible() for visibility
- [`assert-text-content`](references/assert-text-content.md) - Use toHaveTextContent() for text
- [`assert-have-value`](references/assert-have-value.md) - Use toHaveValue() for inputs
- [`assert-accessible-description`](references/assert-accessible-description.md) - Use toHaveAccessibleDescription()

### 6. Component Setup (MEDIUM)

- [`setup-wrapper-providers`](references/setup-wrapper-providers.md) - Use wrapper option for providers
- [`setup-custom-render`](references/setup-custom-render.md) - Create custom render with providers
- [`setup-mock-modules`](references/setup-mock-modules.md) - Mock modules at module level
- [`setup-fake-timers`](references/setup-fake-timers.md) - Configure userEvent with fake timers
- [`setup-render-hook`](references/setup-render-hook.md) - Use renderHook for testing hooks

### 7. Test Structure (MEDIUM)

- [`struct-arrange-act-assert`](references/struct-arrange-act-assert.md) - Follow Arrange-Act-Assert pattern
- [`struct-one-behavior-per-test`](references/struct-one-behavior-per-test.md) - Test one behavior per test
- [`struct-descriptive-names`](references/struct-descriptive-names.md) - Use descriptive test names
- [`struct-avoid-beforeeach-render`](references/struct-avoid-beforeeach-render.md) - Avoid render() in beforeEach

### 8. Debugging (LOW-MEDIUM)

- [`debug-screen-debug`](references/debug-screen-debug.md) - Use screen.debug() to inspect DOM
- [`debug-logroles`](references/debug-logroles.md) - Use logRoles to find available roles
- [`debug-testing-playground`](references/debug-testing-playground.md) - Use Testing Playground for queries

### 9. Accessibility Testing (LOW)

- [`a11y-role-queries-verify`](references/a11y-role-queries-verify.md) - Role queries verify accessibility
- [`a11y-verify-focus`](references/a11y-verify-focus.md) - Test focus management
- [`a11y-test-aria-states`](references/a11y-test-aria-states.md) - Test ARIA states and properties

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
