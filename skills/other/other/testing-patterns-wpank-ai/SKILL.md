---
name: testing-patterns
model: standard
category: testing
description: Unit, integration, and E2E testing patterns with framework-specific guidance. Use when asked to "write tests", "add test coverage", "testing strategy", "test this function", "create test suite", "fix flaky tests", or "improve test quality".
version: 1.0
---

# Testing Patterns

> **Write tests that catch bugs, not tests that pass.** — Confidence through coverage, speed through isolation.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install testing-patterns
```


---

## Testing Pyramid

| Level | Ratio | Speed | Cost | Confidence | Scope |
|-------|-------|-------|------|------------|-------|
| **Unit** | ~70% | ms | Low | Low (isolated) | Single function/class |
| **Integration** | ~20% | seconds | Medium | Medium | Module boundaries, APIs, DB |
| **E2E** | ~10% | minutes | High | High (realistic) | Full user workflows |

> **Rule:** If your E2E tests outnumber your unit tests, invert the pyramid.

---

## Unit Testing Patterns

### Core Patterns

| Pattern | When to Use | Structure |
|---------|------------|-----------|
| **Arrange-Act-Assert** | Default for all unit tests | Setup, Execute, Verify |
| **Given-When-Then** | BDD-style, behavior-focused | Precondition, Action, Outcome |
| **Parameterized** | Same logic, multiple inputs | Data-driven test cases |
| **Snapshot** | UI components, serialized output | Compare against saved baseline |
| **Property-Based** | Mathematical invariants | Generate random inputs, assert properties |

### Arrange-Act-Assert (AAA)

The default structure for every unit test. Clear separation of setup, execution, and verification makes tests readable and maintainable.

```typescript
// Clean AAA structure
test('calculates order total with tax', () => {
  // Arrange
  const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
  const taxRate = 0.08;

  // Act
  const total = calculateTotal(items, taxRate);

  // Assert
  expect(total).toBe(27.0);
});
```

### Test Doubles

Use the right type of test double for the situation. Each serves a different purpose.

| Double | Purpose | When to Use | Example |
|--------|---------|-------------|---------|
| **Stub** | Returns canned data | Control indirect input | `jest.fn().mockReturnValue(42)` |
| **Mock** | Verifies interactions | Assert something was called | `expect(mock).toHaveBeenCalledWith('arg')` |
| **Spy** | Wraps real implementation | Observe without replacing | `jest.spyOn(service, 'save')` |
| **Fake** | Working simplified impl | Need realistic behavior | In-memory database, fake HTTP server |

```typescript
// Stub — control indirect input
const getUser = jest.fn().mockResolvedValue({ id: 1, name: 'Alice' });

// Spy — observe without replacing
const spy = jest.spyOn(logger, 'warn');
processInvalidInput(data);
expect(spy).toHaveBeenCalledWith('Invalid input received');

// Fake — lightweight substitute
class FakeUserRepo implements UserRepository {
  private users = new Map<string, User>();
  async save(user: User) { this.users.set(user.id, user); }
  async findById(id: string) { return this.users.get(id) ?? null; }
}
```

### Parameterized Tests

Use parameterized tests when the same logic needs verification with multiple inputs. This eliminates copy-paste tests while providing comprehensive coverage.

```typescript
// Vitest/Jest
test.each([
  ['hello', 'HELLO'],
  ['world', 'WORLD'],
  ['', ''],
  ['123abc', '123ABC'],
])('toUpperCase(%s) returns %s', (input, expected) => {
  expect(input.toUpperCase()).toBe(expected);
});
```

```python
# pytest
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_to_upper(input, expected):
    assert input.upper() == expected
```

```go
// Go — table-driven tests (idiomatic)
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"zero", 0, 0, 0},
        {"negative", -1, -2, -3},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            if got := Add(tc.a, tc.b); got != tc.expected {
                t.Errorf("Add(%d,%d) = %d, want %d", tc.a, tc.b, got, tc.expected)
            }
        })
    }
}
```

---

## Integration Testing Patterns

### Database Testing Strategies

| Strategy | Approach | Trade-off |
|----------|----------|-----------|
| **Transaction rollback** | Wrap each test in a transaction, rollback after | Fast, but hides commit bugs |
| **Fixtures/seeds** | Load known data before suite | Predictable, but brittle if schema changes |
| **Factory functions** | Generate data programmatically | Flexible, but more setup code |
| **Testcontainers** | Spin up real DB in Docker | Realistic, but slower startup |

```typescript
// Transaction rollback pattern (Prisma)
beforeEach(async () => {
  await prisma.$executeRaw`BEGIN`;
});
afterEach(async () => {
  await prisma.$executeRaw`ROLLBACK`;
});

