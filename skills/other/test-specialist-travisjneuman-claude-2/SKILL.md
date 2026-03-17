---
name: test-specialist
description: This skill should be used when writing test cases, fixing bugs, analyzing code for potential issues, or improving test coverage for JavaScript/TypeScript applications. Use this for unit tests, integration tests, end-to-end tests, debugging runtime errors, logic bugs, performance issues, security vulnerabilities, and systematic code analysis.
---

# Test Specialist

Systematic testing methodologies and debugging techniques for JS/TS applications.

## When to Use

**Use for:**

- Writing unit, integration, or E2E tests
- Fixing bugs and debugging
- Improving test coverage
- Analyzing code for potential issues
- Security and performance testing

**Don't use when:**

- Code review → use `generic-code-reviewer`
- Technical debt → use `tech-debt-analyzer`
- Feature development → use `generic-feature-developer`

## Testing Stack by Project

| Project Type  | Unit Tests  | Component       | E2E        |
| ------------- | ----------- | --------------- | ---------- |
| React/Next.js | Vitest/Jest | Testing Library | Playwright |
| Node.js       | Vitest/Jest | Supertest       | Playwright |
| Static        | Jest        | -               | Playwright |

## Test Patterns

### Unit Tests (AAA Pattern)

```typescript
describe("calculateTotal", () => {
  test("sums amounts correctly", () => {
    // Arrange
    const items = [{ amount: 100 }, { amount: 50 }];
    // Act
    const total = calculateTotal(items);
    // Assert
    expect(total).toBe(150);
  });

  test("handles empty list", () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### Component Tests (User Behavior)

```typescript
// ✅ Test user behavior, not implementation
it('creates item when user clicks Add', async () => {
  const user = userEvent.setup();
  render(<ItemList />);

  await user.click(screen.getByRole('button', { name: /add/i }));
  await user.type(screen.getByLabelText(/title/i), 'New item');
  await user.click(screen.getByRole('button', { name: /save/i }));

  expect(screen.getByText('New item')).toBeInTheDocument();
});
```

### E2E Tests (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("user can complete checkout", async ({ page }) => {
  await page.goto("/products");

  // Add to cart
  await page.click('button:has-text("Add to Cart")');
  await page.click('a:has-text("Cart")');

  // Checkout
  await page.click('button:has-text("Checkout")');
  await page.fill('[name="email"]', "test@example.com");
  await page.click('button:has-text("Place Order")');

  // Verify
  await expect(page.locator("h1")).toContainText("Order Confirmed");
});
```

### Integration Tests

```typescript
test("POST /items creates item", async () => {
  const response = await request(app)
    .post("/api/items")
    .send({ name: "Test" })
    .expect(201);

  expect(response.body).toMatchObject({ id: expect.any(Number) });
});
```

## Bug Analysis Process

1. **Reproduce** - Document exact steps, expected vs actual
2. **Isolate** - Binary search, minimal reproduction
3. **Root Cause** - Trace execution, check assumptions, git blame
4. **Fix** - Write failing test first, implement fix
5. **Validate** - Run full suite, test edge cases

## Debugging Checklist

When debugging an issue:

- [ ] Can reproduce consistently
- [ ] Minimal reproduction created
- [ ] Console/network logs checked
- [ ] State at failure point inspected
- [ ] Git blame checked for recent changes
- [ ] Failing test written before fix

## Common Bug Patterns

### Race Conditions

```typescript
test("handles concurrent updates", async () => {
  const promises = Array.from({ length: 100 }, () => increment());
  await Promise.all(promises);
  expect(getCount()).toBe(100);
});
```

### Null Safety

```typescript
test.each([null, undefined, "", 0])("handles invalid input: %p", (input) => {
  expect(() => process(input)).toThrow("Invalid");
});
```

### Boundary Values

```typescript
test("handles edge cases", () => {
  expect(paginate([], 1, 10)).toEqual([]); // empty
  expect(paginate([item], 1, 10)).toEqual([item]); // single
  expect(paginate(items25, 3, 10)).toHaveLength(5); // partial last page
});
```

## Security Tests

