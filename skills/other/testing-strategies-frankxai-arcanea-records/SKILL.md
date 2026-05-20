---
name: Testing Strategies
description: Comprehensive testing approaches for reliable software
version: 1.0.0
license: MIT
tier: community
---

# Testing Strategies

> **Write tests that catch bugs, not tests that waste time**

This skill provides strategies for effective testing at all levels, from unit to end-to-end.

## Core Principles

### 1. Tests Are Documentation
Good tests explain what the code should do. They're living documentation that can't go stale.

### 2. Test Behavior, Not Implementation
Tests should verify outcomes, not internal details. Implementation can change; behavior shouldn't.

### 3. Fast Feedback Loops
Most tests should run in seconds, not minutes. Save slow tests for CI.

## The Testing Pyramid

```
                         ╱╲
                        ╱  ╲
                       ╱E2E ╲     5-10%
                      ╱──────╲
                     ╱        ╲
                    ╱  Integr- ╲  15-25%
                   ╱   ation    ╲
                  ╱──────────────╲
                 ╱                ╲
                ╱       Unit       ╲  65-80%
               ╱────────────────────╲
```

**Why this distribution:**
- Unit tests are fast, cheap, and precise
- Integration tests catch interface issues
- E2E tests verify critical user journeys

## Unit Testing

### What to Unit Test

```yaml
Always Test:
  - Pure functions with logic
  - State machines
  - Parsers and transformers
  - Validation logic
  - Calculations
  - Data formatting

Skip:
  - Simple getters/setters
  - Direct pass-through functions
  - Framework internals
  - Third-party library code
```

### Unit Test Structure (AAA Pattern)

```javascript
describe('calculateTotal', () => {
  it('calculates total with tax', () => {
    // Arrange - set up test data
    const items = [
      { price: 100, quantity: 2 },
      { price: 50, quantity: 1 }
    ];
    const taxRate = 0.1;

    // Act - perform the action
    const result = calculateTotal(items, taxRate);

    // Assert - verify the outcome
    expect(result).toBe(275); // (200 + 50) * 1.1
  });
});
```

### Test Case Design

```yaml
Coverage Strategy:

  Happy Path:
    - Normal, expected inputs
    - Typical use cases

  Edge Cases:
    - Empty inputs ([], null, undefined)
    - Single item (boundary)
    - Maximum values
    - Minimum values

  Error Cases:
    - Invalid inputs
    - Missing required data
    - Out of range values
    - Type mismatches

  Boundary Conditions:
    - Off-by-one scenarios
    - Exact boundaries
    - Just over/under limits
```

### Example: Comprehensive Unit Tests

```javascript
describe('UserValidator', () => {
  describe('validateEmail', () => {
    // Happy path
    it('accepts valid email', () => {
      expect(validateEmail('user@example.com')).toBe(true);
    });

    // Variations of valid
    it('accepts email with subdomain', () => {
      expect(validateEmail('user@mail.example.com')).toBe(true);
    });

    it('accepts email with plus sign', () => {
      expect(validateEmail('user+tag@example.com')).toBe(true);
    });

    // Edge cases
    it('rejects empty string', () => {
      expect(validateEmail('')).toBe(false);
    });

    it('rejects null', () => {
      expect(validateEmail(null)).toBe(false);
    });

    // Invalid formats
    it('rejects email without @', () => {
      expect(validateEmail('userexample.com')).toBe(false);
    });

    it('rejects email without domain', () => {
      expect(validateEmail('user@')).toBe(false);
    });

    it('rejects email with spaces', () => {
      expect(validateEmail('user @example.com')).toBe(false);
    });
  });
});
```

### Mocking Strategy

```javascript
// Mock external dependencies, not internal code
describe('UserService', () => {
  // Mock the database client (external)
  const mockDb = {
    users: {
      findById: jest.fn(),
      update: jest.fn()
    }
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('updates user name', async () => {
    // Arrange
    mockDb.users.findById.mockResolvedValue({
      id: '123',
      name: 'Old Name'
    });
    mockDb.users.update.mockResolvedValue({
      id: '123',
      name: 'New Name'
    });

    const service = new UserService(mockDb);

    // Act
    const result = await service.updateName('123', 'New Name');

    // Assert
    expect(mockDb.users.update).toHaveBeenCalledWith('123', {
      name: 'New Name'
    });
    expect(result.name).toBe('New Name');
  });
});
```

