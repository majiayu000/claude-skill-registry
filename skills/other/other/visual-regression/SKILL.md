---
name: Visual Regression Testing
description: Visual regression testing skill using Playwright, covering screenshot comparison, visual diff thresholds, responsive testing, baseline management, and CI integration.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [visual-regression, screenshot, playwright, visual-diff, responsive, baseline]
testingTypes: [visual, e2e]
frameworks: [playwright]
languages: [typescript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Visual Regression Testing Skill

You are an expert QA engineer specializing in visual regression testing with Playwright. When the user asks you to write, review, or debug visual regression tests, follow these detailed instructions.

## Core Principles

1. **Pixel-perfect baselines** -- Baseline screenshots are the source of truth for visual correctness.
2. **Deterministic rendering** -- Eliminate sources of visual non-determinism (animations, fonts, dynamic data).
3. **Threshold-based comparison** -- Allow small acceptable differences to reduce false positives.
4. **Responsive coverage** -- Test key breakpoints, not just desktop resolution.
5. **Component and page level** -- Test both individual components and full page layouts.

## Project Structure

```
tests/
  visual/
    pages/
      homepage.visual.spec.ts
      login.visual.spec.ts
      dashboard.visual.spec.ts
    components/
      navigation.visual.spec.ts
      footer.visual.spec.ts
      card.visual.spec.ts
    responsive/
      homepage.responsive.spec.ts
      checkout.responsive.spec.ts
    utils/
      visual-helpers.ts
      mask-helpers.ts
  visual.config.ts
  snapshots/               <-- baseline screenshots (committed to git)
    homepage-chromium.png
    login-chromium.png
playwright.config.ts
```

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/visual',
  snapshotDir: './tests/snapshots',
  snapshotPathTemplate: '{snapshotDir}/{testFileDir}/{testFileName}-snapshots/{arg}{-projectName}{ext}',
  fullyParallel: true,
  retries: 0, // Visual tests should not retry -- flaky visuals indicate real issues
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,           // Allow up to 100 pixels difference
      maxDiffPixelRatio: 0.01,      // Or 1% of total pixels
      threshold: 0.2,               // Per-pixel color threshold (0-1)
      animations: 'disabled',       // Disable CSS animations
    },
    toMatchSnapshot: {
      maxDiffPixelRatio: 0.01,
    },
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Force consistent font rendering
        launchOptions: {
          args: ['--font-render-hinting=none', '--disable-skia-runtime-opts'],
        },
      },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-portrait',
      use: {
        ...devices['iPhone 13'],
      },
    },
    {
      name: 'tablet',
      use: {
        ...devices['iPad Pro 11'],
      },
    },
  ],
});
```

## Writing Visual Tests

### Full Page Screenshots

```typescript
import { test, expect } from '@playwright/test';

