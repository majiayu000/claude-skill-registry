---
name: umbraco-e2e-testing
description: E2E testing for Umbraco backoffice extensions using Playwright and @umbraco/playwright-testhelpers
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco E2E Testing

End-to-end testing for Umbraco backoffice extensions using Playwright and `@umbraco/playwright-testhelpers`. This approach tests against a real running Umbraco instance, validating complete user workflows.

## Critical: Use Testhelpers for Core Umbraco

Use `@umbraco/playwright-testhelpers` for **core Umbraco operations**:

| Package | Purpose | Why Required |
|---------|---------|--------------|
| `@umbraco/playwright-testhelpers` | UI and API helpers | Handles auth, navigation, core entity CRUD |
| `@umbraco/json-models-builders` | Test data builders | Creates valid Umbraco entities with correct structure |

**Why use testhelpers for core Umbraco?**
- Umbraco uses `data-mark` instead of `data-testid` - testhelpers handle this
- Auth token management is complex - testhelpers manage `STORAGE_STAGE_PATH`
- API setup/teardown requires specific payload formats - builders ensure correctness
- Selectors change between versions - testhelpers abstract these away

```typescript
// WRONG - Raw Playwright for core Umbraco (brittle)
await page.goto('/umbraco');
await page.fill('[name="email"]', 'admin@example.com');

// CORRECT - Testhelpers for core Umbraco
import { test } from '@umbraco/playwright-testhelpers';

test('my test', async ({ umbracoApi, umbracoUi }) => {
  await umbracoUi.goToBackOffice();
  await umbracoUi.login.enterEmail('admin@example.com');
});
```

### When to Use Raw Playwright

For **custom extensions**, use `umbracoUi.page` (raw Playwright) because testhelpers don't know about your custom elements:

```typescript
test('my custom extension', async ({ umbracoUi }) => {
  // Testhelpers for core navigation
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.settings);

  // Raw Playwright for YOUR custom elements
  await umbracoUi.page.getByRole('link', { name: 'My Custom Item' }).click();
  await expect(umbracoUi.page.locator('my-custom-workspace')).toBeVisible();
});
```

| Use Testhelpers For | Use `umbracoUi.page` For |
|---------------------|--------------------------|
| Login/logout | Custom tree items |
| Navigate to ANY section (including custom) | Custom workspace elements |
| Create/edit documents via API | Custom entity actions |
| Built-in UI interactions | Custom UI components |

## When to Use

- Testing complete user workflows
- Testing data persistence
- Testing authentication/authorization
- Acceptance testing before release
- Integration testing with real API responses

## Related Skills

- **umbraco-testing** - Master skill for testing overview
- **umbraco-playwright-testhelpers** - Full reference for the testhelpers package
- **umbraco-test-builders** - JsonModels.Builders for test data
- **umbraco-mocked-backoffice** - Test without real backend (faster)

## Documentation

- **Playwright**: https://playwright.dev/docs/intro
- **Reference tests**: `Umbraco-CMS/tests/Umbraco.Tests.AcceptanceTest`

---

## Setup

### Dependencies

Add to `package.json`:

```json
{
  "devDependencies": {
    "@playwright/test": "^1.56",
    "@umbraco/playwright-testhelpers": "^17.0.15",
    "@umbraco/json-models-builders": "^2.0.42",
    "dotenv": "^16.3.1"
  },
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

Then run:
```bash
npm install
npx playwright install chromium
```

**Version Compatibility**: Match testhelpers to your Umbraco version:
| Umbraco | Testhelpers |
|---------|-------------|
| 17.1.x (pre-release) | `17.1.0-beta.x` |
| 17.0.x | `^17.0.15` |
| 14.x | `^14.x` |

### Configuration

Create `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const STORAGE_STATE = join(__dirname, 'tests/e2e/.auth/user.json');

