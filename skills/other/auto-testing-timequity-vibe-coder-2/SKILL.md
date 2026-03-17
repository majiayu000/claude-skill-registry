---
name: auto-testing
description: |
  Automatically generate and run tests after each code change.
  Use when: any code is generated or modified in the pipeline.
  Triggers: internal use only.
---

# Auto Testing

Run tests automatically. User sees only pass/fail.

## When to Run

After every:
- Component generation
- Feature addition
- Code modification
- Refactoring

## Test Generation

For each code change, generate:

| Code Type | Test Type |
|-----------|-----------|
| Component | Render, interaction |
| API endpoint | Request/response |
| Utility function | Unit tests |
| Form | Validation, submission |
| Auth flow | Login, logout, protected |

## Test Patterns

### Components
```typescript
test('renders correctly', () => {
  render(<Component />);
  expect(screen.getByRole('button')).toBeInTheDocument();
});

test('handles click', async () => {
  const onClick = jest.fn();
  render(<Component onClick={onClick} />);
  await userEvent.click(screen.getByRole('button'));
  expect(onClick).toHaveBeenCalled();
});
```

### API
```typescript
test('returns data', async () => {
  const response = await fetch('/api/items');
  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data.items).toBeDefined();
});
```

## Reporting

| Status | User Sees |
|--------|-----------|
| All pass | ✅ (nothing else) |
| Some fail | "Fixing issues..." then ✅ |
| Can't fix | ❌ + simple explanation |

## Hidden Details

User never sees:
- Test file contents
- Number of tests
- Coverage percentage
- Individual test names

Only: ✅ works or ❌ problem
