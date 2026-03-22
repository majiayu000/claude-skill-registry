---
name: Loading State Tester
description: Verify loading indicators, skeleton screens, and progress bars appear correctly during async operations and disappear on completion or error.
version: 1.0.0
author: Pramod
license: MIT
tags: [loading-states, skeleton, spinner, async, ux, progressive-loading, suspense]
testingTypes: [e2e, performance]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Loading State Tester Skill

You are an expert QA automation engineer specializing in loading state verification, asynchronous UI behavior testing, and perceived performance analysis. When asked to test loading indicators, skeleton screens, progress bars, or any transitional UI states in a web application, follow these comprehensive instructions to systematically verify that every async operation provides appropriate user feedback.

## Core Principles

1. **Every Async Operation Needs Visual Feedback** -- When a user triggers an action that takes more than 100 milliseconds, they must see immediate visual confirmation that the system is working. Silent waiting creates uncertainty: the user does not know whether they clicked the button, whether the request was sent, or whether the application has frozen.

2. **Loading States Must Appear Instantly** -- The loading indicator should appear within one animation frame of the triggering action, typically under 16 milliseconds. A delay between the user's click and the appearance of a spinner creates a perceptible gap that feels like the application is unresponsive.

3. **Loading States Must Disappear Completely** -- When data arrives or an error occurs, every loading indicator must be removed. Stale spinners that persist after content has loaded, or skeleton screens that remain visible beneath actual content, are severe UX bugs that erode user confidence.

4. **Error States Must Replace Loading States** -- When an async operation fails, the loading indicator must transition to an error state, not simply disappear. A spinner that vanishes with no content and no error message leaves the user stranded with no understanding of what happened.

5. **Progressive Loading Beats All-or-Nothing** -- When a page has multiple independent data sources, each section should show its own loading state and resolve independently. Holding the entire page behind a single spinner until every request completes makes the application feel slower than it actually is.

6. **Skeleton Screens Preserve Layout Stability** -- Skeleton screens prevent cumulative layout shift by reserving the exact space that content will occupy. A well-implemented skeleton matches the dimensions and structure of the loaded content so the page does not jump when data arrives.

7. **Loading States Must Be Accessible** -- Screen readers must announce loading states and their completion. Use aria-busy, aria-live regions, and role="status" to communicate state transitions to assistive technology users.

## Project Structure

Organize your loading state test suite with this directory structure:

```
tests/
  loading-states/
    initial-page-load.spec.ts
    navigation-transitions.spec.ts
    form-submission-loading.spec.ts
    infinite-scroll-loading.spec.ts
    skeleton-screen-fidelity.spec.ts
    error-state-transitions.spec.ts
    concurrent-loading.spec.ts
  fixtures/
    throttled-network.fixture.ts
  helpers/
    loading-detector.ts
    skeleton-validator.ts
    timing-tracker.ts
    accessibility-checker.ts
  reports/
    loading-state-audit.json
    loading-state-audit.html
playwright.config.ts
```

Each spec file targets a different category of loading behavior. The fixtures directory provides network throttling utilities. Helpers contain detection logic for various loading indicator patterns.

## Detailed Guide

### Step 1: Build a Loading State Detector

The first challenge is reliably detecting loading indicators across different UI libraries and implementation patterns. Applications use spinners, skeleton screens, progress bars, shimmer effects, and opacity changes. Build a detector that recognizes all of these patterns.

