---
name: web-testing-vitest
description: Playwright E2E, Vitest, React Testing Library - E2E for user flows, unit tests for pure functions only, network-level API mocking - inverted testing pyramid prioritizing E2E tests
---

# Testing Standards

> **Quick Guide:** E2E for user flows (Playwright). Unit for pure functions (Vitest). Integration tests okay but not primary (Vitest + RTL + network-level mocking). Current app uses integration tests with network-level API mocking.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST write E2E tests for ALL critical user workflows - NOT unit tests for React components)**

**(You MUST use Playwright for E2E tests and organize by user journey - NOT by component)**

**(You MUST only write unit tests for pure functions - NOT for components, hooks, or side effects)**

**(You MUST co-locate tests with code in feature-based structure - NOT in separate test directories)**

**(You MUST use network-level API mocking - NOT module-level mocks)**

</critical_requirements>

---

**Auto-detection:** E2E testing, Playwright, test-driven development (Tester), Vitest, React Testing Library, test organization

**When to use:**

- Writing E2E tests for user workflows (primary approach with Playwright)
- Unit testing pure utility functions with Vitest
- Setting up network-level mocking for integration tests (current codebase approach)
- Organizing tests in feature-based structure (co-located tests)

**When NOT to use:**

- Unit testing React components (use E2E tests instead)
- Unit testing hooks with side effects (use E2E tests or integration tests)
- Testing third-party library behavior (library already has tests)
- Testing TypeScript compile-time guarantees (TypeScript already enforces)

**Key patterns covered:**

- E2E tests for user workflows (primary - inverted testing pyramid)
- Unit tests for pure functions only (not components)
- Integration tests with Vitest + React Testing Library + network-level mocking (acceptable, not ideal)
- Feature-based test organization (co-located with code)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - E2E and unit test examples
- [examples/integration.md](examples/integration.md) - Integration tests with network-level mocking
- [examples/anti-patterns.md](examples/anti-patterns.md) - What NOT to test
- [reference.md](reference.md) - Vitest v3/v4 migration notes, decision frameworks

---

<philosophy>

## Testing Philosophy

**PRIMARY: E2E tests for most scenarios**

E2E tests verify actual user workflows through the entire stack. They test real user experience, catch integration issues, and provide highest confidence.

**SECONDARY: Unit tests for pure functions**

Pure utilities, business logic, algorithms, data transformations, edge cases.

**Integration tests acceptable but not primary**

React Testing Library + network-level mocking useful for component behavior when E2E too slow. Don't replace E2E for user workflows.

**Testing Pyramid Inverted:**

```
        E2E Tests (Most) - Test real user workflows
        Integration Tests (Some, acceptable) - Component behavior
        Unit Tests (Pure functions only) - Utilities, algorithms
```

**When to use E2E tests:**

- All critical user-facing workflows (login, checkout, data entry)
- Multi-step user journeys (signup -> verify email -> complete profile)
- Cross-browser compatibility needs
- Testing real integration with backend APIs

**When NOT to use E2E tests:**

- Pure utility functions (use unit tests instead)
- Individual component variants in isolation (use story files for documentation)

**When to use unit tests:**

- Pure functions with clear input -> output
- Business logic calculations (pricing, taxes, discounts)
- Data transformations and formatters
- Edge cases and boundary conditions

**When NOT to use unit tests:**

- React components (use E2E tests)
- Hooks with side effects (use E2E tests or integration tests)
- API calls or external integrations (use E2E tests)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: E2E Testing with Playwright (PRIMARY)

E2E tests verify complete user workflows through the entire application stack, providing the highest confidence that features work correctly.

**What to test end-to-end:**

- ALL critical user flows (login, checkout, data entry)
- ALL user-facing features (forms, navigation, interactions)
- Multi-step workflows (signup -> verify email -> complete profile)
- Error states users will encounter
- Happy paths AND error paths
- Cross-browser compatibility (Playwright makes this easy)

**What NOT to test end-to-end:**

- Pure utility functions (use unit tests)
- Individual component variants in isolation (use story files for visual documentation)

**Test Organization:**

- `tests/e2e/` directory at root or in each app
- Test files: `*.spec.ts` or `*.e2e.ts`
- Group by user journey, not by component

See [examples/core.md](examples/core.md) for complete E2E test examples.

---

### Pattern 2: Unit Testing Pure Functions

Only write unit tests for pure functions with no side effects. Never unit test React components - use E2E tests instead.