## Integration Testing

### What to Integration Test

```yaml
Focus Areas:
  - API endpoints (request → response)
  - Database operations (CRUD)
  - Service-to-service calls
  - Authentication flows
  - External integrations (with mocks)
```

### API Integration Test Pattern

```javascript
describe('POST /api/users', () => {
  beforeAll(async () => {
    // Setup test database
    await setupTestDatabase();
  });

  afterAll(async () => {
    // Cleanup
    await teardownTestDatabase();
  });

  afterEach(async () => {
    // Reset between tests
    await clearUsers();
  });

  it('creates a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body).toMatchObject({
      email: 'test@example.com',
      name: 'Test User'
    });
    expect(response.body.id).toBeDefined();
  });

  it('validates required fields', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({});

    expect(response.status).toBe(400);
    expect(response.body.errors).toContain('email is required');
  });

  it('prevents duplicate emails', async () => {
    // Create first user
    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'First' });

    // Try duplicate
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Second' });

    expect(response.status).toBe(409);
  });
});
```

### Database Integration Testing

```javascript
describe('UserRepository', () => {
  let testDb;

  beforeAll(async () => {
    testDb = await createTestDatabase();
  });

  afterAll(async () => {
    await testDb.close();
  });

  beforeEach(async () => {
    await testDb.truncate('users');
  });

  it('creates and retrieves user', async () => {
    const repo = new UserRepository(testDb);

    // Create
    const created = await repo.create({
      email: 'test@example.com',
      name: 'Test User'
    });

    // Retrieve
    const retrieved = await repo.findById(created.id);

    expect(retrieved).toMatchObject({
      email: 'test@example.com',
      name: 'Test User'
    });
  });

  it('handles not found', async () => {
    const repo = new UserRepository(testDb);
    const result = await repo.findById('non-existent-id');
    expect(result).toBeNull();
  });
});
```

## End-to-End Testing

### What to E2E Test

```yaml
Test These Flows:
  - Critical user journeys (signup, purchase, etc.)
  - Revenue-impacting paths
  - Frequently reported bug areas
  - Complex multi-step workflows

Don't E2E Test:
  - Every permutation
  - Edge cases (use unit tests)
  - Visual styling
  - Performance (use dedicated tools)
```

### Playwright E2E Pattern

```javascript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('user can sign up and log in', async ({ page }) => {
    const email = `test-${Date.now()}@example.com`;

    // Navigate to signup
    await page.goto('/signup');

    // Fill signup form
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', 'SecurePass123!');
    await page.fill('[data-testid="confirm-password"]', 'SecurePass123!');

    // Submit
    await page.click('[data-testid="signup-button"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome');

    // Log out
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/');

    // Log back in
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', 'SecurePass123!');
    await page.click('[data-testid="login-button"]');

    // Verify successful login
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### E2E Test Selectors

```yaml
Selector Priority (best to worst):
  1. data-testid: '[data-testid="submit-button"]'
     - Explicit, decoupled from styling
     - Won't break with CSS changes

  2. Role: 'button:has-text("Submit")'
     - Accessibility-based
     - Good for semantic elements

  3. Text: 'text=Submit'
     - Human readable
     - Can break with copy changes

  4. CSS Class: '.submit-btn'
     - Couples tests to styling
     - Avoid if possible
```

## Component Testing (React)

### Testing Library Pattern

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('submits form with credentials', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    // Fill form using accessible queries
    await userEvent.type(
      screen.getByLabelText(/email/i),
      'user@example.com'
    );
    await userEvent.type(
      screen.getByLabelText(/password/i),
      'password123'
    );

    // Submit
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    // Verify
    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'password123'
    });
  });

  it('shows validation errors', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    // Submit without filling form
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    // Verify errors shown
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('disables submit while loading', () => {
    render(<LoginForm onSubmit={mockOnSubmit} isLoading />);

    expect(screen.getByRole('button', { name: /signing in/i })).toBeDisabled();
  });
});
```

### Query Priority for Testing Library

```yaml
Priority (most to least preferred):

  1. getByRole: Accessible roles (button, textbox, etc.)
  2. getByLabelText: Form elements by label
  3. getByPlaceholderText: When label not available
  4. getByText: Non-interactive elements
  5. getByDisplayValue: Current value of form element
  6. getByAltText: Images
  7. getByTitle: Title attribute
  8. getByTestId: Last resort, data-testid attribute
```

