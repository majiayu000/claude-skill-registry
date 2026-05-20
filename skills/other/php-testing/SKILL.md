---
name: php-testing
description: Write PHP tests with PHPUnit — unit tests, mocking, data providers, test doubles, assertions, and TDD practices. Use when writing tests for PHP code, whether in Magento or standalone PHP applications.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# PHP Testing with PHPUnit

## Before writing code

**Fetch live docs**: Web-search `site:docs.phpunit.de phpunit 10` (or current version) for the latest PHPUnit documentation. Check `https://phpunit.de/` for current version.

## PHPUnit Fundamentals

### Test Class Structure

- Test classes extend `PHPUnit\Framework\TestCase`
- Test methods prefixed with `test` or annotated `#[Test]`
- `setUp()` — runs before each test
- `tearDown()` — runs after each test
- `setUpBeforeClass()` / `tearDownAfterClass()` — per-class lifecycle

### Assertions

Common assertions:
- `assertEquals($expected, $actual)` — loose comparison
- `assertSame($expected, $actual)` — strict comparison (type + value)
- `assertTrue($value)` / `assertFalse($value)`
- `assertNull($value)` / `assertNotNull($value)`
- `assertInstanceOf($class, $object)`
- `assertCount($count, $array)`
- `assertArrayHasKey($key, $array)`
- `assertStringContainsString($needle, $haystack)`
- `expectException($class)` — exception testing

### Data Providers

Supply multiple test cases to a single test method:
- `#[DataProvider('providerName')]` attribute (PHPUnit 10+)
- Provider method returns array of arrays (each inner array = one test case)
- Reduces test duplication for parameterized testing

## Test Doubles

### Mocks

Verify behavior — assert that methods were called with expected arguments:
- `$this->createMock(SomeClass::class)`
- `$mock->expects($this->once())->method('save')->with($entity)`
- `$mock->expects($this->never())->method('delete')`

### Stubs

Provide canned responses — no behavior verification:
- `$stub->method('getById')->willReturn($entity)`
- `$stub->method('getList')->willReturn($searchResults)`

### Method Return Behaviors

- `willReturn($value)` — always returns this value
- `willReturnMap($map)` — returns based on argument mapping
- `willReturnCallback($callable)` — dynamic return
- `willThrowException($exception)` — throws on call
- `willReturnSelf()` — returns the mock (for fluent APIs)

### Consecutive Calls

`willReturnOnConsecutiveCalls($val1, $val2, $val3)` — different return per call.

> **Note:** `willReturnOnConsecutiveCalls()` is deprecated in PHPUnit 10.3+. Use `willReturn()` with `$this->onConsecutiveCalls()` or `willReturnCallback()` with a counter instead.

## Testing Patterns

### Arrange-Act-Assert (AAA)

1. **Arrange** — set up test data, mocks, dependencies
2. **Act** — call the method under test
3. **Assert** — verify the result

### Testing Exceptions

```php
$this->expectException(NoSuchEntityException::class);
$this->expectExceptionMessage('Entity not found');
$repository->getById(999);
```

### Testing Private/Protected Methods

Don't test private methods directly — test through public methods. If a private method is complex enough to test independently, it should probably be extracted to its own class.

### Testing with Dependency Injection

Create the class under test with mocked dependencies:
1. Create mocks for all constructor parameters
2. Instantiate the class with mocks
3. Configure mock behavior per test
4. Call the method and assert

## Code Coverage

- `--coverage-html <dir>` — generate HTML coverage report
- `--coverage-text` — terminal output
- Focus on meaningful coverage — high-value business logic
- Don't chase 100% — getters/setters and framework glue don't need coverage

## PHPUnit Configuration

`phpunit.xml` or `phpunit.xml.dist`:
- Test suite directories
- Bootstrap file
- Coverage filters
- Environment variables
- Extensions

## Best Practices

- One assertion per test (or one logical assertion group)
- Name tests descriptively: `testGetByIdThrowsWhenNotFound()`
- Use data providers for parameterized tests
- Mock external dependencies, not the class under test
- Keep tests fast — no I/O, no database, no network in unit tests
- Use `setUp()` for common test setup
- Test edge cases: null, empty, boundary values
- Write the test first (TDD) when practical
- Run tests before committing

Fetch PHPUnit docs for exact assertion methods, mock API, and configuration options for your PHPUnit version before writing tests.
