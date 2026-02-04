---
name: acc-detect-test-smells
description: Detects test antipatterns and code smells in PHP test suites. Identifies 15 smells (Logic in Test, Mock Overuse, Fragile Tests, Mystery Guest, etc.) with fix recommendations and refactoring patterns for testability.
---

# Test Smell Detection

Identifies antipatterns and code smells in PHP test suites.

## 15 Test Smells

### 1. Logic in Test

**Problem:** Test contains conditional logic (if/for/while).

**Detection:**
```bash
Grep: "if \(" --glob "tests/**/*Test.php"
Grep: "for \(" --glob "tests/**/*Test.php"
Grep: "while \(" --glob "tests/**/*Test.php"
Grep: "foreach \(" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
public function test_calculates_total(): void
{
    $items = [10, 20, 30];
    $total = 0;
    foreach ($items as $item) {  // ❌ Logic in test
        $total += $item;
    }
    self::assertEquals($total, $this->calculator->sum($items));
}
```

**Fix:** Use data providers or inline expected values.
```php
public function test_calculates_total(): void
{
    $items = [10, 20, 30];

    self::assertEquals(60, $this->calculator->sum($items));  // ✅
}
```

---

### 2. Mock Overuse

**Problem:** More than 3 mocks in a single test.

**Detection:**
```bash
Grep: "createMock\|createStub" --glob "tests/**/*Test.php" -C 20
# Count mocks per test method
```

**Example (Bad):**
```php
public function test_process_order(): void
{
    $repository = $this->createMock(OrderRepository::class);      // 1
    $mailer = $this->createMock(MailerInterface::class);          // 2
    $logger = $this->createMock(LoggerInterface::class);          // 3
    $eventDispatcher = $this->createMock(EventDispatcher::class); // 4
    $validator = $this->createMock(ValidatorInterface::class);    // 5 ❌
    // ...
}
```

**Fix:** Use Fakes, refactor design, or split test.
```php
public function test_process_order(): void
{
    $repository = new InMemoryOrderRepository();  // Fake
    $mailer = new CollectingMailer();             // Fake
    $eventDispatcher = new CollectingEventDispatcher(); // Fake
    // ...
}
```

---

### 3. Test Interdependence

**Problem:** Tests depend on execution order or shared state.

**Detection:**
```bash
Grep: "static \$" --glob "tests/**/*Test.php"
Grep: "self::\$[a-z]" --glob "tests/**/*Test.php"
# Check for @depends annotation
Grep: "@depends" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
private static array $createdUsers = [];  // ❌ Shared state

public function test_creates_user(): void
{
    $user = $this->service->create('john@example.com');
    self::$createdUsers[] = $user;
}

public function test_finds_created_user(): void
{
    $user = $this->service->find(self::$createdUsers[0]->id);  // ❌ Depends on previous
}
```

**Fix:** Each test creates its own data.
```php
public function test_finds_user(): void
{
    $user = UserMother::default();
    $this->repository->save($user);

    $found = $this->service->find($user->id);

    self::assertEquals($user->id, $found->id);
}
```

---

### 4. Fragile Test

**Problem:** Test breaks when implementation changes (not behavior).

**Detection:**
```bash
# Method call order verification
Grep: "expects\(.*exactly\|expects\(.*at\(" --glob "tests/**/*Test.php"
# Internal method testing
Grep: "->method\('_" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
$mock->expects($this->exactly(3))->method('process');  // ❌ Verifies HOW, not WHAT
$mock->expects($this->at(0))->method('first');
$mock->expects($this->at(1))->method('second');
```

**Fix:** Test outcomes, not call sequences.
```php
$this->service->processAll($items);

self::assertCount(3, $this->repository->findProcessed());  // ✅ Verifies WHAT
```

---

### 5. Mystery Guest

**Problem:** Test uses external files or hidden data sources.

**Detection:**
```bash
Grep: "file_get_contents\|fopen\|include\|require" --glob "tests/**/*Test.php"
Grep: "getenv\|_ENV\|_SERVER" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
public function test_imports_products(): void
{
    $data = json_decode(file_get_contents('fixtures/products.json'));  // ❌ Hidden
    // Where does this file come from? What's in it?
}
```

**Fix:** Inline test data or use explicit builders.
```php
public function test_imports_products(): void
{
    $data = [
        ['name' => 'Book', 'price' => 1000],
        ['name' => 'Pen', 'price' => 100],
    ];

    $this->importer->import($data);

    self::assertCount(2, $this->repository->findAll());
}
```

