---
name: developing-with-php
description: Modern PHP 8.x development with type system, attributes, enums, error handling, and Composer. Use when writing PHP code or working with PHP projects.
---

# PHP Skill - Quick Reference

Core PHP language patterns for modern development. For Laravel-specific patterns, see the Laravel skill.

> **Progressive Disclosure**: This is the quick reference. See [REFERENCE.md](./REFERENCE.md) for comprehensive patterns, advanced examples, and deep-dives.

## Table of Contents

1. [PHP 8.x Type System](#php-8x-type-system)
2. [Constructor Property Promotion](#constructor-property-promotion)
3. [Enums](#enums)
4. [Match Expression & Named Arguments](#match-expression--named-arguments)
5. [Attributes](#attributes)
6. [Null Safety](#null-safety)
7. [OOP Essentials](#oop-essentials)
8. [Handler/Service Pattern](#handlerservice-pattern)
9. [Map/DTO Pattern](#mapdto-pattern)
10. [PDO Database Access](#pdo-database-access)
11. [Composer & Autoloading](#composer--autoloading)
12. [Error Handling](#error-handling)
13. [Testing with PHPUnit](#testing-with-phpunit)
14. [Array Operations Quick Reference](#array-operations-quick-reference)
15. [Security Essentials](#security-essentials)
16. [Quick Reference Tables](#quick-reference-tables)
17. [Related Resources](#related-resources)

---

## PHP 8.x Type System

```php
<?php
// Union types (8.0+)
function process(string|int $value): string|false { }

// Intersection types (8.1+)
function handle(Countable&Iterator $collection): void { }

// Nullable types
function find(int $id): ?User { }

// Never return type (8.1+)
function fail(): never {
    throw new Exception('Fatal error');
}

// True, false, null as standalone types (8.2+)
function isValid(): true { return true; }
```

## Constructor Property Promotion

```php
<?php
// Promoted properties (8.0+) - replaces boilerplate
class User {
    public function __construct(
        private string $name,
        private string $email,
        private bool $active = true,
    ) {}
}

// Readonly class (8.2+) - all properties are readonly
readonly class ValueObject {
    public function __construct(
        public string $value,
        public DateTimeImmutable $createdAt,
    ) {}
}
```

## Enums

```php
<?php
// Backed enum with values (8.1+)
enum Status: string {
    case Draft = 'draft';
    case Published = 'published';
    case Archived = 'archived';

    public function label(): string {
        return match($this) {
            self::Draft => 'Draft',
            self::Published => 'Published',
            self::Archived => 'Archived',
        };
    }
}

// Usage
$status = Status::Published;
$value = $status->value;                 // 'published'
$all = Status::cases();                  // Array of all cases
$fromValue = Status::from('draft');      // Status::Draft
$tryFrom = Status::tryFrom('invalid');   // null (no exception)
```

> See [REFERENCE.md](./REFERENCE.md#enum-patterns) for EnumTrait pattern and advanced enum usage.

## Match Expression & Named Arguments

```php
<?php
// Match returns value, uses strict comparison
$result = match($status) {
    Status::Draft => 'Not ready',
    Status::Published => 'Live',
    Status::Archived => 'Hidden',
};

// Multiple conditions
$category = match($code) {
    200, 201, 204 => 'success',
    400, 422 => 'client_error',
    500, 502, 503 => 'server_error',
    default => 'unknown',
};

// Named arguments (skip defaults, any order)
$user = createUser(
    email: 'john@example.com',
    name: 'John Doe',
    role: 'admin',
);
```

## Attributes

```php
<?php
#[Attribute]
class Route {
    public function __construct(
        public string $path,
        public string $method = 'GET',
    ) {}
}

class UserController {
    #[Route('/users', 'GET')]
    public function index(): array { }
}

// Reading attributes via reflection
$reflection = new ReflectionMethod(UserController::class, 'index');
$attributes = $reflection->getAttributes(Route::class);
$route = $attributes[0]->newInstance();
echo $route->path;  // '/users'
```

## Null Safety

```php
<?php
// Null coalescing
$name = $user->name ?? 'Anonymous';

// Null coalescing assignment
$data['count'] ??= 0;

// Nullsafe operator (8.0+)
$country = $user?->address?->country?->name;

// Combined
$timezone = $user?->settings?->timezone ?? 'UTC';
```

---

## OOP Essentials

### Interfaces & Abstract Classes

```php
<?php
interface RepositoryInterface {
    public function find(int $id): ?object;
    public function save(object $entity): void;
}

abstract class BaseHandler {
    public function __construct(protected PDO $db) {}
    abstract public function handle(array $data): mixed;
}
```

### Traits

```php
<?php
trait Timestamps {
    protected ?DateTimeImmutable $createdAt = null;

    public function setCreatedAt(): void {
        $this->createdAt = new DateTimeImmutable();
    }
}

class User {
    use Timestamps;
}
```

> See [REFERENCE.md](./REFERENCE.md#oop-patterns) for trait conflict resolution, late static binding, and magic methods.

---

## Handler/Service Pattern

```php
<?php
class UserHandler {
    public function __construct(
        private readonly PDO $db,
        private readonly CacheInterface $cache,
    ) {}

    public function get(int $id): ?array {
        $cacheKey = "user:{$id}";
        if ($cached = $this->cache->get($cacheKey)) {
            return $cached;
        }

        $stmt = $this->db->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$id]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user) {
            $this->cache->set($cacheKey, $user, 3600);
        }
        return $user ?: null;
    }
}
```

> See [REFERENCE.md](./REFERENCE.md#handler-patterns) for CRUD handlers, aggregation patterns, and collection mapping.

---

## Map/DTO Pattern

```php
<?php
readonly class UserMap {
    public function __construct(
        public int $id,
        public string $name,
        public string $email,
    ) {}

    public static function fromRow(array $row): self {
        return new self(
            id: (int) $row['id'],
            name: trim($row['first_name'] . ' ' . $row['last_name']),
            email: $row['email'],
        );
    }

    public function toArray(): array {
        return ['id' => $this->id, 'name' => $this->name, 'email' => $this->email];
    }
}
```

> See [REFERENCE.md](./REFERENCE.md#dto-patterns) for nested mapping and collection patterns.

---

## PDO Database Access

### Connection

```php
<?php
$dsn = 'mysql:host=localhost;dbname=myapp;charset=utf8mb4';
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];
$pdo = new PDO($dsn, 'username', 'password', $options);
```

### Prepared Statements

```php
<?php
// Named parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);
$user = $stmt->fetch();

// Positional parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
$stmt->execute([$id]);
```

### Transactions

```php
<?php
try {
    $pdo->beginTransaction();
    // Multiple operations...
    $pdo->commit();
} catch (Exception $e) {
    $pdo->rollBack();
    throw $e;
}
```

> See [REFERENCE.md](./REFERENCE.md#pdo-advanced) for stored procedures, batch operations, and SQL file execution.

---

## Composer & Autoloading

### composer.json Essentials

```json
{
    "require": {
        "php": "^8.2"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    }
}
```

### Version Constraints

| Constraint | Meaning |
|------------|---------|
| `^1.0` | `>=1.0.0 <2.0.0` |
| `~1.2` | `>=1.2.0 <1.3.0` |
| `1.0.*` | `>=1.0.0 <1.1.0` |

---

## Error Handling

### Exception Pattern

```php
<?php
class AppException extends Exception {
    public function __construct(
        string $message,
        int $code = 0,
        public readonly array $context = [],
    ) {
        parent::__construct($message, $code);
    }
}

class NotFoundException extends AppException {
    public function __construct(string $resource, int|string $id) {
        parent::__construct("{$resource} not found", 404, ['id' => $id]);
    }
}
```

### Exception Handling

```php
<?php
try {
    $user = $handler->findOrFail($id);
} catch (NotFoundException $e) {
    return ['error' => $e->getMessage(), 'code' => 404];
} catch (AppException $e) {
    $this->logger->error($e->getMessage(), $e->context);
    return ['error' => 'An error occurred', 'code' => 500];
}
```

> See [REFERENCE.md](./REFERENCE.md#error-handling) for global exception handlers and validation exceptions.

---

## Testing with PHPUnit

```php
<?php
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

class UserHandlerTest extends TestCase
{
    private UserHandler $handler;

    protected function setUp(): void
    {
        $pdo = new PDO('sqlite::memory:');
        $this->handler = new UserHandler($pdo);
    }

    #[Test]
    public function it_creates_a_user(): void
    {
        $id = $this->handler->create(['name' => 'John', 'email' => 'john@example.com']);
        $this->assertIsInt($id);
        $this->assertGreaterThan(0, $id);
    }
}
```

> See [REFERENCE.md](./REFERENCE.md#phpunit) for data providers, mocking, and integration testing.

---

## Array Operations Quick Reference

```php
<?php
// Mapping
$names = array_map(fn($u) => $u['name'], $users);

// Filtering
$active = array_filter($users, fn($u) => $u['active']);

// Reducing
$total = array_reduce($items, fn($sum, $i) => $sum + $i['price'], 0);

// Column extraction
$emails = array_column($users, 'email');
$byId = array_column($users, null, 'id');  // Index by 'id'

// Sorting
usort($users, fn($a, $b) => $a['name'] <=> $b['name']);
```

> See [REFERENCE.md](./REFERENCE.md#arrays-collections) for generators and advanced collection patterns.

---

## Security Essentials

### Password Hashing

```php
<?php
$hash = password_hash($password, PASSWORD_DEFAULT);
if (password_verify($password, $hash)) { /* valid */ }
```

### SQL Injection Prevention

```php
<?php
// NEVER: $sql = "SELECT * FROM users WHERE id = {$_GET['id']}";
// ALWAYS: Use prepared statements
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
$stmt->execute([$_GET['id']]);
```

### Input Validation

```php
<?php
$email = filter_var($_POST['email'], FILTER_VALIDATE_EMAIL);
$cleanHtml = htmlspecialchars($input, ENT_QUOTES | ENT_HTML5, 'UTF-8');
```

> See [REFERENCE.md](./REFERENCE.md#security) for CSRF protection and comprehensive security patterns.

---

## Quick Reference Tables

### Type Declarations

| Type | PHP Version | Example |
|------|-------------|---------|
| `?Type` (nullable) | 7.1+ | `?int` |
| `void` | 7.1+ | `function f(): void` |
| `mixed` | 8.0+ | `function f(mixed $x)` |
| `Type1\|Type2` (union) | 8.0+ | `int\|string` |
| `never` | 8.1+ | `function f(): never` |
| `Type1&Type2` (intersection) | 8.1+ | `A&B` |
| `true`, `false`, `null` | 8.2+ | `function f(): true` |

### PDO Fetch Modes

| Mode | Returns |
|------|---------|
| `PDO::FETCH_ASSOC` | Associative array |
| `PDO::FETCH_OBJ` | stdClass object |
| `PDO::FETCH_CLASS` | Instance of specified class |

---

## Related Resources

- [REFERENCE.md](./REFERENCE.md) - Comprehensive patterns and advanced examples
- [examples/](./examples/) - Real-world code examples
- [templates/](./templates/) - Boilerplate templates
- [Laravel Skill](../laravel/SKILL.md) - Laravel-specific patterns
