---
name: umbraco-mocked-backoffice
description: Run Umbraco backoffice with mocked APIs for visual extension testing
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Umbraco Mocked Backoffice

> **Status:** This skill is currently awaiting an update from Umbraco to allow external extensions to use the mocked backoffice. The patterns documented here work when running from within the Umbraco-CMS source repository.

Run the full Umbraco backoffice UI with all API calls mocked - **no .NET backend required**.

## When to Use

- Visually test extensions during development
- Rapid iteration without backend deployment
- Test extensions in realistic UI environment
- Demonstrate extensions without infrastructure
- CI/CD testing without backend setup

## Related Skills

- **umbraco-example-generator** - Set up extensions for mocked backoffice (start here)
- **umbraco-testing** - Master skill for testing overview
- **umbraco-unit-testing** - Test extension logic in isolation
- **umbraco-e2e-testing** - Test against a real Umbraco instance

---

## Two Mocking Approaches

Extensions with custom APIs can use two mocking approaches:

| Approach | Use Case | Best For |
|----------|----------|----------|
| **[MSW Handlers](patterns/external-msw-handlers.md)** | Network-level API mocking | Testing error handling, loading states, retries |
| **[Mock Repository](patterns/mock-repository-pattern.md)** | Application-level mocking | Testing UI with predictable data (recommended) |

Both approaches require MSW to be enabled (`VITE_UMBRACO_USE_MSW=on`) for core Umbraco APIs.

---

## Setup

### Create Your Extension

Use the **umbraco-example-generator** skill to set up your extension:

**Invoke**: `skill: umbraco-example-generator`

This covers:
- Cloning Umbraco-CMS repository
- Extension structure and `src/index.ts` requirements
- Running with `VITE_EXAMPLE_PATH` and `npm run dev`

### Add Testing Dependencies

```json
{
  "devDependencies": {
    "@playwright/test": "^1.56"
  },
  "scripts": {
    "test:mock-repo": "playwright test --config=tests/mock-repo/playwright.config.ts",
    "test:msw": "playwright test --config=tests/msw/playwright.config.ts"
  }
}
```

```bash
npm install
npx playwright install chromium
```

### Directory Structure

```
my-extension/Client/
├── src/
│   ├── index.ts                # Entry point (loads manifests, registers MSW handlers)
│   ├── manifests.ts            # Production manifests
│   ├── feature/
│   │   ├── my-element.ts
│   │   └── types.ts
│   └── msw/                    # MSW handlers (loaded from index.ts)
│       └── handlers.ts
├── tests/
│   ├── mock-repo/              # Mock repository tests
│   │   ├── playwright.config.ts
│   │   ├── my-extension.spec.ts
│   │   └── mock/
│   │       ├── index.ts        # Mock manifests (replaces repository)
│   │       ├── mock-repository.ts
│   │       └── mock-data.ts
│   └── msw/                    # MSW tests
│       ├── playwright.config.ts
│       └── my-extension.spec.ts
├── package.json
└── tsconfig.json
```

---

## Entry Point (src/index.ts)

The entry point conditionally loads MSW handlers or mock manifests based on environment:

```typescript
// Entry point for external extension loading
// Run from Umbraco.Web.UI.Client with:
//   VITE_EXAMPLE_PATH=/path/to/extension/Client VITE_UMBRACO_USE_MSW=on npm run dev
//   VITE_EXAMPLE_PATH=/path/to/extension/Client VITE_USE_MOCK_REPO=on VITE_UMBRACO_USE_MSW=on npm run dev

// Register MSW handlers when running in MSW mode (but not mock-repo mode)
if (import.meta.env.VITE_UMBRACO_USE_MSW === 'on' && import.meta.env.VITE_USE_MOCK_REPO !== 'on') {
  import('./msw/handlers.js').then(({ createHandlers }) => {
    const { addMockHandlers } = (window as any).MockServiceWorker;
    addMockHandlers(...createHandlers());
  });
}

// Export manifests - use mock repository if VITE_USE_MOCK_REPO is set
export const manifests = import.meta.env.VITE_USE_MOCK_REPO === 'on'
  ? (await import('../tests/mock-repo/mock/index.js')).manifests
  : (await import('./manifests.js')).manifests;
```

---

## Running Tests

### Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `VITE_EXAMPLE_PATH` | `/path/to/extension/Client` | Path to extension directory |
| `VITE_UMBRACO_USE_MSW` | `on` | Enable MSW for core Umbraco APIs |
| `VITE_USE_MOCK_REPO` | `on` | Use mock repository instead of MSW handlers |
| `UMBRACO_CLIENT_PATH` | `/path/to/Umbraco.Web.UI.Client` | Path to Umbraco client (for Playwright) |

### Manual Dev Server

