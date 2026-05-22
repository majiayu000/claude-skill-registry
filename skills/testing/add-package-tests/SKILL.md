---
name: add-package-tests
description: Add unit tests to a Datagrok package
argument-hint: "[package-path]"
---

# Add Package Tests

Add unit tests to a Datagrok package using the platform's custom test framework.

## Usage

```
/add-package-tests [package-path]
```

## Instructions

When this skill is invoked, help the user set up and write tests for a Datagrok package.

### Step 1: Set up test infrastructure

For a new package with tests:

```bash
grok create <package-name> --test
```

For an existing package:

```bash
cd <package-name>
grok add tests
npm install
```

### Step 2: Create test files

Create a `src/tests/` directory. Each file covers one test category.

```ts
import {category, expect, test} from '@datagrok-libraries/utils/src/test';


category('MyCategory', () => {
  test('should do something', async () => {
    expect(actualValue, expectedValue);
  });

  test('should handle edge case', async () => {
    // Test logic
    expect(result, true);
  });
});
```

Key test framework functions:
- `category(name, fn)` - groups related tests
- `test(name, fn, options?)` - defines a single test case
- `expect(actual, expected)` - assertion that checks equality

### Step 3: Register tests in package-test.ts

Import all test files in `src/package-test.ts`:

```ts
import './tests/my-category-tests';
import './tests/another-category-tests';
```

### Step 4: Skip failing tests

Use the `skipReason` parameter to temporarily skip a test (always provide a reason such as a Jira ticket):

```ts
test('flaky test', async () => {
  expect(1, 11);
}, {skipReason: 'GROK-99999'});
```

### Step 5: Add inline function tests

For simple functions, add test cases directly in the function annotation using the `test` parameter:

```ts
//name: square
//input: int x
//output: int y
//test: square(1) == 1
//test: square(2) == 4
//test: square(3) == 9
export function square(x: number): number {
  return x ** 2;
}
```

Supported parameter types for `//test:` annotations: `int`, `double`, `bool`, `string`, `datetime`, `map`. Types like `dataframe`, `column_list`, `column`, `file`, `blob` require an additional helper function call.

### Step 6: Run tests

```bash
# Local testing with datagrok-tools
grok test

# Against a specific server
grok test --host dev

# With visible browser
grok test --gui

# Specific category or test
grok test --category "MyCategory"
grok test --test "should do something"
```

Tests can also be run from the Datagrok console or Test Manager in the platform UI.

### Key points

- Import `category`, `test`, `expect` from `@datagrok-libraries/utils/src/test`
- Always register test files in `src/package-test.ts`
- Use `skipReason` with a Jira key (e.g., `GROK-12345`) when skipping tests
- The `//test:` annotation on functions is for simple input/output validation
- For real examples, see the Chem package: `public/packages/Chem/`

## Behavior

1. Check if the package already has test infrastructure (`src/package-test.ts`, `src/tests/`)
2. If not, set up test support using `grok add tests`
3. Create test files with `category` and `test` blocks for the functionality the user wants to test
4. Register the test files in `src/package-test.ts`
5. Show the user how to run the tests
