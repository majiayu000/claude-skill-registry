---
name: testing-builder
description: Automatically generates comprehensive test suites (unit, integration, E2E) based on code and past testing patterns. Use when user says "write tests", "test this", "add coverage", or after fixing bugs to create regression tests. Eliminates testing friction for ADHD users.
---

# Testing Builder

## Purpose

Automatic test generation that learns your testing style. Eliminates the ADHD barrier to testing by making it effortless:
1. Analyzes code to understand what needs testing
2. Recalls your testing patterns from memory
3. Generates comprehensive test suite
4. Ensures all edge cases covered
5. Saves testing patterns for future

**For ADHD users**: Zero friction - tests created instantly without manual effort.
**For all users**: Comprehensive coverage without the tedious work.
**Learning system**: Gets better at matching your testing style over time.

## Activation Triggers

- User says: "write tests", "test this", "add tests", "coverage"
- After fixing bug: "create regression test"
- Code review: "needs tests"
- User mentions: "unit test", "integration test", "E2E test"

## Core Workflow

### 1. Analyze Code

**Step 1**: Identify what to test

```javascript
// Example: Analyzing a function
function calculateDiscount(price, discountPercent, customerType) {
  if (customerType === 'premium') {
    discountPercent += 10;
  }
  return price * (1 - discountPercent / 100);
}

// Identify:
- Function name: calculateDiscount
- Parameters: price, discountPercent, customerType
- Logic branches: premium vs non-premium
- Edge cases: negative values, zero, boundary conditions
- Return type: number
```

**Step 2**: Determine test type needed

- **Unit test**: Pure functions, utilities, components
- **Integration test**: Multiple components working together, API endpoints
- **E2E test**: Full user workflows, critical paths
- **Regression test**: Specific bug that was fixed

### 2. Recall Testing Patterns

Query context-manager for:

```
search memories:
- Type: PREFERENCE, PROCEDURE
- Tags: testing, test-framework, test-style
- Project: current project
```

**What to recall**:
- Test framework (Jest, Vitest, Pytest, etc.)
- Assertion style (expect, assert, should)
- Test structure (describe/it, test blocks)
- Mocking patterns (jest.mock, vi.mock)
- Coverage requirements
- File naming conventions

**Example memory**:
```
PREFERENCE: Testing style for BOOSTBOX
- Framework: Vitest
- Assertion: expect()
- Structure: describe/it blocks
- Coverage: Minimum 80%
- File naming: {filename}.test.js
```

### 3. Generate Test Suite

**Unit Test Template**:

```javascript
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './discount';

describe('calculateDiscount', () => {
  describe('basic calculations', () => {
    it('should calculate discount correctly for regular customers', () => {
      const result = calculateDiscount(100, 10, 'regular');
      expect(result).toBe(90);
    });

    it('should add bonus discount for premium customers', () => {
      const result = calculateDiscount(100, 10, 'premium');
      expect(result).toBe(80); // 10% + 10% bonus
    });
  });

  describe('edge cases', () => {
    it('should handle zero discount', () => {
      const result = calculateDiscount(100, 0, 'regular');
      expect(result).toBe(100);
    });

    it('should handle 100% discount', () => {
      const result = calculateDiscount(100, 100, 'regular');
      expect(result).toBe(0);
    });

    it('should handle zero price', () => {
      const result = calculateDiscount(0, 10, 'regular');
      expect(result).toBe(0);
    });
  });

  describe('invalid inputs', () => {
    it('should handle negative price', () => {
      const result = calculateDiscount(-100, 10, 'regular');
      expect(result).toBeLessThan(0);
    });

    it('should handle invalid customer type', () => {
      const result = calculateDiscount(100, 10, 'unknown');
      expect(result).toBe(90); // Falls back to regular
    });
  });
});
```

**Integration Test Template** (API endpoint):

