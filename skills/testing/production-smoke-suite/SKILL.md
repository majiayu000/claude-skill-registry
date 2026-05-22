---
name: Production Smoke Suite
description: Build lightweight production smoke test suites that verify critical user paths, API health, and third-party integrations after every deployment.
version: 1.0.0
author: Pramod
license: MIT
tags: [smoke-testing, production, deployment-verification, health-checks, monitoring, canary]
testingTypes: [e2e]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web, api, devops]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Production Smoke Suite

Production smoke testing is the last line of defense between a deployment and a broken user experience. Unlike comprehensive end-to-end suites that may run for 30 minutes or more, a smoke suite must complete in under 2 minutes and verify that the application's critical paths are functional. This skill covers the philosophy behind production smoke testing, the architecture of a reliable smoke suite, concrete implementation patterns with Playwright and raw HTTP clients, integration with deployment pipelines, and strategies for handling third-party dependencies, authentication flows, and flaky network conditions in real production environments.

## Core Principles

### 1. Speed Over Coverage

A smoke suite is not a regression suite. Its sole purpose is to answer one question: "Did this deployment break anything critical?" If the suite takes more than 2 minutes, it is too slow. Every test must justify its inclusion by covering a revenue-critical or user-critical path. Ruthlessly prune tests that do not protect high-value user journeys.

### 2. Production-Safe Execution

Smoke tests run against real production infrastructure. They must never create permanent data, modify user accounts, trigger billing events, or send real notifications. Every test must be read-only or use dedicated smoke-test accounts with sandboxed permissions. A smoke test that accidentally charges a customer or sends spam emails is worse than having no smoke tests at all.

### 3. Deterministic Assertions

Production environments experience variable latency, CDN caching, and third-party service delays. Smoke tests must use generous timeouts, retry logic, and assertions that tolerate minor variations. Check that a response contains expected fields rather than expecting exact string matches. Verify that status codes are in acceptable ranges rather than asserting a single value.

### 4. Immediate Rollback Signal

The smoke suite must integrate with your deployment pipeline to trigger automatic rollback on failure. A passing smoke suite promotes the deployment; a failing suite halts the rollout and alerts the on-call team. Without this integration, smoke tests are just monitoring with extra steps.

### 5. Independent and Isolated

Each smoke test must be fully independent. No test should depend on another test's side effects. Tests should run in parallel where possible to minimize total suite duration. Shared state between tests is a reliability liability that will eventually cause false positives or negatives.

## Project Structure

```
smoke-tests/
  src/
    tests/
      health-check.spec.ts
      homepage.spec.ts
      authentication.spec.ts
      checkout-flow.spec.ts
      api-health.spec.ts
      third-party.spec.ts
    helpers/
      smoke-config.ts
      http-client.ts
      retry.ts
      assertions.ts
      alerting.ts
    fixtures/
      smoke-accounts.ts
  playwright.config.ts
  package.json
  tsconfig.json
  Dockerfile
```

The `src/tests/` directory contains one file per critical path. The `src/helpers/` directory holds shared utilities for configuration, HTTP requests with retry logic, custom assertions, and alerting integrations. The `src/fixtures/` directory manages smoke test account credentials and test data.

## Configuration

### Playwright Configuration for Smoke Testing

Smoke-specific Playwright configuration prioritizes speed, reliability, and minimal resource usage:

```typescript
import { defineConfig, devices } from '@playwright/test';

const BASE_URL = process.env.SMOKE_BASE_URL || 'https://app.example.com';
const TIMEOUT = parseInt(process.env.SMOKE_TIMEOUT || '30000', 10);

export default defineConfig({
  testDir: './src/tests',
  timeout: TIMEOUT,
  expect: {
    timeout: 10000,
  },
  fullyParallel: true,
  forbidOnly: true,
  retries: 2,
  workers: 4,
  reporter: [
    ['list'],
    ['json', { outputFile: 'smoke-results.json' }],
  ],
  use: {
    baseURL: BASE_URL,
    screenshot: 'only-on-failure',
    video: 'off',
    trace: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 15000,
    extraHTTPHeaders: {
      'X-Smoke-Test': 'true',
    },
  },
  projects: [
    {
      name: 'smoke-chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

Key decisions in this configuration: `fullyParallel: true` runs all tests concurrently for speed. `retries: 2` tolerates transient network issues. `video: 'off'` avoids the overhead of recording video for every test. The `X-Smoke-Test` header allows backend services to identify and filter smoke test traffic from real user analytics.

### Smoke Configuration Module

Centralize all smoke test configuration in a typed module:

```typescript
// src/helpers/smoke-config.ts

