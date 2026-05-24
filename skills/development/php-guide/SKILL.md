---
name: php-guide
description: |
  PHP language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with PHP files (.php), composer.json, or when the user mentions PHP.
  Provides type declaration patterns, Composer conventions, PSR standards,
  and testing guidelines specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: php
  extensions: ".php"
---

# PHP Guide

> Applies to: PHP 8.1+, Web Applications, APIs, CLIs, Microservices

## Core Principles

1. **Strict Types Always**: Every PHP file starts with `declare(strict_types=1)`
2. **Type Declarations Everywhere**: All parameters, return types, and properties must have type declarations
3. **PSR Standards**: Follow PSR-12 coding standard, PSR-4 autoloading, PSR-7 HTTP messages
4. **Composition Over Inheritance**: Prefer interfaces, traits, and dependency injection over deep class hierarchies
5. **Modern PHP First**: Use PHP 8.1+ features (enums, readonly properties, fibers, named arguments, match expressions)

## Guardrails

### Version & Dependencies

- Target PHP 8.1+ (enums, readonly properties, fibers, intersection types)
- Define all dependencies in `composer.json` with version constraints
- Run `composer validate` and `composer audit` before committing
- Use `composer.lock` for applications (commit it), omit for libraries
- Separate `require-dev` for development-only dependencies
- Never use `composer update` in production (use `composer install --no-dev`)

### Code Style (PSR-12)

- Run PHP-CS-Fixer or PHP_CodeSniffer before every commit
- Naming: `PascalCase` classes/enums, `camelCase` methods/properties, `UPPER_SNAKE` constants
- One class per file, file name matches class name
- Opening braces on same line for control structures, next line for classes/methods
- `declare(strict_types=1)` as first statement after `<?php` in every file
- No closing `?>` tag in pure PHP files
- Imports: one `use` per declaration, grouped (classes, functions, constants), alphabetized

```php
<?php

declare(strict_types=1);

namespace App\Domain\User;

use App\Domain\Exception\ValidationException;
use App\Domain\ValueObject\Email;

final class UserService
{
    public function __construct(
        private readonly UserRepositoryInterface $repository,
        private readonly EventDispatcherInterface $dispatcher,
    ) {}

    public function register(string $name, string $email): User
    {
        $emailVO = Email::fromString($email);

        if ($this->repository->existsByEmail($emailVO)) {
            throw ValidationException::duplicateEmail($email);
        }

        $user = User::create(name: $name, email: $emailVO);
        $this->repository->save($user);
        $this->dispatcher->dispatch(new UserRegistered($user->id));

        return $user;
    }
}
```

### Type Declarations

- All function parameters MUST have type declarations
- All methods MUST declare return types (including `void`)
- Use union types (`string|int`) instead of `mixed` when possible
- Use intersection types (`Countable&Iterator`) for combined type constraints
- Use `Type|null` for nullable parameters (prefer explicit over `?Type`)
- Use `never` return type for functions that always throw or exit
- Avoid `mixed` -- if truly needed, document why

### Error Handling

- Never use `@` error suppression operator
- Convert PHP errors to exceptions with `set_error_handler` at bootstrap
- Create domain-specific exception hierarchies extending a base exception
- Use specific exception types (not generic `\Exception` or `\RuntimeException`)
- Always include context in exception messages
- Catch specific exceptions, never bare `catch (\Throwable $e)` without re-throwing
- Use `previous` parameter to chain exceptions

```php
<?php

declare(strict_types=1);

namespace App\Domain\Exception;

abstract class DomainException extends \RuntimeException
{
    public function __construct(
        string $message,
        public readonly string $errorCode = 'UNKNOWN',
        int $code = 0,
        ?\Throwable $previous = null,
    ) {
        parent::__construct($message, $code, $previous);
    }
}

final class NotFoundException extends DomainException
{
    public static function forResource(string $resource, string $id): self
    {
        return new self(
            message: sprintf('%s with ID "%s" not found', $resource, $id),
            errorCode: 'NOT_FOUND',
        );
    }
}
```

### Security

- All user input validated before processing (filter functions or validation libraries)
- All SQL queries use prepared statements with bound parameters (PDO or Doctrine DBAL)
- All output escaped for context: `htmlspecialchars()` for HTML, parameterized for SQL
- All file operations validate paths (`realpath()` + check against allowed directories)
- Never use `eval()`, `exec()`, `system()`, `passthru()`, or backtick operator with user input
- Use `password_hash()` with `PASSWORD_ARGON2ID` (or `PASSWORD_BCRYPT` minimum)
- Set `session.cookie_httponly`, `session.cookie_secure`, `session.cookie_samesite`
- Use CSRF tokens for all state-changing requests

## Project Structure

```
myproject/
├── src/                        # Application source (PSR-4: App\)
│   ├── Domain/                 # Business logic, entities, value objects
│   ├── Application/            # Use cases, command/query handlers
│   ├── Infrastructure/         # Framework, database, external services
│   └── Kernel.php
├── tests/
│   ├── Unit/                   # Fast, isolated unit tests
│   ├── Integration/            # Tests with real dependencies
│   └── bootstrap.php
├── config/                     # Configuration files
├── public/                     # Web root (index.php entry point)
├── composer.json
├── composer.lock
├── phpunit.xml
├── phpstan.neon
└── .php-cs-fixer.php
```

- PSR-4 autoloading: `"App\\": "src/"` in `composer.json`
- Domain layer has zero framework dependencies
- Infrastructure implements domain interfaces
- One class per file, directory structure mirrors namespace
- Keep `public/` as the web root with a single `index.php` front controller

