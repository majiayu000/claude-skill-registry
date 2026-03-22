---
name: web-testing-cypress-e2e
description: Cypress E2E testing patterns - test structure, data-cy selectors, cy.intercept() mocking, custom commands, fixtures, component testing, accessibility testing with cypress-axe, and CI/CD integration
---

# Cypress E2E Testing Patterns

> **Quick Guide:** Use Cypress for end-to-end tests that verify complete user workflows. Use data-cy attributes for resilient selectors, cy.intercept() with aliases for deterministic API mocking (never arbitrary cy.wait(ms)), and cy.session() to cache authentication. Each it() block must be independent. Cypress 15 is current stable; cy.origin() is mandatory for multi-origin tests.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use data-cy attributes as your primary selector strategy - they are isolated from CSS/JS changes)**

**(You MUST use cy.intercept() with aliases and cy.wait("@alias") - NEVER use arbitrary cy.wait(ms) delays)**

**(You MUST isolate tests - each it() block runs independently without depending on other tests)**

**(You MUST use cy.origin() for any test that navigates across different origins - required since Cypress 14)**

</critical_requirements>

---

**Auto-detection:** Cypress, cy.visit, cy.get, cy.intercept, cy.origin, cy.session, data-cy, describe, it, beforeEach, cy.fixture, cy.mount, cypress-axe, cy.env

**When to use:**

- Testing critical user-facing workflows (login, checkout, form submission)
- Multi-step user journeys that span multiple pages
- Cross-browser compatibility testing
- Testing real integration with backend APIs
- Component testing in isolation with cy.mount()

**When NOT to use:**

- Testing pure utility functions (use unit tests)
- API-only testing without UI (use direct API tests)
- Testing implementation details (tests become brittle on refactoring)

**Key patterns covered:**

- Test structure and organization (describe, context, it)
- Selector strategies with data-cy attributes
- Custom commands with TypeScript support
- Network mocking with cy.intercept()
- Fixtures and test data management
- Component testing with cy.mount()
- Accessibility testing with cypress-axe
- Multi-origin testing with cy.origin()

**Detailed Resources:**

- [examples/core.md](examples/core.md) - User flows, test structure, selectors, assertions, aliases, sessions
- [examples/intercept.md](examples/intercept.md) - API mocking, error states, request verification, response modification
- [examples/custom-commands.md](examples/custom-commands.md) - Custom commands, TypeScript types, child/dual commands
- [examples/fixtures-data.md](examples/fixtures-data.md) - Fixtures, factories, test data constants
- [examples/component-testing.md](examples/component-testing.md) - Component testing with cy.mount()
- [examples/accessibility.md](examples/accessibility.md) - Accessibility testing with cypress-axe
- [examples/ci-cd.md](examples/ci-cd.md) - GitHub Actions, Docker, parallel execution
- [reference.md](reference.md) - Decision frameworks, anti-patterns, Cypress 14/15 changes

---

<philosophy>

## Philosophy

Cypress E2E tests verify that your application works correctly from the user's perspective. They run in the same run-loop as your application, providing reliable, fast feedback on user-visible behavior.

**Core Principles:**

1. **Test user-visible behavior** - Focus on what end users see and interact with, not implementation details
2. **Use resilient selectors** - data-cy attributes are isolated from CSS/JS changes and won't break on refactoring
3. **Isolate tests completely** - Each it() block must be independent; use beforeEach for common setup
4. **Trust Cypress retry-ability** - Commands automatically retry; never use arbitrary cy.wait(ms)
5. **Mock external dependencies** - Use cy.intercept() for third-party APIs to ensure reliability

**When E2E tests provide the most value:**

- Critical business workflows (authentication, payments, core features)
- User journeys spanning multiple pages or components
- Testing real backend integration with one "true" E2E test per feature
- Cross-browser compatibility verification

**When E2E tests may not be the best choice:**

- Testing pure utility functions (unit tests are faster and more precise)
- Testing every edge case (balance with unit tests; use mocks for edge cases)
- Testing implementation details (tests become brittle and break on refactoring)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Test Structure and Organization

Use `describe` to group related tests, `context` for different scenarios, and `it` for individual test cases. Named constants prevent magic strings. Each test starts fresh via `beforeEach`.

```typescript
const LOGIN_URL = "/login";
const DASHBOARD_URL = "/dashboard";
const VALID_EMAIL = "user@example.com";

describe("Login Flow", () => {
  beforeEach(() => {
    cy.visit(LOGIN_URL);
  });

  context("with valid credentials", () => {
    it("redirects to dashboard after successful login", () => {
      cy.get("[data-cy=email-input]").type(VALID_EMAIL);
      // ...
      cy.url().should("include", DASHBOARD_URL);
    });
  });
});
```

**Why good:** Logical grouping with describe/context, beforeEach ensures isolation, named constants, data-cy selectors

See [examples/core.md](examples/core.md) Pattern 1-2 for complete login flow and grouped test examples.

---

### Pattern 2: Selector Strategies

Use data-cy attributes for reliable element selection. They survive CSS refactoring and make test intent clear.

```typescript
// BEST: data-cy attributes
cy.get("[data-cy=submit-button]").click();

// ACCEPTABLE: cy.contains() when text change should fail the test
cy.contains("button", "Submit").click();

// AVOID: CSS classes, IDs, DOM structure - all fragile
cy.get(".btn-primary").click(); // Breaks on styling changes
cy.get("div > button:nth-child(2)").click(); // Breaks on markup changes
```

