---
name: laravel-i18n
description: Laravel localization - __(), trans_choice(), lang files, JSON translations, pluralization, middleware, formatting. Use when implementing translations.
versions:
  laravel: "12.x"
  php: "8.4"
user-invocable: true
references: references/localization.md, references/pluralization.md, references/blade-translations.md, references/middleware.md, references/formatting.md, references/packages.md, references/best-practices.md, references/templates/SetLocaleMiddleware.php.md, references/templates/lang-files.md, references/templates/LocaleServiceProvider.php.md, references/templates/LocaleRoutes.php.md
related-skills: laravel-blade, laravel-api
---

# Laravel Internationalization

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing translation patterns
2. **fuse-ai-pilot:research-expert** - Verify Laravel i18n best practices via Context7
3. **mcp__context7__query-docs** - Check Laravel localization documentation

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | PHP Files | JSON Files |
|---------|-----------|------------|
| Keys | Short (`messages.welcome`) | Full text |
| Nesting | Supported | Flat only |
| Best for | Structured translations | Large apps |

---

## Critical Rules

1. **Never concatenate strings** - Use `:placeholder` replacements
2. **Always handle zero** in pluralization
3. **Group by feature** - `auth.login.title`, `auth.login.button`
4. **Extract strings early** - No hardcoded text in views
5. **Validate locales** - Use enum or whitelist

---

## Decision Guide

```
Translation task?
├── Basic string → __('key')
├── With variables → __('key', ['name' => $value])
├── Pluralization → trans_choice('key', $count)
├── In Blade → @lang('key') or {{ __('key') }}
├── Locale detection → Middleware
├── Format date/money → LocalizationService
└── Package strings → trans('package::key')
```

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Setup** | [localization.md](references/localization.md) | Initial configuration |
| **Pluralization** | [pluralization.md](references/pluralization.md) | Count-based translations |
| **Blade** | [blade-translations.md](references/blade-translations.md) | View translations |
| **Middleware** | [middleware.md](references/middleware.md) | Locale detection |
| **Formatting** | [formatting.md](references/formatting.md) | Date/number/currency |
| **Packages** | [packages.md](references/packages.md) | Vendor translations |
| **Best Practices** | [best-practices.md](references/best-practices.md) | Large app organization |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [SetLocaleMiddleware.php.md](references/templates/SetLocaleMiddleware.php.md) | URL/session locale detection |
| [lang-files.md](references/templates/lang-files.md) | Translation file examples |
| [LocaleServiceProvider.php.md](references/templates/LocaleServiceProvider.php.md) | Centralized localization service |
| [LocaleRoutes.php.md](references/templates/LocaleRoutes.php.md) | URL prefix locale routing |

---

## Quick Reference

```php
// Basic translation
__('messages.welcome')

// With replacement
__('Hello :name', ['name' => 'John'])

// Pluralization
trans_choice('messages.items', $count)

// Runtime locale
App::setLocale('fr');
App::currentLocale();  // 'fr'
```

---

## Best Practices

### DO
- Use `:placeholder` for dynamic values
- Handle zero case in pluralization
- Group keys by feature module
- Use Locale enum for type safety
- Set Carbon locale in middleware

### DON'T
- Concatenate translated strings
- Hardcode text in views
- Accept any locale without validation
- Create DB-based translations (use files)
