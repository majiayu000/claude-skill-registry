---
name: web-testing-cypress-e2e
description: Cypress E2E testing patterns - test structure, data-cy selectors, cy.intercept() mocking, custom commands, fixtures, component testing, accessibility testing with cypress-axe, and CI/CD integration
---

# Cypress E2E Testing Patterns

> **Quick Guide:** Use Cypress for end-to-end tests that verify complete user workflows through the real application. Focus on critical user journeys, use data-cy attributes for reliable element selection, and leverage cy.intercept() for deterministic API mocking.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use data-cy attributes as your primary selector strategy - they are isolated from CSS/JS changes)**

**(You MUST use cy.intercept() with aliases and cy.wait() - NEVER use arbitrary cy.wait(ms) delays)**

**(You MUST test complete user workflows end-to-end - login flows, checkout processes, form submissions)**

**(You MUST isolate tests - each it() block runs independently without depending on other tests)**

**(You MUST use named constants for test data - no magic strings or numbers in test files)**

</critical_requirements>

---

**Auto-detection:** Cypress, cy.visit, cy.get, cy.intercept, cy.origin, cy.session, data-cy, describe, it, beforeEach, cy.fixture, cy.mount, cypress-axe

**When to use:**

- Testing critical user-facing workflows (login, checkout, form submission)
- Multi-step user journeys that span multiple pages
- Cross-browser compatibility testing
- Testing real integration with backend APIs
- Component testing in isolation with cy.mount()

**When NOT to use:**

- Testing pure utility functions (use unit tests)
- API-only testing without UI (use direct API tests)
- Testing complex async state management logic (use integration tests)

**Key patterns covered:**

- Test structure and organization (describe, context, it)
- Selector strategies with data-cy attributes
- Custom commands with TypeScript support
- Network mocking with cy.intercept()
- Fixtures and test data management
- Component testing with cy.mount()
- Accessibility testing with cypress-axe

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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

Use `describe` to group related tests, `context` for different scenarios, and `it` for individual test cases.

#### Test File Structure

```typescript
// cypress/e2e/auth/login-flow.cy.ts
const LOGIN_URL = "/login";
const DASHBOARD_URL = "/dashboard";
const VALID_EMAIL = "user@example.com";
const VALID_PASSWORD = "securePassword123";

describe("Login Flow", () => {
  beforeEach(() => {
    cy.visit(LOGIN_URL);
  });

  context("with valid credentials", () => {
    it("redirects to dashboard after successful login", () => {
      cy.get("[data-cy=email-input]").type(VALID_EMAIL);
      cy.get("[data-cy=password-input]").type(VALID_PASSWORD);
      cy.get("[data-cy=submit-button]").click();

      cy.url().should("include", DASHBOARD_URL);
      cy.get("[data-cy=welcome-heading]").should("be.visible");
    });
  });

  context("with invalid credentials", () => {
    it("shows validation error for empty email", () => {
      cy.get("[data-cy=submit-button]").click();

      cy.get("[data-cy=error-message]").should("contain", "Email is required");
    });

    it("shows error for wrong password", () => {
      cy.get("[data-cy=email-input]").type(VALID_EMAIL);
      cy.get("[data-cy=password-input]").type("wrongpassword");
      cy.get("[data-cy=submit-button]").click();

      cy.get("[data-cy=error-message]").should(
        "contain",
        "Invalid credentials",
      );
    });
  });
});
```

**Why good:** Groups related tests logically with describe/context, beforeEach eliminates repetition while maintaining isolation, named constants prevent magic strings, data-cy selectors are resilient to styling changes

```typescript
// Bad Example - Coupled tests, magic strings, fragile selectors
let userId: string;

it("creates user", () => {
  cy.visit("/signup");
  cy.get(".email-field").type("test@example.com");
  // stores userId for next test - BAD
  userId = "123";
});

it("edits user profile", () => {
  // FAILS if run alone! Depends on previous test
  cy.visit(`/users/${userId}/edit`);
  cy.wait(3000); // Arbitrary wait - BAD
});
```

**Why bad:** Tests depend on each other causing failures in isolation, CSS selectors break on styling changes, arbitrary wait causes flaky or slow tests, no constants mean magic strings everywhere

---

### Pattern 2: Selector Strategies

Use data-cy attributes for reliable element selection that survives refactoring.

#### Selector Priority (Best to Worst)

```typescript
// BEST: data-cy attributes - isolated from CSS/JS changes
cy.get("[data-cy=submit-button]").click();
cy.get("[data-cy=email-input]").type("user@example.com");

// ACCEPTABLE: cy.contains() when text change should fail the test
cy.contains("Sign In").click();
cy.contains("button", "Submit").click();

// ACCEPTABLE: Semantic selectors for accessible elements
cy.get("input[name='email']").type("user@example.com");
cy.get("button[type='submit']").click();

// AVOID: CSS classes - coupled to styling
cy.get(".btn-primary").click(); // Breaks when styling changes

// AVOID: IDs - coupled to implementation
cy.get("#submit-btn").click(); // Breaks on refactoring

// AVOID: DOM structure - extremely fragile
cy.get("div > form > button:nth-child(2)").click();
```

