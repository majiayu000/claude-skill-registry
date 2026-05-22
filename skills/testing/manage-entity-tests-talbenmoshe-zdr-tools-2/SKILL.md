---
name: manage-entity-tests
description: Create or update test files for TypeScript classes that implement interfaces. Use when user asks to "create tests", "update tests", "generate test file", "fix tests", "test MyClass", or mentions needing tests for a class. Generates vitest test files with describe blocks, createClass helpers, and proper fake dependency injection.
---

# Manage Entity Tests Skill

This skill helps you create or update test files for classes that implement interfaces. Tests follow a specific pattern with vitest, fake builders for dependencies, and structured describe blocks.

## When to Use This Skill

Use this skill when you need to:
- **Create** a new test file for a class
- **Update** an existing test file when the class or interface changes
- **Generate** test coverage for interface methods

The skill will generate/update:
- A test file with vitest imports and describe blocks
- A `createMyClass` helper function for dependency injection
- Individual describe blocks for each interface method
- Test cases for different method behaviors and argument permutations

## Usage

Invoke this skill when the user asks to:
- "Create tests for [ClassName]"
- "Generate a test file for [ClassName]"
- "I need tests for [ClassName]"
- "Update tests for [ClassName]"
- "The [ClassName] changed, update its tests"
- "Fix the tests for [ClassName]"
- "Test [ClassName]"

## Core Principles

### Testing Philosophy
1. **Interface-Driven**: Only test methods defined in the class's interface, not implementation-specific private methods
2. **Dependency Injection**: Use a `createMyClass` helper to handle dependency creation and overrides
3. **Fake Builders**: Use Fake builders from dependencies, avoid `mockReturnValue` when possible
4. **Single Responsibility**: Each `it` block should test one specific scenario with ideally one assertion
5. **Avoid vi.mock**: Only use `vi.mock` for 3rd party dependencies, use Fakes for internal dependencies

## Class Types Supported

This skill supports testing two types of classes:

### Entity Classes
Entity classes that implement interfaces with event brokers (IEntity pattern):
- Have event broker properties (e.g., `name: IPropEventBroker<string>`)
- Follow the ZDR entities pattern
- Focus tests on event broker updates and entity state

### Service/Client Classes
Service or client classes that wrap dependencies (e.g., HTTP clients, APIs):
- Take dependencies through constructor injection
- Focus tests on method calls and return values
- Test data transformations (e.g., DTO conversions)
- Verify correct parameters are passed to dependencies

**Key Difference for Service/Client Classes:**
- Test that methods call dependencies with correct parameters
- Test return value transformations
- Test different response scenarios (success, error, empty data)
- Use backend DTOs in test data to verify transformations

## Prerequisites

Before creating/updating tests:
1. **Verify the class and interface exist** - The class you're testing must already be defined
2. **Check for existing test file** - Use Glob to search for existing `.spec.ts` file
3. **Identify the interface** - Determine which interface the class implements
4. **Locate dependencies** - Identify all dependencies and their available Fake builders

## Create vs Update Decision

**If test file exists:** Update mode
- Read the existing test file
- Read the class and interface definitions
- Compare and identify what's missing or outdated
- Update the test to match current implementation

**If test file does NOT exist:** Create mode
- Read the class and interface definitions
- Identify all dependencies
- Generate complete test file from scratch

## Test File Location

**CRITICAL**: Test files MUST be in the `__tests__` folder, which is a **SIBLING** of the `/src` folder, NOT inside it.

### Directory Structure
```
packages/
  my-package/
    src/
      MyClass.ts
      IMyClass.ts
    __tests__/              # Sibling to src/, NOT inside src/
      myClass.spec.ts       # camelCase filename
      otherClass.spec.ts
```

### Naming Convention
For a class named `MyClass`:
- Test file: `myClass.spec.ts` (camelCase, matches class name but lowercase first letter)
- Located in: `packages/my-package/__tests__/myClass.spec.ts`

