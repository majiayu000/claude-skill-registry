---
name: i18n-nextintl
description: |
  Internationalization with next-intl for Next.js 15.
  Supports core/theme/entity message layers, namespace groups, and translation registry.
  Use this skill when adding translations, validating i18n, or working with localized content.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.0.0
---

# i18n with next-intl Skill

Internationalization patterns for Next.js 15 using next-intl with auto-generated translation registry.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSLATION SOURCES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CORE MESSAGES (Application-wide)                            │
│     core/messages/{locale}/                                     │
│     ├── index.ts          # Re-exports all namespaces           │
│     ├── common.json       # Buttons, labels, etc.               │
│     ├── auth.json         # Authentication messages             │
│     ├── dashboard.json    # Dashboard UI                        │
│     └── ...                                                     │
│                                                                 │
│  2. THEME MESSAGES (Theme-specific overrides)                   │
│     contents/themes/{theme}/messages/{locale}.json              │
│     - Extends/overrides core translations                       │
│     - Custom roles (editor, moderator) ONLY here                │
│                                                                 │
│  3. ENTITY MESSAGES (Entity-specific)                           │
│     contents/themes/{theme}/entities/{entity}/messages/         │
│     - Field labels, placeholders, descriptions                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## When to Use This Skill

- Adding new translations to components
- Validating translation completeness (EN/ES)
- Finding hardcoded strings in UI
- Understanding namespace structure
- Working with custom team roles (theme-level only)

## Supported Locales

- `en` - English (default)
- `es` - Spanish

## Key Concepts

### Namespace Groups

The system uses optimized namespace loading based on page context:

```typescript
const NAMESPACE_GROUPS = {
  // Public pages (includes auth for login/signup buttons)
  PUBLIC_INITIAL: ['common', 'public', 'auth'],

  // Dashboard (authenticated users)
  DASHBOARD_AUTHENTICATED: ['common', 'dashboard', 'settings', 'public', 'teams'],

  // Auth-specific pages
  AUTH_ONLY: ['common', 'auth', 'validation'],

  // Fallback (all namespaces)
  ALL: ['common', 'dashboard', 'settings', 'auth', 'public', 'validation', 'teams']
}
```

### Translation Registry

Auto-generated at `core/lib/registries/translation-registry.ts`:

```typescript
// ✅ CORRECT - Use registry functions
import { loadThemeTranslation } from '@/core/lib/registries/translation-registry'

const translations = await loadThemeTranslation(themeName, locale)

// ❌ NEVER - Runtime string interpolation
const translations = await import(`@/contents/themes/${theme}/messages/${locale}.json`)
```

## Component Patterns

### Server Components

```typescript
import { getTranslations } from 'next-intl/server'

export default async function WelcomePage() {
  const t = await getTranslations('welcome')

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
    </div>
  )
}
```

### Client Components

```typescript
'use client'
import { useTranslations } from 'next-intl'

export function WelcomeCard() {
  const t = useTranslations('welcome')

  return (
    <div>
      <h2>{t('title')}</h2>
      <p>{t('description')}</p>
    </div>
  )
}
```

### With Dynamic Values

```typescript
// Translation file
{
  "welcome": {
    "greeting": "Hello, {name}!",
    "items": "{count, plural, =0 {No items} =1 {One item} other {# items}}"
  }
}

// Component
const t = useTranslations('welcome')
<p>{t('greeting', { name: user.name })}</p>
<p>{t('items', { count: items.length })}</p>
```

## Custom Roles Rule (CRITICAL)

**Custom role translations MUST NEVER be in core/messages/. They belong ONLY in theme messages.**

| Translation Key | Core (`core/messages/`) | Theme (`contents/themes/*/messages/`) |
|-----------------|-------------------------|---------------------------------------|
| `teams.roles.owner` | MUST define here | Can override |
| `teams.roles.admin` | MUST define here | Can override |
| `teams.roles.member` | MUST define here | Can override |
| `teams.roles.viewer` | MUST define here | Can override |
| `teams.roles.editor` | MUST NOT define | MUST define here |
| `teams.roles.moderator` | MUST NOT define | MUST define here |

