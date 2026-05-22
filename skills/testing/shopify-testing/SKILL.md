---
name: shopify-testing
description: Guide for testing Shopify Apps, including Unit Testing with Remix, Mocking Shopify Context, and E2E Testing.
---

# Shopify App Testing

Reliable testing is crucial for ensuring your app handles Shopify's authentication and API quirks correctly.

## 1. Unit & Integration Testing (Vitest + Remix)

Use **Vitest** for running unit and integration tests in the Remix environment.

### Setup
Install dependencies:
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

### Mocking `shopify.server.ts`
Creating a mock for the `authenticate` object is critical for testing loaders and actions without hitting real Shopify APIs.

```typescript
// test/mocks/shopify.ts
import { vi } from 'vitest';

export const mockShopify = {
  authenticate: {
    admin: vi.fn(),
    public: vi.fn(),
    webhook: vi.fn(),
  },
};

// Usage in test file:
vi.mock('../app/shopify.server', () => mockShopify);

test('loader returns data for authenticated shop', async () => {
    mockShopify.authenticate.admin.mockResolvedValue({
        currentShop: 'test-shop.myshopify.com',
        session: { shop: 'test-shop.myshopify.com', accessToken: 'fake_token' },
        admin: {
             graphql: vi.fn().mockResolvedValue({ /* mock response */ })
        }
    });

    const response = await loader({ request: new Request('http://localhost/') });
    // Assertions...
});
```

## 2. Testing Loaders & Actions

Using Remix's `createRemixStub` or calling loaders/actions directly is the best way to test backend logic.

### Direct Function Call (Preferred for logic)
You can import the `loader` or `action` and call it directly with a mock Request.

```typescript
import { loader } from '../app/routes/app.dashboard';

test('dashboard loader returns stats', async () => {
   // Setup mocks...
   const response = await loader({ 
       request: new Request('http://localhost/app/dashboard'), 
       params: {} 
   });
   const data = await response.json();
   expect(data.stats).toBeDefined();
});
```

## 3. End-to-End (E2E) Testing (Playwright)

For E2E tests, you need to handle the OAuth flow or bypass it using session tokens.

### Bypassing Auth (Session Token)
The most stable way to E2E test embedded apps is to generate a valid session token (or mock the validation) so you don't have to automate the Login screen interaction which often triggers captchas.

### Basic Playwright Test
```typescript
import { test, expect } from '@playwright/test';

test('load dashboard', async ({ page }) => {
  await page.goto('http://localhost:3000/app');
  // Expect to see the Polaris Page title
  await expect(page.locator('.Polaris-Page-Header__Title')).toHaveText('Dashboard');
});

```

## 4. Testing Webhooks

To test webhooks locally:

1.  **Trigger via Shopify CLI**: `shopify app webhook trigger --topic ORDERS_CREATE`
2.  **Unit Test**: Import the webhook action and pass a mock Request with the correct HMAC header.

```typescript
import { action } from '../app/routes/webhooks';
import crypto from 'crypto';

test('webhook verifies hmac', async () => {
    const payload = JSON.stringify({ id: 123 });
    const hmac = crypto.createHmac('sha256', 'FULL_SECRET').update(payload).digest('base64');
    
    const request = new Request('http://localhost/webhooks', {
        method: 'POST',
        body: payload,
        headers: { 'X-Shopify-Hmac-Sha256': hmac }
    });

    // Mock authenticate.webhook to succeed
    // ...
    
    const response = await action({ request });
    expect(response.status).toBe(200);
});
```