// CRITICAL: Testhelpers read auth tokens from this file
process.env.STORAGE_STAGE_PATH = STORAGE_STATE;

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  expect: { timeout: 5000 },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI ? 'line' : 'html',
  use: {
    baseURL: process.env.UMBRACO_URL || 'https://localhost:44325',
    trace: 'retain-on-failure',
    ignoreHTTPSErrors: true,
    // CRITICAL: Umbraco uses 'data-mark' not 'data-testid'
    testIdAttribute: 'data-mark',
  },
  projects: [
    {
      name: 'setup',
      testMatch: '**/*.setup.ts',
    },
    {
      name: 'e2e',
      testMatch: '**/*.spec.ts',
      dependencies: ['setup'],
      use: {
        ...devices['Desktop Chrome'],
        ignoreHTTPSErrors: true,
        storageState: STORAGE_STATE,
      },
    },
  ],
});
```

### Critical Settings

| Setting | Value | Why Required |
|---------|-------|--------------|
| `testIdAttribute` | `'data-mark'` | Umbraco uses `data-mark`, not `data-testid` |
| `STORAGE_STAGE_PATH` | Path to user.json | Testhelpers read auth tokens from this file |
| `ignoreHTTPSErrors` | `true` | For local dev with self-signed certs |

**Without `testIdAttribute: 'data-mark'`, all `getByTestId()` calls will fail.**

### Authentication Setup

Create `tests/e2e/auth.setup.ts`:

```typescript
import { test as setup } from '@playwright/test';
import { STORAGE_STATE } from '../../playwright.config';
import { ConstantHelper, UiHelpers } from '@umbraco/playwright-testhelpers';

setup('authenticate', async ({ page }) => {
  const umbracoUi = new UiHelpers(page);

  await umbracoUi.goToBackOffice();
  await umbracoUi.login.enterEmail(process.env.UMBRACO_USER_LOGIN!);
  await umbracoUi.login.enterPassword(process.env.UMBRACO_USER_PASSWORD!);
  await umbracoUi.login.clickLoginButton();
  await umbracoUi.login.goToSection(ConstantHelper.sections.settings);
  await page.context().storageState({ path: STORAGE_STATE });
});
```

### Environment Variables

Create `.env` (add to `.gitignore`):

```bash
UMBRACO_URL=https://localhost:44325
UMBRACO_USER_LOGIN=admin@example.com
UMBRACO_USER_PASSWORD=yourpassword
UMBRACO_DATA_PATH=/path/to/Umbraco.Web.UI/App_Data  # Optional: for data reset
```

| Variable | Required | Purpose |
|----------|----------|---------|
| `UMBRACO_URL` | Yes | Backoffice URL |
| `UMBRACO_USER_LOGIN` | Yes | Admin email |
| `UMBRACO_USER_PASSWORD` | Yes | Admin password |
| `UMBRACO_DATA_PATH` | No | App_Data path for test data reset (see "Testing with Persistent Data") |

### Directory Structure

```
my-extension/
├── src/
│   └── ...
├── tests/
│   └── e2e/
│       ├── .auth/
│       │   └── user.json       # Auth state (gitignored)
│       ├── auth.setup.ts       # Authentication
│       └── my-extension.spec.ts
├── playwright.config.ts
├── .env                        # Gitignored
├── .env.example
└── package.json
```

---

## Patterns

### Test Fixtures

```typescript
import { test } from '@umbraco/playwright-testhelpers';

test('my test', async ({ umbracoApi, umbracoUi }) => {
  // umbracoApi - API helpers for setup/teardown
  // umbracoUi - UI helpers for backoffice interaction
});
```

### AAA Pattern (Arrange-Act-Assert)

```typescript
test('can create content', async ({ umbracoApi, umbracoUi }) => {
  // Arrange - Setup via API
  await umbracoApi.documentType.createDefaultDocumentType('TestDocType');

  // Act - Perform user actions via UI
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.content);
  await umbracoUi.content.clickActionsMenuAtRoot();

  // Assert - Verify results
  expect(await umbracoApi.document.doesNameExist('TestContent')).toBeTruthy();
});
```

### Idempotent Cleanup

```typescript
test.afterEach(async ({ umbracoApi }) => {
  await umbracoApi.document.ensureNameNotExists(contentName);
  await umbracoApi.documentType.ensureNameNotExists(documentTypeName);
});
```

### API Helpers (umbracoApi)

**Document Types:**
```typescript
await umbracoApi.documentType.createDefaultDocumentType('TestDocType');
await umbracoApi.documentType.createDocumentTypeWithPropertyEditor(
  'TestDocType', 'Textstring', dataTypeData.id
);
await umbracoApi.documentType.ensureNameNotExists('TestDocType');
```

**Documents:**
```typescript
await umbracoApi.document.createDefaultDocument('TestContent', docTypeId);
await umbracoApi.document.createDocumentWithTextContent(
  'TestContent', docTypeId, 'value', 'Textstring'
);
await umbracoApi.document.publish(contentId);
await umbracoApi.document.ensureNameNotExists('TestContent');
```

**Data Types:**
```typescript
const dataType = await umbracoApi.dataType.getByName('Textstring');
await umbracoApi.dataType.create('MyType', 'Umbraco.TextBox', 'Umb.PropertyEditorUi.TextBox', []);
```

### Using Builders for Complex Data

For complex test data, use `@umbraco/json-models-builders`:

```typescript
import { DocumentTypeBuilder, DocumentBuilder } from '@umbraco/json-models-builders';

