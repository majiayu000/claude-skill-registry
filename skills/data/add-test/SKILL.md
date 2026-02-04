---
skill: add-test
description: Add unit tests for component or function: $ARGUMENTS
location: project
---

# Add Unit Tests: $ARGUMENTS

I'll create comprehensive unit tests for **$ARGUMENTS** following the project's testing patterns.

This will include:
1. Identifying the source file (component or utility function)
2. Creating a matching test file with proper naming convention
3. Generating test cases with Jest and Testing Library
4. Running tests to verify they pass
5. Reporting results

Let's begin!

---

## Process Steps

### 1. Identify the Source File

First, I'll locate the file to test.

**For React components:**
```bash
# Check components directory
if [ -f "expense-tracker-ai/components/$ARGUMENTS.tsx" ]; then
  SOURCE_FILE="expense-tracker-ai/components/$ARGUMENTS.tsx"
  TEST_FILE="expense-tracker-ai/components/$ARGUMENTS.test.tsx"
  FILE_TYPE="component"
  echo "✅ Found component: $SOURCE_FILE"
elif [ -f "expense-tracker-ai/components/$ARGUMENTS.ts" ]; then
  SOURCE_FILE="expense-tracker-ai/components/$ARGUMENTS.ts"
  TEST_FILE="expense-tracker-ai/components/$ARGUMENTS.test.ts"
  FILE_TYPE="component"
  echo "✅ Found component: $SOURCE_FILE"
fi
```

**For utility functions:**
```bash
# Check lib directory
if [ -f "expense-tracker-ai/lib/$ARGUMENTS.ts" ]; then
  SOURCE_FILE="expense-tracker-ai/lib/$ARGUMENTS.ts"
  TEST_FILE="expense-tracker-ai/lib/$ARGUMENTS.test.ts"
  FILE_TYPE="utility"
  echo "✅ Found utility: $SOURCE_FILE"
fi
```

**For app pages:**
```bash
# Check app directory
if [ -f "expense-tracker-ai/app/$ARGUMENTS.tsx" ]; then
  SOURCE_FILE="expense-tracker-ai/app/$ARGUMENTS.tsx"
  TEST_FILE="expense-tracker-ai/app/$ARGUMENTS.test.tsx"
  FILE_TYPE="page"
  echo "✅ Found page: $SOURCE_FILE"
fi
```

**If file not found:**
```bash
if [ -z "$SOURCE_FILE" ]; then
  echo "❌ Error: Could not find $ARGUMENTS"
  echo ""
  echo "Available components:"
  ls -1 expense-tracker-ai/components/*.tsx 2>/dev/null | sed 's/.*\///' | sed 's/\.tsx$//'
  echo ""
  echo "Available utilities:"
  ls -1 expense-tracker-ai/lib/*.ts 2>/dev/null | sed 's/.*\///' | sed 's/\.ts$//'
  exit 1
fi
```

### 2. Check for Existing Tests

Before creating a new test file, check if one already exists:

```bash
if [ -f "$TEST_FILE" ]; then
  echo "⚠️  Test file already exists: $TEST_FILE"
  echo ""
  echo "Options:"
  echo "1. Update existing tests (add new test cases)"
  echo "2. Replace existing tests (overwrite file)"
  echo "3. Cancel (leave existing tests unchanged)"
  echo ""
  echo "What would you like to do?"
  # Wait for user decision
else
  echo "✅ No existing test file - will create new one"
fi
```

### 3. Read and Analyze Source File

Read the source file to understand what needs testing:

```bash
# Read the source file to understand its structure
echo "Analyzing $SOURCE_FILE..."

# Look for key patterns:
# - Export statements (what's being exported)
# - Function definitions (what functions exist)
# - Props interfaces (what props are expected)
# - State hooks (what state is managed)
```

Use the Read tool to examine the source file and identify:
- Exported components/functions
- Props interfaces
- State management
- Event handlers
- Key functionality to test

### 4. Generate Test Template

Create a test file based on the file type:

**For React Components:**

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // Setup and teardown
  beforeEach(() => {
    // Clear any mocks or state before each test
  });

  afterEach(() => {
    // Cleanup after each test
  });

  // Happy path tests
  test('should render correctly', () => {
    render(<ComponentName />);
    expect(screen.getByTestId('component-name')).toBeInTheDocument();
  });

  test('should display expected content', () => {
    render(<ComponentName />);
    // Add specific content checks based on component
  });

  // Interaction tests
  test('should handle user interaction', () => {
    render(<ComponentName />);
    const button = screen.getByRole('button', { name: /button text/i });
    fireEvent.click(button);
    // Assert expected behavior after interaction
  });

  // Props tests
  test('should render with custom props', () => {
    const mockProps = {
      // Define test props
    };
    render(<ComponentName {...mockProps} />);
    // Assert component renders correctly with props
  });

  // Edge cases
  test('should handle empty state', () => {
    render(<ComponentName />);
    // Assert behavior with no data
  });

  test('should handle error state', () => {
    // Test error scenarios
  });

  // Accessibility tests
  test('should be accessible', () => {
    const { container } = render(<ComponentName />);
    // Basic accessibility checks
    // Consider using @axe-core/react for comprehensive checks
  });
});
```

**For Utility Functions:**

```typescript
import { functionName } from './fileName';

describe('functionName', () => {
  // Happy path tests
  test('should return expected output for valid input', () => {
    const result = functionName(validInput);
    expect(result).toBe(expectedOutput);
  });

  // Edge cases
  test('should handle edge case: empty input', () => {
    const result = functionName('');
    expect(result).toBe(expectedEmptyOutput);
  });

  test('should handle edge case: null input', () => {
    const result = functionName(null);
    expect(result).toBe(expectedNullOutput);
  });

  test('should handle edge case: undefined input', () => {
    const result = functionName(undefined);
    expect(result).toBe(expectedUndefinedOutput);
  });

  // Boundary conditions
  test('should handle minimum value', () => {
    const result = functionName(minValue);
    expect(result).toBe(expectedMinOutput);
  });

  test('should handle maximum value', () => {
    const result = functionName(maxValue);
    expect(result).toBe(expectedMaxOutput);
  });

  // Error handling
  test('should throw error for invalid input', () => {
    expect(() => functionName(invalidInput)).toThrow();
  });
});
```

### 5. Customize Tests Based on Source Analysis

Based on the source file analysis, customize the test template:

**For components with props:**
- Add tests for each prop variation
- Test required vs optional props
- Test prop validation

**For components with state:**
- Test initial state
- Test state changes
- Test state-dependent rendering

**For components with events:**
- Test each event handler
- Test event handler with different inputs
- Test event handler error cases

**For utility functions:**
- Test return values for various inputs
- Test edge cases (empty, null, undefined)
- Test boundary conditions (min, max)
- Test error handling

### 6. Create the Test File

Write the customized test template to the test file using the Write tool.

**Important conventions:**
- Use `data-testid` attributes for stable selectors
- Follow existing test patterns from the project
- Include descriptive test names
- Group related tests with `describe` blocks
- Cover happy path, edge cases, and error states

### 7. Run the Tests

Execute the test suite to verify the tests work:

```bash
cd expense-tracker-ai

# Run just the new test file
npm test -- $ARGUMENTS.test

# If tests fail, run in watch mode for debugging
npm run test:watch -- $ARGUMENTS.test
```

### 8. Handle Test Failures

If tests fail, categorize and address the issues:

**Type 1: Test Implementation Issues**
- Incorrect selectors → Update test selectors
- Wrong assertions → Fix test expectations
- Missing mocks → Add required mocks

```bash
# Debug in watch mode
npm run test:watch -- $ARGUMENTS.test

# Run with verbose output
npm test -- --verbose $ARGUMENTS.test
```

**Type 2: Missing Test Infrastructure**
- Missing `data-testid` in component → Add to source file
- Missing test setup → Update jest.setup.js
- Missing mocks → Create mock files

**Type 3: Source Code Issues**
- Bugs revealed by tests → Fix source code
- Type errors → Fix TypeScript issues

**Resolution approach:**
1. Read error messages carefully
2. Identify the root cause (test vs source)
3. Fix the appropriate file
4. Re-run tests
5. Iterate until all tests pass

### 9. Validate Test Quality

Ensure tests meet quality standards:

**Coverage checklist:**
- ✅ Happy path scenarios tested
- ✅ Edge cases covered (empty, null, boundary conditions)
- ✅ Error states tested
- ✅ User interactions tested (for components)
- ✅ Props variations tested (for components)
- ✅ Return values tested (for functions)

**Quality checklist:**
- ✅ Tests are independent (can run in any order)
- ✅ Tests are deterministic (same result every time)
- ✅ Tests use stable selectors (`data-testid`, not CSS classes)
- ✅ Tests have descriptive names
- ✅ Tests follow project conventions
- ✅ No console errors or warnings

### 10. Report Results

Generate a summary of what was created:

```
✅ Unit Tests Created Successfully

📊 Summary:
- Source file: $SOURCE_FILE
- Test file: $TEST_FILE
- File type: $FILE_TYPE
- Test cases: [count]
- All tests passing: ✓

