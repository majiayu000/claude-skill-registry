---
name: Laravel Eloquent
description: Advanced Eloquent ORM patterns for performance and query reuse.
metadata:
  labels: [laravel, eloquent, orm, database]
  triggers:
    files: ['app/Models/**/*.php']
    keywords: [scope, with, eager, chunk, model]
---

# Laravel Eloquent

## **Priority: P0 (CRITICAL)**

## Structure

```text
app/
└── Models/
    ├── {Model}.php
    └── Scopes/         # Advanced global scopes
```

## Implementation Guidelines

- **N+1 Prevention**: Always use `with()` or `$with` for relationships.
- **Eager Loading**: Set strict loading via `Eloquent::preventLazyLoading()`.
- **Reusable Scopes**: Define `scopeName` methods for common query filters.
- **Mass Assignment**: Define `$fillable` and use `$request->validated()`.
- **Performance**: Use `chunk()`, `lazy()`, or `cursor()` for large tasks.
- **Casting**: Use `$casts` for dates, JSON, and custom types.

## Anti-Patterns

- **N+1 Queries**: **No lazy loading**: Never query relationships in loops.
- **Fat Models**: **No business logic**: Models are for data access only.
- **Magic Queries**: **No raw SQL**: Use Query Builder or Eloquent.
- **Select \***: **No excessive data**: Select only required columns.

## References

- [Eloquent Performance Guide](references/implementation.md)
