---
name: software-localisation
description: Production-grade i18n/l10n patterns for React, Vue, Angular, and Node.js. Covers i18next, react-intl, vue-i18n, ICU message format, RTL support, TMS integration, and CI/CD translation workflows.
---

# Software Localisation — Quick Reference

Production patterns for internationalisation (i18n) and localisation (l10n) in modern web applications. Covers library selection, translation management, ICU message format, RTL support, and CI/CD workflows.

**Modern Best Practices (Dec 2025)**: react-i18next 15.x (2.1M weekly downloads), react-intl 7.x (FormatJS), vue-i18n 10.x (Vue 3 Composition API), @angular/localize 19.x, LinguiJS 5.x (smallest bundle). ICU MessageFormat 2.0 draft, CLDR 46. TMS leaders: Phrase, Lokalise, Crowdin.

**Authoritative References**:
- [i18next Documentation](https://www.i18next.com/)
- [FormatJS/react-intl](https://formatjs.github.io/)
- [ICU Message Format](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [MDN Intl API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)

---

## Quick Reference

| Task | Tool/Library | Command | When to Use |
|------|--------------|---------|-------------|
| React i18n | react-i18next 15.x | `npm i i18next react-i18next` | Most React apps, flexibility |
| React i18n (ICU) | react-intl 7.x | `npm i react-intl` | Enterprise, ICU/CLDR standards |
| Vue i18n | vue-i18n 10.x | `npm i vue-i18n` | Vue 3 apps |
| Angular i18n | @angular/localize 19.x | `ng add @angular/localize` | Angular apps |
| Next.js i18n | next-intl 3.x | `npm i next-intl` | Next.js App Router |
| Minimal bundle | LinguiJS 5.x | `npm i @lingui/core @lingui/react` | Bundle size critical |
| Type-safe | typesafe-i18n 5.x | `npm i typesafe-i18n` | TypeScript-first projects |
| String extraction | i18next-parser | `npx i18next-parser` | Extract keys from code |
| ICU linting | @formatjs/cli | `npx formatjs extract` | Validate ICU messages |

---

## When to Use This Skill

Use this skill when the user requests:

- Setting up i18n/l10n in a React, Vue, Angular, or Next.js project
- Choosing between i18n libraries (i18next vs react-intl vs LinguiJS)
- Implementing pluralisation, interpolation, or ICU message format
- Adding RTL (right-to-left) language support
- Integrating with translation management systems (TMS)
- Setting up CI/CD pipelines for translation workflows
- Handling dates, numbers, currencies across locales
- Lazy loading translations for performance
- TypeScript integration with i18n

---

## Decision Tree: Library Selection

```text
Project requirements:
    │
    ├─ React/Next.js project?
    │   ├─ Enterprise, ICU/CLDR standards, TMS-first?
    │   │   └─ react-intl (FormatJS) — 17.8 kB, native ICU
    │   │
    │   ├─ Flexibility, plugins, lazy loading?
    │   │   └─ react-i18next — 22.2 kB, most popular
    │   │
    │   ├─ Bundle size critical (<15 kB)?
    │   │   └─ LinguiJS — 10.4 kB, ICU syntax
    │   │
    │   └─ TypeScript-first, compile-time safety?
    │       └─ typesafe-i18n — 2 kB runtime
    │
    ├─ Vue/Nuxt project?
    │   └─ vue-i18n — Native Vue integration, Composition API
    │
    ├─ Angular project?
    │   ├─ Built-in solution preferred?
    │   │   └─ @angular/localize — First-party, AOT support
    │   │
    │   └─ Need i18next ecosystem?
    │       └─ angular-i18next — Plugin wrapper
    │
    └─ Framework-agnostic / Node.js?
        └─ i18next core — Works everywhere
```

---

## Library Comparison

| Library | Bundle Size | ICU Support | Lazy Loading | TypeScript | Best For |
|---------|-------------|-------------|--------------|------------|----------|
| react-i18next | 22.2 kB | Plugin | Native | Good | Most React apps |
| react-intl | 17.8 kB | Native | Manual | Good | Enterprise, ICU standards |
| LinguiJS | 10.4 kB | Native | Native | Excellent | Bundle-conscious apps |
| typesafe-i18n | 2 kB | No | Manual | Excellent | TypeScript-first |
| vue-i18n | ~15 kB | Native | Native | Good | Vue 3 apps |
| @angular/localize | Built-in | Native | AOT | Native | Angular apps |

---

## Core Concepts

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

---

## Navigation

### Resources (Deep Dives)

- [resources/framework-guides.md](resources/framework-guides.md) — React, Vue, Angular, Next.js implementation
- [resources/icu-message-format.md](resources/icu-message-format.md) — Pluralisation, select, formatting
- [resources/translation-workflows.md](resources/translation-workflows.md) — TMS, CI/CD, string extraction
- [resources/rtl-support.md](resources/rtl-support.md) — Right-to-left language support
- [resources/locale-handling.md](resources/locale-handling.md) — Dates, numbers, currencies

### Templates (Production Starters)

- [templates/react-i18next-setup.md](templates/react-i18next-setup.md) — React + i18next complete setup
- [templates/vue-i18n-setup.md](templates/vue-i18n-setup.md) — Vue 3 + vue-i18n setup
- [templates/nextjs-i18n-setup.md](templates/nextjs-i18n-setup.md) — Next.js App Router i18n

### Data

- [data/sources.json](data/sources.json) — 50+ curated external references

### Related Skills

- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Frontend architecture patterns (React, Vue, Angular, Next.js)
- [../marketing-seo-technical/SKILL.md](../marketing-seo-technical/SKILL.md) — Hreflang, international SEO

---

## Quick Setup Examples

### React + i18next (5 minutes)

```bash
npm install i18next react-i18next i18next-http-backend i18next-browser-languagedetector
```

```typescript
// src/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    ns: ['common', 'auth', 'dashboard'],
    defaultNS: 'common',
    interpolation: { escapeValue: false },
    backend: { loadPath: '/locales/{{lng}}/{{ns}}.json' }
  });

export default i18n;
```

```typescript
// Usage in component
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome')}</h1>;
}
```

### Vue 3 + vue-i18n (5 minutes)

```bash
npm install vue-i18n
```

```typescript
// src/i18n.ts
import { createI18n } from 'vue-i18n';

export const i18n = createI18n({
  legacy: false, // Composition API
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: { welcome: 'Welcome' },
    de: { welcome: 'Willkommen' }
  }
});
```

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

<template>
  <h1>{{ t('welcome') }}</h1>
</template>
```

### Next.js App Router + next-intl (5 minutes)

```bash
npm install next-intl
```

```typescript
// i18n/request.ts
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`../messages/${locale}.json`)).default
}));
```

```typescript
// app/[locale]/page.tsx
import { useTranslations } from 'next-intl';