export interface SmokeConfig {
  baseUrl: string;
  apiBaseUrl: string;
  timeout: number;
  retries: number;
  smokeAccountEmail: string;
  smokeAccountPassword: string;
  slackWebhookUrl?: string;
  pagerDutyRoutingKey?: string;
  environment: 'production' | 'staging';
}

export function getSmokeConfig(): SmokeConfig {
  const baseUrl = process.env.SMOKE_BASE_URL;
  if (!baseUrl) {
    throw new Error('SMOKE_BASE_URL environment variable is required');
  }

  return {
    baseUrl,
    apiBaseUrl: process.env.SMOKE_API_URL || `${baseUrl}/api`,
    timeout: parseInt(process.env.SMOKE_TIMEOUT || '30000', 10),
    retries: parseInt(process.env.SMOKE_RETRIES || '2', 10),
    smokeAccountEmail: process.env.SMOKE_ACCOUNT_EMAIL || '',
    smokeAccountPassword: process.env.SMOKE_ACCOUNT_PASSWORD || '',
    slackWebhookUrl: process.env.SLACK_WEBHOOK_URL,
    pagerDutyRoutingKey: process.env.PAGERDUTY_ROUTING_KEY,
    environment: (process.env.SMOKE_ENV as 'production' | 'staging') || 'production',
  };
}
```

## Health Check Tests

### API Health Endpoint

Every production application should expose a health endpoint. The smoke suite should verify it first, as a failing health check makes all subsequent tests pointless:

```typescript
// src/tests/api-health.spec.ts
import { test, expect } from '@playwright/test';
import { getSmokeConfig } from '../helpers/smoke-config';

const config = getSmokeConfig();

