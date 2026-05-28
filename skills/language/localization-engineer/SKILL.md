---
name: localization-engineer
description: Expert in internationalization (i18n), multi-language support, and localization
version: 1.0.0
tags: [i18n, localization, translation, multilingual, internationalization]
---

# Localization Engineer Skill

I help you build multilingual applications with proper internationalization (i18n) and localization (l10n) support.

## What I Do

**Internationalization:**

- Multi-language text content
- Date/time formatting
- Number and currency formatting
- Right-to-left (RTL) support

**Localization:**

- Translation management
- Language detection
- Language switching
- Locale-specific content

## Next.js Internationalization

### Setup with next-intl

```bash
npm install next-intl
```

```typescript
// i18n/request.ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`../messages/${locale}.json`)).default
}))
```

```typescript
// middleware.ts
import createMiddleware from 'next-intl/middleware'

export default createMiddleware({
  locales: ['en', 'es', 'fr', 'de', 'ja'],
  defaultLocale: 'en'
})

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)']
}
```

### Translation Files

```json
// messages/en.json
{
  "common": {
    "welcome": "Welcome",
    "loading": "Loading...",
    "error": "Something went wrong"
  },
  "navigation": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "auth": {
    "login": "Log in",
    "logout": "Log out",
    "signUp": "Sign up",
    "emailPlaceholder": "Enter your email",
    "passwordPlaceholder": "Enter your password"
  }
}
```

```json
// messages/es.json
{
  "common": {
    "welcome": "Bienvenido",
    "loading": "Cargando...",
    "error": "Algo salió mal"
  },
  "navigation": {
    "home": "Inicio",
    "about": "Acerca de",
    "contact": "Contacto"
  },
  "auth": {
    "login": "Iniciar sesión",
    "logout": "Cerrar sesión",
    "signUp": "Registrarse",
    "emailPlaceholder": "Ingrese su correo electrónico",
    "passwordPlaceholder": "Ingrese su contraseña"
  }
}
```

---

## Using Translations

### Client Component

```typescript
'use client'
import { useTranslations } from 'next-intl'

export function LoginForm() {
  const t = useTranslations('auth')

  return (
    <form>
      <input
        type="email"
        placeholder={t('emailPlaceholder')}
      />
      <input
        type="password"
        placeholder={t('passwordPlaceholder')}
      />
      <button>{t('login')}</button>
    </form>
  )
}
```

### Server Component

```typescript
import { useTranslations } from 'next-intl'

export default function HomePage() {
  const t = useTranslations('common')

  return (
    <div>
      <h1>{t('welcome')}</h1>
    </div>
  )
}
```

---

## Language Switcher

```typescript
'use client'
import { useLocale } from 'next-intl'
import { useRouter, usePathname } from 'next/navigation'

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' }
]

export function LanguageSwitcher() {
  const locale = useLocale()
  const router = useRouter()
  const pathname = usePathname()

  const switchLanguage = (newLocale: string) => {
    // Remove current locale from pathname
    const pathWithoutLocale = pathname.replace(`/${locale}`, '')
    // Navigate to new locale
    router.push(`/${newLocale}${pathWithoutLocale}`)
  }

  return (
    <select
      value={locale}
      onChange={(e) => switchLanguage(e.target.value)}
      className="px-4 py-2 border rounded"
    >
      {languages.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.flag} {lang.name}
        </option>
      ))}
    </select>
  )
}
```

---

## Date and Time Formatting

```typescript
'use client'
import { useFormatter } from 'next-intl'

export function FormattedDate({ date }: { date: Date }) {
  const format = useFormatter()

  return (
    <div>
      {/* Full date */}
      <p>{format.dateTime(date, { dateStyle: 'full' })}</p>

      {/* Short date */}
      <p>{format.dateTime(date, { dateStyle: 'short' })}</p>

      {/* Custom format */}
      <p>{format.dateTime(date, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      })}</p>

      {/* Relative time */}
      <p>{format.relativeTime(date)}</p>
    </div>
  )
}

// Examples:
// en: "Monday, October 22, 2025"
// es: "lunes, 22 de octubre de 2025"
// ja: "2025年10月22日月曜日"
```

---

## Number and Currency Formatting

```typescript
'use client'
import { useFormatter } from 'next-intl'

export function FormattedNumber({ value }: { value: number }) {
  const format = useFormatter()

  return (
    <div>
      {/* Number */}
      <p>{format.number(value)}</p>

      {/* Currency */}
      <p>{format.number(value, { style: 'currency', currency: 'USD' })}</p>

      {/* Percentage */}
      <p>{format.number(value / 100, { style: 'percent' })}</p>

      {/* Compact notation */}
      <p>{format.number(value, { notation: 'compact' })}</p>
    </div>
  )
}

// Examples:
// en: "1,234.56" "$1,234.56" "12%" "1.2K"
// de: "1.234,56" "1.234,56 $" "12 %" "1200"
// ja: "1,234.56" "$1,234.56" "12%" "1.2千"
```

---

## Pluralization

```json
// messages/en.json
{
  "items": {
    "count": "{count, plural, =0 {No items} one {# item} other {# items}}"
  }
}
```

