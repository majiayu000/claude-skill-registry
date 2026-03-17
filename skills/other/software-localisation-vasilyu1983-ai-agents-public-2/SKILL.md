---
name: software-localisation
description: Production-grade i18n/l10n patterns for React, Vue, Angular, Next.js, and Node.js. Covers library selection (i18next/react-i18next, FormatJS/react-intl, next-intl, vue-i18n, @angular/localize, Lingui, typesafe-i18n), ICU message format, RTL support, locale routing/detection, TMS integration, string extraction, and CI/CD translation workflows. Use when setting up or debugging localisation in a codebase.
---

# Software Localisation - Quick Reference

Production patterns for internationalisation (i18n) and localisation (l10n) in modern web applications. Covers library selection, translation management, ICU message format, RTL support, and CI/CD workflows.

**Snapshot (2026-01)**: i18next 25.x, react-i18next 16.x, react-intl 8.x, vue-i18n 11.x, next-intl 4.x, @angular/localize 21.x. Always verify current versions in the target repo (see Currency Check Protocol).

**Authoritative References**:
- [i18next Documentation](https://www.i18next.com/)
- [FormatJS/react-intl](https://formatjs.github.io/)
- [ICU Message Format](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [MDN Intl API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)

## Quick Reference

| Task | Tool/Library | Command | When to Use |
|------|--------------|---------|-------------|
| React i18n | react-i18next | `npm i i18next react-i18next` | Most React apps, flexibility |
| React i18n (ICU) | react-intl (FormatJS) | `npm i react-intl` | ICU-first message catalog + tooling |
| Vue i18n | vue-i18n | `npm i vue-i18n` | Vue 3 apps |
| Angular i18n | @angular/localize | `ng add @angular/localize` | Angular apps |
| Next.js i18n | next-intl | `npm i next-intl` | Next.js App Router |
| Minimal bundle | LinguiJS | `npm i @lingui/core @lingui/react` | Bundle size critical |
| Type-safe | typesafe-i18n | `npm i typesafe-i18n` | TypeScript-first projects |
| String extraction | i18next-parser | `npx i18next-parser` | Extract keys from code |
| ICU linting | @formatjs/cli | `npx formatjs extract` | Validate ICU messages |

## Decision Tree: Library Selection

```text
Project requirements:
    │
    ├─ React/Next.js project?
    │   ├─ ICU-first message catalogs + FormatJS tooling?
    │   │   └─ react-intl (FormatJS)
    │   │
    │   ├─ Flexibility, plugins, lazy loading?
    │   │   └─ react-i18next
    │   │
    │   ├─ Bundle size critical?
    │   │   └─ LinguiJS (ICU syntax)
    │   │
    │   └─ TypeScript-first, compile-time safety?
    │       └─ typesafe-i18n
    │
    ├─ Vue/Nuxt project?
    │   └─ vue-i18n (Composition API)
    │
    ├─ Angular project?
    │   ├─ Built-in solution preferred?
    │   │   └─ @angular/localize (first-party, AOT support)
    │   │
    │   └─ Need i18next ecosystem?
    │       └─ angular-i18next (wrapper)
    │
    └─ Framework-agnostic / Node.js?
        └─ i18next core (works everywhere)
```

## Library Comparison

| Library | ICU Support | Lazy Loading | TypeScript | Best For |
|---------|-------------|--------------|------------|----------|
| react-i18next | Plugin/optional | Native | Good | Flexible, popular React choice |
| react-intl | Native | Manual | Good | ICU-first catalogs + tooling |
| LinguiJS | Native | Native | Excellent | Bundle-conscious apps |
| typesafe-i18n | Limited | Manual | Excellent | Compile-time key safety |
| vue-i18n | Native | Native | Good | Vue 3 apps |
| @angular/localize | Native | AOT | Native | Angular apps |

## Core Concepts

### Character Encoding (Critical)

**Always use UTF-8** across your entire stack to prevent text corruption:

```text
PASS Required: UTF-8 everywhere
- Database: utf8mb4 (MySQL) or UTF-8 (PostgreSQL)
- HTML: <meta charset="UTF-8">
- HTTP headers: Content-Type: text/html; charset=utf-8
- File encoding: Save all source files as UTF-8
- API responses: JSON with UTF-8 encoding
```

UTF-8 supports all Unicode characters including emojis, mathematical symbols, and all language scripts. Inconsistent encoding causes: corrupted characters (�), failed searches for accented names, and rejected international input.

### Translation Key Patterns

```typescript
// Flat keys (simple)
"welcome": "Welcome to our app"
"user.greeting": "Hello, {name}"

// Nested keys (organised)
{
  "user": {
    "greeting": "Hello, {name}",
    "profile": {
      "title": "Your Profile"
    }
  }
}

// Namespace separation (scalable)
// common.json, auth.json, dashboard.json
```

### ICU Message Format Essentials

```text
// Simple interpolation
"Hello, {name}!"

// Pluralisation
"{count, plural, one {# item} other {# items}}"

// Select (gender, category)
"{gender, select, male {He} female {She} other {They}} liked your post"

// Number formatting
"Price: {price, number, currency}"

// Date formatting
"Posted: {date, date, medium}"
```

### Locale Detection Strategy

```text
Priority order:
1. User preference (stored in profile/localStorage)
2. URL parameter or path (/en/about, ?lang=de)
3. Cookie (NEXT_LOCALE, i18next)
4. Accept-Language header
5. Default locale fallback
```

## Navigation

### Resources (Deep Dives)

- [references/framework-guides.md](references/framework-guides.md) - React, Vue, Angular, Next.js implementation
- [references/icu-message-format.md](references/icu-message-format.md) - Pluralisation, select, formatting
- [references/translation-workflows.md](references/translation-workflows.md) - TMS, CI/CD, string extraction
- [references/rtl-support.md](references/rtl-support.md) - Right-to-left language support
- [references/locale-handling.md](references/locale-handling.md) - Dates, numbers, currencies

### Templates (Production Starters)

- [assets/react-i18next-setup.md](assets/react-i18next-setup.md) - React + i18next complete setup
- [assets/vue-i18n-setup.md](assets/vue-i18n-setup.md) - Vue 3 + vue-i18n setup
- [assets/nextjs-i18n-setup.md](assets/nextjs-i18n-setup.md) - Next.js App Router i18n

### Data

- [data/sources.json](data/sources.json) - 60+ curated external references

### Related Skills

- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) - Frontend architecture patterns (React, Vue, Angular, Next.js)
- [../marketing-seo-complete/SKILL.md](../marketing-seo-complete/SKILL.md) - Hreflang, international SEO

## Common Patterns

### Namespace Organisation

```text
locales/
├── en/
│   ├── common.json      # Shared: buttons, errors, nav
│   ├── auth.json        # Login, register, password
│   ├── dashboard.json   # Dashboard-specific
│   └── validation.json  # Form validation messages
├── de/
│   └── ... (same structure)
└── ar/
    └── ... (same structure)
```

### Lazy Loading (Performance)

```typescript
// i18next: Load namespaces on demand
i18n.loadNamespaces('dashboard').then(() => {
  // Dashboard translations now available
});

// React Suspense integration
<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

### TypeScript Integration

```typescript
// resources.d.ts - Type-safe keys
import common from './locales/en/common.json';

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common';
    resources: {
      common: typeof common;
    };
  }
}