```typescript
test("prevents SQL injection", async () => {
  const malicious = "'; DROP TABLE users; --";
  await expect(search(malicious)).resolves.not.toThrow();
});

test("sanitizes XSS", () => {
  const xss = '<script>alert("xss")</script>';
  expect(sanitize(xss)).not.toContain("<script>");
});

test("requires auth", async () => {
  await request(app).post("/api/items").expect(401);
});
```

## Performance Tests

```typescript
test("handles large datasets efficiently", () => {
  const largeList = Array.from({ length: 10000 }, (_, i) => ({ value: i }));
  const start = performance.now();
  process(largeList);
  expect(performance.now() - start).toBeLessThan(100);
});
```

## Coverage Targets

| Code Type      | Target |
| -------------- | ------ |
| Critical paths | 90%+   |
| Business logic | 85%+   |
| UI components  | 75%+   |
| Utilities      | 70%+   |

## Test Quality Principles

1. **One behavior per test**
2. **Descriptive names** - test names explain scenario
3. **Independent tests** - no shared state
4. **Cover edge cases** - null, empty, boundaries, errors
5. **Mock external deps** - tests should be fast
6. **Test behavior** - not implementation details

## Workflow Decision Tree

| Situation          | Action                               |
| ------------------ | ------------------------------------ |
| Adding feature     | Write test first (TDD)               |
| Fixing bug         | Write failing test, then fix         |
| Improving coverage | Find gaps, prioritize critical paths |
| Code review        | Check edge cases, error handling     |

---

## Python Testing (pytest)

### Fixtures and Parametrize

```python
import pytest
from myapp.services import UserService

@pytest.fixture
def user_service(db_session):
    """Provide a UserService with test database."""
    return UserService(session=db_session)

@pytest.fixture
def sample_user(user_service):
    """Create and return a sample user."""
    return user_service.create(name="Test User", email="test@example.com")

class TestUserService:
    def test_create_user(self, user_service):
        user = user_service.create(name="John", email="john@example.com")
        assert user.name == "John"
        assert user.id is not None

    def test_get_user_not_found(self, user_service):
        with pytest.raises(UserNotFoundError, match="User 999 not found"):
            user_service.get(999)

    @pytest.mark.parametrize("email,is_valid", [
        ("user@example.com", True),
        ("user@sub.domain.com", True),
        ("invalid", False),
        ("@example.com", False),
        ("", False),
    ])
    def test_validate_email(self, user_service, email: str, is_valid: bool):
        assert user_service.validate_email(email) == is_valid
```

### Mocking

```python
from unittest.mock import Mock, patch, AsyncMock

def test_send_notification(user_service):
    with patch("myapp.services.email_client") as mock_email:
        mock_email.send = Mock(return_value=True)
        user_service.notify(user_id=1, message="Hello")
        mock_email.send.assert_called_once_with(
            to="test@example.com",
            body="Hello",
        )

# Async mocking
@pytest.mark.asyncio
async def test_fetch_data():
    with patch("myapp.client.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"status": "ok"}
        result = await process_data()
        assert result["status"] == "ok"
```

### conftest.py Patterns

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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
```

---

## Go Testing

### Table-Driven Tests

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        amount   float64
        code     string
        want     float64
        wantErr  bool
    }{
        {
            name:   "valid 10% discount",
            amount: 100.0,
            code:   "SAVE10",
            want:   90.0,
        },
        {
            name:   "no discount",
            amount: 100.0,
            code:   "",
            want:   100.0,
        },
        {
            name:    "invalid code",
            amount:  100.0,
            code:    "INVALID",
            wantErr: true,
        },
        {
            name:   "zero amount",
            amount: 0,
            code:   "SAVE10",
            want:   0,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateDiscount(tt.amount, tt.code)
            if (err != nil) != tt.wantErr {
                t.Errorf("CalculateDiscount() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("CalculateDiscount() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Testify Assertions and Mocks

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/stretchr/testify/require"
)

// Mock
type MockUserRepo struct {
    mock.Mock
}

func (m *MockUserRepo) FindByID(id string) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func TestGetUser(t *testing.T) {
    repo := new(MockUserRepo)
    repo.On("FindByID", "123").Return(&User{ID: "123", Name: "John"}, nil)

    service := NewUserService(repo)
    user, err := service.GetUser("123")

    require.NoError(t, err)
    assert.Equal(t, "John", user.Name)
    repo.AssertExpectations(t)
}

// HTTP handler testing
func TestGetUserHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/users/123", nil)
    w := httptest.NewRecorder()

    handler := NewHandler(mockService)
    handler.GetUser(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var user User
    err := json.NewDecoder(w.Body).Decode(&user)
    require.NoError(t, err)
    assert.Equal(t, "123", user.ID)
}
```

