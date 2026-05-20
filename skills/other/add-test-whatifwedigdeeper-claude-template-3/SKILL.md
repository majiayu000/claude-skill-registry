---
skill: add-test
description: Add unit tests for a component or function
arguments: component or function name
---

# Add Tests: $ARGUMENTS

Create comprehensive unit tests for the specified component or function.

## Process

### 1. Locate Source File

Search in order:
- `components/$ARGUMENTS.tsx` (React component)
- `lib/$ARGUMENTS.ts` (utility function)
- `app/$ARGUMENTS.tsx` (page component)

### 2. Analyze Source

Read the file to identify:
- Exported functions/components
- Props interfaces
- State management
- Event handlers
- Key functionality to test

### 3. Create Test File

Place test adjacent to source: `[name].test.tsx` or `[name].test.ts`

### 4. Generate Tests

**For React components:**

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  test('renders correctly', () => {
    render(<ComponentName />);
    expect(screen.getByTestId('component-name')).toBeInTheDocument();
  });

  test('handles user interaction', () => {
    render(<ComponentName />);
    fireEvent.click(screen.getByRole('button'));
    // assert expected behavior
  });

  test('handles empty state', () => { /* ... */ });
  test('handles error state', () => { /* ... */ });
});
```

**For utility functions:**

```typescript
import { functionName } from './fileName';

describe('functionName', () => {
  test('returns expected output', () => {
    expect(functionName(input)).toBe(expected);
  });

  test('handles empty input', () => { /* ... */ });
  test('handles edge cases', () => { /* ... */ });
  test('throws on invalid input', () => {
    expect(() => functionName(invalid)).toThrow();
  });
});
```

### 5. Run Tests

```bash
npm test -- $ARGUMENTS.test
```

Fix any failures, then report results.

## Coverage Requirements

- Happy path scenarios
- Edge cases (empty, null, boundary values)
- Error states
- User interactions (for components)
- Accessibility (keyboard navigation)

## Best Practices

- Use `data-testid` for stable selectors
- Mock localStorage if needed
- Tests should be independent and deterministic
- Descriptive test names that explain the scenario
