---
name: Stale Cache Finder
description: Identify stale cache issues across browser cache, CDN layers, API response caching, and application-level caches that cause users to see outdated content
version: 1.0.0
author: Pramod
license: MIT
tags: [cache-testing, stale-cache, cdn, cache-invalidation, cache-busting, etag, cache-headers, browser-cache]
testingTypes: [integration, e2e]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Stale Cache Finder Skill

You are an expert QA automation engineer specializing in cache correctness testing. When the user asks you to write, review, or debug tests for stale cache issues, follow these detailed instructions to identify caching defects across browser caches, CDN layers, API response caches, service workers, and application-level caching systems.

## Core Principles

1. **Cache correctness over cache performance** -- A fast response that serves stale data is worse than a slower response that serves correct data. Always prioritize correctness in cache testing, then optimize for performance.
2. **Test the full cache chain** -- Modern web applications have multiple cache layers: browser memory cache, disk cache, service worker cache, CDN edge cache, reverse proxy cache, and application-level cache. Test each layer independently and verify they interact correctly.
3. **Verify after mutation** -- The most critical cache tests verify that caches are properly invalidated after data mutations. Every write operation (create, update, delete) should be followed by a read that confirms the cache reflects the new state.
4. **Assert on headers, not assumptions** -- Never assume cache behavior based on how you configured it. Always verify the actual `Cache-Control`, `ETag`, `Last-Modified`, `Age`, and `X-Cache` headers in responses.
5. **Test cache across deployments** -- Stale cache issues frequently appear during deployments when old cached assets reference new APIs or vice versa. Simulate deployment scenarios in your test suite.
6. **Reproduce user complaints** -- "I still see the old version" is one of the most common user complaints. Build tests that simulate the exact user journey: visit page, data changes, revisit page, verify updated content.

## Project Structure

Organize stale cache testing projects with this structure:

```
tests/
  cache/
    headers/
      cache-control.spec.ts
      etag-validation.spec.ts
      last-modified.spec.ts
      vary-header.spec.ts
    cdn/
      cdn-invalidation.spec.ts
      edge-cache.spec.ts
      purge-verification.spec.ts
    service-worker/
      sw-cache-audit.spec.ts
      sw-update-flow.spec.ts
    api-cache/
      response-cache.spec.ts
      stale-while-revalidate.spec.ts
    browser/
      disk-cache.spec.ts
      memory-cache.spec.ts
      storage-cache.spec.ts
    post-deployment/
      asset-version.spec.ts
      cache-busting.spec.ts
  helpers/
    cache-header-parser.ts
    cdn-client.ts
    cache-inspector.ts
  fixtures/
    cache-test.fixture.ts
playwright.config.ts
```

## Cache Header Validation

Cache headers are the foundation of caching behavior. Incorrect headers cause all downstream cache layers to behave incorrectly.

### Cache-Control Header Testing

