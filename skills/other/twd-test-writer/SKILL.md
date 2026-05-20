---
name: twd-test-writer
description: TWD test writing context — teaches AI agents how to write correct TWD (Test While Developing) in-browser tests. Use this when writing, reviewing, or modifying TWD test files (*.twd.test.ts).
---

# TWD Test Writing Guide

You are writing tests for **TWD (Test While Developing)**, an in-browser testing library. Tests run in the browser (not Node.js) with a sidebar UI for instant visual feedback. Syntax is similar to Jest/Cypress but with key differences.

**Key characteristics:**
- Designed for SPAs (React, Vue, Angular, Solid.js)
- Not suitable for SSR-first architectures (Next.js App Router)
- Uses Mock Service Worker (MSW) for API mocking
- Uses `@testing-library/dom` for element queries

## Testing Philosophy: Flow-Based Tests

TWD tests should focus on **full user flows**, not granular unit-style assertions. Each `it()` block should test a meaningful user journey through a page — load, interact, verify — rather than isolating individual elements.

**Why flow-based?**
- TWD runs in the browser with full rendering — leverage that to test real user behavior
- Flow tests catch integration issues (data loading → rendering → interaction → submission)
- Fewer, richer tests are more maintainable than dozens of shallow ones

**DO — test a full flow per `it()` block:**
```typescript
it("should allow user to search and view results", async () => {
  await twd.mockRequest("getUsers", { method: "GET", url: "/api/users", response: mockUsers, status: 200 });
  await twd.visit("/users");
  await twd.waitForRequest("getUsers");

  // Verify page loaded
  twd.should(screenDom.getByRole("heading", { name: "Users" }), "be.visible");
  expect(screenDom.getAllByRole("row")).to.have.length(mockUsers.length + 1); // +1 for header

  // Search interaction
  const user = userEvent.setup();
  await user.type(screenDom.getByLabelText("Search"), "John");
  await user.click(screenDom.getByRole("button", { name: "Search" }));
  await twd.waitForRequest("searchUsers");

  // Verify filtered results
  expect(screenDom.getAllByRole("row")).to.have.length(2);
  twd.should(screenDom.getByText("John Doe"), "be.visible");
});
```

**DON'T — write one tiny test per element:**
```typescript
// BAD: too granular, doesn't test real user behavior
it("should render heading", async () => { /* only checks heading */ });
it("should render search input", async () => { /* only checks input exists */ });
it("should render table", async () => { /* only checks table exists */ });
it("should render first row", async () => { /* only checks one row */ });
```

**Guidelines:**
- One `describe()` per page or major feature
- Each `it()` covers a complete flow: setup → navigate → interact → assert outcome
- Group related flows: happy path, error states, empty states, CRUD operations
- It's fine for an `it()` block to have multiple assertions — they should tell a story
- Avoid testing implementation details; test what the user sees and does

## Required Imports

Every TWD test file needs these exact imports:

```typescript
import { twd, userEvent, screenDom, expect } from "twd-js";
import { describe, it, beforeEach, afterEach } from "twd-js/runner";
```

**Package exports:**
- `twd-js` — Main API (`twd`, `userEvent`, `screenDom`, `screenDomGlobal`, `expect`)
- `twd-js/runner` — Test functions (`describe`, `it`, `beforeEach`, `afterEach`)
- `twd-js/ui` — UI components (`MockedComponent`)

NEVER import `describe`, `it`, `beforeEach` from Jest, Mocha, or other libraries. They MUST come from `twd-js/runner`. `expect` MUST come from `twd-js`.

## File Location and Naming

Place all test files in `src/twd-tests/`. For larger projects, organize by domain:

```
src/twd-tests/
  app.twd.test.ts
  auth/
    login.twd.test.ts
    register.twd.test.ts
  dashboard/
    overview.twd.test.ts
  mocks/
    users.ts
```

Test files must follow: `*.twd.test.ts` or `*.twd.test.tsx`.

**When to use `.tsx`:** If your test uses `twd.mockComponent()` with JSX in the mock implementation, the file **must** use the `.tsx` extension. Use `.ts` for tests that don't contain JSX. When using `.tsx` test files, ensure the entry point glob pattern includes them: `import.meta.glob("./**/*.twd.test.{ts,tsx}")`.

## Core Rules

### Async/Await is Required

```typescript
// twd.get() and twd.getAll() are async — ALWAYS await
const button = await twd.get("button");
const items = await twd.getAll(".item");

// userEvent methods are async — ALWAYS await
await userEvent.click(button.el);
await userEvent.type(input, "text");

// Test functions should be async
it("should do something", async () => { /* ... */ });
```

### Element Selection