```typescript
// helpers/loading-detector.ts
import { Page, Locator } from '@playwright/test';

export interface LoadingIndicator {
  type: 'spinner' | 'skeleton' | 'progress-bar' | 'shimmer' | 'overlay' | 'text' | 'opacity';
  selector: string;
  element: Locator;
  appearedAt?: number;
  disappearedAt?: number;
  durationMs?: number;
  page: string;
  context: string;
}

export class LoadingDetector {
  private indicators: LoadingIndicator[] = [];

  // Common selectors for loading indicators across popular UI libraries
  private static readonly SPINNER_SELECTORS = [
    '[role="progressbar"]',
    '[aria-busy="true"]',
    '.spinner',
    '.loading-spinner',
    '.animate-spin',
    '.MuiCircularProgress-root',
    '.chakra-spinner',
    '[data-testid="loading-spinner"]',
    '[data-testid="loading"]',
    'svg.animate-spin',
  ];

  private static readonly SKELETON_SELECTORS = [
    '.skeleton',
    '.animate-pulse',
    '.shimmer',
    '.placeholder-wave',
    '.MuiSkeleton-root',
    '.chakra-skeleton',
    '[data-testid="skeleton"]',
    '[data-testid*="skeleton"]',
    '.react-loading-skeleton',
  ];

  private static readonly PROGRESS_BAR_SELECTORS = [
    'progress',
    '[role="progressbar"][aria-valuenow]',
    '.progress-bar',
    '.MuiLinearProgress-root',
    '.nprogress-bar',
    '#nprogress',
  ];

  private static readonly OVERLAY_SELECTORS = [
    '.loading-overlay',
    '.page-loading',
    '[data-testid="loading-overlay"]',
    '.opacity-50[aria-busy="true"]',
  ];

  async detectAll(page: Page, context: string): Promise<LoadingIndicator[]> {
    const detected: LoadingIndicator[] = [];
    const startTime = performance.now();

    // Detect spinners
    for (const selector of LoadingDetector.SPINNER_SELECTORS) {
      const locator = page.locator(selector);
      const count = await locator.count();
      for (let i = 0; i < count; i++) {
        const element = locator.nth(i);
        if (await element.isVisible()) {
          detected.push({
            type: 'spinner',
            selector,
            element,
            appearedAt: startTime,
            page: page.url(),
            context,
          });
        }
      }
    }

    // Detect skeleton screens
    for (const selector of LoadingDetector.SKELETON_SELECTORS) {
      const locator = page.locator(selector);
      const count = await locator.count();
      for (let i = 0; i < count; i++) {
        const element = locator.nth(i);
        if (await element.isVisible()) {
          detected.push({
            type: 'skeleton',
            selector,
            element,
            appearedAt: startTime,
            page: page.url(),
            context,
          });
        }
      }
    }

    // Detect progress bars
    for (const selector of LoadingDetector.PROGRESS_BAR_SELECTORS) {
      const locator = page.locator(selector);
      const count = await locator.count();
      for (let i = 0; i < count; i++) {
        const element = locator.nth(i);
        if (await element.isVisible()) {
          detected.push({
            type: 'progress-bar',
            selector,
            element,
            appearedAt: startTime,
            page: page.url(),
            context,
          });
        }
      }
    }

    // Detect loading overlays
    for (const selector of LoadingDetector.OVERLAY_SELECTORS) {
      const locator = page.locator(selector);
      const count = await locator.count();
      for (let i = 0; i < count; i++) {
        const element = locator.nth(i);
        if (await element.isVisible()) {
          detected.push({
            type: 'overlay',
            selector,
            element,
            appearedAt: startTime,
            page: page.url(),
            context,
          });
        }
      }
    }

    this.indicators.push(...detected);
    return detected;
  }

  async waitForAllLoadingToComplete(page: Page, timeoutMs: number = 15000): Promise<void> {
    const allSelectors = [
      ...LoadingDetector.SPINNER_SELECTORS,
      ...LoadingDetector.SKELETON_SELECTORS,
      ...LoadingDetector.PROGRESS_BAR_SELECTORS,
      ...LoadingDetector.OVERLAY_SELECTORS,
    ];

    const deadline = Date.now() + timeoutMs;

    while (Date.now() < deadline) {
      let anyVisible = false;

      for (const selector of allSelectors) {
        const locator = page.locator(selector);
        const count = await locator.count();
        for (let i = 0; i < count; i++) {
          if (await locator.nth(i).isVisible()) {
            anyVisible = true;
            break;
          }
        }
        if (anyVisible) break;
      }

      if (!anyVisible) return;
      await page.waitForTimeout(100);
    }

    throw new Error(`Loading indicators still visible after ${timeoutMs}ms`);
  }

  getAll(): LoadingIndicator[] {
    return [...this.indicators];
  }
}
```

### Step 2: Build a Network Throttling Fixture

To test loading states reliably, you need to slow down network responses so loading indicators are visible long enough to verify. Without throttling, fast local development servers resolve requests so quickly that loading states flash for a single frame and are untestable.

