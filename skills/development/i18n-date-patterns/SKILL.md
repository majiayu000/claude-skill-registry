---
name: i18n-date-patterns
description: Use this skill for internationalization (i18n) in React applications. Covers ALL user-facing strings, date/time handling, locale-aware formatting (useFormatting hook), ICU MessageFormat, Trans component, and RTL/LTR support.
context: fork
agent: frontend-ui-developer
version: 1.2.0
author: Yonatan Gross
tags: [i18n, internationalization, dayjs, dates, react-i18next, localization, rtl, useTranslation, useFormatting, ICU, Trans]
user-invocable: false
---

# i18n and Localization Patterns

## Overview

This skill provides comprehensive guidance for implementing internationalization in React applications. It ensures ALL user-facing strings, date displays, currency, lists, and time calculations are locale-aware.

**When to use this skill:**
- Adding ANY user-facing text to components
- Formatting dates, times, currency, lists, or ordinals
- Implementing complex pluralization
- Embedding React components in translated text
- Supporting RTL languages (Hebrew, Arabic)

**Bundled Resources:**
- `references/formatting-utilities.md` - useFormatting hook API reference
- `references/icu-messageformat.md` - ICU plural/select syntax
- `references/trans-component.md` - Trans component for rich text
- `checklists/i18n-checklist.md` - Implementation and review checklist
- `examples/component-i18n-example.md` - Complete component example

**Canonical Reference:** See `docs/i18n-standards.md` for the full i18n standards document.

---

## Core Patterns

### 1. useTranslation Hook (All UI Strings)

Every visible string MUST use the translation function:

```tsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation(['patients', 'common']);
  
  return (
    <div>
      <h1>{t('patients:title')}</h1>
      <button>{t('common:actions.save')}</button>
    </div>
  );
}
```

### 2. useFormatting Hook (Locale-Aware Data)

All locale-sensitive formatting MUST use the centralized hook:

```tsx
import { useFormatting } from '@/hooks';

function PriceDisplay({ amount, items }) {
  const { formatILS, formatList, formatOrdinal } = useFormatting();
  
  return (
    <div>
      <p>Price: {formatILS(amount)}</p>        {/* ₪1,500.00 */}
      <p>Items: {formatList(items)}</p>        {/* "a, b, and c" */}
      <p>Position: {formatOrdinal(3)}</p>      {/* "3rd" */}
    </div>
  );
}
```

See `references/formatting-utilities.md` for the complete API.

### 3. Date Formatting

All dates MUST use the centralized `@/lib/dates` library:

```tsx
import { formatDate, formatDateShort, calculateWaitTime } from '@/lib/dates';

const date = formatDate(appointment.date);    // "Jan 6, 2026"
const waitTime = calculateWaitTime('09:30');  // "15 min"
```

### 4. ICU MessageFormat (Complex Plurals)

Use ICU syntax in translation files for pluralization:

```json
{
  "patients": "{count, plural, =0 {No patients} one {# patient} other {# patients}}"
}
```

```tsx
t('patients', { count: 5 })  // → "5 patients"
```

See `references/icu-messageformat.md` for full syntax.

### 5. Trans Component (Rich Text)

For embedded React components in translated text:

```tsx
import { Trans } from 'react-i18next';

<Trans
  i18nKey="richText.welcome"
  values={{ name: userName }}
  components={{ strong: <strong /> }}
/>
```

See `references/trans-component.md` for patterns.

---

## Translation File Structure

```
frontend/src/i18n/locales/
├── en/
│   ├── common.json      # Shared: actions, status, time
│   ├── patients.json    # Patient-related strings
│   ├── dashboard.json   # Dashboard strings
│   ├── owner.json       # Owner portal strings
│   └── invoices.json    # Invoice strings
└── he/
    └── (same structure)
```

---

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ NEVER hardcode strings
<h1>מטופלים</h1>                    // Use t('patients:title')
<button>Save</button>               // Use t('common:actions.save')

// ❌ NEVER use .join() for lists
items.join(', ')                    // Use formatList(items)

// ❌ NEVER hardcode currency
"₪" + price                         // Use formatILS(price)

// ❌ NEVER use new Date() for formatting
new Date().toLocaleDateString()     // Use formatDate() from @/lib/dates

// ❌ NEVER use inline plural logic
count === 1 ? 'item' : 'items'      // Use ICU MessageFormat

// ❌ NEVER leave console.log in production
console.log('debug')                // Remove before commit

// ❌ NEVER use dangerouslySetInnerHTML for i18n
dangerouslySetInnerHTML             // Use <Trans> component
```

---

## Quick Reference

| Need | Solution |
|------|----------|
| UI text | `t('namespace:key')` from `useTranslation` |
| Currency | `formatILS(amount)` from `useFormatting` |
| Lists | `formatList(items)` from `useFormatting` |
| Ordinals | `formatOrdinal(n)` from `useFormatting` |
| Dates | `formatDate(date)` from `@/lib/dates` |
| Plurals | ICU MessageFormat in translation files |
| Rich text | `<Trans>` component |
| RTL check | `isRTL` from `useFormatting` |

---

## Checklist

See `checklists/i18n-checklist.md` for complete implementation and review checklists.

---

## Integration with Agents

### Frontend UI Developer
- Uses all i18n patterns for components
- References this skill for formatting
- Ensures no hardcoded strings

### Code Quality Reviewer
- Checks for anti-patterns (`.join()`, `console.log`, etc.)
- Validates translation key coverage
- Ensures RTL compatibility

---

**Skill Version**: 1.2.0
**Last Updated**: 2026-01-06
**Maintained by**: Yonatan Gross

## Related Skills

- `a11y-testing` - Accessibility testing for internationalized components and RTL layouts
- `type-safety-validation` - Zod schemas for validating translation key structures and locale configs
- `react-server-components-framework` - Server-side locale detection and RSC i18n patterns
- `focus-management` - RTL-aware focus management for bidirectional UI navigation

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Translation Library | react-i18next | React-native hooks, namespace support, ICU format |
| Date Library | dayjs | Lightweight, locale plugins, immutable API |
| Message Format | ICU MessageFormat | Industry standard, complex plural/select support |
| Locale Storage | Per-namespace JSON | Code-splitting, lazy loading per feature |
| RTL Detection | CSS logical properties | Native browser support, no JS overhead |

## Capability Details

### translation-hooks
**Keywords:** useTranslation, t(), i18n hook, translation hook
**Solves:**
- Translate UI strings with useTranslation
- Implement namespaced translations
- Handle missing translation keys

### formatting-hooks
**Keywords:** useFormatting, formatCurrency, formatList, formatOrdinal
**Solves:**
- Format currency values with locale
- Format lists with proper separators
- Handle ordinal numbers across locales

### icu-messageformat
**Keywords:** ICU, MessageFormat, plural, select, pluralization
**Solves:**
- Implement pluralization rules
- Handle gender-specific translations
- Build complex message patterns

### date-time-formatting
**Keywords:** date format, time format, dayjs, locale date, calendar
**Solves:**
- Format dates with dayjs and locale
- Handle timezone-aware formatting
- Build calendar components with i18n

### rtl-support
**Keywords:** RTL, right-to-left, hebrew, arabic, direction
**Solves:**
- Support RTL languages like Hebrew
- Handle bidirectional text
- Configure RTL-aware layouts

### trans-component
**Keywords:** Trans, rich text, embedded JSX, interpolation
**Solves:**
- Embed React components in translations
- Handle rich text formatting
- Implement safe HTML in translations
