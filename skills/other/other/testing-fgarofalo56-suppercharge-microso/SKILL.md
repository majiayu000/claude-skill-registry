---
name: testing
description: Comprehensive testing skill covering unit, integration, and E2E testing with pytest, Jest, Cypress, and Playwright. Use for writing tests, improving coverage, debugging test failures, and setting up testing infrastructure.
---

# Testing Skill

Expert guidance for software testing across multiple frameworks and testing types.

## Covered Frameworks

| Framework | Type | Language | Use For |
|-----------|------|----------|---------|
| **pytest** | Unit/Integration | Python | Python backend testing |
| **Jest** | Unit/Integration | JavaScript/TypeScript | React, Node.js testing |
| **Cypress** | E2E | JavaScript | Frontend E2E testing |
| **Playwright** | E2E | Multi-language | Cross-browser E2E testing |

## Testing Principles

### AAA Pattern (Arrange-Act-Assert)

```python
# Python (pytest)
def test_user_creation():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # Act
    user = create_user(user_data)

    # Assert
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

```typescript
// TypeScript (Jest)
describe('UserService', () => {
  it('should create user with valid data', () => {
    // Arrange
    const userData = { name: 'Alice', email: 'alice@example.com' };

    // Act
    const user = createUser(userData);

    // Assert
    expect(user.name).toBe('Alice');
    expect(user.email).toBe('alice@example.com');
  });
});
```

### Test Types

| Type | Scope | Speed | When to Use |
|------|-------|-------|-------------|
| **Unit** | Single function/class | Fast | Business logic, utilities |
| **Integration** | Multiple components | Medium | API endpoints, database ops |
| **E2E** | Full user flow | Slow | Critical user journeys |

### Coverage Targets

| Type | Target | Priority |
|------|--------|----------|
| Unit | 80%+ | High |
| Integration | Critical paths | Medium |
| E2E | Happy paths | Medium |

## pytest (Python)

### Basic Test

```python
import pytest

def test_addition():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError):
        int("not a number")
```

### Fixtures

```python
import pytest

@pytest.fixture
def user():
    return User(name="Test User", email="test@example.com")

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()

def test_user_save(db_session, user):
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
])
def test_string_length(input, expected):
    assert len(input) == expected
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data()
    assert result is not None
```

### Mocking

```python
from unittest.mock import Mock, patch

def test_external_api():
    with patch('module.external_api') as mock_api:
        mock_api.return_value = {"status": "ok"}
        result = call_external_api()
        assert result["status"] == "ok"
```

## Jest (JavaScript/TypeScript)

### Basic Test

```typescript
describe('Math', () => {
  it('should add numbers', () => {
    expect(1 + 1).toBe(2);
  });

  it('should throw on invalid input', () => {
    expect(() => throwingFunction()).toThrow('Error message');
  });
});
```

### Mocking

```typescript
jest.mock('./api');

import { fetchUser } from './api';

const mockFetchUser = fetchUser as jest.MockedFunction<typeof fetchUser>;

beforeEach(() => {
  mockFetchUser.mockResolvedValue({ id: 1, name: 'Test' });
});

it('should fetch user', async () => {
  const user = await getUser(1);
  expect(user.name).toBe('Test');
});
```

### React Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

it('should render button and handle click', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  fireEvent.click(screen.getByRole('button'));

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

## Cypress (E2E)

### Basic Test

```javascript
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login with valid credentials', () => {
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();

    cy.url().should('include', '/dashboard');
    cy.contains('Welcome').should('be.visible');
  });
});
```

### API Testing

```javascript
it('should create user via API', () => {
  cy.request('POST', '/api/users', {
    name: 'Test User',
    email: 'test@example.com'
  }).then((response) => {
    expect(response.status).to.eq(201);
    expect(response.body).to.have.property('id');
  });
});
```

## Playwright (Cross-browser E2E)

### Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('should navigate and login', async ({ page }) => {
  await page.goto('/login');

  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="submit"]');

  await expect(page).toHaveURL(/dashboard/);
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

### API Testing

```typescript
import { test, expect } from '@playwright/test';

test('should create user via API', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'Test', email: 'test@example.com' }
  });

  expect(response.ok()).toBeTruthy();
  expect(await response.json()).toHaveProperty('id');
});
```

## Best Practices

1. **Test behavior, not implementation** - Tests should verify what code does, not how
2. **One assertion per test** (when practical) - Makes failures clear
3. **Use descriptive test names** - "should return user when valid ID provided"
4. **Keep tests independent** - No test should depend on another
5. **Mock external dependencies** - Tests should be deterministic
6. **Use test data builders** - Create consistent test data
7. **Clean up after tests** - Reset state, close connections

## Running Tests

```bash
# pytest
pytest                          # Run all
pytest tests/test_user.py       # Run file
pytest -k "test_login"          # Run by name pattern
pytest --cov=src                # With coverage

# Jest
npm test                        # Run all
npm test -- --watch             # Watch mode
npm test -- --coverage          # With coverage

# Cypress
npx cypress run                 # Headless
npx cypress open                # Interactive

# Playwright
npx playwright test             # Run all
npx playwright test --ui        # Interactive UI
npx playwright test --debug     # Debug mode
```

## See Also

- `testing/pytest-advanced/` - Advanced pytest patterns
- `testing/jest/` - Jest-specific guidance
- `testing/cypress/` - Cypress patterns and recipes