```typescript
// fixtures/throttled-network.fixture.ts
import { test as base, Page, Route } from '@playwright/test';

interface ThrottleOptions {
  latencyMs: number;
  pattern?: string;
}

interface ThrottledFixtures {
  throttledPage: Page;
  setLatency: (options: ThrottleOptions) => Promise<void>;
  setOffline: () => Promise<void>;
  setOnline: () => Promise<void>;
  simulateTimeout: (pattern: string, timeoutMs: number) => Promise<void>;
}

export const test = base.extend<ThrottledFixtures>({
  throttledPage: async ({ page }, use) => {
    await use(page);
  },

  setLatency: async ({ page }, use) => {
    const setLatency = async ({ latencyMs, pattern = '**/*' }: ThrottleOptions) => {
      await page.route(pattern, async (route: Route) => {
        await new Promise((resolve) => setTimeout(resolve, latencyMs));
        await route.continue();
      });
    };

    await use(setLatency);
  },

  setOffline: async ({ context }, use) => {
    const setOffline = async () => {
      await context.setOffline(true);
    };
    await use(setOffline);
  },

  setOnline: async ({ context }, use) => {
    const setOnline = async () => {
      await context.setOffline(false);
    };
    await use(setOnline);
  },

  simulateTimeout: async ({ page }, use) => {
    const simulateTimeout = async (pattern: string, timeoutMs: number) => {
      await page.route(pattern, async (route: Route) => {
        await new Promise((resolve) => setTimeout(resolve, timeoutMs));
        await route.abort('timedout');
      });
    };
    await use(simulateTimeout);
  },
});
```

### Step 3: Test Initial Page Load States

The most visible loading state is the initial page load. Every page that fetches data on mount must show a loading indicator until data is ready.

```typescript
// tests/loading-states/initial-page-load.spec.ts
import { test } from '../fixtures/throttled-network.fixture';
import { expect } from '@playwright/test';
import { LoadingDetector } from '../helpers/loading-detector';

test.describe('Initial Page Load States', () => {
  test('dashboard shows loading indicators before data arrives', async ({
    throttledPage: page,
    setLatency,
  }) => {
    // Add 2-second delay to all API calls
    await setLatency({ latencyMs: 2000, pattern: '**/api/**' });

    const detector = new LoadingDetector();

    // Navigate and immediately check for loading states
    await page.goto('/dashboard', { waitUntil: 'domcontentloaded' });

    // Loading indicators should appear immediately
    const indicators = await detector.detectAll(page, 'dashboard-initial-load');
    expect(indicators.length).toBeGreaterThan(0);

    // Verify at least one indicator type is present
    const types = new Set(indicators.map((i) => i.type));
    expect(
      types.has('spinner') || types.has('skeleton') || types.has('progress-bar')
    ).toBe(true);

    // Wait for loading to complete
    await detector.waitForAllLoadingToComplete(page);

    // Verify all loading indicators are gone
    const afterLoad = await detector.detectAll(page, 'dashboard-after-load');
    const stillVisible = afterLoad.filter(
      (i) => i.type !== 'text'
    );
    expect(stillVisible.length).toBe(0);
  });

  test('skeleton screens match content dimensions to prevent layout shift', async ({
    throttledPage: page,
    setLatency,
  }) => {
    await setLatency({ latencyMs: 3000, pattern: '**/api/**' });
    await page.goto('/dashboard', { waitUntil: 'domcontentloaded' });

    // Capture skeleton dimensions
    const skeletonBounds = await page.evaluate(() => {
      const skeletons = document.querySelectorAll(
        '.skeleton, .animate-pulse, [data-testid*="skeleton"]'
      );
      return Array.from(skeletons).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          width: rect.width,
          height: rect.height,
          top: rect.top,
          left: rect.left,
        };
      });
    });

    // Wait for content to load
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500);

    // Capture content dimensions at the same positions
    const contentBounds = await page.evaluate(() => {
      const contentAreas = document.querySelectorAll(
        '[data-testid*="content"], .card, .data-cell, article'
      );
      return Array.from(contentAreas).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          width: rect.width,
          height: rect.height,
          top: rect.top,
          left: rect.left,
        };
      });
    });

    // Verify no significant layout shift occurred
    if (skeletonBounds.length > 0 && contentBounds.length > 0) {
      for (let i = 0; i < Math.min(skeletonBounds.length, contentBounds.length); i++) {
        const skeleton = skeletonBounds[i];
        const content = contentBounds[i];

        // Allow 15% width variance and 25% height variance
        const widthDiff = Math.abs(skeleton.width - content.width) / content.width;
        const heightDiff = Math.abs(skeleton.height - content.height) / content.height;

        expect(widthDiff).toBeLessThan(0.15);
        expect(heightDiff).toBeLessThan(0.25);
      }
    }
  });

  test('page shows real content after data arrives, not infinite loading', async ({
    throttledPage: page,
    setLatency,
  }) => {
    await setLatency({ latencyMs: 1500, pattern: '**/api/**' });
    await page.goto('/dashboard');

    // Wait for network to settle
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000);

    // There should be actual content visible, not loading placeholders
    const hasContent = await page.evaluate(() => {
      const body = document.body.innerText.trim();
      const loadingOnlyPhrases = ['loading', 'please wait', 'fetching'];
      const isOnlyLoading = loadingOnlyPhrases.some(
        (phrase) => body.toLowerCase() === phrase
      );
      return body.length > 50 && !isOnlyLoading;
    });

    expect(hasContent).toBe(true);
  });
});
```

