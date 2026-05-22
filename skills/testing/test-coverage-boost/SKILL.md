---
name: test-coverage-boost
description: "Increase test coverage from 0% to 80%+ in ANY project, ANY testing framework"
---

# Test Coverage Boost - From Zero to Hero Testing

## 🎯 When to Use This Skill

Use when you need to:
- Add tests to untested code
- Increase coverage for CI/CD requirements
- Prepare for major refactoring
- Meet team coverage goals (usually 70-80%)
- Fix flaky or broken tests
- Implement TDD practices

## ⚡ Quick Coverage Check

### Check Current Coverage:

```bash
# JavaScript (Jest/Vitest)
npm test -- --coverage

# Python
pytest --cov=. --cov-report=html

# Go
go test -cover ./...

# Java
mvn clean test jacoco:report

# Ruby
bundle exec rspec --coverage

# .NET
dotnet test /p:CollectCoverage=true
```

## 📊 The Coverage Ladder (0% → 80%)

### Level 0: No Tests (0% coverage)
### Level 1: Critical Path (20% coverage)
### Level 2: Happy Path (40% coverage)
### Level 3: Edge Cases (60% coverage)
### Level 4: Error Handling (80% coverage)
### Level 5: Full Coverage (95%+)

## 🎯 Strategic Test Writing (80/20 Rule)

### WITH MCP (Test Generator):
```
"Generate tests for the most critical untested functions"
"Create tests to reach 80% coverage for [module]"
```

### WITHOUT MCP - Priority Order:

### 1. Test Business Critical Code First (20% effort → 80% value)

```javascript
// Priority 1: Money/Payment handling
test('calculateTotal should handle discounts correctly', () => {
  expect(calculateTotal(100, 0.2)).toBe(80); // 20% discount
  expect(calculateTotal(100, 0)).toBe(100);   // No discount
  expect(calculateTotal(100, 1)).toBe(0);     // 100% discount
});

// Priority 2: Authentication/Authorization
test('user should not access admin functions', () => {
  const user = { role: 'user' };
  expect(() => adminFunction(user)).toThrow('Unauthorized');
});

// Priority 3: Data validation
test('email validator should reject invalid emails', () => {
  expect(validateEmail('notanemail')).toBe(false);
  expect(validateEmail('test@example.com')).toBe(true);
});
```

### 2. The Test Writing Formula

```javascript
// Universal Test Structure (AAA Pattern)
test('should [expected behavior] when [condition]', () => {
  // Arrange - Set up test data
  const input = { /* test data */ };
  const expected = { /* expected result */ };

  // Act - Execute the function
  const result = functionUnderTest(input);

  // Assert - Verify the result
  expect(result).toEqual(expected);
});
```

## 📝 Test Patterns by Code Type

### 1. Pure Functions (Easiest to Test)

```javascript
// Function to test
function addTax(price, taxRate) {
  return price * (1 + taxRate);
}

// Tests
describe('addTax', () => {
  test('should add tax correctly', () => {
    expect(addTax(100, 0.1)).toBe(110);
  });

  test('should handle zero tax', () => {
    expect(addTax(100, 0)).toBe(100);
  });

  test('should handle negative price', () => {
    expect(addTax(-100, 0.1)).toBe(-110);
  });
});
```

### 2. Async Functions

```javascript
// Function to test
async function fetchUser(id) {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// Tests
describe('fetchUser', () => {
  test('should fetch user successfully', async () => {
    // Mock the API
    api.get = jest.fn().mockResolvedValue({
      data: { id: 1, name: 'John' }
    });

    const user = await fetchUser(1);
    expect(user.name).toBe('John');
  });

  test('should handle API errors', async () => {
    api.get = jest.fn().mockRejectedValue(new Error('Network error'));

    await expect(fetchUser(1)).rejects.toThrow('Network error');
  });
});
```

### 3. Classes/Objects

```javascript
// Class to test
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    this.items.push(item);
  }

  getTotal() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

// Tests
describe('ShoppingCart', () => {
  let cart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  test('should start empty', () => {
    expect(cart.items).toHaveLength(0);
  });

  test('should add items', () => {
    cart.addItem({ name: 'Book', price: 10 });
    expect(cart.items).toHaveLength(1);
  });

  test('should calculate total', () => {
    cart.addItem({ name: 'Book', price: 10 });
    cart.addItem({ name: 'Pen', price: 2 });
    expect(cart.getTotal()).toBe(12);
  });
});
```

### 4. API Endpoints

```javascript
// Express endpoint
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

// Tests
describe('GET /api/users/:id', () => {
  test('should return user when exists', async () => {
    const response = await request(app)
      .get('/api/users/1')
      .expect(200);

    expect(response.body).toHaveProperty('id', 1);
  });

  test('should return 404 when user not found', async () => {
    const response = await request(app)
      .get('/api/users/999')
      .expect(404);

    expect(response.body.error).toBe('Not found');
  });
});
```

## 🚀 Rapid Coverage Improvement Strategy

