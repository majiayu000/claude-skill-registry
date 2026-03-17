---
name: testing-library
description: |
  Test React components with Testing Library patterns. Covers queries (getBy/findBy/queryBy), user-event interactions, async testing (findBy vs waitFor), accessibility testing, and MSW integration for API mocking.

  Use when: testing React components, simulating user interactions, testing forms, mocking API calls with MSW, or writing accessible tests. Keywords: testing-library, react testing library, getByRole, user-event, waitFor, MSW, screen.
license: MIT
---

# React Testing Library

**Status**: Production Ready
**Last Updated**: 2026-02-06
**Version**: 16.x
**User Event**: 14.x

---

## Quick Start

```bash
# Install with Vitest
pnpm add -D @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom

# Or with Jest
pnpm add -D @testing-library/react @testing-library/user-event @testing-library/jest-dom
```

### Setup File (src/test/setup.ts)

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

### Vitest Config

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

---

## Query Priority (Accessibility First)

Use queries in this order for accessible, resilient tests:

| Priority | Query | Use For |
|----------|-------|---------|
| 1 | `getByRole` | Buttons, links, headings, inputs |
| 2 | `getByLabelText` | Form inputs with labels |
| 3 | `getByPlaceholderText` | Inputs without visible labels |
| 4 | `getByText` | Non-interactive text content |
| 5 | `getByTestId` | Last resort only |

### Examples

```typescript
import { render, screen } from '@testing-library/react';

// ✅ GOOD - semantic role queries
screen.getByRole('button', { name: /submit/i });
screen.getByRole('heading', { level: 1 });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('link', { name: /learn more/i });

// ✅ GOOD - label-based queries for forms
screen.getByLabelText(/email address/i);

// ⚠️ OK - when no better option
screen.getByText(/welcome to our app/i);

// ❌ AVOID - not accessible, brittle
screen.getByTestId('submit-button');
```

---

## Query Variants

| Variant | Returns | Throws | Use For |
|---------|---------|--------|---------|
| `getBy` | Element | Yes | Element exists now |
| `queryBy` | Element or null | No | Element might not exist |
| `findBy` | Promise<Element> | Yes | Async, appears later |
| `getAllBy` | Element[] | Yes | Multiple elements |
| `queryAllBy` | Element[] | No | Multiple or none |
| `findAllBy` | Promise<Element[]> | Yes | Multiple, async |

### When to Use Each

```typescript
// Element exists immediately
const button = screen.getByRole('button');

// Check element doesn't exist
expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

// Wait for async element to appear
const modal = await screen.findByRole('dialog');

// Multiple elements
const items = screen.getAllByRole('listitem');
```

---

## User Event (Realistic Interactions)

**Always use `userEvent` over `fireEvent`** - it simulates real user behavior.

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Form', () => {
  it('submits form data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    // Type in inputs
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'secret123');

    // Click submit
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'secret123',
    });
  });
});
```

### Common User Events

```typescript
const user = userEvent.setup();

// Clicking
await user.click(element);
await user.dblClick(element);
await user.tripleClick(element); // Select all text

// Typing
await user.type(input, 'hello world');
await user.clear(input);
await user.type(input, '{Enter}'); // Special keys

// Keyboard
await user.keyboard('{Shift>}A{/Shift}'); // Shift+A
await user.tab(); // Tab navigation

// Selection
await user.selectOptions(select, ['option1', 'option2']);

// Hover
await user.hover(element);
await user.unhover(element);

// Clipboard
await user.copy();
await user.paste();
```

---

## Async Testing

### findBy - Wait for Element

```typescript
it('shows loading then content', async () => {
  render(<AsyncComponent />);

  // Shows loading initially
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for content to appear (auto-retries)
  const content = await screen.findByText(/data loaded/i);
  expect(content).toBeInTheDocument();
});
```

### waitFor - Wait for Condition

```typescript
import { waitFor } from '@testing-library/react';

it('updates count after click', async () => {
  const user = userEvent.setup();
  render(<Counter />);

  await user.click(screen.getByRole('button', { name: /increment/i }));

  // Wait for state update
  await waitFor(() => {
    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });
});
```

### waitForElementToBeRemoved

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

it('hides modal after close', async () => {
  const user = userEvent.setup();
  render(<ModalComponent />);

  await user.click(screen.getByRole('button', { name: /close/i }));

  // Wait for modal to disappear
  await waitForElementToBeRemoved(() => screen.queryByRole('dialog'));
});
```

---

## MSW Integration (API Mocking)