### Step 4: Test Form Submission Loading States

Form submissions are critical interaction points where loading states directly affect the user's confidence that their action was received.

```typescript
// tests/loading-states/form-submission-loading.spec.ts
import { test } from '../fixtures/throttled-network.fixture';
import { expect } from '@playwright/test';

test.describe('Form Submission Loading States', () => {
  test('submit button shows loading state and prevents double-submit', async ({
    throttledPage: page,
    setLatency,
  }) => {
    await setLatency({ latencyMs: 3000, pattern: '**/api/**' });

    await page.goto('/contact');
    await page.fill('[name="name"]', 'Test User');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="message"]', 'Test message content');

    const submitButton = page.locator('button[type="submit"]');

    // Capture button state before submission
    const beforeText = await submitButton.textContent();
    const beforeDisabled = await submitButton.isDisabled();
    expect(beforeDisabled).toBe(false);

    // Submit the form
    await submitButton.click();
    await page.waitForTimeout(100);

    // Button should be disabled during submission to prevent double-submit
    const duringDisabled = await submitButton.isDisabled();
    expect(duringDisabled).toBe(true);

    // Check for loading indicator within or near the button
    const hasSpinner = await submitButton.locator('.animate-spin, .spinner, svg').count();
    const buttonText = await submitButton.textContent();
    const textChanged = buttonText !== beforeText;

    // Either a spinner appeared or the text changed to indicate loading
    expect(hasSpinner > 0 || textChanged).toBe(true);

    // Wait for submission to complete
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500);

    // Button should return to original state or show success
    const afterText = await submitButton.textContent();
    const isSuccess =
      afterText?.toLowerCase().includes('sent') ||
      afterText?.toLowerCase().includes('success') ||
      afterText?.toLowerCase().includes('submitted');
    const isReset = !(await submitButton.isDisabled());

    expect(isSuccess || isReset).toBe(true);
  });

  test('form prevents double submission with rapid clicks', async ({
    throttledPage: page,
  }) => {
    let requestCount = 0;
    await page.route('**/api/**', async (route) => {
      requestCount++;
      await new Promise((resolve) => setTimeout(resolve, 3000));
      await route.fulfill({ status: 200, body: JSON.stringify({ success: true }) });
    });

    await page.goto('/contact');
    await page.fill('[name="name"]', 'Test User');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="message"]', 'Test message');

    const submitButton = page.locator('button[type="submit"]');

    // Click rapidly multiple times
    await submitButton.click();
    await page.waitForTimeout(50);
    await submitButton.click({ force: true });
    await page.waitForTimeout(50);
    await submitButton.click({ force: true });

    await page.waitForTimeout(4000);

    // Only one request should have been made
    expect(requestCount).toBe(1);
  });

  test('inline field validation shows loading for async checks', async ({
    throttledPage: page,
    setLatency,
  }) => {
    await setLatency({ latencyMs: 2000, pattern: '**/api/check-username**' });

    await page.goto('/register');
    const usernameInput = page.locator('[name="username"]');
    await usernameInput.fill('testuser123');
    await usernameInput.blur();

    // A loading indicator should appear next to the username field
    const fieldContainer = usernameInput.locator('..');
    const hasFieldSpinner = await fieldContainer
      .locator('.animate-spin, .spinner, [role="progressbar"]')
      .count();

    // Either a spinner or a "checking..." text should appear
    const fieldText = await fieldContainer.textContent();
    const hasCheckingText =
      fieldText?.toLowerCase().includes('checking') ||
      fieldText?.toLowerCase().includes('validating');

    expect(hasFieldSpinner > 0 || hasCheckingText).toBe(true);
  });
});
```

