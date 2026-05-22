---
name: testing-library
description: Tests UI components with Testing Library including queries, user events, and async utilities. Use when testing React/Vue/Svelte components, writing accessible tests, or testing user interactions.
---

# Testing Library

Simple and complete testing utilities that encourage good testing practices.

## Quick Start

**Install (React):**
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**Install (Vue):**
```bash
npm install --save-dev @testing-library/vue
```

## Basic Test

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

test('renders button with text', () => {
  render(<Button>Click me</Button>);

  expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
});

test('calls onClick when clicked', async () => {
  const user = userEvent.setup();
  const handleClick = vi.fn();

  render(<Button onClick={handleClick}>Click me</Button>);

  await user.click(screen.getByRole('button'));

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

## Queries

### Query Priority (Accessibility First)

```tsx
// 1. Accessible to everyone
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText(/email/i);
screen.getByPlaceholderText(/search/i);
screen.getByText(/welcome/i);
screen.getByDisplayValue(/john/i);

// 2. Semantic queries
screen.getByAltText(/profile/i);
screen.getByTitle(/close/i);

// 3. Test IDs (last resort)
screen.getByTestId('submit-button');
```

### Query Types

```tsx
// getBy* - Throws if not found (for elements that should exist)
screen.getByRole('button');

// queryBy* - Returns null if not found (for asserting absence)
expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

// findBy* - Returns Promise, waits for element (for async)
await screen.findByText('Loaded!');

// getAllBy* - Returns array of all matching elements
screen.getAllByRole('listitem');

// queryAllBy* - Returns empty array if none found
expect(screen.queryAllByRole('alert')).toHaveLength(0);

// findAllBy* - Returns Promise of array
await screen.findAllByRole('option');
```

### Query by Role

```tsx
// Button
screen.getByRole('button', { name: /submit/i });

// Link
screen.getByRole('link', { name: /learn more/i });

// Textbox
screen.getByRole('textbox', { name: /email/i });

// Checkbox
screen.getByRole('checkbox', { name: /agree/i });

// Radio
screen.getByRole('radio', { name: /option 1/i });

// Combobox (select)
screen.getByRole('combobox', { name: /country/i });

// Heading
screen.getByRole('heading', { name: /welcome/i, level: 1 });

// List
screen.getByRole('list');
screen.getAllByRole('listitem');

// Navigation
screen.getByRole('navigation');

// Dialog
screen.getByRole('dialog');

// Alert
screen.getByRole('alert');

// Tab
screen.getByRole('tab', { name: /settings/i });
screen.getByRole('tabpanel');
```

### Query Options

```tsx
// Case insensitive regex (recommended)
screen.getByText(/hello world/i);

// Exact string
screen.getByText('Hello World', { exact: true });

// Substring
screen.getByText('Hello', { exact: false });

// Custom function
screen.getByText((content, element) => {
  return element?.tagName === 'SPAN' && content.includes('Hello');
});

// Hidden elements
screen.getByRole('button', { hidden: true });
```

## User Events

### Setup

```tsx
import userEvent from '@testing-library/user-event';

test('user interactions', async () => {
  const user = userEvent.setup();

  render(<MyComponent />);

  // All interactions are async
  await user.click(screen.getByRole('button'));
});
```

### Click Events

```tsx
const user = userEvent.setup();

// Single click
await user.click(element);

// Double click
await user.dblClick(element);

// Right click
await user.pointer({ keys: '[MouseRight]', target: element });

// Hover
await user.hover(element);
await user.unhover(element);
```

### Keyboard Events

```tsx
const user = userEvent.setup();

// Type text
await user.type(input, 'Hello World');

// Type with special keys
await user.type(input, 'Hello{Enter}');
await user.type(input, '{Shift>}hello{/Shift}'); // HELLO

// Clear and type
await user.clear(input);
await user.type(input, 'New value');

// Tab navigation
await user.tab();

// Keyboard shortcuts
await user.keyboard('{Control>}a{/Control}'); // Select all
await user.keyboard('{Control>}c{/Control}'); // Copy
```

### Form Interactions

```tsx
const user = userEvent.setup();

// Select option
await user.selectOptions(select, 'option-value');
await user.selectOptions(select, ['opt1', 'opt2']); // Multiple

// Checkbox
await user.click(checkbox);

// File upload
const file = new File(['hello'], 'hello.png', { type: 'image/png' });
await user.upload(fileInput, file);

// Paste
await user.paste('pasted text');
```

## Async Utilities

### waitFor

```tsx
import { waitFor } from '@testing-library/react';

test('shows success after submit', async () => {
  const user = userEvent.setup();

  render(<Form />);

  await user.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });
});

// With options
await waitFor(
  () => {
    expect(screen.getByText(/loaded/i)).toBeInTheDocument();
  },
  { timeout: 3000, interval: 100 }
);
```

### findBy Queries

```tsx
// findBy = getBy + waitFor
const element = await screen.findByText(/loaded/i);

// With timeout
const element = await screen.findByRole('dialog', {}, { timeout: 5000 });
```

### waitForElementToBeRemoved

```tsx
import { waitForElementToBeRemoved } from '@testing-library/react';

test('loading disappears', async () => {
  render(<AsyncComponent />);

  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

  expect(screen.getByText(/content/i)).toBeInTheDocument();
});
```

## Component Testing

### React

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Counter', () => {
  test('increments counter on click', async () => {
    const user = userEvent.setup();

    render(<Counter initialCount={0} />);

    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### With Providers

```tsx
function renderWithProviders(
  ui: React.ReactElement,
  { initialState, ...options }: RenderOptions = {}
) {
  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>{children}</ThemeProvider>
      </QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...options });
}

test('renders with providers', () => {
  renderWithProviders(<MyComponent />);
  // ...
});
```

### Form Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  test('submits form with user data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  test('shows validation errors', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument();
  });
});
```

## jest-dom Matchers

```tsx
import '@testing-library/jest-dom';

