---
name: add-react-i18n
description: Add react-i18next internationalization to a React NPM library package. Creates isolated i18n instance, translation files, modifies provider and components. Use when the user wants to add multi-language support to a React component library.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: [default-language] [additional-languages]
---

# Add react-i18next to a React NPM Library Package

This skill adds internationalization (i18n) to a React NPM library package using `react-i18next` with an **isolated i18n instance** pattern that avoids conflicts with the consuming application's own i18n setup.

## Arguments

- `default-language` (optional): The default language code (e.g., `en`, `pt`). Defaults to `en`.
- `additional-languages` (optional): Space-separated additional language codes to create translation files for (e.g., `pt es fr`).

## Overview

The implementation follows these principles:

1. **Isolated i18n instance** — Uses `i18next.createInstance()` instead of the global instance to prevent conflicts with the consuming app
2. **Dedicated namespace** — All library translations live under a unique namespace (derived from the package name) to avoid key collisions
3. **Consumer customization** — The library's Provider accepts `language` and `translations` props so consumers can override/extend translations
4. **Synchronous init** — Uses `initImmediate: false` so translations are available immediately without async loading
5. **Dynamic Zod schemas** — Zod validation schemas are wrapped in factory functions + `useMemo` to re-evaluate when language changes
6. **Utility function i18n** — Utility functions accept an optional `t` parameter with English hardcoded fallback

## Step-by-Step Instructions

### Step 1: Analyze the Project

Before making any changes, thoroughly analyze the project structure:

1. **Find the entry point** — Read `package.json` to find the `main`/`module` field, then read the entry file (usually `src/index.ts`) to understand all public exports.

2. **Find the Provider/Context** — Search for React Context providers. Look for patterns like:
   ```
   Glob: src/**/Context*.tsx, src/**/Provider*.tsx, src/contexts/**
   Grep: createContext, Provider
   ```

3. **Find all components with hardcoded strings** — Search for visible text:
   ```
   Grep patterns: placeholder=", label, >.*</,  title=", aria-label="
   ```
   Read each component and catalog all hardcoded strings (labels, placeholders, error messages, validation messages, button text, titles, etc.).

4. **Find Zod schemas** — Search for `z.object`, `z.string()`, `.email(`, `.min(`, `.max(` to identify validation schemas with hardcoded error messages.

5. **Find utility functions with strings** — Check `src/utils/` or `src/helpers/` for functions that return user-facing strings (e.g., password strength validators, formatters with error messages).

6. **Count total strings** — Estimate the total number of unique translatable strings. This helps plan the translation file structure.

### Step 2: Install Dependencies

```bash
npm install i18next react-i18next
```

Install as **regular dependencies** (not peer), since the library uses its own isolated instance that doesn't need to share with the consuming app.

### Step 3: Create Translation Files

#### Directory structure:
```
src/
  i18n/
    index.ts          # i18n setup + hooks
    locales/
      en.ts           # English translations (always required)
      pt.ts           # Additional languages as needed
      es.ts
```

#### Translation file pattern (`src/i18n/locales/en.ts`):

```typescript
const en = {
  common: {
    email: 'Email',
    password: 'Password',
    cancel: 'Cancel',
    save: 'Save',
    delete: 'Delete',
    loading: 'Loading...',
    // ... shared strings used across multiple components
  },
  validation: {
    emailInvalid: 'Please enter a valid email address',
    passwordRequired: 'Password is required',
    passwordMinLength: 'Password must be at least {{minLength}} characters',
    // ... all validation error messages
  },
  // One section per component/feature:
  login: {
    signIn: 'Sign In',
    signingIn: 'Signing in...',
    rememberMe: 'Remember me',
    // ...
  },
  register: { /* ... */ },
  // etc.
};

export default en;
```

**Key guidelines for translation files:**
- Use **flat namespace with prefixes** per feature/component (e.g., `login.signIn`, `validation.emailInvalid`)
- Use `{{variable}}` syntax for interpolation (i18next standard)
- Keep keys in camelCase
- Group by feature, not by component file
- Put shared strings in `common.*`
- Put all validation messages in `validation.*`
- Export as `default` for clean imports

#### Additional language files:

Copy the English file structure exactly and translate all values. The keys must be identical.

### Step 4: Create i18n Setup (`src/i18n/index.ts`)

```typescript
import i18next, { type Resource } from 'i18next';
import { initReactI18next, useTranslation } from 'react-i18next';
import en from './locales/en';
// import additional languages...

// Derive namespace from package name to avoid collisions
export const NAMESPACE = 'your-lib-name';

export const defaultTranslations = { en /* , pt, es, ... */ };

export function createI18nInstance(
  language: string = 'en',
  customTranslations?: Record<string, Record<string, unknown>>
) {
  const instance = i18next.createInstance();

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const resources: Record<string, Record<string, any>> = {
    en: { [NAMESPACE]: { ...en } },
    // Add built-in languages here...
  };

  // Merge custom translations from consumer
  if (customTranslations) {
    for (const [lang, translations] of Object.entries(customTranslations)) {
      if (resources[lang]) {
        resources[lang][NAMESPACE] = {
          ...resources[lang][NAMESPACE],
          ...translations,
        };
      } else {
        resources[lang] = { [NAMESPACE]: { ...translations } };
      }
    }
  }

  instance.use(initReactI18next).init({
    resources: resources as Resource,
    lng: language,
    fallbackLng: 'en',
    defaultNS: NAMESPACE,
    ns: [NAMESPACE],
    interpolation: { escapeValue: false },
    initImmediate: false, // Synchronous init — critical for SSR and tests
  });

  return instance;
}

export function useLibTranslation() {
  return useTranslation(NAMESPACE);
}
```

**Critical details:**
- `i18next.createInstance()` — NOT the global `i18next` instance
- `initImmediate: false` — Ensures synchronous initialization
- `escapeValue: false` — React already escapes output
- The `customTranslations` parameter allows consumers to add/override translations
- Export the `useLibTranslation` hook for use in components

### Step 5: Modify the Provider/Context Config Types

Add i18n configuration to the library's config interface:

```typescript
export interface LibConfig {
  // ... existing config props
  language?: string;
  translations?: Record<string, Record<string, unknown>>;
}
```

### Step 6: Integrate i18n in the Provider

In the Provider component:

```typescript
import { I18nextProvider } from 'react-i18next';
import { createI18nInstance } from '../i18n';

export const LibProvider: React.FC<ProviderProps> = ({ config, children }) => {
  // Create i18n instance (memoized)
  const i18nInstance = useMemo(
    () => createI18nInstance(config.language, config.translations),
    [config.language, config.translations]
  );

  // Handle language changes
  const currentLang = useRef(config.language);
  useEffect(() => {
    if (config.language && config.language !== currentLang.current) {
      i18nInstance.changeLanguage(config.language);
      currentLang.current = config.language;
    }
  }, [config.language, i18nInstance]);

  return (
    <I18nextProvider i18n={i18nInstance}>
      <LibContext.Provider value={contextValue}>
        {children}
      </LibContext.Provider>
    </I18nextProvider>
  );
};
```

### Step 7: Modify Components

For each component with hardcoded strings, follow this pattern:

#### Import the translation hook:
```typescript
import { useLibTranslation } from '../i18n';
```

#### Inside the component:
```typescript
const { t } = useLibTranslation();
```

#### Replace all hardcoded strings:
```typescript
// Before:
<Label>Email</Label>
<Input placeholder="Enter your email" />
<Button>Sign In</Button>

// After:
<Label>{t('common.email')}</Label>
<Input placeholder={t('login.emailPlaceholder')} />
<Button>{t('login.signIn')}</Button>
```

#### For Zod schemas with validation messages:

Move schemas into factory functions and wrap with `useMemo`:

```typescript
// Before (outside component):
const schema = z.object({
  email: z.string().email('Please enter a valid email'),
});

// After:
function createSchema(t: (key: string) => string) {
  return z.object({
    email: z.string().email(t('validation.emailInvalid')),
  });
}

// Inside component:
const { t } = useLibTranslation();
const schema = useMemo(() => createSchema(t), [t]);
```

This ensures validation messages update when the language changes.