test('create complex document type', async ({ umbracoApi }) => {
  // Build a document type with multiple properties
  const docType = new DocumentTypeBuilder()
    .withName('Article')
    .withAlias('article')
    .addGroup()
      .withName('Content')
      .addTextBoxProperty()
        .withAlias('title')
        .withLabel('Title')
        .done()
      .addRichTextProperty()
        .withAlias('body')
        .withLabel('Body')
        .done()
      .done()
    .build();

  await umbracoApi.documentType.create(docType);
});
```

**Why use builders?**
- Fluent API makes complex structures readable
- Ensures valid payload structure for Umbraco API
- Handles required fields and defaults
- Type-safe in TypeScript

### UI Helpers (umbracoUi)

**Navigation:**
```typescript
await umbracoUi.goToBackOffice();
await umbracoUi.content.goToSection(ConstantHelper.sections.content);
await umbracoUi.content.goToContentWithName('My Page');
```

### Testing Custom Trees in Sidebar

When testing custom tree extensions (e.g., in Settings), use this pattern to handle async loading and scrolling:

```typescript
test('should click custom tree item', async ({ umbracoUi }) => {
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.settings);

  // 1. Wait for your tree heading (custom trees often at bottom of sidebar)
  await umbracoUi.page.getByRole('heading', { name: 'My Tree' }).waitFor({ timeout: 15000 });

  // 2. Scroll into view (important - sidebar may be long)
  await umbracoUi.page.getByRole('heading', { name: 'My Tree' }).scrollIntoViewIfNeeded();

  // 3. Wait for tree items to load (async from API)
  const item1Link = umbracoUi.page.getByRole('link', { name: 'Item 1' });
  await item1Link.waitFor({ timeout: 15000 });

  // 4. Click the item
  await item1Link.click();

  // Assert workspace loads
  await expect(umbracoUi.page.locator('my-tree-workspace-editor')).toBeVisible({ timeout: 15000 });
});
```

**Why this pattern?**
- Custom trees are often at the bottom of the Settings sidebar
- Tree items load asynchronously from your API
- Using `getByRole('link', { name: '...' })` is more reliable than generic `umb-tree-item` selectors
- Built-in trees (Document Types, etc.) also use `umb-tree-item`, causing selector conflicts

**Content Actions:**
```typescript
await umbracoUi.content.clickActionsMenuAtRoot();
await umbracoUi.content.clickCreateActionMenuOption();
await umbracoUi.content.chooseDocumentType('TestDocType');
await umbracoUi.content.enterContentName('My Page');
await umbracoUi.content.enterTextstring('My text value');
await umbracoUi.content.clickSaveButton();
```

**Constants:**
```typescript
import { ConstantHelper } from '@umbraco/playwright-testhelpers';

ConstantHelper.sections.content
ConstantHelper.sections.settings
ConstantHelper.buttons.save
ConstantHelper.buttons.saveAndPublish
```

---

## Examples

### Complete Test

```typescript
import { expect } from '@playwright/test';
import { ConstantHelper, NotificationConstantHelper, test } from '@umbraco/playwright-testhelpers';

const contentName = 'TestContent';
const documentTypeName = 'TestDocType';
const dataTypeName = 'Textstring';
const contentText = 'Test content text';