// Visibility
expect(element).toBeVisible();
expect(element).not.toBeVisible();

// Presence
expect(element).toBeInTheDocument();
expect(element).not.toBeInTheDocument();

// Content
expect(element).toHaveTextContent(/hello/i);
expect(element).toContainHTML('<span>Hello</span>');

// Form state
expect(input).toHaveValue('test');
expect(input).toBeDisabled();
expect(input).toBeEnabled();
expect(input).toBeRequired();
expect(input).toBeValid();
expect(input).toBeInvalid();
expect(checkbox).toBeChecked();

// Attributes
expect(element).toHaveAttribute('href', '/about');
expect(element).toHaveClass('active');
expect(element).toHaveStyle({ display: 'flex' });

// Focus
expect(input).toHaveFocus();

// Accessibility
expect(element).toHaveAccessibleName('Submit form');
expect(element).toHaveAccessibleDescription('Click to submit');
```

## Mocking

### Mock Functions

```tsx
test('calls callback on click', async () => {
  const user = userEvent.setup();
  const handleClick = vi.fn();

  render(<Button onClick={handleClick}>Click</Button>);

  await user.click(screen.getByRole('button'));

  expect(handleClick).toHaveBeenCalledTimes(1);
  expect(handleClick).toHaveBeenCalledWith(expect.any(Object));
});
```

### Mock API (with MSW)

```tsx
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/user', () => {
    return HttpResponse.json({ name: 'John' });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('loads and displays user', async () => {
  render(<UserProfile />);

  expect(await screen.findByText(/john/i)).toBeInTheDocument();
});
```

## Debugging

```tsx
// Print DOM
screen.debug();

// Print specific element
screen.debug(screen.getByRole('button'));

// Log testing playground URL
screen.logTestingPlaygroundURL();

// Get accessible roles
import { getRoles } from '@testing-library/dom';
console.log(getRoles(container));
```

## Best Practices

1. **Query by role** - Most accessible selector
2. **Use userEvent** - Not fireEvent
3. **Avoid implementation details** - Test behavior
4. **Use findBy for async** - Not getBy + waitFor
5. **Test from user perspective** - What they see/do

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using getByTestId first | Try getByRole, getByLabelText |
| Using fireEvent | Use userEvent.setup() |
| Testing internal state | Test visible behavior |
| Wrapping everything in act() | Let queries handle it |
| queryBy for existing elements | Use getBy (throws helpful error) |

## Reference Files

- [references/queries.md](references/queries.md) - All query types
- [references/matchers.md](references/matchers.md) - jest-dom matchers
- [references/async.md](references/async.md) - Async patterns
