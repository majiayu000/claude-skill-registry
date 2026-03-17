---
name: e2e-testing
description: End-to-end testing with Cypress and Playwright for IntelliFill. Use when writing E2E tests, custom commands, or CI integration.
---

# E2E Testing Skill

This skill provides comprehensive guidance for writing end-to-end tests in IntelliFill using Cypress and Playwright.

## Table of Contents

1. [Testing Strategy](#testing-strategy)
2. [Cypress Setup](#cypress-setup)
3. [Playwright Setup](#playwright-setup)
4. [Test Patterns](#test-patterns)
5. [Custom Commands](#custom-commands)
6. [Fixtures and Data](#fixtures-and-data)
7. [Docker E2E Setup](#docker-e2e-setup)
8. [CI Integration](#ci-integration)

## Testing Strategy

IntelliFill uses both Cypress and Playwright for E2E testing.

### When to Use Each

**Cypress**:
- Interactive development
- Visual debugging
- Quick feedback loop
- Component testing
- Real browser testing

**Playwright**:
- CI/CD pipelines
- Multi-browser testing
- Headless execution
- Parallel execution
- Network interception

### Test Structure

```
e2e/
├── cypress/
│   ├── e2e/                    # Cypress test specs
│   │   ├── auth/
│   │   │   ├── login.cy.ts
│   │   │   └── registration.cy.ts
│   │   ├── documents/
│   │   │   ├── upload.cy.ts
│   │   │   └── processing.cy.ts
│   │   └── templates/
│   │       └── crud.cy.ts
│   ├── support/
│   │   ├── commands.ts         # Custom commands
│   │   ├── e2e.ts              # Global setup
│   │   └── index.d.ts          # Type definitions
│   └── fixtures/
│       ├── users.json
│       └── documents.json
├── playwright/
│   ├── tests/                  # Playwright test specs
│   │   ├── auth.spec.ts
│   │   ├── documents.spec.ts
│   │   └── templates.spec.ts
│   ├── fixtures/
│   └── helpers/
└── cypress.config.ts
```

## Cypress Setup

### Configuration

```typescript
// e2e/cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8080',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',
    fixturesFolder: 'cypress/fixtures',
    videosFolder: 'cypress/videos',
    screenshotsFolder: 'cypress/screenshots',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,

    env: {
      apiUrl: 'http://localhost:3002/api',
      testUser: {
        email: 'test@example.com',
        password: 'TestPassword123!',
      },
    },

    setupNodeEvents(on, config) {
      // Task plugins
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },

        // Database reset task
        async resetDatabase() {
          // Reset test database
          return null;
        },
      });

      return config;
    },
  },
});
```

### Global Setup

```typescript
// e2e/cypress/support/e2e.ts
import './commands';

// Global before hook
beforeEach(() => {
  // Clear cookies and storage
  cy.clearCookies();
  cy.clearLocalStorage();
});

// Global error handler
Cypress.on('uncaught:exception', (err, runnable) => {
  // Don't fail tests on uncaught exceptions
  // Adjust based on your needs
  return false;
});
```

### Type Definitions

```typescript
// e2e/cypress/support/index.d.ts
declare namespace Cypress {
  interface Chainable {
    /**
     * Custom command to login
     * @example cy.login('user@example.com', 'password')
     */
    login(email: string, password: string): Chainable<void>;

    /**
     * Custom command to register user
     * @example cy.register('user@example.com', 'password')
     */
    register(email: string, password: string): Chainable<void>;

    /**
     * Custom command to upload document
     * @example cy.uploadDocument('document.pdf')
     */
    uploadDocument(fileName: string): Chainable<void>;

    /**
     * Custom command to wait for API call
     * @example cy.waitForApi('POST', '/api/documents')
     */
    waitForApi(method: string, url: string): Chainable<void>;
  }
}
```

## Playwright Setup

### Configuration

```typescript
// e2e/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './playwright/tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:8080',
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
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test Helpers

```typescript
// e2e/playwright/helpers/auth.ts
import { Page } from '@playwright/test';

export async function login(page: Page, email: string, password: string) {
  await page.goto('/login');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');
}

export async function register(page: Page, email: string, password: string) {
  await page.goto('/register');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);
  await page.fill('input[name="confirmPassword"]', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');
}
```

## Test Patterns

### Cypress Test Template

```typescript
// e2e/cypress/e2e/auth/login.cy.ts
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully with valid credentials', () => {
    cy.get('input[name="email"]').type(Cypress.env('testUser').email);
    cy.get('input[name="password"]').type(Cypress.env('testUser').password);
    cy.get('button[type="submit"]').click();

    // Verify redirect to dashboard
    cy.url().should('include', '/dashboard');

    // Verify user is logged in
    cy.contains('Welcome').should('be.visible');
  });

  it('should show error with invalid credentials', () => {
    cy.get('input[name="email"]').type('invalid@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();

    // Verify error message
    cy.contains('Invalid credentials').should('be.visible');

    // Verify still on login page
    cy.url().should('include', '/login');
  });

  it('should validate required fields', () => {
    cy.get('button[type="submit"]').click();

    // Verify validation errors
    cy.contains('Email is required').should('be.visible');
    cy.contains('Password is required').should('be.visible');
  });

  it('should navigate to registration page', () => {
    cy.contains('Sign up').click();
    cy.url().should('include', '/register');
  });
});
```

### Playwright Test Template

```typescript
// e2e/playwright/tests/auth.spec.ts
import { test, expect } from '@playwright/test';
import { login, register } from '../helpers/auth';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await login(page, 'test@example.com', 'password123');

    // Verify redirect
    await expect(page).toHaveURL(/.*dashboard/);

    // Verify user is logged in
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Verify error message
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });

  test('should register new user', async ({ page }) => {
    const email = `test+${Date.now()}@example.com`;
    await register(page, email, 'password123');

    // Verify redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
  });
});
```

### Document Upload Test

```typescript
// e2e/cypress/e2e/documents/upload.cy.ts
describe('Document Upload', () => {
  beforeEach(() => {
    cy.login(Cypress.env('testUser').email, Cypress.env('testUser').password);
    cy.visit('/documents');
  });

  it('should upload document successfully', () => {
    // Intercept upload request
    cy.intercept('POST', '/api/documents/upload').as('uploadDocument');

    // Click upload button
    cy.contains('Upload Document').click();

    // Fill form
    cy.get('input[name="name"]').type('Test Invoice');
    cy.get('input[name="description"]').type('Test invoice document');

    // Upload file
    cy.get('input[type="file"]').attachFile('test-invoice.pdf');

    // Submit
    cy.get('button[type="submit"]').click();

    // Wait for upload
    cy.wait('@uploadDocument').its('response.statusCode').should('eq', 201);

    // Verify success message
    cy.contains('Document uploaded successfully').should('be.visible');

    // Verify document appears in list
    cy.contains('Test Invoice').should('be.visible');
  });

  it('should validate file size', () => {
    cy.contains('Upload Document').click();

    // Upload large file
    cy.get('input[type="file"]').attachFile('large-file.pdf');

    // Verify error
    cy.contains('File must be less than 10MB').should('be.visible');
  });

  it('should validate file type', () => {
    cy.contains('Upload Document').click();

    // Upload invalid file
    cy.get('input[type="file"]').attachFile('document.txt');

    // Verify error
    cy.contains('Only PDF and image files are allowed').should('be.visible');
  });
});
```

### API Testing Pattern

```typescript
// e2e/cypress/e2e/api/documents.cy.ts
describe('Documents API', () => {
  let authToken: string;

  before(() => {
    // Get auth token
    cy.request('POST', `${Cypress.env('apiUrl')}/auth/v2/login`, {
      email: Cypress.env('testUser').email,
      password: Cypress.env('testUser').password,
    }).then((response) => {
      authToken = response.body.token;
    });
  });

  it('should list documents', () => {
    cy.request({
      method: 'GET',
      url: `${Cypress.env('apiUrl')}/documents`,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('success', true);
      expect(response.body.data).to.have.property('items');
      expect(response.body.data.items).to.be.an('array');
    });
  });

  it('should create document', () => {
    cy.request({
      method: 'POST',
      url: `${Cypress.env('apiUrl')}/documents`,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      body: {
        name: 'API Test Document',
        description: 'Created via API',
      },
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body.data).to.have.property('id');
      expect(response.body.data.name).to.eq('API Test Document');
    });
  });

  it('should return 401 without auth', () => {
    cy.request({
      method: 'GET',
      url: `${Cypress.env('apiUrl')}/documents`,
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(401);
    });
  });
});
```

## Custom Commands

### Cypress Custom Commands

```typescript
// e2e/cypress/support/commands.ts
import '@testing-library/cypress/add-commands';

