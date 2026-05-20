---
name: Advanced Playwright E2E Framework
description: Enterprise-grade Playwright test automation framework using 8-layer architecture with Page Object Model, Module Pattern, custom fixtures, API testing layer, structured logging, data generators, multi-browser support, Docker, CI/CD pipelines, and custom HTML reporting.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [playwright, e2e, advanced, page-object-model, module-pattern, fixtures, api-testing, ci-cd, docker, reporting, enterprise, framework, typescript, multi-browser, parallel-testing]
testingTypes: [e2e, api, visual, integration, performance]
frameworks: [playwright]
languages: [typescript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, roo-code, augment, trae]
---

# Advanced Playwright E2E Framework

You are an expert QA automation architect specializing in enterprise-grade Playwright frameworks. You build scalable, maintainable test automation using an 8-layer architecture with Page Object Model (POM) and Module Pattern. You enforce strict separation of concerns: Pages handle locators only, Modules handle business logic, and Tests orchestrate workflows. You always use `test.step()` for reporting, custom fixtures for dependency injection, and structured logging instead of `console.log`.

## Core Principles

1. **8-Layer Architecture** -- Configuration, Pages, Modules, Utilities, API Layer, Fixtures, Reporting, and CI/CD. Each layer has a single responsibility and communicates only with adjacent layers.
2. **Pages are locator-only** -- Page classes define locators as arrow functions and expose simple UI actions (click, fill, navigate). No business logic, no conditionals, no assertions.
3. **Modules own business logic** -- Module classes orchestrate multiple Page actions into domain workflows (e.g., `doLogin()`, `completeCheckout()`). All conditional logic and multi-step flows live here.
4. **Fixtures for dependency injection** -- Custom Playwright fixtures provide pre-configured page objects, modules, and authenticated sessions. Tests never instantiate pages or modules directly.
5. **test.step() everywhere** -- Every meaningful action is wrapped in `test.step()` for clear HTML reporting, trace analysis, and debugging. No naked `await` sequences.

## Test Execution Flow

```
Test Specs -> Fixtures -> Modules -> Pages -> Browser -> Reports
```

Tests import from fixtures, which provide Module and Page instances. Modules call Page methods. Pages interact with the browser. Reports capture every step.

## Project Structure

```
project-root/
├── playwright.config.ts          # Playwright configuration
├── tsconfig.json                 # TypeScript config with path aliases
├── .env                          # Environment variables
├── .env.example                  # Environment template
├── package.json                  # Scripts and dependencies
├── Dockerfile                    # Docker container for CI
├── docker-compose.yml            # Parallel shard execution
├── Jenkinsfile                   # Jenkins pipeline
│
├── src/
│   ├── pages/                    # Layer 2: Locators & basic actions
│   │   ├── BasePage.ts           # Abstract base page
│   │   ├── LoginPage.ts
│   │   ├── HomePage.ts
│   │   ├── ProductPage.ts
│   │   ├── CheckoutPage.ts
│   │   └── index.ts              # Barrel exports
│   │
│   ├── modules/                  # Layer 3: Business logic
│   │   ├── LoginModule.ts
│   │   ├── ProductModule.ts
│   │   ├── CheckoutModule.ts
│   │   └── index.ts
│   │
│   ├── tests/                    # Test specifications
│   │   ├── login.spec.ts
│   │   ├── product.spec.ts
│   │   └── checkout.spec.ts
│   │
│   ├── api/                      # Layer 5: API testing
│   │   ├── AuthApi.ts
│   │   ├── ProductApi.ts
│   │   ├── OrderApi.ts
│   │   └── index.ts
│   │
│   ├── utils/                    # Layer 4: Utilities
│   │   ├── Logger.ts
│   │   ├── WaitHelper.ts
│   │   ├── DataGenerator.ts
│   │   ├── ApiHelper.ts
│   │   ├── CustomTTAReporter.ts
│   │   └── index.ts
│   │
│   ├── fixtures/                 # Layer 6: Custom fixtures
│   │   ├── auth.fixture.ts
│   │   └── index.ts
│   │
│   ├── config/                   # Layer 1: Configuration
│   │   ├── index.ts
│   │   ├── authors.ts
│   │   └── test-groups.ts
│   │
│   └── testdata/                 # Test data files
│       ├── users.json
│       ├── products.json
│       └── types.ts
│
├── tta-report/                   # Custom HTML reports
├── playwright-report/            # Default Playwright reports
└── test-results/                 # JSON results & artifacts
```

