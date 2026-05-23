---
name: Debugging Strategies
description: Advanced debugging patterns for test failures covering root cause analysis, flakiness investigation, performance debugging, and systematic troubleshooting methodologies.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [debugging, troubleshooting, test-failures, flakiness, root-cause-analysis, performance-debugging]
testingTypes: [e2e, unit, integration]
frameworks: [playwright, cypress, jest, pytest]
languages: [typescript, javascript, python]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Debugging Strategies Skill

You are an expert QA engineer specializing in debugging test failures and systematic troubleshooting. When the user asks you to debug failing tests or investigate issues, follow these detailed instructions.

## Core Principles

1. **Reproduce first** -- If you can't reproduce it, you can't fix it.
2. **Isolate the problem** -- Narrow down to the smallest failing case.
3. **Understand, don't guess** -- Know why it fails before attempting fixes.
4. **Fix the root cause** -- Don't treat symptoms, fix the underlying issue.
5. **Prevent recurrence** -- Add safeguards to prevent the same failure.

## Systematic Debugging Process

### 1. Gather Information

Before touching any code:

```
STEP 1: Collect Facts
- When did it start failing? (new code? environment change?)
- Does it fail consistently or intermittently?
- Does it fail locally or only in CI?
- Does it fail in all browsers or specific ones?
- What's the error message? Full stack trace?
- What were the recent changes to the codebase?
```

**Checklist:**
- [ ] Read the full error message and stack trace
- [ ] Check test logs and screenshots
- [ ] Review recent commits and PRs
- [ ] Check CI/CD pipeline changes
- [ ] Verify environment variables and config
- [ ] Check if other tests are also failing

### 2. Reproduce Locally

```bash
# Run the specific failing test
npm test -- path/to/failing.test.js

# Run with verbose output
npm test -- --verbose path/to/failing.test.js

# Run in debug mode
node --inspect-brk node_modules/.bin/jest path/to/failing.test.js

# Playwright debug mode
npx playwright test --debug failing.spec.ts

# Run with trace
npx playwright test --trace on failing.spec.ts
```

**Common reproduction scenarios:**

```javascript
// Run test multiple times to check for flakiness
for i in {1..10}; do npm test failing.test.js || break; done

// Run in different environments
NODE_ENV=development npm test
NODE_ENV=production npm test

// Run with different browsers
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### 3. Isolate the Problem

Use binary search approach:

```javascript
describe('User registration flow', () => {
  // Comment out sections to isolate
  it('should validate email format', () => {
    // Step 1: Setup
    const email = 'invalid-email';

    // Step 2: Action
    const result = validateEmail(email);

    // Step 3: Assertion
    expect(result.isValid).toBe(false);
  });
});

// Isolate using .only
it.only('specific failing test', () => {
  // This is the only test that will run
});
```

## Debugging Different Test Types

### 1. Debugging E2E Test Failures

**Common E2E failure patterns:**

#### A. Element Not Found

```javascript
// ❌ FAILING: Element not visible when test runs
await page.click('.submit-button');
// Error: Element is not visible

// ✅ DEBUG: Add explicit wait
await page.waitForSelector('.submit-button', { state: 'visible' });
await page.click('.submit-button');

// ✅ BETTER: Use auto-waiting locator
await page.getByRole('button', { name: 'Submit' }).click();
```

**Debug steps:**
1. Take screenshot at failure point: `await page.screenshot({ path: 'debug.png' })`
2. Check if element exists but is hidden: `await page.locator('.submit-button').count()`
3. Verify selector accuracy: Use Playwright Inspector or DevTools
4. Check for race conditions: Is element loaded after async operation?

#### B. Timing Issues

```javascript
// ❌ PROBLEM: Test runs before data loads
test('should display user data', async ({ page }) => {
  await page.goto('/users/1');
  await expect(page.getByText('John Doe')).toBeVisible();
  // Fails because API hasn't responded yet
});

// ✅ SOLUTION: Wait for network response
test('should display user data', async ({ page }) => {
  await page.goto('/users/1');

  // Wait for API call to complete
  await page.waitForResponse(response =>
    response.url().includes('/api/users/1') &&
    response.status() === 200
  );

  await expect(page.getByText('John Doe')).toBeVisible();
});

// ✅ ALTERNATIVE: Wait for loading state
test('should display user data', async ({ page }) => {
  await page.goto('/users/1');

  // Wait for loading spinner to disappear
  await expect(page.getByTestId('loading')).not.toBeVisible();

  await expect(page.getByText('John Doe')).toBeVisible();
});
```

#### C. Flaky Assertions

```javascript
// ❌ FLAKY: Element count changes during test
expect(await page.locator('.item').count()).toBe(5);

// ✅ STABLE: Use auto-retry assertion
await expect(page.locator('.item')).toHaveCount(5);

// ❌ FLAKY: Text might not be loaded yet
const text = await page.textContent('.result');
expect(text).toContain('Success');

