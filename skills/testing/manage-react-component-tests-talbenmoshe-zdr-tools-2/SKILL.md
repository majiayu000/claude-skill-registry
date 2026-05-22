---
name: manage-react-component-tests
description: Create or update test files for React components. Use when user asks to "create component tests", "test MyComponent", "generate tests for component", "update component tests", or mentions needing tests for a React component. Generates vitest test files with render, mocked sub-components, and proper test structure focusing on logic and prop validation.
---

# Manage React Component Tests Skill

This skill helps you create or update test files for React components. Tests follow a specific pattern with vitest, `render` from React Testing Library, and mocked sub-components to test logic and prop passing in isolation.

## When to Use This Skill

Use this skill when you need to:
- **Create** a new test file for a React component
- **Update** an existing test file when the component changes
- **Generate** test coverage for component logic and prop validation

The skill will generate/update:
- A test file with vitest and React Testing Library imports
- Mocked versions of all imported sub-components
- A `renderMyComponent` helper function using `render`
- Individual test cases for different component behaviors and prop permutations

## Usage

Invoke this skill when the user asks to:
- "Create tests for [MyComponent]"
- "Generate a test file for [MyComponent]"
- "I need tests for [MyComponent]"
- "Update tests for [MyComponent]"
- "The [MyComponent] changed, update its tests"
- "Test [MyComponent]"

## Core Principles

### Testing Philosophy
1. **Logic-Focused**: Test component logic, not UI appearance
2. **Prop Validation**: Verify sub-components receive correct props
3. **Isolation**: Mock all sub-components to test the component in isolation
4. **Callback Testing**: Simulate callbacks to test handlers
5. **Unit Testing**: Each component has its own tests; dependencies should have separate tests

## Prerequisites

Before creating/updating component tests:
1. **Verify the component exists** - The component you're testing must already be defined
2. **Check for existing test file** - Use Glob to search for existing `.spec.tsx` file
3. **Identify sub-components** - Determine what components are imported and rendered
4. **Verify @testing-library/react** - Ensure it's installed (for `render`)

## Create vs Update Decision

**If test file exists:** Update mode
- Read the existing test file
- Read the component definition
- Compare and identify what's missing or outdated
- Update the test to match current implementation

**If test file does NOT exist:** Create mode
- Read the component definition
- Identify all sub-components to mock
- Generate complete test file from scratch

## Test File Location

**CRITICAL**: Test files MUST be in the `__tests__` folder, which is a **SIBLING** of the `/src` folder, NOT inside it.

### Directory Structure
```
packages/
  my-package/
    src/
      components/
        MyComponent.tsx
    __tests__/              # Sibling to src/, NOT inside src/
      MyComponent.spec.tsx  # .tsx extension for React components
```

### Naming Convention
For a component named `MyComponent`:
- Test file: `MyComponent.spec.tsx` (matches component name exactly, with `.tsx` extension)
- Located in: `packages/my-package/__tests__/MyComponent.spec.tsx`

## Test File Structure

### 1. Imports