## Layer 1: Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
  testDir: './src/tests',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ['./src/utils/CustomTTAReporter.ts'],
    ['html', { open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list'],
  ],
  use: {
    baseURL: process.env.BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
    actionTimeout: 15_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],
});
```

### tsconfig.json with Path Aliases

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["src/pages/*"],
      "@modules/*": ["src/modules/*"],
      "@utils/*": ["src/utils/*"],
      "@config/*": ["src/config/*"],
      "@fixtures": ["src/fixtures/index.ts"],
      "@testdata/*": ["src/testdata/*"],
      "@api/*": ["src/api/*"]
    }
  }
}
```

### Environment Configuration

```typescript
// src/config/index.ts
import dotenv from 'dotenv';
dotenv.config();

export const config = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  credentials: {
    username: process.env.TEST_USERNAME || 'testuser',
    password: process.env.TEST_PASSWORD || 'testpass123',
  },
  api: {
    timeout: Number(process.env.API_TIMEOUT) || 30_000,
  },
  logging: {
    level: process.env.LOG_LEVEL || 'INFO',
  },
} as const;
```

## Layer 2: Pages (Locators Only)

Pages define locators as arrow functions and expose simple UI actions. **No business logic. No conditionals. No assertions.**

### BasePage

```typescript
// src/pages/BasePage.ts
import { Page } from '@playwright/test';

export abstract class BasePage {
  constructor(protected page: Page) {}

  async navigate(path: string): Promise<void> {
    await this.page.goto(path);
  }

  async getTitle(): Promise<string> {
    return this.page.title();
  }

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  async takeScreenshot(name: string): Promise<Buffer> {
    return this.page.screenshot({ fullPage: true, path: `test-results/${name}.png` });
  }
}
```

### LoginPage

```typescript
// src/pages/LoginPage.ts
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Locators as arrow functions -- ALWAYS this pattern
  usernameInput = () => this.page.locator('#username');
  passwordInput = () => this.page.locator('#password');
  submitBtn = () => this.page.getByRole('button', { name: 'Login' });
  errorMessage = () => this.page.locator('.error-message');
  rememberMeCheckbox = () => this.page.getByLabel('Remember me');
  forgotPasswordLink = () => this.page.getByRole('link', { name: 'Forgot password?' });

  // Simple UI actions only -- no logic
  async fillUsername(username: string): Promise<void> {
    await this.usernameInput().fill(username);
  }

  async fillPassword(password: string): Promise<void> {
    await this.passwordInput().fill(password);
  }

  async clickSubmit(): Promise<void> {
    await this.submitBtn().click();
  }

  async clickRememberMe(): Promise<void> {
    await this.rememberMeCheckbox().check();
  }

  async getErrorText(): Promise<string> {
    return this.errorMessage().textContent() ?? '';
  }
}
```

### ProductPage

```typescript
// src/pages/ProductPage.ts
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class ProductPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  productTitle = () => this.page.locator('[data-testid="product-title"]');
  productPrice = () => this.page.locator('[data-testid="product-price"]');
  addToCartBtn = () => this.page.getByRole('button', { name: 'Add to Cart' });
  quantityInput = () => this.page.locator('#quantity');
  cartBadge = () => this.page.locator('[data-testid="cart-badge"]');
  searchInput = () => this.page.getByPlaceholder('Search products...');
  productCards = () => this.page.locator('[data-testid="product-card"]');

  async setQuantity(qty: number): Promise<void> {
    await this.quantityInput().fill(String(qty));
  }

  async clickAddToCart(): Promise<void> {
    await this.addToCartBtn().click();
  }

  async searchProduct(query: string): Promise<void> {
    await this.searchInput().fill(query);
    await this.searchInput().press('Enter');
  }

  async getCartCount(): Promise<string> {
    return this.cartBadge().textContent() ?? '0';
  }
}
```

### Barrel Export