```typescript
import { test, expect } from '@playwright/test';

interface CacheExpectation {
  urlPattern: string | RegExp;
  expectedDirectives: string[];
  forbiddenDirectives?: string[];
  maxAgeRange?: { min: number; max: number };
  description: string;
}

const CACHE_EXPECTATIONS: CacheExpectation[] = [
  {
    urlPattern: /\.(js|css)(\?.*)?$/,
    expectedDirectives: ['public', 'max-age', 'immutable'],
    maxAgeRange: { min: 2592000, max: 31536000 }, // 30 days to 1 year
    description: 'Static assets should be cached long-term with immutable',
  },
  {
    urlPattern: /\.(png|jpg|jpeg|gif|svg|webp|avif)(\?.*)?$/,
    expectedDirectives: ['public', 'max-age'],
    maxAgeRange: { min: 86400, max: 31536000 }, // 1 day to 1 year
    description: 'Images should be cached with public directive',
  },
  {
    urlPattern: /\/api\//,
    expectedDirectives: ['no-store'],
    forbiddenDirectives: ['public'],
    description: 'API responses should not be cached by default',
  },
  {
    urlPattern: /\.html$/,
    expectedDirectives: ['no-cache'],
    forbiddenDirectives: ['immutable'],
    description: 'HTML pages should revalidate on every request',
  },
  {
    urlPattern: /\/api\/public\//,
    expectedDirectives: ['public', 's-maxage'],
    maxAgeRange: { min: 60, max: 3600 }, // 1 min to 1 hour
    description: 'Public API endpoints should use s-maxage for CDN caching',
  },
];

function parseCacheControl(header: string): Map<string, string | boolean> {
  const directives = new Map<string, string | boolean>();
  header.split(',').forEach((part) => {
    const trimmed = part.trim();
    const [key, value] = trimmed.split('=');
    directives.set(key.trim(), value ? value.trim() : true);
  });
  return directives;
}

test.describe('Cache-Control Header Validation', () => {
  test('all responses should have correct Cache-Control headers', async ({ page }) => {
    const violations: string[] = [];

    page.on('response', (response) => {
      const url = response.url();
      const cacheControl = response.headers()['cache-control'];

      for (const expectation of CACHE_EXPECTATIONS) {
        const matches =
          typeof expectation.urlPattern === 'string'
            ? url.includes(expectation.urlPattern)
            : expectation.urlPattern.test(url);

        if (!matches) continue;

        if (!cacheControl) {
          violations.push(
            `Missing Cache-Control for ${url} (${expectation.description})`
          );
          continue;
        }

        const directives = parseCacheControl(cacheControl);

        for (const required of expectation.expectedDirectives) {
          if (required === 'max-age') {
            if (!directives.has('max-age') && !directives.has('s-maxage')) {
              violations.push(
                `${url}: missing max-age directive (${expectation.description})`
              );
            }
          } else if (!directives.has(required)) {
            violations.push(
              `${url}: missing "${required}" directive (${expectation.description})`
            );
          }
        }

        if (expectation.forbiddenDirectives) {
          for (const forbidden of expectation.forbiddenDirectives) {
            if (directives.has(forbidden)) {
              violations.push(
                `${url}: has forbidden "${forbidden}" directive (${expectation.description})`
              );
            }
          }
        }

        if (expectation.maxAgeRange) {
          const maxAge = parseInt(
            (directives.get('max-age') || directives.get('s-maxage') || '0') as string,
            10
          );
          if (maxAge < expectation.maxAgeRange.min || maxAge > expectation.maxAgeRange.max) {
            violations.push(
              `${url}: max-age=${maxAge} outside expected range [${expectation.maxAgeRange.min}, ${expectation.maxAgeRange.max}]`
            );
          }
        }
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Navigate to a few key pages to capture more responses
    const routes = ['/dashboard', '/settings', '/about'];
    for (const route of routes) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
    }

    if (violations.length > 0) {
      console.log('Cache-Control violations:');
      violations.forEach((v) => console.log(`  - ${v}`));
    }

    expect(violations).toHaveLength(0);
  });
});
```

### ETag and Last-Modified Validation

```typescript
import { test, expect } from '@playwright/test';

test.describe('ETag Validation', () => {
  test('API responses should include ETag headers', async ({ request }) => {
    const response = await request.get('/api/public/skills');

    const etag = response.headers()['etag'];
    expect(etag, 'API response missing ETag header').toBeDefined();

    // Verify conditional request works
    const conditionalResponse = await request.get('/api/public/skills', {
      headers: { 'If-None-Match': etag },
    });

    expect(conditionalResponse.status()).toBe(304);
  });

  test('ETag should change when content changes', async ({ request }) => {
    // First request to get initial ETag
    const response1 = await request.get('/api/public/skills');
    const etag1 = response1.headers()['etag'];

    // Modify data (via API or direct DB mutation)
    await request.post('/api/skills', {
      data: {
        name: 'Test Skill',
        description: 'A test skill for cache validation that verifies ETags change properly',
        version: '1.0.0',
      },
    });

    // Second request should have a different ETag
    const response2 = await request.get('/api/public/skills');
    const etag2 = response2.headers()['etag'];

    expect(etag2).not.toBe(etag1);
  });

  test('Last-Modified should be present and accurate', async ({ request }) => {
    const response = await request.get('/api/public/skills/1');
    const lastModified = response.headers()['last-modified'];

    expect(lastModified, 'Missing Last-Modified header').toBeDefined();

    const lastModifiedDate = new Date(lastModified);
    expect(lastModifiedDate.getTime()).not.toBeNaN();

    // Verify conditional request with If-Modified-Since
    const conditionalResponse = await request.get('/api/public/skills/1', {
      headers: { 'If-Modified-Since': lastModified },
    });

    expect(conditionalResponse.status()).toBe(304);
  });
});
```

