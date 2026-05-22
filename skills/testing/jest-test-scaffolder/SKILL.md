---
name: jest-test-scaffolder
description: "Scaffolds Jest unit tests for React components and hooks. Use when creating tests for frontend components."
---

# Jest Test Scaffolder Workflow

This skill creates comprehensive unit tests for React components using Jest, React Testing Library, and user-event.

## Workflow Steps

1. **Identify component to test:**
   - Ask for component file path (e.g., `src/components/ui/Button/Button.tsx`)
   - Read component file to extract:
     - Component name
     - Props interface/types
     - Event handlers
     - Component role (button, input, form, etc.)
   - Determine test location: `{{COMPONENT_DIR}}/__tests__/{{COMPONENT_NAME}}.test.tsx`

2. **Analyze component structure:**
   - Extract prop names and types from TypeScript interface
   - Identify event handlers (onClick, onChange, onSubmit, etc.)
   - Determine accessibility role (button, textbox, combobox, etc.)
   - Identify state variations (disabled, loading, error, etc.)
   - Check for conditional rendering

3. **Generate test file:**
   - Read template: `.claude/skills/jest-test-scaffolder/templates/component.test.tsx.tpl`
   - Replace placeholders:
     - `{{COMPONENT_NAME}}` - Component name (PascalCase)
     - `{{COMPONENT_PATH}}` - Relative import path
     - `{{COMPONENT_ROLE}}` - Accessibility role (button, textbox, etc.)
     - `{{DEFAULT_PROPS}}` - Default props for rendering
     - `{{EVENT_HANDLERS}}` - Event handler tests
     - `{{STATE_TESTS}}` - State variation tests (disabled, loading, etc.)
   - Write to: `{{COMPONENT_DIR}}/__tests__/{{COMPONENT_NAME}}.test.tsx`

4. **Include comprehensive test scenarios:**
   - ✅ **Render Test**: Component renders without errors
   - ✅ **Props Test**: Component accepts and displays props correctly
   - ✅ **Interaction Test**: User interactions trigger expected behavior
   - ✅ **State Test**: Component handles state changes (disabled, loading, etc.)
   - ✅ **Accessibility Test**: Component is accessible (role, labels)
   - ⚠️ **Edge Cases**: Empty props, long text, null values (TODO placeholders)
   - ⚠️ **Snapshot Test**: Visual regression (TODO placeholder)

5. **Use React Testing Library best practices:**
   - Use `screen` queries (getByRole, getByText, getByLabelText)
   - Use `userEvent` for realistic interactions
   - Use `jest.fn()` for Jest mocks
   - Avoid implementation details (no enzyme shallow rendering)
   - Test accessibility (roles, labels, keyboard navigation)

6. **Report success:**
   - Show test file path
   - Display test coverage (number of test cases)
   - Provide command to run tests: `yarn test {{COMPONENT_NAME}}`
   - Remind user to add edge case tests

## For React Hooks

When testing custom React hooks:

1. **Use template:** `.claude/skills/jest-test-scaffolder/templates/hook.test.tsx.tpl`
2. **Use `@testing-library/react` renderHook:**
   ```typescript
   import { renderHook, act } from "@testing-library/react";
   import { useCustomHook } from "./useCustomHook";
   ```
3. **Test hook behavior:**
   - Initial state
   - State updates via `act()`
   - Return values
   - Side effects

## Template Structure

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';
import { {{COMPONENT_NAME}} } from './{{COMPONENT_NAME}}';

describe('{{COMPONENT_NAME}}', () => {
  it('renders without errors', () => {
    render(<{{COMPONENT_NAME}} {{DEFAULT_PROPS}} />);
    expect(screen.getByRole('{{ROLE}}')).toBeInTheDocument();
  });

  it('handles user interactions', async () => {
    const user = userEvent.setup();
    const mock{{HANDLER}} = jest.fn();
    render(<{{COMPONENT_NAME}} on{{HANDLER}}={mock{{HANDLER}}} />);

    await user.click(screen.getByRole('{{ROLE}}'));
    expect(mock{{HANDLER}}).toHaveBeenCalledTimes(1);
  });

  it('handles disabled state', async () => {
    const user = userEvent.setup();
    const mockHandler = jest.fn();
    render(<{{COMPONENT_NAME}} disabled on{{HANDLER}}={mockHandler} />);

    const element = screen.getByRole('{{ROLE}}');
    expect(element).toBeDisabled();

    await user.click(element);
    expect(mockHandler).not.toHaveBeenCalled();
  });

  // TODO: Add accessibility tests
  // TODO: Add snapshot tests
  // TODO: Add edge case tests (empty props, long text, null values)
});
```

## Example Usage

```
User: "Create tests for the Button component"

Claude (using jest-test-scaffolder):
1. Reads src/components/ui/Button/Button.tsx
2. Extracts props: { children, onClick, disabled, variant, size }
3. Generates src/components/ui/Button/__tests__/Button.test.tsx
4. Creates 5 test cases:
   - Renders with correct text
   - Calls onClick handler when clicked
   - Is disabled when disabled prop is true
   - Renders correct variant styles (TODO)
   - Handles different sizes (TODO)

Files created:
- src/components/ui/Button/__tests__/Button.test.tsx (42 lines, 3 complete tests, 2 TODO tests)

Run tests:
yarn test Button

Test coverage:
✅ Render test
✅ Click interaction test
✅ Disabled state test
⚠️ Variant test (TODO)
⚠️ Size test (TODO)
```

## Pattern Matching

This skill follows the existing test pattern from:

- `src/components/ui/Button/__tests__/Button.test.tsx` (36 lines, 3 tests)
- Uses `describe` and `it` blocks
- Uses `screen.getByRole` for queries
- Uses `userEvent.setup()` and `await user.click()`
- Uses `jest.fn()` for Jest mocks
- Tests rendering, interactions, and state

## Best Practices

1. **Test user behavior, not implementation:**
   - Query by role, label, text (user-visible)
   - Avoid querying by class names or test IDs (unless necessary)
   - Test what users see and do

2. **Use userEvent over fireEvent:**
   - More realistic user interactions
   - Handles complex interactions (hover, tab, type)
   - Follows browser behavior

3. **Keep tests simple and focused:**
   - One assertion per test (when possible)
   - Clear test descriptions
   - Avoid complex setup

4. **Test accessibility:**
   - Use semantic roles
   - Verify labels and descriptions
   - Test keyboard navigation

5. **Mock external dependencies:**
   - Mock API calls
   - Mock context providers
   - Mock navigation (useNavigate, useRouter)

## Jest vs Vitest

This skill uses **Jest** (not Vitest):

- `jest.fn()` instead of `vi.fn()`
- `jest.mock()` instead of `vi.mock()`
- `jest.spyOn()` instead of `vi.spyOn()`
- Everything else is the same (React Testing Library patterns)

## When NOT to Use This Skill

- ❌ E2E tests → Use `webapp-testing` skill (Playwright)
- ❌ Integration tests → Use `api-integration-test-scaffolder`
- ❌ Backend tests → Use `pytest-test-scaffolder`
- ❌ Storybook stories → Use `storybook-scaffolder`