**Why good:** data-cy attributes are explicitly for testing, survive CSS refactoring, and make test intent clear

#### Custom Selector Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add("getBySel", (selector: string, ...args) => {
  return cy.get(`[data-cy=${selector}]`, ...args);
});

Cypress.Commands.add("getBySelLike", (selector: string, ...args) => {
  return cy.get(`[data-cy*=${selector}]`, ...args);
});

// Usage in tests
cy.getBySel("submit-button").click();
cy.getBySelLike("error").should("be.visible"); // Matches data-cy="error-message"
```

**Why good:** Reduces boilerplate, enforces consistent selector strategy, makes tests more readable

---

### Pattern 3: Network Mocking with cy.intercept()

Mock API responses for deterministic, fast tests.

#### Basic API Mocking

```typescript
const API_USERS_ENDPOINT = "/api/users";
const MOCK_USER = {
  id: "user-123",
  name: "John Doe",
  email: "john@example.com",
};

describe("User Profile", () => {
  beforeEach(() => {
    // Setup default mock
    cy.intercept("GET", API_USERS_ENDPOINT, {
      statusCode: 200,
      body: MOCK_USER,
    }).as("getUser");

    cy.visit("/profile");
  });

  it("displays user information", () => {
    cy.wait("@getUser"); // Wait for intercepted request
    cy.getBySel("user-name").should("contain", MOCK_USER.name);
    cy.getBySel("user-email").should("contain", MOCK_USER.email);
  });
});
```

**Why good:** Tests are deterministic and fast, mock data is clearly defined, alias + wait ensures request completed

#### Error State Testing

```typescript
const HTTP_SERVER_ERROR = 500;
const HTTP_NOT_FOUND = 404;

it("shows error message on server error", () => {
  cy.intercept("GET", "/api/users", {
    statusCode: HTTP_SERVER_ERROR,
    body: { error: "Internal server error" },
  }).as("getUser");

  cy.visit("/profile");
  cy.wait("@getUser");

  cy.getBySel("error-message").should("contain", "Something went wrong");
  cy.getBySel("retry-button").should("be.visible");
});

it("handles network failure gracefully", () => {
  cy.intercept("GET", "/api/users", { forceNetworkError: true }).as("getUser");

  cy.visit("/profile");

  cy.getBySel("error-message").should("contain", "Network error");
});
```

**Why good:** Tests error handling without breaking external services, simulates conditions hard to reproduce otherwise

---

### Pattern 4: Fixtures and Test Data

Use fixtures for reusable test data and factories for dynamic data.

#### Using Fixtures

```typescript
// cypress/fixtures/users.json
{
  "validUser": {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  },
  "adminUser": {
    "email": "admin@example.com",
    "password": "AdminPassword123!",
    "role": "admin"
  }
}

// In test file
describe("Login", () => {
  beforeEach(function () {
    cy.fixture("users").as("users");
  });

  it("logs in valid user", function () {
    cy.visit("/login");
    cy.getBySel("email-input").type(this.users.validUser.email);
    cy.getBySel("password-input").type(this.users.validUser.password);
    cy.getBySel("submit-button").click();

    cy.url().should("include", "/dashboard");
  });
});
```

#### cy.intercept() with Fixtures

```typescript
it("displays products from fixture", () => {
  cy.intercept("GET", "/api/products", { fixture: "products.json" }).as(
    "getProducts",
  );

  cy.visit("/products");
  cy.wait("@getProducts");

  cy.getBySel("product-card").should("have.length.at.least", 1);
});
```

**Why good:** Separates test data from test logic, fixtures are reusable across tests, easy to maintain and update

---

### Pattern 5: Custom Commands with TypeScript

Create reusable commands with proper type definitions.

#### Command Definition

```typescript
// cypress/support/commands.ts
export function registerCommands() {
  Cypress.Commands.add("login", (email: string, password: string) => {
    cy.session([email, password], () => {
      cy.visit("/login");
      cy.getBySel("email-input").type(email);
      cy.getBySel("password-input").type(password);
      cy.getBySel("submit-button").click();
      cy.url().should("include", "/dashboard");
    });
  });

  Cypress.Commands.add("getBySel", (selector: string, ...args) => {
    return cy.get(`[data-cy=${selector}]`, ...args);
  });

  Cypress.Commands.add("getBySelLike", (selector: string, ...args) => {
    return cy.get(`[data-cy*=${selector}]`, ...args);
  });
}

// cypress/support/e2e.ts
import { registerCommands } from "./commands";
registerCommands();
```

#### Type Declarations

```typescript
// cypress/support/index.d.ts
declare namespace Cypress {
  interface Chainable {
    /**
     * Custom command to log in a user
     * @param email - User email address
     * @param password - User password
     */
    login(email: string, password: string): Chainable<void>;

