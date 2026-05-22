---
name: e2e-test-writer
description: Write comprehensive end-to-end tests using Playwright with page object
  model pattern. Use when creating browser-based tests for user workflows.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, mcp__playwright-mcp__playwright_navigate,
  mcp__playwright-mcp__playwright_screenshot, mcp__playwright-mcp__playwright_click,
  mcp__playwright-mcp__playwright_fill, mcp__playwright-mcp__playwright_evaluate
---

# E2E Test Writer Skill

## Purpose

This skill provides comprehensive guidance for writing end-to-end tests using Playwright, following best practices including page object model pattern, proper test isolation, and maintainable test architecture.

## When to Use

- Implementing E2E tests for new features
- Testing user workflows and journeys
- Validating browser interactions
- Testing responsive design across devices
- Regression testing after changes
- CI/CD test automation

## E2E Testing Workflow

### 1. Setup Playwright Project

**Initialize Playwright:**

```bash
# Install Playwright
npm init playwright@latest

# Or add to existing project
npm install -D @playwright/test
npx playwright install
```

**Project Structure:**

```
tests/
├── e2e/
│   ├── auth/
│   ├── features/
│   └── workflows/
├── pages/
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   └── DashboardPage.ts
├── fixtures/
│   ├── test-data.ts
│   └── custom-fixtures.ts
├── utils/
│   ├── helpers.ts
│   └── constants.ts
└── playwright.config.ts
```

**Playwright Configuration:**

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**Deliverable:** Playwright project configured and ready

---

### 2. Page Object Model Pattern

**Base Page Class:**

```typescript
// pages/BasePage.ts
import { Page, Locator } from '@playwright/test';

export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto(path: string) {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  async clickElement(locator: Locator) {
    await locator.waitFor({ state: 'visible' });
    await locator.click();
  }

  async fillInput(locator: Locator, value: string) {
    await locator.waitFor({ state: 'visible' });
    await locator.fill(value);
  }

  async getText(locator: Locator): Promise<string> {
    await locator.waitFor({ state: 'visible' });
    return await locator.textContent() || '';
  }
}
```

**Example Page Object:**

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  // Locators
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signUpLink: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
    this.forgotPasswordLink = page.locator('a[href="/forgot-password"]');
    this.signUpLink = page.locator('a[href="/signup"]');
  }

  // Actions
  async goto() {
    await super.goto('/login');
  }

  async login(username: string, password: string) {
    await this.fillInput(this.usernameInput, username);
    await this.fillInput(this.passwordInput, password);
    await this.clickElement(this.submitButton);
  }

  async clickForgotPassword() {
    await this.clickElement(this.forgotPasswordLink);
  }

  async clickSignUp() {
    await this.clickElement(this.signUpLink);
  }

  // Assertions helpers
  async getErrorMessage(): Promise<string> {
    return await this.getText(this.errorMessage);
  }

  async isLoginButtonEnabled(): Promise<boolean> {
    return await this.submitButton.isEnabled();
  }

  async waitForErrorMessage() {
    await this.errorMessage.waitFor({ state: 'visible' });
  }
}
```

**Deliverable:** Page objects for all application pages

---

### 3. Writing Test Cases

**Basic Test Structure:**

```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { DashboardPage } from '../../pages/DashboardPage';

test.describe('User Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login with valid credentials', async ({ page }) => {
    await loginPage.login('user@example.com', 'ValidPassword123!');

    const dashboardPage = new DashboardPage(page);
    await expect(page).toHaveURL('/dashboard');
    await expect(dashboardPage.welcomeMessage).toContainText('Welcome back');
  });

  test('failed login with invalid credentials shows error', async ({ page }) => {
    await loginPage.login('user@example.com', 'WrongPassword');

    await loginPage.waitForErrorMessage();
    const errorMsg = await loginPage.getErrorMessage();
    expect(errorMsg).toContain('Invalid username or password');
    await expect(page).toHaveURL('/login');
  });

  test('login button disabled with empty fields', async ({ page }) => {
    const isEnabled = await loginPage.isLoginButtonEnabled();
    expect(isEnabled).toBe(false);
  });

  test('forgot password link navigates correctly', async ({ page }) => {
    await loginPage.clickForgotPassword();
    await expect(page).toHaveURL('/forgot-password');
  });

  test('sign up link navigates correctly', async ({ page }) => {
    await loginPage.clickSignUp();
    await expect(page).toHaveURL('/signup');
  });
});
```

**Testing User Workflows:**

```typescript
// tests/e2e/workflows/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { ProductPage } from '../../pages/ProductPage';
import { CartPage } from '../../pages/CartPage';
import { CheckoutPage } from '../../pages/CheckoutPage';

