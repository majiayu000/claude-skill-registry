---
name: PHP Modern Features
description: Use when modern PHP features including typed properties, union types, match expressions, named arguments, attributes, enums, and patterns for writing type-safe, expressive PHP code with latest language improvements.
allowed-tools: []
---

# PHP Modern Features

## Introduction

Modern PHP (7.4+, 8.0+, 8.1+, 8.2+) has evolved dramatically with features that
improve type safety, expressiveness, and developer experience. These additions
transform PHP from a loosely-typed scripting language into a powerful,
type-safe platform for building robust applications.

Key improvements include strict typing, property and parameter types, union and
intersection types, match expressions, named arguments, attributes (annotations),
enumerations, and readonly properties. These features enable clearer intent,
better IDE support, and fewer runtime errors.

This skill covers typed properties, union/intersection types, match expressions,
enums, attributes, named arguments, and patterns for leveraging modern PHP
effectively.

## Typed Properties and Parameters

Type declarations improve code reliability by enforcing types at runtime and
enabling better static analysis.

```php
<?php
// PHP 7.4+ typed properties
class User {
    public string $name;
    public int $age;
    public ?string $email = null; // Nullable
    private array $roles = [];
    protected bool $active = true;
}

$user = new User();
$user->name = "Alice"; // OK
$user->age = 30; // OK
// $user->age = "thirty"; // TypeError

// Constructor property promotion (PHP 8.0+)
class Product {
    public function __construct(
        public string $name,
        public float $price,
        public int $stock,
        private ?string $sku = null
    ) {}
}

$product = new Product("Laptop", 999.99, 10);
echo $product->name; // "Laptop"
// echo $product->sku; // Error: private property

// Return type declarations
function calculateTotal(float $price, int $quantity): float {
    return $price * $quantity;
}

function findUser(int $id): ?User {
    // Return User or null
    return $id > 0 ? new User() : null;
}

function getUsers(): array {
    return [new User(), new User()];
}

// Void return type
function logMessage(string $message): void {
    echo $message . "\n";
}

// Never return type (PHP 8.1+)
function fail(string $message): never {
    throw new Exception($message);
}

// Mixed type (PHP 8.0+)
function process(mixed $value): mixed {
    return $value;
}

// Static return type
class Builder {
    public function setName(string $name): static {
        return $this;
    }

    public function build(): static {
        return new static();
    }
}

// Parameter types
function greet(
    string $name,
    int $age,
    bool $formal = false
): string {
    $greeting = $formal ? "Good day" : "Hello";
    return "$greeting, $name ($age)";
}

// Variadic typed parameters
function sum(int ...$numbers): int {
    return array_sum($numbers);
}

$total = sum(1, 2, 3, 4, 5); // 15
```

Typed properties and parameters catch type errors early and provide clear
contracts for function interfaces.

## Union and Intersection Types

Union types allow multiple type possibilities, while intersection types require
all specified types simultaneously.

```php
<?php
// Union types (PHP 8.0+)
function processId(int|string $id): void {
    if (is_int($id)) {
        echo "Processing integer ID: $id\n";
    } else {
        echo "Processing string ID: $id\n";
    }
}

processId(123);
processId("ABC-456");

// Union type properties
class Response {
    public function __construct(
        public int|string $code,
        public array|string $data
    ) {}
}

// Nullable as union type
function findProduct(int $id): Product|null {
    return $id > 0 ? new Product("Item", 10.0, 5) : null;
}

// Multiple union types
function format(int|float|string $value): string {
    return match (true) {
        is_int($value) => "Integer: $value",
        is_float($value) => "Float: $value",
        is_string($value) => "String: $value",
    };
}

// False pseudo-type in unions
function parseValue(string $input): int|false {
    $result = filter_var($input, FILTER_VALIDATE_INT);
    return $result !== false ? $result : false;
}

// Union types with built-in types
function getData(): array|object|null {
    return ['key' => 'value'];
}

// Intersection types (PHP 8.1+)
interface Loggable {
    public function log(): void;
}

interface Cacheable {
    public function cache(): void;
}

// Function accepting intersection type
function process(Loggable&Cacheable $object): void {
    $object->log();
    $object->cache();
}

class Service implements Loggable, Cacheable {
    public function log(): void {
        echo "Logging\n";
    }

    public function cache(): void {
        echo "Caching\n";
    }
}

// Intersection with union
function handle((Loggable&Cacheable)|null $object): void {
    $object?->log();
}

// DNF types (PHP 8.2+ - Disjunctive Normal Form)
function advanced((Loggable&Cacheable)|(Loggable&Serializable) $object): void {
    $object->log();
}
```