## Key Patterns

Use PHP 8.1+ features idiomatically:

- **Enums**: Backed enums with methods for labels, state machines, role-based permissions
- **Readonly classes** (PHP 8.2+): Value objects, DTOs, Money pattern -- all properties implicitly readonly
- **Named arguments**: Improve readability for constructors and functions with many parameters
- **Match expressions**: Prefer over `switch` -- strict comparison, expression-based, no fallthrough
- **Fibers**: Cooperative multitasking foundation for async frameworks

### Enums (PHP 8.1+)

```php
<?php

declare(strict_types=1);

enum UserRole: string
{
    case Admin = 'admin';
    case Editor = 'editor';
    case Viewer = 'viewer';

    public function label(): string
    {
        return match ($this) {
            self::Admin => 'Administrator',
            self::Editor => 'Editor',
            self::Viewer => 'Viewer',
        };
    }

    /** @return list<Permission> */
    public function permissions(): array
    {
        return match ($this) {
            self::Admin => Permission::cases(),
            self::Editor => [Permission::Read, Permission::Write],
            self::Viewer => [Permission::Read],
        };
    }
}
```

### Readonly Classes (PHP 8.2+)

```php
<?php

declare(strict_types=1);

readonly class Money
{
    public function __construct(
        public int $amount,
        public string $currency,
    ) {}

    public function add(self $other): self
    {
        if ($this->currency !== $other->currency) {
            throw new \InvalidArgumentException('Cannot add different currencies');
        }

        return new self($this->amount + $other->amount, $this->currency);
    }
}
```

See [references/patterns.md](references/patterns.md) for additional patterns: dependency injection, repository pattern, value objects, command/handler, fibers, match expressions, and tooling configurations.

## Testing

### Standards

- Test files: `*Test.php` in `tests/` mirroring `src/` structure
- Test methods: `test_<unit>_<scenario>_<expected>` or `#[Test]` attribute
- PHPUnit as primary framework; Pest as alternative
- Coverage: >80% business logic, >60% overall
- Use data providers for parameterized tests
- Mock external dependencies with Mockery or PHPUnit mocks
- No database or network calls in unit tests
- Each test method tests one behavior

### PHPUnit with Data Providers

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Domain\ValueObject;

use App\Domain\Exception\ValidationException;
use App\Domain\ValueObject\Email;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class EmailTest extends TestCase
{
    #[Test]
    #[DataProvider('validEmailProvider')]
    public function it_accepts_valid_emails(string $input): void
    {
        $email = Email::fromString($input);

        self::assertSame(strtolower($input), $email->toString());
    }

    /** @return iterable<string, array{string}> */
    public static function validEmailProvider(): iterable
    {
        yield 'simple' => ['user@example.com'];
        yield 'with subdomain' => ['user@mail.example.com'];
        yield 'with plus' => ['user+tag@example.com'];
        yield 'uppercase' => ['User@Example.COM'];
    }

    #[Test]
    #[DataProvider('invalidEmailProvider')]
    public function it_rejects_invalid_emails(string $input): void
    {
        $this->expectException(ValidationException::class);

        Email::fromString($input);
    }

    /** @return iterable<string, array{string}> */
    public static function invalidEmailProvider(): iterable
    {
        yield 'empty string' => [''];
        yield 'no at sign' => ['userexample.com'];
        yield 'no domain' => ['user@'];
        yield 'no local part' => ['@example.com'];
        yield 'spaces' => ['user @example.com'];
    }
}
```

## Tooling

### Required Dev Dependencies

- `phpunit/phpunit` ^10.0 -- testing
- `phpstan/phpstan` ^1.10 -- static analysis (level 8)
- `friendsofphp/php-cs-fixer` ^3.0 -- code style
- `mockery/mockery` ^1.6 -- mocking
- `vimeo/psalm` ^5.0 -- alternative static analysis

### PHPStan: Always Level 8

```neon
# phpstan.neon
parameters:
    level: 8
    paths:
        - src
    treatPhpDocTypesAsCertain: false
    checkMissingIterableValueType: true
```

See [references/patterns.md](references/patterns.md) for full `composer.json`, `phpstan.neon`, and `.php-cs-fixer.php` configurations.

## Essential Commands

```bash
composer install              # Install dependencies
composer validate             # Validate composer.json
composer audit                # Check for security vulnerabilities
php vendor/bin/phpunit        # Run all tests
php vendor/bin/phpunit --coverage-text  # With coverage summary
php vendor/bin/phpstan analyse         # Static analysis (level 8)
php vendor/bin/psalm                   # Alternative static analysis
php vendor/bin/php-cs-fixer fix        # Auto-fix code style
php vendor/bin/php-cs-fixer fix --dry-run --diff  # Preview fixes
```

## References

For detailed code examples, see:

- [references/patterns.md](references/patterns.md) -- Enum patterns, readonly classes, dependency injection, repository pattern, type declarations, error handling, modern PHP features, mocking, tooling configurations

## External References

- [PHP: The Right Way](https://phptherightway.com/)
- [PSR-12: Extended Coding Style](https://www.php-fig.org/psr/psr-12/)
- [PSR-4: Autoloading Standard](https://www.php-fig.org/psr/psr-4/)
- [PHPStan Documentation](https://phpstan.org/user-guide/getting-started)
- [PHPUnit Documentation](https://docs.phpunit.de/)
- [Psalm Documentation](https://psalm.dev/docs/)
- [PHP-CS-Fixer Documentation](https://cs.symfony.com/)