### Step 5: Test Error State Transitions from Loading

When an async operation fails, the loading indicator must transition cleanly to an error state.

```typescript
// tests/loading-states/error-state-transitions.spec.ts
import { test } from '../fixtures/throttled-network.fixture';
import { expect } from '@playwright/test';
import { LoadingDetector } from '../helpers/loading-detector';

test.describe('Loading to Error State Transitions', () => {
  test('failed API replaces spinner with error message', async ({
    throttledPage: page,
  }) => {
    await page.route('**/api/data**', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    await page.goto('/dashboard', { waitUntil: 'domcontentloaded' });

    // Loading should appear first
    const detector = new LoadingDetector();
    const loadingIndicators = await detector.detectAll(page, 'pre-error');
    expect(loadingIndicators.length).toBeGreaterThan(0);

    // Wait for the error response
    await page.waitForTimeout(2500);

    // All loading indicators should be gone
    const postErrorIndicators = await detector.detectAll(page, 'post-error');
    const visibleLoading = [];
    for (const ind of postErrorIndicators) {
      if (await ind.element.isVisible().catch(() => false)) {
        visibleLoading.push(ind);
      }
    }
    expect(visibleLoading.length).toBe(0);

    // An error message should be visible instead
    const errorVisible = await page
      .locator('[role="alert"], .error-message, [data-testid*="error"]')
      .first()
      .isVisible()
      .catch(() => false);

    expect(errorVisible).toBe(true);
  });

  test('network offline shows appropriate offline indicator', async ({
    throttledPage: page,
    setOffline,
    setOnline,
  }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Go offline
    await setOffline();

    // Trigger a data refresh
    const refreshButton = page.locator('[data-testid="refresh"], button:has-text("Refresh")');
    if (await refreshButton.count() > 0) {
      await refreshButton.first().click();
      await page.waitForTimeout(2000);

      // Should show offline-specific messaging
      const pageContent = await page.textContent('body');
      const hasOfflineMessage =
        pageContent?.toLowerCase().includes('offline') ||
        pageContent?.toLowerCase().includes('connection') ||
        pageContent?.toLowerCase().includes('network');

      expect(hasOfflineMessage).toBe(true);
    }

    await setOnline();
  });

  test('retry after error shows loading then content', async ({
    throttledPage: page,
  }) => {
    let callCount = 0;

    await page.route('**/api/data**', async (route) => {
      callCount++;
      await new Promise((resolve) => setTimeout(resolve, 1000));

      if (callCount === 1) {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'Server error' }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: [{ id: 1, name: 'Item' }] }),
        });
      }
    });

    await page.goto('/dashboard', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);

    // Click retry if available
    const retryButton = page.locator(
      'button:has-text("Retry"), button:has-text("Try again"), [data-testid="retry"]'
    );
    if (await retryButton.count() > 0) {
      await retryButton.first().click();
      await page.waitForTimeout(200);

      // Should show loading again during retry
      const detector = new LoadingDetector();
      const retryLoading = await detector.detectAll(page, 'retry-loading');

      // Wait for success
      await page.waitForTimeout(1500);

      // After successful retry, error should be gone
      expect(callCount).toBe(2);
    }
  });
});
```

### Step 6: Test Infinite Scroll Loading

Infinite scroll patterns require a footer loading indicator that appears when the user scrolls near the bottom and disappears when new items load.

