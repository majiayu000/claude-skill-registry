---
name: e2e-playwright
description: Comprehensive Playwright end-to-end testing expertise covering browser automation, cross-browser testing, visual regression, API testing, mobile emulation, accessibility testing, test architecture, page object models, fixtures, parallel execution, CI/CD integration, debugging strategies, and production-grade E2E test patterns. Activates for playwright, e2e testing, end-to-end testing, browser automation, cross-browser testing, visual testing, screenshot testing, API testing, mobile testing, accessibility testing, test fixtures, page object model, POM, test architecture, parallel testing, playwright config, trace viewer, codegen, test debugging, flaky tests, CI integration, playwright best practices.
---

# E2E Playwright Testing Expert

## Core Expertise

### 1. Playwright Fundamentals
**Browser Automation**:
- Multi-browser support (Chromium, Firefox, WebKit)
- Context isolation and parallel execution
- Auto-waiting and actionability checks
- Network interception and mocking
- File downloads and uploads
- Geolocation and permissions
- Authentication state management

**Test Structure**:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login successfully', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('should show validation errors', async ({ page }) => {
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });
});
```

### 2. Page Object Model (POM)
**Pattern**: Encapsulate page interactions for maintainability

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async loginWithGoogle() {
    await this.page.getByRole('button', { name: 'Continue with Google' }).click();
    // Handle OAuth popup
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// Usage in tests
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### 3. Test Fixtures & Custom Contexts
**Fixtures**: Reusable setup/teardown logic

```typescript
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type AuthFixtures = {
  authenticatedPage: Page;
  loginPage: LoginPage;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: Login before test
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForURL('/dashboard');

    await use(page);

    // Teardown: Logout after test
    await page.getByRole('button', { name: 'Logout' }).click();
  },

  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },
});

export { expect } from '@playwright/test';

// Usage
test('authenticated user can view profile', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage.getByText('Profile Settings')).toBeVisible();
});
```

### 4. API Testing with Playwright
**Pattern**: Test backend APIs alongside E2E flows

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Testing', () => {
  test('should fetch user data', async ({ request }) => {
    const response = await request.get('/api/users/123');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toMatchObject({
      id: 123,
      email: expect.any(String),
      name: expect.any(String),
    });
  });

  test('should handle authentication', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'user@example.com',
        password: 'password123',
      },
    });

    expect(response.ok()).toBeTruthy();
    const { token } = await response.json();
    expect(token).toBeTruthy();

    // Use token in subsequent requests
    const profileResponse = await request.get('/api/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    expect(profileResponse.ok()).toBeTruthy();
  });

  test('should mock API responses', async ({ page }) => {
    await page.route('/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([
          { id: 1, name: 'John Doe' },
          { id: 2, name: 'Jane Smith' },
        ]),
      });
    });

    await page.goto('/users');
    await expect(page.getByText('John Doe')).toBeVisible();
    await expect(page.getByText('Jane Smith')).toBeVisible();
  });
});
```

### 5. Visual Regression Testing
**Pattern**: Screenshot comparison for UI changes

```typescript
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches baseline', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('component states', async ({ page }) => {
    await page.goto('/components');

    // Default state
    const button = page.getByRole('button', { name: 'Submit' });
    await expect(button).toHaveScreenshot('button-default.png');

    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');

    // Disabled state
    await page.evaluate(() => {
      document.querySelector('button')?.setAttribute('disabled', 'true');
    });
    await expect(button).toHaveScreenshot('button-disabled.png');
  });

  test('responsive screenshots', async ({ page }) => {
    await page.goto('/');

    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('homepage-desktop.png');

    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('homepage-tablet.png');

    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
```

### 6. Mobile Emulation & Device Testing
**Pattern**: Test responsive behavior and touch interactions

```typescript
import { test, expect, devices } from '@playwright/test';

test.use(devices['iPhone 13 Pro']);

test.describe('Mobile Experience', () => {
  test('should render mobile navigation', async ({ page }) => {
    await page.goto('/');

    // Mobile menu should be visible
    await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible();

    // Desktop nav should be hidden
    await expect(page.getByRole('navigation').first()).toBeHidden();
  });

  test('touch gestures', async ({ page }) => {
    await page.goto('/gallery');

    const image = page.getByRole('img').first();

    // Swipe left
    await image.dispatchEvent('touchstart', { touches: [{ clientX: 300, clientY: 200 }] });
    await image.dispatchEvent('touchmove', { touches: [{ clientX: 100, clientY: 200 }] });
    await image.dispatchEvent('touchend');

    await expect(page.getByText('Next Image')).toBeVisible();
  });

  test('landscape orientation', async ({ page }) => {
    await page.setViewportSize({ width: 812, height: 375 }); // iPhone landscape
    await page.goto('/video');

    await expect(page.locator('video')).toHaveCSS('width', '100%');
  });
});

// Test across multiple devices
for (const deviceName of ['iPhone 13', 'Pixel 5', 'iPad Pro']) {
  test.describe(`Device: ${deviceName}`, () => {
    test.use(devices[deviceName]);

    test('critical user flow', async ({ page }) => {
      await page.goto('/');
      // Test critical flow on each device
    });
  });
}
```