test.describe('Checkout Workflow', () => {
  test('complete purchase from product to confirmation', async ({ page }) => {
    // 1. Browse product
    const productPage = new ProductPage(page);
    await productPage.goto('/products/item-123');
    await expect(productPage.productTitle).toBeVisible();

    // 2. Add to cart
    await productPage.addToCart();
    await expect(productPage.cartBadge).toHaveText('1');

    // 3. View cart
    await productPage.goToCart();
    const cartPage = new CartPage(page);
    await expect(cartPage.cartItems).toHaveCount(1);

    // 4. Proceed to checkout
    await cartPage.proceedToCheckout();
    const checkoutPage = new CheckoutPage(page);

    // 5. Fill shipping info
    await checkoutPage.fillShippingInfo({
      name: 'John Doe',
      address: '123 Main St',
      city: 'San Francisco',
      zip: '94102',
      country: 'US',
    });

    // 6. Fill payment info
    await checkoutPage.fillPaymentInfo({
      cardNumber: '4242424242424242',
      expiry: '12/25',
      cvv: '123',
    });

    // 7. Submit order
    await checkoutPage.submitOrder();

    // 8. Verify confirmation
    await expect(page).toHaveURL(/\/order-confirmation/);
    await expect(page.locator('.success-message')).toContainText('Order placed successfully');
  });
});
```

**Deliverable:** Comprehensive test suite covering user journeys

---

### 4. Test Data Management

**Test Fixtures:**

```typescript
// fixtures/test-data.ts
export const testUsers = {
  validUser: {
    email: 'user@example.com',
    password: 'ValidPassword123!',
  },
  adminUser: {
    email: 'admin@example.com',
    password: 'AdminPassword123!',
  },
  newUser: {
    email: 'newuser@example.com',
    password: 'NewPassword123!',
    firstName: 'John',
    lastName: 'Doe',
  },
};

export const testProducts = {
  product1: {
    id: 'item-123',
    name: 'Test Product',
    price: 29.99,
  },
};
```

**Custom Fixtures:**

```typescript
// fixtures/custom-fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

type MyFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Auto-login before test
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'ValidPassword123!');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

**Using Custom Fixtures:**

```typescript
// tests/e2e/features/profile.spec.ts
import { test, expect } from '../../fixtures/custom-fixtures';

test.describe('User Profile', () => {
  test('user can update profile information', async ({ authenticatedPage, dashboardPage }) => {
    // Already logged in via authenticatedPage fixture
    await dashboardPage.goToProfile();

    // Test continues with authenticated context
    await dashboardPage.updateProfile({
      firstName: 'Jane',
      lastName: 'Smith',
    });

    await expect(dashboardPage.profileName).toHaveText('Jane Smith');
  });
});
```

**Deliverable:** Reusable test data and fixtures

---

### 5. Responsive Design Testing

**Test Multiple Viewports:**

```typescript
// tests/e2e/responsive/layout.spec.ts
import { test, expect, devices } from '@playwright/test';

const viewports = [
  { name: 'Desktop', device: devices['Desktop Chrome'] },
  { name: 'Tablet', device: devices['iPad Pro'] },
  { name: 'Mobile', device: devices['iPhone 12'] },
];

viewports.forEach(({ name, device }) => {
  test.describe(`${name} Layout`, () => {
    test.use(device);

    test('navigation menu displays correctly', async ({ page }) => {
      await page.goto('/');

      if (name === 'Mobile') {
        // Mobile should show hamburger menu
        await expect(page.locator('.hamburger-menu')).toBeVisible();
        await expect(page.locator('.desktop-nav')).not.toBeVisible();
      } else {
        // Desktop/Tablet should show full navigation
        await expect(page.locator('.desktop-nav')).toBeVisible();
        await expect(page.locator('.hamburger-menu')).not.toBeVisible();
      }
    });

    test('images are responsive', async ({ page }) => {
      await page.goto('/products');

      const images = page.locator('img');
      const count = await images.count();

      for (let i = 0; i < count; i++) {
        const img = images.nth(i);
        const bbox = await img.boundingBox();
        if (bbox) {
          // Images should not overflow viewport
          expect(bbox.width).toBeLessThanOrEqual(device.viewport.width);
        }
      }
    });
  });
});
```

**Deliverable:** Tests covering responsive design

---

### 6. Visual Regression Testing

**Screenshot Comparison:**

