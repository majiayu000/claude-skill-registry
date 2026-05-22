---
name: create-e2e-test
description: Create end-to-end tests using Playwright with page objects and fixtures following project conventions
user-invocable: true
---

# Create E2E Test

Create end-to-end tests for the user flow described below.

## Instructions

### 1. Understand the User Flow

First, analyze the `User Flow` to identify:
- **Entry point**: Which page/route does the flow start from?
- **Steps**: What user actions are involved (clicks, form fills, navigation)?
- **Assertions**: What should be verified at each step or at the end?
- **Prerequisites**: Does the user need to be authenticated? Any setup data needed?

### 2. Explore Existing Patterns

Before writing code, explore relevant existing files:

```
apps/e2e-tests/
├── pages/                    # Page Objects - check for reusable pages
├── fixtures/                 # Base fixtures (auth.fixtures.ts)
└── tests/
    └── [feature]/            # Existing test patterns
        ├── [feature].fixtures.ts
        └── [feature].spec.ts
```

**Key files to reference**:
- `apps/e2e-tests/fixtures/auth.fixtures.ts` - Authentication fixtures
- `apps/e2e-tests/pages/SiteCreationPage.ts` - Page object pattern example
- `apps/e2e-tests/tests/site-creation/site-creation.fixtures.ts` - Fixture composition example

### 3. Create/Update Page Objects

For each page/screen in the flow, create or update a page object in `apps/e2e-tests/pages/`:

**Page Object Pattern**:
```typescript
import { expect, type Page } from "@playwright/test";

export class FeaturePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Navigation
  async goto(): Promise<void> {
    await this.page.goto("/route-path");
  }

  // Assertions (prefix with expect*)
  async expectStepVisible(): Promise<void> {
    await expect(this.page.getByRole("heading", { name: "Step Title" })).toBeVisible();
  }

  // User Actions (verb-based names)
  async clickButton(): Promise<void> {
    await this.page.getByRole("button", { name: "Button Text" }).click();
  }

  async fillInput(value: string): Promise<void> {
    await this.page.getByLabel("Input Label").fill(value);
  }

  async selectOption(value: string): Promise<void> {
    await this.page.getByRole("radio", { name: value }).check({ force: true });
    await this.submit();
  }

  // Private helpers
  private async submit(): Promise<void> {
    await this.page.getByRole("button", { name: /Valider|Suivant/ }).click();
  }
}
```

**Selector Priority** (accessibility-first):
1. `getByRole()` - buttons, links, headings, textboxes
2. `getByLabel()` - form inputs with labels
3. `getByText()` - visible text content
4. `locator()` - CSS selectors (last resort)

### 4. Create Feature Fixtures

Create `apps/e2e-tests/tests/[feature]/[feature].fixtures.ts`:

```typescript
import { test as authTest } from "../../fixtures/auth.fixtures";
import { FeaturePage } from "../../pages/FeaturePage";

type FeatureFixtures = {
  featurePage: FeaturePage;
};

export const test = authTest.extend<FeatureFixtures>({
  featurePage: async ({ authenticatedPage }, use) => {
    const featurePage = new FeaturePage(authenticatedPage);
    await use(featurePage);
  },
});

export { expect } from "@playwright/test";
```

**If authentication is NOT needed**, extend from base Playwright test instead:
```typescript
import { test as base, expect } from "@playwright/test";
```

### 5. Write Test File

Create `apps/e2e-tests/tests/[feature]/[feature].spec.ts`:

```typescript
import { test } from "./[feature].fixtures";

test.describe("Feature Name", () => {
  test("describes what the user can do", async ({ featurePage }) => {
    // Navigate to starting point
    await featurePage.goto();

    // Step 1: Action + optional assertion
    await featurePage.expectStepVisible();
    await featurePage.clickStart();

    // Step 2: Another action
    await featurePage.fillInput("value");
    await featurePage.submit();

    // Final assertions
    await featurePage.expectSuccessMessage();
  });
});
```

**Test Naming**: Use descriptive names that explain what the user can do:
- `"allows authenticated user to create a new project"`
- `"shows error when required field is empty"`
- `"redirects to login when not authenticated"`

### 6. Run and Verify

```bash
# Start the e2e stack (if not already running)
docker compose --env-file .env.e2e -f docker-compose.e2e.yml up -d

# Run specific test file
pnpm --filter e2e-tests test:e2e tests/[feature]/[feature].spec.ts

# Run with browser visible (for debugging)
pnpm --filter e2e-tests test:headed tests/[feature]/[feature].spec.ts

# Type check
pnpm --filter e2e-tests typecheck
```

## File Checklist

Before completing, ensure you have created/updated:

- [ ] Page object(s) in `apps/e2e-tests/pages/[PageName].ts`
- [ ] Fixtures in `apps/e2e-tests/tests/[feature]/[feature].fixtures.ts`
- [ ] Test file in `apps/e2e-tests/tests/[feature]/[feature].spec.ts`
- [ ] Tests pass: `pnpm --filter e2e-tests test:e2e tests/[feature]/`
- [ ] Type check passes: `pnpm --filter e2e-tests typecheck`

## Patterns Reference

### Using Shared Types
```typescript
import type { SiteNature, FricheActivity } from "shared";
import { getLabelForSiteNature } from "shared";
```

### Waiting for Async Content
```typescript
// Wait for element to appear
await this.page.getByRole("option").first().waitFor({ state: "visible", timeout: 10000 });

// Wait for navigation
await expect(this.page).toHaveURL("/expected-path");
```

### Form Autocomplete
```typescript
async fillAutocomplete(searchText: string): Promise<void> {
  const input = this.page.getByRole("searchbox", { name: /Label/i });
  await input.pressSequentially(searchText, { delay: 50 });
  const firstOption = this.page.getByRole("option").first();
  await firstOption.waitFor({ state: "visible", timeout: 10000 });
  await firstOption.click();
}
```

### Data Verification
```typescript
async expectDataInList(expectedData: [label: string, value: string][]): Promise<void> {
  for (const [label, value] of expectedData) {
    await expect(
      this.page.locator("dl").filter({ hasText: label }).locator("dt")
    ).toHaveText(value);
  }
}
```

---

## User Flow

$ARGUMENTS