### Vary Header Verification

```typescript
import { test, expect } from '@playwright/test';

test.describe('Vary Header Verification', () => {
  test('API responses should include appropriate Vary headers', async ({ request }) => {
    const response = await request.get('/api/public/skills');
    const vary = response.headers()['vary'];

    expect(vary, 'Missing Vary header on API response').toBeDefined();

    // API should vary on Accept and Accept-Encoding at minimum
    const varyParts = vary.split(',').map((v: string) => v.trim().toLowerCase());
    expect(varyParts).toContain('accept');
    expect(varyParts).toContain('accept-encoding');
  });

  test('locale-dependent responses should Vary on Accept-Language', async ({ request }) => {
    const response = await request.get('/api/public/content', {
      headers: { 'Accept-Language': 'en-US' },
    });
    const vary = response.headers()['vary'];

    expect(vary).toBeDefined();
    const varyParts = vary.split(',').map((v: string) => v.trim().toLowerCase());
    expect(varyParts).toContain('accept-language');
  });

  test('auth-dependent responses should Vary on Authorization', async ({ request }) => {
    const response = await request.get('/api/dashboard');
    const vary = response.headers()['vary'];

    expect(vary).toBeDefined();
    const varyParts = vary.split(',').map((v: string) => v.trim().toLowerCase());
    expect(varyParts).toContain('authorization');
  });
});
```

## CDN Cache Testing

CDN caches add a layer of complexity because they cache at the edge, geographically distributed from the origin.

```typescript
import { test, expect } from '@playwright/test';

interface CDNCacheResult {
  url: string;
  cacheStatus: string;  // HIT, MISS, STALE, BYPASS
  age: number;
  edgeLocation?: string;
}

async function checkCDNCacheStatus(
  url: string,
  headers?: Record<string, string>
): Promise<CDNCacheResult> {
  const response = await fetch(url, { headers });

  // Common CDN cache status headers
  const cacheStatus =
    response.headers.get('x-cache') ||
    response.headers.get('cf-cache-status') ||       // Cloudflare
    response.headers.get('x-vercel-cache') ||         // Vercel
    response.headers.get('x-cdn-cache-status') ||
    response.headers.get('x-fastly-cache-status') ||  // Fastly
    'UNKNOWN';

  const age = parseInt(response.headers.get('age') || '0', 10);
  const edgeLocation =
    response.headers.get('x-served-by') ||
    response.headers.get('cf-ray') ||
    response.headers.get('x-vercel-id');

  return {
    url,
    cacheStatus: cacheStatus.toUpperCase(),
    age,
    edgeLocation: edgeLocation || undefined,
  };
}

test.describe('CDN Cache Testing', () => {
  test('static assets should be served from CDN cache', async () => {
    const staticAssets = [
      '/assets/main.js',
      '/assets/styles.css',
      '/images/logo.svg',
    ];

    for (const asset of staticAssets) {
      const baseUrl = process.env.BASE_URL || 'https://example.com';

      // First request may be a MISS
      await checkCDNCacheStatus(`${baseUrl}${asset}`);

      // Second request should be a HIT
      const result = await checkCDNCacheStatus(`${baseUrl}${asset}`);

      expect(
        ['HIT', 'STALE'].includes(result.cacheStatus),
        `${asset}: expected CDN cache HIT but got ${result.cacheStatus}`
      ).toBe(true);
    }
  });

  test('CDN should respect s-maxage for API responses', async () => {
    const baseUrl = process.env.BASE_URL || 'https://example.com';
    const url = `${baseUrl}/api/public/skills`;

    const response = await fetch(url);
    const cacheControl = response.headers.get('cache-control') || '';

    // Verify s-maxage is present for CDN-cached APIs
    expect(cacheControl).toContain('s-maxage');

    const sMaxAge = parseInt(
      cacheControl.match(/s-maxage=(\d+)/)?.[1] || '0',
      10
    );
    expect(sMaxAge).toBeGreaterThan(0);
  });

  test('CDN should purge cache after content update', async ({ request }) => {
    const baseUrl = process.env.BASE_URL || 'https://example.com';

    // Get initial content
    const before = await fetch(`${baseUrl}/api/public/skills/test-skill`);
    const beforeBody = await before.json();
    const beforeEtag = before.headers.get('etag');

    // Update the content
    await request.patch('/api/skills/test-skill', {
      data: { description: `Updated at ${Date.now()}` },
    });

    // Allow time for cache invalidation propagation
    await new Promise((resolve) => setTimeout(resolve, 5000));

    // Verify CDN serves the updated content
    const after = await fetch(`${baseUrl}/api/public/skills/test-skill`);
    const afterBody = await after.json();
    const afterEtag = after.headers.get('etag');

    expect(afterBody.description).not.toBe(beforeBody.description);
    expect(afterEtag).not.toBe(beforeEtag);
  });
});
```

