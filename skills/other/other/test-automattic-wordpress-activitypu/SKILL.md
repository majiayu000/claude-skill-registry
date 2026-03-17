---
name: test
description: Testing patterns for PHPUnit and Playwright E2E tests. Use when writing tests, debugging test failures, setting up test coverage, or implementing test patterns for ActivityPub features.
---

# ActivityPub Testing

This skill provides guidance on writing and running tests for the WordPress ActivityPub plugin.

## Quick Reference

For complete testing commands and environment setup, see [Testing Reference](../../../tests/README.md).

### Key Commands
- **PHP:** `npm run env-test`
- **E2E:** `npm run test:e2e`
- **JavaScript:** `npm run test:unit`

## PHPUnit Testing

### Test Structure

```php
<?php
namespace Activitypub\Tests;

use WP_UnitTestCase;

class Test_Feature extends WP_UnitTestCase {
    public function set_up(): void {
        parent::set_up();
        // Setup
    }

    public function tear_down(): void {
        // Cleanup
        parent::tear_down();
    }

    public function test_functionality() {
        // Test implementation
    }
}
```

### Common Test Patterns

For transformer and handler testing patterns, see [Testing Reference - Writing Effective Tests](../../../tests/README.md#writing-effective-tests).

For mocking HTTP requests and other utilities, see [Testing Reference - Test Utilities](../../../tests/README.md#test-utilities).

### Test Groups

Use `@group` annotations:
```php
/**
 * @group activitypub
 * @group federation
 */
public function test_federation_feature() {
    // Test code
}
```

## E2E Testing with Playwright

### Basic E2E Test

```javascript
const { test, expect } = require('@playwright/test');

test('ActivityPub settings page loads', async ({ page }) => {
    await page.goto('/wp-admin/options-general.php?page=activitypub');
    await expect(page.locator('h1')).toContainText('ActivityPub');
});
```

### Testing Federation

```javascript
test('WebFinger discovery works', async ({ page }) => {
    const response = await page.request.get('/.well-known/webfinger', {
        params: {
            resource: 'acct:admin@localhost:8888'
        }
    });

    expect(response.ok()).toBeTruthy();
    const json = await response.json();
    expect(json.subject).toBe('acct:admin@localhost:8888');
});
```

## Test Data Factories

For creating test data (users, posts, comments), see [Testing Reference - Test Utilities](../../../tests/README.md#test-utilities).

## Coverage Reports

See [Testing Reference](../../../tests/README.md) for detailed coverage generation instructions.

## Debugging Tests

### Debug Output

```php
// In tests
var_dump( $data );
error_log( print_r( $result, true ) );

// Run with verbose
npm run env-test -- --verbose --debug
```

### Isolating Tests

```bash
# Run single test method
npm run env-test -- --filter=test_specific_method

# Stop on first failure
npm run env-test -- --stop-on-failure
```