**Preferred: Testing Library queries via `screenDom`**

```typescript
// By role (most accessible — RECOMMENDED)
const button = screenDom.getByRole("button", { name: "Submit" });
const heading = screenDom.getByRole("heading", { name: "Welcome", level: 1 });

// By label (for form inputs)
const emailInput = screenDom.getByLabelText("Email Address");

// By text content
const message = screenDom.getByText("Success!");
const partial = screenDom.getByText(/welcome/i);

// By test ID
const card = screenDom.getByTestId("user-card");

// Query variants
screenDom.getByRole("button");        // Throws if not found
screenDom.queryByRole("button");      // Returns null if not found
await screenDom.findByRole("button"); // Waits for element (async)
screenDom.getAllByRole("button");     // Returns array
```

**For modals/portals use `screenDomGlobal`:**

```typescript
import { screenDomGlobal } from "twd-js";
const modal = screenDomGlobal.getByRole("dialog");
```

**Fallback: CSS selectors via `twd.get()`**

```typescript
const button = await twd.get("button");
const byId = await twd.get("#email");
const byClass = await twd.get(".error-message");
const multiple = await twd.getAll(".item");
```

### User Interactions

```typescript
const user = userEvent.setup();

// With screenDom elements (direct)
await user.click(screenDom.getByRole("button", { name: "Save" }));
await user.type(screenDom.getByLabelText("Email"), "hello@example.com");

// With twd.get() elements (use .el for raw DOM)
const twdButton = await twd.get(".save-btn");
await user.click(twdButton.el);

// Other interactions
await user.dblClick(element);
await user.clear(input);
await user.selectOptions(select, "option-value");
await user.keyboard("{Enter}");
```

### Assertions

**Method style (on twd elements):**

```typescript
const element = await twd.get("h1");
element.should("have.text", "Welcome");
element.should("contain.text", "come");
element.should("be.visible");
element.should("not.be.visible");
element.should("have.class", "header");
element.should("have.value", "test@example.com");
element.should("have.attr", "type", "submit");
element.should("be.disabled");
element.should("be.enabled");
element.should("be.checked");
element.should("be.focused");
element.should("be.empty");
```

**Function style (any element):**

```typescript
twd.should(screenDom.getByRole("button"), "be.visible");
twd.should(screenDom.getByRole("button"), "have.text", "Submit");
```

**URL assertions:**

```typescript
await twd.url().should("eq", "http://localhost:3000/dashboard");
await twd.url().should("contain.url", "/dashboard");
```

**Chai expect (for non-element assertions):**

```typescript
expect(array).to.have.length(3);
expect(value).to.equal("expected");
expect(obj).to.deep.equal({ key: "value" });
```

### Navigation and Waiting

```typescript
await twd.visit("/");
await twd.visit("/login");
await twd.wait(1000); // Wait for time (ms)
await screenDom.findByText("Success!"); // Wait for element
await twd.notExists(".loading-spinner"); // Wait for element to NOT exist
```

## API Mocking

TWD uses Mock Service Worker. **Always mock BEFORE the request fires.**

```typescript
// Mock GET request
await twd.mockRequest("getUser", {
  method: "GET",
  url: "/api/user/123",
  response: { id: 123, name: "John Doe" },
  status: 200,
});

// Mock POST request
await twd.mockRequest("createUser", {
  method: "POST",
  url: "/api/users",
  response: { id: 456, created: true },
  status: 201,
});

// URL patterns with regex
await twd.mockRequest("getUserById", {
  method: "GET",
  url: /\/api\/users\/\d+/,
  response: { id: 999, name: "Dynamic User" },
  urlRegex: true,
});

// Error responses
await twd.mockRequest("serverError", {
  method: "GET",
  url: "/api/data",
  response: { error: "Server error" },
  status: 500,
});

// Wait for request and inspect body
const rule = await twd.waitForRequest("submitForm");
expect(rule.request).to.deep.equal({ email: "test@example.com" });

// Wait for multiple requests
await twd.waitForRequests(["getUser", "getPosts"]);
```

## Component Mocking

```tsx
// In your component — wrap with MockedComponent
import { MockedComponent } from "twd-js/ui";

function Dashboard() {
  return (
    <MockedComponent name="ExpensiveChart">
      <ExpensiveChart data={data} />
    </MockedComponent>
  );
}
```

```typescript
// In your test
twd.mockComponent("ExpensiveChart", () => (
  <div data-testid="mock-chart">Mocked Chart</div>
));
```

## Module Stubbing with Sinon

Tests run in the browser. ESM named exports are **IMMUTABLE** and **cannot be stubbed**.

**Solution:** wrap hooks/services in objects with default export.