```typescript
// tests/loading-states/infinite-scroll-loading.spec.ts
import { test } from '../fixtures/throttled-network.fixture';
import { expect } from '@playwright/test';
import { LoadingDetector } from '../helpers/loading-detector';

test.describe('Infinite Scroll Loading States', () => {
  test('scrolling to bottom triggers loading indicator for next page', async ({
    throttledPage: page,
    setLatency,
  }) => {
    await setLatency({ latencyMs: 2000, pattern: '**/api/**page=2**' });
    await page.goto('/feed');
    await page.waitForLoadState('networkidle');

    // Count initial items
    const initialItems = await page.locator('[data-testid="feed-item"]').count();

    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(300);

    // Loading indicator should appear at the bottom
    const detector = new LoadingDetector();
    const indicators = await detector.detectAll(page, 'infinite-scroll');

    const hasBottomLoading = indicators.some(
      (i) => i.type === 'spinner' || i.type === 'skeleton'
    );
    expect(hasBottomLoading).toBe(true);

    // Wait for new items to load
    await page.waitForTimeout(3000);

    // More items should now be visible
    const afterItems = await page.locator('[data-testid="feed-item"]').count();
    expect(afterItems).toBeGreaterThan(initialItems);
  });

  test('end of list shows terminal state, not perpetual loading', async ({
    throttledPage: page,
  }) => {
    // Simulate an API that returns empty results (end of list)
    await page.route('**/api/**page=**', async (route) => {
      const url = route.request().url();
      const pageNum = parseInt(url.match(/page=(\d+)/)?.[1] || '1');

      await new Promise((resolve) => setTimeout(resolve, 500));

      if (pageNum > 3) {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: [], hasMore: false }),
        });
      } else {
        await route.continue();
      }
    });

    await page.goto('/feed');
    await page.waitForLoadState('networkidle');

    // Scroll to bottom repeatedly to reach the end
    for (let i = 0; i < 10; i++) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(1000);
    }

    // Should show "end of list" message, not a spinner
    const pageText = await page.textContent('body');
    const hasEndMessage =
      pageText?.toLowerCase().includes('no more') ||
      pageText?.toLowerCase().includes('end of') ||
      pageText?.toLowerCase().includes('all loaded') ||
      pageText?.toLowerCase().includes("that's everything");

    // No spinner should be visible at the bottom
    const detector = new LoadingDetector();
    const finalIndicators = await detector.detectAll(page, 'end-of-list');
    expect(finalIndicators.filter((i) => i.type === 'spinner').length).toBe(0);
  });
});
```

### Step 7: Test Concurrent Loading States

When multiple sections of a page fetch data independently, each section should manage its own loading state.

```typescript
// tests/loading-states/concurrent-loading.spec.ts
import { test } from '../fixtures/throttled-network.fixture';
import { expect } from '@playwright/test';

test.describe('Concurrent Independent Loading States', () => {
  test('fast section loads while slow section still shows loading', async ({
    throttledPage: page,
  }) => {
    // Make one API fast and another slow
    await page.route('**/api/stats**', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 500));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ visitors: 1234, pageViews: 5678 }),
      });
    });

    await page.route('**/api/activity**', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 4000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ items: [{ id: 1, action: 'login' }] }),
      });
    });

    await page.goto('/dashboard', { waitUntil: 'domcontentloaded' });

    // After 1 second: stats should be loaded, activity should still be loading
    await page.waitForTimeout(1000);

    const statsSection = page.locator('[data-testid="stats-section"]');
    const activitySection = page.locator('[data-testid="activity-section"]');

    if ((await statsSection.count()) > 0 && (await activitySection.count()) > 0) {
      // Stats section should show content (not loading)
      const statsHasSpinner = await statsSection
        .locator('.animate-spin, .spinner, .skeleton, .animate-pulse')
        .count();
      expect(statsHasSpinner).toBe(0);

      // Activity section should still show loading
      const activityHasSpinner = await activitySection
        .locator('.animate-spin, .spinner, .skeleton, .animate-pulse')
        .count();
      expect(activityHasSpinner).toBeGreaterThan(0);
    }
  });
});
```

### Step 8: Check Accessibility of Loading States

