---
name: Laravel Tooling
description: Ecosystem management, Artisan, and asset bundling.
metadata:
  labels: [laravel, artisan, vite, horizon, pint]
  triggers:
    files: ['package.json', 'composer.json', 'vite.config.js']
    keywords: [artisan, vite, horizon, pint, blade]
---

# Laravel Tooling

## **Priority: P2 (MEDIUM)**

## Structure

```text
project/
├── app/Console/        # Custom Artisan commands
├── resources/js/       # Frontend assets (Vite)
└── pint.json           # Code styling
```

## Implementation Guidelines

- **Artisan Focus**: Build custom commands for repetitive tasks.
- **Vite Integration**: Use `@vite` directive for CSS/JS bundling.
- **Pint Styling**: Enforce Laravel style standard automatically.
- **Background Jobs**: Use **Horizon** for monitoring Redis queues.
- **Blade Components**: Encapsulate UI into `@component` or `<x-comp>`.
- **Caching**: Prune/refresh caches via `optimize:clear`.

## Anti-Patterns

- **Mix Usage**: **No Laravel Mix**: Migrate to Vite for faster HMR.
- **Raw JS**: **No JS in Blade**: Move to `resources/js`.
- **Manual CLI**: **No manual DB edits**: Use Artisan or migrations.
- **Unformatted Code**: **No unstyled merge**: Run `pint` before commit.

## References

- [Artisan & Vite Patterns](references/implementation.md)
