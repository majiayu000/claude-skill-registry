---
name: PHP Error Handling
description: Modern PHP error and exception handling standards.
metadata:
  labels: [php, exceptions, error-handling, psr-3]
  triggers:
    files: ['**/*.php']
    keywords: [try, catch, finally, Throwable, set_exception_handler]
---

# PHP Error Handling

## **Priority: P0 (CRITICAL)**

## Structure

```text
src/
└── Exceptions/
    ├── {Domain}Exception.php
    └── Handler.php
```

## Implementation Guidelines

- **Exception-Driven**: Prefer throwing exceptions over returning `false`.
- **Throwable Interface**: Catch `Throwable` for both Errors and Exceptions.
- **Custom Exceptions**: Extend `RuntimeException` for domain-specific errors.
- **Multi-catch**: Use `catch (TypeA | TypeB $e)` for identical handling.
- **Finally Cleanup**: Use `finally` to ensure resource release.
- **Global Handling**: Set `set_exception_handler` in entry points.
- **PSR-3 Logging**: Log critical faults using standard loggers.

## Anti-Patterns

- **Error Suppression**: **No @**: Avoid suppressing errors with `@`.
- **Silent Catch**: **No Empty Catches**: Log or handle all caught exceptions.
- **Logic Flow**: **No Flow Control**: Don't use exceptions for expected logic.
- **Panic Display**: **No display_errors**: Log to file, never to production screen.

## References

- [Exception & Logging Patterns](references/implementation.md)