## Test Data Management

### Test Data Strategies

```yaml
Strategies:

  Inline Data:
    When: Simple, few tests
    How: Define in test file
    Pro: Visible, explicit
    Con: Can clutter tests

  Factories:
    When: Multiple tests need similar data
    How: Factory functions that generate data
    Pro: Reusable, consistent
    Con: Extra abstraction

  Fixtures:
    When: Complex, realistic data needed
    How: JSON/YAML files loaded by tests
    Pro: Realistic, shareable
    Con: Can become stale

  Seeded Database:
    When: Integration/E2E tests
    How: Migration scripts for test data
    Pro: Real database state
    Con: Slower, more complex
```

### Factory Pattern Example

```javascript
// test/factories/user.factory.js
export function createUser(overrides = {}) {
  return {
    id: `user-${Date.now()}`,
    email: `test-${Date.now()}@example.com`,
    name: 'Test User',
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides
  };
}

export function createUsers(count, overrides = {}) {
  return Array.from({ length: count }, (_, i) =>
    createUser({ ...overrides, name: `Test User ${i + 1}` })
  );
}

// Usage in tests
describe('UserList', () => {
  it('displays users', () => {
    const users = createUsers(3);
    render(<UserList users={users} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });
});
```

## Test Organization

### File Structure

```
src/
├── components/
│   └── Button/
│       ├── Button.tsx
│       ├── Button.test.tsx     # Unit tests
│       └── index.ts
├── services/
│   └── user/
│       ├── userService.ts
│       └── userService.test.ts # Unit tests
tests/
├── integration/
│   └── api/
│       └── users.test.ts       # API integration tests
├── e2e/
│   └── auth.spec.ts            # E2E tests
├── factories/
│   └── user.factory.ts         # Test factories
└── setup/
    └── testDatabase.ts         # Test utilities
```

### Naming Conventions

```yaml
Unit Tests:
  File: ComponentName.test.ts
  Describe: 'ComponentName'
  It: 'does specific thing'

Integration Tests:
  File: feature.test.ts
  Describe: 'POST /api/endpoint'
  It: 'returns 201 when valid'

E2E Tests:
  File: feature.spec.ts
  Describe: 'Feature Name Flow'
  Test: 'user can complete flow'
```

## Continuous Integration

### Test Pipeline Structure

```yaml
name: Test

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: codecov/codecov-action@v3

  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install
      - run: npm run build
      - run: npm run test:e2e
```

### Test Coverage Targets

```yaml
Coverage Guidelines:

  Overall: Aim for 70-80%
    - 100% is often counterproductive
    - Focus on meaningful coverage

  Critical Paths: 90%+
    - Payment processing
    - Authentication
    - Data validation

  UI Components: 60-70%
    - Business logic: High
    - Rendering: Medium
    - Styling: Low

  Utilities: 90%+
    - Pure functions should be well tested
```

## Debugging Failing Tests

### Common Issues & Solutions

```yaml
Flaky Tests:
  Symptoms:
    - Pass sometimes, fail others
    - Fail in CI, pass locally

  Causes:
    - Timing issues (async not awaited)
    - Shared state between tests
    - External dependencies

  Solutions:
    - Use proper async/await
    - Reset state in beforeEach
    - Mock external services

Slow Tests:
  Symptoms:
    - Test suite takes minutes
    - Developers skip running tests

  Causes:
    - Too many E2E tests
    - No parallel execution
    - Heavy setup/teardown

  Solutions:
    - Move tests down the pyramid
    - Run tests in parallel
    - Optimize fixtures

False Positives:
  Symptoms:
    - Tests pass but bugs exist
    - Tests don't catch regressions

  Causes:
    - Testing implementation not behavior
    - Missing edge cases
    - Over-mocking

  Solutions:
    - Test from user perspective
    - Add edge case tests
    - Use real implementations where possible
```

## Quality Checklist

### Before Merging

- [ ] All tests pass locally
- [ ] New code has test coverage
- [ ] No skipped tests without reason
- [ ] Test descriptions are clear
- [ ] No flaky tests introduced
- [ ] Coverage hasn't decreased

---

*"A test suite is like a fire alarm. You want it sensitive enough to catch problems, but not so sensitive that you ignore it."*