## Test File Structure

### 1. Imports

```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest';
import type { IMyClass } from '../src/IMyClass';
import { MyClass } from '../src/MyClass';
import { FakeOtherClassBuilder } from '@someScope/some-library/fakes';
import type { IOtherClass } from '@someScope/some-library';
```

**Import Rules:**
- Import vitest utilities from `'vitest'`
- Import the interface using `type` import
- Import the class being tested
- Import Fake builders from dependency packages using `/fakes` subpath
- Import dependency interfaces when needed for typing

### 2. Main Describe Block

```typescript
describe('MyClass', () => {
  // Helper function
  function createMyClass(/* ... */): { /* ... */ } {
    // ...
  }

  // Method describe blocks
  describe('someMethod', () => {
    // Test cases
  });

  describe('anotherMethod', () => {
    // Test cases
  });
});
```

**Structure Rules:**
- Main describe uses the class name
- Contains one `createMyClass` helper function at the top
- One describe block per interface method
- No tests directly in main describe (only in method describes)

### 3. createMyClass Helper Function

**Purpose:** Factory function that creates an instance of the class with all its dependencies, allowing for easy overrides in tests.

**Standard Pattern:**
```typescript
function createMyClass(overrides?: {
  otherClass?: IOtherClass;
  anotherService?: IAnotherService;
}) {
  const otherClass = overrides?.otherClass ?? new FakeOtherClassBuilder().build();
  const anotherService = overrides?.anotherService ?? new FakeAnotherServiceBuilder().build();

  const myClass = new MyClass({
    otherClass,
    anotherService
  });

  return {
    otherClass,
    anotherService,
    myClass
  };
}
```

**Rules:**
- Accept an `overrides` parameter (optional object)
- One override parameter per dependency (typed with interface, not Fake)
- Use nullish coalescing (`??`) to provide default Fake instances
- Instantiate the class using all dependencies
- **Return an object** containing all dependencies AND the class instance
- Never instantiate the class directly in tests (always use this helper)

**Advanced Pattern (with primitive parameters):**
```typescript
function createMyClass(
  params?: {
    initialValue?: string;
    config?: { timeout: number };
  },
  overrides?: {
    otherClass?: IOtherClass;
  }
) {
  const otherClass = overrides?.otherClass ?? new FakeOtherClassBuilder().build();

  const myClass = new MyClass({
    initialValue: params?.initialValue ?? 'default',
    config: params?.config ?? { timeout: 1000 },
    otherClass
  });

  return {
    otherClass,
    myClass
  };
}
```

### 4. Method Describe Blocks

**One describe per interface method:**
```typescript
describe('login', () => {
  it('should return true when credentials are valid', () => {
    const { myClass, authService } = createMyClass({
      authService: new FakeAuthServiceBuilder()
        .withValidateReturnValue(Promise.resolve(true))
        .build()
    });

    const result = await myClass.login('user', 'pass');

    expect(result).toBe(true);
  });

  it('should return false when credentials are invalid', () => {
    const { myClass, authService } = createMyClass({
      authService: new FakeAuthServiceBuilder()
        .withValidateReturnValue(Promise.resolve(false))
        .build()
    });

    const result = await myClass.login('user', 'wrong');

    expect(result).toBe(false);
  });

  it('should call authService.validate with correct parameters', () => {
    const { myClass, authService } = createMyClass();

    await myClass.login('testuser', 'testpass');

    expect(authService.validate).toHaveBeenCalledWith('testuser', 'testpass');
  });
});
```

**Rules for Test Cases:**
- Create one `it` block per test scenario
- Test different argument permutations
- Test different branches based on dependency behavior
- Test edge cases (null, undefined, empty strings, etc.)
- Use descriptive test names that explain the expected behavior
- Prefer single assertion per test when possible

### 5. Mocking Dependencies