### 7. Accessibility Testing
**Pattern**: Automated accessibility checks

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('keyboard navigation', async ({ page }) => {
    await page.goto('/form');

    // Tab through form fields
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Email')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Password')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Submit' })).toBeFocused();

    // Submit with Enter
    await page.keyboard.press('Enter');
  });

  test('screen reader support', async ({ page }) => {
    await page.goto('/');

    // Check ARIA labels
    await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible();
    await expect(page.getByRole('main')).toHaveAttribute('aria-label', 'Main content');

    // Check alt text
    const images = page.getByRole('img');
    for (const img of await images.all()) {
      await expect(img).toHaveAttribute('alt');
    }
  });
});
```

### 8. Performance Testing
**Pattern**: Monitor performance metrics

```typescript
import { test, expect } from '@playwright/test';

test.describe('Performance', () => {
  test('page load performance', async ({ page }) => {
    await page.goto('/');

    const performanceMetrics = await page.evaluate(() => {
      const perfData = window.performance.timing;
      return {
        loadTime: perfData.loadEventEnd - perfData.navigationStart,
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
      };
    });

    expect(performanceMetrics.loadTime).toBeLessThan(3000); // 3s max
    expect(performanceMetrics.domContentLoaded).toBeLessThan(2000); // 2s max
  });

  test('Core Web Vitals', async ({ page }) => {
    await page.goto('/');

    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lcp = entries.find(e => e.entryType === 'largest-contentful-paint');
          const fid = entries.find(e => e.entryType === 'first-input');
          const cls = entries.find(e => e.entryType === 'layout-shift');

          resolve({ lcp: lcp?.startTime, fid: fid?.processingStart, cls: cls?.value });
        }).observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] });
      });
    });

    expect(vitals.lcp).toBeLessThan(2500); // Good LCP
    expect(vitals.fid).toBeLessThan(100);  // Good FID
    expect(vitals.cls).toBeLessThan(0.1);  // Good CLS
  });
});
```

### 9. Advanced Configuration
**playwright.config.ts**:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Desktop browsers
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
    // Mobile browsers
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
    // Tablet browsers
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### 10. CI/CD Integration
**GitHub Actions**:

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: https://staging.example.com

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload traces
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-traces
          path: test-results/
```

### 11. Debugging Strategies
**Tools & Techniques**:

```typescript
// 1. Debug mode (headed browser + slow motion)
test('debug example', async ({ page }) => {
  await page.goto('/');
  await page.pause(); // Pauses execution, opens inspector
});

// 2. Console logs
test('capture console', async ({ page }) => {
  page.on('console', msg => console.log(`Browser: ${msg.text()}`));
  await page.goto('/');
});

// 3. Network inspection
test('inspect network', async ({ page }) => {
  page.on('request', request => console.log('Request:', request.url()));
  page.on('response', response => console.log('Response:', response.status()));
  await page.goto('/');
});

// 4. Screenshots on failure
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    await page.screenshot({
      path: `screenshots/${testInfo.title}.png`,
      fullPage: true
    });
  }
});

// 5. Trace viewer
// Run: npx playwright test --trace on
// View: npx playwright show-trace trace.zip
```

**Common Debugging Commands**:
```bash
# Run in headed mode (see browser)
npx playwright test --headed

# Run with UI mode (interactive debugging)
npx playwright test --ui

# Run single test
npx playwright test tests/login.spec.ts

# Debug specific test
npx playwright test tests/login.spec.ts --debug

# Generate test code
npx playwright codegen http://localhost:3000
```

### 12. Handling Flaky Tests
**Patterns for Reliability**:

