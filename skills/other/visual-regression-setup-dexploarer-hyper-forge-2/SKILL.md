---
name: visual-regression-test-setup
description: Sets up visual regression testing using Percy, Chromatic, or Playwright to catch unintended UI changes through screenshot comparison. Use when user asks to "setup visual testing", "add screenshot tests", "prevent visual bugs", or "setup Percy/Chromatic".
allowed-tools: [Write, Read, Bash]
---

# Visual Regression Test Setup

Sets up automated visual regression testing to catch unintended UI changes through pixel-perfect screenshot comparison.

## When to Use

- "Setup visual regression testing"
- "Add screenshot tests"
- "Prevent visual bugs"
- "Setup Percy/Chromatic"
- "Test UI changes automatically"

## Instructions

### 1. Choose Testing Tool

**Popular Options:**
- **Percy** (BrowserStack) - Easy setup, CI/CD integration
- **Chromatic** (Storybook) - Best for component libraries
- **Playwright** - Free, self-hosted
- **BackstopJS** - Free, self-hosted
- **Applitools** - AI-powered

### 2. Setup Percy (Recommended for Most Projects)

**Install:**
```bash
npm install --save-dev @percy/cli @percy/playwright
# or for other frameworks
npm install --save-dev @percy/cypress
npm install --save-dev @percy/puppeteer
npm install --save-dev @percy/storybook
```

**Playwright + Percy:**
```javascript
// tests/visual/homepage.spec.ts
import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test.describe('Homepage Visual Tests', () => {
  test('homepage desktop', async ({ page }) => {
    await page.goto('http://test-frontend:3000');
    await percySnapshot(page, 'Homepage - Desktop');
  });

  test('homepage mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('http://test-frontend:3000');
    await percySnapshot(page, 'Homepage - Mobile');
  });

  test('homepage tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('http://test-frontend:3000');
    await percySnapshot(page, 'Homepage - Tablet');
  });

  test('dark mode', async ({ page }) => {
    await page.goto('http://test-frontend:3000');
    await page.click('[data-testid="theme-toggle"]');
    await page.waitForTimeout(500); // Wait for transition
    await percySnapshot(page, 'Homepage - Dark Mode');
  });
});
```

**package.json:**
```json
{
  "scripts": {
    "test:visual": "percy exec -- playwright test tests/visual",
    "test:visual:update": "percy exec -- playwright test tests/visual --update-snapshots"
  }
}
```

**.percy.yml:**
```yaml
version: 2
snapshot:
  widths:
    - 375   # Mobile
    - 768   # Tablet
    - 1280  # Desktop
  min-height: 1024
  percy-css: |
    /* Hide dynamic content */
    .timestamp,
    .random-number,
    [data-testid="current-time"] {
      visibility: hidden;
    }
```

**GitHub Actions:**
```yaml
name: Visual Tests

on: [push, pull_request]

jobs:
  visual-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Run visual tests
        run: npm run test:visual
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

### 3. Setup Chromatic (Best for Storybook)

**Install:**
```bash
npm install --save-dev chromatic
```

**Setup Storybook (if not already):**
```bash
npx storybook init
```

**Run Chromatic:**
```bash
npx chromatic --project-token=<your-project-token>
```

**package.json:**
```json
{
  "scripts": {
    "chromatic": "chromatic --exit-zero-on-changes"
  }
}
```

**GitHub Actions:**
```yaml
name: Chromatic

on: push

jobs:
  chromatic:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Required for Chromatic

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run Chromatic
        uses: chromaui/action@v1
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true  # Don't fail on visual changes
          autoAcceptChanges: main  # Auto-accept on main branch
```

**Storybook Story Example:**
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    chromatic: {
      // Delay for animations
      delay: 300,
      // Test specific viewports
      viewports: [320, 768, 1200],
      // Disable animations
      disableSnapshot: false,
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
};

export const AllStates: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexDirection: 'column' }}>
      <Button variant="primary">Normal</Button>
      <Button variant="primary" className="hover">Hover</Button>
      <Button variant="primary" disabled>Disabled</Button>
      <Button variant="primary" loading>Loading</Button>
    </div>
  ),
};
```

### 4. Setup Playwright Visual Comparisons (Free)

**playwright.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  snapshotDir: './tests/snapshots',

  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://test-frontend:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**Test:**
```typescript
// tests/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('homepage looks correct', async ({ page }) => {
    await page.goto('http://test-frontend:3000');

    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');

    // Hide dynamic content
    await page.addStyleTag({
      content: '.timestamp { visibility: hidden; }'
    });

    // Take screenshot
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('button states', async ({ page }) => {
    await page.goto('http://test-frontend:3000/components');

    const button = page.locator('[data-testid="primary-button"]');

    // Normal state
    await expect(button).toHaveScreenshot('button-normal.png');

    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');

    // Focus state
    await button.focus();
    await expect(button).toHaveScreenshot('button-focus.png');
  });

  test('responsive design', async ({ page }) => {
    await page.goto('http://test-frontend:3000');

    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('homepage-desktop.png');

    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('homepage-tablet.png');

    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
```

**Update snapshots:**
```bash
npx playwright test --update-snapshots
```

### 5. Setup BackstopJS (Free, Self-Hosted)

**Install:**
```bash
npm install --save-dev backstopjs
```

