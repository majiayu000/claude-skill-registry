---
name: web-testing
description: (ePost) Use when writing tests, configuring Jest/Playwright, checking coverage, or working with test patterns
user-invocable: false

metadata:
  agent-affinity: [epost-tester, epost-fullstack-developer]
  keywords: [test, jest, playwright, coverage, e2e, unit-test, rtl, testing-library]
  platforms: [web]
  triggers: ["test", "jest", "playwright", "coverage", "e2e", "unit test", "spec"]
---

# Testing — Jest + Playwright Patterns

## Purpose

Testing patterns for Next.js web applications. Covers Jest + React Testing Library for unit/component tests, Playwright for E2E, and test runner targets.

## Test Structure

Tests live in a `tests/` directory and **mirror the app route structure**:

```
app/[locale]/(auth)/feature-a/utils/mapping/mapping.ts
tests/[locale]/feature-a/utils/mapping/mapping.test.ts

app/[locale]/(auth)/hooks/sidebar/useSidebarBuilder.ts
tests/[locale]/hooks/useSidebarBuilder.test.ts
```

## Jest Configuration

### Project Config

**Location**: `jest.config.ts`

- Uses `next/jest` with `ts-jest` transform
- `testEnvironment: 'jsdom'`
- `pathsToModuleNameMapper` from `tsconfig.base.json` for path aliases
- `@testing-library/jest-dom` loaded via `setupFilesAfterSetup`
- Global mocks for `IntersectionObserver`, `TextEncoder`, `TextDecoder`, `fetch`
- Custom `transformIgnorePatterns` to whitelist ESM-only dependencies

### Coverage

```bash
# Run tests
npm test -- --testFile=path/to/test.test.ts
npm test -- --coverage
```

Coverage is reported via `lcov` + `jest-junit` + `jest-sonar-reporter`. No enforced thresholds — coverage is tracked but not gated.

## Unit Test Patterns

### Mock Function Typing

```typescript
jest.mock('../../caller/feature-caller');
jest.mock('../../app/[locale]/(auth)/feature-a/utils/image-util');

const mockGetLogo = getLogo as jest.MockedFunction<typeof getLogo>;
const mockGetDocumentById = getDocumentById as jest.MockedFunction<typeof getDocumentById>;
```

### Mock Module with Factory

```typescript
// Getter pattern for mutable config
const mockMenuConfig: any[] = [];
jest.mock('../../../app/[locale]/(auth)/config/menu-items.config', () => ({
  get MENU_ITEMS_CONFIG() { return mockMenuConfig; },
}));

// Auto-mock with inline defaults
jest.mock('@app/service/feature-flag-service', () => ({
  getFeatureFlagStatuses: jest.fn().mockResolvedValue(new Map()),
}));
```

### Test Structure

```typescript
describe('feature-service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch logo for given tenant', async () => {
    mockGetLogo.mockResolvedValue(logoData);

    const result = await getLogoForTenant(tenantId);

    expect(mockGetLogo).toHaveBeenCalledWith(tenantId);
    expect(result).toEqual(expectedLogo);
  });
});
```

### Key Patterns

- **Always `jest.clearAllMocks()` in `beforeEach`** — prevents cross-test contamination
- **`jest.MockedFunction<typeof fn>`** — type-safe mock setup
- **Module mocks at top level** — `jest.mock()` calls hoisted automatically
- **Test one behavior per `it()`** — clear arrange/act/assert

## Playwright E2E

### Configuration

**Location**: `playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';
import { getEnvironment } from './tests/config/environments';

const env = getEnvironment(); // reads TEST_ENV env var, defaults to 'dev'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  workers: process.env.CI ? 2 : 3,
  maxFailures: 1,
  use: {
    baseURL: env.baseUrl,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    navigationTimeout: 60000,
    actionTimeout: 30000,
  },
  projects: [
    { name: 'setup-auth', testMatch: '**/setup/authen.setup.ts' },
    { name: 'setup-cleanup', testMatch: '**/setup/cleanup.setup.ts', dependencies: ['setup-auth'] },
    {
      name: 'feature-navigation',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup-auth', 'setup-cleanup'],
      testMatch: '**/feature-a/feature-navigation.spec.ts',
    },
  ],
});
```

### Environment Config

```typescript
// tests/config/environments.ts
export const environments: Record<string, TestEnvironment> = {
  local:   { baseUrl: 'http://localhost:3000', ... },
  dev:     { baseUrl: 'https://app-dev.example.com', ... },
  staging: { baseUrl: 'https://app-staging.example.com', ... },
  test:    { baseUrl: 'https://app-test.example.com', ... },
};
```

### PageHelper

```typescript
// tests/helpers/navigation.helpers.ts
export class PageHelper {
  constructor(private page: Page) {}

  async goToFeatureTab() {
    await this.triggerSelectorAndWaitForNavigation('div[id="feature-a"]', /.*feature-a.*/);
    await expect(this.page).toHaveURL(/.*feature-a.*/);
    return this;
  }

  triggerSelectorAndWaitForNavigation = async (selector: string, urlPattern: RegExp) => {
    const element = await this.page.waitForSelector(selector, { timeout: 5000 });
    await Promise.all([element.click(), this.page.waitForURL(urlPattern, { timeout: 10000 })]);
  };
}
```

### E2E Test Pattern

```typescript
test.describe.serial('Feature Tab - Sequential Tests', () => {
  let pageHelper: PageHelper;

  test.beforeEach(async ({ page }) => {
    test.setTimeout(120000);  // 120 seconds per test
    pageHelper = new PageHelper(page);
    await page.goto(`${env.baseUrl}/en`);
    await page.waitForLoadState('domcontentloaded');
    await pageHelper.goToFeatureTab();
  });

  test('01 - Create Item', async ({ page }) => {
    await createItem({ page, itemName });
  });
});
```

### API Call Helpers

```typescript
// tests/helpers/api-call.helpers.ts — module-level cached auth
export const cleanupTestData = async () => {
  const response = await fetch(`${env.baseUrl}/api/internal/e2e-test/cleanup?tenantId=${tenantId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}`, 'x-api-key': E2E_API_KEY },
  });
};
```

## Test Commands

```bash
# Unit tests
npm test                                       # All tests
npm test -- --testFile=path/to/test            # Single file
npm test -- --coverage                         # With coverage

# E2E tests
TEST_ENV=dev npx playwright test               # Run against dev
npx playwright test --ui                       # Interactive UI mode
```

## Rules

- Mirror app structure in `tests/` directory
- Use `jest.MockedFunction<typeof fn>` for type-safe mocks
- Always `jest.clearAllMocks()` in `beforeEach`
- Use `test.describe.serial` for E2E tests with order dependencies
- Set `test.setTimeout(120000)` for E2E tests — default is too short
- Use page helpers for navigation in E2E
- Use `storageState` for authenticated E2E tests (avoid re-login per test)
