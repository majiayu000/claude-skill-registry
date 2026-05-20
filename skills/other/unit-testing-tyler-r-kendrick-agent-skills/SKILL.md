---
name: unit-testing
description: |
    Use when writing, improving, or debugging unit tests that verify isolated functions, methods, and classes. Covers cross-platform frameworks including Vitest, Jest, xUnit, NUnit, MSTest, pytest, JUnit 5, and Go testing with mocking strategies, test doubles, AAA pattern, and naming conventions.
    USE FOR: unit test frameworks, Vitest, Jest, xUnit, NUnit, pytest, JUnit, Go test, mocking, test doubles, AAA pattern
    DO NOT USE FOR: multi-component tests (use integration-testing), browser tests (use e2e-testing), API contract verification (use contract-testing)
license: MIT
metadata:
  displayName: "Unit Testing"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Vitest Documentation"
    url: "https://vitest.dev"
  - title: "Jest Documentation"
    url: "https://jestjs.io/docs/getting-started"
  - title: "pytest Documentation"
    url: "https://docs.pytest.org"
  - title: "xUnit.net Documentation"
    url: "https://xunit.net/#documentation"
---

# Unit Testing — Testing Isolated Functions and Classes

## Overview
Unit tests verify the **smallest testable parts** of an application in isolation. They are fast, cheap to run, and provide rapid feedback on whether individual functions, methods, and classes behave correctly. In the Test Trophy model, unit tests sit above static analysis and below integration tests.

> **When to unit test:** Pure functions, business logic, algorithms, data transformations, edge cases, error handling, and any code with complex branching.

## The AAA Pattern (Arrange-Act-Assert)

Every unit test should follow three distinct phases:

1. **Arrange** — Set up test data, dependencies, and preconditions
2. **Act** — Execute the function or method under test
3. **Assert** — Verify the result matches expectations

### AAA in TypeScript (Vitest)
```typescript
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  it('should apply 10% discount for orders over $100', () => {
    // Arrange
    const orderTotal = 150;
    const discountThreshold = 100;
    const discountRate = 0.1;

    // Act
    const result = calculateDiscount(orderTotal, discountThreshold, discountRate);

    // Assert
    expect(result).toBe(135);
  });
});
```

### AAA in C# (xUnit)
```csharp
public class PricingTests
{
    [Fact]
    public void CalculateDiscount_OrderOver100_Applies10PercentDiscount()
    {
        // Arrange
        var calculator = new PricingCalculator();
        var orderTotal = 150m;

        // Act
        var result = calculator.CalculateDiscount(orderTotal);

        // Assert
        Assert.Equal(135m, result);
    }
}
```

### AAA in Python (pytest)
```python
from pricing import calculate_discount

def test_calculate_discount_order_over_100_applies_10_percent():
    # Arrange
    order_total = 150.0
    discount_threshold = 100.0
    discount_rate = 0.1

    # Act
    result = calculate_discount(order_total, discount_threshold, discount_rate)

    # Assert
    assert result == 135.0
```

---

## JavaScript / TypeScript

### Vitest
Vitest is the modern standard for JS/TS testing — fast, ESM-native, and Vite-compatible.

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',          // or 'jsdom' for browser APIs
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
    include: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
  },
});
```

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './user-service';
import type { UserRepository } from './user-repository';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: UserRepository;

  beforeEach(() => {
    mockRepo = {
      findById: vi.fn(),
      save: vi.fn(),
      delete: vi.fn(),
    };
    service = new UserService(mockRepo);
  });

  it('should return user when found', async () => {
    const expectedUser = { id: '1', name: 'Alice', email: 'alice@example.com' };
    vi.mocked(mockRepo.findById).mockResolvedValue(expectedUser);

    const result = await service.getUser('1');

    expect(result).toEqual(expectedUser);
    expect(mockRepo.findById).toHaveBeenCalledWith('1');
  });

  it('should throw when user not found', async () => {
    vi.mocked(mockRepo.findById).mockResolvedValue(null);

    await expect(service.getUser('999')).rejects.toThrow('User not found');
  });

  it('should validate email before saving', async () => {
    const invalidUser = { name: 'Bob', email: 'not-an-email' };

    await expect(service.createUser(invalidUser)).rejects.toThrow('Invalid email');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });
});
```

