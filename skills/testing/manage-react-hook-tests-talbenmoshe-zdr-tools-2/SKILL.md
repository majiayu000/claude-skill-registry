---
name: manage-react-hook-tests
description: Create or update test files for React hooks. Use when user asks to "create hook tests", "test useMyHook", "generate tests for hook", "update hook tests", or mentions needing tests for a React hook. Generates vitest test files with renderHook, Fake context providers, and proper test structure.
---

# Manage React Hook Tests Skill

This skill helps you create or update test files for React hooks. Tests follow a specific pattern with vitest, `renderHook` from React Testing Library, and Fake context providers for controlled testing.

## When to Use This Skill

Use this skill when you need to:
- **Create** a new test file for a React hook
- **Update** an existing test file when the hook changes
- **Generate** test coverage for hook logic and return values

The skill will generate/update:
- A test file with vitest and React Testing Library imports
- A `renderMyHook` helper function using `renderHook`
- Individual test cases for different hook behaviors and branches
- Proper setup with Fake context providers when needed

## Usage

Invoke this skill when the user asks to:
- "Create tests for [useMyHook]"
- "Generate a test file for [useMyHook]"
- "I need tests for [useMyHook]"
- "Update tests for [useMyHook]"
- "The [useMyHook] changed, update its tests"
- "Test [useMyHook]"

## Core Principles

### Testing Philosophy
1. **Hook-Driven**: Test the hook's behavior, return values, and side effects
2. **Context Isolation**: Use Fake context providers to isolate the hook from external dependencies
3. **Controlled Testing**: Use Fake builders to control all dependencies and return values
4. **Single Responsibility**: Each `it` block should test one specific scenario
5. **Avoid vi.mock for Internal**: Use Fakes for internal dependencies; only use `vi.mock` for external libraries

## Prerequisites

Before creating/updating hook tests:
1. **Verify the hook exists** - The hook you're testing must already be defined
2. **Check for existing test file** - Use Glob to search for existing `.spec.tsx` file
3. **Identify hook dependencies** - Determine what contexts or other hooks it uses
4. **Locate Fake providers** - Find available Fake context providers (usually in the same package under `/fakes`)
5. **Check for @testing-library/react** - Verify that `@testing-library/react` is installed (for `renderHook`)

## Create vs Update Decision

**If test file exists:** Update mode
- Read the existing test file
- Read the hook definition
- Compare and identify what's missing or outdated
- Update the test to match current implementation

**If test file does NOT exist:** Create mode
- Read the hook definition
- Identify all dependencies and context requirements
- Generate complete test file from scratch

## Test File Location

**CRITICAL**: Test files MUST be in the `__tests__` folder, which is a **SIBLING** of the `/src` folder, NOT inside it.

### Directory Structure
```
packages/
  my-package/
    src/
      hooks/
        useMyHook.ts
    __tests__/              # Sibling to src/, NOT inside src/
      useMyHook.spec.tsx    # .tsx extension for React components
```

### Naming Convention
For a hook named `useMyHook`:
- Test file: `useMyHook.spec.tsx` (matches hook name exactly, with `.tsx` extension)
- Located in: `packages/my-package/__tests__/useMyHook.spec.tsx`

## Test File Structure

### 1. Imports