test.afterEach(async ({ umbracoApi }) => {
  await umbracoApi.document.ensureNameNotExists(contentName);
  await umbracoApi.documentType.ensureNameNotExists(documentTypeName);
});

test('can create content', { tag: '@smoke' }, async ({ umbracoApi, umbracoUi }) => {
  // Arrange
  const dataTypeData = await umbracoApi.dataType.getByName(dataTypeName);
  await umbracoApi.documentType.createDocumentTypeWithPropertyEditor(
    documentTypeName, dataTypeName, dataTypeData.id
  );

  // Act
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.content);
  await umbracoUi.content.clickActionsMenuAtRoot();
  await umbracoUi.content.clickCreateActionMenuOption();
  await umbracoUi.content.chooseDocumentType(documentTypeName);
  await umbracoUi.content.enterContentName(contentName);
  await umbracoUi.content.enterTextstring(contentText);
  await umbracoUi.content.clickSaveButton();

  // Assert
  await umbracoUi.content.waitForContentToBeCreated();
  expect(await umbracoApi.document.doesNameExist(contentName)).toBeTruthy();
  const contentData = await umbracoApi.document.getByName(contentName);
  expect(contentData.values[0].value).toBe(contentText);
});

test('can publish content', async ({ umbracoApi, umbracoUi }) => {
  // Arrange
  const dataTypeData = await umbracoApi.dataType.getByName(dataTypeName);
  const docTypeId = await umbracoApi.documentType.createDocumentTypeWithPropertyEditor(
    documentTypeName, dataTypeName, dataTypeData.id
  );
  await umbracoApi.document.createDocumentWithTextContent(
    contentName, docTypeId, contentText, dataTypeName
  );

  // Act
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.content);
  await umbracoUi.content.clickActionsMenuForContent(contentName);
  await umbracoUi.content.clickPublishActionMenuOption();
  await umbracoUi.content.clickConfirmToPublishButton();

  // Assert
  await umbracoUi.content.doesSuccessNotificationHaveText(
    NotificationConstantHelper.success.published
  );
  const contentData = await umbracoApi.document.getByName(contentName);
  expect(contentData.variants[0].state).toBe('Published');
});
```

### Working Example: tree-example

The `tree-example` demonstrates E2E testing for a custom tree extension:

**Location**: `umbraco-backoffice/examples/tree-example/Client/`

```bash
# Run E2E tests (requires running Umbraco)
URL=https://localhost:44325 \
UMBRACO_USER_LOGIN=admin@example.com \
UMBRACO_USER_PASSWORD=yourpassword \
npm run test:e2e                # 7 tests
```

Key files:
- `tests/playwright.e2e.config.ts` - E2E configuration with auth setup
- `tests/auth.setup.ts` - Authentication using testhelpers
- `tests/tree-e2e.spec.ts` - Tests for custom tree in Settings sidebar

### Working Example: notes-wiki (Full-Stack with Data Reset)

The `notes-wiki` demonstrates E2E testing with **persistent data** and **CRUD operations**:

**Location**: `umbraco-backoffice/examples/notes-wiki/Client/`

```bash
# Run E2E tests (with data reset)
URL=https://localhost:44325 \
UMBRACO_USER_LOGIN=admin@example.com \
UMBRACO_USER_PASSWORD=yourpassword \
UMBRACO_DATA_PATH=/path/to/App_Data \
npm run test:e2e                # 16 tests
```

Key files:
- `tests/playwright.e2e.config.ts` - Config with `globalSetup` for data reset
- `tests/global-setup.ts` - Resets data to seed state before tests
- `tests/test-seed-data.json` - Known test data (notes, folders)
- `tests/notes-wiki-e2e.spec.ts` - CRUD and navigation tests

**What it demonstrates:**
- Testing a custom section using `goToSection('notes')`
- Resetting file-based data before each test run
- Testing tree navigation, folders, and workspaces
- Entity actions via "View actions" button (more reliable than right-click)
- Dashboard and workspace view testing

---

## Testing Extensions with Persistent Data

When your extension persists data (JSON files, database, etc.), tests need **predictable starting state**.

### Global Setup Pattern

Add `globalSetup` to reset data before tests:

**playwright.e2e.config.ts:**
```typescript
export default defineConfig({
  // ... other config
  globalSetup: './global-setup.ts',
});
```

**global-setup.ts:**
```typescript
import { FullConfig } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

