---
name: using-tests
description: Testing strategy and workflow. Tests run in parallel with isolated data per suite. Prioritize Playwright for UI, integration tests for APIs, unit tests for logic.
---

# Working with Tests

Testing strategy and workflow. Tests run in parallel with isolated data per suite. Prioritize Playwright for UI, integration tests for APIs, unit tests for logic.

## Testing Strategy

Follow this hierarchy when deciding what kind of test to write:

1. **Playwright tests** (browser) - Preferred for most features
2. **Integration tests** (API) - When Playwright is not practical
3. **Unit tests** (pure functions) - Only for complex isolated logic

---

## When to Use Each Test Type

### Playwright Tests (Default Choice)

Write Playwright tests when the feature involves:

- User interactions (clicking, typing, navigation)
- Visual feedback (toasts, loading states, error messages)
- Form submissions and validation
- Multi-step UI flows
- Protected routes and redirects
- Accessibility behavior

**Example features best tested with Playwright:**

- Sign-in flow with error handling
- Chat creation and deletion with confirmation dialogs
- Theme toggle
- Form validation messages
- Navigation between pages

### Integration Tests

Write integration tests when:

- Testing API responses directly (status codes, JSON structure)
- Verifying database state after operations
- Testing server-side logic without UI
- Playwright would be too slow or complex for the scenario

**Example features best tested with integration tests:**

- API route returns correct status codes
- User creation populates database correctly
- Session cookies are set on sign-in
- Protected API routes return 401/403

### Unit Tests

Write unit tests only when:

- Testing pure functions with complex logic
- Testing code with many edge cases
- Testing type narrowing and error messages
- The function has no external dependencies

**Example features best tested with unit tests:**

- Assertion helpers
- Config schema validation
- Data transformation functions
- Utility functions

---

## Running Tests

All tests run against an isolated Neon database branch that auto-deletes after 1 hour.

```bash
bun run test              # All tests with isolated Neon branch
bun run test:playwright   # Browser tests only
bun run test:integration  # Integration tests only
bun run test:unit         # Unit tests only
```

---

## Folder Structure

```
src/
├── lib/
│   ├── common/
│   │   ├── assert.ts
│   │   └── assert.test.ts      # Unit test (co-located)
│   └── config/
│       ├── schema.ts
│       └── schema.test.ts      # Unit test (co-located)
tests/
├── integration/
│   ├── llms.test.ts            # Integration test
│   ├── r.test.ts
│   ├── mcp/
│   │   └── route.test.ts
│   └── recipes/
│       └── [slug]/
│           └── route.test.ts
└── playwright/
    ├── auth.spec.ts            # Playwright test
    ├── chat.spec.ts
    ├── home.spec.ts
    └── lib/
        └── test-user.ts        # Playwright-specific helpers
```

---

## Writing Tests for New Features

### Step 1: Determine Test Type

Ask: "How would a user verify this feature works?"

- **If through the UI** → Playwright test
- **If through API calls** → Integration test
- **If by calling a function directly** → Unit test

### Step 2: Create Test File

**Playwright tests:** `tests/playwright/{feature}.spec.ts`

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature Name", () => {
  test("should do expected behavior", async ({ page }) => {
    await page.goto("/feature");
    // Test implementation
  });
});
```

**Integration tests:** `tests/integration/{feature}.test.ts`

For API routes, import the handler directly for faster, more reliable tests:

```typescript
import { describe, it, expect } from "bun:test";
import { GET } from "@/app/api/feature/route";

describe("GET /api/feature", () => {
  it("should return expected response", async () => {
    const response = await GET();

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.value).toBeDefined();
  });
});
```

**Unit tests:** `src/lib/{domain}/{file}.test.ts` (co-located)

```typescript
import { describe, it, expect } from "bun:test";
import { myFunction } from "./my-file";

describe("myFunction", () => {
  it("should do expected behavior", () => {
    expect(myFunction()).toBe("expected");
  });
});
```

---

## Test Data Management

### Database Isolation

Tests run against isolated Neon branches. Each test run:

1. Creates a fresh schema-only branch
2. Runs tests against the branch
3. Branch auto-deletes after 1 hour

This ensures tests don't interfere with production data.

### Parallel Test Isolation

Tests run in parallel by default. Each test suite must use its own test data to avoid conflicts:

- **Different test users** - Each spec file should create unique users with distinct emails
- **Different resources** - Tests creating chats, sessions, etc. should not depend on shared state
- **No cleanup required** - The branch TTL handles cleanup automatically

```typescript
// auth.spec.ts - uses auth-specific test user
const testUser = await createTestUser({
  email: `auth-test-${uuid}@example.com`,
});

// chat.spec.ts - uses chat-specific test user
const testUser = await createTestUser({
  email: `chat-test-${uuid}@example.com`,
});
```

Avoid patterns that rely on global state or specific database contents existing from other tests.

---

## Common Patterns

### Testing Protected Routes (Playwright)

```typescript
test("should redirect unauthenticated user", async ({ page }) => {
  await page.goto("/protected-page");
  await expect(page).toHaveURL(/sign-in/);
});
```

### Testing Error States (Playwright)

```typescript
test("should show error for invalid input", async ({ page }) => {
  await page.goto("/form");
  await page.getByRole("button", { name: /submit/i }).click();

  await expect(page.getByText(/error|required/i)).toBeVisible({
    timeout: 5000,
  });
});
```

### Testing API Responses (Integration)

Import route handlers directly for cleaner tests:

```typescript
import { GET } from "@/app/api/endpoint/route";

it("should return 200 for valid request", async () => {
  const response = await GET();
  expect(response.status).toBe(200);
});
```

---

## Debugging Failed Tests

### Playwright

```bash
bunx playwright test --headed              # Watch browser
bunx playwright test --debug               # Step through test
bunx playwright show-report                # View HTML report
```

### Integration/Unit

```bash
bun test --only "test name"                # Run single test
bun test --watch                           # Re-run on changes
```

### View test artifacts

Failed Playwright tests save screenshots and traces to `test-results/`. Check this folder when CI fails.
