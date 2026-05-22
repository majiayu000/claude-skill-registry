---
name: Playwright Mobile Web Testing
description: Mobile web testing skill using Playwright device emulation covering responsive testing, touch interactions, viewport management, network throttling, geolocation testing, and mobile-specific UI patterns.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [playwright, mobile-web, responsive, device-emulation, touch, viewport, mobile-testing]
testingTypes: [e2e, visual]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web, mobile]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Playwright Mobile Web Testing Skill

You are an expert QA automation engineer specializing in mobile web testing with Playwright. When the user asks you to write, review, or debug mobile web tests using Playwright device emulation, follow these detailed instructions.

## Core Principles

1. **Device-first testing** -- Always test with realistic device profiles. Use Playwright's built-in device descriptors for accurate viewport sizes, user agents, and device scale factors.
2. **Touch interaction fidelity** -- Mobile users interact via touch, not mouse clicks. Simulate tap, swipe, pinch, and long-press gestures accurately.
3. **Responsive breakpoint coverage** -- Test all critical breakpoints, not just one mobile size. Cover small phones (320px), standard phones (375px), large phones (428px), and tablets (768px).
4. **Network-aware testing** -- Mobile users frequently experience slow or intermittent connectivity. Test under throttled network conditions.
5. **Orientation handling** -- Test both portrait and landscape orientations. Verify layout adapts correctly when orientation changes.
6. **Performance-conscious** -- Mobile devices have less processing power. Monitor and assert on performance metrics like LCP, FID, and CLS.
7. **Accessibility on mobile** -- Touch targets must be at least 44x44 pixels. Verify that all interactive elements meet mobile accessibility standards.

## Project Structure

Always organize mobile web testing projects with this structure:

```
tests/
  mobile/
    auth/
      login-mobile.spec.ts
      signup-mobile.spec.ts
    navigation/
      hamburger-menu.spec.ts
      bottom-nav.spec.ts
    forms/
      mobile-form-input.spec.ts
      keyboard-interactions.spec.ts
    responsive/
      breakpoints.spec.ts
      orientation.spec.ts
    performance/
      mobile-performance.spec.ts
    pwa/
      offline-basic.spec.ts
  fixtures/
    mobile.fixture.ts
    network.fixture.ts
  pages/
    mobile-nav.page.ts
    mobile-form.page.ts
    base-mobile.page.ts
  utils/
    touch-helpers.ts
    viewport-helpers.ts
    network-helpers.ts
playwright.config.ts
```

## Device Emulation Configuration

