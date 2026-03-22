---
name: cucumber-playwright
description: Cucumber BDD with Playwright policies. Use when writing Gherkin scenarios with Playwright step definitions. Do NOT use for Cypress-based BDD -- use cucumber-cypress instead. Do NOT use for non-BDD Playwright tests.
durability: encoded-preference
---

# Cucumber + Playwright Policies

Use `@cucumber/cucumber` with `@playwright/test` for BDD E2E testing.

## Project Structure

```
features/*.feature
step_definitions/*.steps.ts
support/
├── hooks.ts          # Browser lifecycle
├── world.ts          # Shared page context
cucumber.js
```

## World Object (REQUIRED)

Share Playwright page across steps:

```typescript
// support/world.ts
import { setWorldConstructor, World } from '@cucumber/cucumber'
import { BrowserContext, Page } from '@playwright/test'

export class PlaywrightWorld extends World {
  context!: BrowserContext
  page!: Page
}

setWorldConstructor(PlaywrightWorld)
```

## Hooks for Browser Lifecycle

```typescript
// support/hooks.ts
import { Before, After, BeforeAll, AfterAll } from '@cucumber/cucumber'
import { chromium, Browser } from '@playwright/test'

let browser: Browser

BeforeAll(async () => { browser = await chromium.launch() })
AfterAll(async () => { await browser.close() })

Before(async function (this: PlaywrightWorld) {
  this.context = await browser.newContext()
  this.page = await this.context.newPage()
})

After(async function (this: PlaywrightWorld) {
  await this.context.close()
})
```

## Step Definition Policies

### Use Semantic Selectors

```typescript
// GOOD: Role-based
await this.page.getByRole('button', { name: 'Login' }).click()
await this.page.getByTestId('email-input').fill(email)

// BAD: CSS selectors
await this.page.click('.btn-submit')
```

### Always Type `this` as PlaywrightWorld

```typescript
Given('I am on the login page', async function (this: PlaywrightWorld) {
  await this.page.goto('/login')
})
```

### Use Playwright Assertions

```typescript
import { expect } from '@playwright/test'

await expect(this.page).toHaveURL('/dashboard')
await expect(this.page.getByText(message)).toBeVisible()
```

## Commands

```bash
npx cucumber-js
npx cucumber-js --tags "@smoke"
npx cucumber-js features/login.feature
```

## Configuration

For setup details, use context7 to query `@cucumber/cucumber` documentation.
