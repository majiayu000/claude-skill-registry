---
name: playwright-automation
description: Playwright testing automation patterns. E2E tests, browser automation, visual testing, API testing. Use when writing automated tests with Playwright.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Playwright Automation - E2E Testing Patterns

## Purpose

Expert guidance for Playwright:

- **E2E Testing** - Full user journey tests
- **Browser Automation** - Cross-browser testing
- **Visual Testing** - Screenshots and comparisons
- **API Testing** - Request mocking and validation
- **Page Object Model** - Maintainable test architecture

---

## Project Structure

```
tests/
├── e2e/
│   ├── fixtures/
│   │   ├── index.ts           # Custom fixtures
│   │   ├── auth.fixture.ts    # Auth helpers
│   │   └── db.fixture.ts      # Database helpers
│   ├── pages/
│   │   ├── base.page.ts       # Base page object
│   │   ├── login.page.ts
│   │   └── dashboard.page.ts
│   ├── flows/
│   │   ├── auth.spec.ts       # Auth flow tests
│   │   └── crud.spec.ts       # CRUD flow tests
│   └── api/
│       └── endpoints.spec.ts  # API-only tests
├── playwright.config.ts
└── global-setup.ts
```

---

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
	testDir: './tests/e2e',
	fullyParallel: true,
	forbidOnly: !!process.env['CI'],
	retries: process.env['CI'] ? 2 : 0,
	workers: process.env['CI'] ? 1 : undefined,
	reporter: 'html',

	use: {
		baseURL: 'http://localhost:3000',
		trace: 'on-first-retry',
		screenshot: 'only-on-failure',
	},

	projects: [
		// Desktop browsers
		{ name: 'chromium', use: { ...devices['Desktop Chrome'] } },
		{ name: 'firefox', use: { ...devices['Desktop Firefox'] } },
		{ name: 'webkit', use: { ...devices['Desktop Safari'] } },

		// Mobile viewports
		{ name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
		{ name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },

		// Tablet
		{ name: 'iPad', use: { ...devices['iPad Pro 11'] } },
	],

	webServer: {
		command: 'bun run dev',
		url: 'http://localhost:3000',
		reuseExistingServer: !process.env['CI'],
	},
});
```

---

## Page Object Model

### Base Page

```typescript
// tests/e2e/pages/base.page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export abstract class BasePage {
	protected readonly page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	// Common elements
	get loadingSpinner(): Locator {
		return this.page.getByTestId('loading-spinner');
	}

	get errorMessage(): Locator {
		return this.page.getByTestId('error-message');
	}

	get successMessage(): Locator {
		return this.page.getByTestId('success-message');
	}

	// Common actions
	async waitForLoad(): Promise<void> {
		await this.loadingSpinner.waitFor({ state: 'hidden' });
	}

	async expectError(message: string): Promise<void> {
		await expect(this.errorMessage).toContainText(message);
	}

	async expectSuccess(message: string): Promise<void> {
		await expect(this.successMessage).toContainText(message);
	}

	// Navigation
	async goto(path: string): Promise<void> {
		await this.page.goto(path);
		await this.waitForLoad();
	}
}
```

### Login Page

```typescript
// tests/e2e/pages/login.page.ts
import { type Page, type Locator } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
	readonly emailInput: Locator;
	readonly passwordInput: Locator;
	readonly submitButton: Locator;
	readonly forgotPasswordLink: Locator;

	constructor(page: Page) {
		super(page);
		this.emailInput = page.getByTestId('email-input');
		this.passwordInput = page.getByTestId('password-input');
		this.submitButton = page.getByTestId('submit-button');
		this.forgotPasswordLink = page.getByRole('link', { name: /forgot/i });
	}

	async goto(): Promise<void> {
		await super.goto('/auth/login');
	}

	async login(email: string, password: string): Promise<void> {
		await this.emailInput.fill(email);
		await this.passwordInput.fill(password);
		await this.submitButton.click();
	}
}
```

---

## Custom Fixtures

### Auth Fixture

```typescript
// tests/e2e/fixtures/auth.fixture.ts
import { test as base, type Page } from '@playwright/test';

export interface TestUser {
	name: string;
	email: string;
	password: string;
}

export function generateTestUser(): TestUser {
	const timestamp = Date.now();
	const random = Math.random().toString(36).substring(7);
	return {
		name: `Test User ${timestamp}`,
		email: `testuser_${timestamp}_${random}@test.com`,
		password: 'TestPassword123!',
	};
}

export async function registerUser(page: Page, user: TestUser): Promise<void> {
	await page.goto('/auth/register');
	await page.getByTestId('name-input').fill(user.name);
	await page.getByTestId('email-input').fill(user.email);
	await page.getByTestId('password-input').fill(user.password);
	await page.getByTestId('confirm-password-input').fill(user.password);
	await page.getByTestId('submit-button').click();
	await page.waitForURL(/\/app/, { timeout: 10000 });
}

export async function loginUser(page: Page, user: TestUser): Promise<void> {
	await page.goto('/auth/login');
	await page.getByTestId('email-input').fill(user.email);
	await page.getByTestId('password-input').fill(user.password);
	await page.getByTestId('submit-button').click();
	await page.waitForURL(/\/app/, { timeout: 10000 });
}
```

### Database Cleanup Fixture

```typescript
// tests/e2e/fixtures/db.fixture.ts
import { test as base } from '@playwright/test';
import { MongoClient, type Db, type ObjectId } from 'mongodb';

