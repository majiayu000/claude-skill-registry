---
name: e2e-test
description: Write and validate Playwright E2E tests for Momentum CMS features. UI tests ALWAYS start from /admin dashboard and navigate via sidebar/dashboard — never go directly to deep URLs. Always starts the server and inspects the actual UI before writing assertions. Triggers include "write e2e tests for...", "add e2e tests", "test the admin UI for...", or "/e2e-test <feature>".
argument-hint: <feature-or-collection-name>
allowed-tools: Bash(npx playwright *), Bash(npx nx *), Bash(lsof *), Bash(kill *), Bash(tail *), Bash(sleep *), Bash(cat *), Read, Glob, Grep, Edit, Write
---

# E2E Test Writing Skill

Write Playwright E2E tests for Momentum CMS features. UI tests simulate real user journeys — they **always start from the admin dashboard** and navigate through the actual UI, never jump directly to deep URLs.

## RULE 1: DASHBOARD IS THE STARTING POINT

**Every admin UI test starts at `/admin` (the dashboard) and navigates to the feature via the sidebar or dashboard cards.** This is non-negotiable because:

- It validates that the feature is actually visible and reachable in the admin
- It catches missing sidebar links, broken navigation, missing dashboard cards
- It tests the real user journey, not just isolated pages
- If a feature doesn't appear on the dashboard/sidebar, the test fails — which is the correct outcome

### The Navigation Chain

Every UI test follows this chain:

```
/admin (dashboard) → sidebar click → list view → create/view/edit
```

**NEVER do this:**

```typescript
// BAD: Skipping to a deep URL means you never test if navigation works
await authenticatedPage.goto('/admin/collections/redirects/new');
```

**ALWAYS do this:**

```typescript
// GOOD: Start from dashboard, navigate like a real user
await authenticatedPage.goto('/admin');
await authenticatedPage.waitForLoadState('domcontentloaded');

const sidebar = authenticatedPage.getByLabel('Main navigation');
await sidebar.getByRole('link', { name: 'Redirects' }).click();
await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/redirects$/);

// Now interact with the list page
await authenticatedPage.getByRole('button', { name: /Create Redirect/i }).click();
await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/redirects\/new/);
```

### What each test should prove

| Test                        | Proves                                             |
| --------------------------- | -------------------------------------------------- |
| Dashboard card visible      | Collection is registered, appears in correct group |
| Sidebar link works          | Navigation routing is wired                        |
| List view loads             | Collection data loads, table renders               |
| Create form → submit → view | Full create flow end-to-end                        |
| View page → Edit → Save     | Full edit flow end-to-end                          |

## RULE 2: NEVER WRITE BLIND TESTS

**You MUST see the actual UI before writing any assertions.** Tests written from imagination are fiction.

### Workflow

1. Verify prerequisites (feature wired in, collection in generated config)
2. Run a probe test or start the server and inspect the real page
3. Write tests matching the actual DOM structure
4. Run all tests, confirm 100% pass
5. Only then declare done

### How to inspect the actual UI

Write a probe test that intentionally fails — Playwright's error context includes a YAML snapshot of the page DOM:

```typescript
test('probe: inspect dashboard', async ({ authenticatedPage }) => {
	await authenticatedPage.goto('/admin');
	await authenticatedPage.waitForLoadState('domcontentloaded');
	await expect(authenticatedPage.getByText('XYZZY_WILL_NOT_MATCH')).toBeVisible();
});
```

Run: `npx playwright test --grep "probe:" <spec-file>`

Read the error context file — it shows the exact page structure with element roles, text, and nesting.

## Arguments

- `$ARGUMENTS` - Feature/collection/plugin to test (e.g., "redirects", "analytics dashboard", "seo settings")

## Prerequisites Checklist

Before writing tests, verify:

### 1. Feature is wired into the example app

```bash
grep -n "<feature>" apps/example-angular/src/momentum.config.ts
```

### 2. Collection appears in generated admin config

```bash
grep -n "<slug>" apps/example-angular/src/generated/momentum.config.ts
```

