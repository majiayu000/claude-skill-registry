---
name: e2e-testing-patterns
description: E2E test design patterns for reliable, fast test suites. Use when implementing E2E tests, debugging flaky tests, or establishing testing standards.
---

# E2E Testing Patterns

## Framework Selection

| Factor | Playwright | Cypress |
|--------|-----------|---------|
| **Multi-browser** | Chromium, Firefox, WebKit | Chromium only (natively) |
| **Multi-tab/origin** | Yes | No |
| **Speed** | Faster (parallel by default) | Slower (single-threaded) |
| **API testing** | Built-in `request` context | `cy.request()` |
| **Mobile emulation** | Device profiles built-in | Viewport only |
| **Best for** | Cross-browser, complex flows | Simple apps, quick setup |

**Default choice**: Playwright. Use Cypress only if team already has investment.

## What to E2E Test

**Do test:**
- Critical user journeys (login, checkout, signup, payment)
- Flows crossing multiple services/pages
- Auth flows (OAuth, MFA, session expiry)
- Cross-browser rendering of critical pages

**Do NOT test:**
- Every edge case (too slow -- use unit tests)
- API contracts (use integration tests)
- Visual styling details (use visual regression separately)
- Internal state management

**Rule of thumb**: If it's in the "happy path" a user follows to give you money, E2E test it.

## Test Design Patterns

### Page Object Model
- Encapsulate page interactions in classes
- Tests read like user stories, not DOM manipulation
- One page object per page/component boundary
- Page objects return other page objects for navigation flows

### Selector Strategy (Priority Order)
1. `getByRole` -- accessible, resilient to refactors
2. `getByLabel` -- form elements
3. `getByText` -- visible content
4. `getByTestId` -- last resort

**Never use**: CSS classes, nth-child, complex XPath, DOM structure

### Test Data Management
- Each test creates its own data (API calls in `beforeEach` or fixtures)
- Never depend on data from another test
- Clean up after yourself -- or use isolated test accounts
- Use unique identifiers (timestamps, UUIDs) to avoid collisions in parallel runs

## Flaky Test Prevention

### Waiting Strategy
```
BAD:  page.waitForTimeout(3000)
GOOD: await expect(element).toBeVisible()
GOOD: await page.waitForURL('/dashboard')
GOOD: await page.waitForResponse(resp => resp.url().includes('/api/users'))
```

- Never use fixed timeouts -- they're either too long (slow) or too short (flaky)
- Auto-waiting assertions (`toBeVisible`, `toBeEnabled`) handle timing naturally
- Wait for specific network responses when testing after API calls

### Network Determinism
- Mock third-party services (Stripe, analytics, etc.)
- Use `page.route()` / `cy.intercept()` for deterministic API responses
- Test loading states by delaying mocked responses
- Test error states by returning error responses

### Parallel Execution
- Tests must be fully independent (no shared state)
- Use unique test users/data per worker
- Shard across CI machines: `npx playwright test --shard=1/4`

## CI Integration Opinions

### Configuration
- **Retries**: 0 locally, 2 in CI (masks flakiness locally, handles CI flakiness)
- **Workers**: Auto locally, 1 in CI (predictable resource usage)
- **Traces/screenshots**: On failure only (saves storage)
- **Video**: Off by default, retain on failure only

### Pipeline Strategy
- Run E2E after unit + integration tests pass (fail fast on cheaper tests)
- E2E against deployed staging, not localhost
- Set hard timeout (10-15 min) -- if E2E takes longer, you have too many
- Keep suite under 50 tests -- decompose into integration tests when growing

## Debugging Failed Tests

1. **Trace viewer**: `npx playwright show-trace trace.zip` -- step through every action
2. **Headed mode**: `npx playwright test --headed` -- watch it happen
3. **Debug mode**: `npx playwright test --debug` -- step with inspector
4. **`page.pause()`**: Insert in test to pause at that point
5. **`test.step()`**: Break test into named steps for better reporting

## API Mock Patterns

### Contract-Based Mocking
Generate mocks from OpenAPI specs when available. Validate responses against the contract to catch drift between mock and real API.

### Scenario-Based Mocking
Define named scenarios for deterministic test behavior:

| Scenario | Purpose | Implementation |
|----------|---------|---------------|
| Happy path | Standard flow | 200 responses with valid data |
| Error handling | Error UI/retry logic | 4xx/5xx responses |
| Degraded performance | Timeout/loading states | Delayed responses (5s+) |
| Rate limiting | Throttle behavior | 200 for N requests, then 429 |

### Request Verification
```typescript
// Playwright route mocking with verification
const apiCalls: Request[] = []

await page.route('**/api/users/**', async (route) => {
  apiCalls.push(route.request())
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ id: '123', name: 'Test User' }),
  })
})

// ... perform UI actions ...

// Assert API was called correctly
expect(apiCalls).toHaveLength(1)
expect(apiCalls[0].method()).toBe('GET')
```

### Mock Boundaries
- Mock third-party services (Stripe, analytics, auth providers) -- always
- Mock your own API -- only for specific error/edge scenarios
- Never mock everything in E2E -- defeats the purpose

## Anti-Patterns

- **Test coupling**: Test B depends on state from Test A
- **Sleeping**: `waitForTimeout` instead of condition-based waits
- **Over-mocking in E2E**: If you mock everything, you're not testing E2E
- **Testing through UI when API suffices**: Use API to set up state, UI only for the flow under test
- **Screenshot comparisons without thresholds**: Pixel-perfect matching is inherently flaky
- **Ignoring flaky tests**: Fix or delete them. A flaky test suite is worse than no suite.
