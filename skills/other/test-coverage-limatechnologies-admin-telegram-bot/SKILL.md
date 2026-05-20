---
name: test-coverage
description: Manages test coverage with Playwright E2E and Vitest unit tests. Tracks which files need tests, provides templates with fixture-based cleanup, enforces multi-viewport testing and database validation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Test Coverage - Testing Management System

## Purpose

This skill manages test coverage with **Playwright E2E** and **Vitest unit tests**:

- **Detects** new files that need tests
- **Maps** components consuming API routes (tRPC/REST)
- **Tracks** which pages have E2E coverage
- **Generates** test templates with cleanup
- **Validates** real authentication usage (MANDATORY)
- **Ensures** database validation after UI actions
- **Enforces** multi-viewport testing

---

## CRITICAL RULES

> **MANDATORY - NO EXCEPTIONS:**

1. **CLEANUP ALL TEST DATA** - Use fixture-based tracking
2. **VERIFY IN DATABASE** - Check DB state after UI actions
3. **TEST ALL VIEWPORTS** - Desktop, tablet, iPhone SE minimum
4. **REAL AUTH ONLY** - Never mock authentication
5. **UNIQUE DATA** - Timestamps in emails/names
6. **NO SKIP** - Never use `.skip()` or `.only()`

---

## Test Structure

```
tests/
├── unit/                     # Unit tests (Vitest)
│   └── *.test.ts
└── e2e/                      # E2E tests (Playwright)
    ├── fixtures/
    │   ├── index.ts          # Custom fixtures (auth, db, cleanup)
    │   ├── auth.fixture.ts   # Authentication helpers
    │   └── db.fixture.ts     # Database connection & cleanup
    ├── pages/                # Page Object Model
    │   ├── base.page.ts      # Base page with common methods
    │   ├── login.page.ts
    │   └── register.page.ts
    ├── flows/                # User flow tests
    │   ├── auth.spec.ts      # Login, register, logout
    │   ├── crud.spec.ts      # Create, read, update, delete
    │   └── permissions.spec.ts
    ├── api/                  # API-only tests (no UI)
    │   ├── rest.spec.ts      # REST API tests
    │   └── trpc.spec.ts      # tRPC API tests
    └── playwright.config.ts
```

---

## Cleanup Fixture (MANDATORY)

Every project MUST have cleanup fixtures:

```typescript
// tests/e2e/fixtures/index.ts
import { test as base, expect } from '@playwright/test';
import { MongoClient, Db, ObjectId } from 'mongodb';

type TestFixtures = {
	db: Db;
	createdIds: Map<string, ObjectId[]>;
	trackCreated: (collection: string, id: ObjectId) => void;
};

export const test = base.extend<TestFixtures>(
	{
		db: async ({}, use) => {
			const client = await MongoClient.connect(process.env.MONGODB_URI!);
			const db = client.db();
			await use(db);
			await client.close();
		},

		createdIds: async ({}, use) => {
			const ids = new Map<string, ObjectId[]>();
			await use(ids);
		},

		trackCreated: async ({ createdIds }, use) => {
			const track = (collection: string, id: ObjectId) => {
				const existing = createdIds.get(collection) || [];
				existing.push(id);
				createdIds.set(collection, existing);
			};
			await use(track);
		},

		// AUTO-CLEANUP runs EVEN IF test fails
	},
	async ({ db, createdIds }, use) => {
		await use();

		for (const [collection, ids] of createdIds.entries()) {
			if (ids.length > 0) {
				await db.collection(collection).deleteMany({
					_id: { $in: ids },
				});
			}
		}
	}
);

export { expect };
```

---

## Auth Helper (MANDATORY)

```typescript
// tests/e2e/fixtures/auth.fixture.ts
import { Page } from '@playwright/test';

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

---

## Test Templates

### E2E Flow Test (with cleanup)

```typescript
import { test, expect } from '../fixtures';
import { generateTestUser, registerUser } from '../fixtures/auth.fixture';

