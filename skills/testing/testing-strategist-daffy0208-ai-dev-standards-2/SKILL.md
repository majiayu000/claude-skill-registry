---
name: Testing Strategist
description: Design and implement comprehensive testing strategies. Use when setting up tests, choosing test types, implementing TDD, or improving code quality. Covers unit tests, integration tests, E2E tests, test-driven development, and testing best practices.
version: 1.0.0
---

# Testing Strategist

Test the right things at the right level - write tests that give you confidence to ship.

## Core Principle

**The Testing Pyramid:** 70% unit tests, 20% integration tests, 10% E2E tests.

Tests should be:

- **Fast** - Run in milliseconds (unit) to seconds (integration) to minutes (E2E)
- **Isolated** - Test one thing at a time
- **Repeatable** - Same input = same output
- **Self-checking** - Pass/fail automatically, no manual verification
- **Timely** - Written alongside code (or before, with TDD)

---

## The Testing Pyramid

```
           /\
          /  \         E2E Tests (10%)
         /----\        - Slow, brittle, expensive
        /      \       - Test critical user journeys
       /--------\      - Example: "User can complete checkout"
      /          \
     /------------\    Integration Tests (20%)
    /              \   - Medium speed, test components together
   /----------------\  - Example: "API endpoint returns correct data"
  /                  \
 /--------------------\ Unit Tests (70%)
/______________________\ - Fast, isolated, test functions/components
                        - Example: "calculateTotal returns sum"
```

### Why This Ratio?

- **Unit tests:** Fast feedback, pinpoint bugs precisely, easy to maintain
- **Integration tests:** Ensure components work together, catch interface issues
- **E2E tests:** Verify actual user flows, catch UI bugs, but slow and brittle

---

## Level 1: Unit Tests (70%)

### What to Test

Test individual functions, components, or classes in isolation.

**Good candidates:**

- ✅ Business logic functions (calculations, validation, transformations)
- ✅ Utility functions (formatDate, parseUrl, etc.)
- ✅ React components (rendering, props, state)
- ✅ Hooks (custom React hooks)
- ✅ Pure functions (same input = same output)

**Skip:**

- ❌ Third-party libraries (assume they work)
- ❌ Framework internals (React, Next.js)
- ❌ Simple getters/setters with no logic

### Unit Test Examples

#### Testing Business Logic (Jest + TypeScript)

```typescript
// src/lib/pricing.ts
export function calculateTotal(items: { price: number; quantity: number }[]) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0)
}

export function applyDiscount(total: number, discountPercent: number) {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Invalid discount percentage')
  }
  return total * (1 - discountPercent / 100)
}

// src/lib/pricing.test.ts
import { calculateTotal, applyDiscount } from './pricing'

describe('calculateTotal', () => {
  it('calculates total for single item', () => {
    const items = [{ price: 10, quantity: 2 }]
    expect(calculateTotal(items)).toBe(20)
  })

  it('calculates total for multiple items', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ]
    expect(calculateTotal(items)).toBe(35)
  })

  it('returns 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0)
  })
})

describe('applyDiscount', () => {
  it('applies discount correctly', () => {
    expect(applyDiscount(100, 20)).toBe(80)
  })

  it('throws error for invalid discount', () => {
    expect(() => applyDiscount(100, -10)).toThrow('Invalid discount')
    expect(() => applyDiscount(100, 150)).toThrow('Invalid discount')
  })
})
```

#### Testing React Components (Jest + React Testing Library)

```typescript
// src/components/Button.tsx
export function Button({
  children,
  variant = 'primary',
  onClick
}: {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
}) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('applies primary variant by default', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-primary')
  })

  it('applies secondary variant when specified', () => {
    render(<Button variant="secondary">Click me</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-secondary')
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

#### Testing Custom Hooks

```typescript
// src/hooks/useCounter.ts
import { useState } from 'react'

export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue)

  const increment = () => setCount(c => c + 1)
  const decrement = () => setCount(c => c - 1)
  const reset = () => setCount(initialValue)

  return { count, increment, decrement, reset }
}

// src/hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

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

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })
})
```

### Unit Test Best Practices

✅ **Do:**

- Test behavior, not implementation
- Use descriptive test names (it should...)
- Follow AAA pattern: Arrange, Act, Assert
- Test edge cases (empty arrays, null, negative numbers)
- Keep tests simple and readable

❌ **Don't:**

- Test private methods directly
- Over-mock (makes tests brittle)
- Test framework internals
- Write tests that depend on other tests

---

## Level 2: Integration Tests (20%)

### What to Test

Test multiple units working together - typically API routes, database operations, or service integrations.

**Good candidates:**

- ✅ API endpoints (request → controller → database → response)
- ✅ Database operations (queries, transactions)
- ✅ Third-party integrations (Stripe, SendGrid)
- ✅ Authentication flows
- ✅ File upload/download

### Integration Test Examples

#### Testing API Routes (Next.js + Supertest)

```typescript
// app/api/posts/route.ts
export async function GET() {
  const posts = await db.post.findMany({
    include: { author: true },
    orderBy: { createdAt: 'desc' }
  })
  return Response.json(posts)
}