```typescript
// tests/e2e/visual/snapshot.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches baseline', async ({ page }) => {
    await page.goto('/');

    // Take full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('modal dialog matches baseline', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="open-modal"]');

    // Screenshot of specific element
    const modal = page.locator('.modal');
    await expect(modal).toHaveScreenshot('modal.png');
  });

  test('dark mode matches baseline', async ({ page }) => {
    await page.goto('/');

    // Enable dark mode
    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark');
    });

    await expect(page).toHaveScreenshot('homepage-dark.png', {
      fullPage: true,
    });
  });
});
```

**Deliverable:** Visual regression test suite

---

### 7. API Mocking and Network Testing

**Mock API Responses:**

```typescript
// tests/e2e/network/api-mocking.spec.ts
import { test, expect } from '@playwright/test';

test.describe('API Mocking', () => {
  test('handles slow API response gracefully', async ({ page }) => {
    // Mock slow API
    await page.route('**/api/products', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 3000));
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ products: [] }),
      });
    });

    await page.goto('/products');

    // Should show loading state
    await expect(page.locator('.loading-spinner')).toBeVisible();

    // Should eventually show products
    await expect(page.locator('.product-list')).toBeVisible({ timeout: 5000 });
  });

  test('handles API error gracefully', async ({ page }) => {
    // Mock API error
    await page.route('**/api/products', (route) => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Internal server error' }),
      });
    });

    await page.goto('/products');

    // Should show error message
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('Failed to load products');
  });

  test('handles network timeout', async ({ page }) => {
    await page.route('**/api/products', (route) => {
      // Never fulfill, causing timeout
    });

    await page.goto('/products');

    // Should show timeout message
    await expect(page.locator('.timeout-message')).toBeVisible({ timeout: 10000 });
  });
});
```

**Deliverable:** Tests for API interactions and error states

---

### 8. Authentication State Management

**Reuse Authentication State:**

```typescript
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'ValidPassword123!');

  await page.waitForURL('/dashboard');

  // Save authentication state
  await page.context().storageState({ path: authFile });
});
```

**Use Saved Auth State:**

```typescript
// playwright.config.ts
export default defineConfig({
  // ... other config

  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

**Deliverable:** Efficient authentication handling

---

## Best Practices

**Test Organization:**
- Group related tests with `test.describe()`
- Use meaningful test names (describe behavior, not implementation)
- One assertion per test (or closely related assertions)
- Isolate tests (no dependencies between tests)

**Locator Strategy:**
- Prefer test IDs: `page.locator('[data-testid="submit"]')`
- Use semantic selectors: `page.locator('button:has-text("Submit")')`
- Avoid CSS selectors tied to styling
- Never use XPath unless absolutely necessary

**Waiting Strategy:**
- Use auto-waiting (built into Playwright)
- Avoid fixed waits (`page.waitForTimeout()`)
- Use `waitForLoadState()` for page loads
- Use `waitFor()` for specific elements

**Error Handling:**
- Use try-catch for expected errors
- Add screenshots on failure
- Capture network logs
- Record video on failure

**Performance:**
- Run tests in parallel when possible
- Use `test.describe.configure({ mode: 'parallel' })`
- Share browser contexts when safe
- Reuse authentication state
- Mock slow external APIs

**Maintainability:**
- Page Object Model for all pages
- Extract common logic to helpers
- Use constants for repeated values
- Keep tests DRY (Don't Repeat Yourself)
- Regular refactoring

---

## Integration with Playwright MCP

**Using MCP Tools:**

```typescript
// Example: Using Playwright MCP for navigation
test('navigate using MCP', async ({ page }) => {
  // Use mcp__playwright-mcp__playwright_navigate
  await page.evaluate(async () => {
    // MCP navigation call would go here
  });

  await expect(page).toHaveURL('/expected-page');
});

// Example: Using MCP for screenshots
test('capture screenshot with MCP', async ({ page }) => {
  await page.goto('/');

  // Use mcp__playwright-mcp__playwright_screenshot
  await page.evaluate(async () => {
    // MCP screenshot call would go here
  });
});
```

---

## Remember

- **Test behavior, not implementation**: Tests should survive refactoring
- **User perspective**: Test what users do, not how code works
- **Isolation**: Each test should run independently
- **Fast feedback**: Keep tests fast (< 5 min total suite)
- **Flake-free**: No intermittent failures
- **Clear failures**: Easy to debug when tests fail
- **Maintainable**: Easy to update when app changes
- **Comprehensive**: Cover happy paths and edge cases
- **CI/CD ready**: Tests run reliably in CI environment

Your goal is to create robust, maintainable E2E tests that provide confidence in application functionality across browsers and devices.