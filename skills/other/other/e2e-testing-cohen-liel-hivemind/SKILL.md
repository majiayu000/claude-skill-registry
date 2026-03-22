---
name: e2e-testing
description: End-to-end testing patterns with Playwright. Use when writing browser automation tests, integration tests, testing user flows, or setting up E2E test suites.
---

# End-to-End Testing Patterns (Playwright)

## Setup
```bash
npm init playwright@latest
npx playwright install  # Install browsers
```

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## Page Object Model
```typescript
// tests/e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test'
export class LoginPage {
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(private page: Page) {
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() { await this.page.goto('/login') }
  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}
```

## Writing Tests
```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'

test.describe('Authentication', () => {
  test('login with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page)
    await loginPage.goto()
    await loginPage.login('user@example.com', 'password123')
    await expect(page).toHaveURL('/dashboard')
  })

  test('show error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page)
    await loginPage.goto()
    await loginPage.login('wrong@email.com', 'wrong')
    await expect(loginPage.errorMessage).toContainText('Invalid credentials')
  })
})
```

## Reuse Auth State
```typescript
// tests/e2e/auth.setup.ts
import { test as setup } from '@playwright/test'
setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name=email]', 'test@example.com')
  await page.fill('[name=password]', 'password')
  await page.click('[type=submit]')
  await page.waitForURL('/dashboard')
  await page.context().storageState({ path: 'tests/e2e/.auth/user.json' })
})

// playwright.config.ts — add these projects:
// { name: 'setup', testMatch: '**/auth.setup.ts' },
// { name: 'authenticated', dependencies: ['setup'], use: { storageState: '...' } }
```

## API Mocking
```typescript
test('displays mocked products', async ({ page }) => {
  await page.route('**/api/products', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([{ id: '1', name: 'Test Product', price: 99.99 }]),
    })
  })
  await page.goto('/products')
  await expect(page.getByText('Test Product')).toBeVisible()
})
```

## Common Assertions
```typescript
await expect(element).toBeVisible()
await expect(element).toContainText('partial text')
await expect(page).toHaveURL('/dashboard')
await expect(page.getByRole('listitem')).toHaveCount(5)
await expect(input).toHaveValue('hello')
await expect(button).toBeDisabled()

// Wait for network response
const response = await page.waitForResponse('**/api/submit')
expect(response.status()).toBe(200)
```

## Running Tests
```bash
npx playwright test                  # All tests
npx playwright test auth.spec.ts     # Specific file
npx playwright test --headed         # Show browser
npx playwright test --ui             # Interactive UI
npx playwright show-report           # HTML report
```

## Rules
- Use Page Object Model — never write raw selectors in test bodies
- Prefer role/label selectors over CSS selectors (more resilient)
- Save auth state with storageState — don't login in every test
- Mock external APIs (payment, email) — test in isolation
- Never use waitForTimeout() — use waitForResponse or waitForSelector
- Run E2E against production build in CI
- E2E for critical paths only — unit test business logic separately