test.describe('[Feature] Flow', () => {
	test('complete user journey', async ({ page, db, trackCreated }) => {
		const user = generateTestUser();

		// 1. Register
		await registerUser(page, user);

		// 2. Verify in database
		const dbUser = await db.collection('users').findOne({
			email: user.email,
		});
		expect(dbUser).toBeTruthy();
		trackCreated('users', dbUser!._id); // TRACK FOR CLEANUP

		// 3. Create item
		await page.goto('/items/new');
		await page.getByTestId('title-input').fill('Test Item');
		await page.getByTestId('submit-button').click();

		// 4. Verify item in DB
		const item = await db.collection('items').findOne({
			userId: dbUser!._id,
		});
		expect(item).toBeTruthy();
		trackCreated('items', item!._id); // TRACK FOR CLEANUP

		// Test continues... cleanup is automatic
	});
});
```

### Multi-Viewport Test

```typescript
import { test, expect } from '../fixtures';

test.describe('Responsive Design', () => {
	const viewports = [
		{ name: 'mobile', width: 375, height: 667 },
		{ name: 'tablet', width: 768, height: 1024 },
		{ name: 'desktop', width: 1280, height: 800 },
	];

	for (const viewport of viewports) {
		test(`layout works on ${viewport.name}`, async ({ page }) => {
			await page.setViewportSize(viewport);
			await page.goto('/');

			if (viewport.width < 768) {
				// Mobile: hamburger menu
				await expect(page.getByTestId('hamburger-menu')).toBeVisible();
				await expect(page.getByTestId('sidebar')).toBeHidden();
			} else {
				// Desktop: sidebar visible
				await expect(page.getByTestId('sidebar')).toBeVisible();
			}
		});
	}
});
```

### API Test (REST)

```typescript
import { test, expect } from '@playwright/test';

test.describe('REST API', () => {
	test('requires authentication', async ({ request }) => {
		const response = await request.get('/api/users');
		expect(response.status()).toBe(401);
	});

	test('validates input', async ({ request }) => {
		const response = await request.post('/api/users', {
			data: { email: 'invalid' },
		});
		expect(response.status()).toBe(400);
	});
});
```

### API Test (tRPC)

```typescript
import { test, expect } from '@playwright/test';

test.describe('tRPC API', () => {
	test('query without auth fails', async ({ request }) => {
		const response = await request.get('/api/trpc/user.me');
		expect(response.status()).toBe(401);
	});

	test('mutation validates input', async ({ request }) => {
		const response = await request.post('/api/trpc/user.create', {
			data: { json: { name: '' } },
		});
		const body = await response.json();
		expect(body.error).toBeDefined();
	});
});
```

### Security Test

```typescript
import { test, expect } from '../fixtures';

test.describe('Security - Forbidden Requests', () => {
	test('cannot access other users data', async ({ page, db }) => {
		const userA = await createTestUser(db);
		const userB = await createTestUser(db);

		await loginAs(page, userA);

		// Try to access user B's data
		const response = await page.request.get(`/api/users/${userB._id}`);
		expect(response.status()).toBe(403);

		// Verify nothing changed in DB
		const unchanged = await db.collection('users').findOne({
			_id: userB._id,
		});
		expect(unchanged).toEqual(userB);
	});
});
```

### Unit Test

```typescript
import { describe, it, expect } from 'vitest';

