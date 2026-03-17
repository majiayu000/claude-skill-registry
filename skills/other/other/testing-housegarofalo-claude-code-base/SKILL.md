---
name: testing
description: Comprehensive testing skill covering unit, integration, and E2E testing with pytest, Jest, Cypress, and Playwright. Use for writing tests, improving coverage, debugging test failures, and setting up testing infrastructure.
---

# Testing Skill

Expert guidance for software testing across multiple frameworks and testing types.

## Covered Frameworks

| Framework      | Type             | Language              | Use For                       |
|----------------|------------------|----------------------|-------------------------------|
| **pytest**     | Unit/Integration | Python               | Python backend testing        |
| **Jest**       | Unit/Integration | JavaScript/TypeScript| React, Node.js testing        |
| **Cypress**    | E2E              | JavaScript           | Frontend E2E testing          |
| **Playwright** | E2E              | Multi-language       | Cross-browser E2E testing     |

---

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

| Type            | Scope                 | Speed  | When to Use               |
|-----------------|-----------------------|--------|---------------------------|
| **Unit**        | Single function/class | Fast   | Business logic, utilities |
| **Integration** | Multiple components   | Medium | API endpoints, database ops |
| **E2E**         | Full user flow        | Slow   | Critical user journeys    |

### Coverage Targets

| Type        | Target         | Priority |
|-------------|----------------|----------|
| Unit        | 80%+           | High     |
| Integration | Critical paths | Medium   |
| E2E         | Happy paths    | Medium   |

---

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

### Conftest for Shared Fixtures

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    from app import create_app
    app = create_app(db_session)
    return app.test_client()
```

---

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

### React Testing Library

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('should render button and handle click', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  fireEvent.click(screen.getByRole('button'));

  expect(handleClick).toHaveBeenCalledTimes(1);
});

it('should handle user input', async () => {
  const user = userEvent.setup();
  render(<LoginForm onSubmit={mockSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
```

### Async Testing

```typescript
it('should fetch data asynchronously', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

it('should resolve promise', async () => {
  await expect(asyncFunction()).resolves.toBe('expected value');
});

it('should reject promise', async () => {
  await expect(asyncFunction()).rejects.toThrow('error message');
});
```

### Setup and Teardown

```typescript
describe('Database Tests', () => {
  beforeAll(async () => {
    await setupDatabase();
  });

  afterAll(async () => {
    await teardownDatabase();
  });

  beforeEach(async () => {
    await clearTables();
  });

  it('should insert record', async () => {
    // Test code
  });
});
```

---

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

  it('should show error for invalid credentials', () => {
    cy.get('[data-testid="email"]').type('wrong@example.com');
    cy.get('[data-testid="password"]').type('wrongpassword');
    cy.get('[data-testid="submit"]').click();

    cy.contains('Invalid credentials').should('be.visible');
    cy.url().should('include', '/login');
  });
});
```

### Custom Commands

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="submit"]').click();
  cy.url().should('include', '/dashboard');
});

// Usage in tests
it('should access protected route', () => {
  cy.login('user@example.com', 'password123');
  cy.visit('/protected');
  cy.contains('Protected Content').should('be.visible');
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

// Intercept and mock API calls
it('should handle API error gracefully', () => {
  cy.intercept('GET', '/api/users', {
    statusCode: 500,
    body: { error: 'Internal Server Error' }
  }).as('getUsers');

  cy.visit('/users');
  cy.wait('@getUsers');
  cy.contains('Failed to load users').should('be.visible');
});
```

### Fixtures

```javascript
// cypress/fixtures/user.json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com"
}

// In test
it('should display user data', () => {
  cy.fixture('user').then((user) => {
    cy.intercept('GET', '/api/user/1', user).as('getUser');
    cy.visit('/user/1');
    cy.wait('@getUser');
    cy.contains(user.name).should('be.visible');
  });
});
```

---

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

### Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="submit"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// In test
test('should login successfully', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL(/dashboard/);
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

### Visual Testing

```typescript
test('should match snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});

test('should match element snapshot', async ({ page }) => {
  await page.goto('/');
  const header = page.locator('header');
  await expect(header).toHaveScreenshot('header.png');
});
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
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
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Best Practices

1. **Test behavior, not implementation** - Tests should verify what code does, not how
2. **One assertion per test** (when practical) - Makes failures clear
3. **Use descriptive test names** - "should return user when valid ID provided"
4. **Keep tests independent** - No test should depend on another
5. **Mock external dependencies** - Tests should be deterministic
6. **Use test data builders** - Create consistent test data
7. **Clean up after tests** - Reset state, close connections
8. **Test edge cases** - Empty inputs, nulls, boundaries
9. **Use data-testid attributes** - Stable selectors for E2E tests
10. **Run tests in CI/CD** - Catch regressions early

---

## Running Tests

```bash
# pytest
pytest                          # Run all
pytest tests/test_user.py       # Run file
pytest -k "test_login"          # Run by name pattern
pytest --cov=src                # With coverage
pytest -x                       # Stop on first failure
pytest -v                       # Verbose output

# Jest
npm test                        # Run all
npm test -- --watch             # Watch mode
npm test -- --coverage          # With coverage
npm test -- --testPathPattern="user"  # Run specific tests

# Cypress
npx cypress run                 # Headless
npx cypress open                # Interactive
npx cypress run --spec "cypress/e2e/login.cy.js"  # Specific file

# Playwright
npx playwright test             # Run all
npx playwright test --ui        # Interactive UI
npx playwright test --debug     # Debug mode
npx playwright test --project=chromium  # Specific browser
npx playwright show-report      # View HTML report
```

---

## Test Coverage Tools

| Language   | Tool              | Command                    |
|------------|-------------------|----------------------------|
| Python     | pytest-cov        | `pytest --cov=src`         |
| JavaScript | Jest              | `jest --coverage`          |
| TypeScript | Jest/c8           | `jest --coverage`          |
| E2E        | Playwright        | Built-in with `--coverage` |

### Coverage Thresholds

```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```