**Snapshot testing:**
```typescript
import { describe, it, expect } from 'vitest';
import { formatUserProfile } from './formatters';

describe('formatUserProfile', () => {
  it('should format profile correctly', () => {
    const user = { name: 'Alice', role: 'admin', joinedAt: '2024-01-15' };

    expect(formatUserProfile(user)).toMatchInlineSnapshot(`
      "Name: Alice
      Role: Admin
      Member since: January 2024"
    `);
  });
});
```

```bash
npx vitest              # Watch mode
npx vitest run          # Single run
npx vitest run --coverage
```

### Jest
Jest remains widely used in existing codebases and React projects.

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
};
```

```typescript
import { OrderProcessor } from './order-processor';

describe('OrderProcessor', () => {
  it('should calculate tax correctly', () => {
    const processor = new OrderProcessor();

    const result = processor.calculateTax(100, 'US-CA');

    expect(result).toBeCloseTo(7.25);
  });

  it('should reject negative amounts', () => {
    const processor = new OrderProcessor();

    expect(() => processor.calculateTax(-50, 'US-CA')).toThrow('Amount must be positive');
  });
});

// Mocking modules
jest.mock('./tax-rates', () => ({
  getTaxRate: jest.fn().mockReturnValue(0.0725),
}));
```

```bash
npx jest
npx jest --watch
npx jest --coverage
```

---

## C# / .NET

### xUnit
xUnit is the most popular .NET test framework — used by the .NET team itself.

```csharp
using Xunit;
using Moq;

public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _mockRepo;
    private readonly Mock<IEmailService> _mockEmail;
    private readonly OrderService _service;

    public OrderServiceTests()
    {
        _mockRepo = new Mock<IOrderRepository>();
        _mockEmail = new Mock<IEmailService>();
        _service = new OrderService(_mockRepo.Object, _mockEmail.Object);
    }

    [Fact]
    public async Task PlaceOrder_ValidOrder_SavesAndSendsConfirmation()
    {
        // Arrange
        var order = new Order { CustomerId = "C1", Total = 99.99m };
        _mockRepo.Setup(r => r.SaveAsync(It.IsAny<Order>()))
                 .ReturnsAsync(order with { Id = "O1" });

        // Act
        var result = await _service.PlaceOrderAsync(order);

        // Assert
        Assert.Equal("O1", result.Id);
        _mockRepo.Verify(r => r.SaveAsync(order), Times.Once);
        _mockEmail.Verify(e => e.SendConfirmationAsync("C1", "O1"), Times.Once);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public async Task PlaceOrder_InvalidTotal_ThrowsArgumentException(decimal total)
    {
        var order = new Order { CustomerId = "C1", Total = total };

        await Assert.ThrowsAsync<ArgumentException>(
            () => _service.PlaceOrderAsync(order));
    }

    [Theory]
    [MemberData(nameof(DiscountTestCases))]
    public void ApplyDiscount_VariousInputs_ReturnsExpectedResult(
        decimal amount, string tier, decimal expected)
    {
        var result = _service.ApplyDiscount(amount, tier);

        Assert.Equal(expected, result);
    }

    public static IEnumerable<object[]> DiscountTestCases()
    {
        yield return new object[] { 100m, "gold", 85m };
        yield return new object[] { 100m, "silver", 90m };
        yield return new object[] { 100m, "bronze", 95m };
        yield return new object[] { 100m, "none", 100m };
    }
}
```

### NUnit
```csharp
using NUnit.Framework;
using Moq;

[TestFixture]
public class CalculatorTests
{
    private Calculator _calculator;

    [SetUp]
    public void SetUp()
    {
        _calculator = new Calculator();
    }

    [Test]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        var result = _calculator.Add(2, 3);

        Assert.That(result, Is.EqualTo(5));
    }

    [TestCase(0, 0, 0)]
    [TestCase(1, -1, 0)]
    [TestCase(-5, -3, -8)]
    [TestCase(int.MaxValue, 0, int.MaxValue)]
    public void Add_VariousInputs_ReturnsExpectedSum(int a, int b, int expected)
    {
        var result = _calculator.Add(a, b);

        Assert.That(result, Is.EqualTo(expected));
    }

    [Test]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        Assert.Throws<DivideByZeroException>(() => _calculator.Divide(10, 0));
    }
}
```

### MSTest
```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