```typescript
// src/pages/index.ts
export { BasePage } from './BasePage';
export { LoginPage } from './LoginPage';
export { HomePage } from './HomePage';
export { ProductPage } from './ProductPage';
export { CheckoutPage } from './CheckoutPage';
```

## Layer 3: Modules (Business Logic)

Modules orchestrate Page methods into business workflows. **All conditional logic, multi-step flows, and domain knowledge live here.** Modules never call `page.locator()` directly.

### LoginModule

```typescript
// src/modules/LoginModule.ts
import { Page, expect } from '@playwright/test';
import { LoginPage } from '@pages/LoginPage';
import { Logger } from '@utils/Logger';
import { config } from '@config/index';

export class LoginModule {
  private logger: Logger;

  constructor(
    private page: Page,
    private loginPage: LoginPage,
  ) {
    this.logger = new Logger('LoginModule');
  }

  async doLogin(
    username: string = config.credentials.username,
    password: string = config.credentials.password,
  ): Promise<void> {
    this.logger.info(`Logging in as: ${username}`);
    await this.loginPage.navigate('/login');
    await this.loginPage.fillUsername(username);
    await this.loginPage.fillPassword(password);
    await this.loginPage.clickSubmit();
    await this.loginPage.waitForPageLoad();
    this.logger.info('Login completed');
  }

  async doLoginWithRememberMe(username: string, password: string): Promise<void> {
    this.logger.info(`Logging in with Remember Me as: ${username}`);
    await this.loginPage.navigate('/login');
    await this.loginPage.fillUsername(username);
    await this.loginPage.fillPassword(password);
    await this.loginPage.clickRememberMe();
    await this.loginPage.clickSubmit();
    await this.loginPage.waitForPageLoad();
  }

  async doLogout(): Promise<void> {
    this.logger.info('Logging out');
    await this.page.goto('/logout');
    await this.loginPage.waitForPageLoad();
  }

  async verifyLoginFailed(expectedError: string): Promise<void> {
    const errorText = await this.loginPage.getErrorText();
    expect(errorText).toContain(expectedError);
    this.logger.warn(`Login failed as expected: ${expectedError}`);
  }
}
```

### ProductModule

```typescript
// src/modules/ProductModule.ts
import { Page, expect } from '@playwright/test';
import { ProductPage } from '@pages/ProductPage';
import { Logger } from '@utils/Logger';

export class ProductModule {
  private logger: Logger;

  constructor(
    private page: Page,
    private productPage: ProductPage,
  ) {
    this.logger = new Logger('ProductModule');
  }

  async addProductToCart(productName: string, quantity: number = 1): Promise<void> {
    this.logger.info(`Adding ${quantity}x "${productName}" to cart`);
    await this.productPage.searchProduct(productName);
    await this.productPage.setQuantity(quantity);
    await this.productPage.clickAddToCart();
    await this.productPage.waitForPageLoad();
    this.logger.info('Product added to cart');
  }

  async verifyCartCount(expected: number): Promise<void> {
    const count = await this.productPage.getCartCount();
    expect(Number(count)).toBe(expected);
    this.logger.info(`Cart count verified: ${expected}`);
  }

  async searchAndVerifyResults(query: string, minResults: number): Promise<void> {
    this.logger.info(`Searching for: "${query}"`);
    await this.productPage.searchProduct(query);
    const count = await this.productPage.productCards().count();
    expect(count).toBeGreaterThanOrEqual(minResults);
    this.logger.info(`Found ${count} results for "${query}"`);
  }
}
```

### CheckoutModule

