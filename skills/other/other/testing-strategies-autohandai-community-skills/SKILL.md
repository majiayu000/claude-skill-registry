---
name: testing-strategies
description: Comprehensive testing strategies with Vitest, Jest, and Testing Library
license: MIT
compatibility: vitest 1+, jest 29+, testing-library/react 14+
allowed-tools: read_file write_file apply_patch search_with_context run_command
---

# Testing Strategies

## Testing Pyramid

```
        /\
       /  \      E2E Tests (few)
      /----\     Integration Tests (some)
     /      \    Unit Tests (many)
    /________\
```

1. **Unit Tests** - Test isolated functions/components
2. **Integration Tests** - Test modules working together
3. **E2E Tests** - Test full user flows

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'tests/'],
    },
  },
});
```

## Unit Testing Functions

```typescript
// utils/format.ts
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

// utils/format.test.ts
import { describe, it, expect } from 'vitest';
import { formatCurrency } from './format';

describe('formatCurrency', () => {
  it('formats USD by default', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  it('handles zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  it('supports other currencies', () => {
    expect(formatCurrency(1000, 'EUR')).toBe('€1,000.00');
  });

  it('handles negative amounts', () => {
    expect(formatCurrency(-50)).toBe('-$50.00');
  });
});
```

## React Component Testing

```typescript
// Button.tsx
interface ButtonProps {
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}

export function Button({ onClick, disabled, children }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders children', () => {
    render(<Button onClick={() => {}}>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick} disabled>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

## Testing Hooks

```typescript
// useCounter.ts
import { useState, useCallback } from 'react';

export function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initial), [initial]);
  return { count, increment, decrement, reset };
}

// useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    expect(result.current.count).toBe(5);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    act(() => {
      result.current.increment();
      result.current.reset();
    });
    expect(result.current.count).toBe(10);
  });
});
```

## Mocking

```typescript
// API mocking
import { vi } from 'vitest';

vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Test' }),
}));

// Module mocking
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}));

// Timer mocking
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

## Async Testing

```typescript
import { waitFor, screen } from '@testing-library/react';

it('loads and displays user', async () => {
  render(<UserProfile userId="123" />);

  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });

  expect(screen.getByText('John Doe')).toBeInTheDocument();
});

it('handles error state', async () => {
  vi.mocked(fetchUser).mockRejectedValueOnce(new Error('Not found'));

  render(<UserProfile userId="invalid" />);

  await waitFor(() => {
    expect(screen.getByRole('alert')).toHaveTextContent('Error loading user');
  });
});
```

## Integration Testing APIs

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../src/app';
import { db } from '../src/db';

describe('POST /api/users', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  afterAll(async () => {
    await db.destroy();
  });

  it('creates a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test User' })
      .expect(201);

    expect(response.body.data).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
  });

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## Test Organization

```
tests/
├── unit/           # Pure function tests
├── integration/    # API/DB tests
├── e2e/            # Full flow tests
├── fixtures/       # Test data
├── mocks/          # Mock implementations
└── setup.ts        # Global test setup
```

## Best Practices

1. **Follow AAA pattern** - Arrange, Act, Assert
2. **One assertion per test** when possible
3. **Test behavior, not implementation**
4. **Use descriptive test names** that explain the scenario
5. **Keep tests isolated** - no shared state
6. **Mock external dependencies** but not the code under test
7. **Aim for 80%+ coverage** but prioritize critical paths