test.describe('API Health Checks', () => {
  test('primary health endpoint returns 200', async ({ request }) => {
    const response = await request.get(`${config.apiBaseUrl}/health`);
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toHaveProperty('status', 'healthy');
    expect(body).toHaveProperty('version');
    expect(body).toHaveProperty('uptime');
  });

  test('database connectivity is healthy', async ({ request }) => {
    const response = await request.get(`${config.apiBaseUrl}/health/db`);
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toHaveProperty('database', 'connected');
    expect(body.latencyMs).toBeLessThan(500);
  });

  test('cache layer is responsive', async ({ request }) => {
    const response = await request.get(`${config.apiBaseUrl}/health/cache`);
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toHaveProperty('cache', 'connected');
  });

  test('critical API endpoints respond within SLA', async ({ request }) => {
    const criticalEndpoints = [
      { path: '/api/products', maxLatency: 2000 },
      { path: '/api/categories', maxLatency: 1000 },
      { path: '/api/user/profile', maxLatency: 1500, auth: true },
    ];

    for (const endpoint of criticalEndpoints) {
      const start = Date.now();
      const headers: Record<string, string> = {};

      if (endpoint.auth) {
        headers['Authorization'] = `Bearer ${process.env.SMOKE_API_TOKEN}`;
      }

      const response = await request.get(`${config.baseUrl}${endpoint.path}`, {
        headers,
      });
      const latency = Date.now() - start;

      expect(response.status()).toBeLessThan(500);
      expect(latency).toBeLessThan(endpoint.maxLatency);
    }
  });
});
```

### Homepage and Core Page Smoke Tests

```typescript
// src/tests/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Core Pages', () => {
  test('homepage loads and renders critical elements', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/YourApp/);

    const hero = page.getByRole('heading', { level: 1 });
    await expect(hero).toBeVisible();

    const nav = page.getByRole('navigation');
    await expect(nav).toBeVisible();

    const ctaButton = page.getByRole('link', { name: /get started|sign up/i });
    await expect(ctaButton).toBeVisible();
  });

  test('pricing page loads correctly', async ({ page }) => {
    await page.goto('/pricing');
    await expect(page).toHaveTitle(/pricing/i);

    const plans = page.getByTestId('pricing-plan');
    await expect(plans.first()).toBeVisible();
  });

  test('static assets load without 404 errors', async ({ page }) => {
    const failedRequests: string[] = [];

    page.on('response', (response) => {
      if (response.status() === 404 && response.url().match(/\.(js|css|png|jpg|svg|woff2?)$/)) {
        failedRequests.push(`${response.status()} ${response.url()}`);
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    expect(failedRequests).toEqual([]);
  });

  test('robots.txt is accessible', async ({ request }) => {
    const response = await request.get('/robots.txt');
    expect(response.status()).toBe(200);
    const text = await response.text();
    expect(text).toContain('User-agent');
  });

  test('sitemap.xml is valid', async ({ request }) => {
    const response = await request.get('/sitemap.xml');
    expect(response.status()).toBe(200);
    const text = await response.text();
    expect(text).toContain('<?xml');
    expect(text).toContain('<urlset');
  });
});
```

## Authentication Smoke Tests

Authentication is one of the most critical paths to verify after deployment. A broken login flow immediately locks out every user:

```typescript
// src/tests/authentication.spec.ts
import { test, expect } from '@playwright/test';
import { getSmokeConfig } from '../helpers/smoke-config';

const config = getSmokeConfig();

test.describe('Authentication Flow', () => {
  test('login page renders correctly', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /sign in|log in/i })).toBeVisible();
  });

  test('smoke account can authenticate successfully', async ({ page }) => {
    test.skip(!config.smokeAccountEmail, 'Smoke account not configured');

    await page.goto('/login');
    await page.getByLabel(/email/i).fill(config.smokeAccountEmail);
    await page.getByLabel(/password/i).fill(config.smokeAccountPassword);
    await page.getByRole('button', { name: /sign in|log in/i }).click();

    await expect(page).toHaveURL(/dashboard|home/);
    await expect(page.getByTestId('user-avatar')).toBeVisible({ timeout: 15000 });
  });

  test('OAuth providers are available on login page', async ({ page }) => {
    await page.goto('/login');

    const googleButton = page.getByRole('button', { name: /google/i });
    const githubButton = page.getByRole('button', { name: /github/i });

    const googleVisible = await googleButton.isVisible().catch(() => false);
    const githubVisible = await githubButton.isVisible().catch(() => false);

    expect(googleVisible || githubVisible).toBe(true);
  });

  test('protected route redirects unauthenticated users', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/login|signin|auth/);
  });
});
```

## Critical User Flow Smoke Tests

These tests verify the most important user journeys that directly impact revenue and user satisfaction:

```typescript
// src/tests/checkout-flow.spec.ts
import { test, expect } from '@playwright/test';
import { getSmokeConfig } from '../helpers/smoke-config';

const config = getSmokeConfig();

test.describe('Critical User Paths', () => {
  test('search functionality returns results', async ({ page }) => {
    await page.goto('/');

    const searchInput = page.getByRole('searchbox').or(page.getByPlaceholder(/search/i));
    await searchInput.fill('test query');
    await searchInput.press('Enter');

    await expect(page.getByTestId('search-results').or(page.locator('[data-search-results]')))
      .toBeVisible({ timeout: 10000 });
  });

  test('product listing page loads with items', async ({ page }) => {
    await page.goto('/products');

    const productCards = page.getByTestId('product-card');
    await expect(productCards.first()).toBeVisible({ timeout: 10000 });

    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);
  });

  test('product detail page renders completely', async ({ page }) => {
    await page.goto('/products');

    const firstProduct = page.getByTestId('product-card').first();
    await firstProduct.click();

    await expect(page.getByTestId('product-title')).toBeVisible();
    await expect(page.getByTestId('product-price')).toBeVisible();
    await expect(page.getByRole('button', { name: /add to cart|buy/i })).toBeVisible();
  });

  test('contact form is accessible and functional', async ({ page }) => {
    await page.goto('/contact');

    await expect(page.getByLabel(/name/i)).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/message/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /send|submit/i })).toBeVisible();
  });
});
```

## Third-Party Integration Checks

Third-party services can fail independently of your deployment. Smoke tests should verify their availability:

```typescript
// src/tests/third-party.spec.ts
import { test, expect } from '@playwright/test';
import { getSmokeConfig } from '../helpers/smoke-config';