## Service Worker Cache Auditing

Service workers intercept network requests and can serve stale content indefinitely if not managed correctly.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Service Worker Cache Auditing', () => {
  test('service worker should not cache API responses', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check what the service worker has cached
    const cachedUrls = await page.evaluate(async () => {
      const cacheNames = await caches.keys();
      const allUrls: string[] = [];

      for (const name of cacheNames) {
        const cache = await caches.open(name);
        const keys = await cache.keys();
        allUrls.push(...keys.map((k) => k.url));
      }

      return allUrls;
    });

    // API responses should NOT be in the service worker cache
    const cachedApiUrls = cachedUrls.filter((url) => url.includes('/api/'));
    expect(
      cachedApiUrls,
      `Service worker is caching API responses: ${cachedApiUrls.join(', ')}`
    ).toHaveLength(0);
  });

  test('service worker should update cached assets on new deployment', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get the current service worker version
    const swVersion = await page.evaluate(async () => {
      const registration = await navigator.serviceWorker.getRegistration();
      if (!registration?.active) return null;

      // Most SWs expose a version via a custom message
      return new Promise<string | null>((resolve) => {
        const channel = new MessageChannel();
        channel.port1.onmessage = (event) => resolve(event.data.version);
        registration.active!.postMessage({ type: 'GET_VERSION' }, [channel.port2]);
        setTimeout(() => resolve(null), 2000);
      });
    });

    // Trigger a service worker update check
    const updateFound = await page.evaluate(async () => {
      const registration = await navigator.serviceWorker.getRegistration();
      if (!registration) return false;

      await registration.update();
      return registration.waiting !== null || registration.installing !== null;
    });

    // If an update is available, verify it activates
    if (updateFound) {
      // Wait for the new service worker to activate
      await page.evaluate(async () => {
        const registration = await navigator.serviceWorker.getRegistration();
        if (registration?.waiting) {
          registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        }
      });

      await page.waitForTimeout(2000);

      // Verify the old caches are cleaned up
      const remainingCaches = await page.evaluate(async () => {
        return await caches.keys();
      });

      // Should not have old versioned caches lingering
      const oldCaches = remainingCaches.filter((name) =>
        name.includes('v1') || name.includes('old')
      );
      expect(oldCaches).toHaveLength(0);
    }
  });

  test('service worker should serve fresh content after skip-waiting', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get content before any update
    const contentBefore = await page.locator('h1').first().textContent();

    // Force service worker update and activation
    await page.evaluate(async () => {
      const registration = await navigator.serviceWorker.getRegistration();
      if (registration) {
        await registration.update();
        if (registration.waiting) {
          registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        }
      }
    });

    // Reload and verify content is fresh
    await page.reload();
    await page.waitForLoadState('networkidle');

    const contentAfter = await page.locator('h1').first().textContent();

    // Content should at minimum be non-empty (not a broken cache response)
    expect(contentAfter).toBeTruthy();
    expect(contentAfter!.length).toBeGreaterThan(0);
  });
});
```

## Stale-While-Revalidate Testing

The `stale-while-revalidate` directive allows serving stale content while fetching fresh content in the background. Testing this behavior requires timing-aware assertions.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Stale-While-Revalidate Behavior', () => {
  test('SWR responses should eventually serve fresh content', async ({ request }) => {
    // First request -- populates the cache
    const response1 = await request.get('/api/public/feed');
    expect(response1.ok()).toBe(true);
    const body1 = await response1.json();

    // Wait for the max-age to expire but within SWR window
    // Assuming max-age=60, stale-while-revalidate=300
    const cacheControl = response1.headers()['cache-control'];
    const maxAge = parseInt(cacheControl.match(/max-age=(\d+)/)?.[1] || '60', 10);

    // In testing, we simulate passage of time by waiting slightly longer than max-age
    // For a real test, you might use a test server that controls time
    await new Promise((resolve) => setTimeout(resolve, (maxAge + 1) * 1000));

    // Second request -- should get stale content but trigger revalidation
    const response2 = await request.get('/api/public/feed');
    const age2 = parseInt(response2.headers()['age'] || '0', 10);

    // The response might be stale (age > max-age)
    if (age2 > maxAge) {
      // This is the SWR behavior -- stale content served immediately
      // Wait for background revalidation to complete
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Third request should now have fresh content
      const response3 = await request.get('/api/public/feed');
      const age3 = parseInt(response3.headers()['age'] || '0', 10);
      expect(age3).toBeLessThan(maxAge);
    }
  });

  test('SWR should not serve content beyond stale-while-revalidate window', async ({
    request,
  }) => {
    const response = await request.get('/api/public/feed');
    const cacheControl = response.headers()['cache-control'] || '';

    if (cacheControl.includes('stale-while-revalidate')) {
      const swrWindow = parseInt(
        cacheControl.match(/stale-while-revalidate=(\d+)/)?.[1] || '0',
        10
      );

      // Verify the SWR window is reasonable
      expect(swrWindow).toBeGreaterThan(0);
      expect(swrWindow).toBeLessThanOrEqual(86400); // Max 1 day
    }
  });
});
```

