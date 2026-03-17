---
name: PHP Ecosystem
description: This skill should be used when the user asks to "write php", "php 8", "composer", "phpunit", "pest", "phpstan", "psalm", "psr", or works with modern PHP language patterns and configuration. Provides comprehensive modern PHP ecosystem patterns and best practices.
---

# PHP Version Features

## PHP 8.3 (2023-11)
- Typed class constants
- `json_validate()` function
- `Randomizer::getFloat()` and `nextFloat()`
- Deep cloning of readonly properties
- `#[Override]` attribute

## PHP 8.2 (2022-12)
- Readonly classes
- DNF types (Disjunctive Normal Form)
- `null`, `false`, `true` as standalone types
- Constants in traits
- Dynamic properties deprecated

## PHP 8.1 (2021-11)
- Enums (backed and unit)
- Readonly properties
- Fibers
- Intersection types
- `never` return type
- First-class callable syntax
- `new` in initializers

## PHP 8.0 (2020-11)
- Named arguments
- Attributes
- Constructor property promotion
- Union types
- Match expression
- Nullsafe operator (`?->`)
- `mixed` type

# Type System

**Union types**: `function process(string|int $value): string|null`

**Intersection types** (PHP 8.1+): `function process(Countable&Iterator $collection): int`

**DNF types** (PHP 8.2+): `function handle((Countable&Iterator)|null $items): void`

**Enums** (PHP 8.1+):
```php
enum Status: string {
    case Draft = 'draft';
    case Published = 'published';
    public function label(): string {
        return match($this) { self::Draft => 'Draft', ... };
    }
}
```

**Readonly** (PHP 8.1+ property, PHP 8.2+ class):
```php
readonly class ValueObject {
    public function __construct(public string $name, public int $value) {}
}
```

**Attributes** (PHP 8.0+):
```php
#[Attribute(Attribute::TARGET_METHOD)]
class Route {
    public function __construct(public string $path, public string $method = 'GET') {}
}
```

**Constructor property promotion** (PHP 8.0+):
```php
class Product {
    public function __construct(private string $name, private float $price) {}
}
```

**Named arguments** (PHP 8.0+):
```php
$user = createUser(email: 'user@example.com', name: 'John Doe', role: 'admin');
```

**Typed class constants** (PHP 8.3+):
```php
class Config {
    public const string VERSION = '1.0.0';
    public const int MAX_RETRIES = 3;
}
```

# PSR Standards

- **PSR-1**: Basic coding standard (StudlyCaps classes, camelCase methods, UPPER_CASE constants)
- **PSR-4**: Autoloading (`"App\\": "src/"` in composer.json)
- **PSR-3**: Logger interface (`Psr\Log\LoggerInterface`)
- **PSR-7**: HTTP message interfaces (immutable request/response)
- **PSR-11**: Container interface (`Psr\Container\ContainerInterface`)
- **PSR-12**: Extended coding style (4 spaces indent, braces on next line for classes/methods)
- **PSR-15**: HTTP server request handlers and middleware
- **PSR-17**: HTTP factories
- **PSR-18**: HTTP client interface

# Design Patterns

**Value Object**:
```php
readonly class Money {
    public function __construct(public int $amount, public string $currency) {
        if ($amount < 0) throw new InvalidArgumentException('Amount cannot be negative');
    }
    public function add(Money $other): self { /* ... */ }
}
```

**Repository**: Abstract data persistence behind an interface.

**Service Layer**: Coordinate use cases and transactions.

**Dependency Injection**: Inject dependencies through constructor.

# Composer

**Version constraints**:
- `^7.0` - Allows minor updates (7.0.0 to < 8.0.0)
- `~7.0` - Allows patch updates only (7.0.0 to < 7.1.0)

**Package structure**:
```
my-package/
├── src/
├── tests/
├── composer.json
├── phpunit.xml.dist
├── phpstan.neon
└── .php-cs-fixer.dist.php
```

**Scripts**:
```json
"scripts": {
    "test": "phpunit",
    "analyse": "phpstan analyse",
    "cs-fix": "php-cs-fixer fix",
    "ci": ["@cs-check", "@analyse", "@test"]
}
```

# Testing

## PHPUnit
```php
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

class CalculatorTest extends TestCase {
    #[Test]
    public function itAddsNumbers(): void {
        $this->assertSame(5, (new Calculator())->add(2, 3));
    }

    #[Test, DataProvider('additionProvider')]
    public function itAddsVariousNumbers(int $a, int $b, int $expected): void { /* ... */ }

    public static function additionProvider(): array {
        return ['positive' => [1, 2, 3], 'negative' => [-1, -2, -3]];
    }
}
```

## Pest
```php
test('it adds numbers', function () {
    expect($this->calculator->add(2, 3))->toBe(5);
});

it('throws on division by zero', function () {
    $this->calculator->divide(10, 0);
})->throws(DivisionByZeroError::class);
```

# Static Analysis

## PHPStan
```yaml
# phpstan.neon
parameters:
    level: 8  # 0-10, use max for highest
    paths: [src, tests]
    checkMissingIterableValueType: true
```

Levels: 0-5 basic to argument types, 6 missing type hints, 7-8 no mixed, 9-10 strict.

**Generics**:
```php
/** @template T
 * @param class-string<T> $class
 * @return T */
public function create(string $class): object { return new $class(); }
```

## PHP CS Fixer
```php
// .php-cs-fixer.dist.php
return (new PhpCsFixer\Config())
    ->setRules(['@PER-CS2.0' => true, '@PHP82Migration' => true, 'strict_types' => true])
    ->setFinder(PhpCsFixer\Finder::create()->in(__DIR__ . '/src'))
    ->setRiskyAllowed(true);
```

## Rector
```php
// rector.php
return RectorConfig::configure()
    ->withPaths([__DIR__ . '/src'])
    ->withSets([SetList::CODE_QUALITY, SetList::DEAD_CODE])
    ->withPhpSets(php83: true);
```

# Database (PDO)

**Connection**:
```php
$pdo = new PDO($dsn, $user, $pass, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);
```

**Prepared statements** (ALWAYS use for user input):
```php
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);
```

**Transactions**:
```php
try {
    $pdo->beginTransaction();
    // ... operations ...
    $pdo->commit();
} catch (\Exception $e) {
    $pdo->rollBack();
    throw $e;
}
```

# Performance

**OPcache** (production):
```ini
opcache.enable=1
opcache.validate_timestamps=0  ; Clear cache on deploy
opcache.memory_consumption=256
```

**JIT** (PHP 8.0+): `opcache.jit=1255` - Best for CPU-intensive tasks.

**Preloading** (PHP 7.4+): Load commonly used classes at startup.

# Anti-patterns
- God class - Split into focused single-responsibility classes
- Service locator - Use constructor injection
- Arrays instead of typed objects - Create value objects/DTOs
- `mixed` type abuse - Use union types, generics, proper narrowing
- Static method abuse - Use instance methods with DI
- Null returns for errors - Throw exceptions or use Result type
- SQL concatenation - Always use prepared statements

# Best Practices
- Add `declare(strict_types=1)` to all PHP files
- Use prepared statements for all database queries
- Use PHPStan level 6+ for type safety
- Use readonly classes for value objects
- Follow PSR-12 coding style
- Use enums instead of string/int constants
- Inject dependencies through constructor
- Use named arguments for complex function calls
- Create custom exceptions for domain errors
- Use attributes for metadata instead of docblock annotations