const config = getSmokeConfig();

test.describe('Third-Party Integrations', () => {
  test('CDN serves static assets correctly', async ({ request }) => {
    const cdnUrl = process.env.CDN_URL || 'https://cdn.example.com';
    const response = await request.get(`${cdnUrl}/health`);
    expect(response.status()).toBeLessThan(400);
  });

  test('payment processor is reachable', async ({ request }) => {
    const stripeHealthUrl = 'https://status.stripe.com/api/v2/status.json';
    const response = await request.get(stripeHealthUrl);
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body.status.indicator).not.toBe('critical');
  });

  test('email service is operational', async ({ request }) => {
    const response = await request.get(`${config.apiBaseUrl}/health/email`);
    expect(response.status()).toBe(200);
  });

  test('analytics script loads on page', async ({ page }) => {
    let analyticsLoaded = false;

    page.on('response', (response) => {
      if (response.url().includes('analytics') || response.url().includes('gtag')) {
        if (response.status() === 200) {
          analyticsLoaded = true;
        }
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    if (!analyticsLoaded) {
      console.warn('Analytics script did not load - verify tracking is operational');
    }
  });
});
```

## HTTP Client with Retry Logic

For API-level smoke checks that do not require a browser, use a lightweight HTTP client with built-in retry and backoff:

```typescript
// src/helpers/http-client.ts

interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableStatuses: number[];
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  initialDelayMs: 1000,
  maxDelayMs: 10000,
  backoffMultiplier: 2,
  retryableStatuses: [502, 503, 504, 429],
};

export async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retryConfig: Partial<RetryConfig> = {}
): Promise<Response> {
  const config = { ...DEFAULT_RETRY_CONFIG, ...retryConfig };
  let lastError: Error | null = null;
  let delay = config.initialDelayMs;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        signal: AbortSignal.timeout(30000),
      });

      if (config.retryableStatuses.includes(response.status) && attempt < config.maxRetries) {
        console.warn(
          `Attempt ${attempt + 1}/${config.maxRetries + 1}: ${url} returned ${response.status}, retrying...`
        );
        await sleep(delay);
        delay = Math.min(delay * config.backoffMultiplier, config.maxDelayMs);
        continue;
      }

      return response;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt < config.maxRetries) {
        console.warn(
          `Attempt ${attempt + 1}/${config.maxRetries + 1}: ${url} failed with ${lastError.message}, retrying...`
        );
        await sleep(delay);
        delay = Math.min(delay * config.backoffMultiplier, config.maxDelayMs);
      }
    }
  }

  throw new Error(`All ${config.maxRetries + 1} attempts failed for ${url}: ${lastError?.message}`);
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

## Alerting Integration

When smoke tests fail, the right people need to know immediately:

```typescript
// src/helpers/alerting.ts
import { getSmokeConfig } from './smoke-config';

interface SmokeResult {
  passed: number;
  failed: number;
  skipped: number;
  duration: number;
  failures: Array<{ name: string; error: string }>;
  environment: string;
  url: string;
}

export async function sendSlackAlert(result: SmokeResult): Promise<void> {
  const config = getSmokeConfig();
  if (!config.slackWebhookUrl) return;

  const color = result.failed > 0 ? '#dc2626' : '#16a34a';
  const status = result.failed > 0 ? 'FAILED' : 'PASSED';

  const failureDetails = result.failures
    .slice(0, 5)
    .map((f) => `- ${f.name}: ${f.error.substring(0, 100)}`)
    .join('\n');

  const payload = {
    attachments: [
      {
        color,
        title: `Smoke Tests ${status} - ${config.environment}`,
        fields: [
          { title: 'Passed', value: String(result.passed), short: true },
          { title: 'Failed', value: String(result.failed), short: true },
          { title: 'Duration', value: `${(result.duration / 1000).toFixed(1)}s`, short: true },
          { title: 'Environment', value: config.environment, short: true },
        ],
        text: result.failed > 0 ? `Failures:\n${failureDetails}` : undefined,
        footer: `Smoke Suite | ${new Date().toISOString()}`,
      },
    ],
  };

  await fetch(config.slackWebhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}

export async function triggerPagerDuty(result: SmokeResult): Promise<void> {
  const config = getSmokeConfig();
  if (!config.pagerDutyRoutingKey || result.failed === 0) return;

  const payload = {
    routing_key: config.pagerDutyRoutingKey,
    event_action: 'trigger',
    payload: {
      summary: `Production smoke tests failed: ${result.failed} failures on ${config.environment}`,
      severity: result.failed > 3 ? 'critical' : 'error',
      source: `smoke-suite-${config.environment}`,
      custom_details: {
        passed: result.passed,
        failed: result.failed,
        failures: result.failures.map((f) => f.name),
      },
    },
  };

  await fetch('https://events.pagerduty.com/v2/enqueue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
```

