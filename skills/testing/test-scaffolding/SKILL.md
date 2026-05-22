---
name: test-scaffolding
description: Automatically generate test scaffolding when user writes new code without tests or mentions needing tests. Supports unit, integration, e2e, and data tests for PHP and JavaScript. Invoke when user mentions "tests", "testing", "coverage", "write tests", or shows new untested code.
---

# Test Scaffolding Generator

Automatically generate test scaffolding for untested code.

## When to Use This Skill

Activate this skill when the user:
- Shows new code and says "I need tests for this"
- Asks "how do I test this?"
- Mentions "no tests yet" or "untested code"
- Says "I should write tests" or "need test coverage"
- Shows a class/function and asks about testing
- Mentions specific test types: "unit test", "integration test", "e2e test"

## Workflow

### 1. Analyze the Code to Test

**Identify**:
- Class name and namespace
- Methods to test (public methods)
- Dependencies (constructor parameters)
- Return types
- Drupal vs WordPress context

### 2. Determine Test Type

**Unit Tests** - For isolated logic:
- Services with minimal dependencies
- Utility functions
- Data transformation
- Business logic

**Integration Tests** - For component interaction:
- Controllers with database
- Form handlers
- API endpoints
- Complex workflows

**E2E Tests** - For user workflows:
- Login/authentication
- Multi-step forms
- Content creation
- Admin interfaces

### 3. Generate Appropriate Test Scaffold

## Test Templates

Complete test templates are available for reference:

- **[Unit Test Templates](templates/unit-tests.md)** - PHPUnit (Drupal/WordPress) & Jest
- **[Integration Test Templates](templates/integration-tests.md)** - Functional tests & API testing
- **[E2E Test Templates](templates/e2e-tests.md)** - Cypress & Playwright

Use these templates as starting points, adapting for the specific code being tested.

## Generation Strategy

### 1. Start Simple

Generate basic test structure first:
- Test class/describe block
- Setup/teardown methods
- One or two simple test cases

### 2. Identify Test Cases

For each public method:
- **Happy path** (valid input → expected output)
- **Error cases** (invalid input → exception)
- **Edge cases** (empty, null, boundary values)
- **State changes** (before/after verification)

### 3. Mock Dependencies

Identify what needs mocking:
- Database calls
- External APIs
- File system operations
- Time-dependent code

### 4. Add Assertions

Check:
- Return values
- State changes
- Side effects
- Error handling

## Quick Response Patterns

### For Simple Classes

When user shows a class with 2-3 methods:

1. Identify the test type (unit vs integration)
2. Generate test class with proper structure
3. Create tests for each public method:
   - Happy path test
   - Error case test
   - Edge case test (if applicable)
4. Include setup/teardown as needed
5. Add descriptive test names

**Example Response:**
```
"I'll generate PHPUnit tests for your UserManager class.

I see 3 public methods:
- getUser() - retrieves user data
- createUser() - creates new user
- deleteUser() - removes user

I'll create:
- Unit tests for getUser() (no database needed)
- Integration tests for createUser() and deleteUser() (require database)

[Generates test file with 6-8 test methods covering happy paths,
error cases, and edge cases]

This gives you ~80% coverage to start."
```

### For WordPress Functions

When user shows WordPress function using WP APIs:

1. Determine if unit or integration test
2. Use WP_UnitTestCase for integration
3. Use factories for test data
4. Include setup/teardown for cleanup

**Example Response:**
```
"For WordPress functions using WP_Query, you'll want an integration test.

I'll generate a WP_UnitTestCase test that:
1. Creates test posts using the factory
2. Calls your function
3. Verifies the query results
4. Cleans up automatically in tearDown()

[Generates test code]

The test uses wp_insert_post() to create test data."
```

### For Drupal Services

When user shows Drupal service with dependencies:

1. Identify service dependencies
2. Create mocks for dependencies in setUp()
3. Generate unit tests with dependency injection
4. Add @covers annotations

**Example Response:**
```
"I'll generate unit tests for your DataProcessor service.

I see it depends on:
- EntityTypeManagerInterface
- LoggerInterface

I'll:
1. Create mocks for these dependencies
2. Test each public method in isolation
3. Verify interactions with dependencies
4. Add @covers annotations for coverage tracking

[Generates test file with mocked dependencies]

This keeps tests fast by avoiding database calls."
```

