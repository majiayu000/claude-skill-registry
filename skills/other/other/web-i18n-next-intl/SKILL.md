---
name: web-i18n-next-intl
description: Type-safe i18n for Next.js App Router
---

# next-intl Internationalization Patterns

> **Quick Guide:** Use next-intl for type-safe internationalization in Next.js App Router. `useTranslations` for messages, `useFormatter` for dates/numbers, middleware for locale detection. Call `setRequestLocale(locale)` for static rendering.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `setRequestLocale(locale)` at the top of ALL page/layout components for static rendering)**

**(You MUST validate locale against `routing.locales` before using it)**

**(You MUST use `NextIntlClientProvider` in the root layout to enable client-side hooks)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

</critical_requirements>

---

**Auto-detection:** next-intl, useTranslations, useFormatter, useLocale, NextIntlClientProvider, i18n routing, locale detection, ICU message format

**When to use:**

- Implementing internationalization in Next.js App Router
- Rendering localized messages with interpolation and pluralization
- Formatting dates, numbers, and relative time per locale
- Setting up locale-based routing and middleware
- Generating static pages for multiple locales

**Key patterns covered:**

- Project setup with routing.ts, request.ts, and middleware
- useTranslations hook for messages with ICU syntax
- useFormatter hook for dates, numbers, and lists
- Static rendering with generateStaticParams and setRequestLocale
- TypeScript integration for type-safe translation keys

**When NOT to use:**

- Simple single-locale applications (skip i18n complexity)
- Pages Router (different API - use Pages Router docs)
- Non-Next.js React applications (use react-intl instead)

**Detailed Resources:**