## CI/CD Integration

### GitHub Actions Post-Deployment Smoke

```yaml
name: Post-Deployment Smoke Tests

on:
  deployment_status:
    types: [success]

jobs:
  smoke:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        working-directory: smoke-tests
        run: npm ci

      - name: Install Playwright browsers
        working-directory: smoke-tests
        run: npx playwright install chromium --with-deps

      - name: Run smoke tests
        working-directory: smoke-tests
        env:
          SMOKE_BASE_URL: ${{ github.event.deployment_status.target_url }}
          SMOKE_ACCOUNT_EMAIL: ${{ secrets.SMOKE_ACCOUNT_EMAIL }}
          SMOKE_ACCOUNT_PASSWORD: ${{ secrets.SMOKE_ACCOUNT_PASSWORD }}
          SMOKE_API_TOKEN: ${{ secrets.SMOKE_API_TOKEN }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          SMOKE_ENV: production
        run: npx playwright test

      - name: Upload failure artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: smoke-failure-artifacts
          path: smoke-tests/test-results/
          retention-days: 7

      - name: Trigger rollback on failure
        if: failure()
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"action": "rollback", "deployment_id": "${{ github.event.deployment.id }}"}' \
            https://api.example.com/deployments/rollback
```

### Docker-Based Smoke Runner

Package your smoke suite as a Docker image for consistent execution across environments:

```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /smoke-tests

COPY package*.json ./
RUN npm ci

COPY . .

ENV CI=true

CMD ["npx", "playwright", "test"]
```

Run the containerized smoke suite against any target URL:

```typescript
// scripts/run-smoke-docker.ts
import { execSync } from 'child_process';

const baseUrl = process.argv[2];
if (!baseUrl) {
  console.error('Usage: tsx run-smoke-docker.ts <base-url>');
  process.exit(1);
}

try {
  execSync(
    `docker run --rm \
      -e SMOKE_BASE_URL=${baseUrl} \
      -e SMOKE_ENV=production \
      -v $(pwd)/test-results:/smoke-tests/test-results \
      smoke-tests:latest`,
    { stdio: 'inherit' }
  );
  console.log('Smoke tests passed');
  process.exit(0);
} catch {
  console.error('Smoke tests failed');
  process.exit(1);
}
```

## Scheduled Smoke Monitoring

Run smoke tests on a cron schedule to catch production issues before users report them. This catches problems caused by infrastructure changes, certificate expirations, or third-party outages that happen independently of your deployments:

```typescript
// scripts/scheduled-smoke.ts
import { execSync } from 'child_process';
import { readFileSync } from 'fs';
import { sendSlackAlert, triggerPagerDuty } from '../src/helpers/alerting';

interface PlaywrightJsonReport {
  stats: {
    expected: number;
    unexpected: number;
    skipped: number;
    duration: number;
  };
  suites: Array<{
    specs: Array<{
      title: string;
      ok: boolean;
      tests: Array<{
        results: Array<{
          error?: { message: string };
        }>;
      }>;
    }>;
  }>;
}

async function runScheduledSmoke(): Promise<void> {
  const startTime = Date.now();

  try {
    execSync('npx playwright test --reporter=json', {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        ...process.env,
        PLAYWRIGHT_JSON_OUTPUT_NAME: 'smoke-results.json',
      },
    });
  } catch {
    // Test failures cause non-zero exit code; we handle results via the report file
  }

  const duration = Date.now() - startTime;

  try {
    const report: PlaywrightJsonReport = JSON.parse(
      readFileSync('smoke-results.json', 'utf-8')
    );

    const failures: Array<{ name: string; error: string }> = [];
    for (const suite of report.suites) {
      for (const spec of suite.specs) {
        if (!spec.ok) {
          const errorMsg = spec.tests[0]?.results[0]?.error?.message || 'Unknown error';
          failures.push({ name: spec.title, error: errorMsg });
        }
      }
    }

    const result = {
      passed: report.stats.expected,
      failed: report.stats.unexpected,
      skipped: report.stats.skipped,
      duration,
      failures,
      environment: process.env.SMOKE_ENV || 'production',
      url: process.env.SMOKE_BASE_URL || '',
    };

    await sendSlackAlert(result);

    if (result.failed > 0) {
      await triggerPagerDuty(result);
    }
  } catch (parseError) {
    console.error('Failed to parse smoke results:', parseError);
  }
}

runScheduledSmoke();
```