type CleanupFixtures = {
	db: Db;
	createdIds: Map<string, ObjectId[]>;
	trackCreated: (collection: string, id: ObjectId) => void;
};

export const test = base.extend<CleanupFixtures>({
	db: async ({}, use) => {
		const client = await MongoClient.connect(process.env['MONGODB_URI']!);
		const db = client.db();
		await use(db);
		await client.close();
	},

	createdIds: async ({}, use) => {
		await use(new Map());
	},

	trackCreated: async ({ createdIds }, use) => {
		await use((collection: string, id: ObjectId) => {
			const existing = createdIds.get(collection) || [];
			existing.push(id);
			createdIds.set(collection, existing);
		});
	},
});

// Auto-cleanup after each test
test.afterEach(async ({ db, createdIds }) => {
	for (const [collection, ids] of createdIds.entries()) {
		if (ids.length > 0) {
			await db.collection(collection).deleteMany({ _id: { $in: ids } });
		}
	}
});

export { expect } from '@playwright/test';
```

---

## Test Patterns

### Auth Flow Test

```typescript
// tests/e2e/flows/auth.spec.ts
import { test, expect } from '../fixtures';
import { generateTestUser, registerUser, loginUser } from '../fixtures/auth.fixture';
import { LoginPage } from '../pages/login.page';

test.describe('Authentication Flow', () => {
	test('complete registration and login journey', async ({ page, db, trackCreated }) => {
		const user = generateTestUser();

		// 1. Register
		await registerUser(page, user);

		// 2. Verify in database
		const dbUser = await db.collection('users').findOne({ email: user.email });
		expect(dbUser).toBeTruthy();
		trackCreated('users', dbUser!._id);

		// 3. Logout
		await page.getByTestId('logout-button').click();
		await expect(page).toHaveURL('/auth/login');

		// 4. Login again
		await loginUser(page, user);
		await expect(page).toHaveURL(/\/app/);
	});

	test('shows error for invalid credentials', async ({ page }) => {
		const loginPage = new LoginPage(page);
		await loginPage.goto();

		await loginPage.login('invalid@email.com', 'wrongpassword');

		await loginPage.expectError('Invalid credentials');
	});
});
```

### Multi-Viewport Test

```typescript
// tests/e2e/flows/responsive.spec.ts
import { test, expect } from '@playwright/test';

const viewports = [
	{ name: 'mobile', width: 375, height: 667 },
	{ name: 'tablet', width: 768, height: 1024 },
	{ name: 'desktop', width: 1280, height: 800 },
] as const;

for (const viewport of viewports) {
	test.describe(`Responsive - ${viewport.name}`, () => {
		test.use({ viewport: { width: viewport.width, height: viewport.height } });

		test('navigation adapts to viewport', async ({ page }) => {
			await page.goto('/');

			if (viewport.width < 768) {
				// Mobile: hamburger menu
				await expect(page.getByTestId('hamburger-menu')).toBeVisible();
				await expect(page.getByTestId('sidebar')).toBeHidden();

				// Open mobile menu
				await page.getByTestId('hamburger-menu').click();
				await expect(page.getByTestId('mobile-nav')).toBeVisible();
			} else {
				// Desktop: sidebar visible
				await expect(page.getByTestId('sidebar')).toBeVisible();
				await expect(page.getByTestId('hamburger-menu')).toBeHidden();
			}
		});
	});
}
```

### API Testing

```typescript
// tests/e2e/api/endpoints.spec.ts
import { test, expect } from '@playwright/test';

test.describe('API Endpoints', () => {
	test('requires authentication', async ({ request }) => {
		const response = await request.get('/api/users');
		expect(response.status()).toBe(401);
	});

	test('validates request body', async ({ request }) => {
		const response = await request.post('/api/users', {
			data: { email: 'invalid-email' },
		});
		expect(response.status()).toBe(400);

		const body = await response.json();
		expect(body.errors).toBeDefined();
	});

	test('creates user with valid data', async ({ request }) => {
		const response = await request.post('/api/users', {
			data: {
				name: 'Test User',
				email: 'test@example.com',
				password: 'Password123!',
			},
		});
		expect(response.status()).toBe(201);

		const user = await response.json();
		expect(user.id).toBeDefined();
		expect(user.email).toBe('test@example.com');
	});
});
```

---

## Commands

```bash
# Run all tests
bunx playwright test

# Run with UI
bunx playwright test --ui

# Run specific file
bunx playwright test auth.spec.ts

# Run specific project (viewport)
bunx playwright test --project="Mobile Chrome"

# Debug mode
bunx playwright test --debug

# Generate report
bunx playwright show-report

# Update snapshots
bunx playwright test --update-snapshots

# Trace viewer
bunx playwright show-trace trace.zip
```

---

## Agent Integration

This skill is used by:

- **playwright-e2e** agent
- **playwright-fixtures** agent
- **playwright-page-objects** agent
- **playwright-multi-viewport** agent
- **test-coverage** skill

---

## FORBIDDEN

1. **Hardcoded test data** - Generate unique data
2. **Skipped tests** - Never use `.skip()` or `.only()`
3. **No cleanup** - Always clean up test data
4. **Mocked auth** - Use real authentication
5. **Single viewport** - Test all viewports

---

## Version

- **v1.0.0** - Initial implementation based on Playwright best practices
