---
name: Laravel Architecture
description: Core architectural standards for scalable Laravel applications.
metadata:
  labels: [laravel, architecture, srp, service-layer]
  triggers:
    files: ['app/Http/Controllers/**/*.php', 'routes/*.php']
    keywords: [controller, service, action, request, container]
---

# Laravel Architecture

## **Priority: P0 (CRITICAL)**

## Structure

```text
app/
├── Http/
│   ├── Controllers/    # Slim (Request/Response only)
│   └── Requests/       # Validation logic
├── Services/           # Business logic (Optional)
└── Actions/            # Single-purpose classes (Preferred)
```

## Implementation Guidelines

- **Skinny Controllers**: Keep controllers focused on routing and response.
- **Service/Actions**: Extract complex logic into Service or Action classes.
- **Form Requests**: Use `php artisan make:request` for all validation tags.
- **DI usage**: Inject dependencies via constructors or method injection.
- **No Logic in Routes**: Always delegate route closures to controllers.
- **Contract First**: Use Interfaces for decoupling third-party integrations.

## Anti-Patterns

- **Fat Controllers**: **No logic in Controllers**: Move processing elsewhere.
- **New Keyword**: **No Manual Instantiation**: Use Service Container via DI.
- **Inline Validation**: **No $request->validate()**: Favor Form Requests.
- **Global Helpers**: **No excessive helpers**: Use class-based logic.

## References

- [Slim Controller Patterns](references/implementation.md)