### Correct Pattern

```json
// core/messages/en/teams.json - ONLY core roles
{
  "teams": {
    "roles": {
      "owner": "Owner",
      "admin": "Administrator",
      "member": "Member",
      "viewer": "Viewer"
    }
  }
}

// contents/themes/default/messages/en.json - Theme extends
{
  "teams": {
    "roles": {
      "editor": "Editor",
      "moderator": "Moderator"
    }
  }
}
```

## Translation Key Naming

```typescript
// ✅ CORRECT - Hierarchical, descriptive
{
  "auth": {
    "login": {
      "title": "Sign In",
      "emailLabel": "Email Address",
      "errors": {
        "invalidCredentials": "Invalid email or password"
      }
    }
  }
}

// ❌ FORBIDDEN - Flat, unclear keys
{
  "login_title": "Sign In",
  "email": "Email"
}
```

## Scripts

### Find Hardcoded Strings
```bash
# Find hardcoded strings in components
python .claude/skills/i18n-nextintl/scripts/extract-hardcoded.py \
  --path contents/themes/default/components/

# Preview without file details
python .claude/skills/i18n-nextintl/scripts/extract-hardcoded.py \
  --path app/ \
  --dry-run
```

### Validate Translation Completeness
```bash
# Compare EN and ES translations
python .claude/skills/i18n-nextintl/scripts/validate-translations.py

# Check theme-specific translations
python .claude/skills/i18n-nextintl/scripts/validate-translations.py \
  --theme default

# Strict mode (exit with error if missing keys)
python .claude/skills/i18n-nextintl/scripts/validate-translations.py \
  --strict
```

### Add Translation Key
```bash
# Add key to both locales
python .claude/skills/i18n-nextintl/scripts/add-translation.py \
  --key "settings.profile.title" \
  --en "Profile Settings" \
  --es "Configuracion de Perfil"

# Add to theme messages instead of core
python .claude/skills/i18n-nextintl/scripts/add-translation.py \
  --key "teams.roles.editor" \
  --en "Editor" \
  --es "Editor" \
  --theme default

# Preview without writing
python .claude/skills/i18n-nextintl/scripts/add-translation.py \
  --key "new.key" \
  --en "Value" \
  --es "Valor" \
  --dry-run
```

## Anti-Patterns

```typescript
// ❌ NEVER: Hardcoded user-facing text
export function WelcomeCard() {
  return <h1>Welcome to Dashboard</h1>  // Wrong!
}

// ❌ NEVER: String concatenation
const message = "Welcome, " + userName + "!"

// ❌ NEVER: Runtime string interpolation in imports
const translations = await import(`@/core/messages/${locale}/`)

// ✅ CORRECT: Use translations
export function WelcomeCard() {
  const t = useTranslations('dashboard')
  return <h1>{t('welcome')}</h1>
}

// ✅ CORRECT: Use interpolation
const message = t('greeting', { name: userName })
```

## File Locations

| Type | Location | Who Modifies |
|------|----------|--------------|
| Core translations | `core/messages/{locale}/` | Core maintainers |
| Theme translations | `contents/themes/{theme}/messages/{locale}.json` | Theme developers |
| Entity translations | Entity config `i18n.loaders` | Entity developers |
| Translation registry | `core/lib/registries/translation-registry.ts` | Auto-generated |
| i18n config | `core/i18n.ts` | Core maintainers |

## Checklist

Before committing i18n changes:

- [ ] All user-facing text uses translation keys (no hardcoded strings)
- [ ] Translation keys exist in ALL supported locales (en, es)
- [ ] Translation keys follow hierarchical naming convention
- [ ] Pluralization uses ICU message format
- [ ] Dynamic values use translation interpolation (no concatenation)
- [ ] Custom roles defined ONLY in theme messages (never core)
- [ ] No runtime string interpolation in dynamic imports