---

### 6. Eager Test

**Problem:** Single test verifies multiple unrelated behaviors.

**Detection:**
```bash
# Multiple assert groups with different subjects
Grep: "self::assert" --glob "tests/**/*Test.php" -C 5
# Count assertions per test method
```

**Example (Bad):**
```php
public function test_user_operations(): void
{
    // Testing creation
    $user = $this->service->create('john@example.com');
    self::assertNotNull($user);

    // Testing update (different behavior!)
    $user->setName('John');
    $this->service->update($user);
    self::assertEquals('John', $user->getName());

    // Testing deletion (another behavior!)
    $this->service->delete($user);
    self::assertNull($this->repository->find($user->id));
}
```

**Fix:** One test per behavior.
```php
public function test_creates_user(): void { ... }
public function test_updates_user_name(): void { ... }
public function test_deletes_user(): void { ... }
```

---

### 7. Assertion Roulette

**Problem:** Multiple assertions without messages, unclear which failed.

**Detection:**
```bash
# Count assertions per test method
Grep: "self::assert" --glob "tests/**/*Test.php"
# More than 5 assertions without context
```

**Example (Bad):**
```php
public function test_order_properties(): void
{
    self::assertEquals('pending', $order->status);
    self::assertEquals(100, $order->total);
    self::assertEquals(3, count($order->items));
    self::assertEquals('john@example.com', $order->customer->email);
    self::assertEquals('2024-01-01', $order->createdAt->format('Y-m-d'));
    // Which one failed?
}
```

**Fix:** Group related assertions or add messages.
```php
public function test_order_has_correct_status(): void
{
    self::assertEquals('pending', $order->status);
}

public function test_order_calculates_total(): void
{
    self::assertEquals(100, $order->total);
}
```

---

### 8. Obscure Test

**Problem:** Test purpose unclear from name or structure.

**Detection:**
```bash
# Generic test names
Grep: "test_it_works\|test_test\|test_foo" --glob "tests/**/*Test.php"
# Missing assertions
Grep: "function test_" --glob "tests/**/*Test.php" -A 10
```

**Example (Bad):**
```php
public function test_it_works(): void  // ❌ What works?
{
    $x = $this->service->doSomething($this->data);
    self::assertTrue($x);
}
```

**Fix:** Descriptive name following convention.
```php
public function test_calculate_total_with_discount_returns_reduced_price(): void
{
    // Clear intent
}
```

---

### 9. Test Code Duplication

**Problem:** Same setup/assertion code repeated across tests.

**Detection:**
```bash
# Repeated patterns across test methods
# Manual review or static analysis tools
```

**Example (Bad):**
```php
public function test_confirm_order(): void
{
    $order = new Order(OrderId::generate(), CustomerId::generate());
    $order->addItem(new Product('Book', Money::EUR(100)));
    // ... same setup in 10 tests
}
```

**Fix:** Extract to setUp, Builder, or Mother.
```php
protected function setUp(): void
{
    $this->order = OrderBuilder::anOrder()->withItem($this->book)->build();
}
```

---

### 10. Conditional Test Logic

**Problem:** Different assertions based on conditions.

**Detection:**
```bash
Grep: "if.*assert\|assert.*if" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
public function test_process(): void
{
    $result = $this->service->process($input);
    if ($result !== null) {  // ❌
        self::assertInstanceOf(Order::class, $result);
    } else {
        self::fail('Should not be null');
    }
}
```

**Fix:** Explicit assertions.
```php
public function test_process_returns_order(): void
{
    $result = $this->service->process($input);

    self::assertNotNull($result);
    self::assertInstanceOf(Order::class, $result);
}
```

---

### 11. Hard-Coded Test Data

**Problem:** Magic values without meaning.

**Detection:**
```bash
Grep: "'[a-z0-9]{8,}'" --glob "tests/**/*Test.php"
Grep: "12345\|999\|100" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
$order = new Order('550e8400-e29b-41d4-a716-446655440000');  // ❌ Magic UUID
$money = Money::EUR(12345);  // ❌ Magic number
```

**Fix:** Named constants or builders.
```php
private const KNOWN_ORDER_ID = 'order-123';

$order = OrderBuilder::anOrder()
    ->withId(OrderId::fromString(self::KNOWN_ORDER_ID))
    ->withTotal(Money::EUR(100))  // Meaningful amount
    ->build();
```