test('creates user in database', async () => {
  const user = await createUser({ name: 'Alice', email: 'a@b.com' });
  const found = await prisma.user.findUnique({ where: { id: user.id } });
  expect(found?.name).toBe('Alice');
});
```

### API Testing

```typescript
// Supertest (Node.js)
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  it('creates a user and returns 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com' })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      name: 'Alice',
    });
  });

  it('returns 400 for invalid email', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'not-an-email' })
      .expect(400);
  });
});
```

---

## Mocking Best Practices

### Mock Boundaries, Not Implementations

The fundamental rule: mock at system boundaries (external APIs, databases, file systems) and never mock internal domain logic.

```typescript
// BAD — mocking internal implementation
jest.mock('./utils/formatDate');  // Breaks on refactor

// GOOD — mocking external boundary
jest.mock('./services/paymentGateway');  // Third-party API is the boundary
```

### When to Mock vs Not Mock

| Mock | Don't Mock |
|------|-----------|
| HTTP APIs, external services | Pure functions |
| Database (in unit tests) | Your own domain logic |
| File system, network | Data transformations |
| Time/Date (`Date.now`) | Simple calculations |
| Environment variables | Internal class methods |

### Dependency Injection for Testability

Structure code so dependencies can be swapped in tests. This is the single most impactful pattern for testable code.

```typescript
// Injectable dependencies — easy to test
class OrderService {
  constructor(
    private paymentGateway: PaymentGateway,
    private inventory: InventoryService,
    private notifier: NotificationService,
  ) {}

  async placeOrder(order: Order): Promise<OrderResult> {
    const stock = await this.inventory.check(order.items);
    if (!stock.available) return { status: 'out_of_stock' };

    const payment = await this.paymentGateway.charge(order.total);
    if (!payment.success) return { status: 'payment_failed' };

    await this.notifier.send(order.userId, 'Order confirmed');
    return { status: 'confirmed', id: payment.transactionId };
  }
}

// In tests — inject fakes
const service = new OrderService(
  new FakePaymentGateway(),
  new FakeInventory({ available: true }),
  new FakeNotifier(),
);
```

---

## Framework Quick Reference

| Framework | Language | Type | Test Runner | Assertion |
|-----------|----------|------|-------------|-----------|
| **Jest** | JS/TS | Unit/Integration | Built-in | `expect()` |
| **Vitest** | JS/TS | Unit/Integration | Vite-native | `expect()` (Jest-compatible) |
| **Playwright** | JS/TS/Python | E2E | Built-in | `expect()` / locators |
| **Cypress** | JS/TS | E2E | Built-in | `cy.should()` |
| **pytest** | Python | Unit/Integration | Built-in | `assert` |
| **Go testing** | Go | Unit/Integration | `go test` | `t.Error()` / testify |
| **Rust** | Rust | Unit/Integration | `cargo test` | `assert!()` / `assert_eq!()` |
| **JUnit 5** | Java/Kotlin | Unit/Integration | Built-in | `assertEquals()` |
| **RSpec** | Ruby | Unit/Integration | Built-in | `expect().to` |
| **PHPUnit** | PHP | Unit/Integration | Built-in | `$this->assert*()` |
| **xUnit** | C# | Unit/Integration | Built-in | `Assert.Equal()` |

---

## Test Quality Checklist

| Quality | Rule | Why |
|---------|------|-----|
| **Deterministic** | Same input produces same result, every time | Flaky tests erode trust |
| **Isolated** | No shared mutable state between tests | Order-dependent tests break in CI |
| **Fast** | Unit: < 10ms, Integration: < 1s, E2E: < 30s | Slow tests don't get run |
| **Readable** | Test name describes the scenario and expectation | Tests are documentation |
| **Maintainable** | Change one behavior, change one test | Brittle tests slow development |
| **Focused** | One logical assertion per test | Failures pinpoint the problem |

> **Naming convention:** `test_[unit]_[scenario]_[expected result]` or `should [do X] when [condition Y]`

---

## Coverage Strategy

### When to Aim for What

| Target | When | Rationale |
|--------|------|-----------|
| **80%+ line coverage** | Business logic, utilities, core domain | High ROI — catches most regressions |
| **90%+ branch coverage** | Payment processing, auth, security-critical | Edge cases matter here |
| **100% coverage** | Almost never — diminishing returns | Getter/setter tests add noise, not confidence |
| **Mutation testing** | Critical paths after coverage is high | Verifies tests actually catch bugs |

### What NOT to Test

| Skip | Reason |
|------|--------|
| Generated code (Prisma client, protobuf) | Maintained by tooling |
| Third-party library internals | Not your responsibility |
| Simple getters/setters | No logic to verify |
| Configuration files | Test the behavior they configure instead |
| Console.log / print statements | Side effects with no business value |

---

## Test Organization

```
src/
├── services/
│   ├── order.service.ts
│   └── order.service.test.ts      # Co-located unit tests
├── api/
│   └── routes/
│       └── orders.ts
tests/
├── integration/
│   ├── api/
│   │   └── orders.test.ts         # API integration tests
│   └── db/
│       └── order.repo.test.ts     # DB integration tests
├── e2e/
│   ├── pages/                     # Page objects
│   │   └── checkout.page.ts
│   └── specs/
│       └── checkout.spec.ts       # E2E specs
└── helpers/
    ├── factories.ts               # Test data factories
    └── setup.ts                   # Global test setup