    /**
     * Get element by data-cy attribute
     * @param selector - The data-cy value
     */
    getBySel(
      selector: string,
      options?: Partial<Loggable & Timeoutable & Withinable & Shadow>,
    ): Chainable<JQuery<HTMLElement>>;

    /**
     * Get element by partial data-cy attribute match
     * @param selector - Partial data-cy value
     */
    getBySelLike(
      selector: string,
      options?: Partial<Loggable & Timeoutable & Withinable & Shadow>,
    ): Chainable<JQuery<HTMLElement>>;
  }
}
```

**Why good:** registerCommands() pattern supports tree-shaking, type declarations enable IDE autocomplete, JSDoc comments document usage

---

### Pattern 6: Test Configuration

Configure Cypress for different environments and requirements.

#### Basic Configuration

```typescript
// cypress.config.ts
import { defineConfig } from "cypress";

const BASE_URL = "http://localhost:3000";
const DEFAULT_TIMEOUT_MS = 10000;
const COMMAND_TIMEOUT_MS = 4000;

export default defineConfig({
  e2e: {
    baseUrl: BASE_URL,
    defaultCommandTimeout: COMMAND_TIMEOUT_MS,
    pageLoadTimeout: DEFAULT_TIMEOUT_MS,
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    retries: {
      runMode: 2,
      openMode: 0,
    },
    setupNodeEvents(on, config) {
      // Register plugins here
    },
  },
});
```

**Why good:** baseUrl avoids hardcoded URLs, retries handle CI flakiness, video disabled for speed, named constants for timeouts

</patterns>

---

<integration>

## Integration Guide

**Works with your test organization:**

- Place E2E tests in `cypress/e2e/` directory organized by feature
- Organize by user journey, not by component (e.g., `auth/`, `checkout/`, `search/`)
- Use `.cy.ts` extension for TypeScript test files
- Store fixtures in `cypress/fixtures/`
- Define custom commands in `cypress/support/commands.ts`

**CI/CD Integration:**

Cypress integrates with CI pipelines through the official GitHub Action:

```bash
# Run tests headlessly
npx cypress run

# Run specific spec file
npx cypress run --spec "cypress/e2e/auth/**/*.cy.ts"

# Run in specific browser
npx cypress run --browser chrome
```

**Debugging Tools:**

- Interactive Mode: `npx cypress open`
- Debug breakpoints: `cy.debug()` pauses test execution
- Screenshots on failure: Automatic in headless mode

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `cy.wait(5000)` with arbitrary milliseconds - causes flaky or slow tests, use cy.intercept() aliases instead
- Using CSS selectors like `.btn-primary` or `#submit-btn` - fragile and break on refactoring, use data-cy
- Tests that depend on previous tests - coupled tests fail randomly, each it() must be independent
- Storing values in `const` for later use - Cypress commands are async, use aliases with `.as()` instead
- **Cypress 14+:** Not using `cy.origin()` for multi-origin tests - required due to Chrome's deprecation of document.domain
- Using deprecated `resourceType` option on `cy.intercept()` - deprecated in Cypress 14.0.0, may be removed in future versions

**Medium Priority Issues:**

- Not using beforeEach for common setup - leads to duplicated code and inconsistent state
- Overusing cy.contains() for selectors - text changes may not warrant test failure, prefer data-cy
- No network mocking for external APIs - third-party flakiness affects your tests
- Running only in one browser - cross-browser issues go undetected

**Common Mistakes:**

- Hardcoded test data scattered throughout files - use fixtures and named constants
- Testing implementation details instead of user behavior - tests break on refactoring
- Using `after`/`afterEach` for cleanup - no guarantee it runs, put cleanup in beforeEach
- Starting web server within tests with cy.exec() - server process never exits properly

**Gotchas and Edge Cases:**

- Cypress commands are chainable and async but don't return Promises - use `.then()` for values
- Fixture files are cached and won't reflect file changes during test - use cy.readFile() for dynamic files
- `cy.session()` caches login state but clears on spec file change - one session per spec file
- cy.intercept() routes are global to test - reset in beforeEach to prevent pollution
- Parallel tests cannot share state - use fixtures and beforeEach for per-test setup

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use data-cy attributes as your primary selector strategy - they are isolated from CSS/JS changes)**

**(You MUST use cy.intercept() with aliases and cy.wait() - NEVER use arbitrary cy.wait(ms) delays)**

**(You MUST test complete user workflows end-to-end - login flows, checkout processes, form submissions)**

**(You MUST isolate tests - each it() block runs independently without depending on other tests)**

**(You MUST use named constants for test data - no magic strings or numbers in test files)**

**Failure to follow these rules will result in flaky tests, false positives, and maintenance nightmares.**

</critical_reminders>
