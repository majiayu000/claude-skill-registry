---
name: magento-testing
description: Write tests for Magento 2 — PHPUnit unit tests, integration tests, MFTF functional tests, and API tests. Use when implementing test coverage for modules, debugging, or setting up CI/CD test pipelines.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Testing

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce testing` for testing overview
2. Fetch `https://developer.adobe.com/commerce/testing/functional-testing-framework/` for MFTF guide
3. Web-search `site:developer.adobe.com commerce php development test` for unit/integration test patterns

## Testing Layers

### Unit Tests

**Purpose**: Test individual classes in isolation.

- Location: `Test/Unit/` within the module
- Config: `dev/tests/unit/phpunit.xml.dist`
- Run: `vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist app/code/VendorName/ModuleName/Test/Unit/`
- Mock all dependencies with PHPUnit mocks or `createMock()`
- No Magento bootstrap — pure PHP unit testing
- Fast execution, no database or filesystem dependencies

### Integration Tests

**Purpose**: Test module interactions with the Magento framework.

- Location: `Test/Integration/` or `dev/tests/integration/`
- Config: `dev/tests/integration/phpunit.xml.dist`
- Run: `vendor/bin/phpunit -c dev/tests/integration/phpunit.xml.dist`
- Uses Magento application bootstrap — real DI, real database
- `@magentoDbIsolation enabled` — rolls back DB changes after each test
- `@magentoAppArea` — sets the application area (frontend, adminhtml)
- `@magentoConfigFixture` — sets config values for the test
- `@magentoDataFixture` — loads test data
- Slower but tests real interactions

### MFTF (Magento Functional Testing Framework)

**Purpose**: End-to-end browser tests.

- XML-based test definitions (not PHP)
- Converts to Codeception PHP tests
- Uses Selenium WebDriver for browser automation
- Allure reporting for results
- Location: `Test/Mftf/Test/`, `Test/Mftf/ActionGroup/`, `Test/Mftf/Page/`, `Test/Mftf/Section/`
- Run: `vendor/bin/mftf run:test <TestName>`
- Tests complete user workflows (add to cart, checkout, admin operations)

### API Functional Tests

**Purpose**: Test REST and SOAP API endpoints.

- Location: `dev/tests/api-functional/`
- Config: `dev/tests/api-functional/phpunit_rest.xml.dist`
- Tests API request/response contracts
- Verifies authentication, authorization, and data integrity

### Static Tests

**Purpose**: Code quality and standards.

- Location: `dev/tests/static/`
- Checks: coding standards (PHP_CodeSniffer + Magento standard), dependency validation, copyright headers
- Run: `vendor/bin/phpunit -c dev/tests/static/phpunit.xml.dist`

## Key Testing Patterns

### Mocking in Magento

- Use `$this->createMock(ClassName::class)` for dependencies
- `$mock->expects($this->once())->method('getById')->willReturn($entity)`
- For ObjectManager-dependent classes: use `ObjectManagerHelper` from test framework

### Test Data Fixtures

Integration tests use fixtures to set up test state:
- `@magentoDataFixture` annotation points to a fixture file
- Fixture files create entities (products, customers, orders)
- `@magentoDbIsolation` rolls back after test

### Testing Plugins

Unit test plugin classes independently — call the plugin method with a mock subject and verify behavior.

### Testing Observers

Unit test observer's `execute()` method with a mocked Observer/Event object.

## Best Practices

- Write unit tests for all business logic classes
- Use integration tests for DI wiring and database interaction verification
- Use MFTF for critical user journeys (checkout, customer registration)
- Run static tests in CI/CD to enforce coding standards
- Use `@magentoDbIsolation` to prevent test pollution
- Keep unit tests fast — mock all external dependencies
- Name test methods descriptively: `testSaveThrowsExceptionWhenNameIsEmpty()`

Fetch the testing documentation for exact annotations, fixture patterns, and MFTF XML schema before writing tests.