---

### 12. Testing Private Methods

**Problem:** Tests access private/protected methods directly.

**Detection:**
```bash
Grep: "setAccessible\(true\)" --glob "tests/**/*Test.php"
Grep: "ReflectionMethod\|ReflectionProperty" --glob "tests/**/*Test.php"
```

**Example (Bad):**
```php
$method = new ReflectionMethod(Order::class, 'calculateDiscount');
$method->setAccessible(true);
$result = $method->invoke($order, $amount);  // ❌ Testing internals
```

**Fix:** Test through public API.
```php
$order->applyDiscount($coupon);

self::assertEquals($expectedTotal, $order->total());  // ✅ Public API
```

---

### 13. Slow Test

**Problem:** Unit test takes >100ms.

**Detection:**
```bash
# Run PHPUnit with timing
phpunit --log-junit timing.xml
# Check for sleep, HTTP calls, file I/O
Grep: "sleep\|usleep\|file_\|curl_" --glob "tests/Unit/**/*Test.php"
```

**Fix:** Mock external dependencies, use in-memory implementations.

---

### 14. Mocking Final Classes

**Problem:** Attempting to mock final classes.

**Detection:**
```bash
# Find final classes
Grep: "final class" --glob "src/**/*.php"
# Cross-reference with mocks in tests
Grep: "createMock\(.*::" --glob "tests/**/*Test.php"
```

**Fix:** Mock interfaces, not implementations.
```php
// Bad: $mock = $this->createMock(FinalService::class);
// Good:
$mock = $this->createMock(ServiceInterface::class);
```

---

### 15. Mocking Value Objects

**Problem:** Mocking immutable value objects.

**Detection:**
```bash
# Find readonly classes (likely VOs)
Grep: "readonly class" --glob "src/**/*.php"
# Check if they're mocked
```

**Fix:** Use real value objects — they're simple and deterministic.
```php
// Bad: $email = $this->createMock(Email::class);
// Good:
$email = new Email('test@example.com');
```

## Output Format

```markdown
# Test Smell Report

## Summary

| Smell | Count | Severity |
|-------|-------|----------|
| Logic in Test | 5 | High |
| Mock Overuse | 3 | High |
| Mystery Guest | 2 | Medium |
| Eager Test | 8 | Medium |

## Findings

### Logic in Test (5 occurrences)

| File | Line | Code |
|------|------|------|
| OrderTest.php | 45 | `foreach ($items as $item)` |
| UserTest.php | 23 | `if ($result !== null)` |

**Recommendation:** Extract to data providers or inline values.

### Mock Overuse (3 occurrences)

| File | Test Method | Mock Count |
|------|-------------|------------|
| PaymentTest.php | test_process | 6 |
| OrderServiceTest.php | test_place | 5 |

**Recommendation:** Use Fakes (InMemory implementations) or split tests.

## Action Items

1. **High Priority**
   - Refactor `PaymentTest::test_process` — 6 mocks indicates design smell
   - Remove loops from `OrderTest` — use DataProvider

2. **Medium Priority**
   - Inline fixture data in `ImporterTest`
   - Split `UserTest::test_user_operations` into 3 tests

## Recommended Skills

| Smell | Fix With |
|-------|----------|
| Mock Overuse | `acc-create-mock-repository` |
| Mystery Guest | `acc-create-test-builder` |
| Test Duplication | `acc-create-test-builder` |
```

## Severity Matrix

| Smell | Severity | Impact |
|-------|----------|--------|
| Logic in Test | High | Unreliable results |
| Mock Overuse | High | Design problem indicator |
| Test Interdependence | High | Flaky tests |
| Fragile Test | High | Maintenance burden |
| Mocking Final/VO | High | Runtime errors |
| Mystery Guest | Medium | Hard to understand |
| Eager Test | Medium | Hard to diagnose failures |
| Slow Test | Medium | Development slowdown |
| Obscure Test | Low | Documentation issue |
| Hard-Coded Data | Low | Readability |

## Refactoring for Testability

See `references/refactoring-patterns.md` for detailed refactoring patterns:
- Extract Interface (Seam)
- Constructor Injection
- Replace Singleton with DI
- Break Temporal Coupling
- Extract Pure Function
- Replace new with Factory
- Testability Score Checklist
- Smell → Refactoring Matrix
