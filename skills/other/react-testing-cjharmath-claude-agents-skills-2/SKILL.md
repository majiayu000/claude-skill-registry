---
name: react-testing
description: Testing patterns for React with Jest and React Testing Library. Use when writing tests, mocking modules, testing Zustand stores, or debugging test failures in React web applications.
---

# React Testing (Web)

## Problem Statement

React testing requires understanding component rendering, user interactions, and async state management. This skill covers Jest with React Testing Library patterns for web applications.

---

## Pattern: Zustand Store Testing

**Problem:** Store state persists between tests, causing flaky tests.

```typescript
import { useAppStore } from '@/stores/appStore';

const initialState = {
  items: [],
  loading: false,
  error: null,
};

describe('App Store', () => {
  // Reset store before each test
  beforeEach(() => {
    useAppStore.setState(initialState, true); // true = replace entire state
  });

  it('adds item to store', async () => {
    const store = useAppStore.getState();

    await store.addItem({ id: '1', name: 'Test' });

    expect(useAppStore.getState().items).toHaveLength(1);
  });

  it('handles loading state', async () => {
    const store = useAppStore.getState();

    const loadPromise = store.fetchItems();
    expect(useAppStore.getState().loading).toBe(true);

    await loadPromise;
    expect(useAppStore.getState().loading).toBe(false);
  });
});
```

**Key points:**
- Use `setState(initialState, true)` to replace (not merge) state
- Get fresh state with `getState()` after async operations
- Don't rely on component re-renders in store tests

---

## Pattern: Async Store Operations

**Problem:** Testing async Zustand actions with proper waiting.

```typescript
import { act, waitFor } from '@testing-library/react';

it('loads data correctly', async () => {
  const store = useAppStore.getState();

  // Wrap async store operations in act
  await act(async () => {
    await store.loadData('123');
  });

  // Verify state after async completes
  await waitFor(() => {
    const state = useAppStore.getState();
    expect(Object.keys(state.data).length).toBeGreaterThan(0);
  });
});

// For complex flows, verify each step
it('completes multi-step flow', async () => {
  const store = useAppStore.getState();

  // Step 1
  await act(async () => {
    await store.loadItems();
  });
  expect(useAppStore.getState().items).toBeDefined();

  // Step 2
  await act(async () => {
    await store.processItems();
  });
  expect(useAppStore.getState().processed).toBe(true);
});
```

---

