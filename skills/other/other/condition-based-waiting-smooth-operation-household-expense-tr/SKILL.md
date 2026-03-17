---
name: condition-based-waiting
description: "Use when tests fail intermittently. Replace arbitrary timeouts with condition polling. Eliminates flaky tests caused by timing assumptions."
---

# Condition-Based Waiting

## Core Principle

**Wait for the actual condition you care about, not a guess about how long it takes.**

## Overview

Flaky tests often result from arbitrary timeouts (`sleep(1000)`, `setTimeout(500)`) that assume operations complete within fixed time windows. Condition-based waiting polls for the specific condition you need, making tests reliable regardless of system speed.

## When to Use This Skill

- Tests fail intermittently (pass locally, fail in CI)
- Tests use `sleep()`, `setTimeout()`, or arbitrary delays
- Tests check for events, state changes, or async operations
- Debugging reveals race conditions
- Test reliability < 100%

## The Problem with Timeouts

**Bad Pattern:**
```javascript
// ❌ Arbitrary timeout - brittle and slow
await click('#submit-button');
await sleep(2000); // Hope 2 seconds is enough
expect(successMessage).toBeVisible();
```

**Why it fails:**
- Too short: Test fails on slow systems
- Too long: Wastes time on fast systems
- No verification: Assumes operation completes
- Intermittent: Works 95% of time, fails randomly

## The Solution: Condition Polling

**Good Pattern:**
```javascript
// ✅ Wait for specific condition
await click('#submit-button');
await waitFor(() => successMessage.isVisible(), { timeout: 5000 });
expect(successMessage).toBeVisible();
```

**Why it works:**
- Fast systems: Completes immediately
- Slow systems: Waits as long as needed (up to timeout)
- Verification: Actually checks the condition
- Reliable: 100% pass rate

## Implementation Pattern

### Generic Polling Function

```typescript
async function waitForCondition(
  condition: () => boolean | Promise<boolean>,
  options: {
    timeout?: number;      // Maximum wait time (default: 5000ms)
    interval?: number;     // Check interval (default: 10ms)
    message?: string;      // Error message if timeout
  } = {}
): Promise<void> {
  const {
    timeout = 5000,
    interval = 10,
    message = 'Condition not met within timeout'
  } = options;

  const startTime = Date.now();

  while (true) {
    // Check condition
    if (await condition()) {
      return; // Success!
    }

    // Check timeout
    if (Date.now() - startTime > timeout) {
      throw new Error(`${message} (waited ${timeout}ms)`);
    }

    // Wait before next check
    await sleep(interval);
  }
}
```

### Helper Functions

```typescript
// Wait for element to exist
async function waitForElement(
  selector: string,
  options?: { timeout?: number }
): Promise<Element> {
  let element: Element | null = null;

  await waitForCondition(
    () => {
      element = document.querySelector(selector);
      return element !== null;
    },
    {
      ...options,
      message: `Element "${selector}" not found`
    }
  );

  return element!;
}

// Wait for event count
async function waitForEventCount(
  events: any[],
  expectedCount: number,
  options?: { timeout?: number }
): Promise<void> {
  await waitForCondition(
    () => events.length >= expectedCount,
    {
      ...options,
      message: `Expected ${expectedCount} events, got ${events.length}`
    }
  );
}

// Wait for event matching condition
async function waitForEventMatch(
  events: any[],
  predicate: (event: any) => boolean,
  options?: { timeout?: number }
): Promise<any> {
  let matchedEvent: any = null;

  await waitForCondition(
    () => {
      matchedEvent = events.find(predicate);
      return matchedEvent !== undefined;
    },
    {
      ...options,
      message: 'No event matched predicate'
    }
  );

  return matchedEvent;
}
```

## Usage Examples

### Example 1: Wait for Element

