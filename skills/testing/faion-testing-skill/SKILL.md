---
name: faion-testing-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(pytest:*, jest:*, vitest:*, go test:*, npx playwright:*, npx cypress:*, coverage:*)
---

# Testing Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Provides comprehensive testing patterns across languages and frameworks. This technical skill (Layer 3) is used by `faion-test-agent` to implement testing strategies.

## 3-Layer Architecture

```
Layer 1: Domain Skills ─ orchestrators
    ↓ call
Layer 2: Agents (faion-test-agent) ─ executors
    ↓ use
Layer 3: Technical Skills (this) ─ tools
```

---

# Section 1: pytest (Python)

## Overview

pytest is the most popular Python testing framework. Powerful fixtures, parametrization, and plugin ecosystem.

## Installation

```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-xdist
```

## Project Structure

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── services.py
│       └── models.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_services.py
│   │   └── test_models.py
│   ├── integration/
│   │   └── test_api.py
│   └── e2e/
│       └── test_workflows.py
└── pyproject.toml
```

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "-ra",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "e2e: marks end-to-end tests",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning",
]
asyncio_mode = "auto"

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 80
```

## Test Naming Convention

```python
# Pattern: test_{what}_{when}_{expected}
def test_user_create_with_valid_data_returns_user():
    pass

def test_user_create_with_invalid_email_raises_validation_error():
    pass

def test_order_total_with_discount_calculates_correctly():
    pass
```

## Basic Test Structure (Arrange-Act-Assert)

```python
import pytest
from myapp.services import UserService

class TestUserService:
    """Test suite for UserService."""

    def test_create_user_with_valid_data(self):
        # Arrange
        service = UserService()
        user_data = {"name": "John", "email": "john@example.com"}

        # Act
        user = service.create(user_data)

        # Assert
        assert user.id is not None
        assert user.name == "John"
        assert user.email == "john@example.com"

    def test_create_user_with_invalid_email_raises_error(self):
        # Arrange
        service = UserService()
        user_data = {"name": "John", "email": "invalid"}

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email"):
            service.create(user_data)
```

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest
from myapp.database import Database
from myapp.services import UserService

@pytest.fixture
def db():
    """Create test database connection."""
    database = Database(":memory:")
    database.create_tables()
    yield database
    database.close()

@pytest.fixture
def user_service(db):
    """Create UserService with test database."""
    return UserService(db)

@pytest.fixture
def sample_user(user_service):
    """Create a sample user for testing."""
    return user_service.create({
        "name": "Test User",
        "email": "test@example.com"
    })
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new for each test
def per_test_fixture():
    pass

@pytest.fixture(scope="class")  # Once per test class
def per_class_fixture():
    pass

@pytest.fixture(scope="module")  # Once per test module
def per_module_fixture():
    pass

@pytest.fixture(scope="session")  # Once per test session
def per_session_fixture():
    pass
```

### Parameterized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_type(request):
    """Run tests with different databases."""
    return request.param

@pytest.fixture
def db(db_type):
    """Create database based on type."""
    if db_type == "sqlite":
        return SQLiteDatabase()
    elif db_type == "postgres":
        return PostgresDatabase()
    else:
        return MySQLDatabase()
```

### Factory Fixtures

```python
@pytest.fixture
def user_factory(db):
    """Factory for creating test users."""
    created_users = []

    def _create_user(**kwargs):
        defaults = {
            "name": "Test User",
            "email": f"user{len(created_users)}@example.com"
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup
    for user in created_users:
        db.delete(user)
```

## Parametrization

### Basic Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double(input, expected):
    assert double(input) == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    # Runs 4 times: (0,2), (0,3), (1,2), (1,3)
    assert x + y >= 2
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("email,valid", [
    pytest.param("user@example.com", True, id="valid_email"),
    pytest.param("invalid", False, id="no_at_symbol"),
    pytest.param("@example.com", False, id="no_local_part"),
    pytest.param("user@", False, id="no_domain"),
])
def test_email_validation(email, valid):
    assert validate_email(email) == valid
```

## Mocking

### Using pytest-mock

```python
def test_send_email_calls_smtp(mocker):
    # Arrange
    mock_smtp = mocker.patch("myapp.email.smtplib.SMTP")
    service = EmailService()

    # Act
    service.send("test@example.com", "Hello", "Body")

    # Assert
    mock_smtp.return_value.sendmail.assert_called_once()

def test_external_api_call(mocker):
    # Mock external API response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_data("https://api.example.com")
    assert result["status"] == "ok"