## Cache Key Collision Detection

Cache key collisions happen when different content is cached under the same key, causing one user to see another user's data.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Cache Key Collision Detection', () => {
  test('authenticated endpoints should not share cached responses', async ({ request }) => {
    // Request as User A
    const responseA = await request.get('/api/dashboard', {
      headers: { Authorization: 'Bearer token-user-a' },
    });
    const dataA = await responseA.json();

    // Request as User B
    const responseB = await request.get('/api/dashboard', {
      headers: { Authorization: 'Bearer token-user-b' },
    });
    const dataB = await responseB.json();

    // These should contain different user-specific data
    expect(dataA.userId).not.toBe(dataB.userId);

    // Verify that User B did not receive User A's cached response
    expect(dataB.userId).toBe('user-b');
  });

  test('query parameter variations should produce distinct cache entries', async ({
    request,
  }) => {
    const response1 = await request.get('/api/public/skills?page=1&sort=newest');
    const body1 = await response1.json();

    const response2 = await request.get('/api/public/skills?page=2&sort=newest');
    const body2 = await response2.json();

    const response3 = await request.get('/api/public/skills?page=1&sort=popular');
    const body3 = await response3.json();

    // Each variation should return different content
    expect(JSON.stringify(body1)).not.toBe(JSON.stringify(body2));
    expect(JSON.stringify(body1)).not.toBe(JSON.stringify(body3));
  });

  test('locale-specific responses should not collide', async ({ request }) => {
    const enResponse = await request.get('/api/public/content', {
      headers: { 'Accept-Language': 'en-US' },
    });
    const enBody = await enResponse.json();

    const deResponse = await request.get('/api/public/content', {
      headers: { 'Accept-Language': 'de-DE' },
    });
    const deBody = await deResponse.json();

    // Content should differ by locale
    expect(enBody.locale).not.toBe(deBody.locale);
  });
});
```

## Post-Deployment Cache Busting Verification

Deployments are the most common trigger for stale cache issues. Old JavaScript bundles may reference old API contracts, causing runtime errors.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Post-Deployment Cache Busting', () => {
  test('JavaScript bundles should have content-hashed filenames', async ({ page }) => {
    const scriptUrls: string[] = [];

    page.on('response', (response) => {
      if (response.url().endsWith('.js')) {
        scriptUrls.push(response.url());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    for (const url of scriptUrls) {
      // Content-hashed filenames typically look like: main.abc123.js or main-abc123.js
      const hasContentHash = /[.-][a-f0-9]{6,}\.js/.test(url);
      expect(
        hasContentHash,
        `Script ${url} does not have a content hash in filename`
      ).toBe(true);
    }
  });

  test('CSS files should have content-hashed filenames', async ({ page }) => {
    const cssUrls: string[] = [];

    page.on('response', (response) => {
      const contentType = response.headers()['content-type'] || '';
      if (contentType.includes('text/css') || response.url().endsWith('.css')) {
        cssUrls.push(response.url());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    for (const url of cssUrls) {
      const hasContentHash = /[.-][a-f0-9]{6,}\.css/.test(url);
      expect(
        hasContentHash,
        `CSS file ${url} does not have a content hash in filename`
      ).toBe(true);
    }
  });

  test('HTML should reference current asset versions after deployment', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get all script and link tags
    const assetRefs = await page.evaluate(() => {
      const scripts = Array.from(document.querySelectorAll('script[src]')).map(
        (s) => (s as HTMLScriptElement).src
      );
      const links = Array.from(
        document.querySelectorAll('link[rel="stylesheet"]')
      ).map((l) => (l as HTMLLinkElement).href);
      return { scripts, links };
    });

    // Verify all referenced assets are actually reachable
    for (const src of [...assetRefs.scripts, ...assetRefs.links]) {
      const response = await page.request.get(src);
      expect(
        response.ok(),
        `Asset not found (possible stale HTML cache): ${src}`
      ).toBe(true);
    }
  });

  test('API version header should match deployed version', async ({ request }) => {
    const response = await request.get('/api/health');
    const apiVersion = response.headers()['x-api-version'];
    const deployId = response.headers()['x-deployment-id'];

    expect(apiVersion).toBeDefined();

    // If a deployment ID is available, verify it matches expectations
    if (deployId && process.env.EXPECTED_DEPLOYMENT_ID) {
      expect(deployId).toBe(process.env.EXPECTED_DEPLOYMENT_ID);
    }
  });
});
```