Union types enable flexible parameter acceptance while intersection types
enforce multiple capabilities simultaneously.

## Match Expressions

Match expressions provide pattern matching with strict comparisons and
exhaustive checking, improving upon switch statements.

```php
<?php
// Basic match expression (PHP 8.0+)
$status = 200;

$message = match ($status) {
    200 => "OK",
    404 => "Not Found",
    500 => "Server Error",
    default => "Unknown",
};

echo $message; // "OK"

// Multiple conditions
$result = match ($status) {
    200, 201, 202 => "Success",
    400, 401, 403 => "Client Error",
    500, 502, 503 => "Server Error",
    default => "Unknown",
};

// Match with expressions
$age = 25;

$category = match (true) {
    $age < 13 => "Child",
    $age < 18 => "Teen",
    $age < 65 => "Adult",
    default => "Senior",
};

// Match without default (throws on no match)
function getColor(string $type): string {
    return match ($type) {
        'primary' => '#007bff',
        'success' => '#28a745',
        'danger' => '#dc3545',
        // Missing default throws UnhandledMatchError
    };
}

// Match with complex expressions
enum Status {
    case Draft;
    case Published;
    case Archived;
}

function canEdit(Status $status): bool {
    return match ($status) {
        Status::Draft => true,
        Status::Published => false,
        Status::Archived => false,
    };
}

// Match returning different types
function process(mixed $value): int|string {
    return match (gettype($value)) {
        'integer' => $value * 2,
        'string' => strtoupper($value),
        'array' => count($value),
        default => 0,
    };
}

// Match vs switch strict comparison
$value = "1";

// Switch uses == (loose)
switch ($value) {
    case 1:
        echo "Matches with switch\n"; // Prints
        break;
}

// Match uses === (strict)
$result = match ($value) {
    1 => "Matches with match",
    "1" => "Strict match", // This matches
    default => "No match",
};

echo $result; // "Strict match"
```

Match expressions are safer than switch due to strict comparison and exhaustive
checking requirements.

## Enumerations

Enums provide type-safe sets of possible values, replacing magic strings and
constants with explicit types.

```php
<?php
// Basic enum (PHP 8.1+)
enum Status {
    case Pending;
    case Approved;
    case Rejected;
}

function updateOrder(Status $status): void {
    echo "Order status: " . $status->name . "\n";
}

updateOrder(Status::Approved);

// Backed enum with values
enum Priority: int {
    case Low = 1;
    case Medium = 2;
    case High = 3;
    case Critical = 4;
}

$priority = Priority::High;
echo $priority->value; // 3
echo $priority->name; // "High"

// String-backed enum
enum Role: string {
    case Admin = 'admin';
    case User = 'user';
    case Guest = 'guest';
}

// Enum methods
enum HttpStatus: int {
    case OK = 200;
    case Created = 201;
    case BadRequest = 400;
    case Unauthorized = 401;
    case NotFound = 404;
    case ServerError = 500;

    public function isSuccess(): bool {
        return $this->value >= 200 && $this->value < 300;
    }

    public function isError(): bool {
        return $this->value >= 400;
    }

    public function message(): string {
        return match ($this) {
            self::OK => "Request successful",
            self::Created => "Resource created",
            self::BadRequest => "Invalid request",
            self::Unauthorized => "Authentication required",
            self::NotFound => "Resource not found",
            self::ServerError => "Internal server error",
        };
    }
}

$status = HttpStatus::NotFound;
echo $status->isError() ? "Error: " : "Success: ";
echo $status->message();

// Enum with static methods
enum Color: string {
    case Red = '#FF0000';
    case Green = '#00FF00';
    case Blue = '#0000FF';

    public static function fromRgb(int $r, int $g, int $b): string {
        return sprintf('#%02X%02X%02X', $r, $g, $b);
    }

    public static function random(): self {
        $cases = self::cases();
        return $cases[array_rand($cases)];
    }
}

// Enum iteration
foreach (Priority::cases() as $priority) {
    echo $priority->name . ": " . $priority->value . "\n";
}

// Enum from value
$priority = Priority::from(2); // Priority::Medium
$priority = Priority::tryFrom(10); // null (safe version)

// Enum in match
function getPriorityColor(Priority $priority): string {
    return match ($priority) {
        Priority::Low => 'green',
        Priority::Medium => 'yellow',
        Priority::High => 'orange',
        Priority::Critical => 'red',
    };
}
```