```

### Mocking Classes

```python
def test_with_mock_class(mocker):
    # Create mock class instance
    mock_client = mocker.Mock(spec=DatabaseClient)
    mock_client.query.return_value = [{"id": 1, "name": "Test"}]

    # Inject mock
    service = UserService(client=mock_client)
    users = service.get_all()

    assert len(users) == 1
    mock_client.query.assert_called_with("SELECT * FROM users")
```

### Side Effects

```python
def test_retry_on_failure(mocker):
    # Simulate failures then success
    mock_api = mocker.patch("myapp.api.external_call")
    mock_api.side_effect = [
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        {"result": "success"},
    ]

    result = api_with_retry(max_retries=3)
    assert result == {"result": "success"}
    assert mock_api.call_count == 3
```

## Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_syntax():
    pass

@pytest.mark.xfail(reason="Known bug, fix in progress")
def test_known_issue():
    pass
```

### Custom Markers

```python
# In conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: integration tests")

# In tests
@pytest.mark.slow
def test_heavy_computation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass

# Run specific markers
# pytest -m "slow"
# pytest -m "not integration"
```

## Async Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_concurrent_operations():
    results = await asyncio.gather(
        async_operation_1(),
        async_operation_2(),
        async_operation_3(),
    )
    assert len(results) == 3

# Async fixture
@pytest.fixture
async def async_db():
    db = await AsyncDatabase.connect()
    yield db
    await db.close()
```

## Running pytest

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific file
pytest tests/test_services.py

# Run specific test
pytest tests/test_services.py::TestUserService::test_create_user

# Run tests matching pattern
pytest -k "create or delete"

# Run tests with marker
pytest -m integration

# Parallel execution (pytest-xdist)
pytest -n auto

# Show coverage
pytest --cov=src --cov-report=html

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

---

# Section 2: Jest/Vitest (JavaScript/TypeScript)

## Overview

Jest is the most popular JavaScript testing framework. Vitest is a newer, faster alternative compatible with Jest API.

## Installation

```bash
# Jest
npm install --save-dev jest @types/jest ts-jest

# Vitest
npm install --save-dev vitest @vitest/coverage-v8
```

## Project Structure

```
project/
├── src/
│   ├── services/
│   │   └── userService.ts
│   └── utils/
│       └── helpers.ts
├── tests/
│   ├── setup.ts
│   ├── services/
│   │   └── userService.test.ts
│   └── utils/
│       └── helpers.test.ts
├── jest.config.js         # or vitest.config.ts
└── package.json
```

## Jest Configuration (jest.config.js)

```javascript
/** @type {import('jest').Config} */
const config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  clearMocks: true,
  testTimeout: 10000,
};

module.exports = config;
```

## Vitest Configuration (vitest.config.ts)

```typescript
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.{test,spec}.{ts,tsx}'],
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.d.ts', 'src/index.ts'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
    testTimeout: 10000,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

## Basic Test Structure

```typescript
// userService.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'; // or jest
import { UserService } from '@/services/userService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  afterEach(() => {
    // Cleanup
  });

  describe('createUser', () => {
    it('should create user with valid data', () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };

      // Act
      const user = service.createUser(userData);

      // Assert
      expect(user).toBeDefined();
      expect(user.id).toBeDefined();
      expect(user.name).toBe('John');
      expect(user.email).toBe('john@example.com');
    });

    it('should throw error with invalid email', () => {
      // Arrange
      const userData = { name: 'John', email: 'invalid' };

      // Act & Assert
      expect(() => service.createUser(userData)).toThrow('Invalid email');
    });
  });
});
```

## Matchers