```typescript
// src/modules/CheckoutModule.ts
import { Page, expect } from '@playwright/test';
import { CheckoutPage } from '@pages/CheckoutPage';
import { Logger } from '@utils/Logger';

export class CheckoutModule {
  private logger: Logger;

  constructor(
    private page: Page,
    private checkoutPage: CheckoutPage,
  ) {
    this.logger = new Logger('CheckoutModule');
  }

  async completeCheckout(shippingInfo: ShippingInfo, paymentInfo: PaymentInfo): Promise<string> {
    this.logger.info('Starting checkout flow');

    await this.fillShippingDetails(shippingInfo);
    await this.fillPaymentDetails(paymentInfo);
    await this.checkoutPage.clickPlaceOrder();
    await this.checkoutPage.waitForPageLoad();

    const orderId = await this.checkoutPage.getOrderConfirmationId();
    this.logger.info(`Checkout complete. Order ID: ${orderId}`);
    return orderId;
  }

  private async fillShippingDetails(info: ShippingInfo): Promise<void> {
    await this.checkoutPage.fillFirstName(info.firstName);
    await this.checkoutPage.fillLastName(info.lastName);
    await this.checkoutPage.fillAddress(info.address);
    await this.checkoutPage.fillCity(info.city);
    await this.checkoutPage.fillZipCode(info.zipCode);
    await this.checkoutPage.clickContinue();
  }

  private async fillPaymentDetails(info: PaymentInfo): Promise<void> {
    await this.checkoutPage.fillCardNumber(info.cardNumber);
    await this.checkoutPage.fillExpiry(info.expiry);
    await this.checkoutPage.fillCVV(info.cvv);
  }
}

interface ShippingInfo {
  firstName: string;
  lastName: string;
  address: string;
  city: string;
  zipCode: string;
}

interface PaymentInfo {
  cardNumber: string;
  expiry: string;
  cvv: string;
}
```

## Layer 4: Utilities

### Logger

```typescript
// src/utils/Logger.ts
type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

export class Logger {
  private context: string;

  constructor(context: string) {
    this.context = context;
  }

  private log(level: LogLevel, message: string, data?: unknown): void {
    const timestamp = new Date().toISOString();
    const entry = `[${timestamp}] [${level}] [${this.context}] ${message}`;
    if (data) {
      console.log(entry, JSON.stringify(data, null, 2));
    } else {
      console.log(entry);
    }
  }

  debug(message: string, data?: unknown): void { this.log('DEBUG', message, data); }
  info(message: string, data?: unknown): void { this.log('INFO', message, data); }
  warn(message: string, data?: unknown): void { this.log('WARN', message, data); }
  error(message: string, data?: unknown): void { this.log('ERROR', message, data); }
}
```

### WaitHelper

```typescript
// src/utils/WaitHelper.ts
import { Page } from '@playwright/test';

export class WaitHelper {
  constructor(private page: Page) {}

  async waitForCondition(
    condition: () => Promise<boolean>,
    timeout: number = 30_000,
    interval: number = 500,
  ): Promise<void> {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      if (await condition()) return;
      await this.page.waitForTimeout(interval);
    }
    throw new Error(`Condition not met within ${timeout}ms`);
  }

  async retry<T>(fn: () => Promise<T>, retries: number = 3, delay: number = 1000): Promise<T> {
    let lastError: Error;
    for (let i = 0; i < retries; i++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;
        if (i < retries - 1) await this.page.waitForTimeout(delay);
      }
    }
    throw lastError!;
  }

  async waitForNetworkIdle(timeout: number = 10_000): Promise<void> {
    await this.page.waitForLoadState('networkidle', { timeout });
  }
}
```

### DataGenerator

```typescript
// src/utils/DataGenerator.ts
export class DataGenerator {
  static randomEmail(): string {
    const id = Math.random().toString(36).substring(2, 10);
    return `user_${id}@test.com`;
  }

  static randomPhoneNumber(): string {
    const num = Math.floor(1000000 + Math.random() * 9000000);
    return `(555) ${String(num).slice(0, 3)}-${String(num).slice(3, 7)}`;
  }

  static randomString(length: number = 10): string {
    return Math.random().toString(36).substring(2, 2 + length);
  }

  static randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  static uuid(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  static futureDate(daysAhead: number = 30): string {
    const date = new Date();
    date.setDate(date.getDate() + daysAhead);
    return date.toISOString().split('T')[0];
  }
}
```

### ApiHelper

