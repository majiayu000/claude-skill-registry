---
name: testing-anti-patterns
description: "Use to avoid critical testing mistakes. Five Iron Laws: Never test mock behavior, Never add test-only methods, Never mock without understanding, Always integration test, Always test error paths."
---

# Testing Anti-Patterns

## Core Principle

Avoid the five critical testing mistakes that undermine test value and create false confidence.

## When to Use This Skill

- Writing new tests
- Reviewing test code
- Debugging failing tests
- Test suite feels fragile
- Tests pass but bugs still occur
- Refactoring breaks many tests
- Unsure how to test something

## The Five Iron Laws

### 1. NEVER TEST MOCK BEHAVIOR

**If your test only verifies mock interactions, it tests nothing.**

```php
// ❌ BAD: Testing the mock, not the system
public function test_user_service_calls_repository()
{
    $mockRepo = $this->createMock(UserRepository::class);
    $mockRepo->expects($this->once())
             ->method('save')
             ->with($this->isInstanceOf(User::class));

    $service = new UserService($mockRepo);
    $service->createUser(['name' => 'John']);

    // This test passes if mock is called
    // But does the system actually work? Unknown!
}

// ✅ GOOD: Test actual behavior
public function test_user_service_creates_user()
{
    $service = new UserService(new UserRepository());
    $user = $service->createUser(['name' => 'John']);

    $this->assertDatabaseHas('users', ['name' => 'John']);
    $this->assertEquals('John', $user->name);
    // Tests actual system behavior, not mocks
}
```

### 2. NEVER ADD TEST-ONLY METHODS

**If code only exists for testing, your test is wrong.**

```php
// ❌ BAD: Test-only method
class UserService
{
    private $repository;

    public function __construct(UserRepository $repository)
    {
        $this->repository = $repository;
    }

    // This method ONLY exists for testing!
    public function getRepositoryForTesting()
    {
        return $this->repository;
    }
}

public function test_user_service_uses_repository()
{
    $service = new UserService($repo);
    $this->assertSame($repo, $service->getRepositoryForTesting());
    // Testing implementation, not behavior
}

// ✅ GOOD: Test observable behavior
public function test_user_service_saves_user()
{
    $service = new UserService(new UserRepository());
    $user = $service->createUser(['name' => 'John']);

    // Test through public API, not internals
    $this->assertTrue($user->exists);
}
```

### 3. NEVER MOCK WITHOUT UNDERSTANDING

**If you don't understand what you're mocking, your test is worthless.**

```php
// ❌ BAD: Mocking without understanding
public function test_payment_processing()
{
    // What does StripeClient actually do? Unknown!
    $mockStripe = $this->createMock(StripeClient::class);
    $mockStripe->method('charge')->willReturn(true);

    $service = new PaymentService($mockStripe);
    $result = $service->processPayment($order);

    $this->assertTrue($result);
    // But does this match real Stripe behavior? Unknown!
}

// ✅ GOOD: Understand what you're mocking
public function test_payment_processing()
{
    // I understand Stripe returns PaymentIntent object
    // with specific structure and states
    $mockStripe = $this->createMock(StripeClient::class);
    $mockStripe->method('charge')
               ->willReturn(new PaymentIntent([
                   'id' => 'pi_123',
                   'status' => 'succeeded',
                   'amount' => 1000,
               ]));

    $service = new PaymentService($mockStripe);
    $result = $service->processPayment($order);

    // Test that we handle PaymentIntent correctly
    $this->assertEquals('pi_123', $result->transaction_id);
    $this->assertEquals('succeeded', $result->status);
}
```

### 4. INTEGRATION TESTS ARE NOT AN AFTERTHOUGHT

**Integration tests should be written ALONGSIDE unit tests.**

```php
// ❌ BAD: Only unit tests
// unit/UserServiceTest.php
public function test_create_user()
{
    $mockRepo = $this->createMock(UserRepository::class);
    $service = new UserService($mockRepo);
    // ... test with mocks only
}

// Seems fine, but does the REAL system work?
// Does UserService work with REAL UserRepository?
// Does UserRepository work with REAL database?
// Unknown until production!

// ✅ GOOD: Unit AND integration tests
// unit/UserServiceTest.php
public function test_user_creation_logic()
{
    $mockRepo = $this->createMock(UserRepository::class);
    $mockRepo->method('save')->willReturn(true);

    $service = new UserService($mockRepo);
    $user = $service->createUser(['name' => 'John']);

    $this->assertEquals('John', $user->name);
}

// integration/UserServiceIntegrationTest.php
public function test_user_creation_with_real_database()
{
    $repo = new UserRepository();
    $service = new UserService($repo);

    $user = $service->createUser(['name' => 'John']);

    // Tests entire stack
    $this->assertDatabaseHas('users', ['name' => 'John']);
    $found = User::where('name', 'John')->first();
    $this->assertNotNull($found);
}
```