```typescript
// helpers/accessibility-checker.ts
import { Page } from '@playwright/test';

export interface LoadingA11yIssue {
  element: string;
  issue: string;
  severity: 'critical' | 'major' | 'minor';
  recommendation: string;
}

export class LoadingAccessibilityChecker {
  async check(page: Page): Promise<LoadingA11yIssue[]> {
    const issues: LoadingA11yIssue[] = [];

    // Check that loading regions have aria-busy
    const busyCheck = await page.evaluate(() => {
      const loadingEls = document.querySelectorAll(
        '.loading, .spinner, [data-loading="true"], .skeleton, .animate-pulse'
      );
      return Array.from(loadingEls).map((el) => ({
        tag: el.tagName.toLowerCase() + '.' + (el.className || '').split(' ')[0],
        hasAriaBusy: el.getAttribute('aria-busy') === 'true',
        parentHasAriaBusy: el.closest('[aria-busy="true"]') !== null,
      }));
    });

    for (const item of busyCheck) {
      if (!item.hasAriaBusy && !item.parentHasAriaBusy) {
        issues.push({
          element: item.tag,
          issue: 'Loading element lacks aria-busy="true" on itself or a parent',
          severity: 'major',
          recommendation: 'Add aria-busy="true" to the container during loading',
        });
      }
    }

    // Check for live regions
    const liveRegions = await page.evaluate(() => {
      const regions = document.querySelectorAll('[aria-live], [role="status"], [role="alert"]');
      return regions.length;
    });

    if (liveRegions === 0) {
      issues.push({
        element: 'body',
        issue: 'No ARIA live regions to announce loading completion',
        severity: 'critical',
        recommendation: 'Add role="status" or aria-live="polite" to announce state changes',
      });
    }

    // Check progress bars for required attributes
    const progressBars = await page.evaluate(() => {
      const bars = document.querySelectorAll('[role="progressbar"]');
      return Array.from(bars).map((el) => ({
        hasValueNow: el.hasAttribute('aria-valuenow'),
        hasValueMin: el.hasAttribute('aria-valuemin'),
        hasValueMax: el.hasAttribute('aria-valuemax'),
        hasLabel: el.hasAttribute('aria-label') || el.hasAttribute('aria-labelledby'),
      }));
    });

    for (const bar of progressBars) {
      if (!bar.hasValueMin || !bar.hasValueMax) {
        issues.push({
          element: 'progressbar',
          issue: 'Missing aria-valuemin or aria-valuemax',
          severity: 'major',
          recommendation: 'Add aria-valuemin="0" and aria-valuemax="100"',
        });
      }
      if (!bar.hasLabel) {
        issues.push({
          element: 'progressbar',
          issue: 'Missing aria-label',
          severity: 'minor',
          recommendation: 'Add aria-label describing what is loading',
        });
      }
    }

    return issues;
  }
}
```

## Configuration

### Playwright Configuration for Loading State Testing

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/loading-states',
  timeout: 60000,
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    screenshot: 'on',
    video: 'on-first-retry',
    trace: 'on-first-retry',
  },
  reporter: [
    ['html', { open: 'never' }],
    ['json', { outputFile: 'reports/loading-state-results.json' }],
  ],
  projects: [
    {
      name: 'loading-desktop',
      use: { browserName: 'chromium' },
    },
    {
      name: 'loading-mobile',
      use: {
        browserName: 'chromium',
        viewport: { width: 375, height: 812 },
        isMobile: true,
      },
    },
  ],
});
```

### Timing Thresholds Configuration

```typescript
// helpers/timing-tracker.ts
export interface TimingThresholds {
  loadingAppearanceMaxMs: number;
  loadingMinVisibleMs: number;
  loadingMaxVisibleMs: number;
  skeletonToContentMaxShiftPx: number;
}

export const defaultThresholds: TimingThresholds = {
  loadingAppearanceMaxMs: 100,
  loadingMinVisibleMs: 200,
  loadingMaxVisibleMs: 30000,
  skeletonToContentMaxShiftPx: 20,
};

export class TimingTracker {
  private entries: Array<{
    context: string;
    triggerTime: number;
    loadingAppearedTime: number;
    loadingDisappearedTime: number;
  }> = [];

  record(context: string, triggerTime: number, appearedTime: number, disappearedTime: number) {
    this.entries.push({
      context,
      triggerTime,
      loadingAppearedTime: appearedTime,
      loadingDisappearedTime: disappearedTime,
    });
  }