async function globalSetup(config: FullConfig) {
  const dataPath = process.env.UMBRACO_DATA_PATH;
  if (!dataPath) {
    console.warn('⚠️  UMBRACO_DATA_PATH not set. Skipping data reset.');
    return;
  }

  const targetFile = path.join(dataPath, 'MyExtension/data.json');
  const seedFile = path.join(__dirname, 'test-seed-data.json');

  // Ensure directory exists
  fs.mkdirSync(path.dirname(targetFile), { recursive: true });

  // Copy seed data to target
  fs.copyFileSync(seedFile, targetFile);
  console.log('🌱 Reset data to seed state');
}

export default globalSetup;
```

**test-seed-data.json:**
```json
{
  "items": [
    { "id": "test-1", "name": "Test Item 1" },
    { "id": "test-2", "name": "Test Item 2" }
  ]
}
```

### Environment Variable

Add `UMBRACO_DATA_PATH` to locate your Umbraco's App_Data folder:

```bash
UMBRACO_DATA_PATH=/path/to/Umbraco.Web.UI/App_Data npm run test:e2e
```

---

## Testing Custom Sections

Custom sections work with testhelpers' `goToSection()` method - pass the section pathname:

```typescript
// Section pathname - matches what you defined in section/constants.ts
const MY_SECTION = 'my-section';

// Helper to navigate to custom section using testhelpers
async function goToMySection(umbracoUi: any) {
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(MY_SECTION);
  await umbracoUi.page.waitForTimeout(500);
}

test('should navigate to custom section', async ({ umbracoUi }) => {
  await goToMySection(umbracoUi);

  // Assert - your dashboard or tree should be visible
  await expect(umbracoUi.page.getByText('Welcome')).toBeVisible({ timeout: 15000 });
});

// To verify the section exists in the section bar:
test('should display my section', async ({ umbracoUi }) => {
  await umbracoUi.goToBackOffice();
  await expect(umbracoUi.page.getByRole('tab', { name: 'My Section' })).toBeVisible({ timeout: 15000 });
});
```

---

## Context Menu (Entity Actions) Testing

Testing entity actions on tree items. Uses `umbracoUi.page` since testhelpers don't cover custom entity actions.

**Important:** Entity actions in Umbraco are rendered as **buttons** inside the dropdown menu, not as `menuitem` roles directly. The most reliable approach is to use the "View actions" button rather than right-click:

```typescript
test('should show delete action via actions button', async ({ umbracoUi }) => {
  await goToMySection(umbracoUi);

  // Wait for tree item
  const itemLink = umbracoUi.page.getByRole('link', { name: 'My Item' });
  await itemLink.waitFor({ timeout: 15000 });

  // Hover to reveal action buttons
  await itemLink.hover();

  // Click the "View actions" button to open dropdown
  const actionsButton = umbracoUi.page.getByRole('button', { name: "View actions for 'My Item'" });
  await actionsButton.click();

  // Wait for dropdown and check for actions (actions are BUTTONS, not menuitems!)
  await umbracoUi.page.waitForTimeout(500);
  const deleteButton = umbracoUi.page.getByRole('button', { name: 'Delete' });
  const renameButton = umbracoUi.page.getByRole('button', { name: 'Rename' });

  // Assert - at least one action should be visible
  await expect(deleteButton.or(renameButton)).toBeVisible({ timeout: 5000 });
});