#### For interpolated strings:
```typescript
// Translation key: "Showing {{from}} to {{to}} of {{total}}"
t('common.showingFromTo', { from: startIndex, to: endIndex, total: totalItems })
```

#### For conditional text:
```typescript
// Translation keys: "status.active", "status.inactive", etc.
const STATUS_KEYS: Record<string, string> = {
  active: 'status.active',
  inactive: 'status.inactive',
};
// Usage:
t(STATUS_KEYS[status])
```

### Step 8: Modify Utility Functions

For utility functions that return user-facing strings, add an optional `t` parameter:

```typescript
export function validateSomething(
  value: string,
  options: {
    // ... existing options
    t?: (key: string, opts?: Record<string, unknown>) => string;
  } = {}
) {
  const { t } = options;

  // Helper: use translation if available, otherwise hardcoded English fallback
  const msg = (key: string, fallback: string, interpolation?: Record<string, unknown>) =>
    t ? t(key, interpolation) : fallback;

  // Usage:
  feedback.push(msg('validation.minLength', `Must be at least ${min} characters`, { min }));
}
```

Components that call these utilities should pass `{ t }`:
```typescript
const { t } = useLibTranslation();
const result = validateSomething(value, { t });
```

### Step 9: Update Public Exports (`src/index.ts`)

Add i18n exports to the entry point:

```typescript
// i18n
export { createI18nInstance, useLibTranslation, NAMESPACE, defaultTranslations } from './i18n';
export { default as enTranslations } from './i18n/locales/en';
export { default as ptTranslations } from './i18n/locales/pt';
// ... other language exports
```

This allows consumers to:
- Access default translations for extending/overriding
- Use the translation hook in their own components
- Reference the namespace constant

### Step 10: Update Tests

Tests need the NAuthProvider (or equivalent) wrapper to initialize i18n. If tests already use the Provider wrapper, they should work without changes.

For form validation tests, use `fireEvent.input` + `fireEvent.submit` instead of `fireEvent.change` + `fireEvent.click` for more reliable Zod schema triggering in jsdom.

If tests fail because translations aren't loading, ensure:
1. The Provider wrapper in tests includes the i18n setup
2. `initImmediate: false` is set in the i18n init config

### Step 11: Verify

Run these checks in order:

```bash
npm run type-check    # TypeScript must pass
npm run lint          # No new warnings
npm test              # All tests must pass
npm run build         # Build must succeed (ES + CJS)
```

## Consumer Usage Examples

### Zero config (English default):
```tsx
<LibProvider config={{ apiUrl: 'https://api.example.com' }}>
  <App />
</LibProvider>
```

### With language selection:
```tsx
<LibProvider config={{ apiUrl: 'https://api.example.com', language: 'pt' }}>
  <App />
</LibProvider>
```

### With custom translations:
```tsx
<LibProvider config={{
  apiUrl: 'https://api.example.com',
  language: 'es',
  translations: {
    es: {
      common: { email: 'Correo electrónico' },
      login: { signIn: 'Iniciar sesión' },
    }
  }
}}>
  <App />
</LibProvider>
```

### Overriding default translations:
```tsx
<LibProvider config={{
  apiUrl: 'https://api.example.com',
  translations: {
    en: { login: { signIn: 'Log In' } } // overrides "Sign In"
  }
}}>
  <App />
</LibProvider>
```

## Checklist

Before marking complete, verify:

- [ ] `i18next` and `react-i18next` installed as regular dependencies
- [ ] Isolated i18n instance created with `createInstance()` (not global)
- [ ] `initImmediate: false` set in init config
- [ ] Translation files created for all specified languages
- [ ] Translation keys organized by feature with `common.*` and `validation.*` shared sections
- [ ] Provider wraps children with `<I18nextProvider>`
- [ ] Config interface includes `language?` and `translations?` props
- [ ] All hardcoded strings in components replaced with `t()` calls
- [ ] Zod schemas use factory functions + `useMemo` with `t` dependency
- [ ] Utility functions accept optional `t` parameter with English fallback
- [ ] i18n utilities exported from entry point
- [ ] TypeScript type-check passes
- [ ] Lint passes (no new warnings)
- [ ] Tests pass
- [ ] Build succeeds
