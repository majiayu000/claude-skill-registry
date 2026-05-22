---
name: vitest-testing-patterns
description: Write tests using Vitest and React Testing Library. Use when creating unit tests, component tests, integration tests, or mocking dependencies. Activates for test file creation, mock patterns, coverage, and testing best practices.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Code Quality & Testing
tags:
  - testing
  - code
  - automation
  - jest
  - react
---

# Vitest Testing Patterns

This skill helps you write effective tests using Vitest and React Testing Library following project conventions.

## When to Use

✅ **USE this skill for:**
- Writing unit tests for utilities and functions
- Creating component tests with React Testing Library
- Setting up mocks for API calls, databases, or external services
- Integration testing patterns
- Understanding test coverage and CI setup

❌ **DO NOT use for:**
- Jest-specific patterns → similar but check Jest docs for differences
- End-to-end testing → use Playwright or Cypress skills
- Performance testing → use dedicated performance tools
- API contract testing → use OpenAPI/Pact patterns

## Test Infrastructure

**Configuration**: `vitest.config.ts`
- Environment: jsdom
- Setup file: `src/test/setup.ts`
- Coverage: v8 provider

**Commands**:
```bash
npm test              # Watch mode
npm run test:run      # Single run
npm run test:coverage # With coverage
```

## File Organization

```
src/
├── app/api/__tests__/        # API route tests
├── components/__tests__/     # Component tests
├── lib/__tests__/            # Library/utility tests
└── lib/{feature}/__tests__/  # Feature-specific tests
```

Name tests as `{name}.test.ts` or `{name}.test.tsx`.

## Core Testing Patterns

### 1. API Route Tests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { GET, POST } from '../route';
import { NextRequest } from 'next/server';

// Mock dependencies
vi.mock('@/lib/auth', () => ({
  getSession: vi.fn(),
}));

vi.mock('@/db', () => ({
  db: {
    select: vi.fn().mockReturnThis(),
    from: vi.fn().mockReturnThis(),
    where: vi.fn().mockResolvedValue([]),
  },
}));

describe('GET /api/feature', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns 401 when not authenticated', async () => {
    vi.mocked(getSession).mockResolvedValue(null);

    const request = new NextRequest('http://localhost/api/feature');
    const response = await GET(request);

    expect(response.status).toBe(401);
  });

  it('returns data when authenticated', async () => {
    vi.mocked(getSession).mockResolvedValue({ userId: 'user-123' });
    vi.mocked(db.select).mockReturnValue({
      from: vi.fn().mockReturnValue({
        where: vi.fn().mockResolvedValue([{ id: '1', name: 'Test' }]),
      }),
    });

    const request = new NextRequest('http://localhost/api/feature');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveLength(1);
  });
});
```

### 2. Component Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FeatureComponent } from '../FeatureComponent';

// Mock hooks
vi.mock('@/hooks/useAuth', () => ({
  useAuth: vi.fn().mockReturnValue({
    user: { id: 'user-123', name: 'Test User' },
    isLoading: false,
  }),
}));

describe('FeatureComponent', () => {
  it('renders loading state', () => {
    vi.mocked(useAuth).mockReturnValueOnce({
      user: null,
      isLoading: true,
    });

    render(<FeatureComponent />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<FeatureComponent onSubmit={onSubmit} />);

    await user.type(screen.getByRole('textbox'), 'Test input');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    expect(onSubmit).toHaveBeenCalledWith('Test input');
  });

  it('displays error state', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

    render(<FeatureComponent />);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/error/i);
    });
  });
});
```

### 3. Library/Utility Tests

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { processData, formatDate } from '../utils';

describe('processData', () => {
  it('transforms input correctly', () => {
    const input = { raw: 'data' };
    const result = processData(input);

    expect(result).toEqual({
      processed: true,
      data: 'DATA',
    });
  });

  it('throws on invalid input', () => {
    expect(() => processData(null)).toThrow('Invalid input');
  });
});