## Browser Storage Cache Testing

Applications often cache data in localStorage, sessionStorage, or IndexedDB. Stale data in these stores can cause subtle bugs.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Browser Storage Cache Testing', () => {
  test('localStorage cache should be invalidated on data mutation', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Check what is cached in localStorage
    const cachedData = await page.evaluate(() => {
      const cache: Record<string, string> = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)!;
        if (key.startsWith('cache:') || key.startsWith('data:')) {
          cache[key] = localStorage.getItem(key)!;
        }
      }
      return cache;
    });

    // Perform a mutation
    await page.locator('[data-testid="update-profile"]').click();
    await page.fill('[data-testid="name-input"]', 'Updated Name');
    await page.locator('[data-testid="save-button"]').click();
    await page.waitForResponse('**/api/profile');

    // Verify the cached data was invalidated or updated
    const updatedCache = await page.evaluate(() => {
      const cache: Record<string, string> = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)!;
        if (key.startsWith('cache:') || key.startsWith('data:')) {
          cache[key] = localStorage.getItem(key)!;
        }
      }
      return cache;
    });

    // Cache entries related to profile should be updated or removed
    for (const [key, value] of Object.entries(cachedData)) {
      if (key.includes('profile') || key.includes('user')) {
        const newValue = updatedCache[key];
        expect(
          newValue !== value || newValue === undefined,
          `localStorage key "${key}" was not invalidated after mutation`
        ).toBe(true);
      }
    }
  });

  test('cached data should have TTL and not persist forever', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    const cacheEntries = await page.evaluate(() => {
      const entries: { key: string; hasTimestamp: boolean; age: number | null }[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)!;
        const value = localStorage.getItem(key)!;

        let hasTimestamp = false;
        let age: number | null = null;

        try {
          const parsed = JSON.parse(value);
          if (parsed.timestamp || parsed.cachedAt || parsed.expiresAt) {
            hasTimestamp = true;
            const ts = parsed.timestamp || parsed.cachedAt;
            if (ts) {
              age = Date.now() - new Date(ts).getTime();
            }
          }
        } catch {
          // Not JSON, ignore
        }

        if (key.startsWith('cache:')) {
          entries.push({ key, hasTimestamp, age });
        }
      }
      return entries;
    });

    for (const entry of cacheEntries) {
      expect(
        entry.hasTimestamp,
        `Cache entry "${entry.key}" has no timestamp -- cannot determine staleness`
      ).toBe(true);

      if (entry.age !== null) {
        // Cache entries older than 24 hours are suspicious
        const maxAge = 24 * 60 * 60 * 1000; // 24 hours in ms
        expect(
          entry.age,
          `Cache entry "${entry.key}" is ${Math.round(entry.age / 3600000)}h old`
        ).toBeLessThan(maxAge);
      }
    }
  });
});
```

## Configuration

### Playwright Configuration for Cache Testing

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/cache',
  fullyParallel: false, // Cache tests may interfere with each other
  retries: 1,
  reporter: [
    ['html', { open: 'never' }],
    ['json', { outputFile: 'cache-test-results.json' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'cache-headers',
      testMatch: '**/headers/**',
      use: {
        ...devices['Desktop Chrome'],
        // Disable browser cache for header tests
        bypassCSP: true,
      },
    },
    {
      name: 'cdn-cache',
      testMatch: '**/cdn/**',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'service-worker',
      testMatch: '**/service-worker/**',
      use: {
        ...devices['Desktop Chrome'],
        serviceWorkers: 'allow',
      },
    },
    {
      name: 'browser-cache',
      testMatch: '**/browser/**',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],
});
```

