---
name: acc-create-integration-test
description: Generates PHPUnit integration tests for PHP 8.5. Creates tests with real dependencies, database transactions, HTTP mocking. Supports repositories, API clients, message handlers.
---

# Integration Test Generator

Generates PHPUnit 11+ integration tests for PHP 8.5 infrastructure components.

## Characteristics

- **Real dependencies** — uses actual implementations
- **Database transactions** — rollback after each test
- **Isolated** — no cross-test contamination
- **Slower than unit** — acceptable for infrastructure testing

## Template

```php
<?php

declare(strict_types=1);

namespace Tests\Integration\{Namespace};

use {FullyQualifiedClassName};
use PHPUnit\Framework\Attributes\Group;
use Tests\IntegrationTestCase;

#[Group('integration')]
final class {ClassName}Test extends IntegrationTestCase
{
    private {ClassName} $sut;

    protected function setUp(): void
    {
        parent::setUp();
        $this->sut = $this->getContainer()->get({ClassName}::class);
        $this->beginTransaction();
    }

    protected function tearDown(): void
    {
        $this->rollbackTransaction();
        parent::tearDown();
    }

    public function test_{operation}_{scenario}(): void
    {
        // Arrange
        {arrange_code}

        // Act
        {act_code}

        // Assert
        {assert_code}
    }
}
```

## Base Test Case

```php
<?php

declare(strict_types=1);

namespace Tests;

use Doctrine\DBAL\Connection;
use PHPUnit\Framework\TestCase;
use Psr\Container\ContainerInterface;

abstract class IntegrationTestCase extends TestCase
{
    private static ?ContainerInterface $container = null;
    private ?Connection $connection = null;

    protected function getContainer(): ContainerInterface
    {
        if (self::$container === null) {
            self::$container = require __DIR__ . '/../config/container.php';
        }
        return self::$container;
    }

    protected function beginTransaction(): void
    {
        $this->connection = $this->getContainer()->get(Connection::class);
        $this->connection->beginTransaction();
    }

    protected function rollbackTransaction(): void
    {
        $this->connection?->rollBack();
    }

    protected function getConnection(): Connection
    {
        return $this->connection ?? $this->getContainer()->get(Connection::class);
    }
}
```

## Test Patterns by Component

### Repository Tests

```php
#[Group('integration')]
final class DoctrineOrderRepositoryTest extends IntegrationTestCase
{
    private OrderRepositoryInterface $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = $this->getContainer()->get(OrderRepositoryInterface::class);
        $this->beginTransaction();
    }

    protected function tearDown(): void
    {
        $this->rollbackTransaction();
        parent::tearDown();
    }

    // Save and retrieve
    public function test_saves_and_retrieves_order(): void
    {
        $order = OrderMother::pending();

        $this->repository->save($order);
        $found = $this->repository->findById($order->id());

        self::assertNotNull($found);
        self::assertTrue($order->id()->equals($found->id()));
    }

    // Update existing
    public function test_updates_existing_order(): void
    {
        $order = OrderMother::pending();
        $this->repository->save($order);

        $order->addItem(ProductMother::book(), 1);
        $order->confirm();
        $this->repository->save($order);

        $found = $this->repository->findById($order->id());
        self::assertTrue($found->isConfirmed());
    }

    // Delete
    public function test_deletes_order(): void
    {
        $order = OrderMother::pending();
        $this->repository->save($order);

        $this->repository->delete($order);

        $found = $this->repository->findById($order->id());
        self::assertNull($found);
    }

    // Not found
    public function test_returns_null_for_nonexistent(): void
    {
        $result = $this->repository->findById(OrderId::generate());

        self::assertNull($result);
    }

    // Query methods
    public function test_finds_orders_by_customer(): void
    {
        $customerId = CustomerId::generate();
        $order1 = OrderMother::forCustomer($customerId);
        $order2 = OrderMother::forCustomer($customerId);
        $order3 = OrderMother::forCustomer(CustomerId::generate());
        $this->repository->save($order1);
        $this->repository->save($order2);
        $this->repository->save($order3);

        $orders = $this->repository->findByCustomer($customerId);

        self::assertCount(2, $orders);
    }

    // Pagination
    public function test_paginates_results(): void
    {
        for ($i = 0; $i < 25; $i++) {
            $this->repository->save(OrderMother::pending());
        }

        $page1 = $this->repository->findAll(limit: 10, offset: 0);
        $page2 = $this->repository->findAll(limit: 10, offset: 10);
        $page3 = $this->repository->findAll(limit: 10, offset: 20);

        self::assertCount(10, $page1);
        self::assertCount(10, $page2);
        self::assertCount(5, $page3);
    }
}
```

### HTTP Client Tests

