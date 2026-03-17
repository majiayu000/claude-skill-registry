---
name: arcanea-playwright-testing
description: Playwright E2E testing for the Arcanea web app. Use when writing, running, or debugging Playwright tests, automating browser interactions on the Arcanea platform, capturing screenshots for QA, testing UI flows (academy gate quizzes, lore pages, prompt books, auth), or setting up the test infrastructure. Triggers on: Playwright, E2E test, end-to-end, browser test, UI test, automation, screenshot, test the page. Sourced from Anthropic's official webapp-testing skill and adapted for Arcanea's Next.js 16 stack.
license: MIT (source: anthropics/skills/webapp-testing)
metadata:
  author: Arcanea (adapted from Anthropic)
  version: "1.0.0"
  stack: Playwright, Next.js 16 App Router, TypeScript strict
---

# Arcanea Playwright Testing

> *"Alera guards the Voice Gate at 528 Hz — Truth, expression. Tests are truth-tellers. They reveal what is real, not what we hope."*

## Quick Start

### Decision Tree

```
Test need → Is it a pure unit (function/hook)?
    ├─ Yes → Jest in packages/
    └─ No → Playwright E2E

Playwright task → Is the dev server running?
    ├─ No  → Use with_server.py helper OR next dev directly
    └─ Yes → Reconnaissance-then-action pattern
```

### Run Arcanea Dev Server for Tests
```bash
# From monorepo root
pnpm --filter web dev # starts on :3000

# Or in test scripts — use playwright's webServer config
```

---

## Setup

### playwright.config.ts (apps/web)
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { outputFolder: 'playwright-report' }]],
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  // Auto-start dev server for local testing
  webServer: {
    command: 'pnpm --filter web dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
  ],
})
```

---

## Reconnaissance-Then-Action Pattern

Always inspect before acting on dynamic Next.js pages:

```typescript
import { test, expect } from '@playwright/test'

test('lore page loads', async ({ page }) => {
  // 1. Navigate and wait
  await page.goto('/lore')
  await page.waitForLoadState('networkidle') // CRITICAL for Next.js hydration

  // 2. Reconnaissance — take screenshot to understand DOM state
  await page.screenshot({ path: 'tests/screenshots/lore-debug.png', fullPage: true })

  // 3. Identify selectors from rendered state
  const guardianCards = page.locator('[data-testid="guardian-card"]')
  const count = await guardianCards.count()
  console.log(`Found ${count} guardian cards`)

  // 4. Assert
  expect(count).toBeGreaterThanOrEqual(1)
})
```

---

## Arcanea Test Patterns

### Academy Gate Quiz Flow
```typescript
test('gate quiz — foundation gate completion', async ({ page }) => {
  // Auth: sign in as test user
  await page.goto('/auth/sign-in')
  await page.waitForLoadState('networkidle')
  await page.fill('[data-testid="email-input"]', process.env.TEST_USER_EMAIL!)
  await page.fill('[data-testid="password-input"]', process.env.TEST_USER_PASSWORD!)
  await page.click('[data-testid="sign-in-btn"]')
  await page.waitForURL('/academy')

  // Navigate to Foundation Gate quiz
  await page.goto('/academy/gate-quiz?gate=foundation')
  await page.waitForLoadState('networkidle')

  // Answer questions (10 questions for Foundation gate)
  for (let i = 0; i < 10; i++) {
    const question = page.locator('[data-testid="quiz-question"]')
    await expect(question).toBeVisible()
    
    // Select first answer (test data has correct first answers)
    await page.locator('[data-testid="answer-option"]').first().click()
    await page.locator('[data-testid="next-question-btn"]').click()
  }

  // Verify completion screen
  await expect(page.locator('[data-testid="gate-complete"]')).toBeVisible()
  await expect(page.locator('[data-testid="guardian-name"]')).toContainText('Lyssandria')
})
```

### Lore Navigation Test
```typescript
test('lore explore — elements navigation', async ({ page }) => {
  await page.goto('/lore')
  await page.waitForLoadState('networkidle')

  // Test all five elements navigation
  const elements = ['fire', 'water', 'earth', 'wind', 'void']
  
  for (const element of elements) {
    await page.goto(`/lore/elements/${element}`)
    await page.waitForLoadState('networkidle')
    
    // Verify element page loads with correct title
    const title = page.locator('h1, [data-testid="element-title"]')
    await expect(title).toBeVisible()
    await expect(title).toContainText(element, { ignoreCase: true })
  }
})
```

### Prompt Books CRUD Flow
```typescript
test('prompt books — create and view prompt', async ({ page }) => {
  await authenticateTestUser(page)
  
  await page.goto('/prompt-books')
  await page.waitForLoadState('networkidle')

  // Create new prompt
  await page.click('[data-testid="new-prompt-btn"]')
  await page.waitForLoadState('networkidle')

  // Fill editor
  await page.fill('[data-testid="prompt-title"]', 'Test Guardian Invocation')
  await page.locator('[data-testid="prompt-editor"]').click()
  await page.keyboard.type('Channel the essence of {element} through {gate}')
  
  await page.click('[data-testid="save-prompt-btn"]')
  
  // Verify saved
  await expect(page.locator('[data-testid="save-success"]')).toBeVisible()
  
  // Navigate back and verify prompt appears
  await page.goto('/prompt-books')
  await expect(page.locator('text=Test Guardian Invocation')).toBeVisible()
})
```

### Visual Regression — Glass Design System
```typescript
test('guardian card visual snapshot', async ({ page }) => {
  await page.goto('/lore/guardians')
  await page.waitForLoadState('networkidle')
  
  // Wait for glassmorphism animations to settle
  await page.waitForTimeout(500)
  
  // Snapshot the guardian grid
  const grid = page.locator('[data-testid="guardian-grid"]')
  await expect(grid).toHaveScreenshot('guardian-grid.png', {
    maxDiffPixelRatio: 0.02, // 2% tolerance for antialiasing
  })
})
```

---

## Auth Helper

```typescript
// tests/helpers/auth.ts — reuse across tests
import { type Page } from '@playwright/test'