[TestClass]
public class StringHelperTests
{
    [TestMethod]
    public void Truncate_LongString_TruncatesWithEllipsis()
    {
        var result = StringHelper.Truncate("Hello, World!", 5);

        Assert.AreEqual("Hello...", result);
    }

    [DataTestMethod]
    [DataRow("", 5, "")]
    [DataRow("Hi", 5, "Hi")]
    [DataRow("Hello, World!", 5, "Hello...")]
    public void Truncate_VariousInputs_ReturnsExpected(
        string input, int maxLength, string expected)
    {
        var result = StringHelper.Truncate(input, maxLength);

        Assert.AreEqual(expected, result);
    }
}
```

### AutoFixture (C# test data generation)
```csharp
using AutoFixture;
using AutoFixture.AutoMoq;
using Xunit;

public class UserServiceAutoTests
{
    private readonly IFixture _fixture;

    public UserServiceAutoTests()
    {
        _fixture = new Fixture().Customize(new AutoMoqCustomization());
    }

    [Theory, AutoData]
    public async Task GetUser_ExistingId_ReturnsUser(string userId)
    {
        // AutoFixture generates userId automatically
        var expectedUser = _fixture.Build<User>()
            .With(u => u.Id, userId)
            .Create();

        var mockRepo = _fixture.Freeze<Mock<IUserRepository>>();
        mockRepo.Setup(r => r.FindByIdAsync(userId)).ReturnsAsync(expectedUser);

        var service = _fixture.Create<UserService>();

        var result = await service.GetUserAsync(userId);

        Assert.Equal(expectedUser.Name, result.Name);
    }
}
```

```bash
dotnet test
dotnet test --filter "FullyQualifiedName~OrderService"
dotnet test --collect:"XPlat Code Coverage"
dotnet test --logger "trx;LogFileName=results.trx"
```

---

## Python

### pytest
pytest is the de facto standard for Python testing — simple, powerful, and extensible.

```python
# conftest.py — shared fixtures
import pytest
from unittest.mock import AsyncMock, MagicMock
from myapp.database import Database
from myapp.services import UserService

@pytest.fixture
def mock_db():
    """Create a mock database connection."""
    db = MagicMock(spec=Database)
    db.query = AsyncMock()
    return db

@pytest.fixture
def user_service(mock_db):
    """Create UserService with mocked dependencies."""
    return UserService(db=mock_db)

@pytest.fixture
def sample_user():
    """Create a sample user dict."""
    return {
        "id": "user-123",
        "name": "Alice",
        "email": "alice@example.com",
        "role": "admin",
    }
```

```python
# test_user_service.py
import pytest
from myapp.services import UserService
from myapp.exceptions import UserNotFoundError, ValidationError

class TestUserService:
    async def test_get_user_returns_user_when_found(self, user_service, mock_db, sample_user):
        # Arrange
        mock_db.query.return_value = sample_user

        # Act
        result = await user_service.get_user("user-123")

        # Assert
        assert result["name"] == "Alice"
        mock_db.query.assert_called_once_with("SELECT * FROM users WHERE id = %s", ("user-123",))

    async def test_get_user_raises_when_not_found(self, user_service, mock_db):
        mock_db.query.return_value = None

        with pytest.raises(UserNotFoundError, match="User user-999 not found"):
            await user_service.get_user("user-999")

    @pytest.mark.parametrize("email,is_valid", [
        ("alice@example.com", True),
        ("bob@company.org", True),
        ("not-an-email", False),
        ("", False),
        ("@missing-local.com", False),
    ])
    def test_validate_email(self, user_service, email, is_valid):
        if is_valid:
            assert user_service.validate_email(email) is True
        else:
            with pytest.raises(ValidationError):
                user_service.validate_email(email)