```php
use Symfony\Component\HttpClient\MockHttpClient;
use Symfony\Component\HttpClient\Response\MockResponse;

#[Group('integration')]
final class StripePaymentGatewayTest extends IntegrationTestCase
{
    public function test_charges_card_successfully(): void
    {
        // Arrange
        $mockResponse = new MockResponse(json_encode([
            'id' => 'ch_123',
            'status' => 'succeeded',
            'amount' => 1000,
        ]), ['http_code' => 200]);
        $httpClient = new MockHttpClient($mockResponse);
        $gateway = new StripePaymentGateway($httpClient, 'sk_test_xxx');

        // Act
        $result = $gateway->charge(
            Money::USD(1000),
            new CardToken('tok_visa')
        );

        // Assert
        self::assertTrue($result->isSuccessful());
        self::assertSame('ch_123', $result->transactionId());
    }

    public function test_handles_declined_card(): void
    {
        // Arrange
        $mockResponse = new MockResponse(json_encode([
            'error' => [
                'type' => 'card_error',
                'code' => 'card_declined',
            ],
        ]), ['http_code' => 402]);
        $httpClient = new MockHttpClient($mockResponse);
        $gateway = new StripePaymentGateway($httpClient, 'sk_test_xxx');

        // Act
        $result = $gateway->charge(
            Money::USD(1000),
            new CardToken('tok_chargeDeclined')
        );

        // Assert
        self::assertFalse($result->isSuccessful());
        self::assertSame('card_declined', $result->errorCode());
    }

    public function test_handles_network_error(): void
    {
        // Arrange
        $mockResponse = new MockResponse('', ['error' => 'Connection refused']);
        $httpClient = new MockHttpClient($mockResponse);
        $gateway = new StripePaymentGateway($httpClient, 'sk_test_xxx');

        // Assert
        $this->expectException(PaymentGatewayException::class);

        // Act
        $gateway->charge(Money::USD(1000), new CardToken('tok_visa'));
    }
}
```

### Message Handler Tests

```php
#[Group('integration')]
final class SendOrderConfirmationHandlerTest extends IntegrationTestCase
{
    private SendOrderConfirmationHandler $handler;
    private InMemoryMailer $mailer;

    protected function setUp(): void
    {
        parent::setUp();
        $this->mailer = new InMemoryMailer();
        $this->handler = new SendOrderConfirmationHandler(
            $this->getContainer()->get(OrderRepositoryInterface::class),
            $this->mailer
        );
        $this->beginTransaction();
    }

    protected function tearDown(): void
    {
        $this->rollbackTransaction();
        parent::tearDown();
    }

    public function test_sends_confirmation_email(): void
    {
        // Arrange
        $order = OrderMother::confirmed();
        $this->getRepository()->save($order);
        $message = new SendOrderConfirmation($order->id()->toString());

        // Act
        $this->handler->__invoke($message);

        // Assert
        $sentEmails = $this->mailer->getSentEmails();
        self::assertCount(1, $sentEmails);
        self::assertSame($order->customerEmail()->value, $sentEmails[0]->to);
    }

    public function test_throws_for_nonexistent_order(): void
    {
        // Arrange
        $message = new SendOrderConfirmation('nonexistent-id');

        // Assert
        $this->expectException(OrderNotFoundException::class);

        // Act
        $this->handler->__invoke($message);
    }
}
```

### Cache Tests

```php
#[Group('integration')]
final class RedisCacheAdapterTest extends IntegrationTestCase
{
    private RedisCacheAdapter $cache;

    protected function setUp(): void
    {
        parent::setUp();
        $redis = $this->getContainer()->get(Redis::class);
        $redis->flushDb();
        $this->cache = new RedisCacheAdapter($redis);
    }

    public function test_stores_and_retrieves_value(): void
    {
        $this->cache->set('key', 'value', 60);

        $result = $this->cache->get('key');

        self::assertSame('value', $result);
    }

    public function test_returns_null_for_missing_key(): void
    {
        $result = $this->cache->get('nonexistent');

        self::assertNull($result);
    }

    public function test_returns_default_for_missing_key(): void
    {
        $result = $this->cache->get('nonexistent', 'default');

        self::assertSame('default', $result);
    }

    public function test_deletes_key(): void
    {
        $this->cache->set('key', 'value', 60);

        $this->cache->delete('key');

        self::assertNull($this->cache->get('key'));
    }

    public function test_expires_after_ttl(): void
    {
        $this->cache->set('key', 'value', 1);

        sleep(2);

        self::assertNull($this->cache->get('key'));
    }
}
```

## Database Setup Options

### SQLite In-Memory

```xml
<!-- phpunit.xml -->
<php>
    <env name="DATABASE_URL" value="sqlite:///:memory:"/>
</php>
```

### Testcontainers

```php
use Testcontainers\Container\PostgreSqlContainer;

abstract class DatabaseTestCase extends TestCase
{
    protected static ?PostgreSqlContainer $postgres = null;

    public static function setUpBeforeClass(): void
    {
        self::$postgres = PostgreSqlContainer::make('15.0')
            ->withDatabase('test_db')
            ->start();
    }

    public static function tearDownAfterClass(): void
    {
        self::$postgres?->stop();
    }

    protected function getDsn(): string
    {
        return self::$postgres->getDsn();
    }
}
```

## Generation Instructions

1. **Identify component type:**
   - Repository → Database tests
   - HTTP Client → Mock HTTP responses
   - Message Handler → In-memory transport
   - Cache → Redis/in-memory tests

2. **Determine test cases:**
   - CRUD operations
   - Query methods
   - Error handling
   - Edge cases (not found, duplicates)

3. **Generate base test case if needed:**
   - Transaction management
   - Container access
   - Cleanup utilities

4. **Generate test class:**
   - Match namespace structure
   - Add `#[Group('integration')]`
   - Setup/teardown with transactions

5. **Add test data helpers:**
   - Use existing Mothers/Builders
   - Create fixtures for complex scenarios

## Usage

Provide:
- Path to infrastructure class
- Database type (SQLite/PostgreSQL/MySQL)
- External services to mock (optional)

The generator will:
1. Analyze the infrastructure class
2. Determine appropriate test patterns
3. Generate comprehensive integration tests
4. Include transaction management