```typescript
'use client'
import { useTranslations } from 'next-intl'

export function ItemCounter({ count }: { count: number }) {
  const t = useTranslations('items')

  return <p>{t('count', { count })}</p>
}

// count = 0: "No items"
// count = 1: "1 item"
// count = 5: "5 items"
```

---

## RTL (Right-to-Left) Support

```typescript
// app/[locale]/layout.tsx
import { useLocale } from 'next-intl'

const rtlLanguages = ['ar', 'he', 'fa']

export default function LocaleLayout({ children }) {
  const locale = useLocale()
  const isRTL = rtlLanguages.includes(locale)

  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body>{children}</body>
    </html>
  )
}
```

**RTL CSS:**

```css
/* Automatically flips for RTL */
.container {
  margin-inline-start: 1rem; /* Use logical properties */
  padding-inline-end: 1rem;
}

/* Manual RTL handling */
[dir='rtl'] .menu {
  left: auto;
  right: 0;
}
```

---

## Language Detection

```typescript
// lib/detect-locale.ts

export function detectUserLocale(): string {
  // 1. Check URL parameter
  const urlParams = new URLSearchParams(window.location.search)
  const urlLocale = urlParams.get('lang')
  if (urlLocale) return urlLocale

  // 2. Check localStorage
  const savedLocale = localStorage.getItem('preferredLocale')
  if (savedLocale) return savedLocale

  // 3. Check browser language
  const browserLocale = navigator.language.split('-')[0]
  return browserLocale

  // 4. Default
  return 'en'
}
```

---

## Translation with Variables

```json
// messages/en.json
{
  "welcome": "Welcome, {name}!",
  "itemsInCart": "You have {count} {count, plural, one {item} other {items}} in your cart",
  "priceDisplay": "Price: {price, number, ::currency/USD}"
}
```

```typescript
'use client'
import { useTranslations } from 'next-intl'

export function Greeting({ userName }: { userName: string }) {
  const t = useTranslations()

  return (
    <div>
      <h1>{t('welcome', { name: userName })}</h1>
      <p>{t('itemsInCart', { count: 3 })}</p>
      <p>{t('priceDisplay', { price: 49.99 })}</p>
    </div>
  )
}

// Output:
// "Welcome, John!"
// "You have 3 items in your cart"
// "Price: $49.99"
```

---

## Locale-Specific Content

```typescript
// app/[locale]/page.tsx
import { useLocale } from 'next-intl'

export default function HomePage() {
  const locale = useLocale()

  const content = {
    en: {
      hero: 'Build amazing apps',
      description: 'The best platform for developers'
    },
    es: {
      hero: 'Crea aplicaciones increíbles',
      description: 'La mejor plataforma para desarrolladores'
    },
    ja: {
      hero: '素晴らしいアプリを作成',
      description: '開発者のための最高のプラットフォーム'
    }
  }

  return (
    <div>
      <h1>{content[locale].hero}</h1>
      <p>{content[locale].description}</p>
    </div>
  )
}
```

---

## Translation Management

### Using Translation Service (Lokalise, Crowdin)

```typescript
// scripts/sync-translations.ts

async function syncTranslations() {
  // Download translations from service
  const response = await fetch('https://api.lokalise.com/api2/projects/PROJECT_ID/files/download', {
    headers: {
      'X-Api-Token': process.env.LOKALISE_API_KEY!
    }
  })

  const data = await response.json()

  // Save to messages folder
  await fs.writeFile('./messages/en.json', JSON.stringify(data.en, null, 2))

  console.log('Translations synced!')
}
```

---

## Missing Translation Handling

```typescript
// i18n/request.ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`../messages/${locale}.json`)).default,
  onError: error => {
    console.error('Translation error:', error)
  },
  getMessageFallback: ({ namespace, key, error }) => {
    return `${namespace}.${key}` // Show key if translation missing
  }
}))
```

---

## SEO for Multilingual Sites

```typescript
// app/[locale]/layout.tsx
import { useLocale } from 'next-intl'

export async function generateMetadata({ params: { locale } }) {
  const t = await useTranslations('metadata')

  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `/${locale}`,
      languages: {
        en: '/en',
        es: '/es',
        fr: '/fr',
        de: '/de',
        ja: '/ja'
      }
    }
  }
}
```

**HTML Output:**

```html
<link rel="canonical" href="https://example.com/en" />
<link rel="alternate" hreflang="en" href="https://example.com/en" />
<link rel="alternate" hreflang="es" href="https://example.com/es" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr" />
```

---

## When to Use Me

**Perfect for:**

- Building multilingual applications
- International product launches
- Global SaaS platforms
- E-commerce in multiple countries
- Content management systems

**I'll help you:**

- Set up i18n infrastructure
- Manage translations
- Format dates, numbers, currencies
- Handle RTL languages
- Optimize for SEO

## What I'll Create

```
🌍 Multi-Language Support
📅 Date/Time Formatting
💰 Currency Formatting
🔄 Language Switching
📝 Translation Management
🌐 RTL Support
```

Let's make your app globally accessible!
