---
name: i18next
description: >-
  Internationalize JavaScript apps with i18next. Use when adding translations,
  handling plurals, loading locale files dynamically, or i18n for React/Vue/Node.
license: Apache-2.0
compatibility: 'React, Vue, Node.js, vanilla JS'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags: [i18next, i18n, localization, translations, react-i18next]
---

# i18next

## Overview

i18next is the most popular JS i18n framework. Works with React, Vue, Angular, Node.js. Features: namespace splitting, lazy loading, plurals, interpolation, context, and backend plugins for remote translations.

## Instructions

### Step 1: React Setup

```typescript
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import HttpBackend from 'i18next-http-backend'
import LanguageDetector from 'i18next-browser-languagedetector'

i18n.use(HttpBackend).use(LanguageDetector).use(initReactI18next).init({
  fallbackLng: 'en',
  supportedLngs: ['en', 'de', 'fr', 'ja'],
  ns: ['common', 'dashboard'],
  defaultNS: 'common',
  backend: { loadPath: '/locales/{{lng}}/{{ns}}.json' },
})
```

### Step 2: Usage

```tsx
import { useTranslation, Trans } from 'react-i18next'

function Dashboard() {
  const { t } = useTranslation('dashboard')
  return (
    <div>
      <h1>{t('welcome', { name: 'Alice' })}</h1>
      <p>{t('projects', { count: 5 })}</p>
      <Trans i18nKey="terms">Agree to <a href="/terms">Terms</a>.</Trans>
    </div>
  )
}
```

```json
{
  "welcome": "Welcome back, {{name}}!",
  "projects_one": "You have {{count}} project",
  "projects_other": "You have {{count}} projects"
}
```

## Guidelines

- Split translations into namespaces by feature — don't load everything.
- Use `_one`/`_other` suffixes for plurals.
- `<Trans>` for translations with embedded JSX.
- Language detection: browser → URL → cookie → localStorage.
- For SSR: pass language from server to avoid hydration mismatch.
