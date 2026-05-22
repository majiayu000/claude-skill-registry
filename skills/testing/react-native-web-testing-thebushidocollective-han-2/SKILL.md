---
name: react-native-web-testing
description: Use when testing React Native Web applications. Provides patterns for Jest, React Native Testing Library, component testing, and web-specific testing strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Native Web - Testing

Comprehensive testing patterns for React Native Web applications using Jest and React Native Testing Library.

## Key Concepts

### React Native Testing Library

The standard testing library for React Native components:

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<Button title="Click me" onPress={onPress} />);

    const button = screen.getByText('Click me');
    fireEvent.press(button);

    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

### Jest Configuration

Configure Jest for React Native Web:

```javascript
// jest.config.js
module.exports = {
  preset: 'react-native',
  moduleNameMapper: {
    '^react-native$': 'react-native-web',
  },
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|react-native-web)/)',
  ],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
};
```

### Testing Utilities

Common testing utilities and helpers:

```typescript
import { render, RenderOptions } from '@testing-library/react-native';
import { ReactElement } from 'react';
import { ThemeProvider } from './theme';

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  theme?: Theme;
}

export function renderWithProviders(
  ui: ReactElement,
  { theme = defaultTheme, ...options }: CustomRenderOptions = {}
) {
  return render(
    <ThemeProvider value={theme}>
      {ui}
    </ThemeProvider>,
    options
  );
}
```

## Best Practices

### Component Testing

✅ Test user interactions and behavior:

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits form with valid credentials', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    const emailInput = screen.getByPlaceholderText('Email');
    const passwordInput = screen.getByPlaceholderText('Password');
    const submitButton = screen.getByText('Login');

    fireEvent.changeText(emailInput, 'user@example.com');
    fireEvent.changeText(passwordInput, 'password123');
    fireEvent.press(submitButton);

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123',
      });
    });
  });

  it('shows error for invalid email', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    const emailInput = screen.getByPlaceholderText('Email');
    const submitButton = screen.getByText('Login');

    fireEvent.changeText(emailInput, 'invalid-email');
    fireEvent.press(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid email address')).toBeTruthy();
    });
  });
});
```

### Async Testing

✅ Use waitFor for async operations:

```typescript
import { render, screen, waitFor } from '@testing-library/react-native';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockUser),
      })
    ) as jest.Mock;

    render(<UserProfile userId="1" />);

    // Check loading state
    expect(screen.getByTestId('loading-indicator')).toBeTruthy();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeTruthy();
      expect(screen.getByText('john@example.com')).toBeTruthy();
    });

    expect(screen.queryByTestId('loading-indicator')).toBeNull();
  });
});
```

### Mocking Modules

✅ Mock navigation and other dependencies:

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';

// Mock navigation
const mockNavigate = jest.fn();
jest.mock('@react-navigation/native', () => ({
  useNavigation: () => ({
    navigate: mockNavigate,
  }),
}));

describe('HomeScreen', () => {
  it('navigates to details on item press', () => {
    render(<HomeScreen />);

    const item = screen.getByText('Item 1');
    fireEvent.press(item);

    expect(mockNavigate).toHaveBeenCalledWith('Details', { id: '1' });
  });
});
```

## Examples

### Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

### Testing with Context

```typescript
import { render, screen } from '@testing-library/react-native';
import { AuthProvider } from './auth-context';
import { ProtectedScreen } from './ProtectedScreen';

describe('ProtectedScreen', () => {
  it('shows content when authenticated', () => {
    const mockUser = { id: '1', name: 'John' };

    render(
      <AuthProvider initialUser={mockUser}>
        <ProtectedScreen />
      </AuthProvider>
    );

    expect(screen.getByText('Welcome, John')).toBeTruthy();
  });

  it('shows login prompt when not authenticated', () => {
    render(
      <AuthProvider initialUser={null}>
        <ProtectedScreen />
      </AuthProvider>
    );

    expect(screen.getByText('Please log in')).toBeTruthy();
  });
});
```

### Snapshot Testing

```typescript
import { render } from '@testing-library/react-native';
import { Card } from './Card';

describe('Card', () => {
  it('matches snapshot', () => {
    const { toJSON } = render(
      <Card title="Test Card" description="Test description" />
    );

    expect(toJSON()).toMatchSnapshot();
  });
});
```

### Integration Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from './HomeScreen';
import { DetailsScreen } from './DetailsScreen';

const Stack = createNativeStackNavigator();

function TestApp() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

describe('Navigation Flow', () => {
  it('navigates from home to details', async () => {
    render(<TestApp />);

    // On Home screen
    expect(screen.getByText('Home Screen')).toBeTruthy();

    // Navigate to Details
    const item = screen.getByText('View Details');
    fireEvent.press(item);

    // Wait for Details screen
    await waitFor(() => {
      expect(screen.getByText('Details Screen')).toBeTruthy();
    });
  });
});
```

## Common Patterns

### Testing Forms

```typescript
describe('ContactForm', () => {
  it('validates all fields before submit', async () => {
    const onSubmit = jest.fn();
    render(<ContactForm onSubmit={onSubmit} />);

    const submitButton = screen.getByText('Submit');
    fireEvent.press(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Name is required')).toBeTruthy();
      expect(screen.getByText('Email is required')).toBeTruthy();
      expect(onSubmit).not.toHaveBeenCalled();
    });
  });
});
```

### Testing Lists

```typescript
describe('ItemsList', () => {
  it('renders all items', () => {
    const items = [
      { id: '1', title: 'Item 1' },
      { id: '2', title: 'Item 2' },
      { id: '3', title: 'Item 3' },
    ];

    render(<ItemsList items={items} />);

    items.forEach(item => {
      expect(screen.getByText(item.title)).toBeTruthy();
    });
  });

  it('handles empty state', () => {
    render(<ItemsList items={[]} />);
    expect(screen.getByText('No items found')).toBeTruthy();
  });
});
```

### Testing Accessibility

```typescript
describe('Button accessibility', () => {
  it('has correct accessibility props', () => {
    render(<Button title="Submit" onPress={jest.fn()} />);

    const button = screen.getByRole('button');
    expect(button).toHaveAccessibilityState({ disabled: false });
    expect(button).toHaveAccessibilityHint('Submits the form');
  });

  it('is disabled when loading', () => {
    render(<Button title="Submit" onPress={jest.fn()} loading />);

    const button = screen.getByRole('button');
    expect(button).toHaveAccessibilityState({ disabled: true, busy: true });
  });
});
```

## Anti-Patterns

❌ Don't test implementation details:

```typescript
// Bad - testing internal state
expect(component.state.count).toBe(5);

// Good - test observable behavior
expect(screen.getByText('Count: 5')).toBeTruthy();
```

❌ Don't use querySelector or DOM methods:

```typescript
// Bad
const element = container.querySelector('.button');

// Good
const button = screen.getByRole('button');
```

❌ Don't create overly coupled tests:

```typescript
// Bad - too specific
expect(screen.getByText('Submit')).toHaveStyle({
  backgroundColor: '#007AFF',
  paddingHorizontal: 16
});

// Good - test behavior
const button = screen.getByText('Submit');
expect(button).toBeTruthy();
fireEvent.press(button);
expect(mockSubmit).toHaveBeenCalled();
```

❌ Don't forget to clean up:

```typescript
// Bad
afterEach(() => {
  // No cleanup
});

// Good
afterEach(() => {
  jest.clearAllMocks();
  cleanup();
});
```

## Related Skills

- **react-native-web-core**: Core React Native Web concepts
- **react-native-web-navigation**: Testing navigation flows
- **react-native-web-performance**: Performance testing