export async function POST(request: Request) {
  const body = await request.json()

  // Validate
  const result = PostSchema.safeParse(body)
  if (!result.success) {
    return Response.json({ errors: result.error.issues }, { status: 400 })
  }

  // Create post
  const post = await db.post.create({
    data: {
      title: result.data.title,
      content: result.data.content,
      authorId: request.user.id
    }
  })

  return Response.json(post, { status: 201 })
}

// app/api/posts/route.test.ts
import { testClient } from '@/lib/test-utils'

describe('POST /api/posts', () => {
  beforeEach(async () => {
    // Clean database before each test
    await db.post.deleteMany()
  })

  it('creates a new post', async () => {
    const response = await testClient
      .post('/api/posts')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        title: 'Test Post',
        content: 'This is a test post'
      })

    expect(response.status).toBe(201)
    expect(response.body).toMatchObject({
      title: 'Test Post',
      content: 'This is a test post'
    })

    // Verify in database
    const posts = await db.post.findMany()
    expect(posts).toHaveLength(1)
    expect(posts[0].title).toBe('Test Post')
  })

  it('returns 400 for invalid data', async () => {
    const response = await testClient
      .post('/api/posts')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        title: '' // Invalid: empty title
      })

    expect(response.status).toBe(400)
    expect(response.body.errors).toBeDefined()
  })

  it('returns 401 for unauthenticated request', async () => {
    const response = await testClient.post('/api/posts').send({
      title: 'Test',
      content: 'Test'
    })

    expect(response.status).toBe(401)
  })
})

describe('GET /api/posts', () => {
  beforeEach(async () => {
    await db.post.deleteMany()

    // Seed test data
    await db.post.createMany({
      data: [
        { title: 'Post 1', content: 'Content 1', authorId: user.id },
        { title: 'Post 2', content: 'Content 2', authorId: user.id }
      ]
    })
  })

  it('returns all posts', async () => {
    const response = await testClient.get('/api/posts')

    expect(response.status).toBe(200)
    expect(response.body).toHaveLength(2)
    expect(response.body[0].author).toBeDefined()
  })
})
```

#### Testing Database Operations

```typescript
// src/lib/repositories/userRepository.test.ts
import { db } from '@/lib/db'
import { createUser, findUserByEmail, updateUser } from './userRepository'

