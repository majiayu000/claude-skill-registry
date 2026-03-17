---
name: mobile-testing
description: Write and run tests for React Native apps using Jest and React Native Testing Library. Use when creating tests, debugging failures, or setting up test infrastructure.
allowed-tools: Bash, Read, Write, Edit
---

# Mobile Testing

Testing guide for React Native applications.

## When to Use

- Writing unit tests for components or utilities
- Creating integration tests for features
- Setting up test infrastructure
- Debugging test failures
- Improving test coverage

## Test Setup

```bash
# Install testing dependencies
npm install --save-dev jest @testing-library/react-native

# Add to package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Component Test Template

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import { MyButton } from './MyButton';

describe('MyButton', () => {
  it('renders correctly', () => {
    const { getByText } = render(<MyButton title="Click me" />);
    expect(getByText('Click me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <MyButton title="Click me" onPress={onPress} />
    );

    fireEvent.press(getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

## Hook Test Template

```typescript
import { renderHook, act } from '@testing-library/react-native';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Utility Test Template

```typescript
import { formatDate } from './formatDate';

describe('formatDate', () => {
  it('formats date correctly', () => {
    const date = new Date('2025-01-15');
    expect(formatDate(date)).toBe('2025-01-15');
  });

  it('handles invalid input', () => {
    expect(() => formatDate(null)).toThrow();
  });
});
```

## Mocking Patterns

### Mock External Module
```typescript
jest.mock('expo-notifications', () => ({
  scheduleNotificationAsync: jest.fn(),
}));
```

### Mock Database
```typescript
jest.mock('@/db/client', () => ({
  db: {
    select: jest.fn(),
    insert: jest.fn(),
  },
}));
```

### Mock Navigation
```typescript
jest.mock('expo-router', () => ({
  useRouter: () => ({
    push: jest.fn(),
    back: jest.fn(),
  }),
}));
```

## Running Tests

```bash
# Run all tests
npm test

# Watch mode (auto-rerun on changes)
npm run test:watch

# With coverage report
npm run test:coverage

# Run specific test file
npm test -- MyComponent.test.tsx

# Update snapshots
npm test -- -u
```

## Best Practices

1. **Test Behavior, Not Implementation**: Test what users see and do
2. **Use `testID` for Selection**: More reliable than text matching
3. **Mock External Dependencies**: Keep tests isolated and fast
4. **Test Edge Cases**: Empty states, errors, loading states
5. **Keep Tests Simple**: One assertion per test when possible
6. **Clean Up**: Use `beforeEach`/`afterEach` for setup/teardown

## Common Patterns

### Async Testing
```typescript
it('loads data', async () => {
  const { findByText } = render(<DataComponent />);
  expect(await findByText('Loaded')).toBeTruthy();
});
```

### Testing Forms
```typescript
it('validates input', () => {
  const { getByTestId, getByText } = render(<LoginForm />);

  fireEvent.changeText(getByTestId('email-input'), 'invalid');
  fireEvent.press(getByTestId('submit-button'));

  expect(getByText('Invalid email')).toBeTruthy();
});
```

### Testing Lists
```typescript
it('renders list items', () => {
  const items = [{ id: '1', name: 'Item 1' }];
  const { getAllByTestId } = render(<ItemList items={items} />);

  expect(getAllByTestId('list-item')).toHaveLength(1);
});
```

## Troubleshooting

- **Tests timing out**: Increase timeout or check for unresolved promises
- **Can't find element**: Use `screen.debug()` to see rendered output
- **Mock not working**: Ensure mock is before import
- **Async issues**: Use `waitFor` or `findBy` queries

## Resources

- [Jest Docs](https://jestjs.io/)
- [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)
