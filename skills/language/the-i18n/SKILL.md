---
name: the-i18n
description: Manages internationalization - adds translations, fixes missing keys, and ensures locale consistency.
license: HPL3-ECO-NC-ND-A 2026
---

Task: Audit and maintain internationalization across all 33 supported locales.

Role: You're an internationalization specialist ensuring the app works correctly in all languages.

## Supported Locales

```
ar, be, bg, cs, de, el, en, es, et, fi, fr, he, hi, hr, hu, id,
it, ja, ko, lt, lv, nl, no, pl, pt, ro, ru, sk, sl, sv, th, tr, uk, zh
```

Default locale: `en`

## i18n Architecture

- Translation files: `src/locales/{locale}.json`
- Context: `useI18n()` hook provides `t()` function
- Date formatting: `formatDate()` with locale support
- Task localization: `localeKey` field for translation lookup

## Audit Steps

### 1. Find Missing Translations

```bash
# Extract all translation keys used in code
grep -rh "t\(['\"]" --include="*.tsx" --include="*.ts" src/ |
  grep -oP "t\(['\"][^'\"]+['\"]" |
  sort -u > used_keys.txt

# Compare with en.json
```

### 2. Find Hardcoded Strings

```bash
# Find potential hardcoded text in components
grep -r ">[A-Z][a-z].*<" --include="*.tsx" src/components/
grep -r "title=\"[A-Z]" --include="*.tsx" src/
grep -r "label=\"[A-Z]" --include="*.tsx" src/
```

### 3. Verify All Locales Have Same Keys

```typescript
// Compare key counts across locale files
import en from '@/locales/en.json'
import es from '@/locales/es.json'

const enKeys = Object.keys(flattenObject(en))
const esKeys = Object.keys(flattenObject(es))
const missing = enKeys.filter(k => !esKeys.includes(k))
```

## Translation File Structure

```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "loading": "Loading..."
  },
  "auth": {
    "login": "Log in",
    "logout": "Log out",
    "signUp": "Sign up"
  },
  "tasks": {
    "title": "Tasks",
    "addTask": "Add task",
    "complete": "Mark complete"
  },
  "errors": {
    "generic": "Something went wrong",
    "notFound": "Not found",
    "unauthorized": "Please log in"
  }
}
```

## Usage Patterns

### Basic Translation
```typescript
import { useI18n } from '@/lib/i18n'

function Component() {
  const { t } = useI18n()
  return <h1>{t('page.title')}</h1>
}
```

### With Interpolation
```typescript
// en.json: { "greeting": "Hello, {name}!" }
t('greeting', { name: user.name })
```

### Pluralization
```typescript
// en.json: { "items": "{count, plural, one {# item} other {# items}}" }
t('items', { count: 5 })
```

### Date Formatting
```typescript
const { formatDate } = useI18n()
formatDate(new Date(), 'long') // "January 19, 2026"
formatDate(new Date(), 'short') // "1/19/26"
```

## Task Localization

Tasks use `localeKey` for translation:
```typescript
// Task with localeKey
{ id: '1', localeKey: 'tasks.daily.exercise', name: 'Exercise' }

// Lookup in locale file
{
  "tasks": {
    "daily": {
      "exercise": "Exercise"
    }
  }
}

// Fallback to name if translation missing
const taskName = t(task.localeKey) || task.name
```

## Rules

- Never hardcode user-facing text
- Always provide English fallback
- Use dot notation for nested keys
- Keep keys semantic (describe purpose, not content)
- Group related translations together
- Test RTL languages (Arabic, Hebrew)

## Quality Checks

- [ ] All user-facing strings use `t()`
- [ ] All locales have same key structure
- [ ] Dates formatted with locale
- [ ] Numbers formatted with locale
- [ ] RTL layout works correctly
- [ ] Task localeKeys have translations

## Adding New Translations

1. Add key to `src/locales/en.json`
2. Add translations to all other locale files
3. Use consistent naming convention
4. Test in multiple languages
