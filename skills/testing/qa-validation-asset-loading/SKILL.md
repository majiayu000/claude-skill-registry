---
name: qa-validation-asset-loading
description: Asset loading performance validation using Playwright. Use when validating FBX model loading performance and memory usage, testing asset loading across different environments, ensuring proper error handling for failed asset loads, or verifying browser compatibility for asset formats.
category: validation
---

# Asset Loading Validation

## When to Use

- Validating FBX model loading performance and memory usage
- Testing asset loading across different environments
- Ensuring proper error handling for failed asset loads
- Verifying browser compatibility for asset formats

## Quick Start

### Asset Loading Performance Test

```typescript
// playwright.config.ts
export default defineConfig({
  // ... other config
  expect: {
    toHaveScreenshot: {
      maxPixelRatio: 1,
      threshold: 0.1,
    },
  },
});

// test/asset-loading.spec.ts
import { test, expect } from '../fixtures';

test.describe('Asset Loading Validation', () => {
  test('Sequential FBX model loading', async ({ page }) => {
    await page.goto('/');

    // Monitor memory usage during loading
    const memoryUsage = await page.evaluate(() => {
      return {
        jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
        totalJSHeapSize: performance.memory.totalJSHeapSize,
        usedJSHeapSize: performance.memory.usedJSHeapSize,
      };
    });

    // Check for loading indicators
    await expect(page.locator('.loading-indicator')).toBeVisible();

    // Wait for loading complete
    await expect(page.locator('.loading-indicator')).toBeHidden();

    // Verify models are loaded
    await expect(page.locator('canvas')).toBeVisible();
    await expect(page.locator('[data-testid="character-model"]')).toHaveCount(6);

    // Performance assertions
    const afterLoadMemory = await page.evaluate(() => performance.memory.usedJSHeapSize);
    const memoryIncrease = afterLoadMemory - memoryUsage.usedJSHeapSize;

    expect(memoryIncrease).toBeLessThan(100 * 1024 * 1024); // Less than 100MB increase
  });

  test('Error handling for missing assets', async ({ page }) => {
    await page.goto('/test-error-loading');

    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('Failed to load character');

    // Console check for errors
    const consoleLogs = await page.evaluate(() => {
      return (window as any).__consoleLogs || [];
    });

    expect(consoleLogs).not.toContain('error');
    expect(consoleLogs).toContain('asset loading failed');
  });
});
```

### Browser Compatibility Test

```typescript
test.describe('Cross-Browser Asset Loading', () => {
  ['chromium', 'firefox', 'webkit'].forEach((browserName) => {
    test(`Asset loading in ${browserName}`, async ({ page }) => {
      await page.goto('/');

      // Wait for initial load
      await page.waitForLoadState('networkidle');

      // Test asset loading in different browsers
      const assetResponses = await page.waitForResponse((response) =>
        response.url().includes('/assets/')
      );

      expect(assetResponses.status()).toBe(200);

      // Visual regression check
      await expect(page).toHaveScreenshot(`asset-loading-${browserName}.png`, {
        maxDiffPixels: 100,
      });
    });
  });
});
```

## Anti-Patterns

❌ **DON'T:** Only test assets in development environment

```typescript
// Bad - Only tests local development
test('Asset loading', async ({ page }) => {
  await page.goto('http://localhost:3000'); // E2E tests use baseURL from playwright.config.ts
  // ... tests
});
```

✅ **DO:** Test in multiple environments with different configurations

```typescript
// Good - Tests multiple environments
[process.env.TEST_ENV].forEach((env) => {
  test(`Asset loading in ${env}`, async ({ page }) => {
    const baseUrl = env === 'production' ? 'https://your-game.com' : 'http://localhost:3000';

    await page.goto(`${baseUrl}/characters`);
    // ... environment-specific tests
  });
});
```

❌ **DON'T:** Ignore memory usage during asset loading

```typescript
// Bad - No memory monitoring
test('Load models', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('[data-testid="model-loaded"]');
  // No memory checks
});
```

✅ **DO:** Monitor memory and performance metrics

```typescript
test('Memory-safe asset loading', async ({ page }) => {
  const initialMemory = await page.evaluate(() => {
    return performance.memory?.usedJSHeapSize || 0;
  });

  await page.goto('/characters');
  await page.waitForSelector('[data-testid="all-models-loaded"]');

  const finalMemory = await page.evaluate(() => {
    return performance.memory?.usedJSHeapSize || 0;
  });

  const memoryIncrease = finalMemory - initialMemory;
  expect(memoryIncrease).toBeLessThan(50 * 1024 * 1024); // 50MB limit

  // Check for memory leaks
  await page.waitForTimeout(5000);
  const afterWaitMemory = await page.evaluate(() => {
    return performance.memory?.usedJSHeapSize || 0;
  });

  expect(afterWaitMemory - finalMemory).toBeLessThan(5 * 1024 * 1024); // < 5MB after 5s
});
```

## Performance Validation Patterns

### Load Time Measurement

```typescript
test.describe('Asset Loading Performance', () => {
  test('Sequential loading load time', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/characters');
    await page.waitForSelector('[data-testid="all-characters-loaded"]');

    const loadTime = Date.now() - startTime;

    // Assert load time is reasonable
    expect(loadTime).toBeLessThan(10000); // 10 seconds max

    // Check loading progress
    const progressHistory = await page.evaluate(() => {
      return (window as any).__progressLog || [];
    });

    expect(progressHistory.length).toBeGreaterThan(0);
    expect(progressHistory[progressHistory.length - 1]).toBe(100);
  });
});
```

### Resource Usage Monitoring