/**
 * Login command
 */
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});

/**
 * Register command
 */
Cypress.Commands.add('register', (email: string, password: string) => {
  cy.visit('/register');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get('input[name="confirmPassword"]').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('include', '/dashboard');
});

/**
 * Upload document command
 */
Cypress.Commands.add('uploadDocument', (fileName: string) => {
  cy.contains('Upload Document').click();
  cy.get('input[name="name"]').type(fileName);
  cy.get('input[type="file"]').attachFile(fileName);
  cy.get('button[type="submit"]').click();
  cy.contains('Document uploaded successfully').should('be.visible');
});

/**
 * Wait for API command
 */
Cypress.Commands.add('waitForApi', (method: string, url: string) => {
  cy.intercept(method, url).as('apiRequest');
  cy.wait('@apiRequest');
});

/**
 * Database reset command
 */
Cypress.Commands.add('resetDatabase', () => {
  cy.task('resetDatabase');
});
```

### Playwright Fixtures

```typescript
// e2e/playwright/fixtures/auth.ts
import { test as base } from '@playwright/test';
import { login } from '../helpers/auth';

export const test = base.extend({
  // Authenticated page fixture
  authenticatedPage: async ({ page }, use) => {
    await login(page, 'test@example.com', 'password123');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

```typescript
// Using fixture
import { test, expect } from '../fixtures/auth';

test('should access protected page', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/documents');
  await expect(authenticatedPage.locator('text=My Documents')).toBeVisible();
});
```

## Fixtures and Data

### Cypress Fixtures

```json
// e2e/cypress/fixtures/users.json
{
  "testUser": {
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  },
  "adminUser": {
    "email": "admin@example.com",
    "password": "AdminPassword123!",
    "name": "Admin User"
  }
}
```

```typescript
// Using fixtures
describe('User Management', () => {
  it('should load user data', () => {
    cy.fixture('users').then((users) => {
      cy.login(users.testUser.email, users.testUser.password);
    });
  });
});
```

### Dynamic Test Data

```typescript
// e2e/cypress/support/testData.ts
export function generateTestUser() {
  const timestamp = Date.now();
  return {
    email: `test+${timestamp}@example.com`,
    password: 'TestPassword123!',
    name: `Test User ${timestamp}`,
  };
}

export function generateTestDocument() {
  return {
    name: `Test Document ${Date.now()}`,
    description: 'E2E test document',
  };
}
```

```typescript
// Using in tests
import { generateTestUser } from '../support/testData';

it('should register new user', () => {
  const user = generateTestUser();
  cy.register(user.email, user.password);
});
```

## Docker E2E Setup

### E2E Dockerfile

```dockerfile
# e2e/Dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy test files
COPY . .

# Install Cypress binary
RUN npx cypress install

# Run tests
CMD ["npm", "run", "test:e2e"]
```

### Docker Compose for E2E

```yaml
# docker-compose.e2e.yml
version: '3.8'

services:
  postgres-test:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: intellifill_test

  redis-test:
    image: redis:7-alpine

  backend-test:
    build:
      context: ./quikadmin
      dockerfile: Dockerfile.dev
    environment:
      NODE_ENV: test
      DATABASE_URL: postgresql://postgres:postgres@postgres-test:5432/intellifill_test
      REDIS_URL: redis://redis-test:6379
    depends_on:
      - postgres-test
      - redis-test
    command: sh -c "npx prisma migrate deploy && npm run dev"

  frontend-test:
    build:
      context: ./quikadmin-web
      dockerfile: Dockerfile.dev
    environment:
      VITE_API_URL: http://backend-test:3002/api
    depends_on:
      - backend-test

  e2e-runner:
    build:
      context: ./e2e
      dockerfile: Dockerfile
    environment:
      CYPRESS_BASE_URL: http://frontend-test:8080
      API_URL: http://backend-test:3002/api
    depends_on:
      - frontend-test
    volumes:
      - ./e2e/cypress/videos:/app/cypress/videos
      - ./e2e/cypress/screenshots:/app/cypress/screenshots
```

### Running E2E Tests

```bash
# Run with Docker Compose
docker-compose -f docker-compose.e2e.yml up --abort-on-container-exit

# Run Cypress locally
cd e2e
npm run cypress:open  # Interactive mode
npm run cypress:run   # Headless mode

# Run Playwright locally
npm run playwright:test  # Run all tests
npm run playwright:ui    # Interactive mode
```

## CI Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  cypress:
    name: Cypress Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run E2E tests
        run: |
          docker-compose -f docker-compose.e2e.yml up --abort-on-container-exit

      - name: Upload Cypress videos
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-videos
          path: e2e/cypress/videos

      - name: Upload Cypress screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-screenshots
          path: e2e/cypress/screenshots

  playwright:
    name: Playwright Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: e2e
        run: npm ci

      - name: Install Playwright browsers
        working-directory: e2e
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        working-directory: e2e
        run: npm run playwright:test

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: e2e/playwright-report
```

## Best Practices

1. **Use data-testid** - Add test IDs to elements for stable selectors
2. **Avoid CSS selectors** - Use semantic selectors and test IDs
3. **Wait for elements** - Don't use arbitrary waits
4. **Test user flows** - Test complete journeys, not just pages
5. **Clean up data** - Reset database between tests
6. **Use fixtures** - Reuse test data
7. **Mock external APIs** - Don't depend on third-party services
8. **Test error states** - Don't just test happy paths
9. **Parallel execution** - Run tests in parallel for speed
10. **Visual regression** - Consider Percy or Chromatic for visual tests

## References

- [Cypress Documentation](https://docs.cypress.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Library](https://testing-library.com/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
