---
name: React Testing
description: Testing strategies with RTL and Jest/Vitest.
metadata:
  labels: [react, testing, jest, vitest]
  triggers:
    files: ['**/*.test.tsx', '**/*.spec.tsx']
    keywords: [render, screen, userEvent, expect]
---

# React Testing

## **Priority: P2 (MAINTENANCE)**

Reliable tests focusing on user behavior.

## Implementation Guidelines

- **Tooling**: React Testing Library + Vitest.
- **Philosophy**: Test behavior, not implementation (State/Internal vars).
- **Queries**: `getByRole` > `getByText` > `getByTestId`.
- **Events**: Use `userEvent` (async) over `fireEvent`.
- **Async**: `await screen.findBy*` for async updates.
- **Mocks**: MSW for network. Mock heavy 3rd-party libs.
- **Accessibility**: Testing Lib implicitly tests a11y roles.

## Anti-Patterns

- **No Shallow Rendering**: Render full tree.
- **No Testing Implementation Details**: Don't check `component.state`.
- **No Wait**: Use `findBy`, avoid `waitFor` if possible.

## Code

```tsx
test('submits form', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(screen.getByLabelText(/email/i), 'test@test.com');
  await user.click(screen.getByRole('button', { name: /login/i }));

  expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
});
```