Mock API calls at the network level with Mock Service Worker.

```bash
pnpm add -D msw
```

### Setup (src/test/mocks/handlers.ts)

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({
      id: 1,
      name: 'Test User',
      email: 'test@example.com',
    });
  }),

  http.post('/api/login', async ({ request }) => {
    const body = await request.json();
    if (body.password === 'correct') {
      return HttpResponse.json({ token: 'abc123' });
    }
    return HttpResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    );
  }),
];
```

### Setup (src/test/mocks/server.ts)

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Test Setup

```typescript
// src/test/setup.ts
import { server } from './mocks/server';
import { beforeAll, afterEach, afterAll } from 'vitest';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Using in Tests

```typescript
import { server } from '../test/mocks/server';
import { http, HttpResponse } from 'msw';

it('handles API error', async () => {
  // Override handler for this test
  server.use(
    http.get('/api/user', () => {
      return HttpResponse.json(
        { error: 'Server error' },
        { status: 500 }
      );
    })
  );

  render(<UserProfile />);

  await screen.findByText(/error loading user/i);
});
```

---

## Accessibility Testing

### Check for A11y Violations

```bash
pnpm add -D @axe-core/react
```

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Role-Based Queries Are A11y Tests

Using `getByRole` implicitly tests accessibility:

```typescript
// This passes only if button is properly accessible
screen.getByRole('button', { name: /submit/i });

// Fails if:
// - Element isn't a button or role="button"
// - Accessible name doesn't match
// - Element is hidden from accessibility tree
```

---

## Testing Patterns

### Forms

```typescript
it('validates required fields', async () => {
  const user = userEvent.setup();
  render(<ContactForm />);

  // Submit without filling required fields
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // Check for validation errors
  expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  expect(screen.getByText(/message is required/i)).toBeInTheDocument();
});
```

### Modals/Dialogs

```typescript
it('opens and closes modal', async () => {
  const user = userEvent.setup();
  render(<ModalTrigger />);

  // Modal not visible initially
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

  // Open modal
  await user.click(screen.getByRole('button', { name: /open/i }));
  expect(screen.getByRole('dialog')).toBeInTheDocument();

  // Close modal
  await user.click(screen.getByRole('button', { name: /close/i }));
  await waitForElementToBeRemoved(() => screen.queryByRole('dialog'));
});
```

### Lists

```typescript
it('renders list items', () => {
  render(<TodoList items={['Buy milk', 'Walk dog']} />);

  const items = screen.getAllByRole('listitem');
  expect(items).toHaveLength(2);
  expect(items[0]).toHaveTextContent('Buy milk');
});
```

---

## Common Matchers (jest-dom)

```typescript
// Presence
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeEmptyDOMElement();

// State
expect(button).toBeEnabled();
expect(button).toBeDisabled();
expect(checkbox).toBeChecked();
expect(input).toBeRequired();

// Content
expect(element).toHaveTextContent(/hello/i);
expect(element).toHaveValue('test');
expect(element).toHaveAttribute('href', '/about');

// Styles
expect(element).toHaveClass('active');
expect(element).toHaveStyle({ color: 'red' });

// Focus
expect(input).toHaveFocus();
```

---

## Debugging

### screen.debug()

```typescript
it('debugs rendering', () => {
  render(<MyComponent />);

  // Print entire DOM
  screen.debug();

  // Print specific element
  screen.debug(screen.getByRole('button'));
});
```

### logRoles

```typescript
import { logRoles } from '@testing-library/react';

it('shows available roles', () => {
  const { container } = render(<MyComponent />);
  logRoles(container);
});
```

---

## Common Mistakes

### Using getBy for Async

```typescript
// ❌ WRONG - fails if element appears async
const modal = screen.getByRole('dialog');

// ✅ CORRECT - waits for element
const modal = await screen.findByRole('dialog');
```

### Not Awaiting User Events

```typescript
// ❌ WRONG - race condition
user.click(button);
expect(result).toBeInTheDocument();

// ✅ CORRECT - await the interaction
await user.click(button);
expect(result).toBeInTheDocument();
```

### Using container.querySelector

```typescript
// ❌ WRONG - not accessible, brittle
const button = container.querySelector('.submit-btn');

// ✅ CORRECT - accessible query
const button = screen.getByRole('button', { name: /submit/i });
```

---

## See Also

- `vitest` skill - Test runner configuration
- `testing-patterns` skill - General testing patterns
- Official docs: https://testing-library.com/docs/react-testing-library/intro