## Best Practices

1. **Always validate Cache-Control headers on every response** -- Do not rely on server configuration alone. Add automated tests that verify every response type has the correct caching headers.

2. **Use content-hashed filenames for all static assets** -- Content hashing (e.g., `main.abc123.js`) ensures that new deployments serve new files while old cached files remain valid for users who have not refreshed.

3. **Set `no-store` on authenticated API responses** -- User-specific data must never be cached by shared caches (CDN, proxy). Use `Cache-Control: no-store` for any response that contains user-specific content.

4. **Include `Vary` headers for content negotiation** -- When responses vary by `Accept-Language`, `Accept`, or `Authorization`, the `Vary` header must declare these. Missing `Vary` headers cause cache key collisions.

5. **Test cache behavior after every deployment** -- Run a post-deployment smoke test that verifies cached assets are accessible, HTML references current asset versions, and API responses are fresh.

6. **Implement cache versioning in service workers** -- Service worker caches must be versioned. On each deployment, the new service worker should create new cache entries and delete old versioned caches.

7. **Use `s-maxage` for CDN caching separate from browser caching** -- `s-maxage` controls CDN cache duration independently from `max-age`. This allows short browser cache times with longer CDN cache times.

8. **Add cache TTL to all application-level cache entries** -- Every entry in localStorage, Redis, or in-memory caches must have an explicit expiration time. Cache entries without TTL persist forever and become stale silently.

9. **Monitor cache hit rates in production** -- Low cache hit rates indicate misconfigured caching. High hit rates with user complaints indicate stale cache serving. Track both metrics.

