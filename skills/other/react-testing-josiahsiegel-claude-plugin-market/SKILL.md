---
name: react-testing
description: Complete React testing system. PROACTIVELY activate for: (1) Vitest/Jest setup and configuration, (2) React Testing Library patterns, (3) Component testing with userEvent, (4) Custom hook testing with renderHook, (5) Mocking modules and components, (6) Async component testing, (7) Context and provider testing, (8) Accessibility testing with jest-axe. Provides: Test setup, query priority, user simulation, mock patterns, integration testing. Ensures reliable tests that focus on user behavior.
---

## Quick Reference

| Tool | Purpose | Install |
|------|---------|---------|
| Vitest | Test runner | `npm i -D vitest` |
| @testing-library/react | Component testing | `npm i -D @testing-library/react` |
| @testing-library/user-event | User simulation | `npm i -D @testing-library/user-event` |
| jest-axe | Accessibility testing | `npm i -D jest-axe` |

| Query | When to Use |
|-------|-------------|
| `getByRole` | Best - accessible elements |
| `getByLabelText` | Form inputs |
| `getByText` | Static text |
| `getByTestId` | Last resort |

| Pattern | Example |
|---------|---------|
| Setup user | `const user = userEvent.setup()` |
| Click | `await user.click(button)` |
| Type | `await user.type(input, 'text')` |
| Wait for async | `await waitFor(() => expect(...))` |

## When to Use This Skill

Use for **React testing implementation**:
- Setting up Vitest or Jest with React
- Writing component tests with Testing Library
- Testing forms, async operations, hooks
- Mocking API calls and modules
- Testing components with context/providers
- Adding accessibility tests

**For component patterns**: see `react-patterns`

---

# React Testing Guide

## Testing Tools

### Setup with Vitest

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
    css: true,
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

### Setup with Jest

```bash
npm install -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', { tsconfig: 'tsconfig.json' }],
  },
};
```

## Component Testing

### Basic Component Test

```tsx
// Button.tsx
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  disabled?: boolean;
}

export function Button({ onClick, children, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
```

```tsx
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button onClick={() => {}}>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button onClick={() => {}} disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('does not call onClick when disabled', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick} disabled>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

### Testing Forms

```tsx
// LoginForm.tsx
interface LoginFormProps {
  onSubmit: (data: { email: string; password: string }) => Promise<void>;
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await onSubmit({ email, password });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p role="alert">{error}</p>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

```tsx
// LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits form with email and password', async () => {
    const handleSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('displays error message on failed submission', async () => {
    const handleSubmit = vi.fn().mockRejectedValue(new Error('Invalid credentials'));
    const user = userEvent.setup();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Invalid credentials');
    });
  });

  it('disables submit button while submitting', async () => {
    let resolveSubmit: () => void;
    const handleSubmit = vi.fn().mockImplementation(
      () => new Promise((resolve) => { resolveSubmit = resolve; })
    );
    const user = userEvent.setup();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveTextContent('Logging in...');

    resolveSubmit!();

    await waitFor(() => {
      expect(screen.getByRole('button')).not.toBeDisabled();
    });
  });
});
```

### Testing Async Components

```tsx
// UserProfile.tsx
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

```tsx
// UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserProfile } from './UserProfile';
import * as api from './api';

vi.mock('./api');

describe('UserProfile', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state initially', () => {
    vi.mocked(api.fetchUser).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<UserProfile userId="123" />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays user data when loaded', async () => {
    vi.mocked(api.fetchUser).mockResolvedValue({
      id: '123',
      name: 'John Doe',
      email: 'john@example.com',
    });

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByRole('heading')).toHaveTextContent('John Doe');
    });
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('displays error when fetch fails', async () => {
    vi.mocked(api.fetchUser).mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText(/error: network error/i)).toBeInTheDocument();
    });
  });
});
```

## Testing Hooks

### Custom Hook Testing

```tsx
// useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => setCount((c) => c + 1), []);
  const decrement = useCallback(() => setCount((c) => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);

  return { count, increment, decrement, reset };
}
```

```tsx
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());

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

  it('resets counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(7);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(5);
  });
});
```

### Testing Hooks with Dependencies

```tsx
// useFetch.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useFetch } from './useFetch';

describe('useFetch', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('fetches data successfully', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: 1, name: 'Test' }),
    });

    const { result } = renderHook(() => useFetch('/api/data'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual({ id: 1, name: 'Test' });
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
    });

    const { result } = renderHook(() => useFetch('/api/data'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBeNull();
    expect(result.current.error).toBeInstanceOf(Error);
  });

  it('refetches when URL changes', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: 1 }),
    });

    const { result, rerender } = renderHook(
      ({ url }) => useFetch(url),
      { initialProps: { url: '/api/data/1' } }
    );

    await waitFor(() => {
      expect(result.current.data).toEqual({ id: 1 });
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: 2 }),
    });

    rerender({ url: '/api/data/2' });

    await waitFor(() => {
      expect(result.current.data).toEqual({ id: 2 });
    });
  });
});
```

## Testing with Context

```tsx
// ThemeContext.tsx
const ThemeContext = createContext<{
  theme: 'light' | 'dark';
  toggle: () => void;
} | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggle = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