### For JavaScript/React Components

When user shows JS function or React component:

1. Identify if pure function or component
2. Use Jest for unit tests
3. Use React Testing Library for components
4. Mock external dependencies

## Integration with CMS Cultivator

This skill complements the `/test-generate` slash command:

- **This Skill**: Automatically triggered during conversation
  - "I need tests for this class"
  - "How do I test this function?"
  - Quick single-class test generation

- **`/test-generate` Command**: Explicit batch generation
  - Generate tests for entire module
  - Comprehensive test suite creation
  - Project-wide test coverage

## Best Practices

1. **Test behavior, not implementation** - Test what code does, not how
2. **One assertion per test** - Keep tests focused
3. **Descriptive test names** - `testCreateUserWithValidData()` not `testCreateUser()`
4. **Arrange-Act-Assert** - Setup, execute, verify pattern
5. **Independent tests** - Tests shouldn't depend on each other
6. **Clean up** - Remove test data in tearDown()

## Example Interactions

**Example 1: Simple class**
```
User: "I wrote this UserManager class, need tests"
[Shows class with 3 methods]

Skill: "I'll generate PHPUnit tests for your UserManager class.
I see 3 public methods: createUser(), getUser(), deleteUser().
I'll create tests for the happy path and error cases for each.

[Generates test file]

This gives you 80% coverage to start. You may want to add edge case
tests for boundary conditions."
```

**Example 2: WordPress function**
```
User: "How do I test this WordPress function?"
[Shows custom function that uses WP_Query]

Skill: "For WordPress functions using WP_Query, you'll want an
integration test. I'll generate a WP_UnitTestCase test that:
1. Creates test posts using the factory
2. Calls your function
3. Verifies the query results

[Generates test code]

The test uses wp_insert_post() to create test data, then cleans up
automatically in tearDown()."
```

**Example 3: React component**
```
User: "Need tests for this React component"
[Shows UserProfile component]

Skill: "I'll create React Testing Library tests for your UserProfile component.

I see it:
- Displays user data from props
- Has edit button that calls onEdit callback
- Shows loading state

I'll generate tests for:
1. Rendering with user data
2. Clicking edit button
3. Loading state display

[Generates test file using React Testing Library]

These tests verify the component behavior from a user perspective."
```

## Common Patterns

### Testing Private Methods

Don't. Test public interface instead. If private method needs testing, consider extracting to separate class.

### Testing Static Methods

```php
// Avoid static methods when possible
// If you must, test directly
$result = MyClass::staticMethod($input);
$this->assertEquals($expected, $result);
```

### Testing Database Operations

```php
// Use transactions for rollback
protected function setUp(): void {
  parent::setUp();
  $this->database->beginTransaction();
}

protected function tearDown(): void {
  $this->database->rollbackTransaction();
  parent::tearDown();
}
```

### Testing Async JavaScript

```javascript
it('fetches user data', async () => {
  const user = await fetchUser(123);
  expect(user.name).toBe('John Doe');
});

// Or with promises
it('fetches user data', () => {
  return fetchUser(123).then(user => {
    expect(user.name).toBe('John Doe');
  });
});
```

## Platform-Specific Guidelines

### Drupal Testing

- Use proper namespace: `Drupal\Tests\mymodule\Unit`
- Add @group annotation
- Add @covers annotation for coverage
- Use UnitTestCase for unit tests
- Use KernelTestBase for database tests
- Use BrowserTestBase for functional tests

### WordPress Testing

- Extend WP_UnitTestCase
- Use factories for test data
- Follow WordPress naming: `test_method_name()`
- Use assertions: `$this->assertIsArray()`
- Clean up in tearDown()

### JavaScript Testing

- Use describe() for grouping
- Use test() or it() for individual tests
- Use beforeEach() for setup
- Mock external dependencies
- Test user interactions, not implementation

## Resources

- [PHPUnit Documentation](https://phpunit.de/)
- [Drupal Testing Guide](https://www.drupal.org/docs/testing)
- [WordPress PHPUnit](https://make.wordpress.org/core/handbook/testing/automated-testing/phpunit/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
