---
name: web-i18n
description: (ePost) Use when working with translations, locale routing, next-intl configuration, or internationalization patterns
user-invocable: false

metadata:
  agent-affinity: [epost-fullstack-developer]
  keywords: [i18n, translation, locale, next-intl, internationalization, language]
  platforms: [web]
  triggers: ["translation", "locale", "i18n", "useTranslations", "getTranslations", "next-intl"]
---

# Internationalization — next-intl Patterns

## Purpose

next-intl configuration and translation patterns for Next.js App Router applications. Covers locale setup, server/client usage, navigation re-exports, and translation file structure.

## Configuration

### Supported Locales

```typescript
export const locales = ['en', ...]; // add your supported locales
export const defaultLocale = 'en';  // configure your default locale
```

### i18n.ts

```typescript
// i18n.ts
import { getRequestConfig } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { locales } from './middleware';

export default getRequestConfig(async ({ locale }) => {
  if (!locales.includes(locale as any)) notFound();
  return {
    messages: (await import(`./messages/${locale}.json`)).default,
  };
});
```

### navigation.ts — ALWAYS Import From Here

```typescript
// navigation.ts
import { createSharedPathnamesNavigation } from 'next-intl/navigation';

export const locales = ['en', ...]; // match your supported locales

export const { Link, redirect, usePathname, useRouter } =
  createSharedPathnamesNavigation({ locales });
```

**Import `Link`, `redirect`, `usePathname`, `useRouter` from `navigation.ts`** — NOT from `next/link` or `next/navigation`.

## Translation Usage

### Server Components (layouts, pages, generateMetadata)

```typescript
import { getTranslations } from 'next-intl/server';

// In generateMetadata
export const generateMetadata = async (): Promise<Metadata> => {
  const t = await getTranslations('FeatureName');
  return { title: t('title') + ' - MyApp' };
};

// In Server Component body
export default async function Layout({ children }) {
  const t = await getTranslations('MainPage');
  return <SidebarMenu label={t('dashboard')} />;
}
```

### Client Components

```typescript
'use client';
import { useTranslations } from 'next-intl';

export function FeatureCard() {
  const t = useTranslations('FeatureName.Dashboard');
  const tToast = useTranslations('FeatureName.ToastMessage');
  const tBtn = useTranslations('FeatureName.Button');

  return <Button label={tBtn('submit')} />;
}
```

### Message Injection (Root Layout)

```typescript
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

const messages = await getMessages();
// ...
<NextIntlClientProvider messages={messages}>
  {children}
</NextIntlClientProvider>
```

## Translation Files

**Location**: `messages/` directory — one flat JSON file per locale.

```
messages/
├── en.json
├── de.json
├── fr.json
└── ...
```

### Namespace Structure

```json
{
  "MainPage": { "dashboard": "Dashboard", "featureA": "Feature A" },
  "Dashboard": { "title": "Hello", "selectProfile": "Select profile" },
  "Button": { "search": "Search", "reloadPage": "Reload page" },
  "Error": { "somethingWentWrong": "Something went wrong" },
  "FeatureName": {
    "title": "Feature Name",
    "Table": { "recipient": "Recipient", "status": "Status" },
    "DetailPanel": { "Info": { "title": "Info" } }
  },
  "AnotherFeature": {
    "Dashboard": { "title": "Another Feature" },
    "ToastMessage": { "success": "Action completed" },
    "Button": { "submit": "Submit" }
  }
}
```

### Nested Namespace Access

Use dot notation for nested namespaces:

```typescript
const t = useTranslations('FeatureName.Table');
t('recipient') // → "Recipient"

const tDetail = useTranslations('FeatureName.DetailPanel.Info');
tDetail('title') // → "Info"
```

## Adding New Translations

1. Add keys to all locale files (e.g., `en.json`, `de.json`, etc.)
2. Use a consistent namespace matching the feature/module name
3. Group related keys under a namespace object
4. Use `getTranslations('Namespace')` (server) or `useTranslations('Namespace')` (client)

## Rules

- Import navigation helpers (`Link`, `redirect`, `useRouter`, `usePathname`) from `navigation.ts` — never from `next/link` or `next/navigation`
- Always add translations to ALL locale files
- Use `getTranslations` in Server Components, `useTranslations` in Client Components
- Use dot notation for nested namespace access
- Configure your default locale appropriately for your primary user base