describe('userRepository', () => {
  beforeEach(async () => {
    await db.user.deleteMany()
  })

  afterAll(async () => {
    await db.$disconnect()
  })

  describe('createUser', () => {
    it('creates user with hashed password', async () => {
      const user = await createUser({
        email: 'test@example.com',
        password: 'password123'
      })

      expect(user.email).toBe('test@example.com')
      expect(user.password).not.toBe('password123') // Should be hashed
      expect(user.password).toMatch(/^\$2[aby]/) // bcrypt hash format
    })

    it('throws error for duplicate email', async () => {
      await createUser({ email: 'test@example.com', password: 'pass' })

      await expect(createUser({ email: 'test@example.com', password: 'pass' })).rejects.toThrow()
    })
  })

  describe('findUserByEmail', () => {
    it('finds existing user', async () => {
      await createUser({ email: 'test@example.com', password: 'pass' })

      const user = await findUserByEmail('test@example.com')
      expect(user).toBeDefined()
      expect(user?.email).toBe('test@example.com')
    })

    it('returns null for non-existent user', async () => {
      const user = await findUserByEmail('nonexistent@example.com')
      expect(user).toBeNull()
    })
  })
})
```

### Integration Test Best Practices

✅ **Do:**

- Use test database (separate from development/production)
- Clean up test data (beforeEach/afterEach)
- Test happy path + error cases
- Test authentication/authorization
- Use factories/fixtures for test data

❌ **Don't:**

- Test against production database
- Leave test data behind
- Mock database (defeats purpose of integration test)
- Depend on external services (mock external APIs)

---

## Level 3: E2E Tests (10%)

### What to Test

Test complete user journeys through the actual UI.

**Good candidates:**

- ✅ Critical user flows (signup, login, checkout)
- ✅ Core business processes
- ✅ Multi-step workflows

**Skip:**

- ❌ Every possible UI interaction (too slow/brittle)
- ❌ Edge cases (cover with unit/integration tests)

### E2E Test Examples (Playwright)

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('user can sign up and log in', async ({ page }) => {
    // Navigate to signup
    await page.goto('/signup')

    // Fill signup form
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'SecurePass123!')
    await page.fill('input[name="confirmPassword"]', 'SecurePass123!')

    // Submit form
    await page.click('button[type="submit"]')

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Welcome')

    // Logout
    await page.click('[data-testid="logout-button"]')

    // Should redirect to login
    await expect(page).toHaveURL('/login')

    // Login again
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'SecurePass123!')
    await page.click('button[type="submit"]')

    // Should be back at dashboard
    await expect(page).toHaveURL('/dashboard')
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'wrong@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // Should show error message
    await expect(page.locator('[role="alert"]')).toContainText('Invalid credentials')

    // Should stay on login page
    await expect(page).toHaveURL('/login')
  })
})

// tests/e2e/checkout.spec.ts
test.describe('Checkout Flow', () => {
  test('user can complete purchase', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password')
    await page.click('button[type="submit"]')

    // Add product to cart
    await page.goto('/products')
    await page.click('[data-testid="product-1"] button:text("Add to Cart")')

    // Verify cart badge
    await expect(page.locator('[data-testid="cart-badge"]')).toContainText('1')

    // Go to checkout
    await page.click('[data-testid="cart-button"]')
    await page.click('button:text("Checkout")')

    // Fill shipping info
    await page.fill('input[name="address"]', '123 Main St')
    await page.fill('input[name="city"]', 'San Francisco')
    await page.fill('input[name="zip"]', '94103')

    // Fill payment info (test mode)
    await page.fill('input[name="cardNumber"]', '4242424242424242')
    await page.fill('input[name="expiry"]', '12/25')
    await page.fill('input[name="cvc"]', '123')

    // Submit order
    await page.click('button:text("Place Order")')

    // Should see confirmation
    await expect(page).toHaveURL(/\/orders\/\d+/)
    await expect(page.locator('h1')).toContainText('Order Confirmed')
  })
})
```

### E2E Test Best Practices

✅ **Do:**

- Test critical paths only (< 20 tests)
- Use data-testid attributes (stable selectors)
- Run in CI/CD pipeline
- Test across browsers (Chrome, Firefox, Safari)
- Take screenshots on failure

❌ **Don't:**

- Test every UI variation
- Use fragile selectors (text content, nth-child)
- Run E2E tests on every commit (too slow)
- Ignore flaky tests (fix or remove them)

---

## Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

1. **Red:** Write a failing test
2. **Green:** Write minimal code to make it pass
3. **Refactor:** Improve code while keeping tests green

### TDD Example

```typescript
// 1. RED: Write failing test first
describe('formatCurrency', () => {
  it('formats number as USD currency', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })
})

// Run test: FAILS (formatCurrency doesn't exist)

// 2. GREEN: Write minimal implementation
export function formatCurrency(amount: number): string {
  return `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
}

// Run test: PASSES

// 3. REFACTOR: Improve implementation
export function formatCurrency(
  amount: number,
  currency: string = 'USD',
  locale: string = 'en-US'
): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency
  }).format(amount)
}

// Add more tests
it('formats EUR currency', () => {
  expect(formatCurrency(1234.56, 'EUR', 'de-DE')).toBe('1.234,56 €')
})

it('handles negative amounts', () => {
  expect(formatCurrency(-100)).toBe('-$100.00')
})
```

### When to Use TDD

**Good for:**

- ✅ Complex business logic
- ✅ Bug fixes (write test that reproduces bug first)
- ✅ Well-defined requirements
- ✅ Critical algorithms

**Skip for:**

- ❌ Exploratory coding (don't know requirements yet)
- ❌ Throwaway prototypes
- ❌ Simple CRUD operations

---

## Mocking Strategies

### When to Mock

- ✅ External APIs (slow, unreliable, cost money)
- ✅ Time/randomness (make tests deterministic)
- ✅ File system operations
- ✅ Database (in unit tests only)

### Mock Examples (Jest)

```typescript
// Mock external API
import { fetchUserData } from '@/lib/api'

jest.mock('@/lib/api')
const mockFetchUserData = fetchUserData as jest.MockedFunction<typeof fetchUserData>

it('displays user data', async () => {
  mockFetchUserData.mockResolvedValue({
    id: '1',
    name: 'John Doe',
    email: 'john@example.com'
  })

  render(<UserProfile userId="1" />)

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })
})