If missing, the plugin needs a static `collections` property:

- **Static** `collections: [MyCollection]` on plugin object = admin UI sees it
- **Runtime** `collections.push(MyCollection)` in `onInit` = server-only, invisible to admin
- Both are needed. After fixing: `npx nx run example-angular:generate`

## Test Structure

```
libs/e2e-tests/src/specs/<feature>.spec.ts
```

### Imports and fixtures

```typescript
import { test, expect, TEST_CREDENTIALS } from '../fixtures';
```

- `authenticatedPage` — Browser page logged in as admin
- `request` — API context (needs manual sign-in via `beforeEach`)
- `baseURL`, `playwright` — For creating fresh request contexts

## Admin UI Test Patterns (Dashboard-First)

### Full Navigation Flow Test

```typescript
test.describe('Feature Admin UI', { tag: ['@feature', '@admin'] }, () => {
	test('should navigate from dashboard to list via sidebar', async ({ authenticatedPage }) => {
		await authenticatedPage.goto('/admin');
		await authenticatedPage.waitForLoadState('domcontentloaded');

		// 1. Verify dashboard card in correct group
		const section = authenticatedPage.getByRole('region', { name: 'GroupName' });
		await expect(section).toBeVisible();
		await expect(section.getByRole('heading', { name: 'FeatureLabel' })).toBeVisible();

		// 2. Navigate via sidebar
		const sidebar = authenticatedPage.getByLabel('Main navigation');
		await sidebar.getByRole('link', { name: 'FeatureLabel' }).click();
		await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>$/);

		// 3. Verify list page loaded
		await expect(authenticatedPage.getByRole('heading', { name: 'PluralLabel' })).toBeVisible();
	});

	test('should create via UI from dashboard', async ({ authenticatedPage }) => {
		await authenticatedPage.goto('/admin');
		await authenticatedPage.waitForLoadState('domcontentloaded');

		// Navigate to list
		const sidebar = authenticatedPage.getByLabel('Main navigation');
		await sidebar.getByRole('link', { name: 'FeatureLabel' }).click();
		await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>$/);

		// Click create
		await authenticatedPage.getByRole('button', { name: /Create SingularLabel/i }).click();
		await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>\/new/);

		// Wait for form
		await expect(
			authenticatedPage.getByRole('button', { name: 'Create', exact: true }),
		).toBeVisible();

		// Fill and submit
		await authenticatedPage.locator('input#field-title').fill('Test Value');
		await authenticatedPage.getByRole('button', { name: 'Create', exact: true }).click();

		// After create: navigates to VIEW page (read-only, NOT edit form)
		await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>\/[^/]+$/);
		await expect(authenticatedPage.getByText('Test Value')).toBeVisible();
	});

	test('should edit via UI from dashboard', async ({ authenticatedPage }) => {
		// Create via API first
		const createRes = await authenticatedPage.request.post('/api/<slug>', {
			data: { title: 'Edit Me' },
		});
		expect(createRes.status()).toBe(201);
		const { doc } = (await createRes.json()) as { doc: { id: string } };

		try {
			await authenticatedPage.goto('/admin');
			await authenticatedPage.waitForLoadState('domcontentloaded');

			// Navigate to list
			const sidebar = authenticatedPage.getByLabel('Main navigation');
			await sidebar.getByRole('link', { name: 'FeatureLabel' }).click();
			await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>$/);

			// Click into the item (list row link)
			// Click table row to navigate to view page
			const row = authenticatedPage.locator('mcms-table-body mcms-table-row', {
				hasText: 'Edit Me',
			});
			await expect(row).toBeVisible({ timeout: 10000 });
			await row.click();

			// View page: has Edit and Delete buttons
			await expect(authenticatedPage.getByRole('button', { name: 'Edit' })).toBeVisible();
			await authenticatedPage.getByRole('button', { name: 'Edit' }).click();

			// Edit form: "Save Changes" button (NOT "Save")
			await expect(authenticatedPage.getByRole('button', { name: 'Save Changes' })).toBeVisible({
				timeout: 15000,
			});

			const input = authenticatedPage.locator('input#field-title');
			await input.clear();
			await input.fill('Updated Value');

			await authenticatedPage.getByRole('button', { name: 'Save Changes' }).click();

			// Returns to list
			await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/<slug>$/);
		} finally {
			await authenticatedPage.request.delete(`/api/<slug>/${doc.id}`);
		}
	});
});
```