// Now t('nonexistent') shows TypeScript error
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Hardcoded strings | Not translatable | Extract all user-facing text |
| String concatenation | Breaks translation context | Use interpolation `{name}` |
| Manual pluralisation | Wrong for many languages | Use ICU plural rules |
| Inline styles for RTL | Doesn't scale | Use CSS logical properties |
| Storing locale in URL only | Lost on navigation | Also persist to cookie/storage |
| No fallback locale | Blank text for missing keys | Always set `fallbackLng` |
| Loading all locales upfront | Slow initial load | Lazy load per namespace/locale |

## Operational Checklist

### Initial Setup

- REQUIRED: Choose i18n library based on decision tree
- REQUIRED: Set up directory structure for translations
- REQUIRED: Configure fallback locale chain
- REQUIRED: Set up locale detection strategy
- REQUIRED: Add TypeScript types for translation keys
- REQUIRED: Configure lazy loading for namespaces

### Translation Workflow

- REQUIRED: Set up string extraction (i18next-parser, formatjs, Lingui)
- REQUIRED: Integrate with a TMS when needed (Phrase, Lokalise, Crowdin, Locize)
- REQUIRED: Configure CI/CD for translation sync
- REQUIRED: Set up translation review process (glossary + style guide + QA gates)
- REQUIRED: Add missing key detection in development

### RTL Support

- REQUIRED: Use CSS logical properties (margin-inline-start)
- REQUIRED: Set `dir="rtl"` for RTL locales
- REQUIRED: Test with real RTL content (Arabic, Hebrew)
- REQUIRED: Handle bidirectional text (BiDi) in mixed strings
- REQUIRED: Mirror directional icons and images where appropriate

### Testing

- REQUIRED: Test pluralisation with 0, 1, 2, 5, 21 (language-specific)
- REQUIRED: Test date/number/currency formatting per locale
- REQUIRED: Test RTL layout in key screens/components
- REQUIRED: Test missing translation key handling (dev-only warnings)
- REQUIRED: Test locale switching and persistence (cookie/storage/url)

## Currency Check Protocol

When recommending libraries, versions, or tooling, verify what is current for the target ecosystem and project constraints. Prefer package registries and release notes over stale hard-coded numbers.

### Package versions (Node/npm)

```bash
npm view i18next version
npm view react-i18next version
npm view react-intl version
npm view vue-i18n version
npm view next-intl version
npm view @angular/localize version
npm view @lingui/core version
npm view typesafe-i18n version
```

### "Is X still recommended?" checks

- Check the project's last release date, open issues, and maintenance activity (GitHub releases/issues).
- Check framework compatibility (Next.js App Router/RSC, React 19, Vue 3, Angular current major).
- For bundle concerns, measure in the real app with a bundle analyzer instead of relying on published size claims.