**Preferred Method (Fake Builders):**
```typescript
it('should handle success case', () => {
  const { myClass } = createMyClass({
    otherService: new FakeOtherServiceBuilder()
      .withProcessReturnValue(Promise.resolve({ success: true }))
      .withIsActiveValue(true)
      .build()
  });

  // Test using the configured fake
});
```

**Avoid (mockReturnValue) unless absolutely necessary:**
```typescript
// DON'T DO THIS unless impossible to avoid
it('should handle changing return values', () => {
  const { myClass, otherService } = createMyClass();

  // ONLY use this as a LAST RESORT
  otherService.process.mockReturnValue(Promise.resolve({ success: false }));

  // Test...
});
```

**When mockReturnValue is Acceptable:**
- Testing a sequence of calls with different return values
- Dynamic behavior that can't be pre-configured
- Testing error recovery where you need to simulate failures mid-test

### 6. Testing Method Calls

**Good Pattern:**
```typescript
it('should call dependency method with correct arguments', () => {
  const { myClass, otherService } = createMyClass();

  myClass.processData({ id: '123', name: 'test' });

  expect(otherService.process).toHaveBeenCalledWith({ id: '123', name: 'test' });
  expect(otherService.process).toHaveBeenCalledTimes(1);
});
```

**Testing with Multiple Calls:**
```typescript
it('should call dependency multiple times', () => {
  const { myClass, otherService } = createMyClass();

  myClass.processBatch([item1, item2, item3]);

  expect(otherService.process).toHaveBeenCalledTimes(3);
  expect(otherService.process).toHaveBeenNthCalledWith(1, item1);
  expect(otherService.process).toHaveBeenNthCalledWith(2, item2);
  expect(otherService.process).toHaveBeenNthCalledWith(3, item3);
});
```

### 7. Using vi.mock (Only for 3rd Party)

**When to use:**
- Mocking external libraries (axios, fs, etc.)
- Mocking Node.js built-in modules
- Mocking modules that don't have Fake implementations

**Example:**
```typescript
import { vi, describe, it, expect } from 'vitest';
import axios from 'axios';

vi.mock('axios');

describe('ApiClient', () => {
  it('should fetch data from API', async () => {
    vi.mocked(axios.get).mockResolvedValue({ data: { id: 1 } });

    const client = new ApiClient();
    const result = await client.fetchUser(1);

    expect(result).toEqual({ id: 1 });
    expect(axios.get).toHaveBeenCalledWith('/users/1');
  });
});
```

## Workflow

### Create Workflow (No existing test)

1. **Identify the class and interface** - Ask user which class to test if not clear
2. **Locate the class file** - Use Glob to find the class definition
3. **Read the interface** - Get all methods that need testing (ONLY interface methods)
4. **Identify dependencies** - Look at class constructor to find all dependencies
5. **Locate Fake builders** - For each dependency, find its Fake builder (usually in the same package under `/fakes`)
6. **Ensure `__tests__` folder exists** - Check if `__tests__/` directory exists at package root (sibling to `/src`), create if needed
7. **Create the test file** in `__tests__/myClass.spec.ts` with:
   - Vitest imports
   - Interface and class imports
   - Fake builder imports for dependencies
   - Main describe block with class name
   - `createMyClass` helper function
   - One describe block per interface method
   - Multiple `it` blocks per method covering different scenarios

### Update Workflow (Test exists)

1. **Identify the class and test** - Determine which class/test to update
2. **Read all relevant files**:
   - Read the existing test file
   - Read the current class definition
   - Read the current interface definition
3. **Compare and identify changes**:
   - **New methods in interface** - Add new describe blocks with test cases
   - **Removed methods** - Remove corresponding describe blocks
   - **Changed method signatures** - Update test cases to match new signatures
   - **New dependencies** - Add to `createMyClass` function and imports
   - **Removed dependencies** - Remove from `createMyClass` and imports