### Day 1: Foundation (0% → 20%)
```bash
# 1. Setup test infrastructure
npm install --save-dev jest @types/jest

# 2. Create test script
# package.json
"scripts": {
  "test": "jest",
  "test:coverage": "jest --coverage",
  "test:watch": "jest --watch"
}

# 3. Write first test for main function
echo "describe('app', () => {
  test('should start', () => {
    expect(true).toBe(true);
  });
});" > app.test.js
```

### Day 2: Critical Paths (20% → 40%)
```javascript
// Test the money flow
test('payment processing flow', async () => {
  // Test the entire payment pipeline
});

// Test user authentication
test('login flow', async () => {
  // Test login process end-to-end
});
```

### Day 3: Happy Paths (40% → 60%)
```javascript
// Test successful scenarios
test('user can create account', () => {});
test('user can update profile', () => {});
test('user can delete account', () => {});
```

### Day 4: Edge Cases (60% → 70%)
```javascript
// Test boundaries and limits
test('handles maximum input size', () => {});
test('handles empty input', () => {});
test('handles special characters', () => {});
```

### Day 5: Error Cases (70% → 80%)
```javascript
// Test error handling
test('handles network timeout', () => {});
test('handles invalid data', () => {});
test('handles concurrent access', () => {});
```

## 🎯 Coverage Improvement Techniques

### 1. Find Untested Code
```bash
# Generate coverage report
npm test -- --coverage

# Open HTML report
open coverage/index.html  # Mac
xdg-open coverage/index.html  # Linux
start coverage/index.html  # Windows

# Red lines = untested code
```

### 2. Test the Untestable

**Mocking External Dependencies:**
```javascript
// Mock database
jest.mock('./database', () => ({
  query: jest.fn(),
  connect: jest.fn()
}));

// Mock file system
jest.mock('fs', () => ({
  readFile: jest.fn((path, callback) => {
    callback(null, 'mock file content');
  })
}));

// Mock HTTP requests
jest.mock('axios');
axios.get.mockResolvedValue({ data: 'test' });
```

**Testing Private Methods:**
```javascript
// Option 1: Test through public interface
class Calculator {
  #privateMethod() { return 42; }
  publicMethod() { return this.#privateMethod(); }
}

test('private method via public', () => {
  const calc = new Calculator();
  expect(calc.publicMethod()).toBe(42);
});

// Option 2: Extract to separate testable function
function complexLogic(input) { /* ... */ }
export { complexLogic };  // Test directly
```

### 3. Parameterized Tests (Test Multiple Cases)

```javascript
// Jest
test.each([
  [1, 1, 2],
  [1, 2, 3],
  [2, 2, 4],
])('add(%i, %i) = %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});

// Python pytest
@pytest.mark.parametrize("input,expected", [
  (1, 2),
  (2, 4),
  (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

## 📊 Coverage Goals by Project Type

### Web Application
- **Controllers/Routes**: 90%+ (critical paths)
- **Business Logic**: 85%+ (core features)
- **Utilities**: 95%+ (pure functions)
- **UI Components**: 70%+ (focus on logic)
- **Database Models**: 80%+ (validations)

### API Service
- **Endpoints**: 95%+ (all routes)
- **Middleware**: 90%+ (auth, validation)
- **Services**: 85%+ (business logic)
- **Error Handlers**: 100% (critical)

### Library/Package
- **Public API**: 100% (all exports)
- **Core Logic**: 95%+ (main features)
- **Edge Cases**: 90%+ (robustness)
- **Examples**: 100% (documentation)

## 💡 Pro Tips

### Speed Up Test Writing:
```bash
# Generate test boilerplate
# VS Code: Install "Jest Snippets" extension
# Type: "desc" → describe block
# Type: "test" → test block
# Type: "exp" → expect statement
```

### Test Data Builders:
```javascript
// Create reusable test data
class UserBuilder {
  constructor() {
    this.user = {
      id: 1,
      name: 'Test User',
      email: 'test@example.com'
    };
  }

  withName(name) {
    this.user.name = name;
    return this;
  }

  withEmail(email) {
    this.user.email = email;
    return this;
  }

  build() {
    return this.user;
  }
}

// Usage
const user = new UserBuilder()
  .withName('John')
  .withEmail('john@example.com')
  .build();
```

### Coverage Exclusions:
```javascript
// Istanbul ignore comments
/* istanbul ignore next */  // Ignore next line
/* istanbul ignore if */    // Ignore if block
/* istanbul ignore else */  // Ignore else block

// Jest coverage config
// package.json
"jest": {
  "coveragePathIgnorePatterns": [
    "node_modules",
    "test-fixtures",
    ".mock.js"
  ],
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

## 🎯 Success Checklist

Your tests are good when:
- ✅ Coverage > 80%
- ✅ Tests run fast (< 1 minute)
- ✅ Tests are deterministic (no flakiness)
- ✅ Tests are readable (clear descriptions)
- ✅ Tests catch real bugs
- ✅ CI/CD pipeline includes tests
- ✅ Team writes tests for new features

Remember: 80% coverage with good tests > 100% coverage with bad tests! 🎯