**Import Rules:**
- Import React (required for this project's JSX transform)
- Import vitest utilities from `'vitest'`
- Import `render` and `screen` from `'@testing-library/react'`
- Import the component being tested
- DO NOT import sub-components (they will be mocked)

**Example:**
```typescript
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MyComponent } from '../src/components/MyComponent';
```

### 2. Mocking Sub-Components

**All imported sub-components must be mocked** to test the component in isolation.

**Pattern:**
```typescript
// Mock all sub-component modules
vi.mock('../src/components/SubComponentA', () => ({
  SubComponentA: vi.fn(() => <div data-testid="mock-sub-component-a">SubComponentA</div>)
}));

vi.mock('../src/components/SubComponentB', () => ({
  SubComponentB: vi.fn(() => <div data-testid="mock-sub-component-b">SubComponentB</div>)
}));
```

**Rules:**
- Place mocks at the top of the file, after imports
- Use `vi.fn()` to create a mock function that returns a simple `<div>`
- Add `data-testid` for easy querying in tests
- Mock EVERY component imported by the component under test

### 3. Main Describe Block

```typescript
describe('MyComponent', () => {
  // Helper function
  function renderMyComponent(props?: Partial<MyComponentProps>) {
    // ...
  }

  // Reset mocks before each test
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Test cases
  it('should render sub-components with correct props', () => {
    // Test...
  });
});
```

**Structure Rules:**
- Main describe uses the component name
- Contains one `renderMyComponent` helper function at the top
- Includes `beforeEach` to clear mocks
- All test cases use the `renderMyComponent` helper

### 4. renderMyComponent Helper Function

**Purpose:** Factory function that renders the component with default or custom props.

**Pattern:**
```typescript
function renderMyComponent(props?: Partial<MyComponentProps>) {
  const defaultProps: MyComponentProps = {
    title: 'Test Title',
    onSubmit: vi.fn(),
    items: [],
  };

  return render(<MyComponent {...defaultProps} {...props} />);
}
```

**Rules:**
- Accept partial props (optional)
- Define sensible defaults for all required props
- Use `vi.fn()` for callback props
- Spread defaults first, then custom props
- Return the result of `render()`

### 5. Testing Sub-Component Props

**Access the mock to verify props:**
```typescript
import { SubComponentA } from '../src/components/SubComponentA';

it('should pass correct props to SubComponentA', () => {
  renderMyComponent({ title: 'My Title', count: 5 });

  expect(SubComponentA).toHaveBeenCalledWith(
    expect.objectContaining({
      title: 'My Title',
      count: 5
    }),
    expect.anything() // React context
  );
});
```

**Rules:**
- Import the mocked component at the top
- Use `expect(MockedComponent).toHaveBeenCalledWith()`
- Use `expect.objectContaining()` to match props
- Use `expect.anything()` as second arg (React context)

### 6. Testing Callbacks

**Simulate callback invocation to test handlers:**
```typescript
it('should call onSubmit when button is clicked', () => {
  const mockOnSubmit = vi.fn();
  const { SubButton } = require('../src/components/SubButton');

  renderMyComponent({ onSubmit: mockOnSubmit });

  // Get the onClick prop passed to SubButton
  const onClickProp = SubButton.mock.calls[0][0].onClick;

  // Simulate the click
  onClickProp();

  expect(mockOnSubmit).toHaveBeenCalled();
});
```

**Rules:**
- Pass `vi.fn()` as callback props
- Extract callback from mock's call arguments
- Invoke the callback to test the handler
- Assert the handler was called correctly

### 7. Testing Conditional Rendering

**Test different branches:**
```typescript
it('should render ErrorMessage when error prop is provided', () => {
  const { ErrorMessage } = require('../src/components/ErrorMessage');

  renderMyComponent({ error: 'Something went wrong' });

  expect(ErrorMessage).toHaveBeenCalledWith(
    expect.objectContaining({
      message: 'Something went wrong'
    }),
    expect.anything()
  );
});

it('should not render ErrorMessage when no error', () => {
  const { ErrorMessage } = require('../src/components/ErrorMessage');

  renderMyComponent({ error: null });

  expect(ErrorMessage).not.toHaveBeenCalled();
});
```

### 8. Testing Lists and Iterations

**Test components rendered in loops:**
```typescript
it('should render ListItem for each item', () => {
  const { ListItem } = require('../src/components/ListItem');
  const items = [
    { id: '1', name: 'Item 1' },
    { id: '2', name: 'Item 2' },
    { id: '3', name: 'Item 3' }
  ];

  renderMyComponent({ items });

  expect(ListItem).toHaveBeenCalledTimes(3);
  expect(ListItem).toHaveBeenNthCalledWith(
    1,
    expect.objectContaining({ id: '1', name: 'Item 1' }),
    expect.anything()
  );
  expect(ListItem).toHaveBeenNthCalledWith(
    2,
    expect.objectContaining({ id: '2', name: 'Item 2' }),
    expect.anything()
  );
  expect(ListItem).toHaveBeenNthCalledWith(
    3,
    expect.objectContaining({ id: '3', name: 'Item 3' }),
    expect.anything()
  );
});
```

## Workflow

### Create Workflow

1. **Identify the component** - Determine which component to test
2. **Locate the component file** - Use Glob to find the component definition
3. **Read the component** - Understand props, sub-components, logic branches
4. **Identify sub-components** - List all imported components to mock
5. **Ensure `__tests__` exists** - Create folder if needed (sibling to `/src`)
6. **Verify @testing-library/react** - Check package.json
7. **Create test file** in `__tests__/MyComponent.spec.tsx` with:
   - All required imports (including React)
   - Mock declarations for all sub-components
   - Main describe block
   - `renderMyComponent` helper function
   - `beforeEach` to clear mocks
   - Test cases covering all scenarios

### Update Workflow

1. **Read existing test and component** - Compare current state
2. **Identify changes**:
   - New sub-components → Add mocks
   - Changed props → Update test cases
   - New logic branches → Add test cases
   - Removed functionality → Remove tests
3. **Apply updates using Edit tool** - Targeted changes only
4. **Verify coverage** - Ensure all logic branches tested

### Update Guidelines

- **Preserve structure** - Use Edit tool, not Write
- **Maintain consistency** - Follow existing patterns
- **Keep descriptive names** - Clear, behavior-focused
- **Don't delete passing tests** - Only update broken/obsolete tests
- **Add missing coverage** - Test new logic and props

## Best Practices

1. **Test Logic, Not UI** - Focus on props passed and callbacks invoked
2. **Mock All Sub-Components** - Test the component in complete isolation
3. **Descriptive Test Names** - Explain expected behavior clearly
4. **Clear Mocks Between Tests** - Use `beforeEach` with `vi.clearAllMocks()`
5. **Test All Branches** - Cover conditional rendering, loops, error states
6. **Test Callbacks** - Simulate sub-component callbacks to test handlers
7. **Use expect.objectContaining** - Match specific props without over-specifying

## Common Pitfalls to Avoid

1. ❌ **Don't Import Sub-Components Normally** - They should be mocked, not imported
2. ❌ **Don't Forget React Import** - Required for JSX in this project
3. ❌ **Don't Forget beforeEach** - Mocks persist between tests
4. ❌ **Don't Test UI Appearance** - Focus on logic and prop passing
5. ❌ **Don't Skip expect.anything()** - It's needed as the second argument for React context
6. ❌ **Don't Forget to Mock Everything** - ALL sub-components must be mocked

## Example Reference

See `examples.md` in the same directory for complete working examples of:
- Simple component with sub-components
- Component with conditional rendering
- Component with lists and iterations
- Component with callbacks and handlers
- Component with complex prop passing
- Component with multiple branches

## Important Notes

### File Organization
- Tests in `__tests__/` at package root (sibling to `/src`)
- Use `.tsx` extension
- Match component name exactly

### Dependencies
- Ensure `@testing-library/react` is installed
- Use `vi.mock()` for all sub-components
- Mock at the module level, not inside tests

### Test Quality
- Many small tests > few large tests
- Test happy path and error cases
- Test all conditional branches
- Descriptive test names
- Simple, focused tests

### Running Tests
After creating/updating:
1. Run `pnpm test` to verify tests pass
2. Run `pnpm lint` to check linting
3. Run `pnpm build` to verify TypeScript compiles

### Mocking Best Practices
- Always use `vi.fn()` for mock components
- Return simple `<div>` elements with `data-testid`
- Clear mocks in `beforeEach`
- Import mocked components when you need to assert on them
- Use `expect.objectContaining()` to verify props