```

> **Rule:** Co-locate unit tests with source. Separate integration and E2E tests into dedicated directories.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Testing implementation** | Tests break on refactor, not on bugs | Test behavior and outputs, not internals |
| **Flaky tests** | Non-deterministic failures erode CI trust | Remove time/order/network dependencies |
| **Test pollution** | Shared mutable state leaks between tests | Reset state in `beforeEach` / `setUp` |
| **Sleeping in tests** | `sleep(2000)` is slow and unreliable | Use explicit waits, polling, or events |
| **Giant arrange** | 50 lines of setup obscure intent | Extract factories/builders/fixtures |
| **Assert-free tests** | Test runs but verifies nothing | Every test must assert or expect |
| **Overmocking** | Mocking everything tests nothing real | Only mock external boundaries |
| **Copy-paste tests** | Duplicated tests diverge and rot | Use parameterized tests or helpers |
| **Testing the framework** | Verifying library code works | Test *your* logic, trust dependencies |
| **Ignoring test failures** | `skip`, `xit`, `@Disabled` accumulate | Fix or delete — never hoard skipped tests |
| **Tight coupling to DB** | Tests fail when schema changes | Use repository pattern + fakes for unit tests |
| **One giant test** | Single test covers 10 scenarios | Split into focused, named tests |
| **No test for bug fix** | Regression reappears later | Every bug fix gets a regression test |

---

## NEVER Do

1. **NEVER test implementation details instead of behavior** — tests must verify what the code does, not how it does it
2. **NEVER use `sleep()` in tests** — use explicit waits, polling, events, or assertions that auto-retry
3. **NEVER share mutable state between tests** — each test sets up and tears down its own state
4. **NEVER write assert-free tests** — a test that asserts nothing proves nothing
5. **NEVER mock internal domain logic** — only mock at system boundaries (network, DB, filesystem, clock)
6. **NEVER skip tests without a linked issue and a plan to re-enable** — skipped tests rot into permanent gaps
7. **NEVER leave a test suite in a failing state** — fix it or remove it with justification before moving on
8. **NEVER chase 100% coverage as a goal** — coverage percentage is a tool, not a target; strong assertions on critical paths beat weak assertions everywhere

---

## Summary

| Do | Don't |
|----|-------|
| Test behavior, not implementation | Mock everything in sight |
| Write the test before fixing a bug | Skip tests to ship faster |
| Keep tests fast and deterministic | Use `sleep()` or shared state |
| Use factories for test data | Copy-paste setup across tests |
| Mock at system boundaries | Mock internal functions |
| Name tests descriptively | Name tests `test1`, `test2` |
| Run tests in CI on every push | Only run tests locally |
| Delete or fix skipped tests | Let `@skip` accumulate forever |
| Use parameterized tests for variants | Duplicate test code |
| Inject dependencies for testability | Hard-code dependencies |

> **Remember:** Tests are a safety net — a fast, trustworthy suite lets you refactor fearlessly and ship with confidence.