test.describe('Homepage Visual Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('homepage should match baseline', async ({ page }) => {
    await expect(page).toHaveScreenshot('homepage-full.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('homepage above-the-fold should match baseline', async ({ page }) => {
    await expect(page).toHaveScreenshot('homepage-above-fold.png', {
      fullPage: false, // Viewport only
    });
  });

  test('homepage with content loaded should match baseline', async ({ page }) => {
    // Wait for all dynamic content
    await page.getByRole('heading', { name: 'Featured Products' }).waitFor();
    await page.waitForSelector('img[src*="product"]', { state: 'visible' });

    await expect(page).toHaveScreenshot('homepage-loaded.png', {
      fullPage: true,
    });
  });
});
```

### Component-Level Screenshots

```typescript
test.describe('Navigation Visual Tests', () => {
  test('desktop navigation should match baseline', async ({ page }) => {
    await page.goto('/');
    const nav = page.getByRole('navigation', { name: 'Main' });

    await expect(nav).toHaveScreenshot('nav-desktop.png');
  });

  test('navigation hover state should match baseline', async ({ page }) => {
    await page.goto('/');
    const productsLink = page.getByRole('link', { name: 'Products' });

    await productsLink.hover();
    await expect(page.getByRole('navigation')).toHaveScreenshot('nav-hover.png');
  });

  test('navigation dropdown should match baseline', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Account' }).click();

    const dropdown = page.getByRole('menu');
    await expect(dropdown).toHaveScreenshot('nav-dropdown.png');
  });
});
```

### State-Based Visual Tests

```typescript
test.describe('Form Visual States', () => {
  test('empty form should match baseline', async ({ page }) => {
    await page.goto('/register');
    await expect(page.locator('form')).toHaveScreenshot('form-empty.png');
  });

  test('form with validation errors should match baseline', async ({ page }) => {
    await page.goto('/register');
    await page.getByRole('button', { name: 'Submit' }).click();

    // Wait for validation messages to appear
    await page.getByText('Email is required').waitFor();

    await expect(page.locator('form')).toHaveScreenshot('form-errors.png');
  });

  test('form with filled data should match baseline', async ({ page }) => {
    await page.goto('/register');
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByLabel('Password').fill('SecurePass123!');

    await expect(page.locator('form')).toHaveScreenshot('form-filled.png');
  });

  test('disabled button state should match baseline', async ({ page }) => {
    await page.goto('/register');
    const button = page.getByRole('button', { name: 'Submit' });

    await expect(button).toHaveScreenshot('button-disabled.png');
  });
});
```

### Responsive Visual Tests

```typescript
test.describe('Responsive Layout Tests', () => {
  const viewports = [
    { name: 'mobile', width: 375, height: 667 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'desktop', width: 1280, height: 720 },
    { name: 'wide', width: 1920, height: 1080 },
  ];

  for (const viewport of viewports) {
    test(`homepage at ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      await expect(page).toHaveScreenshot(`homepage-${viewport.name}.png`, {
        fullPage: true,
      });
    });
  }
});
```

## Handling Dynamic Content

### Masking Dynamic Elements

```typescript
test('dashboard should match baseline with dynamic content masked', async ({ page }) => {
  await page.goto('/dashboard');

  await expect(page).toHaveScreenshot('dashboard.png', {
    mask: [
      page.locator('[data-testid="current-time"]'),
      page.locator('[data-testid="user-avatar"]'),
      page.locator('[data-testid="notification-count"]'),
      page.locator('.chart-container'), // Dynamic chart data
      page.locator('.ad-banner'),        // Third-party ads
    ],
    fullPage: true,
  });
});
```

### Replacing Dynamic Content

```typescript
test('profile page should match baseline', async ({ page }) => {
  await page.goto('/profile');

  // Replace dynamic text with consistent values
  await page.evaluate(() => {
    // Replace timestamps
    document.querySelectorAll('[data-testid="timestamp"]').forEach((el) => {
      el.textContent = 'January 1, 2024';
    });

    // Replace user-specific data
    const nameEl = document.querySelector('[data-testid="user-name"]');
    if (nameEl) nameEl.textContent = 'Test User';

    // Remove random elements
    document.querySelectorAll('.random-recommendation').forEach((el) => el.remove());
  });

  await expect(page).toHaveScreenshot('profile-page.png', {
    fullPage: true,
  });
});
```

### Disabling Animations

```typescript
test.beforeEach(async ({ page }) => {
  // Disable all CSS animations and transitions
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
        scroll-behavior: auto !important;
      }
    `,
  });
});
```

### Waiting for Fonts

```typescript
test('page with custom fonts should match baseline', async ({ page }) => {
  await page.goto('/');

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);

  // Additional wait for font rendering
  await page.waitForTimeout(500); // acceptable for font rendering

  await expect(page).toHaveScreenshot('page-with-fonts.png');
});
```

## Baseline Management

### Updating Baselines

```bash
# Update all baselines
npx playwright test --update-snapshots

# Update baselines for specific tests
npx playwright test tests/visual/homepage.visual.spec.ts --update-snapshots

# Update baselines for specific project
npx playwright test --project=chromium --update-snapshots
```

### Baseline Workflow

```markdown
## Baseline Update Process

1. **Intentional change:** Developer modifies UI deliberately
2. **Visual tests fail:** CI detects the visual difference
3. **Review the diff:** Download artifacts, inspect the visual diff
4. **Approve the change:** If the change is intended:
   a. Run `npx playwright test --update-snapshots` locally
   b. Commit the updated baseline screenshots
   c. Push and verify CI passes
5. **Reject the change:** If the change is unintended:
   a. Revert the code change causing the visual difference
   b. Verify visual tests pass again
```

### Git LFS for Baselines

```bash
# Install Git LFS
git lfs install

# Track screenshot files
git lfs track "tests/snapshots/**/*.png"
git lfs track "tests/snapshots/**/*.jpg"

