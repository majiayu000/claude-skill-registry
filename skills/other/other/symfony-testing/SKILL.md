---
description: "Symfony testing — PHPUnit test organization, unit tests, integration tests, functional tests, TDD workflow, PHPStan, mocking ports, test patterns. Triggers on: test, PHPUnit, TDD, unit test, integration test, functional test, mock, testing, test driven, code quality, PHPStan"
---

# Symfony Testing

You are an expert in testing within Symfony hexagonal architecture.

## When to Activate

- User needs to write tests
- User asks about test organization or TDD
- User needs mocking strategies for ports
- User asks about PHPStan or code quality
- User mentions test-driven development

## Test Directory Structure (Mirrors src/)

```
tests/
├── Unit/
│   └── Domain/
│       └── {Module}/
│           ├── Entity/
│           │   └── {Entity}Test.php
│           └── ValueObject/
│               └── {ValueObject}Test.php
├── Integration/
│   └── Application/
│       └── {Module}/
│           ├── Command/
│           │   └── {Handler}Test.php
│           └── Query/
│               └── {Handler}Test.php
├── Functional/
│   └── Presentation/
│       └── {Module}/
│           └── API/
│               └── {Controller}Test.php
└── Support/
    └── Adapter/
        └── InMemory{Repository}.php
```

## Test Types by Layer

### Unit Tests (Domain) — Pure PHP, no framework
```php
namespace Tests\Unit\Domain\User\ValueObject;

use App\Domain\User\ValueObject\Email;
use App\Domain\User\Exception\InvalidEmailException;
use PHPUnit\Framework\TestCase;

final class EmailTest extends TestCase
{
    public function test_valid_email_is_created(): void
    {
        $email = new Email('user@example.com');
        $this->assertSame('user@example.com', $email->value);
    }

    public function test_invalid_email_throws_exception(): void
    {
        $this->expectException(InvalidEmailException::class);
        new Email('invalid');
    }

    public function test_emails_are_equal(): void
    {
        $email1 = new Email('user@example.com');
        $email2 = new Email('user@example.com');
        $this->assertTrue($email1->equals($email2));
    }
}
```

### Integration Tests (Application) — Mock ports
```php
namespace Tests\Integration\Application\User\Command;

use App\Application\User\Command\RegisterUser;
use App\Application\User\Command\RegisterUserHandler;
use App\Domain\User\Port\UserRepositoryInterface;
use PHPUnit\Framework\TestCase;

final class RegisterUserHandlerTest extends TestCase
{
    public function test_it_registers_a_user(): void
    {
        $repository = $this->createMock(UserRepositoryInterface::class);
        $repository->expects($this->once())->method('save');
        $repository->method('existsByEmail')->willReturn(false);

        $handler = new RegisterUserHandler($repository);
        $result = $handler(new RegisterUser('test@example.com', 'Test', 'password123'));

        $this->assertNotEmpty($result);
    }
}
```

### Functional Tests (Presentation) — Full HTTP stack
```php
namespace Tests\Functional\Presentation\User\API;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

final class UserControllerTest extends WebTestCase
{
    public function test_create_user(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/users', [], [], [
            'CONTENT_TYPE' => 'application/json',
        ], json_encode([
            'email' => 'test@example.com',
            'name' => 'Test User',
            'password' => 'Password123',
        ]));

        $this->assertResponseStatusCodeSame(201);
        $response = json_decode($client->getResponse()->getContent(), true);
        $this->assertNotNull($response['result']['id']);
        $this->assertNull($response['error']);
    }
}
```

## TDD Workflow

1. Write test first (RED)
2. Write minimal code to pass (GREEN)
3. Refactor (REFACTOR)
4. Run PHPStan
5. Repeat

## References

See `references/` for detailed guides:
- `test-organization.md` — phpunit.xml config, test suites, fixtures
- `test-patterns.md` — In-memory adapters, test builders, assertion helpers