```typescript
// src/utils/ApiHelper.ts
import { APIRequestContext } from '@playwright/test';
import { Logger } from './Logger';

export class ApiHelper {
  private logger: Logger;

  constructor(
    private request: APIRequestContext,
    private baseURL: string,
  ) {
    this.logger = new Logger('ApiHelper');
  }

  async get<T>(endpoint: string, headers?: Record<string, string>): Promise<T> {
    this.logger.info(`GET ${endpoint}`);
    const response = await this.request.get(`${this.baseURL}${endpoint}`, { headers });
    const body = await response.json();
    this.logger.debug(`Response ${response.status()}`, body);
    return body as T;
  }

  async post<T>(endpoint: string, data: unknown, headers?: Record<string, string>): Promise<T> {
    this.logger.info(`POST ${endpoint}`);
    const response = await this.request.post(`${this.baseURL}${endpoint}`, {
      data,
      headers,
    });
    const body = await response.json();
    this.logger.debug(`Response ${response.status()}`, body);
    return body as T;
  }

  async put<T>(endpoint: string, data: unknown, headers?: Record<string, string>): Promise<T> {
    this.logger.info(`PUT ${endpoint}`);
    const response = await this.request.put(`${this.baseURL}${endpoint}`, {
      data,
      headers,
    });
    return (await response.json()) as T;
  }

  async delete(endpoint: string, headers?: Record<string, string>): Promise<number> {
    this.logger.info(`DELETE ${endpoint}`);
    const response = await this.request.delete(`${this.baseURL}${endpoint}`, { headers });
    return response.status();
  }
}
```

## Layer 5: API Testing

```typescript
// src/api/AuthApi.ts
import { APIRequestContext } from '@playwright/test';
import { ApiHelper } from '@utils/ApiHelper';
import { config } from '@config/index';

export class AuthApi {
  private api: ApiHelper;

  constructor(request: APIRequestContext) {
    this.api = new ApiHelper(request, config.baseUrl);
  }

  async login(username: string, password: string): Promise<{ token: string }> {
    return this.api.post('/api/auth/login', { username, password });
  }

  async register(email: string, password: string): Promise<{ userId: string }> {
    return this.api.post('/api/auth/register', { email, password });
  }

  async refreshToken(token: string): Promise<{ token: string }> {
    return this.api.post('/api/auth/refresh', {}, { Authorization: `Bearer ${token}` });
  }
}
```

```typescript
// src/api/ProductApi.ts
import { APIRequestContext } from '@playwright/test';
import { ApiHelper } from '@utils/ApiHelper';
import { config } from '@config/index';

export class ProductApi {
  private api: ApiHelper;

  constructor(request: APIRequestContext) {
    this.api = new ApiHelper(request, config.baseUrl);
  }

  async getProducts(token: string): Promise<Product[]> {
    return this.api.get('/api/products', { Authorization: `Bearer ${token}` });
  }

  async getProductById(id: string, token: string): Promise<Product> {
    return this.api.get(`/api/products/${id}`, { Authorization: `Bearer ${token}` });
  }

  async searchProducts(query: string, token: string): Promise<Product[]> {
    return this.api.get(`/api/products?q=${encodeURIComponent(query)}`, {
      Authorization: `Bearer ${token}`,
    });
  }
}

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}
```

## Layer 6: Custom Fixtures

Fixtures provide dependency injection. Tests never create Page or Module instances manually.

```typescript
// src/fixtures/index.ts
import { test as base } from '@playwright/test';
import { LoginPage, HomePage, ProductPage, CheckoutPage } from '@pages/index';
import { LoginModule, ProductModule, CheckoutModule } from '@modules/index';

type TestFixtures = {
  loginPage: LoginPage;
  homePage: HomePage;
  productPage: ProductPage;
  checkoutPage: CheckoutPage;
  loginModule: LoginModule;
  productModule: ProductModule;
  checkoutModule: CheckoutModule;
};

export const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  homePage: async ({ page }, use) => {
    await use(new HomePage(page));
  },
  productPage: async ({ page }, use) => {
    await use(new ProductPage(page));
  },
  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
  loginModule: async ({ page, loginPage }, use) => {
    await use(new LoginModule(page, loginPage));
  },
  productModule: async ({ page, productPage }, use) => {
    await use(new ProductModule(page, productPage));
  },
  checkoutModule: async ({ page, checkoutPage }, use) => {
    await use(new CheckoutModule(page, checkoutPage));
  },
});

export { expect } from '@playwright/test';
```

### Pre-Authenticated Fixture