test('should delete item via actions menu', async ({ umbracoUi }) => {
  await goToMySection(umbracoUi);

  const itemLink = umbracoUi.page.getByRole('link', { name: 'Item to Delete' });
  await itemLink.waitFor({ timeout: 15000 });

  // Hover and open actions menu
  await itemLink.hover();
  await umbracoUi.page.getByRole('button', { name: "View actions for 'Item to Delete'" }).click();

  // Click delete button
  await umbracoUi.page.getByRole('button', { name: 'Delete' }).click();

  // Confirm deletion (if modal appears)
  const confirmButton = umbracoUi.page.getByRole('button', { name: /Confirm|Delete/i });
  if (await confirmButton.isVisible({ timeout: 2000 }).catch(() => false)) {
    await confirmButton.click();
  }

  // Assert - item should be gone
  await expect(itemLink).not.toBeVisible({ timeout: 15000 });
});
```

### Alternative: Right-Click Context Menu

Right-click also works but the actions button approach is more reliable:

```typescript
// Right-click approach (less reliable than actions button)
await itemLink.click({ button: 'right' });
await umbracoUi.page.waitForTimeout(500);
await umbracoUi.page.getByRole('button', { name: 'Delete' }).click();
```

---

## CRUD Testing Patterns

For custom extensions, use `umbracoUi.page` for UI interactions. For core Umbraco content, prefer `umbracoApi` helpers for setup/teardown.

### Create via Actions Menu (Custom Extension)

```typescript
test('should create new item', async ({ umbracoUi }) => {
  await goToMySection(umbracoUi);

  // Hover over parent folder and use Create button
  const folderLink = umbracoUi.page.getByRole('link', { name: 'Parent Folder' });
  await folderLink.hover();

  // Scope to specific menu to avoid ambiguity with multiple items
  const folderMenu = umbracoUi.page.getByRole('menu').filter({ hasText: 'Parent Folder' });
  const createButton = folderMenu.getByRole('button', { name: 'Create Note' });
  await createButton.click();

  // Assert - workspace should open with "New" indicator
  await expect(umbracoUi.page.locator('my-workspace-editor')).toBeVisible({ timeout: 15000 });
});
```

### Scoping to Specific Tree Items

When multiple tree items exist with similar elements, scope selectors to avoid ambiguity:

```typescript
// WRONG - ambiguous when multiple folders have "Create" buttons
const createButton = page.getByRole('button', { name: 'Create' });

// CORRECT - scoped to specific folder's menu
const folderMenu = page.getByRole('menu').filter({ hasText: 'My Folder' });
const createButton = folderMenu.getByRole('button', { name: 'Create' });
```

### Update and Save

```typescript
test('should update item', async ({ umbracoUi }) => {
  await goToMySection(umbracoUi);

  // Navigate to item
  await umbracoUi.page.getByRole('link', { name: 'Test Item' }).click();
  await umbracoUi.page.locator('my-workspace-editor').waitFor({ timeout: 15000 });

  // Update field
  const titleInput = umbracoUi.page.locator('uui-input#title');
  await titleInput.clear();
  await titleInput.fill('Updated Title');

  // Save
  await umbracoUi.page.getByRole('button', { name: /Save/i }).click();

  // Wait for save to complete
  await umbracoUi.page.waitForTimeout(2000);

  // Assert - header should reflect change
  await expect(umbracoUi.page.getByText('Updated Title')).toBeVisible();
});
```

---

## Running Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run with UI mode (visual debugging)
npm run test:e2e:ui

# Run specific test file
npx playwright test tests/e2e/my-extension.spec.ts

# Run with specific tag
npx playwright test --grep "@smoke"

# Run in debug mode
npx playwright test --debug
```

---

## Troubleshooting

### getByTestId() not finding elements

Ensure `testIdAttribute: 'data-mark'` is set in playwright.config.ts.

### Authentication fails

- Check `.env` credentials are correct
- Ensure Umbraco instance is running
- Verify `STORAGE_STAGE_PATH` is set

### Tests timeout

- Increase timeouts in config
- Ensure Umbraco is responsive
- Check for JS errors in browser console

### Tests fail in CI

- Ensure Umbraco instance is accessible
- Set environment variables in CI
- Use `npx playwright install chromium`

---

## Alternative: MSW Mode (No Backend Required)

For faster testing without a real Umbraco backend, use the **mocked backoffice** approach.

**Invoke**: `skill: umbraco-mocked-backoffice`

| Aspect | Real Backend (this skill) | MSW Mode |
|--------|---------------------------|----------|
| Setup | Running Umbraco instance | Clone Umbraco-CMS, npm install |
| Auth | Required | Not required |
| Speed | Slower | Faster |
| Use case | Integration/acceptance | UI/component testing |