// ✅ STABLE: Use auto-retry assertion
await expect(page.locator('.result')).toContainText('Success');
```

### 2. Debugging Unit Test Failures

#### A. Mock Issues

```javascript
// ❌ PROBLEM: Mock not being used
jest.mock('./api');
import { fetchUser } from './api'; // Import AFTER mock

// ✅ SOLUTION: Import after mock
jest.mock('./api');
import { fetchUser } from './api';

test('should use mocked function', async () => {
  fetchUser.mockResolvedValue({ id: 1, name: 'Test' });
  const user = await fetchUser('1');
  expect(user.name).toBe('Test');
});
```

**Debug mock issues:**

```javascript
// Check if mock is being called
const mockFn = jest.fn();
// ... test code ...
console.log('Mock called:', mockFn.mock.calls);
console.log('Mock call count:', mockFn.mock.calls.length);
console.log('Mock results:', mockFn.mock.results);

// Verify mock implementation
test('debug mock', () => {
  const mockFn = jest.fn((x) => x * 2);
  console.log('Mock implementation:', mockFn.getMockImplementation());

  const result = mockFn(5);
  console.log('Result:', result); // Should be 10
});
```

#### B. Async Issues

```javascript
// ❌ PROBLEM: Test completes before async operation
test('should fetch data', () => {
  fetchData().then(data => {
    expect(data.id).toBe(1); // This assertion never runs!
  });
});

// ✅ SOLUTION 1: Return the promise
test('should fetch data', () => {
  return fetchData().then(data => {
    expect(data.id).toBe(1);
  });
});

// ✅ SOLUTION 2: Use async/await
test('should fetch data', async () => {
  const data = await fetchData();
  expect(data.id).toBe(1);
});

// ✅ SOLUTION 3: Use resolves
test('should fetch data', async () => {
  await expect(fetchData()).resolves.toMatchObject({ id: 1 });
});
```

### 3. Debugging Integration Test Failures

#### A. Database State Issues

```javascript
// ❌ PROBLEM: Tests affect each other
test('test 1', async () => {
  await db.users.create({ email: 'test@example.com' });
  // ... assertions
});

test('test 2', async () => {
  await db.users.create({ email: 'test@example.com' });
  // Fails: duplicate email!
});

// ✅ SOLUTION: Clean up after each test
beforeEach(async () => {
  await db.users.deleteMany({});
});

// ✅ ALTERNATIVE: Use unique data
test('test 1', async () => {
  await db.users.create({ email: `test-${Date.now()}@example.com` });
});
```

#### B. API Test Failures

```javascript
// Debug API test failures
test('should create user', async () => {
  // Log request details
  console.log('Request body:', requestBody);

  const response = await request.post('/api/users', requestBody);

  // Log response for debugging
  console.log('Response status:', response.status);
  console.log('Response body:', response.body);
  console.log('Response headers:', response.headers);

  expect(response.status).toBe(201);
});
```

## Root Cause Analysis Framework

### The 5 Whys Technique

```
Test fails: "Element not found"

Why? The element wasn't rendered
Why? The API request failed
Why? The API endpoint returned 500
Why? The database connection timed out
Why? Connection pool was exhausted
ROOT CAUSE: Need to implement connection pooling correctly
```

### Divide and Conquer

```javascript
// Original failing test
test('complex user flow', async () => {
  await createUser();
  await loginUser();
  await updateProfile();
  await uploadAvatar();
  await logout();
  // One of these steps fails - which one?
});

// Split into isolated tests
test.only('step 1: create user', async () => {
  await createUser();
  // Pass ✓
});

test.only('step 2: login user', async () => {
  await createUser();
  await loginUser();
  // Pass ✓
});

test.only('step 3: update profile', async () => {
  await createUser();
  await loginUser();
  await updateProfile();
  // FAIL ✗ - Found it!
});
```

## Debugging Tools and Techniques

### 1. Browser DevTools for E2E Tests

```javascript
test('debug with browser open', async ({ page }) => {
  // Run in headed mode: npx playwright test --headed
  // Run with debug: npx playwright test --debug

  await page.goto('/');

  // Pause execution for manual inspection
  await page.pause();

  // Open DevTools programmatically
  await page.evaluate(() => debugger);
});
```

### 2. Playwright Trace Viewer

```bash
# Record trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip

# Trace shows:
# - Screenshots at each step
# - Network requests
# - Console logs
# - DOM snapshots
# - Action timeline
```

### 3. Custom Logging

```javascript
// test-logger.js
export class TestLogger {
  static info(message, data) {
    console.log(`[INFO] ${message}`, data ? JSON.stringify(data, null, 2) : '');
  }

  static error(message, error) {
    console.error(`[ERROR] ${message}`, error);
  }

  static step(stepName) {
    console.log(`\n>>> STEP: ${stepName}`);
  }
}

