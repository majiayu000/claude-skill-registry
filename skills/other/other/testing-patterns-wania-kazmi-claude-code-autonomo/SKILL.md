---
name: testing-patterns
description: |
  Comprehensive testing patterns for Jest, Vitest, Playwright, and React Testing Library.
  Use when writing unit tests, integration tests, or E2E tests.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Testing Patterns & Best Practices

## Testing Principles

### 1. Test Behavior, Not Implementation
- Test what the code does, not how it does it
- Tests shouldn't break when refactoring
- Focus on inputs and outputs

### 2. Arrange-Act-Assert (AAA)
```typescript
// Arrange - Set up test data
const user = { name: 'John', email: 'john@example.com' }

// Act - Execute the code
const result = validateUser(user)

// Assert - Verify the outcome
expect(result.isValid).toBe(true)
```

### 3. Test Isolation
- Each test should be independent
- No shared state between tests
- Clean up after each test

## Unit Testing Patterns

### Basic Test Structure

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const userData = { name: 'John', email: 'john@example.com' }
      const result = await userService.createUser(userData)
      
      expect(result).toMatchObject({
        id: expect.any(String),
        name: 'John',
        email: 'john@example.com'
      })
    })

    it('should throw error for invalid email', async () => {
      const userData = { name: 'John', email: 'invalid' }
      
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Invalid email format')
    })
  })
})
```

### Mocking Patterns

```typescript
// Mock a module
jest.mock('./database', () => ({
  query: jest.fn()
}))

// Mock implementation
const mockQuery = jest.mocked(query)
mockQuery.mockResolvedValue([{ id: '1', name: 'Test' }])

// Spy on method
const spy = jest.spyOn(userService, 'sendEmail')
spy.mockResolvedValue(undefined)

// Verify mock was called
expect(mockQuery).toHaveBeenCalledWith(
  'SELECT * FROM users WHERE id = ?',
  ['123']
)
expect(mockQuery).toHaveBeenCalledTimes(1)
```

### Testing Async Code

```typescript
// Async/await
it('should fetch user data', async () => {
  const user = await fetchUser('123')
  expect(user.name).toBe('John')
})

// Testing promises that reject
it('should handle fetch errors', async () => {
  await expect(fetchUser('invalid'))
    .rejects
    .toThrow('User not found')
})

// Testing timers
it('should debounce calls', () => {
  jest.useFakeTimers()
  
  const callback = jest.fn()
  const debounced = debounce(callback, 100)
  
  debounced()
  debounced()
  debounced()
  
  expect(callback).not.toHaveBeenCalled()
  
  jest.advanceTimersByTime(100)
  
  expect(callback).toHaveBeenCalledTimes(1)
})
```

### Testing Error Handling

```typescript
it('should handle network errors gracefully', async () => {
  mockFetch.mockRejectedValue(new Error('Network error'))
  
  const result = await fetchDataWithRetry('/api/data')
  
  expect(result).toEqual({ error: 'Failed to fetch data' })
  expect(mockFetch).toHaveBeenCalledTimes(3) // Retried 3 times
})
```

## React Testing Library Patterns

### Component Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

describe('LoginForm', () => {
  it('should submit form with credentials', async () => {
    const onSubmit = jest.fn()
    render(<LoginForm onSubmit={onSubmit} />)
    
    // Find elements by accessible roles/text
    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })
    
    // Interact with form
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.click(submitButton)
    
    // Assert
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      })
    })
  })

  it('should display validation errors', async () => {
    render(<LoginForm onSubmit={jest.fn()} />)
    
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))
    
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument()
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument()
  })
})
```

### Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react'

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter(0))
    
    expect(result.current.count).toBe(0)
    
    act(() => {
      result.current.increment()
    })
    
    expect(result.current.count).toBe(1)
  })

  it('should reset counter', () => {
    const { result } = renderHook(() => useCounter(5))
    
    act(() => {
      result.current.increment()
      result.current.reset()
    })
    
    expect(result.current.count).toBe(5)
  })
})
```

### Testing with Context

```typescript
const wrapper = ({ children }) => (
  <AuthProvider>
    <ThemeProvider>
      {children}
    </ThemeProvider>
  </AuthProvider>
)