📝 Test Coverage:
- Happy path scenarios ([count] tests)
- Edge cases ([count] tests)
- Error handling ([count] tests)
- User interactions ([count] tests - for components)
- Props variations ([count] tests - for components)

✅ Test Quality:
- Independent tests: ✓
- Stable selectors: ✓
- Descriptive names: ✓
- Project conventions: ✓

💡 Next Steps:
- Run full test suite: npm test
- Check coverage: npm test -- --coverage
- Run in watch mode: npm run test:watch
```

---

## Example Usage

### Testing a Component

```bash
# Add tests for ExpenseForm component
add-test ExpenseForm
```

**Expected output:**
```
✅ Found component: expense-tracker-ai/components/ExpenseForm.tsx
✅ No existing test file - will create new one
Analyzing expense-tracker-ai/components/ExpenseForm.tsx...

Creating test file with coverage for:
- Form rendering
- Input validation
- Form submission
- Error states
- Props handling

✅ Unit Tests Created Successfully

📊 Summary:
- Source file: expense-tracker-ai/components/ExpenseForm.tsx
- Test file: expense-tracker-ai/components/ExpenseForm.test.tsx
- File type: component
- Test cases: 12
- All tests passing: ✓
```

### Testing a Utility Function

```bash
# Add tests for getCategoryColor utility
add-test getCategoryColor
```

**Expected output:**
```
✅ Found utility: expense-tracker-ai/lib/utils.ts
Analyzing getCategoryColor function...

Creating test file with coverage for:
- Valid category names
- Hash consistency
- Edge cases (empty, null)
- Return value format

✅ Unit Tests Created Successfully

📊 Summary:
- Source file: expense-tracker-ai/lib/utils.ts
- Test file: expense-tracker-ai/lib/utils.test.ts
- File type: utility
- Test cases: 8
- All tests passing: ✓
```

---

## Project-Specific Patterns

This skill follows the expense tracker app's testing conventions:

### Test Setup Patterns

From `jest.setup.js`:
```javascript
// ResizeObserver mock for Recharts components
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};
```

### Common Test Patterns

**localStorage mocking:**
```typescript
beforeEach(() => {
  const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    clear: jest.fn(),
  };
  global.localStorage = localStorageMock as any;
});
```

**Testing Library selectors:**
```typescript
// Prefer data-testid
screen.getByTestId('submit-button')

// Use semantic queries
screen.getByRole('button', { name: /submit/i })

// Avoid brittle selectors
// ❌ screen.getByClassName('btn-primary')
// ❌ container.querySelector('.form button:nth-child(2)')
```

**Async testing:**
```typescript
test('should load data asynchronously', async () => {
  render(<Component />);

  // Wait for element to appear
  const element = await screen.findByTestId('loaded-data');
  expect(element).toBeInTheDocument();
});
```

---

## Troubleshooting

### Tests Fail: Module Not Found

**Error:** `Cannot find module '@testing-library/react'`

**Solution:**
```bash
cd expense-tracker-ai
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

### Tests Fail: ResizeObserver Not Defined

**Error:** `ReferenceError: ResizeObserver is not defined`

**Solution:** Already handled in `jest.setup.js`. If error persists:
```bash
# Verify jest.setup.js is configured in jest.config.js
cat jest.config.js | grep setupFilesAfterEnv
```

### Tests Fail: Type Errors

**Error:** `Type error: Cannot find name 'describe'`

**Solution:**
```bash
# Install Jest types
npm install --save-dev @types/jest

# Verify tsconfig.json includes jest types
cat tsconfig.json | grep jest
```

### Tests Pass But Don't Actually Test Anything

**Symptom:** Tests pass but don't catch obvious bugs

**Solution:** Review assertions:
```typescript
// ❌ Weak test (always passes)
test('should work', () => {
  const result = someFunction();
  expect(result).toBeDefined();
});

// ✅ Strong test (validates actual behavior)
test('should return correct calculation', () => {
  const result = calculateTotal([10, 20, 30]);
  expect(result).toBe(60);
});
```

---

## Related Documentation

- **Testing Guide:** [expense-tracker-ai/docs/dev/testing-guide.md](expense-tracker-ai/docs/dev/testing-guide.md)
- **Jest Configuration:** [expense-tracker-ai/jest.config.js](expense-tracker-ai/jest.config.js)
- **Example Tests:** [expense-tracker-ai/components/MonthlyInsights.test.tsx](expense-tracker-ai/components/MonthlyInsights.test.tsx)
- **Testing Library Docs:** https://testing-library.com/docs/react-testing-library/intro/