Use `cy.getBySel()` custom command to reduce boilerplate. See [examples/core.md](examples/core.md) Pattern 3 and [examples/custom-commands.md](examples/custom-commands.md) Pattern 1 for implementation.

---

### Pattern 3: Network Mocking with cy.intercept()

Mock API responses for deterministic, fast tests. Always alias intercepts and wait on the alias.

```typescript
cy.intercept("GET", "/api/users", {
  statusCode: 200,
  body: MOCK_USER,
}).as("getUser");

cy.visit("/profile");
cy.wait("@getUser");
cy.getBySel("user-name").should("contain", MOCK_USER.name);
```

**Why good:** Tests are deterministic, alias + wait ensures request completed, no arbitrary delays

Test error states with status codes and `forceNetworkError: true`. See [examples/intercept.md](examples/intercept.md) for error state testing, request verification, response modification, and pagination patterns.

---

### Pattern 4: Custom Commands with TypeScript

Wrap common flows (login, selectors) in custom commands with type declarations for IDE autocomplete.

```typescript
// cypress/support/commands.ts
Cypress.Commands.add("login", (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit("/login");
    cy.getBySel("email-input").type(email);
    cy.getBySel("password-input").type(password);
    cy.getBySel("submit-button").click();
    cy.url().should("include", "/dashboard");
  });
});
```

Type declarations go in `cypress/support/index.d.ts`. See [examples/custom-commands.md](examples/custom-commands.md) for selector commands, auth commands with `cacheAcrossSpecs`, form commands, child/dual commands, database task commands, and cy.origin() commands.

---

### Pattern 5: Fixtures and Test Data

Use fixtures for reusable test data, factories for dynamic data.

```typescript
// Fixture: cy.intercept with fixture file
cy.intercept("GET", "/api/products", { fixture: "products.json" }).as(
  "getProducts",
);

// Factory: dynamic data for specific scenarios
const users = createUsers(5);
cy.intercept("GET", "/api/users", { body: users }).as("getUsers");
```

**Why good:** Separates test data from test logic, fixtures are reusable, factories generate scenario-specific data

See [examples/fixtures-data.md](examples/fixtures-data.md) for organized fixture directories, factory patterns, and centralized test constants.

---

### Pattern 6: Multi-Origin Testing with cy.origin()

Cypress 14+ requires `cy.origin()` for any test that navigates across different origins (scheme + hostname + port). This is mandatory for OAuth, SSO, and cross-domain workflows.

```typescript
cy.visit("/login");
cy.getBySel("oauth-button").click();

cy.origin(
  "https://auth.provider.com",
  { args: { email, password } },
  ({ email, password }) => {
    cy.get("#email").type(email);
    cy.get("#password").type(password);
    cy.get("#submit").click();
  },
);

cy.url().should("include", "/dashboard"); // Back on original origin
```

**Why required:** Chrome deprecated `document.domain`, which Cypress previously used for cross-origin testing.

See [examples/custom-commands.md](examples/custom-commands.md) Pattern 7 for reusable OAuth command with session caching.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `cy.wait(5000)` with arbitrary milliseconds - causes flaky or slow tests, use cy.intercept() aliases instead
- Using CSS selectors like `.btn-primary` or `#submit-btn` - fragile and break on refactoring, use data-cy
- Tests that depend on previous tests - coupled tests fail randomly, each it() must be independent
- Storing values in `const` for later use - Cypress commands are async, use aliases with `.as()` instead
- Not using `cy.origin()` for multi-origin tests - required since Cypress 14 due to Chrome's deprecation of document.domain
- Using deprecated `Cypress.env()` - use `cy.env()` for secrets, `Cypress.expose()` for public values (deprecated in v15.10.0, removed in 16)

**Medium Priority Issues:**

- Not using beforeEach for common setup - leads to duplicated code and inconsistent state
- Overusing cy.contains() for selectors - text changes may not warrant test failure, prefer data-cy
- No network mocking for external APIs - third-party flakiness affects your tests
- Running only in one browser - cross-browser issues go undetected
- Using `Cypress.Commands.overwrite()` for queries - use `Cypress.Commands.overwriteQuery()` since Cypress 14

**Common Mistakes:**

- Hardcoded test data scattered throughout files - use fixtures and named constants
- Testing implementation details instead of user behavior - tests break on refactoring
- Using `after`/`afterEach` for cleanup - no guarantee it runs, put cleanup in beforeEach
- Starting web server within tests with cy.exec() - server process never exits properly

**Gotchas & Edge Cases:**

- Cypress commands are chainable and async but don't return Promises - use `.then()` for values
- Fixture files are cached and won't reflect file changes during test - use cy.readFile() for dynamic files
- `cy.session()` caches login state but clears on spec file change - use `cacheAcrossSpecs: true` (Cypress 12.4+)
- cy.intercept() routes are global to test - reset in beforeEach to prevent pollution
- Parallel tests cannot share state - use fixtures and beforeEach for per-test setup
- Chrome 137+ no longer supports `--load-extension` in branded Chrome - use Electron, Chrome for Testing, or Chromium for extensions

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use data-cy attributes as your primary selector strategy - they are isolated from CSS/JS changes)**

**(You MUST use cy.intercept() with aliases and cy.wait("@alias") - NEVER use arbitrary cy.wait(ms) delays)**

**(You MUST isolate tests - each it() block runs independently without depending on other tests)**

**(You MUST use cy.origin() for any test that navigates across different origins - required since Cypress 14)**

**Failure to follow these rules will result in flaky tests, false positives, and maintenance nightmares.**

</critical_reminders>