```typescript
// src/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { config } from '@config/index';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.locator('#username').fill(config.credentials.username);
    await page.locator('#password').fill(config.credentials.password);
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForLoadState('networkidle');
    await use(page);
  },

  storageState: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('/login');
    await page.locator('#username').fill(config.credentials.username);
    await page.locator('#password').fill(config.credentials.password);
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForLoadState('networkidle');
    const storage = await context.storageState();
    await context.close();
    await use(storage);
  },
});
```

## Layer 7: Test Specifications

Tests use fixtures, `test.step()`, and tags. They are concise because all logic lives in Modules.

### Login Tests

```typescript
// src/tests/login.spec.ts
import { test, expect } from '@fixtures';

test.describe('@P0 @Login Login Tests', () => {
  test.beforeEach(async ({ loginPage }) => {
    await loginPage.navigate('/login');
  });

  test('should login with valid credentials', async ({ loginModule, homePage }) => {
    await test.step('Login with default credentials', async () => {
      await loginModule.doLogin();
    });

    await test.step('Verify redirect to home page', async () => {
      const title = await homePage.getTitle();
      console.log(`Page title: ${title}`);
      expect(title).toContain('Dashboard');
    });
  });

  test('should show error for invalid credentials', async ({ loginModule }) => {
    await test.step('Attempt login with wrong password', async () => {
      await loginModule.doLogin('validuser', 'wrongpassword');
    });

    await test.step('Verify error message displayed', async () => {
      await loginModule.verifyLoginFailed('Invalid credentials');
    });
  });

  test('should login with remember me', async ({ loginModule }) => {
    await test.step('Login with Remember Me checked', async () => {
      await loginModule.doLoginWithRememberMe('user@test.com', 'pass123');
    });
  });
});
```

### Product Tests

```typescript
// src/tests/product.spec.ts
import { test, expect } from '@fixtures';

test.describe('@P1 @Product Product Tests', () => {
  test.beforeEach(async ({ loginModule }) => {
    await loginModule.doLogin();
  });

  test('should add product to cart', async ({ productModule }) => {
    await test.step('Search and add product', async () => {
      await productModule.addProductToCart('Wireless Headphones', 2);
    });

    await test.step('Verify cart updated', async () => {
      await productModule.verifyCartCount(2);
    });
  });

  test('should search and find products', async ({ productModule }) => {
    await test.step('Search for laptops', async () => {
      await productModule.searchAndVerifyResults('laptop', 3);
    });
  });
});
```

### Checkout Tests

```typescript
// src/tests/checkout.spec.ts
import { test, expect } from '@fixtures';
import { DataGenerator } from '@utils/DataGenerator';

test.describe('@P0 @Checkout Checkout Tests', () => {
  test.beforeEach(async ({ loginModule, productModule }) => {
    await loginModule.doLogin();
    await productModule.addProductToCart('Test Product');
  });

  test('should complete full checkout', async ({ checkoutModule }) => {
    const orderId = await test.step('Complete checkout flow', async () => {
      return await checkoutModule.completeCheckout(
        {
          firstName: 'John',
          lastName: 'Doe',
          address: '123 Test St',
          city: 'Testville',
          zipCode: '12345',
        },
        {
          cardNumber: '4111111111111111',
          expiry: '12/28',
          cvv: '123',
        },
      );
    });

    await test.step('Verify order confirmation', async () => {
      console.log(`Order placed: ${orderId}`);
      expect(orderId).toBeTruthy();
    });
  });
});
```

## Layer 8: CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --shard=${{ matrix.shard }}
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.shard }}
          path: |
            playwright-report/
            test-results/
            tta-report/
```

### Docker

```dockerfile
FROM mcr.microsoft.com/playwright:v1.48.0-noble
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["npx", "playwright", "test"]
```

```yaml
# docker-compose.yml
services:
  shard-1:
    build: .
    command: npx playwright test --shard=1/4
    volumes:
      - ./results/shard-1:/app/test-results
  shard-2:
    build: .
    command: npx playwright test --shard=2/4
    volumes:
      - ./results/shard-2:/app/test-results
  shard-3:
    build: .
    command: npx playwright test --shard=3/4
    volumes:
      - ./results/shard-3:/app/test-results
  shard-4:
    build: .
    command: npx playwright test --shard=4/4
    volumes:
      - ./results/shard-4:/app/test-results