```

**Monkeypatch for environment and dependencies:**
```python
def test_get_api_url_from_env(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://api.example.com")

    from myapp.config import get_api_url
    assert get_api_url() == "https://api.example.com"

def test_get_api_url_default_when_not_set(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)

    from myapp.config import get_api_url
    assert get_api_url() == "http://localhost:3000"
```

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks integration tests
```

```bash
pytest
pytest -x                     # Stop on first failure
pytest -k "test_user"         # Run tests matching pattern
pytest -m "not slow"          # Skip slow tests
pytest --cov=src --cov-report=html
```

---

## Java

### JUnit 5
```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import org.mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    @DisplayName("Should place order and send notification")
    void placeOrder_validOrder_savesAndNotifies() {
        // Arrange
        var order = new Order("customer-1", BigDecimal.valueOf(99.99));
        when(orderRepository.save(any(Order.class)))
            .thenReturn(order.withId("order-1"));

        // Act
        var result = orderService.placeOrder(order);

        // Assert
        assertEquals("order-1", result.getId());
        verify(orderRepository).save(order);
        verify(notificationService).sendConfirmation("customer-1", "order-1");
    }

    @Test
    @DisplayName("Should throw when order total is negative")
    void placeOrder_negativeTotal_throwsException() {
        var order = new Order("customer-1", BigDecimal.valueOf(-10));

        assertThrows(IllegalArgumentException.class,
            () -> orderService.placeOrder(order));

        verifyNoInteractions(orderRepository);
    }

    @ParameterizedTest
    @CsvSource({
        "100, gold, 85",
        "100, silver, 90",
        "100, bronze, 95",
        "100, none, 100",
    })
    @DisplayName("Should apply tier-based discounts correctly")
    void applyDiscount_variousTiers_returnsExpected(
            BigDecimal amount, String tier, BigDecimal expected) {
        var result = orderService.applyDiscount(amount, tier);

        assertEquals(expected, result);
    }

    @Nested
    @DisplayName("When order has items")
    class WhenOrderHasItems {

        @Test
        void totalShouldSumAllItems() {
            var order = new Order();
            order.addItem(new Item("Widget", BigDecimal.valueOf(10)));
            order.addItem(new Item("Gadget", BigDecimal.valueOf(25)));

            assertEquals(BigDecimal.valueOf(35), order.getTotal());
        }
    }
}
```

```bash
mvn test
mvn test -Dtest="OrderServiceTest"
gradle test
gradle test --tests "com.example.OrderServiceTest"
```

---

## Go

### Go testing Package
```go
package pricing_test

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "myapp/pricing"
)

func TestCalculateDiscount(t *testing.T) {
    t.Run("applies 10% discount for orders over 100", func(t *testing.T) {
        // Arrange
        calculator := pricing.NewCalculator()

        // Act
        result, err := calculator.CalculateDiscount(150.0, "gold")

        // Assert
        require.NoError(t, err)
        assert.InDelta(t, 135.0, result, 0.01)
    })

    t.Run("returns error for negative amount", func(t *testing.T) {
        calculator := pricing.NewCalculator()

        _, err := calculator.CalculateDiscount(-50.0, "gold")

        assert.Error(t, err)
        assert.Contains(t, err.Error(), "amount must be positive")
    })
}

// Table-driven tests — idiomatic Go
func TestApplyDiscount(t *testing.T) {
    tests := []struct {
        name     string
        amount   float64
        tier     string
        expected float64
        wantErr  bool
    }{
        {name: "gold tier 15% off", amount: 100, tier: "gold", expected: 85},
        {name: "silver tier 10% off", amount: 100, tier: "silver", expected: 90},
        {name: "bronze tier 5% off", amount: 100, tier: "bronze", expected: 95},
        {name: "no tier no discount", amount: 100, tier: "none", expected: 100},
        {name: "negative amount errors", amount: -1, tier: "gold", wantErr: true},
        {name: "zero amount is valid", amount: 0, tier: "gold", expected: 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            calculator := pricing.NewCalculator()

            result, err := calculator.ApplyDiscount(tt.amount, tt.tier)

            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            require.NoError(t, err)
            assert.InDelta(t, tt.expected, result, 0.01)
        })
    }
}
```

```bash
go test ./...
go test ./... -v
go test ./... -count=1             # Disable test caching
go test ./... -cover
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out   # Open HTML coverage report
go test -run TestCalculateDiscount ./pricing
```

---

## Test Doubles: Mock, Stub, Spy, Fake

| Double | Purpose | Behavior |
|--------|---------|----------|
| **Stub** | Provides canned answers to calls | Returns predefined data, no verification |
| **Mock** | Verifies interactions (calls, args) | Asserts specific methods were called correctly |
| **Spy** | Wraps real object, records calls | Real behavior + call recording |
| **Fake** | Working implementation (simplified) | In-memory DB, fake HTTP server |

### Stub Example (TypeScript)
```typescript
const stubRepo: UserRepository = {
  findById: async () => ({ id: '1', name: 'Alice', email: 'a@b.com' }),
  save: async (user) => user,
  delete: async () => {},
};
```

### Mock Example (C# — Moq)
```csharp
var mock = new Mock<IEmailService>();
mock.Setup(e => e.SendAsync(It.IsAny<string>(), It.IsAny<string>()))
    .ReturnsAsync(true);

// ... use mock.Object ...

mock.Verify(e => e.SendAsync("alice@example.com", It.Is<string>(s => s.Contains("Welcome"))),
    Times.Once);
```

### Spy Example (Python)
```python
from unittest.mock import patch

def test_logs_user_creation(user_service):
    with patch.object(user_service, 'logger') as spy_logger:
        user_service.create_user({"name": "Alice", "email": "a@b.com"})

        spy_logger.info.assert_called_once_with("User created: Alice")
```

### Fake Example (Go)
```go
type FakeUserStore struct {
    users map[string]*User
}

func NewFakeUserStore() *FakeUserStore {
    return &FakeUserStore{users: make(map[string]*User)}
}

func (f *FakeUserStore) Save(u *User) error {
    f.users[u.ID] = u
    return nil
}

func (f *FakeUserStore) FindByID(id string) (*User, error) {
    u, ok := f.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}
```

---

## Test Naming Conventions

### Pattern: `MethodName_Scenario_ExpectedBehavior`
```
CalculateDiscount_OrderOver100_Applies10PercentDiscount
PlaceOrder_NegativeTotal_ThrowsArgumentException
ValidateEmail_EmptyString_ReturnsFalse
```

### Pattern: `should <expected behavior> when <scenario>`
```
should apply 10% discount when order is over $100
should throw when order total is negative
should return false when email is empty
```

### Pattern: `given_when_then` (BDD-style)
```
givenGoldTierCustomer_whenOrderOver100_thenApplies15PercentDiscount
givenNewUser_whenEmailIsInvalid_thenThrowsValidationError
```

### By Language Convention

| Language | Convention | Example |
|----------|-----------|---------|
| **TypeScript/JS** | `describe`/`it` with natural language | `it('should apply discount for gold tier')` |
| **C# (xUnit)** | `Method_Scenario_Expected` | `CalculateDiscount_GoldTier_Returns85` |
| **C# (NUnit)** | `Method_Scenario_Expected` or `Should_Expected_When_Scenario` | Same |
| **Python** | `test_` prefix with snake_case | `test_calculate_discount_gold_tier_returns_85` |
| **Java** | `@DisplayName` annotation | `@DisplayName("Should apply 15% discount for gold tier")` |
| **Go** | `Test` prefix + descriptive | `TestCalculateDiscount_GoldTier` |

---

## CI Integration

### GitHub Actions
```yaml
name: Unit Tests

on: [push, pull_request]

jobs:
  test-node:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
      - run: npm ci
      - run: npx vitest run --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  test-dotnet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "9.x"
      - run: dotnet test --collect:"XPlat Code Coverage" --logger "trx"

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[test]"
      - run: pytest --cov=src --cov-report=xml --junitxml=results.xml
```

## Best Practices
- Follow the AAA pattern (Arrange-Act-Assert) in every test for readability and consistency.
- Test one behavior per test — if a test has multiple `assert`/`expect` calls testing different behaviors, split it.
- Name tests descriptively — a failing test name should tell you exactly what broke without reading the test body.
- Prefer stubs for queries and mocks for commands (Command-Query Separation).
- Do not mock what you do not own — wrap third-party libraries and mock the wrapper.
- Keep test setup minimal — use factories or builders instead of massive arrange blocks.
- Avoid testing implementation details — test behavior (inputs and outputs), not internal method calls.
- Use parameterized/data-driven tests for the same logic with different inputs.
- Make tests deterministic — no random data, no reliance on time, no shared mutable state.
- Run unit tests on every commit — they should complete in seconds, not minutes.
- Aim for high coverage of business logic, not 100% coverage of all code.
- Use code coverage as a guide, not a goal — 80% meaningful coverage beats 100% with trivial assertions.