### 5. ALWAYS TEST ERROR PATHS

**The happy path is 10% of your code. The other 90% is error handling.**

```php
// ❌ BAD: Only testing success
public function test_user_registration()
{
    $response = $this->postJson('/api/register', [
        'email' => 'john@example.com',
        'password' => 'secret123',
    ]);

    $response->assertStatus(200);
    // What about validation errors?
    // What about duplicate emails?
    // What about database failures?
}

// ✅ GOOD: Test happy path AND error paths
public function test_user_registration_success()
{
    $response = $this->postJson('/api/register', [
        'email' => 'john@example.com',
        'password' => 'secret123',
    ]);

    $response->assertStatus(200);
}

public function test_registration_requires_email()
{
    $response = $this->postJson('/api/register', [
        'password' => 'secret123',
    ]);

    $response->assertStatus(422)
             ->assertJsonValidationErrors('email');
}

public function test_registration_rejects_duplicate_email()
{
    User::factory()->create(['email' => 'john@example.com']);

    $response = $this->postJson('/api/register', [
        'email' => 'john@example.com',
        'password' => 'secret123',
    ]);

    $response->assertStatus(422)
             ->assertJsonValidationErrors('email');
}

public function test_registration_handles_database_failure()
{
    // Simulate database down
    DB::shouldReceive('transaction')
      ->andThrow(new QueryException());

    $response = $this->postJson('/api/register', [
        'email' => 'john@example.com',
        'password' => 'secret123',
    ]);

    $response->assertStatus(500);
}
```

## The Four Major Anti-Patterns

### Anti-Pattern 1: Testing Mocks Instead of Behavior

```
What it looks like:
- Tests verify mock method calls
- Tests check mock expectations
- No assertions on actual behavior
- Tests pass but code doesn't work

Why it happens:
- Misunderstanding of mocking purpose
- Following bad examples
- Cargo cult testing
- Not understanding what to test

The fix:
1. Mock only external dependencies
2. Assert on observable behavior
3. Verify actual outcomes
4. Test through public API

Example:
```php
// ❌ TESTS MOCK
public function test_email_is_sent()
{
    $mockMailer = $this->createMock(Mailer::class);
    $mockMailer->expects($this->once())
               ->method('send');

    $service = new NotificationService($mockMailer);
    $service->notifyUser($user);

    // Test passes if mock.send() was called
    // But was email actually sent? Unknown!
}

