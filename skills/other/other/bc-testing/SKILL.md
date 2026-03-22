---
name: bc-testing
description: Test BigCommerce integrations — API testing, Stencil theme testing, Cypress/Playwright E2E tests, webhook testing, and sandbox stores. Use when writing tests for BigCommerce apps, themes, or integrations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Testing

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com testing` for testing guidance
2. Web-search `bigcommerce stencil theme testing` for theme testing patterns
3. Web-search `bigcommerce api testing sandbox` for sandbox store setup

## Testing Environments

### Sandbox Stores

BigCommerce provides sandbox/trial stores for testing:
- Free trial stores (limited time)
- Partner sandbox stores (BigCommerce Partner Program)
- Use for: API testing, theme development, app development
- Never test against production stores

### Test vs Production Credentials

- Create separate API credentials for test environments
- Use test/sandbox mode for payment gateways (Stripe test keys, PayPal sandbox)
- Use different webhook endpoints for test environments

## API Testing

### Testing REST API Calls

Use tools like Postman, Insomnia, or `curl`:
```bash
curl -X GET \
  https://api.bigcommerce.com/stores/{hash}/v3/catalog/products \
  -H 'X-Auth-Token: {token}' \
  -H 'Accept: application/json'
```

### Automated API Tests

Write integration tests that exercise the BigCommerce API:

```javascript
// Jest/Vitest example
describe('Products API', () => {
  it('should create a product', async () => {
    const response = await fetch(`${API_URL}/v3/catalog/products`, {
      method: 'POST',
      headers: { 'X-Auth-Token': TOKEN, 'Content-Type': 'application/json' },
      body: JSON.stringify([{ name: 'Test Product', type: 'physical', price: 9.99, weight: 1 }]),
    });
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.data[0].name).toBe('Test Product');
    // Cleanup: delete the test product
  });
});
```

### Testing Rate Limits

- Monitor `X-Rate-Limit-Requests-Left` header in tests
- Add delays between rapid API calls
- Test your retry/backoff logic

### Testing Pagination

- Create enough test data to exceed one page
- Verify your pagination logic handles `pageInfo` / `meta.pagination` correctly
- Test edge cases: empty results, last page, single item

## GraphQL Testing

### GraphQL Playground

Use GraphQL explorers to test queries:
- Apollo Studio, GraphQL Playground, or `graphql-request` library
- Storefront API endpoint: `https://{store_url}/graphql`
- Include `Authorization: Bearer {storefront_token}` header

### Automated GraphQL Tests

```javascript
describe('GraphQL Storefront', () => {
  it('should fetch products', async () => {
    const query = `{ site { products(first: 5) { edges { node { name entityId } } } } }`;
    const response = await fetch(`${STORE_URL}/graphql`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${STOREFRONT_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const { data } = await response.json();
    expect(data.site.products.edges.length).toBeGreaterThan(0);
  });
});
```

## Stencil Theme Testing

### Local Testing with Stencil CLI

`stencil start` provides a local development server:
- Live reload on template/SCSS/JS changes
- Proxies API data from your BigCommerce store
- Test theme changes locally before pushing

### Visual Testing

- Test across theme variations (`config.json` variations)
- Test responsive layouts at multiple breakpoints
- Verify dynamic content (front matter data injection)
- Test with different product types, category structures

### Theme Bundle Validation

`stencil bundle` validates the theme before upload:
- Checks template syntax
- Validates config.json and schema.json
- Reports errors and warnings

## Webhook Testing

### Local Webhook Testing

Use tunneling tools for local webhook development:
- `ngrok http 3000` — expose local port to public URL
- Register the ngrok URL as webhook destination
- Trigger events in BigCommerce admin (create order, update product)
- Inspect webhook payloads in your local handler

### Webhook Replay

Log all webhook payloads during development for replay testing:
- Store raw request body and headers
- Replay recorded payloads in tests
- Test idempotency (replay same webhook multiple times)

## E2E Testing

### Playwright/Cypress

Test complete user flows against a running BigCommerce store:

```javascript
// Playwright example
test('complete purchase flow', async ({ page }) => {
  await page.goto('/products/test-product');
  await page.click('button:has-text("Add to Cart")');
  await page.goto('/cart');
  await page.click('a:has-text("Proceed to Checkout")');
  // Fill checkout fields...
  await page.click('button:has-text("Place Order")');
  await expect(page.locator('.order-confirmation')).toBeVisible();
});
```

### What to Test E2E

- Product browsing and search
- Add to cart and cart management
- Full checkout flow (with test payment gateway)
- Customer registration and login
- My Account pages (orders, addresses, wishlists)
- Responsive design across viewports

## App Testing

### OAuth Flow Testing

- Test install callback with valid and invalid auth codes
- Test load callback JWT verification
- Test uninstall callback cleanup
- Test with multiple stores (different store hashes)

### Webhook Subscription Testing

- Verify webhook creation via API
- Test webhook handler with sample payloads
- Test retry handling (return non-200 to trigger retry)
- Test deactivation recovery

## Best Practices

- Use sandbox stores — never test destructively against production
- Clean up test data after each test run
- Test rate limit handling and backoff logic
- Mock external APIs (payment gateways) in unit tests
- Use real BigCommerce APIs in integration tests
- Test with different store configurations (tax, currency, shipping)
- Use ngrok/tunnels for webhook development
- Validate API responses against expected schemas
- Test error paths — invalid data, missing fields, auth failures

Fetch the BigCommerce developer documentation for current testing guidance, sandbox store setup, and API testing patterns before implementing.
