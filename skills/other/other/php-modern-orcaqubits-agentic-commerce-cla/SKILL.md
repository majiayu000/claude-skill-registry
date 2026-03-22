---
name: php-modern
description: Write modern PHP 8.x code — typed properties, enums, readonly classes, match expressions, named arguments, union/intersection types, fibers, attributes, and constructor promotion. Use when writing PHP for WooCommerce or any PHP 8.x project.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Modern PHP 8.x Development

## Before writing code

**Fetch live docs**: Web-search `site:php.net manual migration` for the latest PHP migration guide and new features. Check `https://www.php.net/releases/` for current supported versions.

## PHP 8.0 Features

### Constructor Property Promotion

Declare and assign properties directly in the constructor signature — eliminates boilerplate. Useful in WooCommerce extension classes.

### Named Arguments

Call functions with parameter names: `array_slice(array: $arr, offset: 2)`. Improves readability for functions with many parameters.

### Match Expressions

Type-safe `switch` replacement that returns a value. No fall-through, strict comparison. Better than switch for value mapping.

### Union Types

`int|string` in parameter and return types. Allows multiple type declarations.

### Nullsafe Operator

`$obj?->method()?->property` — short-circuits to null if any part is null. Replaces nested null checks.

### Attributes

Native metadata annotations: `#[Route('/path')]`, `#[Override]`. Replace docblock annotations with first-class language support.

## PHP 8.1 Features

### Enums

First-class enumerations — backed (string/int) and unit enums. Perfect for status codes, types, categories. Use backed enums for database/API values.

### Readonly Properties

`public readonly string $name` — can only be set once (usually in constructor). Enforces immutability.

### Fibers

Lightweight concurrency primitives — PHP-level coroutines. Foundation for async frameworks.

### Intersection Types

`TypeA&TypeB` — value must satisfy ALL types. Useful for ensuring a parameter implements multiple interfaces.

### First-class Callable Syntax

`strlen(...)` creates a Closure from a function. Cleaner than `Closure::fromCallable('strlen')`.

## PHP 8.2 Features

### Readonly Classes

`readonly class Dto { ... }` — all properties are implicitly readonly. Perfect for Data Transfer Objects and value objects.

### Deprecated: Dynamic Properties

Creating properties not declared in the class is deprecated. Always declare properties.

### Standalone Types

`true`, `false`, `null` as standalone types in declarations.

### Constants in Traits

Traits can now define constants.

## PHP 8.3 Features

### Typed Class Constants

`const string NAME = 'value';` — type-safe constants. Strengthens contract enforcement.

### `#[\Override]` Attribute

Documents that a method intentionally overrides a parent method. Compiler error if the parent method doesn't exist.

### `json_validate()` Function

Validate JSON without decoding — faster than `json_decode` + error check.

### Dynamic Class Constant Fetch

`$class::{$constant}` — dynamic constant access.

## PHP 8.4 Features

### Property Hooks

Define get/set behavior directly on properties:
```php
public string $name {
    set => strtolower($value);
    get => ucfirst($this->name);
}
```

### Asymmetric Visibility

`public private(set) string $name` — readable publicly, writable only privately.

## PHP for WooCommerce Specifically

### Type Safety

- Use strict types: `declare(strict_types=1);` in all files
- Type all parameters, return types, and properties
- Use union types for nullable: `?string` or `string|null`

### Value Objects

Use readonly classes for DTOs and value objects — common in service layers.

### Enums for Status Codes

Replace string/int constants with backed enums for order statuses, product types, etc.

### WordPress Coding Standards Note

WPCS uses **tabs** for indentation and **Yoda conditions** (`'value' === $var`). This differs from PSR-12 (spaces, non-Yoda). When writing WooCommerce extensions, follow WPCS; for standalone PHP libraries, follow PSR-12.

## Best Practices

- Always use `declare(strict_types=1);`
- Type everything: parameters, returns, properties, constants
- Use readonly for immutable data
- Use enums instead of string/int constants
- Use match instead of switch for value mapping
- Use named arguments for clarity with many-parameter functions
- Use `#[\Override]` when overriding parent methods
- Follow WordPress Coding Standards (WPCS) for WooCommerce extensions

Fetch php.net docs for exact syntax and behavior of new features before using them.