- For code examples, see [examples/](examples/) (core.md, formatting.md, pluralization.md, markup.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

next-intl follows the principle of **type-safe, locale-aware rendering** with ICU message format support. Translations are organized as namespaced JSON objects, loaded per-request for Server Components and provided via context for Client Components. The middleware handles locale detection automatically, while `setRequestLocale` enables static rendering at build time.

**Core principles:**

1. **Server-first**: Load translations in Server Components for better performance
2. **Type-safe keys**: TypeScript augmentation catches missing translations at compile time
3. **ICU standard**: Use industry-standard ICU message syntax for pluralization and formatting
4. **Static-friendly**: Support static generation with explicit locale parameters

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Project Setup

Set up next-intl with the App Router using the standard file structure.

#### File Structure

```
src/
  i18n/
    routing.ts       # Locale configuration
    request.ts       # Server-side locale resolution
    navigation.ts    # Locale-aware Link, useRouter
  proxy.ts           # Locale detection and routing (middleware.ts before Next.js 16)
  app/
    [locale]/
      layout.tsx     # Root layout with NextIntlClientProvider
      page.tsx       # Pages within locale segment
messages/
  en.json            # English translations
  de.json            # German translations
```

> **Note:** In Next.js 16+, `middleware.ts` was renamed to `proxy.ts`. If using Next.js 15 or earlier, use `middleware.ts`.

#### Configuration Files

```typescript
// src/i18n/routing.ts
import { defineRouting } from "next-intl/routing";

export const SUPPORTED_LOCALES = ["en", "de", "fr"] as const;
export const DEFAULT_LOCALE = "en";

export const routing = defineRouting({
  locales: SUPPORTED_LOCALES,
  defaultLocale: DEFAULT_LOCALE,
});

export type Locale = (typeof routing.locales)[number];
```

**Why good:** named constants for locales enable type-safe usage throughout app, exported Locale type enables type checking of locale parameters

```typescript
// src/i18n/request.ts
import { getRequestConfig } from "next-intl/server";
import { hasLocale } from "next-intl";
import { routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  const locale = hasLocale(routing.locales, requested)
    ? requested
    : routing.defaultLocale;

  return {
    locale,
    messages: (await import(`../../messages/${locale}.json`)).default,
  };
});
```

**Why good:** validates locale against supported list, falls back to default for invalid locales, dynamically imports only needed translation file

```typescript
// src/i18n/navigation.ts
import { createNavigation } from "next-intl/navigation";
import { routing } from "./routing";

export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
```

**Why good:** wraps Next.js navigation APIs with locale awareness, Link automatically includes locale prefix

```typescript
// src/proxy.ts (Next.js 16+) or src/middleware.ts (Next.js 15 and earlier)
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  matcher: "/((?!api|trpc|_next|_vercel|.*\\..*).*)",
};
```

**Why good:** proxy/middleware handles locale detection from URL, cookies, and Accept-Language header, matcher excludes API routes, tRPC routes, and static files

---

### Pattern 2: Root Layout with Provider

Wrap the application with NextIntlClientProvider and validate the locale.

```typescript
// src/app/[locale]/layout.tsx
import { NextIntlClientProvider, hasLocale } from "next-intl";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";
import { routing, type Locale } from "@/i18n/routing";

type Props = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;

  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }

  setRequestLocale(locale);

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
```

**Why good:** validates locale and returns 404 for invalid locales, setRequestLocale enables static rendering, generateStaticParams pre-renders all locale variants, html lang attribute improves accessibility

---

### Pattern 3: useTranslations Hook

Use the useTranslations hook for rendering localized messages.

#### Basic Usage

```typescript
// src/app/[locale]/about/page.tsx
import { useTranslations } from "next-intl";
import { setRequestLocale } from "next-intl/server";

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function AboutPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  const t = useTranslations("About");

  return (
    <article>
      <h1>{t("title")}</h1>
      <p>{t("description")}</p>
    </article>
  );
}
```

```json
// messages/en.json
{
  "About": {
    "title": "About Us",
    "description": "Learn more about our company."
  }
}
```

**Why good:** namespaced translations keep messages organized, setRequestLocale at top of component enables static rendering

#### With Interpolation

```typescript
const t = useTranslations("Profile");

// Message: "Hello, {name}!"
t("greeting", { name: user.name }); // "Hello, Jane!"

// Message: "You have {count} unread messages"
t("unreadCount", { count: messages.length }); // "You have 5 unread messages"
```

**Why good:** named placeholders are explicit and refactorable, TypeScript can validate placeholder names with augmentation

---

### Pattern 4: Pluralization with ICU Syntax

Use ICU plural syntax for count-based messages.

```typescript
const t = useTranslations("Notifications");

// Renders correct plural form based on locale rules
t("itemCount", { count: items.length });
```

```json
// messages/en.json
{
  "Notifications": {
    "itemCount": "{count, plural, =0 {No items} one {# item} other {# items}}"
  }
}
```

**Plural categories by language:**

- English: `one`, `other`
- Russian: `one`, `few`, `many`, `other`
- Arabic: `zero`, `one`, `two`, `few`, `many`, `other`

**Why good:** ICU plural syntax handles locale-specific plural rules automatically, `#` is replaced with the formatted count

#### Ordinal Pluralization

```typescript
// Message: "It's your {year, selectordinal, one {#st} two {#nd} few {#rd} other {#th}} birthday!"
t("birthday", { year: 21 }); // "It's your 21st birthday!"
```

---

### Pattern 5: Rich Text Formatting

Use `t.rich()` for messages containing markup.

```typescript
const t = useTranslations("Legal");

const content = t.rich("terms", {
  link: (chunks) => <a href="/terms">{chunks}</a>,
  bold: (chunks) => <strong>{chunks}</strong>,
});

return <p>{content}</p>;
```

```json
{
  "Legal": {
    "terms": "By signing up, you agree to our <link>Terms of Service</link> and <bold>Privacy Policy</bold>."
  }
}
```

**Why good:** keeps translation strings complete and translatable, markup tags are defined by developers and can be React components

---

### Pattern 6: useFormatter Hook

Use useFormatter for locale-aware formatting of dates, numbers, and lists.

#### Date and Time Formatting

```typescript
import { useFormatter } from "next-intl";

function EventDate({ date }: { date: Date }) {
  const format = useFormatter();

  return (
    <time dateTime={date.toISOString()}>
      {format.dateTime(date, {
        year: "numeric",
        month: "long",
        day: "numeric",
      })}
    </time>
  );
}
```

**Why good:** uses Intl.DateTimeFormat under the hood, respects locale-specific date formats automatically

#### Relative Time with useNow

```typescript
import { useFormatter, useNow } from "next-intl";

const UPDATE_INTERVAL_MS = 60000;

function RelativeTime({ date }: { date: Date }) {
  const format = useFormatter();
  const now = useNow({ updateInterval: UPDATE_INTERVAL_MS });

  return <time>{format.relativeTime(date, now)}</time>;
}
```

**Why good:** useNow provides a reactive "now" value that updates on interval, relative time updates automatically

#### Number and Currency Formatting

```typescript
import { useFormatter } from "next-intl";

function Price({ amount, currency }: { amount: number; currency: string }) {
  const format = useFormatter();

  return (
    <span>
      {format.number(amount, {
        style: "currency",
        currency,
      })}
    </span>
  );
}
```

**Why good:** handles locale-specific number formatting (1,234.56 vs 1.234,56), currency symbols and positions vary by locale

---

### Pattern 7: Static Rendering with generateStaticParams

Enable static generation for all locale variants.

```typescript
// src/app/[locale]/blog/[slug]/page.tsx
import { setRequestLocale } from "next-intl/server";
import { routing } from "@/i18n/routing";

type Props = {
  params: Promise<{ locale: string; slug: string }>;
};

export function generateStaticParams() {
  const slugs = ["getting-started", "advanced-features", "faq"];

  return routing.locales.flatMap((locale) =>
    slugs.map((slug) => ({ locale, slug })),
  );
}

export default async function BlogPost({ params }: Props) {
  const { locale, slug } = await params;
  setRequestLocale(locale);

  // Component implementation
}
```

**Why good:** generates all combinations of locales and slugs at build time, setRequestLocale enables next-intl to work in static context

---

### Pattern 8: Locale Switching

Implement a locale switcher component using next-intl navigation.

```typescript
"use client";

import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/navigation";
import { routing, type Locale } from "@/i18n/routing";

const LOCALE_LABELS: Record<Locale, string> = {
  en: "English",
  de: "Deutsch",
  fr: "Francais",
};

export function LocaleSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const handleChange = (newLocale: Locale) => {
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <select
      value={locale}
      onChange={(e) => handleChange(e.target.value as Locale)}
      aria-label="Select language"
    >
      {routing.locales.map((loc) => (
        <option key={loc} value={loc}>
          {LOCALE_LABELS[loc]}
        </option>
      ))}
    </select>
  );
}
```

**Why good:** uses next-intl navigation APIs to preserve current path, aria-label provides accessibility, type-safe locale handling

---

### Pattern 9: TypeScript Integration

Enable type-safe translation keys with TypeScript augmentation using the `AppConfig` interface (next-intl v4.0+).

#### Configuration

```typescript
// src/i18n/types.ts (or global.d.ts)
import type en from "../../messages/en.json";
import { routing } from "./routing";
import type { formats } from "./request";

declare module "next-intl" {
  interface AppConfig {
    Locale: (typeof routing.locales)[number];
    Messages: typeof en;
    Formats: typeof formats;
  }
}
```

```json
// tsconfig.json (add to compilerOptions)
{
  "compilerOptions": {
    "allowArbitraryExtensions": true
  }
}
```

**Why good:** typos in translation keys become compile-time errors, IDE autocomplete for translation keys, strictly-typed locales prevent invalid locale strings, Formats registration enables type-safe formatting

#### Optional: Type-Safe Message Arguments (Experimental)

For automatic type inference of ICU message arguments, configure `createMessagesDeclaration`:

```typescript
// next.config.mjs
import { createNextIntlPlugin } from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin({
  experimental: {
    createMessagesDeclaration: "./messages/en.json",
  },
});

export default withNextIntl({});
```

This generates type declarations enabling autocomplete for message arguments like `{name}` or `{count, plural, ...}`.

---

### Pattern 10: Server Actions and Metadata

Use async getTranslations for Server Actions and Metadata.

```typescript
// src/app/[locale]/page.tsx
import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "Metadata" });

  return {
    title: t("title"),
    description: t("description"),
  };
}

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  const t = await getTranslations("Home");

  return <h1>{t("welcome")}</h1>;
}
```

**Why good:** getTranslations works in async contexts like generateMetadata, locale parameter is required for metadata since it runs outside component tree

</patterns>

---

<integration>

## Integration Guide

**next-intl is routing and rendering-aware.** It integrates with Next.js App Router patterns for SSR, SSG, and client-side navigation.

**Works with:**

- **Next.js App Router**: Designed specifically for App Router with Server Components support
- **Next.js Metadata API**: Use getTranslations in generateMetadata for localized SEO
- **Next.js Static Generation**: generateStaticParams + setRequestLocale enables SSG

**Component State Guidance:**

- Use Server Components for initial translation loading (better performance)
- Use Client Components with NextIntlClientProvider for interactive locale switching
- Locale state is managed by next-intl - use useLocale() to read it

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `setRequestLocale(locale)` at the top of ALL page/layout components for static rendering)**

**(You MUST validate locale against `routing.locales` before using it)**

**(You MUST use `NextIntlClientProvider` in the root layout to enable client-side hooks)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**Failure to follow these rules will break static generation and cause runtime errors with invalid locales.**

</critical_reminders>