```typescript
test('GPU memory usage during loading', async ({ page }) => {
  // Note: This requires browser extensions or specific APIs
  const gpuInfo = await page.evaluate(() => {
    return (navigator as any).gpu?.memoryInfo || {};
  });

  expect(gpuInfo.totalAvailableVram).toBeGreaterThan(0);
  expect(gpuInfo.usedVram).toBeLessThan(gpuInfo.totalAvailableVram * 0.8);
});
```

## Error Handling Validation

### Error Recovery Test

```typescript
test.describe('Asset Loading Error Handling', () => {
  test('Graceful handling of missing assets', async ({ page }) => {
    // Mock a failed asset load
    await page.route('**/assets/missing.fbx', (route) => {
      route.abort('failed');
    });

    await page.goto('/test-missing-assets');

    // Check error display
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).not.toContain('crashed');

    // Check fallback content
    await expect(page.locator('.fallback-model')).toBeVisible();

    // Console error check
    const consoleErrors = await page.evaluate(() => {
      return (window as any).__consoleErrors || [];
    });

    expect(consoleErrors.length).toBe(0); // No unhandled errors
  });

  test('Retry mechanism for transient failures', async ({ page }) => {
    let attemptCount = 0;

    // Mock 2 failures then success
    await page.route('**/assets/retry-test.fbx', (route) => {
      attemptCount++;
      if (attemptCount < 3) {
        route.abort('failed');
      } else {
        route.fulfill({
          status: 200,
          contentType: 'application/octet-stream',
          body: new ArrayBuffer(1024), // Mock FBX data
        });
      }
    });

    await page.goto('/test-retry-mechanism');

    // Should eventually succeed
    await expect(page.locator('.model-loaded')).toBeVisible();
    expect(attemptCount).toBe(3); // 2 failures + 1 success
  });
});
```

### Network Conditions Testing

```typescript
test.describe('Network Condition Testing', () => {
  ['slow-3g', 'offline'].forEach((condition) => {
    test(`Asset loading under ${condition}`, async ({ page }) => {
      await page.route('**/*', (route) => {
        if (route.request().resourceType() === 'document') {
          route.continue();
        } else {
          route.abort();
        }
      });

      // Set network condition
      await page.emulateNetworkConditions({
        offline: condition === 'offline',
        downloadThroughput: condition === 'slow-3g' ? 500 * 1024 : 0,
        uploadThroughput: condition === 'slow-3g' ? 500 * 1024 : 0,
      });

      await page.goto('/characters');

      if (condition === 'offline') {
        await expect(page.locator('.offline-message')).toBeVisible();
      } else {
        await expect(page.locator('.loading-message')).toBeVisible();
      }
    });
  });
});
```

## Visual Regression Testing

### Loading States

```typescript
test.describe('Visual Regression for Loading States', () => {
  test('Loading state appearance', async ({ page }) => {
    await page.goto('/characters');

    // Capture loading state
    await expect(page).toHaveScreenshot('loading-state.png', {
      mask: [page.locator('.loading-spinner')], // Animate elements
    });

    await page.waitForSelector('[data-testid="characters-loaded"]');

    // Capture loaded state
    await expect(page).toHaveScreenshot('loaded-state.png');
  });
});
```

### Error State Visuals

```typescript
test('Error state visual consistency', async ({ page }) => {
  // Mock asset loading failure
  await page.route('**/assets/error-test.fbx', (route) => {
    route.abort('failed');
  });

  await page.goto('/error-test');

  await expect(page).toHaveScreenshot('error-state.png');
  await expect(page.locator('.error-icon')).toBeVisible();
  await expect(page.locator('.retry-button')).toBeVisible();
});
```

## Automated Performance Metrics

### Performance Budget Checker

```typescript
function createPerformanceBudget() {
  return {
    maxLoadTime: 10000, // 10 seconds
    maxMemoryIncrease: 50 * 1024 * 1024, // 50MB
    maxConcurrentLoads: 3,
    allowedErrors: 0,

    async checkBudget(page: Page, testId: string) {
      const metrics = await page.evaluate(() => {
        return {
          loadTime:
            window.performance.timing.loadEventEnd - window.performance.timing.navigationStart,
          memory: {
            used: performance.memory?.usedJSHeapSize || 0,
            total: performance.memory?.jsHeapSizeLimit || 0,
          },
          errors: (window as any).__consoleErrors?.length || 0,
        };
      });

      const violations = [];

      if (metrics.loadTime > this.maxLoadTime) {
        violations.push(`Load time exceeded: ${metrics.loadTime}ms > ${this.maxLoadTime}ms`);
      }

      if (metrics.memory.used > this.maxMemoryIncrease) {
        violations.push(`Memory increase exceeded: ${metrics.memory.used} bytes`);
      }

      if (metrics.errors > this.allowedErrors) {
        violations.push(`Error count exceeded: ${metrics.errors} errors`);
      }

      if (violations.length > 0) {
        throw new Error(`Performance budget violated:\n${violations.join('\n')}`);
      }

      return metrics;
    },
  };
}

// Usage in test
const budget = createPerformanceBudget();
test('Performance budget compliance', async ({ page }) => {
  await page.goto('/characters');
  await page.waitForSelector('[data-testid="all-loaded"]');

  await budget.checkBudget(page, 'sequential-loading-test');
});
```

## Reference

- [Playwright Testing](https://playwright.dev/) — Browser automation testing
- [Web Performance APIs](https://developer.mozilla.org/en-US/docs/Web/API/Performance) — Performance monitoring
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) — Automated performance testing
- [Three.js Memory Management](https://threejs.org/docs/#manual/en/introduction/Performance) — Three.js optimization