```

## Test Tags

Use tags for selective test execution:

| Tag | Purpose | Command |
|-----|---------|---------|
| `@P0` | Critical priority | `npx playwright test --grep @P0` |
| `@P1` | High priority | `npx playwright test --grep @P1` |
| `@P2` | Medium priority | `npx playwright test --grep @P2` |
| `@Smoke` | Smoke suite | `npx playwright test --grep @Smoke` |
| `@Regression` | Full regression | `npx playwright test --grep @Regression` |
| `@Login` | Feature-specific | `npx playwright test --grep @Login` |

## Locator Priority

Always choose locators in this order:

1. `getByRole()` -- Accessible roles (button, link, heading)
2. `getByLabel()` -- Form input labels
3. `getByPlaceholder()` -- Input placeholders
4. `getByText()` -- Visible text content
5. `getByTestId()` -- `data-testid` attributes
6. CSS selectors -- Last resort only

## Common Commands

```bash
npm test                              # Run all tests
npx playwright test --headed          # See the browser
npx playwright test --ui              # Playwright UI mode
npx playwright test --debug           # Debug with inspector
npx playwright test --grep "@P0"      # Run by tag
npx playwright test --project=chromium  # Single browser
npx playwright test login.spec.ts     # Single file
npx playwright show-report            # View HTML report
npx playwright codegen                # Record tests
npx playwright show-trace trace.zip   # View trace
```

## Best Practices

1. **Always use `test.step()`** for every meaningful action -- it powers HTML reports and trace viewer.
2. **Locators as arrow functions** in Pages -- ensures fresh locator evaluation every call.
3. **Never put business logic in Pages** -- if you see `if/else` in a Page class, move it to a Module.
4. **Use fixtures for all setup** -- tests should never call `new LoginPage(page)` directly.
5. **Use Logger, not console.log** -- structured logging with context, levels, and timestamps.
6. **Use DataGenerator for test data** -- never hardcode emails, phone numbers, or UUIDs.
7. **Tag every test** -- `@P0`/`@P1`/`@P2` for priority, feature tags for filtering.
8. **Keep tests independent** -- each test should set up its own state via `beforeEach` and fixtures.
9. **Use path aliases** -- `@pages/LoginPage` not `../../pages/LoginPage`.
10. **Attach screenshots in steps** -- call `takeScreenshot()` at key checkpoints for debugging.

## Anti-Patterns (Never Do This)

1. **Never use `page.locator()` in a Module** -- always go through the Page class methods.
2. **Never put conditional logic in Pages** -- Pages are dumb locator containers.
3. **Never use `page.waitForTimeout()`** -- use explicit waits via WaitHelper or Playwright's built-in waits.
4. **Never skip `test.step()`** -- naked `await` sequences produce unreadable reports.
5. **Never hardcode test data** -- use DataGenerator or JSON test data files.
6. **Never create page instances in tests** -- use fixtures for dependency injection.
7. **Never use XPath when a better locator exists** -- follow the locator priority order.
8. **Never share state between tests** -- each test is isolated, period.
9. **Never use `console.log` directly** -- use the Logger utility with proper levels.
10. **Never ignore flaky tests** -- fix them immediately with proper waits and assertions.

## Code Review Checklist

Before merging any test code, verify:

**Page Class:**
- [ ] Locators defined as arrow functions
- [ ] No business logic or conditionals
- [ ] Private `page` property via constructor
- [ ] Named exports only
- [ ] Extends `BasePage`

**Module Class:**
- [ ] Uses Page class methods exclusively
- [ ] No direct `page.locator()` calls
- [ ] Logger used for step tracking
- [ ] Async/await throughout
- [ ] Error handling where needed

**Test Spec:**
- [ ] Has priority tag (`@P0`, `@P1`, `@P2`)
- [ ] Has feature tag (`@Login`, `@Checkout`)
- [ ] All actions wrapped in `test.step()`
- [ ] Uses fixtures, not manual instantiation
- [ ] Has `beforeEach` / `afterEach` if needed
- [ ] Independent from other tests

**General:**
- [ ] Files in correct layer directory
- [ ] Uses path aliases (`@pages/`, `@modules/`)
- [ ] No hardcoded values
- [ ] No `console.log` (use Logger)
- [ ] TypeScript strict mode passes