// ✅ TESTS BEHAVIOR
public function test_email_is_sent()
{
    Mail::fake();

    $service = new NotificationService();
    $service->notifyUser($user);

    Mail::assertSent(NotificationEmail::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
    // Tests that email was actually sent
}
```
```

### Anti-Pattern 2: Test-Only Methods and Properties

```
What it looks like:
- Methods named "...ForTesting()"
- Public methods only used by tests
- Properties made public for testing
- Protected changed to public for tests

Why it happens:
- Can't figure out how to test properly
- Testing implementation instead of behavior
- Not using dependency injection
- Over-mocking

The fix:
1. Test through public API only
2. If you can't test it, redesign it
3. Use proper dependency injection
4. Test behavior, not implementation

Example:
```php
// ❌ TEST-ONLY METHOD
class OrderProcessor
{
    private $validator;

    // This method ONLY for testing!
    public function getValidatorForTesting()
    {
        return $this->validator;
    }
}

public function test_processor_has_validator()
{
    $processor = new OrderProcessor();
    $this->assertInstanceOf(
        Validator::class,
        $processor->getValidatorForTesting()
    );
}

// ✅ TEST BEHAVIOR
class OrderProcessor
{
    private $validator;

    public function process(Order $order): bool
    {
        if (!$this->validator->isValid($order)) {
            return false;
        }
        // ... process order
        return true;
    }
}

public function test_processor_rejects_invalid_order()
{
    $processor = new OrderProcessor();
    $invalidOrder = new Order(['total' => -100]);

    $result = $processor->process($invalidOrder);

    $this->assertFalse($result);
    // Tests validation through behavior, not internals
}
```
```

### Anti-Pattern 3: Incomplete or Incorrect Mocks

```
What it looks like:
- Mock returns wrong data types
- Mock behavior doesn't match real object
- Mock is missing key behaviors
- Tests pass but production fails

Why it happens:
- Don't understand the mocked dependency
- Copy/paste mock setup
- Mock created before understanding real behavior
- No integration tests to catch mismatches

The fix:
1. Understand what you're mocking FIRST
2. Make mock behavior match reality
3. Write integration tests alongside unit tests
4. Consider using real object instead

Example:
```php
// ❌ INCORRECT MOCK
public function test_api_client_handles_response()
{
    $mockClient = $this->createMock(HttpClient::class);
    $mockClient->method('get')->willReturn([
        'data' => 'something'
    ]);
    // Real API returns Response object, not array!

    $service = new ApiService($mockClient);
    $result = $service->fetchData();

    // Test passes but production will fail!
}

// ✅ CORRECT MOCK
public function test_api_client_handles_response()
{
    // I understand HttpClient returns Response object
    $mockResponse = new Response(200, [], json_encode([
        'data' => 'something'
    ]));

    $mockClient = $this->createMock(HttpClient::class);
    $mockClient->method('get')->willReturn($mockResponse);
    // Mock matches real behavior

    $service = new ApiService($mockClient);
    $result = $service->fetchData();

    $this->assertEquals('something', $result);
}

// ✅ EVEN BETTER: Integration test too
public function test_api_service_with_real_client()
{
    // Use real HTTP client with test endpoint
    $client = new HttpClient();
    $service = new ApiService($client);

    $result = $service->fetchData();

    // Tests with real HTTP client
    $this->assertNotNull($result);
}
```
```

### Anti-Pattern 4: Integration Testing as Afterthought

```
What it looks like:
- Only unit tests with mocks
- Integration tests added "later" (never)
- No end-to-end tests
- Bugs found in production

Why it happens:
- "Unit tests are enough" mentality
- Integration tests seen as slower/harder
- Prioritizing coverage over confidence
- Not understanding test pyramid

The fix:
1. Write integration tests alongside unit tests
2. Test full stack for critical paths
3. Use test-driven-development for both
4. Balance unit and integration tests

Example:
```php
// ❌ ONLY UNIT TESTS
class OrderServiceTest extends TestCase
{
    public function test_creates_order()
    {
        $mockRepo = $this->createMock(OrderRepository::class);
        $mockPayment = $this->createMock(PaymentService::class);
        $mockInventory = $this->createMock(InventoryService::class);

        $service = new OrderService($mockRepo, $mockPayment, $mockInventory);
        $order = $service->createOrder($items);

        // Everything mocked, does real system work? Unknown!
    }
}

// ✅ UNIT AND INTEGRATION TESTS
// unit/OrderServiceTest.php
class OrderServiceTest extends TestCase
{
    public function test_order_creation_logic()
    {
        // Mock external dependencies only
        $mockPayment = $this->createMock(PaymentService::class);
        $mockPayment->method('charge')->willReturn(true);

        $service = new OrderService(
            new OrderRepository(),
            $mockPayment,
            new InventoryService()
        );

        $order = $service->createOrder($items);

        $this->assertNotNull($order->id);
        $this->assertEquals('pending', $order->status);
    }
}

// integration/OrderServiceIntegrationTest.php
class OrderServiceIntegrationTest extends TestCase
{
    public function test_full_order_flow()
    {
        // No mocks, test entire stack
        $service = new OrderService(
            new OrderRepository(),
            new PaymentService(),
            new InventoryService()
        );

        $order = $service->createOrder($items);

        // Verify database
        $this->assertDatabaseHas('orders', ['id' => $order->id]);

        // Verify inventory reduced
        $this->assertDatabaseHas('inventory', [
            'product_id' => $items[0]->id,
            'quantity' => $originalQuantity - $items[0]->quantity
        ]);

        // Verify payment recorded
        $this->assertDatabaseHas('payments', [
            'order_id' => $order->id,
            'status' => 'completed'
        ]);

        // Tests REAL system integration
    }
}
```
```

## Recognizing Anti-Patterns in the Wild

### Red Flag 1: High Mock-to-Assertion Ratio

```php
// 🚩 RED FLAG
public function test_something()
{
    // 20 lines of mock setup
    $mock1->expects($this->once())->method('foo');
    $mock2->expects($this->once())->method('bar');
    $mock3->expects($this->once())->method('baz');
    // ... 17 more lines ...

    $service->doSomething();

    // 1 assertion
    $this->assertTrue(true);

    // Ratio: 20:1 mock:assertion
    // Probably testing mocks, not behavior!
}
```

### Red Flag 2: Tests Break on Refactoring

```php
// 🚩 RED FLAG
public function test_user_service()
{
    $mockRepo = $this->createMock(UserRepository::class);
    $mockRepo->expects($this->once())->method('save');

    $service = new UserService($mockRepo);
    $service->createUser(['name' => 'John']);
}

// Refactor: Rename save() to persist()
class UserRepository
{
    public function persist(User $user) { } // Renamed!
}

// Test breaks! Even though behavior unchanged
// This indicates testing implementation, not behavior
```

### Red Flag 3: Test Names Don't Describe Behavior

```php
// 🚩 RED FLAGS
public function test_calls_repository() { }
public function test_uses_correct_method() { }
public function test_mocks_are_called() { }

// These describe implementation, not behavior!

// ✅ GOOD
public function test_creates_user_in_database() { }
public function test_rejects_invalid_email() { }
public function test_sends_welcome_email() { }

// These describe observable behavior
```

### Red Flag 4: Can't Run Tests Independently

```php
// 🚩 RED FLAG
public function test_step_1_creates_user()
{
    $this->user = User::create(['name' => 'John']);
    $this->assertNotNull($this->user->id);
}

public function test_step_2_updates_user()
{
    // Depends on test_step_1 running first!
    $this->user->update(['name' => 'Jane']);
    $this->assertEquals('Jane', $this->user->name);
}

// Tests must be independent!
// This is test pollution
```

## How to Fix Anti-Patterns

### Fix 1: Convert Mock Tests to Behavior Tests

```php
// BEFORE: Testing mocks
public function test_notification_sent()
{
    $mockMailer->expects($this->once())->method('send');
    $service->notifyUser($user);
}

// AFTER: Testing behavior
public function test_notification_sent()
{
    Mail::fake();
    $service->notifyUser($user);
    Mail::assertSent(NotificationEmail::class);
}
```

### Fix 2: Remove Test-Only Methods

```php
// BEFORE: Test-only method
class Service
{
    private $dep;
    public function getDepForTesting() { return $this->dep; }
}

// AFTER: Test through behavior
class Service
{
    private $dep;
    // No test-only methods

    public function process() {
        return $this->dep->doSomething();
    }
}

// Test the process() result, not internal dep
```

### Fix 3: Add Integration Tests

```php
// BEFORE: Only unit tests with mocks
public function test_with_mocks()
{
    $mockDb = $this->createMock(Database::class);
    // ... test with mocks only
}

// AFTER: Add integration test
public function test_with_real_database()
{
    // Use real database
    $service = new Service(new Database());
    $result = $service->process();
    $this->assertDatabaseHas('results', ['data' => $result]);
}
```

### Fix 4: Test Error Paths

```php
// BEFORE: Only happy path
public function test_success_case() { }

// AFTER: Happy path AND error paths
public function test_success_case() { }
public function test_validation_errors() { }
public function test_database_failure() { }
public function test_network_timeout() { }
public function test_invalid_input() { }
```

## Integration with Skills

**Use with:**
- `test-driven-development` - Avoid anti-patterns from start
- `code-review` - Catch anti-patterns in review
- `systematic-debugging` - Debug test issues

**Prevents:**
- False confidence from bad tests
- Tests that pass but code fails
- Brittle tests that break on refactoring

## Checklist

When writing tests:
- [ ] Not testing mock behavior
- [ ] No test-only methods
- [ ] Understand what I'm mocking
- [ ] Have integration tests
- [ ] Test error paths
- [ ] Test describes behavior
- [ ] Test is independent
- [ ] Refactoring won't break test

When reviewing tests:
- [ ] Check mock-to-assertion ratio
- [ ] Look for test-only methods
- [ ] Verify integration tests exist
- [ ] Check error path coverage
- [ ] Ensure tests describe behavior

## Authority

**This skill is based on:**
- "Growing Object-Oriented Software, Guided by Tests" (Freeman & Pryce)
- Martin Fowler's testing patterns
- Research on test effectiveness
- Professional testing practices

**Research**: Studies show proper testing reduces bugs by 40-80%, but anti-patterns reduce effectiveness to near zero.

**Social Proof**: All mature engineering teams avoid these anti-patterns.

## Your Commitment

When writing tests:
- [ ] I will not test mock behavior
- [ ] I will not add test-only methods
- [ ] I will understand what I mock
- [ ] I will write integration tests
- [ ] I will test error paths
- [ ] I will test behavior, not implementation
- [ ] I will keep tests independent

---

**Bottom Line**: Five Iron Laws prevent bad tests. Don't test mocks. Don't add test-only methods. Understand mocks. Write integration tests. Test error paths. Follow these, and your tests will actually protect you.
