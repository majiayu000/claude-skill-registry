---
name: typescript-component-testing
version: "1.0"
description: >
  Jest, Vitest, and React Testing Library patterns for component testing.
  PROACTIVELY activate for: (1) Writing React component tests, (2) Using Testing Library queries,
  (3) Testing user interactions, (4) Async component testing, (5) Accessibility-focused testing.
  Triggers: "jest", "vitest", "testing-library", "react test", "component test", "render", "screen", "userEvent"
core-integration:
  techniques:
    primary: ["exhaustive_edge_case_enumeration"]
    secondary: ["completeness_verification"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# TypeScript Component Testing Skill

## Metadata (Tier 1)

**Keywords**: jest, vitest, testing-library, react, component test, render

**File Patterns**: *.test.tsx, *.spec.ts, *.test.js

**Modes**: testing_frontend

---

## Instructions (Tier 2)

### React Testing Library Philosophy

**Core Principle**: Test from user's perspective, not implementation

### Query Priority
1. `getByRole` (accessible roles)
2. `getByLabelText` (form elements)
3. `getByPlaceholderText`
4. `getByText`
5. `getByTestId` (last resort)

### Basic Test Pattern

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits login form', async () => {
  const handleSubmit = jest.fn();
  render(<LoginForm onSubmit={handleSubmit} />);

  await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /log in/i }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123'
  });
});
```

### Async Testing

```typescript
test('loads and displays data', async () => {
  render(<UserProfile userId="123" />);

  // Wait for data to load
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});

// Or with waitFor
await waitFor(() => {
  expect(screen.getByText('John Doe')).toBeInTheDocument();
});
```

### User Interactions (userEvent)

```typescript
// Preferred: userEvent (realistic)
await userEvent.click(button);
await userEvent.type(input, 'text');
await userEvent.selectOptions(select, ['option1']);

// Avoid: fireEvent (low-level)
fireEvent.click(button);
```

### Anti-Patterns

- Testing implementation details (state, methods)
- Using container.querySelector
- Not waiting for async updates
- Manually wrapping in act()