Enums replace magic strings and constants with type-safe alternatives that
support IDE autocompletion and refactoring.

## Attributes (Annotations)

Attributes attach metadata to declarations, enabling declarative configuration
and reflection-based frameworks.

```php
<?php
// Built-in attributes
#[Attribute]
class Route {
    public function __construct(
        public string $path,
        public array $methods = ['GET']
    ) {}
}

#[Attribute]
class Validate {
    public function __construct(
        public array $rules
    ) {}
}

// Using attributes
class UserController {
    #[Route('/users', methods: ['GET'])]
    public function index(): array {
        return ['users' => []];
    }

    #[Route('/users/{id}', methods: ['GET'])]
    #[Validate(rules: ['id' => 'required|integer'])]
    public function show(int $id): array {
        return ['user' => ['id' => $id]];
    }

    #[Route('/users', methods: ['POST'])]
    #[Validate(rules: ['name' => 'required', 'email' => 'required|email'])]
    public function store(array $data): array {
        return ['user' => $data];
    }
}

// Reading attributes via reflection
function getRoutes(string $class): array {
    $reflection = new ReflectionClass($class);
    $routes = [];

    foreach ($reflection->getMethods() as $method) {
        $attributes = $method->getAttributes(Route::class);

        foreach ($attributes as $attribute) {
            $route = $attribute->newInstance();
            $routes[] = [
                'path' => $route->path,
                'methods' => $route->methods,
                'handler' => [$class, $method->getName()],
            ];
        }
    }

    return $routes;
}

$routes = getRoutes(UserController::class);

// Multiple attributes
#[Attribute(Attribute::TARGET_METHOD)]
class Cache {
    public function __construct(
        public int $ttl = 3600
    ) {}
}

#[Attribute(Attribute::TARGET_METHOD)]
class RateLimit {
    public function __construct(
        public int $maxRequests,
        public int $perSeconds
    ) {}
}

class ApiController {
    #[Route('/api/data')]
    #[Cache(ttl: 300)]
    #[RateLimit(maxRequests: 100, perSeconds: 60)]
    public function getData(): array {
        return ['data' => []];
    }
}

// Class attributes
#[Attribute(Attribute::TARGET_CLASS)]
class Entity {
    public function __construct(
        public string $table
    ) {}
}

#[Entity(table: 'users')]
class UserEntity {
    public int $id;
    public string $name;
}

// Property attributes
#[Attribute(Attribute::TARGET_PROPERTY)]
class Column {
    public function __construct(
        public string $name,
        public string $type = 'string'
    ) {}
}

class Post {
    #[Column(name: 'id', type: 'integer')]
    public int $id;

    #[Column(name: 'title')]
    public string $title;

    #[Column(name: 'created_at', type: 'datetime')]
    public DateTime $createdAt;
}
```

Attributes enable declarative metadata for dependency injection, routing,
validation, ORM mapping, and other framework features.

## Named Arguments and Other Modern Features

Named arguments improve readability and make optional parameters more usable.