```typescript
describe('Matchers', () => {
  // Equality
  it('equality matchers', () => {
    expect(2 + 2).toBe(4);                    // Strict equality
    expect({ a: 1 }).toEqual({ a: 1 });       // Deep equality
    expect({ a: 1, b: 2 }).toMatchObject({ a: 1 }); // Partial match
  });

  // Truthiness
  it('truthiness matchers', () => {
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
    expect('hello').toBeDefined();
    expect(true).toBeTruthy();
    expect(false).toBeFalsy();
  });

  // Numbers
  it('number matchers', () => {
    expect(4).toBeGreaterThan(3);
    expect(4).toBeGreaterThanOrEqual(4);
    expect(4).toBeLessThan(5);
    expect(0.1 + 0.2).toBeCloseTo(0.3);
  });

  // Strings
  it('string matchers', () => {
    expect('hello world').toContain('world');
    expect('hello').toMatch(/^hel/);
    expect('hello').toHaveLength(5);
  });

  // Arrays
  it('array matchers', () => {
    expect([1, 2, 3]).toContain(2);
    expect([1, 2, 3]).toHaveLength(3);
    expect(['a', 'b', 'c']).toEqual(expect.arrayContaining(['a', 'c']));
  });

  // Objects
  it('object matchers', () => {
    expect({ name: 'John' }).toHaveProperty('name');
    expect({ name: 'John' }).toHaveProperty('name', 'John');
    expect({ a: 1, b: 2 }).toEqual(expect.objectContaining({ a: 1 }));
  });

  // Exceptions
  it('exception matchers', () => {
    expect(() => { throw new Error('fail'); }).toThrow();
    expect(() => { throw new Error('fail'); }).toThrow('fail');
    expect(() => { throw new Error('fail'); }).toThrow(Error);
  });
});
```

## Mocking

### Function Mocks

```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('Mocking', () => {
  it('should mock function', () => {
    const mockFn = vi.fn();
    mockFn('arg1', 'arg2');

    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('should mock return value', () => {
    const mockFn = vi.fn()
      .mockReturnValue('default')
      .mockReturnValueOnce('first')
      .mockReturnValueOnce('second');

    expect(mockFn()).toBe('first');
    expect(mockFn()).toBe('second');
    expect(mockFn()).toBe('default');
  });

  it('should mock implementation', () => {
    const mockFn = vi.fn().mockImplementation((x: number) => x * 2);
    expect(mockFn(5)).toBe(10);
  });
});
```

### Module Mocks

```typescript
// Mock entire module
vi.mock('@/services/api', () => ({
  fetchData: vi.fn().mockResolvedValue({ data: 'mocked' }),
}));

// Mock specific export
vi.mock('@/utils/helpers', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    formatDate: vi.fn().mockReturnValue('2024-01-01'),
  };
});

// Spy on module
import * as helpers from '@/utils/helpers';

it('should spy on module', () => {
  const spy = vi.spyOn(helpers, 'formatDate');
  helpers.formatDate(new Date());
  expect(spy).toHaveBeenCalled();
});
```

### Mocking HTTP Requests

```typescript
import { vi } from 'vitest';

// Mock fetch
global.fetch = vi.fn();

describe('API calls', () => {
  beforeEach(() => {
    vi.mocked(fetch).mockReset();
  });

  it('should fetch data', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ users: [] }),
    } as Response);

    const result = await fetchUsers();

    expect(fetch).toHaveBeenCalledWith('/api/users');
    expect(result).toEqual({ users: [] });
  });

  it('should handle error', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

    await expect(fetchUsers()).rejects.toThrow('Network error');
  });
});
```

## Async Testing

```typescript
describe('Async', () => {
  // Async/await
  it('should resolve async', async () => {
    const result = await asyncFetchData();
    expect(result).toBeDefined();
  });

  // Promises
  it('should resolve promise', () => {
    return fetchData().then(result => {
      expect(result).toBeDefined();
    });
  });

  // Callbacks
  it('should call callback', (done) => {
    fetchDataCallback((error, result) => {
      expect(error).toBeNull();
      expect(result).toBeDefined();
      done();
    });
  });

  // Timeouts
  it('should handle timers', () => {
    vi.useFakeTimers();

    const callback = vi.fn();
    setTimeout(callback, 1000);

    vi.advanceTimersByTime(1000);
    expect(callback).toHaveBeenCalled();

    vi.useRealTimers();
  });
});
```

## Snapshot Testing

```typescript
describe('Snapshots', () => {
  it('should match snapshot', () => {
    const user = { id: 1, name: 'John', email: 'john@example.com' };
    expect(user).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const result = formatUser({ name: 'John' });
    expect(result).toMatchInlineSnapshot(`"Hello, John!"`);
  });
});
```

## Running Tests

```bash
# Jest
npx jest
npx jest --watch
npx jest --coverage
npx jest path/to/test.ts
npx jest -t "test name pattern"

# Vitest
npx vitest
npx vitest run
npx vitest --coverage
npx vitest path/to/test.ts
npx vitest -t "test name pattern"
```

---

# Section 3: Go Testing

## Overview

Go has built-in testing support via the `testing` package. No external dependencies required.

## Project Structure

