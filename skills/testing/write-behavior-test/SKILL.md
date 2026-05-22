---
name: write-behavior-test
description: Write Playwright behavior tests (.spec.ts) that verify complete user workflows. Use when creating end-to-end tests for behaviors based on their specifications with Act:/Check: steps. Triggers on "write a behavior test", "create a spec test", or "test this behavior".
---

# Write Behavior Test

## Overview

This skill creates Playwright behavior tests (.spec.ts) that verify complete user workflows. Tests translate behavior specifications (with Act:/Check: steps) into executable Playwright code using PreDB for database state setup.

## Architecture Context

```
Behavior Spec (behavior.md)
  Rules + Examples (Act:/Check: steps)
            |
            v
Spec Test (.spec.ts)
  PreDB -> Playwright Actions -> UI Assertions
```

Behavior tests:
- Run in browser via Playwright
- Verify complete user workflows end-to-end
- Use PreDB to set up database state (PreDB)
- Use Playwright for user interactions (Act: steps)
- Use UI assertions for verifications (Check: steps)
- Verify outcomes through UI, not database queries

## Test Location

```
app/[role]/[page]/behaviors/[behavior-name]/
  tests/
    [behavior-name].spec.ts
```

## Translating Behavior Specs to Tests

### Behavior Spec Format (Input)

```markdown
## Examples

### User creates project successfully

#### PreDB
users:
id, email, role
1, user@example.com, client

projects:
(empty)

#### Steps
* Act: User navigates to the home page
* Act: User fills in project description "Create a CRM"
* Act: User clicks submit button
* Check: "Your Project is Ready" message is visible
* Act: User clicks "Start Building" button
* Check: User is redirected to the project page

#### PostDB
projects:
id, user_id, description
<uuid>, 1, Create a CRM
```

### Spec Test Format (Output)

```typescript
import { expect, test } from '@playwright/test';
import { PreDB } from '@/lib/db-test';
import { db } from '@/db';
import * as schema from '@/db/schema';

test.describe('Create Project Behavior', () => {
  test('User creates project successfully', async ({ page }) => {
    // PreDB
    await PreDB(db, schema, {
      projects: [],
    });

    // Act: User navigates to the home page
    await page.goto('/client/home');

    // Act: User fills in project description
    const textarea = page.locator('textarea[placeholder*="Describe"]');
    await textarea.fill('Create a CRM');

    // Act: User clicks submit button
    await page.locator('button[type="submit"]').click();

    // Check: "Your Project is Ready" message is visible
    await expect(page.getByText('Your Project is Ready')).toBeVisible({
      timeout: 60000,
    });

    // Act: User clicks "Start Building" button
    await page.locator('button:has-text("Start Building")').click();

    // Check: User is redirected to the project page
    await page.waitForURL(/\/client\/project\/.*/, { timeout: 30000 });
  });
});
```

## Step Translation Guide

### Act: Steps -> Playwright Actions

| Act: Step | Playwright Code |
|-----------|-----------------|
| User navigates to [url] | `await page.goto('/path')` |
| User clicks [element] | `await page.locator('selector').click()` |
| User fills [field] with "value" | `await page.locator('selector').fill('value')` |
| User types "text" | `await page.keyboard.type('text')` |
| User presses [key] | `await page.keyboard.press('Enter')` |
| User selects [option] | `await page.selectOption('selector', 'value')` |
| User hovers over [element] | `await page.locator('selector').hover()` |
| User waits for [time] | `await page.waitForTimeout(1000)` |

### Check: Steps -> Playwright Assertions

| Check: Step | Playwright Code |
|-------------|-----------------|
| [text] is visible | `await expect(page.getByText('text')).toBeVisible()` |
| [element] is visible | `await expect(page.locator('selector')).toBeVisible()` |
| [element] is hidden | `await expect(page.locator('selector')).toBeHidden()` |
| [element] contains "text" | `await expect(page.locator('selector')).toContainText('text')` |
| User is redirected to [url] | `await page.waitForURL(/pattern/, { timeout: 30000 })` |
| Error "message" is shown | `await expect(page.getByText('message')).toBeVisible()` |
| [count] items in list | `await expect(page.locator('selector')).toHaveCount(count)` |

## Implementation Pattern

```typescript
import { expect, test } from '@playwright/test';
import { PreDB } from '@/lib/db-test';
import { db } from '@/db';
import * as schema from '@/db/schema';
import { getTestUser } from '@/shared/tests/helpers';

test.describe('[Behavior Name] Behavior', () => {
  test.afterEach(async () => {
    // Cleanup if needed
  });

  test('[Example name from spec]', async ({ page }) => {
    // Get test user if needed
    const testUser = await getTestUser();

    // PreDB - translate CSV tables to PreDB
    await PreDB(db, schema, {
      projects: [
        {
          id: 'test-project-id',
          name: 'Test Project',
          userId: testUser.id,
          // ... other fields from spec
        },
      ],
      // ... other tables
    });

    // Steps - translate Act:/Check: to Playwright

    // Act: User navigates to the page
    await page.goto('/client/path');

    // Check: Page content is visible
    await expect(page.getByText('Expected Text')).toBeVisible();

    // Act: User performs action
    await page.locator('[data-testid="button"]').click();

    // Check: Result is visible (verify outcome through UI)
    await expect(page.getByText('Success')).toBeVisible();
  });
});
```