10. **Test the `no-cache` vs `no-store` distinction** -- `no-cache` means "revalidate before use" (still caches, but checks freshness). `no-store` means "never cache at all". Using the wrong one causes either stale content or unnecessary requests.

11. **Purge CDN cache as part of the deployment pipeline** -- Automate CDN cache purging in your CI/CD pipeline. Manual purging is error-prone and delays fresh content delivery.

12. **Test with multiple browsers** -- Browser caching implementations differ. Chrome, Firefox, and Safari handle `Cache-Control` directives slightly differently, especially around `stale-while-revalidate` and service worker interactions.

## Anti-Patterns to Avoid

1. **Using `Cache-Control: no-cache` when you mean `no-store`** -- `no-cache` still caches the response; it just requires revalidation. For sensitive data, always use `no-store` to prevent any caching.

2. **Relying on CDN purge without verification** -- CDN purge APIs are eventually consistent. A purge request does not guarantee instant cache invalidation across all edge locations. Always verify with a follow-up request.

3. **Caching responses without `Vary` headers** -- If your endpoint returns different content based on request headers (Accept-Language, Authorization), missing `Vary` headers will cause the CDN to serve the wrong cached response to the wrong user.

4. **Setting long `max-age` on HTML documents** -- HTML pages are the entry point for loading all other assets. A long `max-age` on HTML means users will not receive updated asset references until the HTML cache expires. Use `no-cache` or short `max-age` for HTML.

5. **Storing sensitive data in browser cache without encryption** -- Browser disk cache stores response bodies in plaintext. Sensitive data cached to disk can be read by other applications or users on shared computers.

6. **Ignoring service worker cache during testing** -- Service workers operate independently of the browser's HTTP cache. A test that clears the browser cache but ignores the service worker cache will still see stale content.

7. **Using timestamps as cache busters in query strings** -- Appending `?t=1234567890` to URLs defeats caching entirely and wastes CDN bandwidth. Use content-hashed filenames instead, which only change when content actually changes.

## Debugging Tips

1. **Use Chrome DevTools Network panel with "Disable cache" unchecked** -- The "Disable cache" checkbox in DevTools prevents testing real cache behavior. Turn it off to see actual cache hits and misses in the Size column.

2. **Check the `Age` header to determine how long content has been cached** -- The `Age` header (in seconds) tells you how long the response has been in a shared cache. A high `Age` value on content that should be fresh indicates a stale cache problem.

3. **Use `curl -I` to inspect response headers without browser interference** -- Browsers add their own caching behavior. Use `curl -I <url>` to see the raw response headers from the server without any browser-side caching modifications.

4. **Verify service worker state in Application tab** -- Chrome DevTools Application tab shows registered service workers, their status (active, waiting, installing), and the contents of each cache storage. This is essential for debugging service worker caching issues.

5. **Check for cache poisoning with different request variations** -- Test the same URL with different `Accept`, `Accept-Language`, and `Authorization` headers. If you receive the same cached response regardless of header variations, the cache is not respecting `Vary`.

6. **Monitor the `X-Cache` header across multiple requests** -- Make the same request 3-4 times in sequence. The first should show `MISS`, and subsequent requests should show `HIT`. If all show `MISS`, caching is not working. If all show `HIT` after content changes, the cache is stale.

7. **Use Lighthouse to audit cache policy** -- Lighthouse's "Serve static assets with an efficient cache policy" audit identifies resources with short or missing cache lifetimes. Run this after deployments to verify caching is configured correctly.

8. **Compare `ETag` values before and after data changes** -- If the `ETag` does not change after you modify data, the server is generating ETags incorrectly (possibly from a stale cache layer). Track ETags across mutations to verify they update.

9. **Test with `Cache-Control: no-cache` request header** -- Sending `Cache-Control: no-cache` in your request forces the server (and most CDNs) to bypass cache and return a fresh response. Compare this fresh response to the normally cached response to verify they match.

10. **Check for `Set-Cookie` headers on cached responses** -- Responses with `Set-Cookie` headers should never be cached by shared caches. If you see `Set-Cookie` alongside `Cache-Control: public`, this is a serious bug that can leak session cookies between users.
