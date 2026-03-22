---
name: woo-testing
description: Test WooCommerce extensions — PHPUnit unit/integration tests, WP test suite, WooCommerce test helpers, E2E with Playwright, and WP-CLI test scaffolding. Use when writing tests for WooCommerce plugins or setting up a test environment.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Testing

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com testing` for WooCommerce testing guide
2. Web-search `site:developer.wordpress.org plugins testing` for WordPress Plugin testing handbook
3. Web-search `woocommerce e2e testing playwright` for E2E patterns

## Test Types

### Unit Tests

Isolated class/function testing:
- No WordPress/WooCommerce bootstrap
- Mock all dependencies
- Fast execution
- Test pure business logic

### Integration Tests

Tests with WordPress + WooCommerce loaded:
- Extend `WC_Unit_Test_Case` (which extends `WP_UnitTestCase`)
- Full WordPress database (using transactions for rollback)
- Access to all WooCommerce APIs and hooks
- Test plugin integration with WooCommerce

### E2E (End-to-End) Tests

Browser-based tests with Playwright:
- Test complete user flows (add to cart, checkout, payment)
- WooCommerce provides Playwright utilities
- Run against a real WordPress + WooCommerce instance

## Setting Up PHPUnit Tests

### Scaffold with WP-CLI

`wp scaffold plugin-tests my-plugin` creates:
- `tests/bootstrap.php` — test bootstrap
- `tests/test-sample.php` — sample test
- `phpunit.xml.dist` — PHPUnit configuration
- `bin/install-wp-tests.sh` — install WordPress test suite

### WooCommerce Test Bootstrap

After WordPress test bootstrap, load WooCommerce and your plugin:
```php
// In tests/bootstrap.php
require_once dirname( __DIR__ ) . '/vendor/woocommerce/woocommerce/tests/legacy/bootstrap.php';
// Or manually: activate WooCommerce, then your plugin
```

### WC_Unit_Test_Case

Base class providing:
- Transaction-based test isolation (each test rolled back)
- WooCommerce helper methods
- Proper environment setup/teardown

## Test Helpers

### WC_Helper_Product

Factory for creating test products:
- `WC_Helper_Product::create_simple_product()` — simple product with defaults
- `WC_Helper_Product::create_variation_product()` — variable + variations
- `WC_Helper_Product::create_grouped_product()` — grouped product
- `WC_Helper_Product::create_external_product()` — external/affiliate

### WC_Helper_Order

Factory for creating test orders:
- `WC_Helper_Order::create_order( $customer_id )` — order with line items
- Configurable status, products, addresses

### WC_Helper_Customer

- `WC_Helper_Customer::create_customer()` — customer with address
- `WC_Helper_Customer::create_mock_customer()` — mock customer object

### WC_Helper_Shipping

- `WC_Helper_Shipping::create_simple_flat_rate()` — flat rate shipping zone
- Set up shipping zones and methods for checkout tests

### WC_Helper_Coupon

- `WC_Helper_Coupon::create_coupon()` — discount coupon with configurable type/amount

## Testing Patterns

### Testing Hooks

Verify your hooks fire correctly:
- Check that a callback is registered: `has_action( 'hook_name', [ $instance, 'method' ] )`
- Test the callback's effect by triggering the hook
- Use `did_action( 'hook_name' )` to verify an action fired

### Testing CRUD Operations

1. Create an object (product, order, etc.)
2. Perform operations (update, delete, query)
3. Assert expected state
4. Cleanup happens automatically via transaction rollback

### Testing REST API Endpoints

Use `WP_REST_Server` to dispatch requests:
- `$request = new WP_REST_Request( 'GET', '/wc/v3/products' )`
- `$response = rest_get_server()->dispatch( $request )`
- Assert status code, response data, headers

### Testing Payment Gateways

- Create order, set payment method
- Call `process_payment()` with test credentials
- Assert order status changes
- Test refund flow

### Mocking

- Use PHPUnit mocks: `$this->createMock( ClassName::class )`
- Mock HTTP requests: `add_filter( 'pre_http_request', $mock_response )`
- WooCommerce provides `WC_Mock_Payment_Gateway` and similar mocks

## E2E Testing with Playwright

### Setup

WooCommerce uses `@woocommerce/e2e-utils` and Playwright:
- Configure in `playwright.config.js`
- Tests in `tests/e2e/specs/`
- Page objects for common pages (shop, cart, checkout, my-account)

### Common E2E Flows

- Add product to cart → verify cart → proceed to checkout → complete order
- Customer registration and login
- Admin: create product, manage orders, configure settings
- Payment gateway integration testing

## Best Practices

- Use `WC_Unit_Test_Case` for integration tests
- Use WooCommerce helper classes (`WC_Helper_Product`, etc.) for test fixtures
- Test with HPOS enabled and disabled
- Test with both classic and block checkout
- Mock external API calls (payment processors, shipping carriers)
- Use `@group` annotations for test organization
- Clean up created data (helpers handle this via transaction rollback)
- Run tests in CI with WordPress test suite

Fetch the WooCommerce testing documentation and WordPress testing handbook for exact helper methods, bootstrap setup, and E2E configuration before implementing.