```typescript
// hooks/useAuth.ts — CORRECT: stubbable
const useAuth = () => useAuth0();
export default { useAuth };

// hooks/useAuth.ts — WRONG: cannot be stubbed
export const useAuth = () => useAuth0();
```

```typescript
// In test:
import Sinon from "sinon";
import authModule from "../hooks/useAuth";

Sinon.stub(authModule, "useAuth").returns({
  isAuthenticated: true,
  user: { name: "John" },
});
// Always Sinon.restore() in beforeEach
```

## Standard Test Template

```typescript
import { twd, userEvent, screenDom, expect } from "twd-js";
import { describe, it, beforeEach } from "twd-js/runner";

// Mock data — define at the top for reuse across tests
const mockItems = [
  { id: 1, name: "Item One", status: "active" },
  { id: 2, name: "Item Two", status: "draft" },
];

describe("Items Page", () => {
  beforeEach(() => {
    twd.clearRequestMockRules();
    twd.clearComponentMocks();
  });

  it("should load and display items, then filter by status", async () => {
    // 1. Setup mocks BEFORE visiting
    await twd.mockRequest("getItems", {
      method: "GET",
      url: "/api/items",
      response: mockItems,
      status: 200,
    });

    // 2. Navigate and wait for data
    await twd.visit("/items");
    await twd.waitForRequest("getItems");

    // 3. Verify page loaded correctly
    twd.should(screenDom.getByRole("heading", { name: "Items" }), "be.visible");
    expect(screenDom.getAllByRole("listitem")).to.have.length(2);

    // 4. Interact — filter by status
    const user = userEvent.setup();
    await user.selectOptions(screenDom.getByLabelText("Status"), "active");

    // 5. Assert filtered result
    expect(screenDom.getAllByRole("listitem")).to.have.length(1);
    twd.should(screenDom.getByText("Item One"), "be.visible");
  });

  it("should create a new item via the form", async () => {
    await twd.mockRequest("getItems", {
      method: "GET",
      url: "/api/items",
      response: mockItems,
      status: 200,
    });
    await twd.mockRequest("createItem", {
      method: "POST",
      url: "/api/items",
      response: { id: 3, name: "New Item", status: "draft" },
      status: 201,
    });

    await twd.visit("/items");
    await twd.waitForRequest("getItems");

    // Fill and submit the form
    const user = userEvent.setup();
    await user.type(screenDom.getByLabelText("Name"), "New Item");
    await user.selectOptions(screenDom.getByLabelText("Status"), "draft");
    await user.click(screenDom.getByRole("button", { name: "Create" }));

    // Verify the request payload and success state
    const req = await twd.waitForRequest("createItem");
    expect(req.request).to.deep.equal({ name: "New Item", status: "draft" });
    twd.should(await screenDom.findByText("Item created successfully"), "be.visible");
  });

  it("should show empty state when no items exist", async () => {
    await twd.mockRequest("getItems", {
      method: "GET",
      url: "/api/items",
      response: [],
      status: 200,
    });

    await twd.visit("/items");
    await twd.waitForRequest("getItems");

    twd.should(screenDom.getByText(/no items found/i), "be.visible");
    twd.should(screenDom.getByRole("button", { name: "Create" }), "be.visible");
  });

  it("should handle server error gracefully", async () => {
    await twd.mockRequest("getItems", {
      method: "GET",
      url: "/api/items",
      response: { error: "Internal server error" },
      status: 500,
    });

    await twd.visit("/items");
    await twd.waitForRequest("getItems");

    twd.should(await screenDom.findByText(/something went wrong/i), "be.visible");
  });

  it.only("debug this test", async () => { /* Only this test runs */ });
  it.skip("skip this test", async () => { /* This test won't run */ });
});
```

## Common Mistakes to AVOID

1. **Forgetting `await`** on `twd.get()`, `userEvent.*`, `twd.visit()`, `screenDom.findBy*`
2. **Mocking AFTER visit** — always mock before `twd.visit()` or the action triggering the request
3. **Not clearing mocks** — always `twd.clearRequestMockRules()` and `twd.clearComponentMocks()` in `beforeEach`
4. **Using Node.js APIs** — tests run in the browser, no `fs`, `path`, etc.
5. **Importing from wrong package** — `describe`/`it`/`beforeEach` from `twd-js/runner`, `expect` from `twd-js`, NOT Jest/Mocha
6. **Using Cypress syntax** — no `cy.get()`, `cy.visit()`. Use `twd.get()`, `twd.visit()`
7. **Stubbing named exports** — ESM makes them immutable. Use the default-export object pattern
8. **Using global describe/it** — always import from `twd-js/runner`
