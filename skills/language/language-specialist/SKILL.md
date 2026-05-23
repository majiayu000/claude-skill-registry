---
name: language-specialist
description: |
  Expert in internationalization (i18n) and localization (l10n) for the Raamattu Nyt monorepo.
  Fluent in all world languages with deep knowledge of multilingual app development.

  Use when:
  - Adding translations for new UI strings
  - Creating new translation namespaces
  - Adding support for new languages (sv, de, etc.)
  - Migrating components to use useTranslation()
  - Reviewing translation quality and consistency
  - Fixing translation key mismatches
  - Setting up i18n for new features
  - Working with date/number/currency formatting per locale
  - Handling RTL languages or special character sets

  Triggers: "translate", "translation", "i18n", "l10n", "localization", "language", "Finnish", "English", "Swedish", "multilingual", "locale", "useTranslation"
---

# Language Specialist

Expert assistant for all i18n/l10n work in the Raamattu Nyt project.

## Architecture Overview

```
packages/shared-i18n/          # Shared i18n package
├── src/
│   ├── config.ts              # i18next initialization
│   ├── types.ts               # SupportedLanguage, LANGUAGE_INFO
│   ├── provider.tsx           # I18nProvider component
│   ├── hooks/useLanguage.ts   # Language preference hook
│   └── utils/
│       ├── setLanguage.ts     # Simple language switcher
│       └── dateLocale.ts      # date-fns locale helper

apps/raamattu-nyt/public/locales/   # Translation files (lazy-loaded)
├── fi/
│   ├── common.json            # Shared UI strings
│   └── profile.json           # Profile page strings
└── en/
    ├── common.json
    └── profile.json
```

## Quick Reference

### Add translation to existing namespace

1. Add key to both locale files:
```json
// public/locales/fi/common.json
{ "myKey": "Suomeksi" }

// public/locales/en/common.json
{ "myKey": "In English" }
```

2. Use in component:
```tsx
import { useTranslation } from '@shared-i18n/index';

const { t } = useTranslation('common');
return <span>{t('myKey')}</span>;
```

### Create new namespace

1. Add namespace to `packages/shared-i18n/src/config.ts`:
```ts
ns: ['common', 'profile', 'newNamespace'],
```

2. Create files: `public/locales/{fi,en}/newNamespace.json`

3. Use: `const { t } = useTranslation('newNamespace');`

### Add new language

1. Update `packages/shared-i18n/src/types.ts`:
```ts
export type SupportedLanguage = 'fi' | 'en' | 'sv';
export const SUPPORTED_LANGUAGES = ['fi', 'en', 'sv'] as const;
export const LANGUAGE_INFO = {
  fi: { code: 'fi', name: 'Finnish', nativeName: 'Suomi' },
  en: { code: 'en', name: 'English', nativeName: 'English' },
  sv: { code: 'sv', name: 'Swedish', nativeName: 'Svenska' },
};
```

2. Update DB constraint in new migration:
```sql
ALTER TABLE public.profiles
DROP CONSTRAINT profiles_language_preference_check,
ADD CONSTRAINT profiles_language_preference_check
CHECK (language_preference IN ('fi', 'en', 'sv'));
```

3. Create locale files: `public/locales/sv/*.json`

4. Update `dateLocale.ts` with new locale import

## Translation Patterns

### Interpolation
```json
{ "greeting": "Hello, {{name}}!" }
```
```tsx
t('greeting', { name: 'John' })
```

### Pluralization
```json
{
  "item_one": "{{count}} item",
  "item_other": "{{count}} items"
}
```
```tsx
t('item', { count: 5 })
```

### Nested keys
```json
{ "nav": { "home": "Home", "settings": "Settings" } }
```
```tsx
t('nav.home')
```

### Trans component (JSX interpolation)
```tsx
import { Trans } from '@shared-i18n/index';

<Trans i18nKey="terms" t={t}>
  By continuing you agree to our <Link to="/terms">terms</Link>.
</Trans>
```

## Migration Workflow

When migrating a component to i18n:

1. Identify all user-visible strings
2. Create translation keys (use descriptive, nested structure)
3. Add to appropriate namespace (common for shared, feature-specific otherwise)
4. Replace inline strings with `t()` calls
5. Test both languages

Example migration:
```tsx
// Before
<Button>Tallenna</Button>

// After
const { t } = useTranslation('common');
<Button>{t('common.save')}</Button>
```

## Files Reference

For detailed API and patterns, see [references/i18n-api.md](references/i18n-api.md).
