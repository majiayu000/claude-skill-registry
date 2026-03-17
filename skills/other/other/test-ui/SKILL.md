---
name: test:ui
description: Write and run Playwright UI E2E tests for Kagenti - login, navigation, agent chat, across CI/Kind/HyperShift
---

# Playwright UI Tests

Write and run Playwright UI E2E tests for the Kagenti UI across all environments.

> **Not to be confused with `test:playwright`** which is for recording narrated demo videos.
> This skill is for functional UI testing (login, navigate, interact, assert).

## Test Location

```
kagenti/ui-v2/
├── e2e/
│   ├── agent-chat.spec.ts     # Login -> agent -> chat flow
│   ├── agent-catalog.spec.ts  # Agent listing page
│   ├── tool-catalog.spec.ts   # Tool listing page
│   └── home.spec.ts           # Home page
├── playwright.config.ts       # Playwright config (baseURL, webServer)
└── package.json               # npm run test:e2e
```

## Writing Tests

### Login Helper

All tests should handle Keycloak login when auth is enabled:

```typescript
import { test, expect, Page } from '@playwright/test';

const KEYCLOAK_USER = process.env.KEYCLOAK_USER || 'admin';
const KEYCLOAK_PASSWORD = process.env.KEYCLOAK_PASSWORD || 'admin';

async function loginIfNeeded(page: Page) {
  await page.waitForLoadState('networkidle', { timeout: 15000 });
  const isKeycloakLogin = await page.locator('#kc-form-login, #username, input[name="username"]')
    .first().isVisible({ timeout: 3000 }).catch(() => false);
  if (isKeycloakLogin) {
    await page.locator('#username, input[name="username"]').first().fill(KEYCLOAK_USER);
    await page.locator('#password, input[name="password"]').first().fill(KEYCLOAK_PASSWORD);
    await page.locator('#kc-login, input[type="submit"]').first().click();
    await page.waitForURL(/^(?!.*keycloak)/, { timeout: 15000 });
    await page.waitForLoadState('networkidle');
  }
}
```

### Test Pattern

```typescript
test('should login and interact with agent', async ({ page }) => {
  test.setTimeout(120000); // LLM calls can be slow

  await page.goto('/agents');
  await loginIfNeeded(page);

  // Navigate
  await expect(page.getByRole('heading', { name: /Agent Catalog/i })).toBeVisible();
  await page.getByRole('link', { name: /weather-service/i }).click();

  // Interact
  await page.getByPlaceholder('Type your message...').fill('What is the weather?');
  await page.getByRole('button', { name: /Send/i }).click();

  // Assert response
  await expect(page.locator('text=/weather|temperature/i').first())
    .toBeVisible({ timeout: 90000 });
});
```

### Selector Patterns

| Element | Selector |
|---------|----------|
| Chat input | `page.getByPlaceholder('Type your message...')` |
| Send button | `page.getByRole('button', { name: /Send/i })` |
| Agent link | `page.getByRole('link', { name: /weather-service/i })` |
| Page heading | `page.getByRole('heading', { name: /Agent Catalog/i })` |
| Namespace selector | `page.locator('[aria-label="Select namespace"]')` |
| Status badge | `page.locator('.pf-v5-c-label')` |
| Import button | `page.getByRole('button', { name: /Import Agent/i })` |

### Timeouts

| Operation | Timeout | Reason |
|-----------|---------|--------|
| Page load | 15s | Network + Keycloak init |
| API response | 30s | Backend query |
| LLM response | 90s | Ollama inference + tool calls |
| Full test | 120s | End-to-end including chat |

## Running Tests

### On Kind (local)

```bash
# Prerequisites: Kind cluster running, backend port-forwarded
kubectl port-forward -n kagenti-system svc/kagenti-backend 8000:8000 &

cd kagenti/ui-v2
npm ci
npx playwright install chromium

npm run test:e2e              # Headless (starts Vite dev server)
npm run test:e2e:ui           # Interactive Playwright UI
npm run test:e2e:debug        # Debug mode
npx playwright test agent-chat.spec.ts  # Single file
```

The Vite dev server starts automatically and proxies `/api` to `localhost:8000`.

### On HyperShift

```bash
export CLUSTER=<suffix> MANAGED_BY_TAG=${MANAGED_BY_TAG:-kagenti-hypershift-custom}
export KUBECONFIG=~/clusters/hcp/$MANAGED_BY_TAG-$CLUSTER/auth/kubeconfig

# Get UI URL from OpenShift route
KAGENTI_UI_URL="https://$(kubectl get route kagenti-ui -n kagenti-system -o jsonpath='{.spec.host}')"

cd kagenti/ui-v2
npm ci
npx playwright install chromium

KAGENTI_UI_URL="$KAGENTI_UI_URL" npx playwright test
KAGENTI_UI_URL="$KAGENTI_UI_URL" npm run test:e2e:ui  # Interactive
```

**HyperShift notes:**
- Always set `KAGENTI_UI_URL` to the OpenShift route (no dev server needed)
- May need `PLAYWRIGHT_IGNORE_HTTPS_ERRORS=1` for self-signed certs
- Keycloak credentials: `kubectl get secret keycloak-initial-admin -n keycloak -o jsonpath='{.data.password}' | base64 -d`

### In CI

CI step `91-run-ui-tests.sh` runs after pytest E2E tests:

1. Installs npm dependencies + Playwright chromium
2. Starts Vite dev server (proxies to port-forwarded backend)
3. Runs `npx playwright test`
4. Uploads `playwright-report/` as artifact

### Analyzing CI Failures

```bash
# Download Playwright report
gh run download <run-id> -n e2e-test-results -D /tmp/test-results

# Open HTML report
npx playwright show-report /tmp/test-results/kagenti/ui-v2/playwright-report
```

## Related Skills

- **`test:playwright`** - Playwright demo video tests (different purpose)
- **`test:write`** - General E2E test writing patterns
- **`test:review`** - Review test quality
- **`tdd:ci`** - CI-driven TDD (invokes this skill for UI tests)
- **`tdd:kind`** - Kind TDD (invokes this skill for UI tests)
- **`tdd:hypershift`** - HyperShift TDD (invokes this skill for UI tests)
- **`kagenti:ui-debug`** - Debug UI issues (502, proxy, auth)