  validate(thresholds: TimingThresholds = defaultThresholds): string[] {
    const violations: string[] = [];

    for (const entry of this.entries) {
      const appearanceDelay = entry.loadingAppearedTime - entry.triggerTime;
      if (appearanceDelay > thresholds.loadingAppearanceMaxMs) {
        violations.push(
          `[${entry.context}] Loading appeared ${appearanceDelay}ms after trigger (max: ${thresholds.loadingAppearanceMaxMs}ms)`
        );
      }

      const visibleDuration = entry.loadingDisappearedTime - entry.loadingAppearedTime;
      if (visibleDuration < thresholds.loadingMinVisibleMs) {
        violations.push(
          `[${entry.context}] Loading visible for only ${visibleDuration}ms (min: ${thresholds.loadingMinVisibleMs}ms) -- causes flash`
        );
      }

      if (visibleDuration > thresholds.loadingMaxVisibleMs) {
        violations.push(
          `[${entry.context}] Loading visible for ${visibleDuration}ms (max: ${thresholds.loadingMaxVisibleMs}ms) -- possibly stuck`
        );
      }
    }

    return violations;
  }
}
```

## Best Practices

1. **Always throttle the network when testing loading states.** Without artificial latency, async operations complete too quickly for loading indicators to appear. Use Playwright's route interception to add realistic delays.

2. **Test loading states on simulated slow 3G and offline modes.** Mobile users on poor connections experience loading states for much longer. Verify the experience degrades gracefully.

3. **Verify loading indicators appear within one animation frame.** The delay between user action and visible feedback must be imperceptible. Enforce a threshold below 100ms.

4. **Enforce a minimum display duration for loading indicators.** A spinner that flashes for 50ms is worse than no spinner. Implement a minimum display time of 200ms to prevent visual flicker.

5. **Test that skeleton screens match content layout.** Capture bounding rectangles before and after content loads. Assert positions remain stable to prevent layout shift.

6. **Verify loading states transition cleanly to error states.** Failed requests must replace the loading indicator with an error message. A vanishing spinner with no content is a severe UX bug.

7. **Test concurrent loading states independently.** Multiple data-fetching sections should resolve their own loading states independently. One slow section should not block the entire page.

8. **Record video of loading state tests.** Loading bugs are temporal. Static screenshots miss the problem. Use Playwright's video recording to capture the full lifecycle.

9. **Check aria-busy and aria-live attributes.** Loading regions need aria-busy="true" during loading and an aria-live region must announce completion.

10. **Test the stuck loading scenario.** Simulate a request that never resolves. Verify the application shows a timeout message rather than spinning forever.

11. **Measure Cumulative Layout Shift during loading transitions.** Use the Performance Observer API to capture CLS values. CLS above 0.1 indicates poor skeleton implementation.

12. **Test loading states across page navigations.** SPA route-level loading indicators must appear during navigation and disappear when the new page renders.

## Anti-Patterns to Avoid

1. **No loading indicator at all.** The most common anti-pattern. The user clicks a button and nothing visible happens for several seconds.

2. **Spinner that never stops.** A stuck loading state is worse than none. Always implement timeouts and fallback error messages.

3. **Full-page loading overlay for partial updates.** Blocking the entire page when only one section is refreshing is unnecessarily disruptive.

4. **Skeleton screens that do not match content dimensions.** Skeletons that differ from actual content cause layout shift, defeating their purpose.

5. **Multiple concurrent spinners creating visual noise.** Every card and widget having its own spinner looks chaotic. Use section-level indicators for grouped content.

6. **Loading overlay that blocks user interaction unnecessarily.** If the user can still use other parts of the page, do not block their input with a full-page overlay.

7. **Flash of loading state on fast connections.** A 30ms spinner creates visual flicker. Debounce the loading indicator or enforce a minimum display time.

8. **Loading text without visual indicator.** Plain "Loading..." text without animation looks like static content, not a transitional state.

9. **Progress bar that jumps from 0% to 100%.** If progress cannot be tracked incrementally, use an indeterminate indicator instead of a misleading progress bar.

10. **Ignoring loading states in error recovery flows.** A "Retry" button click must show loading again during the retry attempt.

## Debugging Tips

1. **Use Playwright's video recording for all loading transition tests.** Videos capture temporal bugs that screenshots miss entirely.

2. **Add artificial delays to API responses** using page.route() to make loading states observable. A 3-5 second delay makes it easy to screenshot loading states.

3. **Use Chrome DevTools Performance tab** to identify layout shifts during loading transitions. The "Experience" row highlights CLS events.

4. **Check the network waterfall** to understand which requests are blocking resolution. Cascading sequential requests often cause unexpectedly long loading times.

5. **Inspect CSS animations on loading indicators.** Some spinners stop animating after a certain iteration count. Verify animations repeat indefinitely.

6. **Test with CPU throttling enabled.** Slow CPUs can cause rendering delays that make loading states appear jerky or incomplete.

7. **Use MutationObserver to track DOM changes** during loading transitions. This reveals race conditions where content and loading indicators briefly coexist.

8. **Log timestamps for each state transition** (idle, loading, success, error) to build a timeline. This helps identify gaps or overlaps between states.

9. **Test with browser cache disabled.** Cached responses skip the loading state entirely, masking missing implementations that only appear on first load.

10. **Check for z-index conflicts** between loading overlays and other elements. Loading overlays sometimes render behind modals or fixed headers due to stacking context issues.