```tsx
// ThemedButton.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { ThemeProvider } from './ThemeContext';
import { ThemedButton } from './ThemedButton';

// Custom render function with providers
function renderWithTheme(ui: React.ReactElement) {
  return render(<ThemeProvider>{ui}</ThemeProvider>);
}

describe('ThemedButton', () => {
  it('uses light theme by default', () => {
    renderWithTheme(<ThemedButton>Click me</ThemedButton>);
    expect(screen.getByRole('button')).toHaveClass('light');
  });

  it('toggles theme on click', async () => {
    const user = userEvent.setup();
    renderWithTheme(<ThemedButton>Toggle</ThemedButton>);

    const button = screen.getByRole('button');
    expect(button).toHaveClass('light');

    await user.click(button);
    expect(button).toHaveClass('dark');

    await user.click(button);
    expect(button).toHaveClass('light');
  });
});
```

## Mocking

### Mocking Modules

```tsx
// api.ts
export async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

// UserProfile.test.tsx
import { vi } from 'vitest';

// Mock the entire module
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

// Or mock specific exports
vi.mock('./api', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./api')>();
  return {
    ...actual,
    fetchUser: vi.fn(),
  };
});
```

### Mocking Components

```tsx
// Mock a child component
vi.mock('./ExpensiveChart', () => ({
  ExpensiveChart: ({ data }: { data: number[] }) => (
    <div data-testid="mock-chart">Chart with {data.length} points</div>
  ),
}));
```

### Mocking Timers

```tsx
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Debounced Input', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('debounces input changes', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });

    render(<DebouncedInput onChange={onChange} delay={300} />);

    await user.type(screen.getByRole('textbox'), 'hello');

    // Not called yet (within debounce window)
    expect(onChange).not.toHaveBeenCalled();

    // Advance time past debounce delay
    vi.advanceTimersByTime(300);

    expect(onChange).toHaveBeenCalledWith('hello');
    expect(onChange).toHaveBeenCalledTimes(1);
  });
});
```

## Integration Testing

### Testing Data Flow

```tsx
// TodoApp.test.tsx
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { TodoApp } from './TodoApp';

describe('TodoApp Integration', () => {
  it('allows adding, completing, and deleting todos', async () => {
    const user = userEvent.setup();
    render(<TodoApp />);

    // Add a todo
    const input = screen.getByPlaceholderText(/add todo/i);
    await user.type(input, 'Buy groceries{Enter}');

    // Verify todo was added
    const todo = screen.getByText('Buy groceries');
    expect(todo).toBeInTheDocument();

    // Complete the todo
    const checkbox = screen.getByRole('checkbox');
    await user.click(checkbox);
    expect(checkbox).toBeChecked();

    // Delete the todo
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);
    expect(screen.queryByText('Buy groceries')).not.toBeInTheDocument();
  });

  it('filters todos correctly', async () => {
    const user = userEvent.setup();
    render(<TodoApp />);

    // Add todos
    const input = screen.getByPlaceholderText(/add todo/i);
    await user.type(input, 'Task 1{Enter}');
    await user.type(input, 'Task 2{Enter}');

    // Complete first task
    const checkboxes = screen.getAllByRole('checkbox');
    await user.click(checkboxes[0]);

    // Filter by active
    await user.click(screen.getByRole('button', { name: /active/i }));
    expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();

    // Filter by completed
    await user.click(screen.getByRole('button', { name: /completed/i }));
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
  });
});
```

## Accessibility Testing

```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { describe, it, expect } from 'vitest';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('Form has no accessibility violations', async () => {
    const { container } = render(<LoginForm onSubmit={() => {}} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('Navigation has no accessibility violations', async () => {
    const { container } = render(<Navigation />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Best Practices

### 1. Query Priority

```tsx
// Best - accessible queries
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText(/email/i);
screen.getByPlaceholderText(/search/i);
screen.getByText(/welcome/i);
screen.getByDisplayValue(/john/i);

// Fallback - test IDs (last resort)
screen.getByTestId('custom-element');
```

### 2. Avoid Implementation Details

```tsx
// Bad - testing implementation
expect(component.state.isOpen).toBe(true);

// Good - testing behavior
expect(screen.getByRole('dialog')).toBeVisible();
```

### 3. Test User Behavior

```tsx
// Bad - testing clicks
fireEvent.click(button);

// Good - simulating real user
const user = userEvent.setup();
await user.click(button);
```

### 4. Use Test Utilities

```tsx
// test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from './ThemeContext';

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>{children}</ThemeProvider>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { renderWithProviders as render };
```

## Additional References

For comprehensive testing patterns and recipes, see:

- `references/testing-recipes.md` - Complete testing patterns for forms, async, hooks, mocking, and accessibility