```
project/
├── pkg/
│   └── user/
│       ├── user.go
│       ├── user_test.go
│       └── testdata/
│           └── fixtures.json
├── internal/
│   └── service/
│       ├── service.go
│       └── service_test.go
├── go.mod
└── go.sum
```

## Basic Test Structure

```go
// user_test.go
package user

import (
    "testing"
)

func TestCreateUser(t *testing.T) {
    // Arrange
    service := NewUserService()
    input := UserInput{Name: "John", Email: "john@example.com"}

    // Act
    user, err := service.Create(input)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "John" {
        t.Errorf("expected name 'John', got '%s'", user.Name)
    }
    if user.Email != "john@example.com" {
        t.Errorf("expected email 'john@example.com', got '%s'", user.Email)
    }
}
```

## Table-Driven Tests

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {
            name:    "valid email",
            email:   "user@example.com",
            wantErr: false,
        },
        {
            name:    "missing at symbol",
            email:   "invalid",
            wantErr: true,
        },
        {
            name:    "missing domain",
            email:   "user@",
            wantErr: true,
        },
        {
            name:    "empty string",
            email:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail(%q) error = %v, wantErr %v",
                    tt.email, err, tt.wantErr)
            }
        })
    }
}
```

## Subtests

```go
func TestUserService(t *testing.T) {
    service := NewUserService()

    t.Run("Create", func(t *testing.T) {
        t.Run("with valid data", func(t *testing.T) {
            user, err := service.Create(validInput)
            if err != nil {
                t.Fatal(err)
            }
            if user.ID == 0 {
                t.Error("expected non-zero ID")
            }
        })

        t.Run("with invalid email", func(t *testing.T) {
            _, err := service.Create(invalidInput)
            if err == nil {
                t.Error("expected error for invalid email")
            }
        })
    })

    t.Run("Update", func(t *testing.T) {
        // Update tests
    })
}
```

## Test Helpers

```go
// testutil/helpers.go
package testutil

import "testing"

// AssertNoError fails the test if err is not nil
func AssertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

// AssertError fails the test if err is nil
func AssertError(t *testing.T, err error) {
    t.Helper()
    if err == nil {
        t.Fatal("expected error, got nil")
    }
}

// AssertEqual fails if got != want
func AssertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

## Mocking with Interfaces

```go
// Define interface
type UserRepository interface {
    Create(user User) (User, error)
    FindByID(id int) (User, error)
}

// Mock implementation
type MockUserRepository struct {
    CreateFunc   func(user User) (User, error)
    FindByIDFunc func(id int) (User, error)
}

func (m *MockUserRepository) Create(user User) (User, error) {
    if m.CreateFunc != nil {
        return m.CreateFunc(user)
    }
    return User{}, nil
}

func (m *MockUserRepository) FindByID(id int) (User, error) {
    if m.FindByIDFunc != nil {
        return m.FindByIDFunc(id)
    }
    return User{}, nil
}

// Test with mock
func TestUserService_Create(t *testing.T) {
    mockRepo := &MockUserRepository{
        CreateFunc: func(user User) (User, error) {
            user.ID = 1
            return user, nil
        },
    }

    service := NewUserService(mockRepo)
    user, err := service.Create(UserInput{Name: "John"})

    if err != nil {
        t.Fatal(err)
    }
    if user.ID != 1 {
        t.Errorf("expected ID 1, got %d", user.ID)
    }
}
```

## Setup and Teardown

```go
func TestMain(m *testing.M) {
    // Global setup
    setup()

    // Run tests
    code := m.Run()

    // Global teardown
    teardown()

    os.Exit(code)
}

func setup() {
    // Initialize test database, etc.
}

func teardown() {
    // Cleanup
}
```

## Benchmarks

```go
func BenchmarkProcessData(b *testing.B) {
    data := generateTestData(1000)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ProcessData(data)
    }
}

func BenchmarkProcessData_Parallel(b *testing.B) {
    data := generateTestData(1000)

    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            ProcessData(data)
        }
    })
}
```

## Fuzzing (Go 1.18+)

```go
func FuzzParseEmail(f *testing.F) {
    // Add seed corpus
    f.Add("user@example.com")
    f.Add("invalid")
    f.Add("")

    f.Fuzz(func(t *testing.T, email string) {
        _, err := ParseEmail(email)
        // Just verify it doesn't panic
        _ = err
    })
}
```

## Running Go Tests