4. **Apply updates using Edit tool**:
   - Add/remove imports as needed
   - Update `createMyClass` function
   - Add/remove/modify describe blocks
   - Ensure coverage for all interface methods
5. **Verify completeness** - Ensure all interface methods have test coverage

### Update Guidelines

When updating an existing test:
- **Preserve existing structure** - Don't rewrite the entire file, use Edit tool for targeted changes
- **Maintain consistency** - Follow the same patterns used in the existing test
- **Keep test names descriptive** - Use clear, behavior-focused test names
- **Don't delete passing tests** - Only update tests that are failing or testing removed functionality
- **Add missing coverage** - If new methods were added, create new describe blocks

## Common Test Scenarios

### Scenario 1: Testing Async Methods

```typescript
describe('fetchData', () => {
  it('should return data when fetch succeeds', async () => {
    const expectedData = { id: 1, name: 'Test' };
    const { myClass } = createMyClass({
      apiClient: new FakeApiClientBuilder()
        .withGetReturnValue(Promise.resolve(expectedData))
        .build()
    });

    const result = await myClass.fetchData('123');

    expect(result).toEqual(expectedData);
  });

  it('should throw error when fetch fails', async () => {
    const { myClass } = createMyClass({
      apiClient: new FakeApiClientBuilder()
        .withGetReturnValue(Promise.reject(new Error('Network error')))
        .build()
    });

    await expect(myClass.fetchData('123')).rejects.toThrow('Network error');
  });
});
```

### Scenario 2: Testing Methods with Multiple Arguments

```typescript
describe('updateUser', () => {
  it('should call repository with user ID and updates', async () => {
    const { myClass, userRepository } = createMyClass();

    await myClass.updateUser('user-123', { name: 'New Name', email: 'new@email.com' });

    expect(userRepository.update).toHaveBeenCalledWith('user-123', {
      name: 'New Name',
      email: 'new@email.com'
    });
  });

  it('should handle empty updates object', async () => {
    const { myClass, userRepository } = createMyClass();

    await myClass.updateUser('user-123', {});

    expect(userRepository.update).toHaveBeenCalledWith('user-123', {});
  });

  it('should handle undefined user ID', async () => {
    const { myClass } = createMyClass();

    await expect(myClass.updateUser(undefined, { name: 'Test' }))
      .rejects.toThrow('User ID is required');
  });
});
```

### Scenario 3: Testing Methods with Conditional Logic

```typescript
describe('processOrder', () => {
  it('should use express shipping when order is marked as urgent', async () => {
    const { myClass, shippingService } = createMyClass();

    await myClass.processOrder({ id: '123', urgent: true });

    expect(shippingService.ship).toHaveBeenCalledWith(
      expect.objectContaining({ shippingMethod: 'express' })
    );
  });

  it('should use standard shipping when order is not urgent', async () => {
    const { myClass, shippingService } = createMyClass();

    await myClass.processOrder({ id: '123', urgent: false });

    expect(shippingService.ship).toHaveBeenCalledWith(
      expect.objectContaining({ shippingMethod: 'standard' })
    );
  });

  it('should apply discount when customer is premium', async () => {
    const { myClass } = createMyClass({
      customerService: new FakeCustomerServiceBuilder()
        .withIsPremiumReturnValue(true)
        .build()
    });

    const result = await myClass.processOrder({ id: '123', total: 100 });

    expect(result.total).toBe(90); // 10% discount
  });

  it('should not apply discount for regular customers', async () => {
    const { myClass } = createMyClass({
      customerService: new FakeCustomerServiceBuilder()
        .withIsPremiumReturnValue(false)
        .build()
    });

    const result = await myClass.processOrder({ id: '123', total: 100 });

    expect(result.total).toBe(100);
  });
});
```

### Scenario 4: Testing with beforeEach

