---
name: nextjs-i18n
description: Next.js 16 internationalization with next-intl or DIY. Use when implementing i18n, translations, localization, multilingual, language switch, locale routing, or formatters.
versions:
  next-intl: 4.0
  nextjs: 16
user-invocable: true
references: references/installation.md, references/pages-router.md, references/routing-setup.md, references/routing-config.md, references/translations.md, references/formatting.md, references/navigation.md, references/server-components.md, references/client-components.md, references/middleware-proxy.md, references/error-files.md, references/configuration.md, references/plugin.md, references/extraction.md, references/messages-validation.md, references/typescript.md, references/testing.md, references/integrations.md, references/seo.md, references/core-library.md, references/runtime-requirements.md, references/diy-dictionaries.md, references/diy-locale-detection.md
related-skills: nextjs-16, solid-nextjs
---

# Next.js 16 Internationalization

Complete i18n solution with next-intl or DIY dictionary approach.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing i18n setup and message files
2. **fuse-ai-pilot:research-expert** - Verify latest next-intl docs via Context7/Exa
3. **mcp__context7__query-docs** - Check locale config and patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building multilingual Next.js 16 applications
- Need locale-based routing with `[locale]` dynamic segment
- Implementing language switcher and URL localization
- Formatting dates, numbers, currencies, and relative times per locale
- SEO optimization with hreflang tags and localized metadata
- Supporting right-to-left (RTL) languages

### Why next-intl

| Feature | Benefit |
|---------|---------|
| App Router native | Full Server Components support |
| Type-safe messages | TypeScript autocompletion for keys |
| ICU MessageFormat | Pluralization, gender, select expressions |
| Async message loading | Load translations on-demand per locale |
| proxy.ts compatible | Works with Next.js 16 proxy pattern |
| Rich formatting | Dates, numbers, lists, relative time |

---

## Two Approaches

### 1. next-intl (Recommended)

Full-featured library with routing, formatting, and type safety. Best for production applications needing comprehensive i18n support.

### 2. DIY Dictionary

Lightweight approach using dynamic imports for simple translation needs. Good for projects wanting minimal dependencies.

---

## SOLID Architecture

### Module Structure

All i18n code organized in `modules/cores/i18n/`:

- **config/** - Routing configuration, locale definitions
- **interfaces/** - TypeScript types for messages and locales
- **services/** - Request handlers, message loaders
- **messages/** - JSON translation files per locale

### File Locations

- `src/modules/cores/i18n/src/config/routing.ts` - Locale routing config
- `src/modules/cores/i18n/messages/en.json` - English translations
- `src/modules/cores/i18n/messages/fr.json` - French translations
- `proxy.ts` - Locale detection and redirect logic

---

## Routing Patterns

### Locale Segment

All routes prefixed with `[locale]` dynamic segment:

- `/en/about` → English about page
- `/fr/about` → French about page
- `/` → Redirects to default locale

### Navigation Components

Use localized navigation from next-intl for automatic locale handling:

- **Link** - Locale-aware anchor links
- **redirect** - Server-side locale redirect
- **usePathname** - Current path without locale
- **useRouter** - Programmatic navigation

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md), [routing-setup.md](references/routing-setup.md) |
| Route config | [routing-config.md](references/routing-config.md), [middleware-proxy.md](references/middleware-proxy.md) |
| Translations | [translations.md](references/translations.md), [messages-validation.md](references/messages-validation.md) |
| Formatting | [formatting.md](references/formatting.md) |
| Components | [server-components.md](references/server-components.md), [client-components.md](references/client-components.md) |
| Navigation | [navigation.md](references/navigation.md) |
| TypeScript | [typescript.md](references/typescript.md) |
| SEO | [seo.md](references/seo.md) |
| Testing | [testing.md](references/testing.md) |
| DIY approach | [diy-dictionaries.md](references/diy-dictionaries.md), [diy-locale-detection.md](references/diy-locale-detection.md) |

---

## Message Formatting

### ICU MessageFormat

- **Pluralization** - `{count, plural, one {# item} other {# items}}`
- **Select** - `{gender, select, male {He} female {She} other {They}}`
- **Rich text** - Support for bold, italic, links in messages

### Formatters

- **formatDate** - Locale-aware date formatting
- **formatNumber** - Currency, percentages, decimals
- **formatList** - Conjunction/disjunction lists
- **formatRelativeTime** - "2 hours ago", "in 3 days"

---

## Best Practices

1. **Type-safe keys** - Use TypeScript for message key autocompletion
2. **Namespace messages** - Organize by feature/page for maintainability
3. **Server-first** - Load translations on server, avoid client bundles
4. **SEO hreflang** - Add alternate links for all locales
5. **RTL support** - Use `dir` attribute for right-to-left languages
6. **Fallback locale** - Configure default for missing translations

---

## Error Handling

### Special Files

Localized error and loading states require specific handling:

- `[locale]/error.tsx` - Localized error boundary
- `[locale]/not-found.tsx` - Localized 404 page
- `global-error.tsx` - Root error fallback

See [error-files.md](references/error-files.md) for complete patterns.
