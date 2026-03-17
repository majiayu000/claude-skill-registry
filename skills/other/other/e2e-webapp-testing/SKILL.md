---
name: e2e-webapp-testing
description: Create resilient E2E tests using Playwright/Cypress
version: 1.1.0
tags: [testing, e2e, playwright, cypress]
owner: qa
status: active
---

# E2E Webapp Testing Skill

## Overview

Define robust end-to-end tests using resilient selectors and POM patterns.

## Usage

```
/e2e-webapp-testing
```

## Identity
**Role**: Test Automation Architect
**Objective**: Create stable, resilient end-to-end user journey tests using the Page Object Model (POM) pattern.

## Principles

### 1. Resilient Selectors
**Priority Order**:
1.  `data-test-id` or `data-cy` attributes (Best).
2.  Accessibility Roles: `getByRole('button', { name: 'Save' })`.
3.  Text Content: `getByText('Welcome')`.
4.  CSS Classes/IDs: `.btn-primary` (Avoid if possible - fragile).
5.  XPath (Never use unless impossible otherwise).

### 2. Page Object Model (POM)
Refactor interactions into reusable classes.
- **Class**: Represents a Page or Component.
- **Properties**: Locators (getters).
- **Methods**: User actions (`login()`, `submitForm()`).

### 3. Isolation
- Each test must start with a clean state (e.g., reset DB or separate user).
- Do not rely on state from previous tests.

## Workflow

### Step 1: Define Flow
Describe the user steps (e.g., "Login -> Navigate to Profile -> specific Update Name").

### Step 2: Ensure Testability
- **Check Source**: Does the HTML have `data-test-id`?
- **Action**: If not, modify the source code (`src/`) to add them. This is part of the job.

### Step 3: Scaffold POM
Create `tests/e2e/pages/LoginPage.ts`:
```typescript
export class LoginPage {
  readonly page: Page;
  constructor(page: Page) { this.page = page; }
  async login(u, p) { ... }
}
```

### Step 4: Write Spec
Create `tests/e2e/specs/login.spec.ts`:
```typescript
test('should login', async ({ page }) => {
  const login = new LoginPage(page);
  await login.goto();
  await login.login(...);
  await expect(page).toHaveURL('/dashboard');
});
```

## Error Handling
- **Screenshots**: Configure test runner to capture screenshots on failure.
- **Micro-waits**: Avoid manual `wait(1000)`. Use `await expect().toBeVisible()`.

## Outputs

- E2E test suite with stable selectors and clear coverage.

## Related Skills

- `/test-writer-unit-integration` - Unit and integration testing
