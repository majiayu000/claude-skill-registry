---
name: react-testing
description: React testing with Vitest, React Testing Library, and MSW. Focuses on user-centric testing, component isolation, and API mocking. Use when writing tests for React components, hooks, or debugging test failures in frontend code.
---

# React Testing

Testing patterns for React 19 + TypeScript projects with Vitest.

## When to Use

- Writing component tests
- Testing custom hooks
- Mocking API calls with MSW
- Debugging test failures
- Improving frontend test coverage

## MCP Workflow

```typescript
# 1. Find existing test patterns
serena.search_for_pattern("describe|it|test", relative_path="src/", paths_include_glob="**/*.test.{ts,tsx}")

# 2. Check test utilities
serena.get_symbols_overview(relative_path="src/test/")

# 3. Find component test patterns
jetbrains.search_in_files_by_text("render(", fileMask="*.test.tsx")

# 4. React Testing Library docs
context7.get-library-docs("/testing-library/react-testing-library", "queries")
```

## Testing Principles

1. **Test user behavior**, not implementation
2. **Query by accessibility**: `getByRole` > `getByTestId`
3. **Avoid testing internal state** directly
4. **Mock at boundaries**: API calls, not internal functions

## Query Priority

| Priority | Query | Use When |
|----------|-------|----------|
| 1 | `getByRole` | Interactive elements (button, input) |
| 2 | `getByLabelText` | Form fields |
| 3 | `getByPlaceholderText` | Input with placeholder |
| 4 | `getByText` | Non-interactive text |
| 5 | `getByTestId` | Last resort |

## Component Test Patterns

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  it('should display user name', () => {
    render(<UserCard user={{ id: '1', name: 'Alice' }} />);

    expect(screen.getByRole('heading')).toHaveTextContent('Alice');
  });

  it('should call onSelect when clicked', async () => {
    const user = userEvent.setup();
    const handleSelect = vi.fn();

    render(
      <UserCard
        user={{ id: '1', name: 'Alice' }}
        onSelect={handleSelect}
      />
    );

    await user.click(screen.getByRole('button', { name: /select/i }));

    expect(handleSelect).toHaveBeenCalledWith('1');
  });
});
```

### Async Component Test

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserList } from './UserList';

describe('UserList', () => {
  it('should show loading then data', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <UserList />
      </QueryClientProvider>
    );

    // Loading state
    expect(screen.getByRole('progressbar')).toBeInTheDocument();

    // Wait for data
    await waitFor(() => {
      expect(screen.getByRole('list')).toBeInTheDocument();
    });

    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });
});
```

## Custom Hook Testing

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should debounce value changes', async () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'initial' } }
    );

    expect(result.current).toBe('initial');

    rerender({ value: 'updated' });
    expect(result.current).toBe('initial'); // Not updated yet

    vi.advanceTimersByTime(500);
    await waitFor(() => {
      expect(result.current).toBe('updated');
    });
  });
});
```

## MSW API Mocking

### Setup

```typescript
// src/test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ]);
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  }),

  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'User' });
  }),
];
```

### Test Setup

```typescript
// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { handlers } from './mocks/handlers';

export const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Override Handler in Test

```typescript
import { server } from '@/test/setup';
import { http, HttpResponse } from 'msw';

it('should handle API error', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Server error' }, { status: 500 });
    })
  );

  render(<UserList />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

## Testing Patterns for TanStack Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Don't retry in tests
        gcTime: Infinity,    // Keep cache during test
      },
    },
  });
}

function wrapper({ children }: { children: React.ReactNode }) {
  const client = createTestQueryClient();
  return (
    <QueryClientProvider client={client}>
      {children}
    </QueryClientProvider>
  );
}

// Usage
render(<UserList />, { wrapper });
```

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `getByTestId` for buttons | Tests implementation | Use `getByRole('button')` |
| Testing state directly | Brittle | Test rendered output |
| `fireEvent` for clicks | Doesn't match user | Use `userEvent` |
| Mocking child components | Over-isolation | Render real children |
| `await waitFor(() => {})` empty | Flaky | Wait for specific element |
| Testing third-party libs | Wasted effort | Trust libraries work |

## TDD Workflow for React

### 1. RED: Write Failing Test

```typescript
it('should show error when name is empty', async () => {
  const user = userEvent.setup();
  render(<CreateUserForm />);

  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(screen.getByRole('alert')).toHaveTextContent('Name is required');
});
```

### 2. GREEN: Implement

```typescript
export function CreateUserForm() {
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    if (!form.name.value) {
      setError('Name is required');
      return;
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" />
      {error && <div role="alert">{error}</div>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 3. REFACTOR: Improve accessibility, extract validation

## Quality Checklist

- [ ] Tests query by role/label, not testId
- [ ] `userEvent` used instead of `fireEvent`
- [ ] Async operations use `waitFor`
- [ ] MSW for API mocking (not `vi.mock`)
- [ ] Loading/error states tested
- [ ] No testing of implementation details
- [ ] Test names describe user behavior