```bash
# Run all tests
go test ./...

# Verbose output
go test -v ./...

# Run specific package
go test ./pkg/user

# Run specific test
go test -run TestCreateUser ./pkg/user

# Run subtests
go test -run TestUserService/Create/with_valid_data ./pkg/user

# With coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run benchmarks
go test -bench=. ./...
go test -bench=BenchmarkProcessData -benchmem ./...

# Race detection
go test -race ./...

# Timeout
go test -timeout 30s ./...

# Run tests in parallel
go test -parallel 4 ./...
```

---

# Section 4: E2E Testing

## Playwright (Recommended)

### Installation

```bash
npm install --save-dev @playwright/test
npx playwright install
```

### Configuration (playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should login with valid credentials', async ({ page }) => {
    // Navigate to login
    await page.click('[data-testid="login-button"]');

    // Fill form
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');

    // Submit
    await page.click('[data-testid="submit-button"]');

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.click('[data-testid="login-button"]');
    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpassword');
    await page.click('[data-testid="submit-button"]');

    await expect(page.locator('[data-testid="error-message"]'))
      .toBeVisible();
  });
});
```

### Page Object Pattern

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.submitButton = page.locator('[data-testid="submit-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
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

// Using in tests
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

### Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

type Fixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  authenticatedPage: async ({ page }, use) => {
    // Login before test
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('test@example.com', 'password');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### API Testing with Playwright

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Tests', () => {
  test('should create user via API', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: {
        name: 'John',
        email: 'john@example.com',
      },
    });

    expect(response.status()).toBe(201);
    const user = await response.json();
    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
  });

  test('should authenticate via API', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'user@example.com',
        password: 'password',
      },
    });

    expect(response.status()).toBe(200);
    const { token } = await response.json();

    // Use token for subsequent requests
    const profileResponse = await request.get('/api/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    expect(profileResponse.status()).toBe(200);
  });
});
```

### Running Playwright

```bash
# Run all tests
npx playwright test

# Run in headed mode
npx playwright test --headed

# Run specific file
npx playwright test e2e/auth.spec.ts

# Run specific project
npx playwright test --project=chromium

# Debug mode
npx playwright test --debug

# UI mode
npx playwright test --ui

# Generate tests
npx playwright codegen http://localhost:3000

# Show report
npx playwright show-report
```

## Cypress (Alternative)

### Installation

```bash
npm install --save-dev cypress
```

### Configuration (cypress.config.ts)

```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.ts',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
  },
});
```

### Basic Test

```typescript
// cypress/e2e/auth.cy.ts
describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should login successfully', () => {
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="email-input"]').type('user@example.com');
    cy.get('[data-testid="password-input"]').type('password');
    cy.get('[data-testid="submit-button"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="welcome-message"]').should('contain', 'Welcome');
  });
});
```

### Custom Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="email-input"]').type(email);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="submit-button"]').click();
  cy.url().should('include', '/dashboard');
});

// Usage
cy.login('user@example.com', 'password');
```

---

# Section 5: Test Structure Patterns

## Arrange-Act-Assert (AAA)

```python
def test_user_creation():
    # Arrange - Set up test data and conditions
    service = UserService()
    user_data = {"name": "John", "email": "john@example.com"}

    # Act - Perform the action being tested
    user = service.create(user_data)

    # Assert - Verify the expected outcome
    assert user.id is not None
    assert user.name == "John"
```

## Given-When-Then (BDD)

```python
def test_user_login():
    # Given - A registered user exists
    user = create_user("john@example.com", "password123")

    # When - The user logs in with correct credentials
    result = auth_service.login("john@example.com", "password123")

    # Then - A valid session token is returned
    assert result.token is not None
    assert result.user_id == user.id
