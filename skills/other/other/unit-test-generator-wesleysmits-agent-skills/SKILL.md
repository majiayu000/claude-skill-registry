---
name: generating-unit-tests
description: Generates unit tests for changed files and identifies coverage gaps. Use when the user asks to write tests, generate test suites, check coverage, or mentions Jest, Vitest, Playwright, or Mocha.
---

# Unit Test Generator & Validator

## When to use this skill

- User asks to generate tests for a file or function
- User wants to improve test coverage
- User mentions Jest, Vitest, Playwright, or Mocha
- User asks for edge case suggestions
- User wants to validate existing tests

## Workflow

- [ ] Identify changed or target files
- [ ] Detect test framework in project
- [ ] Analyze code to understand testable units
- [ ] Generate test file with appropriate structure
- [ ] Include edge cases and error scenarios
- [ ] Run tests to validate
- [ ] Check coverage if configured

## Instructions

### Step 1: Identify Target Files

For changed files:

```bash
git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(js|jsx|ts|tsx|vue)$' | grep -v '\.test\.|\.spec\.'
```

For specific file, derive test path:

- `src/utils/format.ts` → `src/utils/format.test.ts` or `__tests__/utils/format.test.ts`

### Step 2: Detect Test Framework

| Framework  | Config Files                               | Test Pattern         |
| ---------- | ------------------------------------------ | -------------------- |
| Jest       | `jest.config.*`, `package.json` (jest key) | `*.test.{js,ts,tsx}` |
| Vitest     | `vitest.config.*`, `vite.config.*`         | `*.test.{js,ts,tsx}` |
| Playwright | `playwright.config.*`                      | `*.spec.{js,ts}`     |
| Mocha      | `.mocharc.*`, `package.json` (mocha key)   | `*.test.{js,ts}`     |

Check installed framework:

```bash
npm ls jest vitest @playwright/test mocha 2>/dev/null
```

### Step 3: Analyze Source Code

Extract testable units:

- Exported functions and their signatures
- Class methods and their visibility
- React/Vue component props and behavior
- API handlers and their responses
- Pure functions vs side-effect functions

Identify inputs and outputs:

- Parameter types and valid ranges
- Return types and possible values
- Thrown errors and conditions
- External dependencies to mock

### Step 4: Generate Test Structure

**Jest/Vitest template:**

```typescript
import { describe, it, expect, vi } from "vitest"; // or from '@jest/globals'
import { functionName } from "../path/to/module";

describe("functionName", () => {
  it("should handle normal input", () => {
    expect(functionName(validInput)).toBe(expectedOutput);
  });

  it("should handle edge case", () => {
    expect(functionName(edgeInput)).toBe(edgeOutput);
  });

  it("should throw on invalid input", () => {
    expect(() => functionName(invalidInput)).toThrow(ExpectedError);
  });
});
```

**React component template:**

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Component } from '../Component';

describe('Component', () => {
  it('renders with default props', () => {
    render(<Component />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const onAction = vi.fn();
    render(<Component onAction={onAction} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalledOnce();
  });
});
```

**Playwright E2E template:**

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature", () => {
  test("should complete user flow", async ({ page }) => {
    await page.goto("/path");
    await page.click('button[data-testid="action"]');
    await expect(page.locator(".result")).toBeVisible();
  });
});
```

### Step 5: Include Edge Cases

Always generate tests for:

- **Boundary values**: 0, -1, empty string, empty array, max values
- **Null/undefined handling**: missing optional params
- **Type coercion**: string numbers, boolean strings
- **Async behavior**: resolved, rejected, timeout
- **Error paths**: invalid input, network failures, permission denied

### Step 6: Run and Validate

Execute tests:

```bash
# Jest
npx jest --testPathPattern="<test-file>" --coverage

# Vitest
npx vitest run <test-file> --coverage

# Playwright
npx playwright test <test-file>

# Mocha
npx mocha <test-file>
```

### Step 7: Check Coverage

View coverage report:

```bash
# Jest/Vitest generate coverage in ./coverage/
open coverage/lcov-report/index.html
```

Coverage targets:

- Statements: 80%+
- Branches: 75%+
- Functions: 80%+
- Lines: 80%+

## Mocking Patterns

**Mock external modules:**

```typescript
vi.mock("../api", () => ({
  fetchData: vi.fn().mockResolvedValue({ data: "mocked" }),
}));
```

**Mock timers:**

```typescript
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

**Mock environment:**

```typescript
const originalEnv = process.env;
beforeEach(() => {
  process.env = { ...originalEnv, API_KEY: "test-key" };
});
afterEach(() => {
  process.env = originalEnv;
});
```

## Validation

Before completing:

- [ ] Tests pass without modification to source
- [ ] Edge cases covered
- [ ] Mocks properly reset between tests
- [ ] No flaky async behavior
- [ ] Coverage improved or maintained

## Error Handling

- **Framework not installed**: Run `npm install --save-dev <framework>`.
- **Tests fail immediately**: Check import paths and module resolution.
- **Mock not working**: Ensure mock is defined before import in Jest, or use `vi.mock` hoisting in Vitest.
- **Coverage not generating**: Add `--coverage` flag and check config for coverage settings.
- **Unsure about command**: Run `npx <framework> --help`.

## Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Vitest Documentation](https://vitest.dev/guide/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Testing Library](https://testing-library.com/docs/)