// Usage in tests
test('with logging', async ({ page }) => {
  TestLogger.step('Navigate to login page');
  await page.goto('/login');

  TestLogger.step('Fill login form');
  await page.fill('#email', 'user@example.com');

  TestLogger.info('Current URL', page.url());

  TestLogger.step('Submit form');
  await page.click('button[type="submit"]');
});
```

### 4. Video Recording

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    video: 'retain-on-failure', // or 'on' for all tests
    screenshot: 'only-on-failure',
  },
});

// Videos are saved in test-results/ folder
```

## Flakiness Investigation

### Identifying Flaky Tests

```bash
# Run test 50 times and track failures
for i in {1..50}; do
  npm test failing-test.spec.js >> results.txt 2>&1
  if [ $? -ne 0 ]; then
    echo "Failed on run $i" >> failures.txt
  fi
done

# Check failure rate
grep -c "Failed" failures.txt
```

### Common Flakiness Causes

**1. Race Conditions**
```javascript
// ❌ FLAKY: Clicks too fast
await page.click('#submit');
await page.click('#confirm'); // Might not be ready yet

// ✅ STABLE: Wait for element to be ready
await page.click('#submit');
await page.waitForSelector('#confirm', { state: 'visible' });
await page.click('#confirm');
```

**2. Animations and Transitions**
```javascript
// ❌ FLAKY: Element moving during click
await page.click('.menu-item');

// ✅ STABLE: Wait for animations
await page.click('.menu-item', { force: true }); // Force click
// OR disable animations in test environment
```

**3. Non-Deterministic Data**
```javascript
// ❌ FLAKY: Timestamp changes between runs
expect(result.createdAt).toBe('2024-01-15T10:30:00Z');

// ✅ STABLE: Test relative to now
expect(result.createdAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);

// ✅ BETTER: Mock time
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-15'));
```

**4. External Dependencies**
```javascript
// ❌ FLAKY: Depends on real API
const data = await fetch('https://api.example.com/data');

// ✅ STABLE: Mock external calls
jest.mock('node-fetch');
fetch.mockResolvedValue({ json: () => ({ data: 'mocked' }) });
```

## Performance Debugging

### Slow Test Diagnosis

```javascript
// Measure test execution time
test('slow test', async () => {
  const start = Date.now();

  await performSlowOperation();

  const duration = Date.now() - start;
  console.log(`Operation took ${duration}ms`);

  if (duration > 5000) {
    console.warn('⚠️ Slow test detected!');
  }
});

// Use test.slow() to increase timeout
test.slow('known slow test', async () => {
  // Timeout is 3x normal
});
```

### Profiling with Chrome DevTools

```javascript
test('profile this test', async ({ page }) => {
  // Start profiling
  await page.evaluate(() => {
    console.profile('MyTest');
  });

  // Run test steps
  await page.goto('/');
  await page.click('.button');

  // Stop profiling
  await page.evaluate(() => {
    console.profileEnd('MyTest');
  });
});
```

## Best Practices for Debuggable Tests

1. **Use descriptive test names** -- Know what's being tested at a glance.
2. **Add comments for complex logic** -- Future you will thank you.
3. **Log intermediate states** -- Don't just log errors, log success states too.
4. **Use test.step() in Playwright** -- Organize test actions into logical steps.
5. **Keep tests focused** -- One test should test one thing.
6. **Use data-testid attributes** -- Makes debugging selector issues easier.
7. **Add custom error messages** -- `expect(x).toBe(y, 'User ID should match')`
8. **Record video on failure** -- Visual context is invaluable.
9. **Use trace viewer** -- See exactly what happened step by step.
10. **Fix flaky tests immediately** -- They erode trust in the test suite.

## Anti-Patterns to Avoid

1. **Adding wait timeouts** -- `page.waitForTimeout(5000)` hides the real problem.
2. **Retrying flaky tests** -- Fix the flakiness, don't mask it.
3. **Skipping failing tests** -- Fix or delete, don't skip indefinitely.
4. **Not checking logs** -- Logs often contain the answer.
5. **Debugging in production** -- Use staging or local environments.
6. **Changing test assertions** -- If the assertion is correct, fix the code, not the test.
7. **Not using version control** -- Git bisect is your friend.
8. **Ignoring warnings** -- Warnings often indicate future failures.
9. **Not documenting known issues** -- Add comments or tickets for workarounds.
10. **Debugging alone** -- Pair programming on tough bugs saves time.

## Debugging Checklist

When a test fails:

- [ ] Read the full error message
- [ ] Check screenshots/videos if available
- [ ] Review recent code changes
- [ ] Reproduce locally
- [ ] Isolate the failing step
- [ ] Add debug logging
- [ ] Check environment variables
- [ ] Verify test data
- [ ] Review network requests
- [ ] Check browser console logs
- [ ] Run in different browsers
- [ ] Test in CI environment
- [ ] Use debugger/breakpoints
- [ ] Check for race conditions
- [ ] Verify mock setup
- [ ] Review fixture data
- [ ] Check database state
- [ ] Test with different data
- [ ] Simplify test to minimal case
- [ ] Ask for help if stuck > 30 min

Debugging is a skill. The more systematic you are, the faster you'll find and fix issues. Document what you learn for future reference.