**Initialize:**
```bash
npx backstop init
```

**backstop.json:**
```json
{
  "id": "myapp_visual_tests",
  "viewports": [
    {
      "label": "phone",
      "width": 375,
      "height": 667
    },
    {
      "label": "tablet",
      "width": 768,
      "height": 1024
    },
    {
      "label": "desktop",
      "width": 1920,
      "height": 1080
    }
  ],
  "scenarios": [
    {
      "label": "Homepage",
      "url": "http://test-frontend:3000",
      "delay": 500,
      "misMatchThreshold": 0.1,
      "requireSameDimensions": true
    },
    {
      "label": "About Page",
      "url": "http://test-frontend:3000/about",
      "delay": 500
    },
    {
      "label": "Dark Mode",
      "url": "http://test-frontend:3000",
      "clickSelector": "[data-testid='theme-toggle']",
      "postInteractionWait": 1000,
      "delay": 500
    },
    {
      "label": "Form States",
      "url": "http://test-frontend:3000/contact",
      "selectors": ["form"],
      "hoverSelector": "button[type='submit']",
      "delay": 200
    }
  ],
  "paths": {
    "bitmaps_reference": "backstop_data/bitmaps_reference",
    "bitmaps_test": "backstop_data/bitmaps_test",
    "engine_scripts": "backstop_data/engine_scripts",
    "html_report": "backstop_data/html_report",
    "ci_report": "backstop_data/ci_report"
  },
  "engine": "puppeteer",
  "report": ["browser", "CI"],
  "debug": false,
  "debugWindow": false
}
```

**package.json scripts:**
```json
{
  "scripts": {
    "backstop:reference": "backstop reference",
    "backstop:test": "backstop test",
    "backstop:approve": "backstop approve"
  }
}
```

**Usage:**
```bash
# Create baseline screenshots
npm run backstop:reference

# Run tests (compare against baseline)
npm run backstop:test

# Approve changes (update baseline)
npm run backstop:approve
```

### 6. Best Practices

**Handling Dynamic Content:**
```typescript
// Hide timestamps, random IDs, etc.
await page.addStyleTag({
  content: `
    .timestamp,
    .random-id,
    [data-dynamic="true"] {
      visibility: hidden !important;
    }
  `
});

// Or use Percy CSS
// .percy.yml
snapshot:
  percy-css: |
    .timestamp { display: none; }
```

**Testing Animations:**
```typescript
// Disable animations for consistent screenshots
await page.addStyleTag({
  content: `
    *,
    *::before,
    *::after {
      animation-duration: 0s !important;
      animation-delay: 0s !important;
      transition-duration: 0s !important;
      transition-delay: 0s !important;
    }
  `
});
```

**Testing Component States:**
```typescript
test('button all states', async ({ page }) => {
  await page.goto('http://test-frontend:3000/components');

  // Create a grid of all states
  await page.evaluate(() => {
    const container = document.querySelector('[data-testid="button-container"]');
    container.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
        <button class="primary">Normal</button>
        <button class="primary hover">Hover</button>
        <button class="primary focus">Focus</button>
        <button class="primary active">Active</button>
        <button class="primary" disabled>Disabled</button>
        <button class="primary loading">Loading</button>
      </div>
    `;
  });

  await expect(page.locator('[data-testid="button-container"]'))
    .toHaveScreenshot('button-all-states.png');
});
```

### 7. CI/CD Integration Tips

**Parallel Testing:**
```yaml
# GitHub Actions
jobs:
  visual-tests:
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
      - run: npx playwright test --project=${{ matrix.browser }}
```

**Only Run on UI Changes:**
```yaml
on:
  pull_request:
    paths:
      - 'src/components/**'
      - 'src/pages/**'
      - 'src/styles/**'
```

**Automatic Approval on Main:**
```yaml
- name: Auto-approve on main
  if: github.ref == 'refs/heads/main'
  run: npm run backstop:approve
```

### 8. Maintenance

**Review Process:**
```markdown
# Visual Regression Review Checklist

When visual tests fail:

1. [ ] Review the diff in Percy/Chromatic dashboard
2. [ ] Verify changes are intentional
3. [ ] Check all viewports (mobile, tablet, desktop)
4. [ ] Test in different browsers if applicable
5. [ ] Approve changes or fix issues
6. [ ] Update baseline snapshots

If changes are intentional:
- Approve in Percy/Chromatic dashboard
- Or run `npm run test:visual:update`

If changes are bugs:
- Fix the CSS/component
- Re-run tests to verify fix
```

### Best Practices

**DO:**
- Test multiple viewports
- Hide dynamic content
- Disable animations
- Test critical user flows
- Review diffs carefully
- Update baselines deliberately
- Test dark mode
- Test component states

**DON'T:**
- Test every page
- Ignore flaky tests
- Auto-approve everything
- Skip mobile testing
- Test with live data
- Forget to wait for loading
- Screenshot entire pages only
- Ignore small differences

## Checklist

- [ ] Visual testing tool selected
- [ ] Dependencies installed
- [ ] Configuration created
- [ ] Baseline snapshots created
- [ ] CI/CD integration added
- [ ] Dynamic content handled
- [ ] Multiple viewports tested
- [ ] Review process documented
- [ ] Team trained on workflow