```typescript
describe('UserManager', () => {
  function createUserManager(/* ... */) {
    // ...
  }

  describe('addUser', () => {
    let userManager: IUserManager;
    let userRepository: IUserRepository;

    beforeEach(() => {
      const created = createUserManager();
      userManager = created.userManager;
      userRepository = created.userRepository;
    });

    it('should add user to repository', () => {
      userManager.addUser({ id: '1', name: 'John' });

      expect(userRepository.save).toHaveBeenCalledWith({ id: '1', name: 'John' });
    });

    it('should validate user before adding', () => {
      userManager.addUser({ id: '1', name: 'John' });

      expect(userRepository.validate).toHaveBeenCalled();
    });
  });
});
```

**Note:** Use `beforeEach` sparingly. It's useful when many tests need the same setup, but can make tests harder to understand. Prefer explicit setup in each test when possible.

### Scenario 5: Testing Event Brokers

```typescript
describe('updateName', () => {
  it('should update the name event broker', () => {
    const { myClass } = createMyClass();

    myClass.updateName('New Name');

    expect(myClass.name.get()).toBe('New Name');
  });

  it('should notify listeners when name changes', () => {
    const { myClass } = createMyClass();
    const listener = vi.fn();
    myClass.name.subscribe(listener);

    myClass.updateName('New Name');

    expect(listener).toHaveBeenCalledWith('New Name');
  });
});
```

### Scenario 6: Testing Service/Client Classes with HTTP Calls

For service/client classes that wrap HTTP clients or APIs:

```typescript
describe('ReportsClient', () => {
  function createReportsClient(overrides?: {
    httpClient?: IHttpClient;
  }) {
    const httpClient = overrides?.httpClient ?? new FakeHttpClientBuilder()
      .withGetCallback(() => Promise.resolve({ data: [], status: 200, headers: {} }))
      .build();

    const reportsClient = new ReportsClient(httpClient);

    return {
      httpClient,
      reportsClient
    };
  }

  describe('listReportTemplates', () => {
    it('should call httpClient.get with correct endpoint', async () => {
      const { reportsClient, httpClient } = createReportsClient();

      await reportsClient.listReportTemplates();

      expect(httpClient.get).toHaveBeenCalledWith('/velocity/reports');
    });

    it('should transform backend DTOs to frontend DTOs', async () => {
      /* eslint-disable camelcase */
      const backendDTO: ReportBackendDTO = {
        id: 'report-1',
        name: 'Test ReportTemplate',
        report_type: 'analytics',
        description: 'Test Description',
        notebook_path: '/path/to/notebook',
        parameters: { key: 'value' },
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z'
      };
      /* eslint-enable camelcase */

      const { reportsClient } = createReportsClient({
        httpClient: new FakeHttpClientBuilder()
          .withGetCallback(() => Promise.resolve({ data: [backendDTO], status: 200, headers: {} }))
          .build()
      });

      const result = await reportsClient.listReportTemplates();

      expect(result.reports).toHaveLength(1);
      expect(result.reports[0]).toEqual({
        id: 'report-1',
        name: 'Test ReportTemplate',
        reportType: 'analytics',
        description: 'Test Description',
        notebookPath: '/path/to/notebook',
        parameters: { key: 'value' },
        createdAt: '2024-01-01T00:00:00Z',
        updatedAt: '2024-01-02T00:00:00Z'
      });
    });

    it('should return empty array when no reports are available', async () => {
      const { reportsClient } = createReportsClient({
        httpClient: new FakeHttpClientBuilder()
          .withGetCallback(() => Promise.resolve({ data: [], status: 200, headers: {} }))
          .build()
      });

      const result = await reportsClient.listReportTemplates();

      expect(result.reports).toEqual([]);
    });
  });

  describe('createReportTemplate', () => {
    it('should call httpClient.post with transformed data', async () => {
      /* eslint-disable camelcase */
      const backendDTO: ReportBackendDTO = {
        id: 'report-1',
        name: 'New ReportTemplate',
        report_type: 'test-type',
        description: 'Test Description',
        notebook_path: '/notebook',
        parameters: { param: 'value' },
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };
      /* eslint-enable camelcase */

      const { reportsClient, httpClient } = createReportsClient({
        httpClient: new FakeHttpClientBuilder()
          .withPostCallback(() => Promise.resolve({ data: backendDTO, status: 201, headers: {} }))
          .build()
      });

      await reportsClient.createReportTemplate({
        name: 'New ReportTemplate',
        reportType: 'test-type',
        description: 'Test Description',
        notebookPath: '/notebook',
        parameters: { param: 'value' }
      });

      expect(httpClient.post).toHaveBeenCalledWith('/velocity/reports', {
        name: 'New ReportTemplate',
        report_type: 'test-type',
        description: 'Test Description',
        notebook_path: '/notebook',
        parameters: { param: 'value' }
      });
    });

    it('should return created report in response object', async () => {
      /* eslint-disable camelcase */
      const backendDTO: ReportBackendDTO = {
        id: 'report-1',
        name: 'New ReportTemplate',
        report_type: 'test-type',
        description: null,
        notebook_path: null,
        parameters: null,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      };
      /* eslint-enable camelcase */

      const { reportsClient } = createReportsClient({
        httpClient: new FakeHttpClientBuilder()
          .withPostCallback(() => Promise.resolve({ data: backendDTO, status: 201, headers: {} }))
          .build()
      });

      const result = await reportsClient.createReportTemplate({
        name: 'New ReportTemplate',
        reportType: 'test-type'
      });

      expect(result.report.id).toBe('report-1');
      expect(result.report.name).toBe('New ReportTemplate');
      expect(result.report.reportType).toBe('test-type');
    });
  });
});
```