```javascript
// ❌ Bad: Arbitrary timeout
test('shows success message', async () => {
  await click('#submit');
  await sleep(1000);
  expect(getByText('Success!')).toBeVisible();
});

// ✅ Good: Wait for condition
test('shows success message', async () => {
  await click('#submit');
  await waitForElement('#success-message', { timeout: 5000 });
  expect(getByText('Success!')).toBeVisible();
});
```

### Example 2: Wait for API Response

```javascript
// ❌ Bad: Arbitrary timeout
test('loads user data', async () => {
  fetchUserData(userId);
  await sleep(2000);
  expect(userData).toBeDefined();
});

// ✅ Good: Wait for condition
test('loads user data', async () => {
  fetchUserData(userId);
  await waitForCondition(() => userData !== null, {
    timeout: 5000,
    message: 'User data not loaded'
  });
  expect(userData).toBeDefined();
});
```

### Example 3: Wait for State Change

```javascript
// ❌ Bad: Arbitrary timeout
test('completes upload', async () => {
  startUpload(file);
  await sleep(3000);
  expect(uploadStatus).toBe('complete');
});

// ✅ Good: Wait for condition
test('completes upload', async () => {
  startUpload(file);
  await waitForCondition(() => uploadStatus === 'complete', {
    timeout: 10000,
    message: 'Upload did not complete'
  });
  expect(uploadStatus).toBe('complete');
});
```

### Example 4: Wait for Event

```javascript
// ❌ Bad: Arbitrary timeout
test('emits analytics event', async () => {
  const events = [];
  analytics.on('event', e => events.push(e));

  await performAction();
  await sleep(500);

  expect(events).toHaveLength(1);
});

// ✅ Good: Wait for condition
test('emits analytics event', async () => {
  const events = [];
  analytics.on('event', e => events.push(e));

  await performAction();
  await waitForEventCount(events, 1, { timeout: 2000 });

  expect(events).toHaveLength(1);
});
```

### Example 5: Wait for Multiple Conditions

```javascript
// ❌ Bad: Multiple timeouts
test('completes multi-step process', async () => {
  startProcess();
  await sleep(1000); // Wait for step 1
  await sleep(1000); // Wait for step 2
  await sleep(1000); // Wait for step 3
  expect(status).toBe('complete');
});

// ✅ Good: Wait for each condition
test('completes multi-step process', async () => {
  startProcess();

  await waitForCondition(() => step1Complete, {
    message: 'Step 1 not complete'
  });

  await waitForCondition(() => step2Complete, {
    message: 'Step 2 not complete'
  });

  await waitForCondition(() => step3Complete, {
    message: 'Step 3 not complete'
  });

  expect(status).toBe('complete');
});
```

## Configuration Guidelines

### Timeout Values

```javascript
// Quick operations (DOM updates)
{ timeout: 1000 }  // 1 second

// Network requests
{ timeout: 5000 }  // 5 seconds

// Heavy operations (file uploads, processing)
{ timeout: 10000 } // 10 seconds

// Very slow operations
{ timeout: 30000 } // 30 seconds
```

### Interval Values

```javascript
// Default: Good for most cases
{ interval: 10 }   // 10ms - checks 100 times per second

// Fast polling: UI updates
{ interval: 1 }    // 1ms - checks 1000 times per second

// Slow polling: Network/disk operations
{ interval: 100 }  // 100ms - checks 10 times per second
```

## Framework-Specific Examples

### Jest / Testing Library

```javascript
import { waitFor } from '@testing-library/react';

test('example', async () => {
  render(<Component />);

  // Built-in waitFor
  await waitFor(() => expect(element).toBeVisible(), {
    timeout: 5000
  });
});
```

### Playwright

```javascript
test('example', async ({ page }) => {
  await page.click('#submit');

  // Built-in auto-waiting
  await page.waitForSelector('#success', { timeout: 5000 });

  // Or with custom condition
  await page.waitForFunction(() => window.status === 'ready');
});
```

### Cypress

```javascript
it('example', () => {
  cy.click('#submit');

  // Built-in retry assertions
  cy.get('#success', { timeout: 5000 }).should('be.visible');

  // Or custom condition
  cy.window().its('status').should('equal', 'ready');
});
```