### Key UI Facts (verified against real admin)

| Element          | Selector                                                                        |
| ---------------- | ------------------------------------------------------------------------------- |
| Sidebar nav      | `getByLabel('Main navigation')`                                                 |
| Dashboard group  | `getByRole('region', { name: 'GroupName' })`                                    |
| Group headings   | Appear as both group headers AND collection links — use `.first()` if ambiguous |
| Text inputs      | `locator('input#field-{fieldName}')`                                            |
| Select dropdowns | `locator('select#field-{fieldName}')`                                           |
| Breadcrumbs      | `locator('mcms-breadcrumbs')`                                                   |
| Create button    | `getByRole('button', { name: 'Create', exact: true })`                          |
| Save button      | `getByRole('button', { name: 'Save Changes' })` — NOT "Save"                    |
| View page        | Shows read-only text values, "Edit" + "Delete" buttons                          |
| Edit URL         | `/{id}/edit` — NOT `/{id}` (that's the view page)                               |

### Alternative: Dashboard "Create" shortcut

The dashboard cards have "Create" and "View all" links. You can also test via those:

```typescript
const section = authenticatedPage.getByRole('region', { name: 'Settings' });
await section.getByRole('link', { name: 'Create' }).click();
await expect(authenticatedPage).toHaveURL(/\/admin\/collections\/redirects\/new/);
```

## API Test Patterns

API tests complement UI tests. They test CRUD, middleware, access control.

```typescript
test.describe('Feature - API', { tag: ['@feature', '@api'] }, () => {
    test.beforeEach(async ({ request }) => {
        const signIn = await request.post('/api/auth/sign-in/email', {
            headers: { 'Content-Type': 'application/json' },
            data: { email: TEST_CREDENTIALS.email, password: TEST_CREDENTIALS.password },
        });
        expect(signIn.ok(), 'Admin sign-in must succeed').toBe(true);
    });

    test('CRUD', async ({ request }) => {
        const create = await request.post('/api/<slug>', {
            headers: { 'Content-Type': 'application/json' },
            data: { ... },
        });
        expect(create.status()).toBe(201);  // Exact status codes always
    });
});
```

### Middleware/Redirect Testing

```typescript
const noRedirectCtx = await playwright.request.newContext({
	baseURL: baseURL!,
	maxRedirects: 0,
});
try {
	const response = await noRedirectCtx.get('/old-path');
	expect(response.status()).toBe(301);
	expect(response.headers()['location']).toBe('/new-path');
} finally {
	await noRedirectCtx.dispose();
}
```

## Banned Patterns (from CLAUDE.md)

1. **NO `.catch(() => false/null/{})` on Playwright calls**
2. **NO `waitForTimeout(N)`** — use `expect(locator).toBeVisible({ timeout: N })` or `expect.poll()`
3. **NO ambiguous OR-logic** like `.ok() || .status() === 201` — use exact assertions
4. **NO direct URL navigation for UI tests** — always start from `/admin` and click through

## Running Tests

```bash
# Run specific spec
npx playwright test --reporter=list libs/e2e-tests/src/specs/<feature>.spec.ts

# Run by name
npx playwright test --grep "test name" libs/e2e-tests/src/specs/<feature>.spec.ts
```

**ALL tests MUST pass. Do not declare done until you see 0 failures.**

## Reference Specs

- `admin-dashboard.spec.ts` — Dashboard regions, sidebar navigation
- `collection-edit.spec.ts` — Create form, field rendering, Cancel button
- `signal-forms.spec.ts` — Edit flow with "Save Changes"
- `collection-list.spec.ts` — List view patterns
- `redirects.spec.ts` — Full example: dashboard-first UI + API + middleware tests