**Key Points for Service/Client Tests:**
- Use backend DTOs (snake_case) in test data to verify transformation
- Test that correct HTTP methods and endpoints are called
- Test that request data is properly transformed (camelCase → snake_case)
- Test that response data is properly transformed (snake_case → camelCase)
- Test different response scenarios (empty, single item, multiple items)
- Verify the structure of returned Response objects

## Best Practices

### 1. Test Behavior, Not Implementation
- Focus on what the method does (outputs, side effects)
- Don't test internal implementation details
- Test the public interface only

### 2. Descriptive Test Names
```typescript
// Good
it('should return null when user is not found', () => { /* ... */ });
it('should throw error when email is invalid', () => { /* ... */ });

// Bad
it('should work', () => { /* ... */ });
it('test login', () => { /* ... */ });
```

### 3. Arrange-Act-Assert Pattern
```typescript
it('should calculate total with tax', () => {
  // Arrange
  const { calculator } = createCalculator();

  // Act
  const result = calculator.calculateTotal(100, 0.1);

  // Assert
  expect(result).toBe(110);
});
```

### 4. One Assertion Per Test (When Possible)
```typescript
// Preferred
it('should return user ID', () => {
  const { service } = createService();
  const result = service.getUser();
  expect(result.id).toBe('123');
});

it('should return user name', () => {
  const { service } = createService();
  const result = service.getUser();
  expect(result.name).toBe('John');
});

// Acceptable when testing object shape
it('should return complete user object', () => {
  const { service } = createService();
  const result = service.getUser();
  expect(result).toEqual({
    id: '123',
    name: 'John',
    email: 'john@example.com'
  });
});
```

### 5. Avoid Test Interdependence
- Each test should be independent
- Tests should pass in any order
- Use `createMyClass` in each test, not shared instances

### 6. Test Edge Cases
- Null/undefined inputs
- Empty strings/arrays
- Boundary values
- Error conditions