```javascript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from './app';
import { db } from './db';

describe('POST /api/users', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('test@example.com');
  });

  it('should reject duplicate email', async () => {
    await request(app).post('/api/users').send({
      email: 'duplicate@example.com',
      name: 'User 1'
    });

    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'duplicate@example.com',
        name: 'User 2'
      });

    expect(response.status).toBe(409);
    expect(response.body.error).toContain('already exists');
  });

  it('should validate required fields', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'No Email'
      });

    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });
});
```

**E2E Test Template** (Playwright):

```javascript
import { test, expect } from '@playwright/test';

test.describe('User Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.welcome-message')).toContainText('Welcome');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText('Invalid');
    await expect(page).toHaveURL('/login');
  });

  test('should validate required fields', async ({ page }) => {
    await page.goto('/login');

    await page.click('button[type="submit"]');

    await expect(page.locator('[name="email"]:invalid')).toBeVisible();
    await expect(page.locator('[name="password"]:invalid')).toBeVisible();
  });
});
```

### 4. Coverage Analysis

**Check what's tested**:

```javascript
// Coverage requirements (from memory or defaults)
const requirements = {
  statements: 80,
  branches: 75,
  functions: 90,
  lines: 80
};

// Identify untested scenarios
const missing = [
  'Error handling for network failures',
  'Loading state transitions',
  'Concurrent operations',
  'Cleanup on unmount'
];

// Generate additional tests for missing coverage
```

### 5. Save Testing Patterns

After generating tests:

```bash
# Save testing style to memory
remember: Testing pattern for authentication
Type: PROCEDURE
Tags: testing, authentication, integration
Content: For auth endpoints, always test:
- Valid credentials → success
- Invalid credentials → 401
- Missing fields → 400
- Expired token → 401
- Token refresh flow
```

## Framework-Specific Patterns

### Jest/Vitest (JavaScript/TypeScript)

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should do something', () => {
    expect(result).toBe(expected);
  });
});
```

**Mocking**:
```javascript
// Mock module
vi.mock('./api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: [] }))
}));

// Mock implementation
const mockFn = vi.fn().mockImplementation(() => 'value');
```

### Pytest (Python)

```python
import pytest
from mymodule import calculate_discount

class TestCalculateDiscount:
    def test_regular_customer(self):
        result = calculate_discount(100, 10, 'regular')
        assert result == 90

    def test_premium_customer(self):
        result = calculate_discount(100, 10, 'premium')
        assert result == 80

    @pytest.mark.parametrize("price,discount,expected", [
        (100, 0, 100),
        (100, 100, 0),
        (0, 10, 0),
    ])
    def test_edge_cases(self, price, discount, expected):
        result = calculate_discount(price, discount, 'regular')
        assert result == expected
```

**Fixtures**:
```python
@pytest.fixture
def sample_user():
    return {
        'id': 1,
        'email': 'test@example.com',
        'name': 'Test User'
    }

def test_user_creation(sample_user):
    assert sample_user['email'] == 'test@example.com'
```

### React Testing Library

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { expect, test } from 'vitest';
import { UserList } from './UserList';

test('renders user list', () => {
  const users = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ];

  render(<UserList users={users} />);

  expect(screen.getByText('Alice')).toBeInTheDocument();
  expect(screen.getByText('Bob')).toBeInTheDocument();
});

test('handles empty user list', () => {
  render(<UserList users={[]} />);

  expect(screen.getByText('No users found')).toBeInTheDocument();
});

test('handles user click', () => {
  const handleClick = vi.fn();
  const users = [{ id: 1, name: 'Alice' }];

  render(<UserList users={users} onUserClick={handleClick} />);

  fireEvent.click(screen.getByText('Alice'));

  expect(handleClick).toHaveBeenCalledWith(users[0]);
});
```

## Test Categories

### Unit Tests

**What to test**:
- Pure functions
- Utility functions
- Component logic
- Class methods

**Focus on**:
- Input/output correctness
- Edge cases
- Error conditions
- Boundary values