**What to test:**

- Pure functions with clear input -> output
- Business logic calculations (pricing, taxes, discounts)
- Data transformations and formatters
- Edge cases and boundary conditions

**What NOT to test:**

- React components (use E2E tests)
- Hooks with side effects (use E2E tests or integration tests)
- API calls or external integrations (use E2E tests)

See [examples/core.md](examples/core.md) for pure function test examples.

---

### Pattern 3: Integration Testing with Network-Level Mocking (Current Approach)

The current codebase uses Vitest + React Testing Library + network-level mocking for integration tests. This is acceptable but not ideal compared to E2E tests.

**When Integration Tests Make Sense:**

- Component behavior in isolation (form validation, UI state)
- When E2E tests are too slow for rapid feedback
- Testing edge cases that are hard to reproduce in E2E
- Development workflow (faster than spinning up full stack)

**Current Pattern:**

- Tests in `__tests__/` directories co-located with code
- Network-level API mocking (intercepts HTTP requests)
- Centralized mock data in shared package
- Test all states: loading, empty, error, success

**Benefits:**

- Tests component with API integration (via network-level mocking)
- Tests all states: loading, empty, error, success
- Centralized mock handlers in shared package
- Shared between tests and development

**Limitations:**

- Doesn't test real API (mocks can drift)
- Doesn't test full user workflow
- Requires maintaining mock parity with API

See [examples/integration.md](examples/integration.md) for integration test examples.

---

### Pattern 4: Feature-Based Test Organization

Co-locate tests with code in feature-based structure. Tests live next to what they test.

**Direct Co-location (Recommended):**

```
src/
  features/
    auth/
      components/
        login-form.tsx
        login-form.test.tsx        # Test next to component
      hooks/
        use-auth.ts
        use-auth.test.ts           # Test next to hook
```

**Alternative: `__tests__/` Subdirectories:**

```
src/features/auth/
  components/
    login-form.tsx
    __tests__/
      login-form.test.tsx
```

**E2E Test Organization:**

```
tests/
  e2e/
    auth/
      login-flow.spec.ts
      register-flow.spec.ts
    checkout/
      checkout-flow.spec.ts
```

**File Naming Convention:**

- `*.test.tsx` / `*.test.ts` for unit and integration tests (Vitest)
- `*.spec.ts` for E2E tests (Playwright)

**Choose one pattern and be consistent across the codebase.**

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- No E2E tests for critical user flows - production bugs reach users before you discover them
- Unit testing React components - wastes time testing implementation details, breaks on refactoring
- Module-level mocking (`vi.mock`) instead of network-level - breaks when import structure changes, doesn't test serialization
- Only testing happy paths - error states go untested until users report them

**Medium Priority Issues:**

- Mocks that don't match real API - tests pass but production fails because mocks drifted
- Complex mocking setup - sign you should use E2E tests instead of fighting with mocks
- Running E2E tests only in CI - need local runs too for fast feedback

**Gotchas & Edge Cases:**

- E2E tests don't show up in coverage metrics (that's okay - they provide more value than coverage numbers suggest)
- Playwright `toBeVisible()` waits for element but `toBeInTheDocument()` doesn't - use visibility checks to avoid flaky tests
- Network mock handlers are typically global - reset handlers after each test to prevent pollution
- Async React updates require `waitFor()` or `findBy*` queries - `getBy*` immediately will cause flaky failures
- Files named `*.test.ts` run with Vitest, `*.spec.ts` with Playwright - mixing causes wrong runner
- **Vitest v3+:** Test options must be second argument: `test("name", { timeout: 10_000 }, () => {})` NOT `test("name", () => {}, { timeout: 10_000 })`
- **Vitest v4:** Multiple mock behavior changes (getMockName, restoreAllMocks, automocked getters) - see [reference.md](reference.md) for full v4 migration notes

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST write E2E tests for ALL critical user workflows - NOT unit tests for React components)**

**(You MUST use Playwright for E2E tests and organize by user journey - NOT by component)**

**(You MUST only write unit tests for pure functions - NOT for components, hooks, or side effects)**

**(You MUST co-locate tests with code in feature-based structure - NOT in separate test directories)**

**(You MUST use network-level API mocking - NOT module-level mocks)**

**Failure to follow these rules will result in fragile tests that break on refactoring, untested critical user paths, and false confidence from high coverage of low-value tests.**

</critical_reminders>