```

## Test Isolation Principles

```python
class TestUserService:
    """
    Test Isolation Rules:
    1. Each test is independent
    2. Tests don't share state
    3. Tests can run in any order
    4. Tests clean up after themselves
    """

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Fresh database for each test."""
        db.clear_all()
        yield
        db.clear_all()

    def test_create_user(self, user_service):
        # This test doesn't depend on other tests
        user = user_service.create({"name": "John"})
        assert user.id == 1  # First user in fresh db

    def test_list_users(self, user_service):
        # This test also starts with empty database
        users = user_service.list_all()
        assert len(users) == 0  # Fresh db
```

## Test Pyramid

```
                    /\
                   /  \
                  / E2E \        <- Few, slow, expensive
                 /------\
                /        \
               / Integration \   <- Some, medium speed
              /--------------\
             /                \
            /    Unit Tests    \ <- Many, fast, cheap
           /--------------------\
```

**Recommended ratio:** 70% Unit, 20% Integration, 10% E2E

---

# Section 6: Mocking and Fixtures

## When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own code logic |
| Database in unit tests | Simple utilities |
| File system | Pure functions |
| Network calls | Domain logic |
| Time/randomness | |

## Fixture Strategies

### Builder Pattern

```python
class UserBuilder:
    def __init__(self):
        self._name = "Default User"
        self._email = "default@example.com"
        self._role = "user"

    def with_name(self, name: str) -> "UserBuilder":
        self._name = name
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def as_admin(self) -> "UserBuilder":
        self._role = "admin"
        return self

    def build(self) -> User:
        return User(
            name=self._name,
            email=self._email,
            role=self._role
        )

# Usage
user = UserBuilder().with_name("John").as_admin().build()
```

### Factory Pattern

```python
import factory
from factory.faker import Faker

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = Faker("name")
    email = Faker("email")
    created_at = factory.LazyFunction(datetime.now)

# Usage
user = UserFactory()  # Random user
user = UserFactory(name="John")  # Override specific field
users = UserFactory.create_batch(10)  # Create many
```

---

# Section 7: Coverage Reporting

## Python (pytest-cov)

```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Enforce minimum coverage
pytest --cov=src --cov-fail-under=80

# Coverage for specific paths
pytest --cov=src/services --cov=src/models tests/
```

## JavaScript (Jest/Vitest)

```bash
# Jest
npx jest --coverage

# Vitest
npx vitest run --coverage
```

## Go

```bash
# Generate coverage
go test -coverprofile=coverage.out ./...

# View in terminal
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html
```

## Coverage Best Practices

1. **Set realistic thresholds** - Start at 70-80%, not 100%
2. **Focus on critical paths** - Business logic > boilerplate
3. **Exclude generated code** - Don't test auto-generated files
4. **Branch coverage matters** - Not just line coverage
5. **Don't game metrics** - Tests should verify behavior, not just execute code

---

# Section 8: TDD Workflow

## Red-Green-Refactor Cycle

```
RED: Write failing test
    ↓
GREEN: Write minimum code to pass
    ↓
REFACTOR: Improve code quality
    ↓
(repeat)
```

## Example TDD Session

```python
# Step 1: RED - Write failing test
def test_calculate_discount():
    calculator = PriceCalculator()
    result = calculator.calculate_discount(100, 10)
    assert result == 90  # FAILS - class doesn't exist

# Step 2: GREEN - Minimal implementation
class PriceCalculator:
    def calculate_discount(self, price: float, percent: float) -> float:
        return price - (price * percent / 100)

# Step 3: REFACTOR - Improve
class PriceCalculator:
    def calculate_discount(self, price: float, percent: float) -> float:
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        return round(price * (1 - percent / 100), 2)

# Step 4: Add more tests for edge cases
@pytest.mark.parametrize("price,discount,expected", [
    (100, 10, 90),
    (100, 0, 100),
    (100, 100, 0),
    (49.99, 20, 39.99),
])
def test_calculate_discount_cases(price, discount, expected):
    calculator = PriceCalculator()
    assert calculator.calculate_discount(price, discount) == expected
```

## TDD Benefits

1. **Design feedback** - Tests expose design problems early
2. **Documentation** - Tests document expected behavior
3. **Confidence** - Safe refactoring with test coverage
4. **Focus** - Work on one thing at a time

---

# Section 9: CI Integration

## GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  test-javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test -- --coverage

  test-go:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Run tests
        run: go test -race -coverprofile=coverage.out ./...
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run E2E tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

# Quick Reference

## Commands

| Framework | Run All | Run Specific | Coverage |
|-----------|---------|--------------|----------|
| pytest | `pytest` | `pytest tests/test_x.py -k name` | `pytest --cov=src` |
| Jest | `npx jest` | `npx jest -t "name"` | `npx jest --coverage` |
| Vitest | `npx vitest` | `npx vitest -t "name"` | `npx vitest --coverage` |
| Go | `go test ./...` | `go test -run TestName` | `go test -cover` |
| Playwright | `npx playwright test` | `npx playwright test file.spec.ts` | N/A |

## Test Naming

| Style | Example |
|-------|---------|
| Descriptive | `test_user_create_with_valid_data_returns_user` |
| BDD | `should_return_user_when_data_is_valid` |
| Simple | `test_create_user_success` |

---

*Testing Skill v1.0 - 2026-01-18*
*Technical Skill (Layer 3)*
*Used by: faion-test-agent*
