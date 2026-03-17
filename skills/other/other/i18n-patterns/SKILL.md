---
name: i18n Patterns
description: Internationalization and translation patterns in LivestockAI
---

# i18n Patterns

LivestockAI supports multiple languages using i18next.

## Configuration

The i18n config is in `app/lib/i18n/`:

```typescript
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

i18n.use(initReactI18next).init({
  lng: 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
})
```

## Using Translations

```typescript
import { useTranslation } from 'react-i18next'

function MyComponent() {
  const { t } = useTranslation()

  return (
    <div>
      <h1>{t('dashboard.title')}</h1>
      <p>{t('dashboard.welcome', { name: user.name })}</p>
    </div>
  )
}
```

## Supported Languages

| Code | Language   | Status      |
| ---- | ---------- | ----------- |
| en   | English    | Complete    |
| fr   | French     | Complete    |
| es   | Spanish    | Complete    |
| pt   | Portuguese | Complete    |
| sw   | Swahili    | Complete    |
| ha   | Hausa      | In progress |
| ar   | Arabic     | Planned     |

## Translation Files

Translations are in `app/lib/i18n/locales/`:

```
locales/
├── en.json
├── fr.json
├── es.json
├── pt.json
├── sw.json
└── ha.json
```

## Key Namespaces

```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete"
  },
  "dashboard": {
    "title": "Dashboard",
    "welcome": "Welcome, {{name}}"
  },
  "batches": {
    "title": "Batches",
    "create": "Create Batch"
  }
}
```

## Pluralization

```typescript
// Translation file
{
  "birds": "{{count}} bird",
  "birds_plural": "{{count}} birds"
}

// Usage
t('birds', { count: 1 })  // "1 bird"
t('birds', { count: 5 })  // "5 birds"
```

## Date/Number Formatting

Use user settings for locale-aware formatting:

```typescript
import { useFormatDate, useFormatNumber } from '~/features/settings'

function MyComponent() {
  const formatDate = useFormatDate()
  const formatNumber = useFormatNumber()

  return (
    <div>
      <span>{formatDate(new Date())}</span>
      <span>{formatNumber(1234.56)}</span>
    </div>
  )
}
```

## Related Skills

- `multi-currency` - Currency formatting
- `rugged-utility` - UI design principles