```typescript
// 1. Proper waiting strategies
test('wait for content', async ({ page }) => {
  await page.goto('/');

  // ❌ BAD: Fixed delays
  // await page.waitForTimeout(5000);

  // ✅ GOOD: Wait for specific conditions
  await page.waitForLoadState('networkidle');
  await page.waitForSelector('.content', { state: 'visible' });
  await page.getByText('Welcome').waitFor();
});

// 2. Retry logic for external dependencies
test('api with retry', async ({ page }) => {
  await page.goto('/');

  let retries = 3;
  while (retries > 0) {
    try {
      const response = await page.waitForResponse(
        response => response.url().includes('/api/data') && response.ok(),
        { timeout: 5000 }
      );
      expect(response.ok()).toBeTruthy();
      break;
    } catch (error) {
      retries--;
      if (retries === 0) throw error;
      await page.reload();
    }
  }
});

// 3. Test isolation
test.describe.configure({ mode: 'parallel' });

test.beforeEach(async ({ page }) => {
  // Clear state before each test
  await page.context().clearCookies();
  await page.context().clearPermissions();
});

// 4. Deterministic test data
test('use fixtures', async ({ page }) => {
  // Seed database with known data
  await page.request.post('/api/test/seed', {
    data: { userId: 'test-123', email: 'test@example.com' }
  });

  await page.goto('/users/test-123');
  await expect(page.getByText('test@example.com')).toBeVisible();

  // Cleanup
  await page.request.delete('/api/test/users/test-123');
});
```

## Best Practices

### Test Organization
```
e2e/
├── fixtures/
│   ├── auth.fixture.ts
│   ├── data.fixture.ts
│   └── mock.fixture.ts
├── pages/
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── ProfilePage.ts
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── signup.spec.ts
│   │   └── logout.spec.ts
│   ├── user/
│   │   ├── profile.spec.ts
│   │   └── settings.spec.ts
│   └── api/
│       ├── users.spec.ts
│       └── posts.spec.ts
└── playwright.config.ts
```

### Naming Conventions
- Test files: `*.spec.ts` or `*.test.ts`
- Page objects: `*Page.ts`
- Fixtures: `*.fixture.ts`
- Descriptive test names: `should allow user to login with valid credentials`

### Performance Optimization
1. **Parallel execution**: Run tests in parallel across workers
2. **Test sharding**: Split tests across CI machines
3. **Selective testing**: Use tags/annotations for smoke tests
4. **Reuse authentication**: Save auth state, reuse across tests
5. **Mock external APIs**: Reduce network latency and flakiness

### Security Considerations
- Never commit credentials in test files
- Use environment variables for sensitive data
- Isolate test data from production
- Clear cookies/storage between tests
- Use disposable test accounts

## Common Patterns

### Authentication State Reuse
```typescript
// global-setup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL('http://localhost:3000/dashboard');

  // Save signed-in state
  await page.context().storageState({ path: 'auth.json' });
  await browser.close();
}

export default globalSetup;

// playwright.config.ts
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  use: {
    storageState: 'auth.json',
  },
});
```

### Multi-Tab/Window Testing
```typescript
test('open in new tab', async ({ context }) => {
  const page = await context.newPage();
  await page.goto('/');

  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page.getByRole('link', { name: 'Open in new tab' }).click()
  ]);

  await newPage.waitForLoadState();
  await expect(newPage).toHaveURL('/new-page');
});
```

### File Upload/Download
```typescript
test('upload file', async ({ page }) => {
  await page.goto('/upload');

  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: 'Upload' }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('path/to/file.pdf');

  await expect(page.getByText('file.pdf uploaded')).toBeVisible();
});

test('download file', async ({ page }) => {
  await page.goto('/downloads');

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('link', { name: 'Download Report' }).click();
  const download = await downloadPromise;

  await download.saveAs(`/tmp/${download.suggestedFilename()}`);
  expect(download.suggestedFilename()).toBe('report.pdf');
});
```

## Troubleshooting

### Common Issues
1. **Timeouts**: Increase timeout, use proper wait strategies
2. **Flaky selectors**: Use stable locators (roles, labels, test IDs)
3. **Race conditions**: Wait for network idle, use explicit waits
4. **Authentication failures**: Clear cookies, check auth state
5. **Screenshot mismatches**: Update baselines, disable animations

### Debug Checklist
- [ ] Test passes locally in headed mode?
- [ ] Network requests succeed (check DevTools)?
- [ ] Selectors are stable and unique?
- [ ] Proper waits before assertions?
- [ ] Test data is deterministic?
- [ ] No race conditions with async operations?
- [ ] Traces/screenshots captured on failure?

## Resources
- **Official Docs**: https://playwright.dev
- **API Reference**: https://playwright.dev/docs/api/class-playwright
- **Best Practices**: https://playwright.dev/docs/best-practices
- **Examples**: https://github.com/microsoft/playwright/tree/main/examples
- **Community**: https://github.com/microsoft/playwright/discussions