## Canary Deployment Verification

For teams using canary or blue-green deployment strategies, smoke tests can verify the canary instance before promoting it to receive full traffic:

```typescript
// src/helpers/canary-verifier.ts

interface CanaryConfig {
  canaryUrl: string;
  stableUrl: string;
  healthEndpoint: string;
  maxLatencyDifferenceMs: number;
  requiredSuccessRate: number;
}

export async function verifyCanary(config: CanaryConfig): Promise<{
  canaryHealthy: boolean;
  latencyComparison: { canary: number; stable: number; difference: number };
  recommendation: 'promote' | 'rollback' | 'investigate';
}> {
  const canaryLatencies: number[] = [];
  const stableLatencies: number[] = [];
  const probeCount = 5;

  for (let i = 0; i < probeCount; i++) {
    const canaryStart = Date.now();
    const canaryResponse = await fetch(`${config.canaryUrl}${config.healthEndpoint}`);
    canaryLatencies.push(Date.now() - canaryStart);

    const stableStart = Date.now();
    const stableResponse = await fetch(`${config.stableUrl}${config.healthEndpoint}`);
    stableLatencies.push(Date.now() - stableStart);

    if (!canaryResponse.ok) {
      return {
        canaryHealthy: false,
        latencyComparison: { canary: 0, stable: 0, difference: 0 },
        recommendation: 'rollback',
      };
    }

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  const avgCanary = canaryLatencies.reduce((a, b) => a + b, 0) / canaryLatencies.length;
  const avgStable = stableLatencies.reduce((a, b) => a + b, 0) / stableLatencies.length;
  const difference = avgCanary - avgStable;

  let recommendation: 'promote' | 'rollback' | 'investigate';
  if (difference > config.maxLatencyDifferenceMs) {
    recommendation = 'investigate';
  } else if (avgCanary > avgStable * 2) {
    recommendation = 'rollback';
  } else {
    recommendation = 'promote';
  }

  return {
    canaryHealthy: true,
    latencyComparison: {
      canary: Math.round(avgCanary),
      stable: Math.round(avgStable),
      difference: Math.round(difference),
    },
    recommendation,
  };
}
```

## Best Practices

1. **Keep the suite under 2 minutes total execution time.** If it takes longer, you have too many tests or tests that are too slow. A smoke suite should contain 10-25 focused tests, not hundreds.

2. **Use dedicated smoke test accounts.** Never use real user credentials. Create service accounts with limited permissions specifically for smoke testing. Rotate credentials regularly and store them in your secrets manager.

3. **Mark smoke test traffic explicitly.** Add custom headers like `X-Smoke-Test: true` or use dedicated user agents. This allows your monitoring tools to filter out smoke traffic from real user metrics and prevents smoke tests from polluting analytics data.

4. **Test the deployment, not the test environment.** Smoke tests should target the actual deployment URL, not a pre-production environment. If your deployment platform provides a unique preview URL per deployment, use that.

5. **Implement graceful degradation for third-party checks.** If a third-party service is down, your smoke suite should report a warning, not fail the entire deployment. Distinguish between first-party failures that block deployment and third-party failures that warrant a warning.

6. **Capture screenshots and traces only on failure.** Recording screenshots and traces for every test wastes resources and slows execution. Configure Playwright to capture these artifacts only when a test fails.

7. **Use API-level checks where possible.** Browser-based tests are slower and more brittle than API checks. If you can verify a critical path with an HTTP request instead of a full browser interaction, prefer the API approach.