it('should use auth context', () => {
  render(<UserProfile />, { wrapper })
  
  expect(screen.getByText('Logged in as John')).toBeInTheDocument()
})
```

## Playwright E2E Patterns

### Basic Page Testing

```typescript
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login')
    
    await page.fill('[data-testid="email"]', 'user@example.com')
    await page.fill('[data-testid="password"]', 'password123')
    await page.click('[data-testid="submit"]')
    
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('[data-testid="welcome"]'))
      .toContainText('Welcome, User')
  })

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login')
    
    await page.fill('[data-testid="email"]', 'wrong@example.com')
    await page.fill('[data-testid="password"]', 'wrongpassword')
    await page.click('[data-testid="submit"]')
    
    await expect(page.locator('[data-testid="error"]'))
      .toContainText('Invalid credentials')
  })
})
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email)
    await this.page.fill('[data-testid="password"]', password)
    await this.page.click('[data-testid="submit"]')
  }

  async getErrorMessage() {
    return this.page.locator('[data-testid="error"]').textContent()
  }
}

// tests/login.spec.ts
test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@example.com', 'password123')
  
  await expect(page).toHaveURL('/dashboard')
})
```

### API Testing with Playwright

```typescript
test('should create user via API', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      name: 'John',
      email: 'john@example.com'
    }
  })
  
  expect(response.ok()).toBeTruthy()
  
  const user = await response.json()
  expect(user).toMatchObject({
    id: expect.any(String),
    name: 'John',
    email: 'john@example.com'
  })
})
```

### Visual Testing

```typescript
test('should match screenshot', async ({ page }) => {
  await page.goto('/dashboard')
  
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100
  })
})
```

## Test Data Patterns

### Factory Pattern

```typescript
// factories/user.factory.ts
export function createUser(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    createdAt: new Date(),
    ...overrides
  }
}

// Usage in tests
const user = createUser({ name: 'Custom Name' })
```

### Builder Pattern

```typescript
class UserBuilder {
  private user: Partial<User> = {}

  withName(name: string) {
    this.user.name = name
    return this
  }

  withEmail(email: string) {
    this.user.email = email
    return this
  }

  asAdmin() {
    this.user.role = 'admin'
    return this
  }

  build(): User {
    return {
      id: faker.string.uuid(),
      name: this.user.name ?? faker.person.fullName(),
      email: this.user.email ?? faker.internet.email(),
      role: this.user.role ?? 'user',
      createdAt: new Date()
    }
  }
}

// Usage
const adminUser = new UserBuilder().withName('Admin').asAdmin().build()
```

## Coverage Requirements

### Minimum Coverage Targets
- **80% overall** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

### Running Coverage

```bash
# Jest
npm test -- --coverage

# Vitest
npx vitest run --coverage

# Check thresholds
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

## Edge Cases to Test

- [ ] Null/undefined inputs
- [ ] Empty arrays/strings
- [ ] Boundary values (0, -1, MAX_INT)
- [ ] Unicode characters
- [ ] Very long strings
- [ ] Concurrent operations
- [ ] Network failures
- [ ] Timeout scenarios
- [ ] Permission denied errors

## Anti-Patterns to Avoid

### Testing Implementation Details
```typescript
// BAD: Testing internal state
expect(component.state.isLoading).toBe(true)

// GOOD: Testing visible behavior
expect(screen.getByTestId('spinner')).toBeInTheDocument()
```

### Brittle Selectors
```typescript
// BAD: Fragile selectors
page.locator('.btn-primary.mt-4.px-6')

// GOOD: Semantic selectors
page.locator('[data-testid="submit-button"]')
page.getByRole('button', { name: 'Submit' })
```

### Over-Mocking
```typescript
// BAD: Mocking everything
jest.mock('./utils')
jest.mock('./helpers')
jest.mock('./constants')

// GOOD: Only mock external dependencies
jest.mock('./api-client')
```

## Checklist

- [ ] Tests follow AAA pattern
- [ ] Each test has single assertion focus
- [ ] No shared state between tests
- [ ] Proper cleanup in afterEach
- [ ] Meaningful test descriptions
- [ ] Edge cases covered
- [ ] Async code properly awaited
- [ ] Coverage meets thresholds