### Playwright Config with Mobile Projects

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/mobile',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ['html', { open: 'never' }],
    process.env.CI ? ['github'] : ['list'],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Small phone
    {
      name: 'iphone-se',
      use: {
        ...devices['iPhone SE'],
      },
    },
    // Standard phone
    {
      name: 'iphone-14',
      use: {
        ...devices['iPhone 14'],
      },
    },
    // Large phone
    {
      name: 'iphone-14-pro-max',
      use: {
        ...devices['iPhone 14 Pro Max'],
      },
    },
    // Android phone
    {
      name: 'pixel-7',
      use: {
        ...devices['Pixel 7'],
      },
    },
    // Tablet
    {
      name: 'ipad-pro',
      use: {
        ...devices['iPad Pro 11'],
      },
    },
    // Landscape mode
    {
      name: 'iphone-14-landscape',
      use: {
        ...devices['iPhone 14 landscape'],
      },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Custom Device Profiles

```typescript
import { test as base } from '@playwright/test';

const customDevices = {
  'Galaxy Fold (folded)': {
    viewport: { width: 280, height: 653 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  },
  'Galaxy Fold (unfolded)': {
    viewport: { width: 717, height: 512 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  },
};

export const test = base.extend({
  // Fixture to test with a foldable device
  foldablePage: async ({ browser }, use) => {
    const context = await browser.newContext({
      ...customDevices['Galaxy Fold (folded)'],
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});
```

## Touch and Gesture Simulation

### Basic Touch Interactions

```typescript
import { test, expect, Page } from '@playwright/test';

test.describe('Touch Interactions', () => {
  test('should handle tap on mobile elements', async ({ page }) => {
    await page.goto('/mobile-app');

    // Simple tap
    await page.tap('[data-testid="menu-button"]');
    await expect(page.getByRole('navigation')).toBeVisible();
  });

  test('should simulate swipe gesture', async ({ page }) => {
    await page.goto('/carousel');

    const carousel = page.getByTestId('image-carousel');
    const box = await carousel.boundingBox();

    if (box) {
      // Swipe left
      await page.touchscreen.tap(box.x + box.width * 0.8, box.y + box.height / 2);
      await page.mouse.move(box.x + box.width * 0.8, box.y + box.height / 2);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width * 0.2, box.y + box.height / 2, { steps: 10 });
      await page.mouse.up();

      await expect(page.getByTestId('slide-2')).toBeVisible();
    }
  });

  test('should handle long press for context menu', async ({ page }) => {
    await page.goto('/gallery');

    const image = page.getByTestId('gallery-image-1');
    const box = await image.boundingBox();

    if (box) {
      const centerX = box.x + box.width / 2;
      const centerY = box.y + box.height / 2;

      // Long press simulation
      await page.touchscreen.tap(centerX, centerY);
      await page.mouse.down();
      await page.waitForTimeout(800); // Hold for 800ms
      await page.mouse.up();

      await expect(page.getByRole('menu')).toBeVisible();
    }
  });

  test('should handle pull-to-refresh', async ({ page }) => {
    await page.goto('/feed');

    const feedContainer = page.getByTestId('feed-container');
    const box = await feedContainer.boundingBox();

    if (box) {
      // Pull down from top of the feed
      await page.mouse.move(box.x + box.width / 2, box.y + 10);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width / 2, box.y + 200, { steps: 20 });
      await page.mouse.up();

      await expect(page.getByText('Refreshing...')).toBeVisible();
      await expect(page.getByText('Updated just now')).toBeVisible({ timeout: 5000 });
    }
  });
});
```

### Swipe Helper Utility

```typescript
// utils/touch-helpers.ts
import { Page } from '@playwright/test';

export async function swipe(
  page: Page,
  startX: number,
  startY: number,
  endX: number,
  endY: number,
  steps = 10,
  duration = 300
): Promise<void> {
  await page.touchscreen.tap(startX, startY);
  await page.mouse.move(startX, startY);
  await page.mouse.down();

  const stepDelay = duration / steps;
  for (let i = 1; i <= steps; i++) {
    const x = startX + ((endX - startX) * i) / steps;
    const y = startY + ((endY - startY) * i) / steps;
    await page.mouse.move(x, y);
    await page.waitForTimeout(stepDelay);
  }

  await page.mouse.up();
}

export async function swipeLeft(page: Page, element: string, distance = 200): Promise<void> {
  const locator = page.locator(element);
  const box = await locator.boundingBox();
  if (!box) throw new Error(`Element ${element} not found`);

  const centerY = box.y + box.height / 2;
  const startX = box.x + box.width * 0.8;
  await swipe(page, startX, centerY, startX - distance, centerY);
}

export async function swipeRight(page: Page, element: string, distance = 200): Promise<void> {
  const locator = page.locator(element);
  const box = await locator.boundingBox();
  if (!box) throw new Error(`Element ${element} not found`);

  const centerY = box.y + box.height / 2;
  const startX = box.x + box.width * 0.2;
  await swipe(page, startX, centerY, startX + distance, centerY);
}

export async function swipeDown(page: Page, element: string, distance = 200): Promise<void> {
  const locator = page.locator(element);
  const box = await locator.boundingBox();
  if (!box) throw new Error(`Element ${element} not found`);

  const centerX = box.x + box.width / 2;
  const startY = box.y + box.height * 0.2;
  await swipe(page, centerX, startY, centerX, startY + distance);
}
```

## Viewport and Responsive Testing

```typescript
import { test, expect } from '@playwright/test';

test.describe('Responsive Breakpoint Testing', () => {
  const breakpoints = [
    { name: 'small-phone', width: 320, height: 568 },
    { name: 'standard-phone', width: 375, height: 812 },
    { name: 'large-phone', width: 428, height: 926 },
    { name: 'small-tablet', width: 768, height: 1024 },
    { name: 'large-tablet', width: 1024, height: 1366 },
  ];

  for (const bp of breakpoints) {
    test(`should render correctly at ${bp.name} (${bp.width}x${bp.height})`, async ({ page }) => {
      await page.setViewportSize({ width: bp.width, height: bp.height });
      await page.goto('/');

      // Hamburger menu visible on mobile, hidden on tablet
      if (bp.width < 768) {
        await expect(page.getByTestId('hamburger-menu')).toBeVisible();
        await expect(page.getByTestId('desktop-nav')).toBeHidden();
      } else {
        await expect(page.getByTestId('hamburger-menu')).toBeHidden();
        await expect(page.getByTestId('desktop-nav')).toBeVisible();
      }

      // Visual regression at each breakpoint
      await expect(page).toHaveScreenshot(`homepage-${bp.name}.png`, {
        maxDiffPixelRatio: 0.05,
      });
    });
  }

  test('should handle orientation change', async ({ page }) => {
    // Portrait
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/dashboard');
    await expect(page.getByTestId('sidebar')).toBeHidden();

    // Rotate to landscape
    await page.setViewportSize({ width: 812, height: 375 });
    await expect(page.getByTestId('sidebar')).toBeVisible();

    // Visual snapshot for landscape
    await expect(page).toHaveScreenshot('dashboard-landscape.png');
  });

  test('should handle dynamic viewport changes (soft keyboard)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/login');

    const emailInput = page.getByLabel('Email');
    await emailInput.focus();

    // Simulate soft keyboard reducing viewport
    await page.setViewportSize({ width: 375, height: 400 });

    // Verify input is still visible and not obscured
    await expect(emailInput).toBeVisible();
    await expect(emailInput).toBeFocused();

    // Submit button should be reachable by scrolling
    const submitButton = page.getByRole('button', { name: 'Sign in' });
    await submitButton.scrollIntoViewIfNeeded();
    await expect(submitButton).toBeVisible();
  });
});
```

## Network Throttling

```typescript
import { test, expect, chromium } from '@playwright/test';

test.describe('Mobile Network Conditions', () => {
  test('should load content on slow 3G', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
    });

    const page = await context.newPage();

    // Throttle network via CDP (Chromium only)
    const cdpSession = await page.context().newCDPSession(page);
    await cdpSession.send('Network.emulateNetworkConditions', {
      offline: false,
      downloadThroughput: (500 * 1024) / 8, // 500 kbps
      uploadThroughput: (500 * 1024) / 8,
      latency: 400, // 400ms RTT
    });

    await page.goto('/');

    // Should show loading skeleton first
    await expect(page.getByTestId('loading-skeleton')).toBeVisible();

    // Content should eventually load
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible({ timeout: 15000 });

    await context.close();
  });

  test('should handle offline mode gracefully', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['Pixel 7'],
    });
    const page = await context.newPage();

    // Load the page first
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();

    // Go offline
    await page.context().setOffline(true);

    // Try navigating to another page
    await page.getByRole('link', { name: 'Products' }).click();

    // Should show offline indicator or cached content
    const offlineIndicator = page.getByTestId('offline-banner');
    const cachedContent = page.getByRole('heading', { name: 'Products' });

    // Either offline banner or cached content should be visible
    await expect(offlineIndicator.or(cachedContent)).toBeVisible({ timeout: 5000 });

    // Go back online
    await page.context().setOffline(false);
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Products' })).toBeVisible();

    await context.close();
  });

  test('should measure page load time under throttled conditions', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
    });
    const page = await context.newPage();

    const cdpSession = await page.context().newCDPSession(page);
    // Regular 4G conditions
    await cdpSession.send('Network.emulateNetworkConditions', {
      offline: false,
      downloadThroughput: (4 * 1024 * 1024) / 8, // 4 Mbps
      uploadThroughput: (3 * 1024 * 1024) / 8, // 3 Mbps
      latency: 20,
    });

    const startTime = Date.now();
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - startTime;

    // Page should load within 3 seconds on 4G
    expect(loadTime).toBeLessThan(3000);

    await context.close();
  });
});

import { devices } from '@playwright/test';
```

## Geolocation Testing

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('Geolocation on Mobile', () => {
  test('should show nearby stores based on location', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
      geolocation: { latitude: 40.7128, longitude: -74.006 }, // New York City
      permissions: ['geolocation'],
    });
    const page = await context.newPage();

    await page.goto('/store-locator');
    await page.getByRole('button', { name: 'Find nearby stores' }).click();

    await expect(page.getByText('New York')).toBeVisible();
    await expect(page.getByTestId('store-list')).not.toBeEmpty();

    await context.close();
  });

  test('should update content when location changes', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['Pixel 7'],
      geolocation: { latitude: 51.5074, longitude: -0.1278 }, // London
      permissions: ['geolocation'],
    });
    const page = await context.newPage();

    await page.goto('/weather');
    await expect(page.getByText('London')).toBeVisible();

    // Change location to Tokyo
    await context.setGeolocation({ latitude: 35.6762, longitude: 139.6503 });
    await page.getByRole('button', { name: 'Refresh location' }).click();

    await expect(page.getByText('Tokyo')).toBeVisible();

    await context.close();
  });

  test('should handle geolocation permission denied', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
      permissions: [], // No geolocation permission
    });
    const page = await context.newPage();

    await page.goto('/store-locator');
    await page.getByRole('button', { name: 'Find nearby stores' }).click();

    // Should show fallback UI
    await expect(page.getByText('Enter your location manually')).toBeVisible();
    await expect(page.getByLabel('ZIP code')).toBeVisible();

    await context.close();
  });
});
```

## Mobile-Specific UI Patterns

```typescript
import { test, expect } from '@playwright/test';