```php
<?php
// Named arguments (PHP 8.0+)
function createUser(
    string $name,
    int $age,
    string $email = '',
    bool $active = true
): User {
    $user = new User();
    $user->name = $name;
    $user->age = $age;
    $user->email = $email;
    $user->active = $active;
    return $user;
}

// Traditional call
$user1 = createUser("Alice", 30, "alice@example.com", true);

// Named arguments (any order, skip defaults)
$user2 = createUser(name: "Bob", age: 25);
$user3 = createUser(age: 28, name: "Charlie", active: false);

// Mixed positional and named
$user4 = createUser("Dave", 35, active: false);

// Readonly properties (PHP 8.1+)
class Config {
    public function __construct(
        public readonly string $apiKey,
        public readonly string $endpoint
    ) {}
}

$config = new Config("key123", "https://api.example.com");
// $config->apiKey = "new"; // Error: readonly property

// Readonly class (PHP 8.2+)
readonly class Point {
    public function __construct(
        public int $x,
        public int $y
    ) {}
}

// First-class callable syntax (PHP 8.1+)
$array = [1, 2, 3, 4, 5];

// Old way
$doubled = array_map(fn($n) => $n * 2, $array);

// First-class callable
function double(int $n): int {
    return $n * 2;
}

$doubled = array_map(double(...), $array);

// New in initializers (PHP 8.1+)
class Service {
    public function __construct(
        private Logger $logger = new Logger()
    ) {}
}

// Nullsafe operator (PHP 8.0+)
$country = $user?->getAddress()?->getCountry()?->getName();

// Throw expression (PHP 8.0+)
$value = $input ?? throw new InvalidArgumentException('Input required');

// str_contains, str_starts_with, str_ends_with (PHP 8.0+)
$text = "Hello, world!";
if (str_contains($text, "world")) {
    echo "Contains world\n";
}

if (str_starts_with($text, "Hello")) {
    echo "Starts with Hello\n";
}

if (str_ends_with($text, "world!")) {
    echo "Ends with world!\n";
}
```

Named arguments make function calls self-documenting and enable skipping
optional parameters in the middle of parameter lists.

## Best Practices

1. **Use strict types declaration** at file start to enable strict type checking
   and catch type errors early

2. **Leverage typed properties** for all class properties to document expected
   types and enable validation

3. **Prefer match over switch** for value-based dispatch to benefit from strict
   comparison and exhaustiveness

4. **Replace magic constants with enums** to create type-safe, self-documenting
   sets of allowed values

5. **Use named arguments for optional parameters** to improve readability and
   skip unnecessary defaults

6. **Apply readonly for immutable data** to prevent accidental mutations and
   express immutability intent

7. **Use union types for flexible parameters** when functions accept multiple
   types instead of accepting mixed

8. **Leverage attributes for metadata** instead of docblocks for
   reflection-based frameworks and tools

9. **Use constructor property promotion** to reduce boilerplate in classes with
   many simple properties

10. **Apply nullsafe operator** for safe property access on potentially null
    objects without explicit null checks

## Common Pitfalls

1. **Forgetting declare(strict_types=1)** allows type coercion that defeats
   purpose of type declarations

2. **Overusing union types** with too many alternatives reduces type safety
   benefits and complicates logic

3. **Not handling all enum cases in match** without default causes runtime
   errors when new cases added

4. **Using enums for non-exhaustive sets** like user IDs where values aren't
   known at compile time

5. **Mixing positional and named arguments incorrectly** can cause errors;
   positional must come before named

6. **Not marking readonly when appropriate** allows mutations that break
   immutability assumptions

7. **Using attributes without understanding reflection** leads to unused
   metadata that has no effect

8. **Overusing mixed type** instead of specific unions or generics reduces
   type safety benefits

9. **Not checking enum::tryFrom() return value** causes crashes when invalid
   values provided

10. **Using void when never is appropriate** for functions that always throw
    affects control flow analysis

## When to Use This Skill

Use modern PHP features when building applications on PHP 7.4+ or preferably
PHP 8.0+ to leverage improved type safety and developer experience.

Apply typed properties and parameters when designing classes and functions to
catch type errors early and improve IDE support.

Employ enums when modeling fixed sets of values like statuses, priorities, or
roles instead of using string or integer constants.

Leverage match expressions for cleaner conditional logic based on values,
especially with enums or typed values.

Use attributes for framework-level metadata like routing, validation, ORM
mapping, or dependency injection configuration.

## Resources

- [PHP 8.0 Release Notes](<https://www.php.net/releases/8.0/en.php>)
- [PHP 8.1 Release Notes](<https://www.php.net/releases/8.1/en.php>)
- [PHP 8.2 Release Notes](<https://www.php.net/releases/8.2/en.php>)
- [PHP: The Right Way](<https://phptherightway.com/>)
- [PHP Type System Documentation](<https://www.php.net/manual/en/language.types.declarations.php>)
