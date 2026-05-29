---
name: dto
description: Readonly data containers with a `fromArray` factory method used to pass structured data between application layers — especially for external API responses and service boundaries.
---

**Name:** DTO (Data Transfer Object)
**Description:** Readonly data containers with a `fromArray` factory method used to pass structured data between application layers — especially for external API responses and service boundaries.
**Compatible Agents:** general-purpose, backend
**Tags:** DataObjects/**/*.php, laravel, php, backend, dto, data-object, readonly

## Rules

- Use `readonly class` with constructor promotion
- Include a `static fromArray(array $data): static` factory method
- Place DTOs in the relevant service's `DataObjects/` directory
- DTOs are immutable — never add setters or mutable state
- Handle API field name variations (PascalCase, camelCase, snake_case) in `fromArray()`
- Use nullable types for optional fields
- Keep DTOs free of business logic — they are data containers only
- All properties must have explicit types — no untyped properties

## Examples

```php
readonly class CustomerData
{
    public function __construct(
        public string $id,
        public ?string $name,
        public ?string $email,
    ) {}

    public static function fromArray(array $data): static
    {
        return new static(
            id: (string) ($data['ID'] ?? $data['id'] ?? ''),
            name: $data['Name'] ?? $data['name'] ?? null,
            email: $data['Email'] ?? $data['email'] ?? null,
        );
    }
}
```

```php
// Usage
$customer = CustomerData::fromArray($apiResponse);
echo $customer->name;
```

## Anti-Patterns

- Adding setters or mutable state to a DTO
- Including business logic inside a DTO
- Using a DTO as a model replacement (DTOs don't persist to the database)
- Not handling API field name variations (assuming a single naming convention)
- Leaving properties untyped or using `mixed` without narrowing
- Placing DTOs in a global `DataObjects/` folder instead of within the relevant service directory

## References

- [PHP Readonly Classes](https://www.php.net/manual/en/language.oop5.readonly-properties.php)
- Related: `Services/SKILL.md` — DTOs are typically returned by service classes
- Related: `Saloon/SKILL.md` — Saloon integrations return typed DTOs
