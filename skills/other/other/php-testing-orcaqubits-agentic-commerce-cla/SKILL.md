---
name: php-testing
description: Write PHP tests with PHPUnit — unit tests, mocking, data providers, assertions, test doubles, and TDD workflow. Use when writing tests for WooCommerce extensions or PHP projects.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# PHP Testing with PHPUnit

## Before writing code

**Fetch live docs**: Web-search `site:phpunit.de documentation` for the latest PHPUnit documentation. Check `https://phpunit.de/` for current version and features.

## PHPUnit Fundamentals

### Test Class Structure

- Extend `PHPUnit\Framework\TestCase` (or `WC_Unit_Test_Case` for WooCommerce)
- Test methods prefixed with `test` or annotated with `#[Test]`
- `setUp()` — runs before each test
- `tearDown()` — runs after each test
- `setUpBeforeClass()` / `tearDownAfterClass()` — run once per class

### Assertions

Core assertions:
- `assertEquals( $expected, $actual )` — loose equality
- `assertSame( $expected, $actual )` — strict identity
- `assertTrue( $condition )` / `assertFalse( $condition )`
- `assertNull( $value )` / `assertNotNull( $value )`
- `assertCount( $expected, $array )`
- `assertContains( $needle, $haystack )`
- `assertInstanceOf( $class, $object )`
- `assertArrayHasKey( $key, $array )`
- `assertStringContainsString( $needle, $haystack )`

### Exception Testing

- `$this->expectException( InvalidArgumentException::class )`
- `$this->expectExceptionMessage( 'Expected message' )`
- `$this->expectExceptionCode( 404 )`

## Test Doubles

### Mocks

Create mock objects to verify interactions:
```php
$mock = $this->createMock( PaymentProcessor::class );
$mock->expects( $this->once() )
     ->method( 'charge' )
     ->with( $this->equalTo( 29.99 ) )
     ->willReturn( true );
```

### Stubs

Return predetermined values without verifying calls:
```php
$stub = $this->createStub( PriceCalculator::class );
$stub->method( 'calculate' )->willReturn( 29.99 );
```

### Expectation Methods

- `$this->once()` — called exactly once
- `$this->exactly( $n )` — called exactly n times
- `$this->never()` — not called
- `$this->atLeastOnce()` — called one or more times
- `$this->any()` — any number of calls

### willReturn Variants

- `willReturn( $value )` — return fixed value
- `willReturnMap( $map )` — return based on arguments
- `willReturnCallback( $callable )` — custom logic
- `willThrowException( $exception )` — throw on call

## Data Providers

### What They Do

Supply multiple test cases to a single test method:

```php
public static function priceProvider(): array {
    return [
        'regular price' => [ 29.99, 29.99, '' ],
        'sale price'    => [ 29.99, 19.99, '19.99' ],
        'zero price'    => [ 0.00, 0.00, '' ],
    ];
}

#[DataProvider('priceProvider')]
public function test_get_display_price( float $regular, float $expected, string $sale ): void {
    // test with each data set
}
```

### Best Practices for Providers

- Name data sets descriptively (keyed array)
- Keep providers as static methods
- Return arrays of arrays (each inner array = one test case)
- Use `#[DataProvider('methodName')]` attribute

## WordPress/WooCommerce Testing Specifics

### WP_UnitTestCase

- Provides WordPress-loaded environment
- Each test wrapped in a database transaction (auto-rollback)
- Factory methods: `$this->factory->post`, `$this->factory->user`
- `go_to( $url )` — simulate page load
- `set_current_screen( 'edit-post' )` — simulate admin screen

### Mocking WordPress Functions

Use `WP_Mock` or `Brain\Monkey` libraries:
- Mock `add_action`, `add_filter`, `do_action`, `apply_filters`
- Mock `wp_remote_get`, `get_option`, etc.
- Useful for isolated unit tests without WordPress bootstrap

### Mocking HTTP Requests

Filter `pre_http_request` to intercept `wp_remote_get()` / `wp_remote_post()`:
```php
add_filter( 'pre_http_request', function( $preempt, $args, $url ) {
    return [ 'response' => [ 'code' => 200 ], 'body' => '{"status":"ok"}' ];
}, 10, 3 );
```

## Test Organization

### Directory Structure

```
tests/
├── bootstrap.php           # Test bootstrap
├── Unit/                   # Pure unit tests (no WP)
│   └── PriceCalculatorTest.php
├── Integration/            # Tests with WP/WC loaded
│   ├── ProductTest.php
│   └── OrderTest.php
└── E2E/                    # Playwright end-to-end
    └── specs/
```

### phpunit.xml.dist Configuration

- Define test suites: `unit`, `integration`
- Set bootstrap file
- Configure coverage report output
- Set environment variables

## TDD Workflow

1. **Red** — write a failing test that describes the desired behavior
2. **Green** — write the minimum code to make the test pass
3. **Refactor** — clean up code while keeping tests green
4. Repeat

## Best Practices

- One assertion per test (when practical)
- Name tests descriptively: `test_process_payment_returns_success_for_valid_card`
- Use data providers for parameterized tests
- Mock external dependencies (APIs, databases, file system)
- Test edge cases: null values, empty strings, boundary values, invalid input
- Keep unit tests fast — no network, no filesystem, no database
- Use integration tests for WordPress/WooCommerce interaction testing
- Run tests in CI on every push

Fetch the PHPUnit documentation for exact assertion signatures, mock API, and configuration options before implementing.