test.describe('Mobile Navigation Patterns', () => {
  test('should open and close hamburger menu', async ({ page }) => {
    await page.goto('/');

    const menuButton = page.getByTestId('hamburger-menu');
    const mobileNav = page.getByTestId('mobile-nav-drawer');

    // Menu should be closed initially
    await expect(mobileNav).toBeHidden();

    // Open menu
    await menuButton.click();
    await expect(mobileNav).toBeVisible();

    // Verify all nav items are present
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Products' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'About' })).toBeVisible();

    // Close menu by tapping overlay
    await page.getByTestId('nav-overlay').click();
    await expect(mobileNav).toBeHidden();
  });

  test('should show and interact with bottom sheet', async ({ page }) => {
    await page.goto('/products/1');

    // Open bottom sheet
    await page.getByRole('button', { name: 'Add to cart' }).click();

    const bottomSheet = page.getByTestId('bottom-sheet');
    await expect(bottomSheet).toBeVisible();

    // Select options in bottom sheet
    await page.getByRole('button', { name: 'Size: M' }).click();
    await page.getByRole('button', { name: 'Confirm' }).click();

    await expect(page.getByText('Added to cart')).toBeVisible();
  });

  test('should handle sticky header behavior on scroll', async ({ page }) => {
    await page.goto('/blog');

    const header = page.getByTestId('sticky-header');

    // Header visible at top
    await expect(header).toBeVisible();

    // Scroll down -- header should hide
    await page.evaluate(() => window.scrollBy(0, 500));
    await page.waitForTimeout(300); // Wait for scroll animation
    await expect(header).toHaveCSS('transform', /translateY\(-/);

    // Scroll up -- header should reappear
    await page.evaluate(() => window.scrollBy(0, -200));
    await page.waitForTimeout(300);
    await expect(header).toBeVisible();
  });

  test('should handle infinite scroll loading', async ({ page }) => {
    await page.goto('/feed');

    // Initial items
    const initialItems = await page.getByTestId('feed-item').count();
    expect(initialItems).toBeGreaterThan(0);

    // Scroll to bottom to trigger infinite scroll
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Wait for new items to load
    await page.waitForResponse('**/api/feed?page=2');

    const updatedItems = await page.getByTestId('feed-item').count();
    expect(updatedItems).toBeGreaterThan(initialItems);
  });
});
```

## Mobile Form Testing

```typescript
import { test, expect } from '@playwright/test';

test.describe('Mobile Form Interactions', () => {
  test('should handle mobile date picker', async ({ page }) => {
    await page.goto('/booking');

    const dateInput = page.getByLabel('Check-in date');
    await dateInput.click();

    // Interact with native mobile date picker
    await dateInput.fill('2025-06-15');
    await expect(dateInput).toHaveValue('2025-06-15');
  });

  test('should support autofill on mobile forms', async ({ page }) => {
    await page.goto('/checkout');

    // Fill form fields -- mobile browsers may suggest autofill
    await page.getByLabel('Full name').fill('Jane Doe');
    await page.getByLabel('Email').fill('jane@example.com');
    await page.getByLabel('Phone').fill('+1234567890');

    // Verify autocomplete attributes are present for mobile autofill
    await expect(page.getByLabel('Full name')).toHaveAttribute('autocomplete', 'name');
    await expect(page.getByLabel('Email')).toHaveAttribute('autocomplete', 'email');
    await expect(page.getByLabel('Phone')).toHaveAttribute('autocomplete', 'tel');
  });

  test('should validate touch target sizes meet accessibility standards', async ({ page }) => {
    await page.goto('/');

    // Check that all clickable elements meet 44x44 minimum touch target
    const clickableElements = page.locator('a, button, input, select, textarea, [role="button"]');
    const count = await clickableElements.count();

    for (let i = 0; i < count; i++) {
      const element = clickableElements.nth(i);
      if (await element.isVisible()) {
        const box = await element.boundingBox();
        if (box) {
          expect(box.width, `Element ${i} width too small`).toBeGreaterThanOrEqual(44);
          expect(box.height, `Element ${i} height too small`).toBeGreaterThanOrEqual(44);
        }
      }
    }
  });
});
```

## Mobile Performance Testing

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('Mobile Performance Metrics', () => {
  test('should meet Core Web Vitals on mobile', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
    });
    const page = await context.newPage();

    // Collect performance metrics
    await page.goto('/', { waitUntil: 'networkidle' });

    const performanceMetrics = await page.evaluate(() => {
      return new Promise<{
        lcp: number;
        fid: number;
        cls: number;
        ttfb: number;
      }>((resolve) => {
        let lcp = 0;
        let cls = 0;

        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          lcp = entries[entries.length - 1].startTime;
        }).observe({ type: 'largest-contentful-paint', buffered: true });

        new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (!(entry as any).hadRecentInput) {
              cls += (entry as any).value;
            }
          }
        }).observe({ type: 'layout-shift', buffered: true });

        const navEntry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

        setTimeout(() => {
          resolve({
            lcp,
            fid: 0, // FID requires real user interaction
            cls,
            ttfb: navEntry.responseStart - navEntry.requestStart,
          });
        }, 3000);
      });
    });

    // Assert Core Web Vitals thresholds
    expect(performanceMetrics.lcp).toBeLessThan(2500); // LCP < 2.5s
    expect(performanceMetrics.cls).toBeLessThan(0.1); // CLS < 0.1
    expect(performanceMetrics.ttfb).toBeLessThan(800); // TTFB < 800ms

    await context.close();
  });

  test('should not load oversized images on mobile', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
    });
    const page = await context.newPage();

    const imageRequests: { url: string; size: number }[] = [];

    page.on('response', async (response) => {
      const contentType = response.headers()['content-type'] || '';
      if (contentType.startsWith('image/')) {
        const body = await response.body().catch(() => Buffer.alloc(0));
        imageRequests.push({
          url: response.url(),
          size: body.length,
        });
      }
    });

    await page.goto('/', { waitUntil: 'networkidle' });

    // No single image should exceed 200KB on mobile
    for (const img of imageRequests) {
      expect(img.size, `Image too large: ${img.url}`).toBeLessThan(200 * 1024);
    }

    await context.close();
  });
});
```

## Visual Regression Testing for Mobile

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('Mobile Visual Regression', () => {
  const mobileDevices = [
    { name: 'iphone-se', config: devices['iPhone SE'] },
    { name: 'iphone-14', config: devices['iPhone 14'] },
    { name: 'pixel-7', config: devices['Pixel 7'] },
    { name: 'ipad-pro', config: devices['iPad Pro 11'] },
  ];

  for (const device of mobileDevices) {
    test(`homepage visual regression on ${device.name}`, async ({ browser }) => {
      const context = await browser.newContext(device.config);
      const page = await context.newPage();

      await page.goto('/');
      await page.waitForLoadState('networkidle');

      await expect(page).toHaveScreenshot(`homepage-${device.name}.png`, {
        fullPage: true,
        maxDiffPixelRatio: 0.05,
        animations: 'disabled',
      });

      await context.close();
    });
  }

  test('should match screenshots in dark mode on mobile', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 14'],
      colorScheme: 'dark',
    });
    const page = await context.newPage();

    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage-mobile-dark.png', {
      maxDiffPixelRatio: 0.05,
    });

    await context.close();
  });
});
```

## Best Practices

1. **Always use Playwright device descriptors** -- Do not manually set viewport and user agent. Use `devices['iPhone 14']` for accurate emulation including scale factor and touch support.
2. **Test on both iOS and Android profiles** -- Safari WebKit and Chrome behave differently. Always include both iPhone and Pixel device projects.
3. **Account for the safe area** -- Modern phones have notches and rounded corners. Verify content is not obscured by safe area insets.
4. **Test both orientations** -- Many layout bugs only appear in landscape mode. Include landscape variants in your test projects.
5. **Throttle network in CI** -- Mobile users are not always on fast Wi-Fi. Run a subset of tests with slow 3G throttling to catch loading issues.
6. **Verify touch target sizes** -- All interactive elements should be at least 44x44 CSS pixels. Automate this check in your test suite.
7. **Test with reduced motion** -- Many mobile users enable reduced motion. Verify animations respect `prefers-reduced-motion` media query.
8. **Use visual regression per device** -- Capture and compare screenshots across all target devices, not just one.
9. **Test scrolling behavior** -- Verify sticky headers, infinite scroll, pull-to-refresh, and scroll-to-top work correctly on mobile.
10. **Test font scaling** -- Mobile users may increase text size in system settings. Verify layout does not break at 150% or 200% font scaling.

## Anti-Patterns to Avoid

1. **Testing only at one viewport size** -- A 375px test does not cover 320px edge cases or tablet layouts.
2. **Using mouse events instead of touch** -- `page.click()` works but does not simulate real touch behavior for gesture-dependent UIs.
3. **Ignoring device pixel ratio** -- Screenshots and visual tests must account for different `deviceScaleFactor` values.
4. **Hardcoding viewport dimensions** -- Use device descriptors instead of magic numbers like `{ width: 390, height: 844 }`.
5. **Not testing offline scenarios** -- Mobile connections drop frequently. Always verify graceful degradation.
6. **Skipping landscape orientation tests** -- Many responsive bugs only manifest in landscape mode.
7. **Testing desktop-only selectors** -- Mobile layouts often hide desktop elements and show mobile-specific components. Test the correct elements.
8. **Ignoring scroll position after navigation** -- Mobile pages should scroll to top on navigation. Verify this behavior.
9. **Not testing the virtual keyboard impact** -- Soft keyboards reduce available viewport. Ensure forms remain usable when the keyboard is open.
10. **Running all tests on all devices** -- Be strategic. Run smoke tests on all devices but detailed tests on representative devices to keep CI fast.

## Running Mobile Tests

- Run all mobile tests: `npx playwright test --config=playwright.config.ts`
- Run tests for a specific device: `npx playwright test --project=iphone-14`
- Run in headed mode to see mobile emulation: `npx playwright test --headed --project=pixel-7`
- Update visual snapshots: `npx playwright test --update-snapshots`
- Debug a mobile test: `npx playwright test --debug --project=iphone-14`
- View trace for failed test: `npx playwright show-trace test-results/trace.zip`
- Generate code with mobile emulation: `npx playwright codegen --device="iPhone 14" https://example.com`
- Run responsive breakpoint tests only: `npx playwright test tests/mobile/responsive/`