describe('formatDate', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2025-01-15T10:00:00Z'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('formats relative dates', () => {
    const yesterday = new Date('2025-01-14T10:00:00Z');
    expect(formatDate(yesterday)).toBe('yesterday');
  });
});
```

## Mocking Patterns

### Module Mocking

```typescript
// Mock entire module
vi.mock('@/lib/auth', () => ({
  getSession: vi.fn(),
  requireAuth: vi.fn(),
}));

// Mock with partial implementation
vi.mock('date-fns', async () => {
  const actual = await vi.importActual('date-fns');
  return {
    ...actual,
    format: vi.fn(() => '2025-01-15'),
  };
});

// Mock default export (like Anthropic SDK)
vi.mock('@anthropic-ai/sdk', () => ({
  default: class MockAnthropic {
    messages = {
      create: vi.fn().mockResolvedValue({
        content: [{ type: 'text', text: 'Mock response' }],
        usage: { input_tokens: 10, output_tokens: 20 },
      }),
    };
  },
}));
```

### Function Mocking

```typescript
// Create mock function
const mockFn = vi.fn();

// Set return values
mockFn.mockReturnValue('sync value');
mockFn.mockResolvedValue('async value');
mockFn.mockRejectedValue(new Error('Failed'));

// One-time behavior
mockFn.mockReturnValueOnce('first call only');

// Custom implementation
mockFn.mockImplementation((arg) => arg.toUpperCase());

// Verify calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('expected', 'args');
```

### Chained Mock Pattern (Drizzle ORM)

```typescript
vi.mock('@/db', () => ({
  db: {
    select: vi.fn().mockReturnValue({
      from: vi.fn().mockReturnValue({
        where: vi.fn().mockReturnValue({
          orderBy: vi.fn().mockReturnValue({
            limit: vi.fn().mockResolvedValue([{ id: '1' }]),
          }),
        }),
      }),
    }),
    insert: vi.fn().mockReturnValue({
      values: vi.fn().mockReturnValue({
        returning: vi.fn().mockResolvedValue([{ id: 'new-1' }]),
      }),
    }),
  },
}));
```

### Timer Mocking

```typescript
describe('debounced function', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('debounces calls', async () => {
    const callback = vi.fn();
    const debounced = debounce(callback, 300);

    debounced();
    debounced();
    debounced();

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(300);

    expect(callback).toHaveBeenCalledTimes(1);
  });
});
```

## Query Priorities

Use queries in this order (most to least preferred):

1. **getByRole** - Accessible queries (buttons, links, headings)
2. **getByLabelText** - Form fields with labels
3. **getByPlaceholderText** - Inputs with placeholders
4. **getByText** - Non-interactive elements
5. **getByTestId** - Last resort (data-testid)

```typescript
// Preferred
screen.getByRole('button', { name: /submit/i });
screen.getByRole('heading', { level: 1 });
screen.getByLabelText(/email/i);

// Avoid unless necessary
screen.getByTestId('submit-button');
```

## Async Patterns

```typescript
// Wait for element to appear
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// Find (built-in waitFor)
const element = await screen.findByText('Loaded');

// Wait for element to disappear
await waitFor(() => {
  expect(screen.queryByText('Loading')).not.toBeInTheDocument();
});
```

## Test Cleanup

```typescript
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();            // React cleanup (automatic with setup.ts)
  vi.clearAllMocks();   // Reset mock call counts
  vi.resetAllMocks();   // Reset mocks to initial state
  vi.restoreAllMocks(); // Restore original implementations
});
```

## Accessibility Testing

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Common Matchers

```typescript
// jest-dom matchers (from setup.ts)
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeDisabled();
expect(element).toHaveTextContent('text');
expect(element).toHaveAttribute('href', '/path');
expect(element).toHaveClass('active');
expect(input).toHaveValue('input value');
```

## References

- [Vitest Mocking Guide](https://vitest.dev/guide/mocking)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro)
- [Testing Library Queries](https://testing-library.com/docs/queries/about)