### Laravel / PHP

```php
// Using Laravel's eventually() helper (Laravel 10+)
test('async operation completes', function () {
    $job = new ProcessJob();
    $job->dispatch();

    // Wait for condition
    expect(fn() => $job->isComplete())
        ->toBeTrue()
        ->eventually(timeout: 5);
});

// Manual implementation
function waitForCondition(callable $condition, int $timeoutMs = 5000): void
{
    $start = microtime(true) * 1000;

    while (true) {
        if ($condition()) {
            return;
        }

        if ((microtime(true) * 1000) - $start > $timeoutMs) {
            throw new Exception("Timeout after {$timeoutMs}ms");
        }

        usleep(10000); // 10ms
    }
}
```

## Real-World Impact

**Before condition-based waiting:**
- Test suite reliability: 60-80%
- Intermittent failures: 20-40%
- Average test time: Slower (excessive timeouts)
- Developer frustration: High
- CI reruns needed: Frequent

**After condition-based waiting:**
- Test suite reliability: 100%
- Intermittent failures: 0%
- Average test time: 40% faster (no excessive waits)
- Developer frustration: Low
- CI reruns needed: Rare

## Common Mistakes

### Mistake 1: Still using timeouts

```javascript
// ❌ Doesn't solve the problem
await waitForCondition(() => element.isVisible());
await sleep(500); // Why? You just waited for the condition!
```

### Mistake 2: Condition too broad

```javascript
// ❌ Too generic
await waitForCondition(() => elements.length > 0);

// ✅ Specific condition
await waitForCondition(() => elements.length === expectedCount);
```

### Mistake 3: Timeout too short

```javascript
// ❌ Too short for CI environments
await waitForCondition(condition, { timeout: 100 });

// ✅ Reasonable timeout
await waitForCondition(condition, { timeout: 5000 });
```

### Mistake 4: Checking too infrequently

```javascript
// ❌ Misses quick state changes
await waitForCondition(condition, { interval: 1000 });

// ✅ Frequent checks
await waitForCondition(condition, { interval: 10 });
```

## Integration with Other Skills

**Use with:**
- `test-driven-development` - Write reliable tests from the start
- `systematic-debugging` - Eliminate flaky test failures
- `testing-anti-patterns` - Avoid async testing mistakes

**When to apply:**
- Any test with timeouts or sleeps
- Tests that fail intermittently
- CI tests that pass locally but fail remotely
- Tests involving async operations

## Migration Strategy

### Step 1: Identify Flaky Tests

```bash
# Run tests multiple times
for i in {1..10}; do npm test; done

# Note which tests fail intermittently
```

### Step 2: Find Timeout Usage

```bash
# Search for sleep/timeout usage
grep -r "sleep(" tests/
grep -r "setTimeout" tests/
grep -r "delay(" tests/
```

### Step 3: Replace with Conditions

For each timeout, ask:
- What condition am I actually waiting for?
- How can I check that condition directly?
- What's a reasonable timeout?

### Step 4: Verify Improvement

```bash
# Run tests 100 times
for i in {1..100}; do npm test || break; done

# Should pass all 100 times
```

## Authority

**This skill is based on:**
- Test automation best practices
- Industry standard: All modern test frameworks support condition-based waiting
- Real-world evidence: Improves reliability from 60% to 100%
- Performance benefit: 40% faster test execution

**Social Proof:** Playwright, Cypress, Testing Library all use condition-based waiting as default.

## Your Commitment

When writing tests:
- [ ] I will NEVER use arbitrary timeouts
- [ ] I will ALWAYS wait for specific conditions
- [ ] I will use reasonable timeout values
- [ ] I will poll frequently (10ms default)
- [ ] I will make tests reliable, not just "usually work"

---

**Bottom Line**: Arbitrary timeouts are guesses. Condition-based waiting is verification. Wait for what you actually need, and tests become 100% reliable.
