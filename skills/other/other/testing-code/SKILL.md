---
name: Testing Code
description: Write automated tests for features, validate functionality against acceptance criteria, and ensure code coverage. Use when writing test code, verifying functionality, or adding test coverage to existing code.
---

# Testing Code

## Core Workflow

Test writing follows a systematic approach: determine scope, understand patterns, map to requirements, write tests, verify coverage.

### 1. Determine Test Scope

**Read project documentation:**
- `docs/user-stories/US-###-*.md` for acceptance criteria to test
- `docs/feature-spec/F-##-*.md` for technical requirements
- `docs/api-contracts.yaml` for API specifications
- Existing test files to understand patterns

**Choose test types needed:**
- **Unit tests:** Individual functions, pure logic, utilities
- **Integration tests:** Multiple components working together, API endpoints
- **Component tests:** UI components, user interactions
- **E2E tests:** Complete user flows, critical paths
- **Contract tests:** API request/response validation
- **Performance tests:** Load, stress, benchmark testing

### 2. Understand Existing Patterns

**Investigate current test approach:**
- Test framework (Jest, Vitest, Pytest, etc.)
- Mocking patterns and utilities
- Test data fixtures and setup/teardown
- Assertion styles

Use `code-finder` agents if unfamiliar with test structure.

### 3. Map Tests to Requirements

Convert 3-5 acceptance criteria to specific test cases across test types:

**Example mapping:**
```markdown
## User Story: US-101 User Login

### Test Cases
1. **Unit: Authentication service**
   - validateCredentials() returns true for valid email/password
   - validateCredentials() returns false for invalid password
   - checkAccountStatus() detects locked accounts

2. **Integration: Login endpoint**
   - POST /api/login with valid creds returns 200 + token
   - POST /api/login with invalid creds returns 401 + error
   - POST /api/login with locked account returns 403

3. **Component: Login form**
   - Submitting form calls login API
   - Error message displays on 401 response
   - Success redirects to /dashboard

4. **E2E: Complete login flow**
   - User enters credentials → submits → sees dashboard
   - User enters wrong password → sees error → retries successfully
```

### 4. Write Tests

**Unit Test Structure:**
```javascript
describe('AuthService', () => {
  describe('validateCredentials', () => {
    it('returns true for valid email and password', async () => {
      const result = await authService.validateCredentials(
        'user@example.com',
        'ValidPass123'
      );
      expect(result).toBe(true);
    });

    it('returns false for invalid password', async () => {
      const result = await authService.validateCredentials(
        'user@example.com',
        'WrongPassword'
      );
      expect(result).toBe(false);
    });
  });
});
```

**Integration Test Structure:**
```javascript
describe('POST /api/auth/login', () => {
  beforeEach(async () => {
    await resetTestDatabase();
    await createTestUser({
      email: 'test@example.com',
      password: 'Test123!'
    });
  });

  it('returns 200 and token for valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'Test123!' });

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('token');
    expect(response.body.token).toMatch(/^eyJ/); // JWT format
  });

  it('returns 401 for invalid password', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'WrongPassword' });

    expect(response.status).toBe(401);
    expect(response.body.error).toBe('Invalid credentials');
  });
});
```

**Component Test Structure:**
```javascript
describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const mockLogin = jest.fn().mockResolvedValue({ success: true });
    render(<LoginForm onLogin={mockLogin} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'Password123');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    expect(mockLogin).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'Password123'
    });
  });

  it('displays error message on API failure', async () => {
    const mockLogin = jest.fn().mockRejectedValue(new Error('Invalid credentials'));
    render(<LoginForm onLogin={mockLogin} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'wrong');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
  });
});
```

**E2E Test Structure:**
```javascript
test('user can log in successfully', async ({ page }) => {
  await page.goto('/login');

  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'Test123!');
  await page.click('button:has-text("Log In")');

  await page.waitForURL('/dashboard');
  expect(page.url()).toContain('/dashboard');
});
```

### 5. Edge Cases & Error Scenarios

Include boundary conditions and error paths:

```javascript
describe('Edge cases', () => {
  it('handles empty email gracefully', async () => {
    await expect(
      authService.validateCredentials('', 'password')
    ).rejects.toThrow('Email is required');
  });

  it('handles extremely long password', async () => {
    const longPassword = 'a'.repeat(10000);
    await expect(
      authService.validateCredentials('user@example.com', longPassword)
    ).rejects.toThrow('Password too long');
  });

  it('handles network timeout', async () => {
    jest.spyOn(global, 'fetch').mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 10000))
    );

    await expect(
      authService.login('user@example.com', 'pass')
    ).rejects.toThrow('Request timeout');
  });
});
```

**Edge cases to always include:**
- Empty/null inputs
- Minimum/maximum values
- Invalid formats
- Network failures
- API errors (4xx, 5xx)
- Timeout conditions
- Concurrent operations

### 6. Test Data & Fixtures

Create reusable test fixtures:

```javascript
// tests/fixtures/users.ts
export const validUser = {
  email: 'test@example.com',
  password: 'Test123!',
  name: 'Test User'
};

export const invalidUsers = {
  noEmail: { password: 'Test123!' },
  noPassword: { email: 'test@example.com' },
  invalidEmail: { email: 'not-an-email', password: 'Test123!' },
  weakPassword: { email: 'test@example.com', password: '123' }
};

// Use in tests
import { validUser, invalidUsers } from './fixtures/users';

it('validates user data', () => {
  expect(validate(validUser)).toBe(true);
  expect(validate(invalidUsers.noEmail)).toBe(false);
});
```

### 7. Parallel Test Implementation

When tests are independent (different modules, different test types), spawn parallel agents:

**Pattern 1: Layer-based**
- Agent 1: Unit tests for services/utilities
- Agent 2: Integration tests for API endpoints
- Agent 3: Component tests for UI
- Agent 4: E2E tests for critical flows

**Pattern 2: Feature-based**
- Agent 1: All tests for Feature A
- Agent 2: All tests for Feature B
- Agent 3: All tests for Feature C

**Pattern 3: Type-based**
- Agent 1: All unit tests
- Agent 2: All integration tests
- Agent 3: All E2E tests

### 8. Run & Verify Tests

**Execute test suite:**
```bash
# Unit tests
npm test -- --coverage

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# All tests
npm run test:all
```

**Verify coverage:**
- Aim for >80% code coverage
- 100% coverage of critical paths
- All acceptance criteria have tests
- All error scenarios tested

## Quality Checklist

**Coverage:**
- [ ] All acceptance criteria from user stories tested
- [ ] Happy path covered
- [ ] Edge cases included
- [ ] Error scenarios tested
- [ ] Boundary conditions validated

**Structure:**
- [ ] Tests follow existing patterns
- [ ] Clear test descriptions
- [ ] Proper setup/teardown
- [ ] No flaky tests (consistent results)
- [ ] Tests are isolated (no interdependencies)

**Data:**
- [ ] Test fixtures reusable
- [ ] Database properly seeded/reset
- [ ] Mocks used appropriately
- [ ] No hardcoded test data in production

**Integration:**
- [ ] Tests run in CI/CD
- [ ] Coverage thresholds enforced
- [ ] Fast feedback (quick tests)
- [ ] Clear failure messages