**Import Rules:**
- Import React (required for this project's JSX transform)
- Import vitest utilities from `'vitest'`
- Import `renderHook` (and `act` if needed) from `'@testing-library/react'`
- Import the hook being tested
- Import Fake context providers from `/fakes` subpath
- Import Fake builders for services/dependencies when needed

**Example:**
```typescript
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useMyHook } from '../src/hooks/useMyHook';
import { FakeMyContextProvider } from '../fakes';
import { FakeServiceBuilder } from '@someScope/some-library/fakes';
import type { IService } from '@someScope/some-library';
```

### 2. Main Describe Block

```typescript
describe('useMyHook', () => {
  // Helper function
  function renderMyHook(/* overrides */): { /* return type */ } {
    // ...
  }

  // Test cases
  it('should return initial state', () => {
    // Test...
  });
});
```

**Structure Rules:**
- Main describe uses the hook name (e.g., `'useMyHook'`)
- Contains one `renderMyHook` helper function at the top
- All test cases use the `renderMyHook` helper
- Tests cover all branches and return values

### 3. renderMyHook Helper Function

**Purpose:** Factory function that renders the hook with all necessary context providers and dependencies, allowing for easy overrides in tests.

**Pattern with Context:**
```typescript
function renderMyHook(overrides?: {
  service?: IService;
}) {
  const service = overrides?.service ?? new FakeServiceBuilder().build();

  const hookRenderResult = renderHook(() => useMyHook(), {
    wrapper: ({ children }) => (
      <FakeMyContextProvider service={service}>
        {children}
      </FakeMyContextProvider>
    ),
  });

  return {
    hookRenderResult,
    service,
  };
}
```

**Pattern without Context:**
```typescript
function renderMyHook(params?: {
  initialValue?: string;
}) {
  const hookRenderResult = renderHook(() => useMyHook(params?.initialValue ?? 'default'));

  return {
    hookRenderResult,
  };
}
```

**Rules:**
- Accept `overrides` parameter for context dependencies
- Accept `params` parameter for hook arguments
- Use nullish coalescing (`??`) for default Fake instances
- Use `renderHook` with `wrapper` option for context providers
- Return object with `hookRenderResult` and all dependencies

### 4. Finding Context Dependencies

**How to Identify:**
1. Read the hook file and look for `useContext` calls or other context hooks
2. Search for the context provider in the codebase
3. Check if a Fake version exists in `/fakes` folder
4. If no Fake exists, create one or use `vi.mock` for external dependencies

**Multiple Contexts:**
Nest providers in the wrapper:
```typescript
wrapper: ({ children }) => (
  <FakeContextA>
    <FakeContextB>
      {children}
    </FakeContextB>
  </FakeContextA>
)
```

### 5. Writing Test Cases

**Structure:**
- Use descriptive test names explaining the expected behavior
- Follow Arrange-Act-Assert pattern
- Access hook result via `hookRenderResult.result.current`
- Use `act()` for state updates
- Use `await act(async () => ...)` for async operations

**Example:**
```typescript
it('should return expected value', () => {
  const { hookRenderResult } = renderMyHook({
    service: new FakeServiceBuilder()
      .withGetDataReturnValue({ id: '123' })
      .build()
  });

  expect(hookRenderResult.result.current.data).toEqual({ id: '123' });
});
```

### 6. Testing State Updates

Always wrap state changes in `act()`:
```typescript
it('should update state when action is called', () => {
  const { hookRenderResult } = renderMyHook();

  act(() => {
    hookRenderResult.result.current.updateValue('new value');
  });

  expect(hookRenderResult.result.current.value).toBe('new value');
});
```

### 7. Testing Async Operations

Use `await act(async () => ...)`:
```typescript
it('should save successfully', async () => {
  const { hookRenderResult } = renderMyHook();

  await act(async () => {
    await hookRenderResult.result.current.save();
  });

  expect(hookRenderResult.result.current.isSaving).toBe(false);
});
```

### 8. Mocking Dependencies

**Preferred (Fake Providers):**
```typescript
const { hookRenderResult } = renderMyHook({
  service: new FakeServiceBuilder()
    .withFetchDataReturnValue(Promise.resolve({ success: true }))
    .build()
});
```

**When to use vi.mock:**
- External React hooks from 3rd party libraries
- Browser APIs
- Modules without Fake implementations

## Workflow

### Create Workflow

1. **Identify the hook** - Determine which hook to test
2. **Locate the hook file** - Use Glob to find the hook definition
3. **Read the hook** - Understand behavior, return values, context usage
4. **Identify dependencies** - Look for context hooks and other dependencies
5. **Locate Fakes** - Find Fake providers and builders
6. **Ensure `__tests__` exists** - Create folder if needed (sibling to `/src`)
7. **Verify @testing-library/react** - Check package.json
8. **Create test file** in `__tests__/useMyHook.spec.tsx` with:
   - All required imports (including React)
   - Main describe block
   - `renderMyHook` helper function
   - Test cases covering all scenarios

### Update Workflow

1. **Read existing test and hook** - Compare current state
2. **Identify changes**:
   - New return values → Add test cases
   - Changed logic → Update test cases
   - New dependencies → Update `renderMyHook` and imports
   - Removed functionality → Remove tests
3. **Apply updates using Edit tool** - Targeted changes only
4. **Verify coverage** - Ensure all logic branches tested

### Update Guidelines

- **Preserve structure** - Use Edit tool, not Write
- **Maintain consistency** - Follow existing patterns
- **Keep descriptive names** - Clear, behavior-focused
- **Don't delete passing tests** - Only update broken/obsolete tests
- **Add missing coverage** - Test new logic

## Best Practices

1. **Test Behavior, Not Implementation** - Focus on return values and side effects
2. **Descriptive Test Names** - Explain expected behavior clearly
3. **Arrange-Act-Assert** - Structure tests consistently
4. **Use act() for Updates** - Always wrap state changes
5. **Test Edge Cases** - Null, undefined, empty values, errors
6. **Appropriate Matchers** - Use correct expect matchers for the assertion

## Common Pitfalls to Avoid

1. ❌ **Don't Render Hook Directly** - Always use `renderHook()`
2. ❌ **Don't Forget React Import** - Required for JSX in this project
3. ❌ **Don't Forget act()** - State updates need to be wrapped
4. ❌ **Don't Use vi.mock for Internal** - Use Fake providers instead
5. ❌ **Don't Forget async/await** - Async operations need proper handling

## Example Reference

See `examples.md` in the same directory for complete working examples of:
- Simple hooks returning context values
- Hooks with complex logic and multiple return values
- Hooks with parameters
- Hooks with state management
- Standalone hooks without context
- Hooks using multiple contexts

## Important Notes

### File Organization
- Tests in `__tests__/` at package root (sibling to `/src`)
- Use `.tsx` extension
- Match hook name exactly

### Dependencies
- Ensure `@testing-library/react` is installed
- Use Fake providers from `/fakes` subpath
- Create Fakes if they don't exist

### Test Quality
- Many small tests > few large tests
- Test happy path and error cases
- Test edge cases and boundaries
- Descriptive test names
- Simple, focused tests

### Running Tests
After creating/updating:
1. Run `pnpm test` to verify tests pass
2. Run `pnpm lint` to check linting
3. Run `pnpm build` to verify TypeScript compiles