```bash
cd /path/to/Umbraco-CMS/src/Umbraco.Web.UI.Client

# MSW mode (uses your handlers for custom APIs)
VITE_EXAMPLE_PATH=/path/to/extension/Client VITE_UMBRACO_USE_MSW=on npm run dev

# Mock repository mode (uses mock repository for custom APIs)
VITE_EXAMPLE_PATH=/path/to/extension/Client VITE_USE_MOCK_REPO=on VITE_UMBRACO_USE_MSW=on npm run dev
```

### Run Tests

```bash
cd /path/to/extension/Client

# Set path to Umbraco client
export UMBRACO_CLIENT_PATH=/path/to/Umbraco-CMS/src/Umbraco.Web.UI.Client

# Run MSW tests
npm run test:msw

# Run mock repository tests
npm run test:mock-repo
```

---

## Playwright Config Example

Create `tests/msw/playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const EXTENSION_PATH = resolve(__dirname, '../..');
const UMBRACO_CLIENT_PATH = process.env.UMBRACO_CLIENT_PATH;
if (!UMBRACO_CLIENT_PATH) {
  throw new Error('UMBRACO_CLIENT_PATH environment variable is required');
}

const DEV_SERVER_PORT = 5176;

export default defineConfig({
  testDir: '.',
  testMatch: ['*.spec.ts'],
  timeout: 60000,
  expect: { timeout: 15000 },
  fullyParallel: false,
  workers: 1,

  // Start dev server with extension and MSW enabled
  webServer: {
    command: `VITE_EXAMPLE_PATH=${EXTENSION_PATH} VITE_UMBRACO_USE_MSW=on npm run dev -- --port ${DEV_SERVER_PORT}`,
    cwd: UMBRACO_CLIENT_PATH,
    port: DEV_SERVER_PORT,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  use: {
    baseURL: `http://localhost:${DEV_SERVER_PORT}`,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

For mock-repo tests, change the command to include `VITE_USE_MOCK_REPO=on`:

```typescript
command: `VITE_EXAMPLE_PATH=${EXTENSION_PATH} VITE_USE_MOCK_REPO=on VITE_UMBRACO_USE_MSW=on npm run dev -- --port ${DEV_SERVER_PORT}`,
```

---

## Test Patterns

### Navigation Helper

```typescript
import { type Page } from '@playwright/test';

async function navigateToSettings(page: Page) {
  await page.goto('/section/settings');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('umb-section-sidebar', { timeout: 30000 });
}
```

### Testing Tree Items

```typescript
test('should display root tree items', async ({ page }) => {
  await navigateToSettings(page);

  await page.waitForSelector('umb-tree-item', { timeout: 15000 });
  const treeItems = page.locator('umb-tree-item');
  await expect(treeItems.first()).toBeVisible();
});

test('should expand tree item to show children', async ({ page }) => {
  await navigateToSettings(page);

  const expandableItem = page.locator('umb-tree-item').filter({ hasText: 'Group A' });
  const expandButton = expandableItem.locator('button[aria-label="toggle child items"]');
  await expandButton.click();

  const childItem = page.locator('umb-tree-item').filter({ hasText: 'Child 1' });
  await expect(childItem).toBeVisible({ timeout: 15000 });
});
```

### MSW Mock Document URLs

| Document Name | URL Path |
|---------------|----------|
| The Simplest Document | `/section/content/workspace/document/edit/the-simplest-document-id` |
| All properties | `/section/content/workspace/document/edit/all-property-editors-document-id` |

---

## Troubleshooting

### Extension not appearing

- Check that your extension exports a `manifests` array from `src/index.ts`
- Check browser console for errors
- Verify `VITE_EXAMPLE_PATH` points to the `Client` directory

### Tests timeout waiting for elements

- Ensure the dev server is running with your extension loaded
- Check the browser console for extension loading errors
- Use longer timeouts (15000ms+) for initial element appearance

### MSW handlers not intercepting requests

- Check console for `[MSW]` logs showing handler registration
- Verify handler URL patterns match the actual API calls
- Use browser DevTools Network tab to see actual request URLs

---

## Working Example

See **tree-example** in `umbraco-backoffice-skills/examples/tree-example/Client/`:

| Path | Description |
|------|-------------|
| `src/index.ts` | Entry point with conditional manifest loading |
| `src/msw/handlers.ts` | MSW handlers for custom API |
| `tests/mock-repo/` | Mock repository tests |
| `tests/msw/` | MSW tests |

```bash
cd tree-example/Client
export UMBRACO_CLIENT_PATH=/path/to/Umbraco-CMS/src/Umbraco.Web.UI.Client

npm run test:msw        # Run MSW tests
npm run test:mock-repo  # Run mock repository tests
```

---

## What's Mocked?

MSW provides mock data for all backoffice APIs:
- Documents, media, members
- Document types, media types, member types
- Data types, templates, stylesheets
- Users, user groups, permissions
- Languages, cultures, dictionary items