## Pattern: Component Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('ItemCard', () => {
  const mockItem = {
    id: '1',
    title: 'Test Item',
    price: 99.99,
  };

  it('displays item data', () => {
    render(<ItemCard item={mockItem} />);

    expect(screen.getByText('Test Item')).toBeInTheDocument();
    expect(screen.getByText('$99.99')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const onClick = jest.fn();

    render(<ItemCard item={mockItem} onClick={onClick} />);

    await user.click(screen.getByRole('button'));

    expect(onClick).toHaveBeenCalledWith(mockItem.id);
  });

  it('shows loading state', () => {
    render(<ItemCard item={mockItem} loading />);

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
});
```

---

## Pattern: React Query Testing

**Problem:** Components using React Query need QueryClientProvider.

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor } from '@testing-library/react';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
    },
  });
}

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}

// Usage in tests
it('fetches and displays data', async () => {
  renderWithQuery(<UserProfile userId="123" />);

  // Shows loading initially
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Wait for data
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
```

---

## Pattern: Custom Hook Testing

```typescript
import { renderHook, act, waitFor } from '@testing-library/react';

describe('useAuth', () => {
  it('signs in user', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider, // If hook needs context
    });

    await act(async () => {
      await result.current.signIn('test@example.com', 'password');
    });

    expect(result.current.user).toBeDefined();
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('handles sign in error', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider,
    });

    await act(async () => {
      try {
        await result.current.signIn('invalid@example.com', 'wrong');
      } catch (e) {
        // Expected
      }
    });

    expect(result.current.error).toBe('Invalid credentials');
  });
});

// Hook with Zustand
describe('useUserData', () => {
  beforeEach(() => {
    useUserStore.setState(initialState, true);
  });

  it('returns current user data', () => {
    // Pre-populate store
    useUserStore.setState({ user: { id: '1', name: 'Test' } });

    const { result } = renderHook(() => useUserData());

    expect(result.current.user.name).toBe('Test');
  });
});
```

---

## Pattern: Mocking API Calls

```typescript
// Mock fetch globally
global.fetch = jest.fn();

beforeEach(() => {
  (fetch as jest.Mock).mockClear();
});

it('fetches user data', async () => {
  (fetch as jest.Mock).mockResolvedValueOnce({
    ok: true,
    json: async () => ({ id: '1', name: 'John' }),
  });

  render(<UserProfile userId="1" />);

  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });

  expect(fetch).toHaveBeenCalledWith('/api/users/1');
});

// Mock specific module
jest.mock('@/api/users', () => ({
  getUser: jest.fn(),
  updateUser: jest.fn(),
}));

import { getUser, updateUser } from '@/api/users';

it('loads and updates user', async () => {
  (getUser as jest.Mock).mockResolvedValue({ id: '1', name: 'John' });
  (updateUser as jest.Mock).mockResolvedValue({ id: '1', name: 'Jane' });

  // Test component that uses these
});
```

---

## Pattern: Router Testing

```typescript
import { MemoryRouter, Routes, Route } from 'react-router-dom';

function renderWithRouter(ui: React.ReactElement, { route = '/' } = {}) {
  return render(
    <MemoryRouter initialEntries={[route]}>
      {ui}
    </MemoryRouter>
  );
}

// Test navigation
it('navigates to profile on button click', async () => {
  const user = userEvent.setup();

  renderWithRouter(
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/profile" element={<ProfilePage />} />
    </Routes>
  );

  await user.click(screen.getByText('Go to Profile'));

  expect(screen.getByText('Profile Page')).toBeInTheDocument();
});

// Test with route params
it('displays user from route params', async () => {
  renderWithRouter(
    <Routes>
      <Route path="/users/:id" element={<UserPage />} />
    </Routes>,
    { route: '/users/123' }
  );

  await waitFor(() => {
    expect(screen.getByText('User 123')).toBeInTheDocument();
  });
});
```

---

## Pattern: Form Testing

```typescript
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('submits form with entered data', async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Sign In' }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={jest.fn()} />);

    // Submit without filling form
    await user.click(screen.getByRole('button', { name: 'Sign In' }));

    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Password is required')).toBeInTheDocument();
  });

  it('disables submit while loading', async () => {
    render(<LoginForm onSubmit={jest.fn()} loading />);

    expect(screen.getByRole('button', { name: 'Sign In' })).toBeDisabled();
  });
});
```

---

## Pattern: Avoiding act() Warnings

**Problem:** "Warning: An update inside a test was not wrapped in act(...)"

```typescript
// WRONG - state update happens after test
it('loads data', () => {
  render(<DataComponent />);
  // Component fetches data async, updates state after test ends
});

// CORRECT - wait for async completion
it('loads data', async () => {
  render(<DataComponent />);

  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});

// CORRECT - use findBy* (has built-in waitFor)
it('loads data', async () => {
  render(<DataComponent />);

  const element = await screen.findByText('Data loaded');
  expect(element).toBeInTheDocument();
});
```

---

## Pattern: Snapshot Testing

**When to use:**
- UI components with stable structure
- Design system components
- Components where visual regression matters

**When to avoid:**
- Components with dynamic content
- Components that change frequently
- Large component trees (brittle)

```typescript
// Good snapshot candidate - stable UI component
it('renders correctly', () => {
  const { container } = render(<Button variant="primary">Submit</Button>);
  expect(container).toMatchSnapshot();
});

// Bad snapshot candidate - dynamic content
it('renders user list', () => {
  // Don't snapshot - list content varies
  // Instead, test specific behaviors
});
```

---

## Pattern: Testing Context Providers

```typescript
// Create a wrapper with all providers
function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

function renderWithProviders(ui: React.ReactElement) {
  return render(ui, { wrapper: AllProviders });
}

// Use in tests
it('renders with all context', () => {
  renderWithProviders(<Dashboard />);
  // Component has access to all providers
});
```

---

## Test Commands

```bash
npm test                      # Run all tests
npm test -- --watch           # Watch mode
npm test -- --coverage        # Coverage report
npm test -- Button            # Run specific test file
npm test -- --updateSnapshot  # Update snapshots
npm test -- --runInBand       # Run tests serially (debugging)
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "Cannot find module" | Check jest moduleNameMapper config |
| act() warning | Wrap state updates in act(), use waitFor/findBy |
| Store state bleeding | Add beforeEach with setState reset |
| Async test timeout | Increase timeout or check for hanging promises |
| Mock not working | Verify mock path matches import path exactly |
| Query not found | Use findBy* for async content, check accessibility |

---

## Recommended File Structure

```
__tests__/
  utils/
    test-utils.tsx         # Custom render with providers
    query-test-utils.tsx   # QueryClient wrapper
jest.setup.js              # Global mocks and setup
jest.config.js             # Jest configuration
```
