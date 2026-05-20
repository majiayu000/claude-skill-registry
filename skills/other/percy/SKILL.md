---
name: percy
description: When the user wants to perform visual testing with automated screenshot comparison using Percy by BrowserStack. Also use when the user mentions "percy," "visual testing," "screenshot comparison," "visual diff," "percy snapshot," or "BrowserStack visual." For Storybook-specific visual testing, see chromatic.
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags:
    - visual-testing
    - screenshots
    - regression
    - ci-integration
---

# Percy

## Overview

You are an expert in Percy (by BrowserStack), the visual testing platform that captures screenshots and compares them against baselines. You help users integrate Percy into their existing test suites (Cypress, Playwright, Selenium, Storybook), configure responsive widths, manage visual baselines, and set up CI pipelines with Percy checks.

## Instructions

### Initial Assessment

1. **Test framework** — Cypress, Playwright, Selenium, or Storybook?
2. **Pages/components** — What needs visual coverage?
3. **Responsive** — Which viewport widths matter?
4. **CI** — Which CI provider?

### Setup with Cypress

```bash
# setup-percy-cypress.sh — Install Percy for Cypress.
npm install --save-dev @percy/cli @percy/cypress
```

```javascript
// cypress/support/e2e.js — Import Percy's Cypress commands.
// Adds cy.percySnapshot() to all Cypress tests.
import '@percy/cypress';
```

```javascript
// cypress/e2e/homepage.cy.js — Cypress test with Percy visual snapshots.
// Takes screenshots at key states for visual comparison.
describe('Homepage', () => {
  it('should render correctly', () => {
    cy.visit('/');
    cy.get('.hero-section').should('be.visible');
    cy.percySnapshot('Homepage - Hero');

    cy.get('.features-section').scrollIntoView();
    cy.percySnapshot('Homepage - Features');
  });

  it('should render mobile layout', () => {
    cy.viewport(375, 812);
    cy.visit('/');
    cy.percySnapshot('Homepage - Mobile');
  });
});
```

### Setup with Playwright

```bash
# setup-percy-playwright.sh — Install Percy for Playwright.
npm install --save-dev @percy/cli @percy/playwright
```

```typescript
// tests/visual.spec.ts — Playwright test with Percy snapshots.
// Captures visual state after interactions.
import { test, expect } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test('dashboard visual test', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForSelector('.chart-container');
  await percySnapshot(page, 'Dashboard - Charts Loaded');

  await page.click('[data-testid="dark-mode-toggle"]');
  await percySnapshot(page, 'Dashboard - Dark Mode');
});
```

### Storybook Integration

```bash
# setup-percy-storybook.sh — Install Percy for Storybook.
npm install --save-dev @percy/cli @percy/storybook
```

```bash
# run-percy-storybook.sh — Run Percy on all Storybook stories.
# Builds Storybook first, then snapshots every story.
npx percy storybook http://localhost:6006
```

### Percy Configuration

```yaml
# .percy.yml — Percy project configuration.
# Controls snapshot widths, CSS overrides, and discovery settings.
version: 2
snapshot:
  widths:
    - 375
    - 768
    - 1280
  min-height: 1024
  percy-css: |
    .animation, [data-animated] {
      animation: none !important;
      transition: none !important;
    }
    .timestamp {
      visibility: hidden;
    }
discovery:
  network-idle-timeout: 500
  disable-cache: true
```

### Per-Snapshot Configuration

```javascript
// tests/visual-config.cy.js — Percy snapshots with per-snapshot options.
// Override widths and CSS for specific snapshots.
describe('Product Page', () => {
  it('captures product card at specific widths', () => {
    cy.visit('/products/1');
    cy.get('.product-card').should('be.visible');

    cy.percySnapshot('Product Card', {
      widths: [375, 1280],
      minHeight: 800,
      percyCSS: '.price-timer { display: none; }',
    });
  });
});
```

### CI Integration

```yaml
# .github/workflows/percy.yml — Run Percy visual tests in GitHub Actions.
# Uses PERCY_TOKEN secret for authentication.
name: Visual Tests
on: [push, pull_request]
jobs:
  percy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx percy exec -- cypress run
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

### Running Percy

```bash
# run-percy.sh — Common Percy commands.
# Wrap your test command with percy exec.

# With Cypress
npx percy exec -- cypress run

# With Playwright
npx percy exec -- playwright test

# With Storybook
npx percy storybook http://localhost:6006

# Finalize (useful in parallel CI)
npx percy build:finalize
```