export async function authenticateTestUser(page: Page) {
  await page.goto('/auth/sign-in')
  await page.waitForLoadState('networkidle')
  await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!)
  await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!)
  await page.click('[type="submit"]')
  await page.waitForURL(/\/(academy|dashboard|lore)/)
}

// Use storage state for faster auth across tests
// playwright.config.ts: use: { storageState: 'playwright/.auth/user.json' }
```

### Save auth state once
```typescript
// tests/auth.setup.ts — runs before test suite
import { test as setup } from '@playwright/test'
import { authenticateTestUser } from './helpers/auth'

const authFile = 'playwright/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await authenticateTestUser(page)
  await page.context().storageState({ path: authFile })
})
```

---

## Common Patterns

### Wait for Next.js hydration
```typescript
// Always after navigation to dynamic Next.js pages
await page.goto('/path')
await page.waitForLoadState('networkidle') // waits for all network requests
```

### Capture screenshots for debugging
```typescript
// Inline debug screenshot (delete after fixing)
await page.screenshot({ path: `/tmp/debug-${Date.now()}.png`, fullPage: true })
```

### Test data attributes — add to Arcanea components
```typescript
// In components: always add data-testid for critical interactive elements
<button data-testid="unlock-gate-btn" onClick={handleUnlock}>
  Unlock Gate
</button>

// In tests: prefer data-testid over CSS selectors (resilient to style changes)
await page.click('[data-testid="unlock-gate-btn"]')
```

### Intercept API calls
```typescript
// Mock Supabase/API calls in tests
await page.route('/api/guardians', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify(MOCK_GUARDIANS),
  })
})
```

---

## Running Tests

```bash
# From apps/web directory
cd apps/web

# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/lore.spec.ts

# Run with UI mode (visual debugger)
npx playwright test --ui

# Debug specific test
npx playwright test --debug tests/e2e/gate-quiz.spec.ts

# Update snapshots
npx playwright test --update-snapshots

# View report
npx playwright show-report
```

---

## Quick Checklist

Before shipping any Playwright test in Arcanea:

- [ ] `waitForLoadState('networkidle')` after every navigation
- [ ] Screenshots taken during reconnaissance, deleted before commit
- [ ] `data-testid` attributes used for selectors (not CSS classes)
- [ ] Auth handled via storage state for speed
- [ ] Environment variables for test credentials (TEST_USER_EMAIL, TEST_USER_PASSWORD)
- [ ] API mocks in place for flaky external calls
- [ ] Tests are independent — no shared state between tests
- [ ] Visual snapshots have 2% tolerance for antialiasing
