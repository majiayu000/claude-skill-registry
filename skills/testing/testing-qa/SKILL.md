---
name: testing-qa
description: Expert guide for testing Next.js applications with Playwright, Jest, and React Testing Library. Use when writing tests, debugging test failures, or setting up test infrastructure.
---

# Testing & QA Skill

## Overview

This skill helps you write comprehensive tests for Next.js applications using Playwright for E2E tests, Jest for unit tests, and React Testing Library for component tests.

## Testing Philosophy

### Testing Pyramid
1. **E2E Tests (10%)**: Critical user journeys
2. **Integration Tests (30%)**: Component interactions
3. **Unit Tests (60%)**: Individual functions and utilities

### What to Test
- **DO**: Test behavior, not implementation
- **DO**: Test user interactions and outcomes
- **DO**: Test error states and edge cases
- **DO**: Test accessibility
- **DON'T**: Test internal implementation details
- **DON'T**: Test third-party libraries
- **DON'T**: Over-test simple presentational components

## Playwright E2E Tests

### Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### Basic E2E Test

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should sign up new user', async ({ page }) => {
    await page.goto('/signup')

    // Fill form
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.fill('input[name="confirmPassword"]', 'password123')

    // Submit
    await page.click('button[type="submit"]')

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard')

    // Verify welcome message
    await expect(page.getByText('Welcome')).toBeVisible()
  })

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'wrong@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // Verify error message
    await expect(page.getByText('Invalid credentials')).toBeVisible()
  })
})
```

### Advanced Playwright Patterns

```typescript
// Page Object Model
// e2e/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email)
    await this.page.fill('input[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }

  async getErrorMessage() {
    return await this.page.locator('[role="alert"]').textContent()
  }
}

// Usage
test('login with page object', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('test@example.com', 'password')
  await expect(page).toHaveURL('/dashboard')
})

// Fixtures for authenticated state
// e2e/fixtures.ts
export const test = base.extend<{ authenticatedPage: Page }>({
  authenticatedPage: async ({ page }, use) => {
    // Login
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')

    await use(page)
  },
})

// Usage
test('dashboard test', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard')
  // Test authenticated functionality
})
```

### Common Playwright Patterns

```typescript
// Wait for network
await page.waitForResponse(resp => resp.url().includes('/api/items'))

// Test file upload
await page.setInputFiles('input[type="file"]', 'path/to/file.jpg')

// Test download
const downloadPromise = page.waitForEvent('download')
await page.click('button:has-text("Download")')
const download = await downloadPromise
await download.saveAs('/path/to/save')

// Mock API responses
await page.route('**/api/items', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ items: [] }),
  })
})

// Screenshot for debugging
await page.screenshot({ path: 'debug.png', fullPage: true })

// Test responsive design
await page.setViewportSize({ width: 375, height: 667 }) // iPhone size

// Test accessibility
const accessibilityScanResults = await new AxeBuilder({ page }).analyze()
expect(accessibilityScanResults.violations).toEqual([])
```

## Component Testing

### Setup React Testing Library

```typescript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
}

// jest.setup.js
import '@testing-library/jest-dom'
```

### Basic Component Test

```typescript
// components/button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByText('Click me')).toBeDisabled()
  })

  it('applies variant styles', () => {
    render(<Button variant="destructive">Delete</Button>)
    const button = screen.getByText('Delete')
    expect(button).toHaveClass('bg-red-600')
  })
})
```

### Testing Async Components

```typescript
// components/user-profile.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './user-profile'

// Mock fetch
global.fetch = jest.fn()

describe('UserProfile', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('displays loading state initially', () => {
    (fetch as jest.Mock).mockImplementation(() =>
      new Promise(() => {}) // Never resolves
    )

    render(<UserProfile userId="123" />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('displays user data when loaded', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ name: 'John Doe', email: 'john@example.com' }),
    })

    render(<UserProfile userId="123" />)

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('john@example.com')).toBeInTheDocument()
    })
  })

  it('displays error message when fetch fails', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Failed to fetch'))

    render(<UserProfile userId="123" />)

    await waitFor(() => {
      expect(screen.getByText('Error loading user')).toBeInTheDocument()
    })
  })
})
```

### Testing Forms

```typescript
// components/contact-form.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ContactForm } from './contact-form'

describe('ContactForm', () => {
  it('validates required fields', async () => {
    render(<ContactForm />)

    const submitButton = screen.getByText('Submit')
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument()
      expect(screen.getByText('Message is required')).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    const onSubmit = jest.fn()

    render(<ContactForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Message'), 'Test message')
    await user.click(screen.getByText('Submit'))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        message: 'Test message',
      })
    })
  })

  it('disables submit button while submitting', async () => {
    const user = userEvent.setup()

    render(<ContactForm />)

    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Message'), 'Test message')

    const submitButton = screen.getByText('Submit')
    await user.click(submitButton)

    expect(submitButton).toBeDisabled()
  })
})
```

### Testing Hooks

```typescript
// hooks/use-counter.test.ts
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './use-counter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10))
    expect(result.current.count).toBe(10)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounter())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('resets count', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })
})
```

## Unit Testing

### Testing Utilities

```typescript
// lib/utils.test.ts
import { formatDate, slugify, truncate } from './utils'

describe('formatDate', () => {
  it('formats date correctly', () => {
    const date = new Date('2024-01-15')
    expect(formatDate(date)).toBe('January 15, 2024')
  })

  it('handles invalid date', () => {
    expect(formatDate(new Date('invalid'))).toBe('Invalid Date')
  })
})