// Mock Date
beforeAll(() => {
  jest.useFakeTimers()
  jest.setSystemTime(new Date('2024-01-01'))
})

afterAll(() => {
  jest.useRealTimers()
})

it('shows correct date', () => {
  expect(getCurrentDate()).toBe('2024-01-01')
})

// Mock Math.random
const mockRandom = jest.spyOn(Math, 'random')
mockRandom.mockReturnValue(0.5)

expect(generateRandomId()).toBe('expected-id-with-0.5-random')

mockRandom.mockRestore()
```

### Mocking Best Practices

✅ **Do:**

- Mock at boundaries (APIs, file system)
- Restore mocks after tests
- Make mocks realistic (same shape as real data)

❌ **Don't:**

- Over-mock (makes tests brittle)
- Mock your own code (test real behavior)
- Mock what you don't own (unless external)

---

## Code Coverage

### Coverage Targets

- **70% minimum** - Below this, you're missing important tests
- **80% good** - Solid coverage of critical paths
- **90%+ diminishing returns** - Chasing 100% often not worth it

### What to Focus On

**High priority (must have 90%+ coverage):**

- Business logic
- Authentication/authorization
- Payment processing
- Data validation

**Medium priority (aim for 70%+):**

- API routes
- Database queries
- Utility functions

**Low priority (okay to skip):**

- UI components (test behavior, not implementation)
- Configuration files
- Type definitions
- Third-party integrations (integration tests better)

### Checking Coverage

```bash
# Jest
npm test -- --coverage

# View HTML report
open coverage/lcov-report/index.html
```

### Coverage Configuration (jest.config.js)

```javascript
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/types/**'
  ],
  coverageThresholds: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    },
    // Critical paths need higher coverage
    './src/lib/auth/**': {
      branches: 90,
      functions: 90,
      lines: 90
    }
  }
}
```

---

## Testing Strategies by Framework

### Next.js (React)

- Unit: Jest + React Testing Library
- Integration: Supertest (API routes)
- E2E: Playwright

### Express API

- Unit: Jest
- Integration: Supertest
- E2E: Playwright (if has UI)

### FastAPI (Python)

- Unit: pytest
- Integration: pytest + TestClient
- E2E: Playwright

---

## Common Testing Patterns

### Testing Async Code

```typescript
// Using async/await
it('fetches user data', async () => {
  const user = await fetchUser('123')
  expect(user.name).toBe('John')
})

// Using waitFor (React Testing Library)
it('shows loading then data', async () => {
  render(<UserProfile userId="123" />)

  expect(screen.getByText('Loading...')).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })
})
```

### Testing Error Handling

```typescript
it('handles errors gracefully', async () => {
  mockFetchUser.mockRejectedValue(new Error('Network error'))

  render(<UserProfile userId="123" />)

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument()
  })
})
```

### Testing Forms

```typescript
it('submits form with valid data', async () => {
  const handleSubmit = jest.fn()
  render(<LoginForm onSubmit={handleSubmit} />)

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com')
  await userEvent.type(screen.getByLabelText('Password'), 'password123')
  await userEvent.click(screen.getByRole('button', { name: 'Login' }))

  await waitFor(() => {
    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    })
  })
})
```

---

## Test Organization

### File Structure

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx         # Co-located with component
├── lib/
│   ├── utils.ts
│   └── utils.test.ts           # Co-located with module
└── __tests__/
    ├── integration/            # Integration tests
    │   └── api.test.ts
    └── e2e/                    # E2E tests
        └── checkout.spec.ts
```

### Naming Conventions

- Unit/Integration: `*.test.ts` or `*.spec.ts`
- E2E: `*.e2e.ts` or `*.spec.ts` (in tests/e2e/)
- Test names: `it('should do X when Y')` or `it('does X')`

---

## When to Use This Skill

Use testing-strategist skill when:

- ✅ Setting up testing for new project
- ✅ Choosing test frameworks
- ✅ Deciding what to test and at what level
- ✅ Implementing TDD
- ✅ Improving code coverage
- ✅ Fixing flaky tests

---

## Related Resources

**Skills:**

- `security-engineer` - Security testing
- `api-designer` - API testing strategies
- `frontend-builder` - React testing patterns

**Patterns:**

- `/STANDARDS/best-practices/testing-best-practices.md`
- `/TEMPLATES/testing/jest-nextjs-setup.md`
- `/TEMPLATES/testing/playwright-e2e-setup.md`

**External:**

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright](https://playwright.dev/)

---

**Good tests give you confidence to ship.** ✅
