---
name: react-i18n
description: react-i18next for React 19 - useTranslation hook, TypeScript Selector API, namespaces, pluralization, lazy loading, Suspense integration. Use when implementing translations in React apps (not Next.js).
version: 1.0.0
user-invocable: true
references: references/i18next-basics.md, references/typescript-types.md, references/namespaces.md, references/pluralization.md, references/interpolation.md, references/lazy-loading.md, references/language-detection.md, references/react-19-integration.md, references/trans-component.md, references/testing.md, references/rtl-support.md, references/fallback-strategies.md, references/templates/basic-setup.md, references/templates/language-switcher.md, references/templates/typed-translations.md, references/templates/form-validation-i18n.md, references/templates/lazy-loading-routes.md, references/templates/date-number-formatter.md, references/templates/plural-interpolation.md, references/templates/trans-component-examples.md, references/templates/testing-i18n.md
---

# react-i18next for React 19

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing i18n setup and translation patterns
2. **fuse-ai-pilot:research-expert** - Verify latest react-i18next/i18next docs via Context7/Exa
3. **mcp__context7__query-docs** - Check TypeScript Selector API and React 19 Suspense patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## MANDATORY: SOLID Principles

**ALWAYS apply SOLID principles from `solid-react` skill.**

→ See `../solid-react/SKILL.md` for complete rules

**Key Rules:**
- Files < 100 lines (split at 90)
- Interfaces in `modules/[feature]/src/interfaces/`
- JSDoc mandatory on all exports
- No business logic in components

---

## Core Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useTranslation()` | Access translations and i18n instance | `references/i18next-basics.md` |
| `useTranslation(ns)` | Load specific namespace | `references/namespaces.md` |
| `useTranslation([ns])` | Load multiple namespaces | `references/namespaces.md` |

→ See `references/i18next-basics.md` for detailed usage

---

## Key Packages

| Package | Purpose | Size |
|---------|---------|------|
| `i18next` | Core library | ~40KB |
| `react-i18next` | React bindings | ~12KB |
| `i18next-http-backend` | Lazy loading | ~5KB |
| `i18next-browser-languagedetector` | Auto-detection | ~8KB |

---

## Key Features

### TypeScript Selector API (i18next ≥25.4)
Type-safe translations with autocompletion.
→ See `references/typescript-types.md`

### Namespaces
Organize translations by feature for code splitting.
→ See `references/namespaces.md`

### Pluralization
Count-based rules with ICU MessageFormat support.
→ See `references/pluralization.md`

### Interpolation
Variables, dates, numbers, and currency formatting.
→ See `references/interpolation.md`

### Lazy Loading
Load translations on-demand per route.
→ See `references/lazy-loading.md`

### Language Detection
Auto-detect from browser, URL, cookie, localStorage.
→ See `references/language-detection.md`

### React 19 Integration
Suspense, useTransition, Concurrent Rendering.
→ See `references/react-19-integration.md`

### Trans Component
JSX elements inside translations.
→ See `references/trans-component.md`

### Testing
Mock i18n for unit tests.
→ See `references/testing.md`

### RTL Support
Right-to-left languages (Arabic, Hebrew).
→ See `references/rtl-support.md`

### Fallback Strategies
Handle missing keys gracefully.
→ See `references/fallback-strategies.md`

---

## Templates

| Template | Use Case |
|----------|----------|
| `templates/basic-setup.md` | Configuration with React 19 |
| `templates/language-switcher.md` | Dropdown component |
| `templates/typed-translations.md` | TypeScript Selector API |
| `templates/form-validation-i18n.md` | Translated form errors |
| `templates/lazy-loading-routes.md` | Per-route loading |
| `templates/date-number-formatter.md` | Intl formatting |
| `templates/plural-interpolation.md` | Count-based messages |
| `templates/trans-component-examples.md` | JSX in translations |
| `templates/testing-i18n.md` | Unit test setup |

---

## Modular Architecture (SOLID)

```text
src/
├── modules/cores/i18n/
│   ├── src/
│   │   ├── interfaces/
│   │   │   └── i18n.interface.ts
│   │   ├── services/
│   │   │   └── i18n.service.ts
│   │   ├── hooks/
│   │   │   └── useLanguage.ts
│   │   └── config/
│   │       └── i18n.config.ts
│   ├── components/
│   │   └── LanguageSwitcher.tsx
│   └── locales/
│       ├── en/
│       │   └── translation.json
│       └── fr/
│           └── translation.json
└── main.tsx
```

---

## Best Practices

1. **Suspense**: Wrap app with `<Suspense>` for loading states
2. **Namespaces**: One namespace per feature/module
3. **TypeScript**: Use Selector API for type-safe keys
4. **Lazy Loading**: Load namespaces on-demand
5. **Detection**: Configure language detection order
6. **Fallback**: Always set `fallbackLng`

---

## Forbidden (Anti-Patterns)

- ❌ Hardcoded strings → use `t('key')`
- ❌ No Suspense → causes loading flicker
- ❌ All translations in one file → use namespaces
- ❌ No fallback language → broken UI
- ❌ String concatenation → use interpolation `{{var}}`
- ❌ Manual language state → use `i18n.changeLanguage()`