---

## Rust Testing

### Unit and Integration Tests

```rust
// src/lib.rs - Unit tests (same file)
pub fn calculate_discount(amount: f64, percentage: f64) -> Result<f64, DiscountError> {
    if percentage < 0.0 || percentage > 100.0 {
        return Err(DiscountError::InvalidPercentage(percentage));
    }
    Ok(amount * (1.0 - percentage / 100.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_discount() {
        let result = calculate_discount(100.0, 10.0).unwrap();
        assert!((result - 90.0).abs() < f64::EPSILON);
    }

    #[test]
    fn test_zero_discount() {
        assert_eq!(calculate_discount(100.0, 0.0).unwrap(), 100.0);
    }

    #[test]
    fn test_invalid_percentage() {
        assert!(matches!(
            calculate_discount(100.0, 150.0),
            Err(DiscountError::InvalidPercentage(_))
        ));
    }

    #[test]
    fn test_negative_percentage() {
        assert!(calculate_discount(100.0, -10.0).is_err());
    }
}

// tests/integration_test.rs - Integration tests (separate file)
use my_crate::calculate_discount;

#[test]
fn test_full_workflow() {
    let original = 200.0;
    let discounted = calculate_discount(original, 25.0).unwrap();
    assert_eq!(discounted, 150.0);
}
```

### Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn discount_never_exceeds_original(amount in 0.0f64..10000.0, pct in 0.0f64..100.0) {
        let result = calculate_discount(amount, pct).unwrap();
        prop_assert!(result <= amount);
        prop_assert!(result >= 0.0);
    }

    #[test]
    fn roundtrip_serialization(name in "[a-zA-Z]{1,50}", age in 0u32..150) {
        let user = User { name: name.clone(), age };
        let json = serde_json::to_string(&user).unwrap();
        let deserialized: User = serde_json::from_str(&json).unwrap();
        prop_assert_eq!(user, deserialized);
    }
}
```

---

## Visual Regression Testing

### Playwright Screenshots

```typescript
import { test, expect } from "@playwright/test";

test("homepage visual regression", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage.png", {
    maxDiffPixelRatio: 0.01,
  });
});

test("component states", async ({ page }) => {
  await page.goto("/components");

  // Default state
  await expect(page.locator(".card")).toHaveScreenshot("card-default.png");

  // Hover state
  await page.locator(".card").hover();
  await expect(page.locator(".card")).toHaveScreenshot("card-hover.png");

  // Full page with specific viewport
  await page.setViewportSize({ width: 375, height: 812 }); // iPhone
  await expect(page).toHaveScreenshot("homepage-mobile.png");
});

// Update snapshots: npx playwright test --update-snapshots
```

### Percy (Cloud Visual Testing)

```typescript
import percySnapshot from "@percy/playwright";

test("visual test with Percy", async ({ page }) => {
  await page.goto("/dashboard");
  await percySnapshot(page, "Dashboard");
  // Percy compares across browsers and viewport sizes
});
```

### Chromatic (Storybook Visual Testing)

```bash
# Run Chromatic on Storybook stories
npx chromatic --project-token=<token>

# CI integration
# Chromatic captures every story as a visual snapshot
# and detects pixel-level changes across PRs
```

| Tool           | Approach                        | Best For                      |
| -------------- | ------------------------------- | ----------------------------- |
| **Playwright** | Local screenshot comparison     | E2E visual tests, free        |
| **Percy**      | Cloud cross-browser comparison  | Multi-browser, team review    |
| **Chromatic**  | Storybook story snapshots       | Component library visual QA   |

---

## See Also

- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Quality requirements
- Project `CLAUDE.md` - Testing rules