### 7. Use Appropriate Matchers
```typescript
// Equality
expect(value).toBe(5);           // Primitive values
expect(obj).toEqual({ id: 1 });  // Objects/arrays

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Numbers
expect(value).toBeGreaterThan(5);
expect(value).toBeLessThanOrEqual(10);

// Strings
expect(str).toContain('substring');
expect(str).toMatch(/regex/);

// Arrays
expect(arr).toContain(item);
expect(arr).toHaveLength(3);

// Exceptions
expect(() => fn()).toThrow('error message');
await expect(asyncFn()).rejects.toThrow();

// Function calls
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledWith(arg1, arg2);
expect(fn).toHaveBeenCalledTimes(2);
```

## Common Pitfalls to Avoid

### 1. ❌ Don't Instantiate Class Directly
```typescript
// BAD
it('should work', () => {
  const myClass = new MyClass({ dep: new FakeDepBuilder().build() });
  // ...
});

// GOOD
it('should work', () => {
  const { myClass } = createMyClass();
  // ...
});
```

### 2. ❌ Don't Overuse mockReturnValue
```typescript
// BAD (if avoidable)
it('should handle success', () => {
  const { myClass, service } = createMyClass();
  service.fetch.mockReturnValue(Promise.resolve(data));
  // ...
});

// GOOD
it('should handle success', () => {
  const { myClass } = createMyClass({
    service: new FakeServiceBuilder()
      .withFetchReturnValue(Promise.resolve(data))
      .build()
  });
  // ...
});
```

### 3. ❌ Don't Test Private Methods
```typescript
// BAD - testing private implementation
it('should call private helper', () => {
  const { myClass } = createMyClass();
  // @ts-ignore
  const result = myClass.privateHelper();
  expect(result).toBe(something);
});

// GOOD - test public interface only
it('should process data correctly', () => {
  const { myClass } = createMyClass();
  const result = myClass.publicMethod();
  expect(result).toBe(expectedOutput);
});
```

### 4. ❌ Don't Use vi.mock for Internal Dependencies
```typescript
// BAD
vi.mock('../src/MyService');

describe('MyClass', () => {
  // ...
});

// GOOD
import { FakeMyServiceBuilder } from '../fakes';

describe('MyClass', () => {
  function createMyClass(overrides?: { myService?: IMyService }) {
    const myService = overrides?.myService ?? new FakeMyServiceBuilder().build();
    // ...
  }
});
```

### 5. ❌ Don't Forget Async/Await
```typescript
// BAD
it('should fetch data', () => {
  const { myClass } = createMyClass();
  const result = myClass.fetchData(); // Returns Promise!
  expect(result).toEqual(data); // This will fail!
});

// GOOD
it('should fetch data', async () => {
  const { myClass } = createMyClass();
  const result = await myClass.fetchData();
  expect(result).toEqual(data);
});
```

## Example Reference

See `examples.md` in the same directory as this skill for complete working examples.

## Important Notes

### File Organization (CRITICAL)
- **All tests MUST be in `__tests__/` directory at package root** (sibling to `/src`, NOT inside `/src`)
- Test files use camelCase naming: `myClass.spec.ts`
- Import paths from tests to src use relative paths: `'../src/MyClass'`

### Interface-Driven Testing
- **ONLY test methods defined in the interface** the class implements
- Do not test private methods or implementation details
- If a method is not in the interface, it should not have tests (unless it's a public utility method also in the interface)

### Dependency Management
- Use Fake builders from `/fakes` subpath exports
- Import Fakes from the same package where the real class is defined
- If a Fake doesn't exist, you may need to create it first (use manage-fake skill)
- For 3rd party libraries without Fakes, use vi.mock sparingly

### When Updating
- Always use the Edit tool for updates, not Write (which overwrites the entire file)
- Update the `createMyClass` function when dependencies change
- Add new describe blocks for new methods
- Remove describe blocks for removed methods
- Update test cases when method signatures change
- Verify all interface methods have corresponding describe blocks

### Test Quality
- Prefer many small tests over few large tests
- Test happy path and error cases
- Test edge cases and boundary conditions
- Use descriptive test names that explain the behavior being tested
- Keep tests simple and focused
- Avoid complex logic in tests themselves