# Add .gitattributes
git add .gitattributes
git commit -m "Track visual baselines with Git LFS"
```

## Visual Diff Analysis

### Understanding Diff Output

When a visual test fails, Playwright generates three images:

```
test-results/
  homepage-visual-spec-ts/
    homepage-full-chromium-expected.png    <-- Baseline (what it should look like)
    homepage-full-chromium-actual.png      <-- Current (what it looks like now)
    homepage-full-chromium-diff.png        <-- Diff (highlighted differences)
```

### Custom Diff Thresholds

```typescript
// Strict comparison for brand-critical pages
test('brand logo should be pixel-perfect', async ({ page }) => {
  await page.goto('/');
  const logo = page.locator('[data-testid="brand-logo"]');
  await expect(logo).toHaveScreenshot('brand-logo.png', {
    maxDiffPixels: 0,        // Zero tolerance
    threshold: 0,            // Exact pixel match
  });
});

// Relaxed comparison for content-heavy pages
test('blog listing visual check', async ({ page }) => {
  await page.goto('/blog');
  await expect(page).toHaveScreenshot('blog-listing.png', {
    maxDiffPixelRatio: 0.05, // Allow 5% difference
    threshold: 0.3,          // More color tolerance
  });
});
```

## Dark Mode and Theme Testing

```typescript
test.describe('Dark Mode Visual Tests', () => {
  test('homepage in dark mode', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/');

    await expect(page).toHaveScreenshot('homepage-dark.png', { fullPage: true });
  });

  test('homepage in light mode', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'light' });
    await page.goto('/');

    await expect(page).toHaveScreenshot('homepage-light.png', { fullPage: true });
  });

  test('reduced motion preference', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/');

    // Verify no animations are visible
    await expect(page).toHaveScreenshot('homepage-reduced-motion.png');
  });
});
```

## CI Integration

### GitHub Actions for Visual Tests

```yaml
visual-tests:
  name: Visual Regression Tests
  runs-on: ubuntu-latest
  timeout-minutes: 30
  container:
    image: mcr.microsoft.com/playwright:v1.42.0-jammy
  steps:
    - uses: actions/checkout@v4
      with:
        lfs: true  # Important: fetch LFS baselines

    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - run: npm ci

    - name: Run Visual Tests
      run: npx playwright test tests/visual/

    - name: Upload Visual Diff
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: visual-diffs
        path: |
          test-results/**/
        retention-days: 14

    - name: Comment PR with Visual Diff
      if: failure() && github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.issue.number,
            body: '## Visual Regression Detected\n\nVisual differences were found. Please download the artifacts to review the diffs.\n\n[View workflow run](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})'
          });
```

## Best Practices

1. **Disable animations** -- CSS animations cause non-deterministic screenshots.
2. **Wait for content** -- Always wait for dynamic content, images, and fonts to load.
3. **Use deterministic data** -- Mock API responses to ensure consistent test data.
4. **Mask dynamic regions** -- Cover timestamps, avatars, and third-party widgets.
5. **Test key breakpoints** -- Cover mobile, tablet, and desktop at minimum.
6. **Set reasonable thresholds** -- Too strict causes false positives; too loose misses real bugs.
7. **Use consistent environments** -- Run visual tests in Docker containers for consistent rendering.
8. **Review diffs carefully** -- Not every pixel change is a bug; some are expected.
9. **Version baselines** -- Commit baselines to source control (with Git LFS for large repos).
10. **Test component states** -- Cover hover, focus, active, disabled, error, and loading states.

## Anti-Patterns to Avoid

1. **No animation control** -- Animations make screenshots non-deterministic.
2. **Testing with live data** -- Real API data changes, causing false failures.
3. **Zero-pixel tolerance** -- Even anti-aliasing differences trigger failures.
4. **Full-page screenshots only** -- Component-level screenshots catch more specific regressions.
5. **Ignoring font loading** -- Fonts not loaded produce blank text in screenshots.
6. **Not masking dynamic content** -- Timestamps and counters change every run.
7. **Running visual tests locally only** -- Different OS renders fonts differently.
8. **Too many visual tests** -- Maintain baselines only for critical pages and components.
9. **Not reviewing failures** -- Auto-updating baselines without review hides real regressions.
10. **Missing responsive tests** -- Desktop-only visual tests miss mobile layout bugs.