export default function Home() {
  const t = useTranslations('Home');
  return <h1>{t('welcome')}</h1>;
}
```

---

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

---

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

---

## Operational Checklist

### Initial Setup

- [ ] Choose i18n library based on decision tree
- [ ] Set up directory structure for translations
- [ ] Configure fallback locale chain
- [ ] Set up locale detection strategy
- [ ] Add TypeScript types for translation keys
- [ ] Configure lazy loading for namespaces

### Translation Workflow

- [ ] Set up string extraction (i18next-parser, formatjs)
- [ ] Integrate with TMS (Phrase, Lokalise, Crowdin)
- [ ] Configure CI/CD for translation sync
- [ ] Set up translation review process
- [ ] Add missing key detection in development

### RTL Support

- [ ] Use CSS logical properties (margin-inline-start)
- [ ] Add dir="rtl" to html/body for RTL locales
- [ ] Test with actual RTL content (Arabic, Hebrew)
- [ ] Handle bidirectional text (BiDi)
- [ ] Mirror icons and images where appropriate

### Testing

- [ ] Test pluralisation with 0, 1, 2, 5, 21 (language-specific)
- [ ] Test date/number formatting per locale
- [ ] Test RTL layout in all components
- [ ] Test missing translation key handling
- [ ] Test locale switching without page reload
