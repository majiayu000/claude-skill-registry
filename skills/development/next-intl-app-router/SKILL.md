---
name: next-intl-app-router
description: Configures and uses next-intl for Next.js App Router with locale-based routing. Use when adding or changing i18n, locale routing, translations, next-intl plugin, middleware/proxy, or message files in Next.js App Router projects.
---

# next-intl (App Router)

Setup and usage of `next-intl` with **prefix-based locale routing** (e.g. `/en/about`, `/ja/about`). Use this skill in any Next.js App Router project.

**Example code:** Copy-paste examples live in this skill's [examples/](examples/) folder. See [examples/README.md](examples/README.md) for where each file goes in your project.

## File layout

Keep this structure:

```
├── messages/
│   ├── en.json
│   ├── ja.json
│   └── ...
├── next.config.ts
└── src/
    ├── i18n/
    │   ├── request.ts
    │   ├── routing.ts
    │   └── navigation.ts
    ├── proxy.ts          # Next.js 16+ (was middleware.ts)
    └── app/
        ├── layout.tsx    # Root layout, no NextIntlClientProvider here
        └── [locale]/
            ├── layout.tsx
            ├── page.tsx
            └── ...
```

Root layout does **not** wrap with `NextIntlClientProvider`; only `app/[locale]/layout.tsx` does.

---

## 1. Next config

Wire the plugin (default path `./i18n/request.ts`):

```ts
// next.config.ts
import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const nextConfig: NextConfig = {
  /* ... */
};
const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
```

Custom path: `createNextIntlPlugin('./src/i18n/request.ts')`.

---

## 2. Routing config

Central config in `src/i18n/routing.ts`:

```ts
import { defineRouting } from "next-intl/routing";

export const routing = defineRouting({
  locales: ["en", "ja", "zh-CN", "zh-TW"],
  defaultLocale: "en",
});
```

---

## 3. Request config

`src/i18n/request.ts`: resolve locale from the `[locale]` segment and load messages.

```ts
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

---

## 4. Proxy / middleware (Next.js 16)

Next.js 16 uses `proxy.ts` instead of `middleware.ts`. Same API:

```ts
// src/proxy.ts
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export const proxy = createMiddleware(routing);

export const config = {
  matcher: "/((?!api|trpc|_next|_vercel|.*\\..*).*)",
};
```

Matcher: all pathnames except `/api`, `/trpc`, `/_next`, `/_vercel`, and paths containing a dot (e.g. `favicon.ico`).

---

## 5. Navigation helpers

Use project navigation wrappers so links keep the current locale:

```ts
// src/i18n/navigation.ts
import { createNavigation } from "next-intl/navigation";
import { routing } from "./routing";

export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
```

In components: import `Link` (and others) from `@/i18n/navigation`, **not** from `next/navigation` or `next/link`, for locale-aware URLs. Example: [examples/Nav-client.tsx](examples/Nav-client.tsx), [examples/BackToHomeButton.tsx](examples/BackToHomeButton.tsx).

---

## 6. Locale layout and static rendering

`app/[locale]/layout.tsx` must (full file: [examples/app-locale-layout.tsx](examples/app-locale-layout.tsx)):

1. Validate `locale` with `hasLocale` → `notFound()` if invalid.
2. Call `setRequestLocale(locale)` for static rendering.
3. Wrap children with `NextIntlClientProvider` and `getMessages()`.

```tsx
// app/[locale]/layout.tsx
import { NextIntlClientProvider, hasLocale } from "next-intl";
import { setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";
import { getMessages } from "next-intl/server";

type Props = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();

  setRequestLocale(locale);
  const messages = await getMessages();

  return (
    <NextIntlClientProvider messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
```

---

## 7. Pages under `[locale]`

For static rendering, every **page** under `[locale]` that uses next-intl must call `setRequestLocale(locale)` (and use `use(params)` if needed). Examples: [app-locale-page.tsx](examples/app-locale-page.tsx), [app-locale-about-page.tsx](examples/app-locale-about-page.tsx). (and use `use(params)` if needed). Layout already sets it; pages that render server components using locale should set it too.

```tsx
// app/[locale]/page.tsx
import { use } from "react";
import { setRequestLocale } from "next-intl/server";

export default function IndexPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  setRequestLocale(locale);
  return <TokyoPage />;
}
```

```tsx
// app/[locale]/about/page.tsx
import { use } from "react";
import { setRequestLocale } from "next-intl/server";
import AboutContainer from "./components/AboutContainer";

export default function AboutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  setRequestLocale(locale);
  return <AboutContainer />;
}
```

Call `setRequestLocale` **before** any `next-intl` APIs in that layout/page.

---

## 8. Using translations

**Client components:** `useTranslations(namespace)`:

```tsx
"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export default function BackToHomeButton() {
  const t = useTranslations("BackToHomeButton");
  return (
    <Link href="/">
      <span>{t("buttonText")}</span>
    </Link>
  );
}
```

```tsx
"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export default function Nav() {
  const t = useTranslations("Navigation");
  return <Link href="/about">{t("links.about")}</Link>;
}
```

**Server components:** use `getTranslations` from `next-intl/server` (await with locale/namespace as needed).

---

## 9. Messages format

One JSON file per locale under `messages/`. Nested keys map to namespaces and keys:

```json
{
  "HomePage": {
    "title": "Hello world!"
  },
  "LandingPage": {
    "title": "Tokyo Sounds",
    "navbar": {
      "home": "Home",
      "about": "About"
    }
  },
  "BackToHomeButton": {
    "buttonText": "Back to Home",
    "tooltip": "Return to the main page"
  }
}
```

- `useTranslations("LandingPage")` → `t("title")`, `t("navbar.about")`.
- Interpolation: `"selectColor": "Select {color} color"` → `t("selectColor", { color: "Blue" })`.

---

## Checklist

- [ ] `next.config.ts`: `createNextIntlPlugin()` wraps config.
- [ ] `src/i18n/routing.ts`: `defineRouting` with `locales` and `defaultLocale`.
- [ ] `src/i18n/request.ts`: `getRequestConfig` + `hasLocale` + dynamic `messages/${locale}.json`.
- [ ] `src/proxy.ts` (or `middleware.ts`): `createMiddleware(routing)` and matcher.
- [ ] `src/i18n/navigation.ts`: `createNavigation(routing)` and re-export `Link`, etc.
- [ ] `app/[locale]/layout.tsx`: `hasLocale` → `notFound`, `setRequestLocale`, `generateStaticParams`, `NextIntlClientProvider` + `getMessages()`.
- [ ] Each `app/[locale]/**/page.tsx`: `setRequestLocale(locale)` when using static rendering.
- [ ] Client components: `useTranslations("Namespace")`; links use `Link` from `@/i18n/navigation`.

---

## Reference

- **Copy-paste examples:** [examples/](examples/) — standalone files for use in any project.
- Extended config (localePrefix, pathnames, etc.): [reference.md](reference.md)
- Official: [next-intl App Router](https://next-intl.dev/docs/getting-started/app-router), [Routing setup](https://next-intl.dev/docs/routing/setup)