### Integration Tests

**What to test**:
- API endpoints
- Database operations
- Multiple components together
- External service integration

**Focus on**:
- Component interactions
- Data flow
- Error propagation
- Transaction handling

### E2E Tests

**What to test**:
- Critical user flows
- Complete features
- Multi-step processes
- Cross-page workflows

**Focus on**:
- User perspective
- Real browser interaction
- Full stack integration
- Production-like environment

### Regression Tests

**When to create**:
- After fixing a bug
- Preventing known issues
- Historical problems

**Structure**:
```javascript
describe('Regression: Bug #123 - User map undefined', () => {
  it('should handle undefined users array', () => {
    // Test that previously failed
    const result = renderUserList(undefined);
    expect(result).not.toThrow();
  });
});
```

## Context Integration

### Recall Testing Preferences

Before generating tests:

```javascript
// Query context-manager
const preferences = searchMemories({
  type: 'PREFERENCE',
  tags: ['testing', project],
  recent: true
});

// Apply preferences
const testConfig = {
  framework: preferences.framework || 'vitest',
  style: preferences.style || 'describe/it',
  coverage: preferences.coverage || 80,
  naming: preferences.naming || '{name}.test.js'
};
```

### Save Testing Patterns

After generating tests:

```bash
remember: Testing pattern for API endpoints
Type: PROCEDURE
Tags: testing, api, integration
Content: For API endpoints, always include:
1. Happy path (200/201)
2. Validation errors (400)
3. Auth errors (401/403)
4. Not found (404)
5. Server errors (500)
6. Rate limiting (429)
```

### Learn from Feedback

If user modifies generated tests:

```javascript
// Analyze what user changed
const changes = diff(generatedTest, userModifiedTest);

// Save as new pattern if significant
if (changes.significant) {
  saveMemory({
    type: 'PREFERENCE',
    content: `User prefers ${changes.pattern}`,
    tags: ['testing', 'user-preference']
  });
}
```

## Integration with Other Skills

### Error Debugger

When error-debugger fixes a bug:
```
Automatically invoke testing-builder
Create regression test for: {bug_scenario}
Ensure test fails before fix, passes after
```

### Context Manager

Load testing preferences:
```
Query for PREFERENCE with tags: [testing, test-framework]
Apply framework, style, coverage preferences
```

Save new patterns:
```
After generating tests for new scenario
Save pattern as PROCEDURE for future reference
```

### Code Quality Auditor

Check test quality:
```
After generating tests:
→ Invoke code-quality-auditor
→ Verify test coverage
→ Check for test smells
→ Ensure meaningful assertions
```

## Quick Reference

### Test Generation Checklist

✅ Happy path covered
✅ Edge cases tested
✅ Error conditions handled
✅ Invalid inputs validated
✅ Boundary values checked
✅ Async operations handled
✅ Mocks properly configured
✅ Cleanup properly done
✅ Assertions are meaningful

### Common Test Patterns

| Scenario | Pattern |
|----------|---------|
| Function | Input → Output assertions |
| Component | Render → Query → Assert |
| API | Request → Response → Assert |
| Async | await → Promise → Result |
| Error | Try/catch → Error assertion |
| Mock | Setup → Call → Verify mock |

### Trigger Phrases

- "write tests"
- "test this"
- "add coverage"
- "create regression test"
- "needs tests"

### File Locations

- **Test patterns**: `/home/toowired/.claude-memories/procedures/` (tagged "testing")
- **Test preferences**: `/home/toowired/.claude-memories/preferences/` (tagged "testing")
- **Generated tests**: `{filename}.test.{ext}` or `tests/{filename}.test.{ext}`

### Success Criteria

✅ Tests generated in <30 seconds
✅ Comprehensive coverage (80%+ by default)
✅ All edge cases included
✅ Tests follow project style
✅ Zero manual effort required
✅ Testing patterns saved for future