describe('slugify', () => {
  it('converts string to slug', () => {
    expect(slugify('Hello World')).toBe('hello-world')
    expect(slugify('Next.js App!')).toBe('next-js-app')
  })

  it('removes special characters', () => {
    expect(slugify('Test@#$%')).toBe('test')
  })
})

describe('truncate', () => {
  it('truncates long strings', () => {
    const text = 'This is a very long text'
    expect(truncate(text, 10)).toBe('This is a...')
  })

  it('does not truncate short strings', () => {
    const text = 'Short'
    expect(truncate(text, 10)).toBe('Short')
  })
})
```

### Testing API Routes

```typescript
// app/api/items/route.test.ts
import { GET, POST } from './route'
import { NextRequest } from 'next/server'

describe('/api/items', () => {
  describe('GET', () => {
    it('returns items', async () => {
      const request = new NextRequest('http://localhost:3000/api/items')
      const response = await GET(request)
      const data = await response.json()

      expect(response.status).toBe(200)
      expect(data.items).toBeDefined()
      expect(Array.isArray(data.items)).toBe(true)
    })
  })

  describe('POST', () => {
    it('creates new item', async () => {
      const request = new NextRequest('http://localhost:3000/api/items', {
        method: 'POST',
        body: JSON.stringify({ title: 'Test Item' }),
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(201)
      expect(data.item).toBeDefined()
      expect(data.item.title).toBe('Test Item')
    })

    it('validates required fields', async () => {
      const request = new NextRequest('http://localhost:3000/api/items', {
        method: 'POST',
        body: JSON.stringify({}),
      })

      const response = await POST(request)

      expect(response.status).toBe(400)
    })
  })
})
```

## Mocking

### Mock Supabase

```typescript
// __mocks__/supabase.ts
export const createClient = jest.fn(() => ({
  from: jest.fn(() => ({
    select: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    update: jest.fn().mockReturnThis(),
    delete: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    single: jest.fn().mockResolvedValue({
      data: { id: '1', title: 'Test' },
      error: null,
    }),
  })),
  auth: {
    getUser: jest.fn().mockResolvedValue({
      data: { user: { id: '123', email: 'test@example.com' } },
      error: null,
    }),
  },
}))
```

### Mock Next.js Router

```typescript
// Mock useRouter
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: () => '/test-path',
  useSearchParams: () => new URLSearchParams(),
}))
```

### Mock External API

```typescript
// Use MSW (Mock Service Worker)
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/items', (req, res, ctx) => {
    return res(
      ctx.json({
        items: [
          { id: '1', title: 'Item 1' },
          { id: '2', title: 'Item 2' },
        ],
      })
    )
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Testing Checklist

### E2E Tests
- [ ] Test critical user journeys (signup, login, checkout)
- [ ] Test on multiple browsers
- [ ] Test on mobile viewport
- [ ] Test error states
- [ ] Test with slow network
- [ ] Test with disabled JavaScript (where applicable)
- [ ] Test accessibility

### Component Tests
- [ ] Test rendering
- [ ] Test user interactions
- [ ] Test props
- [ ] Test conditional rendering
- [ ] Test error states
- [ ] Test loading states
- [ ] Test accessibility

### Unit Tests
- [ ] Test pure functions
- [ ] Test edge cases
- [ ] Test error handling
- [ ] Test with various inputs
- [ ] Test boundary conditions

## Common Testing Patterns

### Test IDs for Reliable Selection

```typescript
// Component
<button data-testid="submit-button">Submit</button>

// Test
const button = screen.getByTestId('submit-button')
```

### Accessible Queries (Preferred)

```typescript
// By role (best)
screen.getByRole('button', { name: /submit/i })

// By label
screen.getByLabelText('Email')

// By text
screen.getByText('Welcome')

// By placeholder
screen.getByPlaceholderText('Enter email')
```

### Testing Loading States

```typescript
it('shows loading then content', async () => {
  render(<Component />)

  // Loading state
  expect(screen.getByText('Loading...')).toBeInTheDocument()

  // Wait for content
  await waitFor(() => {
    expect(screen.getByText('Content')).toBeInTheDocument()
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
  })
})
```

### Testing Error Boundaries

```typescript
it('renders error boundary on error', () => {
  const spy = jest.spyOn(console, 'error').mockImplementation()

  render(
    <ErrorBoundary>
      <ComponentThatThrows />
    </ErrorBoundary>
  )

  expect(screen.getByText('Something went wrong')).toBeInTheDocument()

  spy.mockRestore()
})
```

## Debugging Tests

### Debug Output

```typescript
import { screen, render } from '@testing-library/react'

// Print component tree
render(<Component />)
screen.debug()

// Print specific element
screen.debug(screen.getByRole('button'))
```

### Playwright Debug

```bash
# Run in debug mode with browser
npx playwright test --debug

# Run specific test
npx playwright test auth.spec.ts --debug

# Run with headed browser
npx playwright test --headed
```

### Common Issues

**Element not found:**
- Check if element exists: `screen.getByText` vs `screen.queryByText`
- Use `findBy` for async elements: `screen.findByText`
- Check accessibility tree: `screen.debug()`

**Timing issues:**
- Use `waitFor` for async updates
- Use `findBy` queries (built-in wait)
- Increase timeout if needed

**State updates not reflected:**
- Wrap in `act()` if updating state manually
- Use `userEvent` instead of `fireEvent` for more realistic events

## Performance Testing

```typescript
// Lighthouse CI
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
      },
    },
  },
}
```

## When to Use This Skill

Invoke this skill when:
- Writing new tests
- Debugging test failures
- Setting up test infrastructure
- Testing specific scenarios (forms, async, auth)
- Implementing E2E tests
- Testing accessibility
- Mocking dependencies
- Improving test coverage