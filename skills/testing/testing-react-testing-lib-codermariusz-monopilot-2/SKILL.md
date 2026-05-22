---
name: testing-react-testing-lib
description: Apply when testing React components: rendering, user interactions, and accessibility-focused testing.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://testing-library.com/docs/react-testing-library/intro
  - https://testing-library.com/docs/queries/about
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [testing, react, testing-library, frontend]
---

## When to Use

Apply when testing React components: rendering, user interactions, and accessibility-focused testing.

## Patterns

### Pattern 1: Basic Render and Query
```typescript
// Source: https://testing-library.com/docs/react-testing-library/intro
import { render, screen } from '@testing-library/react';

test('renders greeting', () => {
  render(<Greeting name="World" />);

  // Query by role (preferred - accessible)
  expect(screen.getByRole('heading')).toHaveTextContent('Hello, World');

  // Query by text
  expect(screen.getByText(/hello/i)).toBeInTheDocument();
});
```

### Pattern 2: Query Priority
```typescript
// Source: https://testing-library.com/docs/queries/about#priority
// Priority (most accessible first):
// 1. getByRole - buttons, headings, links
screen.getByRole('button', { name: /submit/i });
screen.getByRole('heading', { level: 1 });

// 2. getByLabelText - form inputs
screen.getByLabelText(/email/i);

// 3. getByPlaceholderText - when no label
screen.getByPlaceholderText('Enter email');

// 4. getByText - non-interactive elements
screen.getByText(/welcome/i);

// 5. getByTestId - last resort
screen.getByTestId('custom-element');
```

### Pattern 3: User Interactions
```typescript
// Source: https://testing-library.com/docs/user-event/intro
import userEvent from '@testing-library/user-event';

test('submits form', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();

  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'secret123');
  await user.click(screen.getByRole('button', { name: /sign in/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'secret123',
  });
});
```

### Pattern 4: Async Waiting
```typescript
// Source: https://testing-library.com/docs/dom-testing-library/api-async
import { waitFor, waitForElementToBeRemoved } from '@testing-library/react';

test('loads data', async () => {
  render(<UserList />);

  // Wait for loading to finish
  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

  // Element appears after async operation
  expect(await screen.findByText('John Doe')).toBeInTheDocument();

  // Custom wait condition
  await waitFor(() => {
    expect(screen.getByRole('list').children).toHaveLength(3);
  });
});
```

### Pattern 5: Testing with Context/Providers
```typescript
// Source: https://testing-library.com/docs/react-testing-library/setup
function renderWithProviders(ui: React.ReactElement) {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <ThemeProvider>
        {ui}
      </ThemeProvider>
    </QueryClientProvider>
  );
}

test('themed component', () => {
  renderWithProviders(<ThemedButton />);
  expect(screen.getByRole('button')).toHaveClass('dark-theme');
});
```

### Pattern 6: Query Variants
```typescript
// Source: https://testing-library.com/docs/queries/about
// getBy - throws if not found (sync)
screen.getByRole('button'); // Error if missing

// queryBy - returns null if not found (sync)
expect(screen.queryByRole('button')).toBeNull(); // Assert absence

// findBy - waits for element (async)
await screen.findByText(/loaded/i); // Waits up to 1000ms
```

## Anti-Patterns

- **Testing implementation** - Test what user sees/does
- **Using container.querySelector** - Use accessible queries
- **Not awaiting user events** - userEvent is async
- **getBy for absence checks** - Use queryBy

## Verification Checklist

- [ ] Queries use accessible selectors (role, label)
- [ ] User interactions use userEvent (not fireEvent)
- [ ] Async operations properly awaited
- [ ] No implementation details tested
- [ ] Custom render includes needed providers