## PreDB Usage

### Set Up Initial State (PreDB)

```typescript
await PreDB(db, schema, {
  // Table name (use schema table names)
  projects: [
    {
      id: 'project-1',
      name: 'Test Project',
      userId: testUser.id,
      status: 'active',
      createdAt: new Date(),
      updatedAt: new Date(),
    },
  ],
  // Empty table
  issues: [],
});
```

### Common Precondition Patterns

```typescript
// Empty state
await PreDB(db, schema, {
  projects: [],
});

// Single record
await PreDB(db, schema, {
  projects: [
    { id: 'proj-1', name: 'Test', userId: testUser.id, status: 'active' },
  ],
});

// Multiple records
await PreDB(db, schema, {
  projects: [
    { id: 'proj-1', name: 'Project A', userId: testUser.id },
    { id: 'proj-2', name: 'Project B', userId: testUser.id },
  ],
});

// Related records
await PreDB(db, schema, {
  projects: [
    { id: 'proj-1', name: 'Test Project', userId: testUser.id },
  ],
  issues: [
    { id: 'issue-1', projectId: 'proj-1', title: 'Test Issue' },
  ],
});
```

## Verifying PostDB Through UI

Instead of using PostDB, verify outcomes through the UI:

```typescript
// Check: Item was created
await expect(page.getByText('New Project')).toBeVisible();

// Check: Item was deleted
await expect(page.getByText('Old Project')).toBeHidden();

// Check: List has correct count
await expect(page.locator('[data-testid="project-card"]')).toHaveCount(3);

// Check: Success message shown
await expect(page.getByText('Project created successfully')).toBeVisible();

// Check: Error message shown
await expect(page.getByText('Name is required')).toBeVisible();

// Check: Redirected to correct page
await page.waitForURL(/\/client\/project\/.*/, { timeout: 30000 });
```

## Locator Strategies

Prefer in this order:

1. **data-testid** (most reliable):
   ```typescript
   page.locator('[data-testid="submit-button"]')
   ```

2. **Role-based** (semantic):
   ```typescript
   page.getByRole('button', { name: 'Submit' })
   ```

3. **Text-based** (readable):
   ```typescript
   page.getByText('Submit')
   page.locator('button:has-text("Submit")')
   ```

4. **CSS selectors** (last resort):
   ```typescript
   page.locator('button[type="submit"]')
   ```

## Timeouts

Set appropriate timeouts for async operations:

```typescript
// For AI-generated content or slow operations
test.setTimeout(180000); // 3 minutes

// For visibility checks
await expect(element).toBeVisible({ timeout: 30000 });

// For navigation
await page.waitForURL(/pattern/, { timeout: 30000 });

// For explicit waits (use sparingly)
await page.waitForTimeout(2000);
```

## Constraints

- **NO MOCKING**: Never use `vi.mock()` in Playwright tests
- **NO PostDB**: Verify outcomes through UI assertions, not database queries
- Use PreDB for database setup only
- Use real navigation, not mocked auth
- Clean up test data in `afterEach`
- Use test database (NODE_ENV=test)
- Write ONE test case per example from spec
- Focus on happy path first

## Checklist

Before finalizing a behavior test:
- [ ] Test file in correct location: `behaviors/[name]/tests/[name].spec.ts`
- [ ] PreDB translated to PreDB call
- [ ] All Act: steps translated to Playwright actions
- [ ] All Check: steps translated to UI assertions
- [ ] PostDB verified through UI (not PostDB)
- [ ] Appropriate timeouts set
- [ ] Cleanup in afterEach if needed
- [ ] Uses data-testid or semantic locators

## Example: Full Translation

### Input: Behavior Spec

```markdown
### User deletes project successfully

#### PreDB
projects:
id, name, user_id, status
proj-1, Test Project, user-1, active

#### Steps
* Act: User navigates to home page
* Act: User clicks project menu dropdown
* Act: User clicks "Delete Project"
* Check: Project card is removed from UI
* Check: Success toast is shown

#### PostDB
projects:
(empty)
```

### Output: Spec Test

```typescript
test('User deletes project successfully', async ({ page }) => {
  const testUser = await getTestUser();

  // PreDB
  await PreDB(db, schema, {
    projects: [
      {
        id: 'proj-1',
        name: 'Test Project',
        userId: testUser.id,
        status: 'active',
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  });

  // Act: User navigates to home page
  await page.goto('/client/home');

  // Act: User clicks project menu dropdown
  const projectCard = page.locator('[data-testid="project-card"]').filter({
    hasText: 'Test Project',
  });
  await projectCard.locator('[data-testid="menu-trigger"]').click();

  // Act: User clicks "Delete Project"
  await page.locator('[role="menuitem"]:has-text("Delete Project")').click();

  // Check: Project card is removed from UI
  await expect(projectCard).toBeHidden({ timeout: 10000 });

  // Check: Success toast is shown
  await expect(page.getByText('Project deleted')).toBeVisible();
});
```
