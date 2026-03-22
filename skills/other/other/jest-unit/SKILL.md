---
name: jest-unit
description: |
  Jest unit testing patterns for this Next.js application.
  Covers test structure, mocking strategies, React component testing, hook testing, and coverage targets.
  Use this skill when writing unit tests for services, hooks, utilities, or components.
allowed-tools: Read, Glob, Grep
version: 1.1.0
---

# Jest Unit Testing Skill

Patterns for writing effective unit tests with Jest and React Testing Library.

## Architecture Overview

```
TEST FILE STRUCTURE:

core/tests/jest/
├── api/                 # API route tests
├── hooks/               # React hooks tests
├── lib/                 # Utility tests
├── components/          # Component tests
├── services/            # Service tests
├── __mocks__/           # Mock utilities
│   ├── db-mocks.ts
│   ├── better-auth.js
│   └── next-server.js
└── setup.ts             # Global configuration

contents/themes/default/tests/jest/
└── ...                  # Theme-specific tests

contents/plugins/*/__tests__/
└── ...                  # Plugin-specific tests
```

## When to Use This Skill

- Writing unit tests for services
- Testing React hooks
- Testing React components
- Mocking database operations
- Setting up test coverage

---

## Test File Structure

### Naming Conventions

```
*.test.ts   - TypeScript unit tests
*.test.tsx  - React component tests
```

### Standard Test Structure

```typescript
import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals'
import { functionToTest } from '@/core/lib/module'

describe('ModuleName', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  afterEach(() => {
    jest.clearAllMocks()
    jest.resetModules()
  })

  describe('Feature Group', () => {
    test('should do expected behavior when condition met', () => {
      // Arrange
      const input = 'test-data'

      // Act
      const result = functionToTest(input)

      // Assert
      expect(result).toBe('expected-output')
    })
  })
})
```

---

## Jest Configuration

```typescript
// jest.config.ts
import type { Config } from 'jest'

export const baseConfig: Partial<Config> = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',

  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^@/core/(.*)$': '<rootDir>/core/$1',
    'next/server': '<rootDir>/core/tests/jest/__mocks__/next-server.js',
  },

  setupFilesAfterEnv: ['<rootDir>/core/tests/setup.ts'],
  testTimeout: 10000,
}
```

### Test Scripts

```bash
pnpm test              # Run all core tests
pnpm test:theme        # Run theme-specific tests
pnpm test:coverage     # Generate coverage reports
pnpm test:watch        # Watch mode
```

---

## Essential Mocking (Quick Reference)

### Database (MANDATORY)

```typescript
jest.mock('@/core/lib/db', () => ({
  queryWithRLS: jest.fn(),
  queryOneWithRLS: jest.fn(),
  mutateWithRLS: jest.fn(),
}))

const mockQueryWithRLS = queryWithRLS as jest.MockedFunction<typeof queryWithRLS>

test('example', async () => {
  mockQueryWithRLS.mockResolvedValue([{ id: '123' }])
  // ...
})
```

### Next.js Navigation

```typescript
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), replace: jest.fn() }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}))
```

### Translations

```typescript
jest.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
  useLocale: () => 'en',
}))
```

→ See `references/mocking-patterns.md` for complete mocking strategies

---

## Quick Testing Patterns

### Component Test

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('form submission', async () => {
  const user = userEvent.setup()
  render(<MyForm />)

  await user.type(screen.getByLabelText('Email'), 'test@example.com')
  await user.click(screen.getByRole('button', { name: /submit/i }))

  expect(await screen.findByText('Success')).toBeInTheDocument()
})
```

→ See `references/component-testing.md` for complete patterns

### Hook Test

```typescript
import { renderHook, act } from '@testing-library/react'

test('hook state update', () => {
  const { result } = renderHook(() => useCounter())

  act(() => {
    result.current.increment()
  })

  expect(result.current.count).toBe(1)
})
```

→ See `references/service-hook-testing.md` for complete patterns

---

## Coverage Targets

| Category | Target | Notes |
|----------|--------|-------|
| **Critical Paths** | 90%+ | Auth, API, Validation |
| **Features** | 80%+ | UI, Business Logic |
| **Utilities** | 80%+ | Helpers, Services |
| **Components** | 70%+ | UI Components |

---

## Common Assertions

```typescript
// Equality
expect(result).toBe('expected')
expect(result).toEqual({ id: '123' })

// Truthiness
expect(result).toBeTruthy()
expect(result).toBeNull()
expect(result).toBeDefined()

// Collections
expect(array).toHaveLength(2)
expect(array).toContain('item')
expect(obj).toHaveProperty('key')

// DOM (Testing Library)
expect(element).toBeInTheDocument()
expect(element).toHaveClass('className')
expect(element).toBeVisible()
expect(element).toBeDisabled()

// Mocks
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith('arg')
expect(mockFn).toHaveBeenCalledTimes(1)
```

---

## Anti-Patterns

```typescript
// ❌ NEVER: Test implementation details
expect(result.current._internalState).toBe('value')

// ✅ CORRECT: Test observable behavior
expect(result.current.displayValue).toBe('value')

// ❌ NEVER: Skip cleanup
// No afterEach → leaks between tests

// ✅ CORRECT: Always cleanup
afterEach(() => jest.clearAllMocks())

// ❌ NEVER: Async without await
fetchData().then(data => expect(data).toBeDefined())

// ✅ CORRECT: Properly await
const data = await fetchData()
expect(data).toBeDefined()

// ❌ NEVER: Use fireEvent for user actions
fireEvent.change(input, { target: { value: 'text' } })

// ✅ CORRECT: Use userEvent
await user.type(input, 'text')
```

---

## Checklist

Before finalizing unit tests:

- [ ] All database calls mocked (queryWithRLS, mutateWithRLS)
- [ ] External APIs mocked (fetch)
- [ ] Next.js functions mocked (useRouter, useSearchParams)
- [ ] afterEach cleanup with jest.clearAllMocks()
- [ ] Async tests properly awaited
- [ ] Test both success and error paths
- [ ] Edge cases covered (null, empty, invalid input)
- [ ] Coverage targets met (90%+ critical, 80%+ features)
- [ ] Test names are descriptive

---

## References

- `references/mocking-patterns.md` - Complete mocking strategies
- `references/component-testing.md` - React component testing patterns
- `references/service-hook-testing.md` - Service and hook testing patterns

## Related Skills

- `cypress-e2e` - Integration/E2E testing
- `cypress-api` - API testing with Cypress
- `zod-validation` - Schema validation testing
- `service-layer` - Service patterns to test