describe('[Feature]', () => {
	describe('success cases', () => {
		it('should [expected behavior] when [condition]', () => {
			// Arrange
			// Act
			// Assert
		});
	});

	describe('error cases', () => {
		it('should throw when [invalid condition]', () => {
			expect(() => fn(invalid)).toThrow();
		});
	});
});
```

---

## Files That NEED Tests

| Type      | Location              | Test Expected               | Required       |
| --------- | --------------------- | --------------------------- | -------------- |
| API Route | `server/routers/*.ts` | `tests/unit/*.test.ts`      | **YES**        |
| API Route | `app/api/**/*.ts`     | `tests/e2e/api/*.spec.ts`   | **YES**        |
| Model     | `server/models/*.ts`  | `tests/unit/*.test.ts`      | **YES**        |
| Page      | `app/**/page.tsx`     | `tests/e2e/flows/*.spec.ts` | **YES**        |
| Component | `components/**/*.tsx` | `tests/e2e/*.spec.ts`       | If interactive |
| Hook      | `hooks/*.ts`          | `tests/unit/*.test.ts`      | YES            |
| Util      | `lib/*.ts`            | `tests/unit/*.test.ts`      | If exported    |

---

## Required Flows (E2E)

Every app MUST have tests for:

- [ ] **Registration** - Create new user, verify in DB
- [ ] **Login/Logout** - Auth state changes correctly
- [ ] **CRUD Create** - Item created, visible, in DB
- [ ] **CRUD Read** - Item displayed correctly
- [ ] **CRUD Update** - Item updated, changes in DB
- [ ] **CRUD Delete** - Item removed from DB
- [ ] **Permissions** - Forbidden requests blocked
- [ ] **Responsive** - Works on all viewports

---

## Required data-testid

```html
<!-- Forms -->
<input data-testid="name-input" />
<input data-testid="email-input" />
<input data-testid="password-input" />
<input data-testid="confirm-password-input" />
<button data-testid="submit-button" />

<!-- Feedback -->
<div data-testid="error-message" />
<div data-testid="success-message" />
<div data-testid="loading-spinner" />

<!-- Navigation -->
<nav data-testid="sidebar" />
<button data-testid="hamburger-menu" />
<nav data-testid="mobile-nav" />
<button data-testid="logout-button" />

<!-- Actions -->
<button data-testid="delete-button" />
<button data-testid="edit-button" />
<button data-testid="confirm-delete" />
```

---

## Playwright Commands

```bash
# Install
bun add -D @playwright/test
bunx playwright install

# Run
bunx playwright test              # All tests
bunx playwright test --ui         # UI mode (recommended)
bunx playwright test --headed     # See browser
bunx playwright test --debug      # Debug mode

# Specific
bunx playwright test flows/auth   # Specific folder
bunx playwright test --project="iPhone SE"  # Specific viewport

# Reports
bunx playwright show-report
```

---

## Checklist

### Before Commit

- [ ] All new features have E2E tests?
- [ ] Tests use fixtures for cleanup?
- [ ] All created data is tracked and cleaned?
- [ ] Database state verified after UI actions?
- [ ] Tests run on all viewports?
- [ ] Forbidden requests tested?
- [ ] No `.skip()` in tests?
- [ ] `bunx playwright test` passes?
- [ ] `bun run test` passes?

---

## FORBIDDEN (Never Do)

```typescript
// WRONG - Skipping tests
test.skip("should work when authenticated", ...);

// WRONG - Mocking auth
const mockAuth = () => { /* fake */ };

// WRONG - Fixed test user
const testUser = { email: "test@test.com" };

// WRONG - No cleanup
const user = await db.create({ ... });  // Orphaned!

// WRONG - No DB validation
await page.click('submit');
// Just trust the UI? NO!
```

---

## Progressive Disclosure

For detailed patterns and templates, see:

- **[reference/playwright-patterns.md](reference/playwright-patterns.md)** - Page Object Model, fixtures, API testing
- **[scripts/coverage-check.sh](scripts/coverage-check.sh)** - Coverage threshold checker

### Quick Commands

```bash
# Check coverage meets threshold
bash .claude/skills/test-coverage/scripts/coverage-check.sh 80

# Run E2E tests
bunx playwright test

# Run with UI
bunx playwright test --ui
```

---

## Version

- **v3.1.0** - Added progressive disclosure with reference files and scripts
- **v3.0.0** - Complete E2E architecture with cleanup, DB validation, multi-viewport
