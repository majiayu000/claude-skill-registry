---
name: testing-infrastructure
description: Complete testing infrastructure and patterns for the monorepo. Use this skill when writing tests, setting up test configuration, troubleshooting test failures, or working with the CI pipeline. Covers vitest configuration, Storybook addon-vitest integration, React Testing Library patterns, mock data setup, and the test-suite-runner agent for comprehensive testing.
---

# Testing Infrastructure

## Test Runners

### Vitest

Primary test runner for:
- Unit tests (`.test.ts`, `.test.tsx`)
- Storybook story tests (via addon-vitest)

### Running Tests

```bash
# Unit tests only
pnpm test

# Specific package
pnpm test --filter @lsst-sqre/squared

# Storybook tests
pnpm test-storybook
pnpm test-storybook:watch
pnpm test-storybook --filter @lsst-sqre/squared

# Comprehensive CI pipeline
pnpm run localci  # Or use test-suite-runner agent
```

## Vitest Configuration

### Squared Package

Two test projects in `vitest.config.ts`:

**Unit tests:**
- Files: `src/**/*.test.{ts,tsx}`
- Environment: jsdom
- Setup: `src/test-setup.ts`
- CSS Modules: non-scoped strategy

**Storybook tests:**
- Browser: Playwright (chromium)
- Environment: browser + jsdom
- Setup: `.storybook/vitest.setup.ts`
- Plugin: `@storybook/addon-vitest`

## Writing Unit Tests

### Basic Pattern

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const handleClick = vi.fn();
    render(<MyComponent onClick={handleClick} />);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### React Testing Library

**Query priority:**
1. `getByRole` - Most accessible
2. `getByLabelText` - For forms
3. `getByPlaceholderText` - For inputs
4. `getByText` - For content
5. `getByTestId` - Last resort

```typescript
// Good - semantic queries
screen.getByRole('button', { name: 'Submit' });
screen.getByLabelText('Email address');

// Avoid - implementation details
container.querySelector('.button');
```

### User Interactions

```typescript
import userEvent from '@testing-library/user-event';

it('handles form submission', async () => {
  const user = userEvent.setup();
  render(<MyForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText('Email'), 'test@example.com');
  await user.click(screen.getByRole('button', { name: 'Submit' }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
  });
});
```

## Storybook Tests

### In Stories

```typescript
import { expect, within, userEvent } from '@storybook/test';

export const WithInteraction: Story = {
  tags: ['test'],
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Assert initial state
    expect(canvas.getByText('Click me')).toBeInTheDocument();

    // Interact
    await userEvent.click(canvas.getByRole('button'));

    // Assert result
    expect(canvas.getByText('Clicked!')).toBeInTheDocument();
  },
};
```

### Running Story Tests

```bash
# Run all story tests
pnpm test-storybook --filter @lsst-sqre/squared

# Watch mode
pnpm test-storybook:watch --filter @lsst-sqre/squared

# Specific story
pnpm test-storybook --filter @lsst-sqre/squared -- --grep "MyComponent"
```

## Mocking

### Mock Functions

```typescript
import { vi } from 'vitest';

const mockFn = vi.fn();
const mockFnWithReturn = vi.fn(() => 'result');

expect(mockFn).toHaveBeenCalledWith('arg');
expect(mockFn).toHaveBeenCalledTimes(2);
```

### Mock Modules

```typescript
vi.mock('../api/client', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mock' })),
}));
```

### Mock SWR

```typescript
import useSWR from 'swr';

vi.mock('swr');

it('renders with data', () => {
  vi.mocked(useSWR).mockReturnValue({
    data: { name: 'Test' },
    error: undefined,
    isLoading: false,
    isValidating: false,
    mutate: vi.fn(),
  });

  render(<MyComponent />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

## Mock Data

### Mock Data Patterns

```typescript
// src/lib/mocks/userData.ts
export const mockUserData = {
  username: 'testuser',
  email: 'test@example.com',
  groups: ['admin'],
};

export const mockUserDataLoading = {
  data: undefined,
  error: undefined,
  isLoading: true,
};

export const mockUserDataError = {
  data: undefined,
  error: new Error('Failed to fetch'),
  isLoading: false,
};
```

### MSW (Mock Service Worker)

For API mocking in Storybook:

```typescript
// .storybook/preview.tsx
import { initialize, mswLoader } from 'msw-storybook-addon';
import { handlers } from '../src/mocks/handlers';

initialize({ onUnhandledRequest: 'bypass' });

export const loaders = [mswLoader];
export const parameters = {
  msw: {
    handlers,
  },
};
```

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user-info', () => {
    return HttpResponse.json({
      username: 'testuser',
      email: 'test@example.com',
    });
  }),
];
```

## Testing Configuration Components

```typescript
import { AppConfigProvider } from '../contexts/AppConfigContext';

const mockConfig = {
  siteName: 'Test Site',
  baseUrl: 'http://localhost:3000',
  // ... other required config
};

function renderWithConfig(ui: React.ReactElement) {
  return render(
    <AppConfigProvider config={mockConfig}>
      {ui}
    </AppConfigProvider>
  );
}

it('uses config', () => {
  renderWithConfig(<MyComponent />);
  expect(screen.getByText('Test Site')).toBeInTheDocument();
});
```

## Async Testing

### Waiting for Elements

```typescript
// Wait for element to appear
await screen.findByText('Loaded data');

// Wait for element to disappear
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));

// Custom wait
await waitFor(() => {
  expect(screen.getByText('Done')).toBeInTheDocument();
});
```

### Testing Async Functions

```typescript
it('fetches data', async () => {
  const { result } = renderHook(() => useMyData());

  // Wait for loading to complete
  await waitFor(() => {
    expect(result.current.isLoading).toBe(false);
  });

  expect(result.current.data).toEqual(expectedData);
});
```

## Coverage

```bash
# Run tests with coverage
pnpm test -- --coverage

# Coverage thresholds in vitest.config.ts
test: {
  coverage: {
    reporter: ['text', 'json', 'html'],
    thresholds: {
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
}
```

## Debugging Tests

```bash
# Run single test file
pnpm test --filter @lsst-sqre/squared -- MyComponent.test.tsx

# Run in watch mode
pnpm test --filter @lsst-sqre/squared -- --watch

# Debug in browser (for Storybook tests)
pnpm test-storybook:watch --filter @lsst-sqre/squared
```

### Debug Queries

```typescript
import { screen } from '@testing-library/react';

// Print DOM tree
screen.debug();

// Print specific element
screen.debug(screen.getByRole('button'));

// Log available roles
screen.logTestingPlaygroundURL();
```

## CI Pipeline

### test-suite-runner Agent

Use the test-suite-runner agent (via Task tool) for comprehensive testing:

```typescript
// Agent runs: pnpm run localci
// Which includes:
// - pnpm format:check
// - pnpm lint
// - pnpm type-check
// - pnpm test
// - pnpm build
```

The agent:
- Runs full CI pipeline
- Analyzes failures across all stages
- Provides detailed failure reports
- Suggests fixes

## Best Practices

1. **Test behavior, not implementation**
2. **Use semantic queries** (getByRole, etc.)
3. **Mock external dependencies** (APIs, modules)
4. **Test user interactions** with userEvent
5. **Use descriptive test names**
6. **Keep tests focused and small**
7. **Avoid testing internal state**
8. **Test accessibility** with role queries
9. **Use story tests for visual testing**
10. **Run tests before committing**