8. **Run smoke tests on a schedule, not just after deployments.** Production issues can emerge from infrastructure changes, certificate expirations, database migrations, or third-party outages that happen independently of your deployments.

9. **Integrate with your incident management system.** Failed smoke tests should trigger PagerDuty alerts, Slack notifications, or whatever your team uses for incident response. Do not rely on engineers manually checking CI dashboards.

10. **Version your smoke test configuration.** Store all smoke test code, configuration, and pipeline definitions in version control. Treat smoke tests as production infrastructure code with the same review and deployment rigor.

11. **Never test write operations against production.** If your smoke suite must verify a form submission or API write, use a sandboxed endpoint or a mock mode. Accidentally creating real orders or sending real emails from smoke tests is a common and costly mistake.

12. **Use health check endpoints as the first gate.** Before running browser-based smoke tests, verify that the application's health endpoints return healthy. If the health check fails, skip the more expensive browser tests and report immediately.

## Anti-Patterns to Avoid

**Running the full regression suite as a smoke suite.** This defeats the purpose. A 30-minute regression suite is not a smoke test. Extract only the critical paths into a dedicated, lightweight smoke suite with a strict time budget.

**Testing implementation details instead of user outcomes.** Smoke tests should verify that users can accomplish critical tasks, not that specific DOM elements have specific CSS classes. Assertions should be about functionality, not about internal implementation choices.

**Ignoring flaky smoke tests.** A flaky smoke test is worse than no smoke test because it erodes trust in the entire suite. When a smoke test becomes flaky, either fix it immediately or remove it until the root cause is resolved. There is no middle ground.

**Hard-coding URLs and selectors.** Use environment variables for base URLs and data-testid attributes for element selection. Hard-coded URLs break when deployment targets change; hard-coded CSS selectors break with every UI refactor.

**Running smoke tests only in CI.** Developers should be able to run the smoke suite locally against any environment. This enables pre-deployment validation and faster debugging when smoke tests fail in CI.

**Sharing state between smoke tests.** Tests that depend on execution order, such as "create user" must run before "user can login," are fragile and fail unpredictably when parallelized. Each test must be completely self-contained.

**Not having a rollback mechanism.** Smoke tests without automated rollback are just monitoring with extra steps. The primary value of post-deployment smoke tests is their ability to trigger automatic rollback before users are affected.

**Over-testing error paths in smoke suites.** Smoke tests verify that happy paths work. Error handling, edge cases, and validation rules belong in the regression suite. Every test in the smoke suite should exercise the golden path of a critical feature.

## Debugging Tips

**Smoke tests pass locally but fail in CI.** Check for differences in network configuration, DNS resolution, and SSL certificates. CI runners may not have access to your production network. Verify that environment variables are correctly propagated to the test runner. Also check if your production environment has IP-based rate limiting that blocks CI runner IP addresses.

**Inconsistent timeouts across runs.** Production latency varies based on traffic patterns, geographic distance, and server load. Increase your default timeout to accommodate peak traffic periods. Use Playwright's `expect` timeout separately from the navigation timeout, and set both generously for smoke tests running against production.

**Authentication tests fail intermittently.** Rate limiting, CAPTCHA challenges, and bot detection systems may block smoke test logins. Work with your security team to whitelist your smoke test IP addresses or user agents. Consider using API-based authentication with tokens instead of form-based login.

**Tests fail after a CDN cache purge.** CDN edge caches may take several minutes to populate after a deployment. Add a short delay or retry loop for the first request to accommodate cache warming. Alternatively, bypass the CDN for smoke tests by hitting the origin server directly.

**Screenshots show blank pages.** This often indicates that JavaScript failed to load or execute. Check the browser console for errors by adding `page.on('console', msg => console.log(msg.text()))` and `page.on('pageerror', err => console.error(err))` to your test setup.

**Third-party status checks are unreliable.** External status APIs can be slow or rate-limited. Set aggressive timeouts for third-party checks (5 seconds maximum) and do not allow them to block deployment decisions. Log warnings for slow third-party responses so you can track degradation trends over time.

**Docker-based smoke runner cannot resolve internal DNS.** When running smoke tests in Docker, ensure the container uses the correct DNS resolver. Use `--network=host` during local testing or configure the container's DNS settings appropriately for your CI environment.
